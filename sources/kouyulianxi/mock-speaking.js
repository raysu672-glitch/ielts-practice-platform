// 口语模考（Mock Speaking）
// 流程：P1(前奏话题组 + 当季话题组) → P2(准备+陈述) → P3(4题) → 上传 → 报告
// 全场连续录音，混录系统题目声
// 「一组话题」= 同一 topicEn（如 Hometown）下的若干小问，对齐真考/同桌题库

const MOCK_P1_WARMUP_TOPICS = new Set([
    'Work or studies',
    'Hometown',
    'Home & Accommodation',
    'The area you live in',
    'The city you live in'
]);
const MOCK_P1_WARMUP_PRIMARY = new Set([
    'Work or studies',
    'Hometown',
    'Home & Accommodation'
]);
const MOCK_P1_PER_TOPIC = 4; // 每组抽至多 4 题，优先高热
const MOCK_P1_MIN_TOPIC_SIZE = 3;

class MockSpeakingExam {
    constructor() {
        this.config = window.MOCK_SPEAKING_CONFIG || {};
        this.data = { p1: null, p2: null, p3: null };
        this.state = 'idle'; // idle → preparing → p1_qN → p2_prep → p2_talk → p3_qN → uploading → report
        this.examId = null;
        this.startedAt = 0;
        this.segments = []; // { part, qid, startMs, endMs, transcript, score }
        this.currentSegment = null;

        // 录音相关
        this.audioCtx = null;
        this.micStream = null;
        this.micSource = null;
        this.systemGain = null; // 题目声增益
        this.mixDest = null;
        this.recorder = null;
        this.recordedChunks = [];
        this.recordStartTs = 0;

        // 计时
        this.tickTimer = null;
        this.deadlineTs = 0;
        this.partTimeLeft = 0; // 当前 part 剩余秒

        // DOM
        this.el = {};
        this.bindDom();

        // 题库
        this.p1Questions = [];
        this.p2Card = null;
        this.p3Questions = [];

        this.init();
    }

    bindDom() {
        const ids = [
            'mockStartOverlay', 'mockExamView', 'mockReportView',
            'mockPhaseLabel', 'mockTimer', 'mockQuestionText', 'mockCueCard',
            'mockTip', 'mockProgress', 'mockRecordDot', 'mockSilenceHint',
            'mockStartBtn', 'mockAbortBtn', 'mockNextBtn',
            'mockReportBody', 'mockDownloadAudioBtn', 'mockBackBtn',
            'mockMicCheck', 'mockMicStatus'
        ];
        ids.forEach(id => { this.el[id] = document.getElementById(id); });
    }

    async init() {
        this.renderStart();
        this.bindEvents();
        // 等数据脚本加载完再抽题
        let tries = 0;
        while (tries < 20) {
            try {
                await this.pickQuestions();
                if (this.p1Questions.length && this.p2Card && this.p3Questions.length) {
                    break;
                }
            } catch (e) {
                console.warn('pickQuestions 第', tries + 1, '次失败', e);
            }
            tries += 1;
            await new Promise(r => setTimeout(r, 200));
        }
        if (!this.p1Questions.length || !this.p2Card || !this.p3Questions.length) {
            this.el.mockMicStatus.textContent = '题库加载失败，请刷新';
            return;
        }
        this.el.mockMicStatus.textContent = '题库已加载，检测麦克风…';
        // 自动检测麦克风
        setTimeout(() => this.checkMic(), 300);
    }

    /* ---------- 按 topicEn 归组 ---------- */
    groupP1ByTopic(p1Data) {
        const map = new Map();
        for (const cat of (p1Data && p1Data.categories) || []) {
            for (const q of (cat && cat.questions) || []) {
                const key = (q.topicEn || '').trim() || 'Unknown';
                if (!map.has(key)) {
                    map.set(key, {
                        topicEn: key,
                        topicZh: q.topicZh || key,
                        questions: []
                    });
                }
                const g = map.get(key);
                if (!g.topicZh && q.topicZh) g.topicZh = q.topicZh;
                g.questions.push(q);
            }
        }
        return [...map.values()];
    }

    pickQsFromTopic(topic, count) {
        const available = (topic.questions || []).length;
        const n = Math.min(count, available);
        return [...(topic.questions || [])]
            .sort((a, b) => (b.recentCount || 0) - (a.recentCount || 0))
            .slice(0, n);
    }

    topicHeat(topic) {
        return (topic.questions || []).reduce((s, q) => s + (q.recentCount || 0), 0);
    }

    pickRandom(list) {
        if (!list || !list.length) return null;
        return list[Math.floor(Math.random() * list.length)];
    }

    /* ---------- 抽题 ---------- */
    async pickQuestions() {
        // p1/p2 用 const 声明；兼容 window 挂载与同页全局词法
        const p1Data = (typeof P1_DATA !== 'undefined' ? P1_DATA : null) || window.P1_DATA;
        const p2Data = (typeof P2_DATA !== 'undefined' ? P2_DATA : null) || window.P2_DATA;
        const p3Data = (typeof P3_DATA !== 'undefined' ? P3_DATA : null) || window.P3_DATA;

        // P1：1 组前奏必考话题 + 1 组当季话题（按 topicEn，对齐同桌/真考）
        const groups = this.groupP1ByTopic(p1Data)
            .filter(g => (g.questions || []).length >= MOCK_P1_MIN_TOPIC_SIZE);
        if (!groups.length) {
            throw new Error('P1 题库为空或未加载');
        }
        const warmups = groups.filter(g => MOCK_P1_WARMUP_PRIMARY.has(g.topicEn));
        const seasonals = groups.filter(g => !MOCK_P1_WARMUP_TOPICS.has(g.topicEn));
        const warmup = this.pickRandom(warmups.length ? warmups : groups.filter(g => MOCK_P1_WARMUP_TOPICS.has(g.topicEn)));
        const seasonalPool = seasonals.length
            ? seasonals
            : groups.filter(g => g.topicEn !== (warmup && warmup.topicEn));
        // 当季话题：高热优先，再在前半里随机，避免永远抽同一组
        const seasonalSorted = [...seasonalPool].sort((a, b) => this.topicHeat(b) - this.topicHeat(a));
        const seasonalTop = seasonalSorted.slice(0, Math.max(6, Math.ceil(seasonalSorted.length / 2)));
        let seasonal = this.pickRandom(seasonalTop);
        if (!seasonal || seasonal.topicEn === warmup.topicEn) {
            seasonal = seasonalSorted.find(g => g.topicEn !== warmup.topicEn) || null;
        }
        if (!warmup) {
            throw new Error('P1 前奏话题组不足');
        }
        if (!seasonal) {
            throw new Error('P1 当季话题组不足');
        }

        const warmQs = this.pickQsFromTopic(warmup, MOCK_P1_PER_TOPIC);
        const seasonQs = this.pickQsFromTopic(seasonal, MOCK_P1_PER_TOPIC);
        const qs = [...warmQs, ...seasonQs];
        this.data.p1 = {
            mode: 'topicGroups',
            frames: [
                { topicEn: warmup.topicEn, topicZh: warmup.topicZh, count: warmQs.length },
                { topicEn: seasonal.topicEn, topicZh: seasonal.topicZh, count: seasonQs.length }
            ],
            questions: qs
        };

        // P2：按 heatRank 抽 1 张卡
        const p2qs = (p2Data && p2Data.questions) || [];
        if (!p2qs.length) {
            throw new Error('P2 题库为空或未加载');
        }
        const p2Top = [...p2qs].sort((a, b) => (a.heatRank || 99) - (b.heatRank || 99)).slice(0, 12);
        const p2 = this.pickRandom(p2Top);
        if (!p2) {
            throw new Error('P2 随机选题失败');
        }
        this.data.p2 = p2;

        // P3：找 relatedP2Title 与 P2 title 相同/相近的 topic；否则按 heatRank 取第一
        const p3Topics = (p3Data && p3Data.topics) || [];
        if (!p3Topics.length) {
            throw new Error('P3 题库为空或未加载');
        }
        let topic = p3Topics.find(t => (t.relatedP2Title || '') === (p2 && p2.title));
        if (!topic) {
            topic = [...p3Topics].sort((a, b) => (a.heatRank || 99) - (b.heatRank || 99))[0];
        }
        if (!topic || !Array.isArray(topic.questions)) {
            throw new Error('P3 选题失败');
        }
        const p3qs = topic.questions.slice(0, 4);
        this.data.p3 = { topic: topic.titleZh || topic.titleEn || topic.title, questions: p3qs };

        // 打平成题序
        this.p1Questions = this.data.p1.questions.map((q, i) => ({ part: 'p1', idx: i + 1, ...q }));
        this.p2Card = this.data.p2;
        this.p3Questions = this.data.p3.questions.map((q, i) => ({ part: 'p3', idx: i + 1, ...q }));
    }

    /* ---------- 起始页 ---------- */
    renderStart() {
        this.el.mockStartOverlay.style.display = 'flex';
        this.el.mockStartOverlay.classList.remove('mock-hidden');
        this.el.mockExamView.classList.add('mock-hidden');
        this.el.mockExamView.style.display = 'none';
        this.el.mockReportView.classList.add('mock-hidden');
        this.el.mockReportView.style.display = 'none';
        this.el.mockMicStatus.textContent = '待检测';
        this.el.mockStartBtn.disabled = true;
    }

    bindEvents() {
        this.el.mockStartBtn.addEventListener('click', () => this.startExam());
        this.el.mockAbortBtn.addEventListener('click', () => this.abortExam());
        this.el.mockNextBtn.addEventListener('click', () => this.nextStep());
        this.el.mockBackBtn.addEventListener('click', () => {
            window.location.href = '/jianyazhenti/student/mock?embed=1';
        });
        this.el.mockDownloadAudioBtn.addEventListener('click', () => this.downloadAudio());
        window.addEventListener('beforeunload', (e) => {
            if (this.state !== 'idle' && this.state !== 'report') {
                e.preventDefault();
                e.returnValue = '';
            }
        });
    }

    /* ---------- 麦克风检测 ---------- */
    async checkMic() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(t => t.stop());
            this.el.mockMicStatus.textContent = '✅ 正常';
            this.el.mockStartBtn.disabled = false;
        } catch (e) {
            this.el.mockMicStatus.textContent = '❌ 无法访问麦克风';
            alert('请允许浏览器使用麦克风后再开始模考');
        }
    }

    /* ---------- 开考 ---------- */
    async startExam() {
        if (this.el.mockStartBtn.disabled) return;
        this.el.mockStartBtn.disabled = true;
        try {
            if (!this.p1Questions.length || !this.p2Card || !this.p3Questions.length) {
                throw new Error('题库未加载完成，请刷新页面重试');
            }
            this.el.mockStartOverlay.style.display = 'none';
            this.el.mockStartOverlay.classList.add('mock-hidden');
            this.el.mockExamView.classList.remove('mock-hidden');
            this.el.mockExamView.style.display = 'flex';
            this.el.mockExamView.style.flexDirection = 'column';
            this.startedAt = Date.now();
            this.state = 'preparing';

            await this.setupRecording();
            await this.createServerExam();

            // 进入 P1 第 1 题
            this.runP1Question(0);
        } catch (e) {
            console.error('开始模考失败', e);
            alert('开始失败：' + (e && e.message ? e.message : '未知错误'));
            this.el.mockStartOverlay.classList.remove('mock-hidden');
            this.el.mockStartOverlay.style.display = 'flex';
            this.el.mockExamView.classList.add('mock-hidden');
            this.el.mockExamView.style.display = 'none';
            this.el.mockStartBtn.disabled = false;
        }
    }

    async setupRecording() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('当前浏览器不支持麦克风访问');
        }
        this.micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        // 混音目标：麦克风 + 系统声
        this.mixDest = this.audioCtx.createMediaStreamDestination();

        // 麦克风
        this.micSource = this.audioCtx.createMediaStreamSource(this.micStream);
        this.micSource.connect(this.mixDest);

        // 系统题目声增益节点（播放 TTS/mp3 时接入）
        this.systemGain = this.audioCtx.createGain();
        this.systemGain.gain.value = 1.0;
        this.systemGain.connect(this.mixDest);

        // 录音器
        const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
            ? 'audio/webm;codecs=opus'
            : (MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : '');
        this.recorder = new MediaRecorder(this.mixDest.stream, mimeType ? { mimeType } : undefined);
        this.recordedChunks = [];
        this.recorder.ondataavailable = (e) => {
            if (e.data && e.data.size) this.recordedChunks.push(e.data);
        };
        this.recorder.start(1000);
        this.recordStartTs = Date.now();
        this.el.mockRecordDot.classList.add('recording');
    }

    async createServerExam() {
        try {
            const res = await fetch(`${this.config.examApiBase}/start`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    p1: this.data.p1,
                    p2: this.data.p2,
                    p3: this.data.p3,
                    started_at: new Date(this.startedAt).toISOString()
                })
            });
            const data = await res.json();
            if (data && data.data && data.data.exam_id) {
                this.examId = data.data.exam_id;
            }
        } catch (e) {
            console.warn('创建模考记录失败，继续本地进行', e);
        }
    }

    /* ---------- 播放题目声（并混录） ---------- */
    async speakQuestion(text) {
        if (!text) return;
        return new Promise((resolve) => {
            const done = () => resolve();
            // 把 <audio> 元素输出接入 AudioContext，这样题目声会录进 mixDest
            const speakWithOnlineTts = () => {
                try {
                    const url = 'https://dict.youdao.com/dictvoice?type=2&audio=' + encodeURIComponent(text);
                    const audio = new Audio();
                    this._ttsAudio = audio;
                    audio.crossOrigin = 'anonymous';
                    audio.preload = 'auto';
                    // 关键：接入混音节点；CORS 失败会抛错，回退浏览器 TTS
                    if (this.audioCtx && this.systemGain) {
                        try {
                            const source = this.audioCtx.createMediaElementSource(audio);
                            source.connect(this.systemGain);
                            source.connect(this.audioCtx.destination); // 同时外放
                        } catch (e) {
                            console.warn('createMediaElementSource 失败，回退浏览器 TTS', e);
                            this.speakWithBrowserTts(text, done);
                            return;
                        }
                    }
                    audio.src = url;
                    audio.onended = done;
                    audio.onerror = () => {
                        this.speakWithBrowserTts(text, done);
                    };
                    audio.play().catch(() => {
                        this.speakWithBrowserTts(text, done);
                    });
                } catch (e) {
                    this.speakWithBrowserTts(text, done);
                }
            };
            speakWithOnlineTts();
        });
    }

    speakWithBrowserTts(text, done) {
        try {
            const utter = new SpeechSynthesisUtterance(text);
utter.lang = 'en-GB';
  utter.rate = 1.0;
            utter.onend = done;
            utter.onerror = done;
            speechSynthesis.speak(utter);
        } catch (e) {
            done();
        }
    }

    /* ---------- P1 ---------- */
    runP1Question(idx) {
        if (idx >= this.p1Questions.length) {
            this.runP2Prep();
            return;
        }
        this.stopSpeak();
        this.clearTick();
        this.state = `p1_q${idx + 1}`;
        const q = this.p1Questions[idx];
        this.currentSegment = {
            part: 'p1',
            qid: q.id,
            title: q.title,
            q: q.q,
            startMs: Date.now() - this.recordStartTs
        };

        this.el.mockPhaseLabel.textContent = `Part 1 · 第 ${idx + 1} / ${this.p1Questions.length} 题`;
        // 真考 Part 1：只听题，不显示文字
        this.el.mockQuestionText.textContent = '🎧 请听题，然后作答';
        this.el.mockCueCard.style.display = 'none';
        this.el.mockTip.textContent = '建议 20–30 秒作答，超时将自动进入下一题';
        this.el.mockNextBtn.textContent = '下一题';
        this.el.mockNextBtn.disabled = false;

        this.speakQuestion(q.q);

        // 单题 45 秒上限 → 自动下一题
        this.startCountdown(45, () => this.advanceFromCurrent(true), (left) => {
            this.el.mockTimer.textContent = `${left}s`;
            this.el.mockTimer.classList.toggle('warn', left <= 10);
        });

        // P1 总时长 5 分钟硬顶
        if (idx === 0) {
            if (this._p1HardTimer) clearTimeout(this._p1HardTimer);
            this._p1HardTimer = setTimeout(() => {
                if (this.state.startsWith('p1_')) {
                    this.advanceToP2();
                }
            }, 5 * 60 * 1000);
        }
    }

    /* ---------- P2 ---------- */
    runP2Prep() {
        this.stopSpeak();
        this.clearTick();
        // 若仍有未收口的 P1 段，先收口
        this.finishSegment(false);
        this.state = 'p2_prep';
        const card = this.p2Card;
        this.el.mockPhaseLabel.textContent = 'Part 2 · 准备';
        this.el.mockQuestionText.textContent = '请查看题目卡片，准备 1 分钟';
        this.el.mockCueCard.style.display = 'block';
        this.el.mockCueCard.innerHTML = `
            <h3>${this.escape(card.title)}</h3>
            <p><strong>${this.escape(card.q)}</strong></p>
            <ul>${(card.cuePoints || []).map(p => `<li>${this.escape(p)}</li>`).join('')}</ul>
        `;
        this.el.mockTip.textContent = '1 分钟准备，可以做笔记；时间到自动开始陈述';
        this.el.mockNextBtn.textContent = '跳过准备，直接开始';
        this.el.mockNextBtn.disabled = false;
        this.startCountdown(60, () => this.runP2Talk(), (left) => {
            this.el.mockTimer.textContent = `准备 ${left}s`;
            this.el.mockTimer.classList.toggle('warn', left <= 10);
        });
    }

    runP2Talk() {
        this.stopSpeak();
        this.clearTick();
        this.state = 'p2_talk';
        this.currentSegment = {
            part: 'p2',
            qid: this.p2Card.id,
            title: this.p2Card.title,
            q: this.p2Card.q,
            startMs: Date.now() - this.recordStartTs
        };
        this.el.mockPhaseLabel.textContent = 'Part 2 · 陈述';
        this.el.mockQuestionText.textContent = '请开始陈述（卡片可继续参考）';
        this.el.mockCueCard.style.display = 'block';
        this.el.mockTip.textContent = '请说满 1–2 分钟；少于 90 秒总分封顶 5.5，到 2 分钟自动进入 Part 3';
        this.el.mockNextBtn.textContent = '结束陈述';
        this.el.mockNextBtn.disabled = false;
        this.startCountdown(120, () => this.advanceFromCurrent(true), (left) => {
            this.el.mockTimer.textContent = `${left}s`;
            this.el.mockTimer.classList.toggle('warn', left <= 15);
            if (left === 30) {
                this.el.mockTip.textContent = '还剩约 30 秒，请注意收尾';
            }
        });
    }

    /* ---------- P3 ---------- */
    runP3Question(idx) {
        if (idx >= this.p3Questions.length) {
            this.finishExam();
            return;
        }
        this.stopSpeak();
        this.clearTick();
        this.state = `p3_q${idx + 1}`;
        const q = this.p3Questions[idx];
        this.currentSegment = {
            part: 'p3',
            qid: q.id,
            title: q.q,
            q: q.q,
            startMs: Date.now() - this.recordStartTs
        };
        this.el.mockPhaseLabel.textContent = `Part 3 · 第 ${idx + 1} / ${this.p3Questions.length} 题`;
        this.el.mockQuestionText.textContent = q.q;
        this.el.mockCueCard.style.display = 'none';
        this.el.mockTip.textContent = '建议 30–40 秒作答，超时将自动进入下一题';
        this.el.mockNextBtn.textContent = idx === this.p3Questions.length - 1 ? '结束考试' : '下一题';
        this.el.mockNextBtn.disabled = false;

        this.speakQuestion(q.q);
        this.startCountdown(60, () => this.advanceFromCurrent(true), (left) => {
            this.el.mockTimer.textContent = `${left}s`;
            this.el.mockTimer.classList.toggle('warn', left <= 10);
        });

        if (idx === 0) {
            if (this._p3HardTimer) clearTimeout(this._p3HardTimer);
            this._p3HardTimer = setTimeout(() => {
                if (this.state.startsWith('p3_')) {
                    this.finishExam();
                }
            }, 5 * 60 * 1000);
        }
    }

    stopSpeak() {
        try { speechSynthesis.cancel(); } catch (_) {}
        if (this._ttsAudio) {
            try { this._ttsAudio.pause(); this._ttsAudio.removeAttribute('src'); } catch (_) {}
            this._ttsAudio = null;
        }
    }

    /* ---------- 分段与推进 ---------- */
    nextStep() {
        this.advanceFromCurrent(false);
    }

    /** 收口当前段并进入下一题 / 下一 Part */
    advanceFromCurrent(auto) {
        if (this._advancing) return;
        this._advancing = true;
        try {
            this.clearTick();
            this.stopSpeak();
            const state = this.state;
            this.finishSegment(!!auto);

            if (state.startsWith('p1_q')) {
                const n = parseInt(state.split('_q')[1], 10); // 当前 1-based
                if (n < this.p1Questions.length) this.runP1Question(n);
                else this.advanceToP2();
            } else if (state === 'p2_prep') {
                this.runP2Talk();
            } else if (state === 'p2_talk') {
                this.advanceToP3();
            } else if (state.startsWith('p3_q')) {
                const n = parseInt(state.split('_q')[1], 10);
                if (n < this.p3Questions.length) this.runP3Question(n);
                else this.finishExam();
            }
        } finally {
            this._advancing = false;
        }
    }

    advanceToP2() {
        if (this._p1HardTimer) {
            clearTimeout(this._p1HardTimer);
            this._p1HardTimer = null;
        }
        this.runP2Prep();
    }

    advanceToP3() {
        this.runP3Question(0);
    }

    finishSegment(auto) {
        if (!this.currentSegment) return;
        this.currentSegment.endMs = Date.now() - this.recordStartTs;
        this.currentSegment.durationS = Math.round((this.currentSegment.endMs - this.currentSegment.startMs) / 1000);
        this.currentSegment.autoEnded = !!auto;
        this.segments.push(this.currentSegment);
        this.currentSegment = null;
    }

    /* ---------- 交卷 ---------- */
    async finishExam() {
        this.clearTick();
        this.finishSegment(false);
        this.state = 'uploading';
        this.el.mockPhaseLabel.textContent = '正在交卷…';
        this.el.mockTimer.textContent = '';
        this.el.mockQuestionText.textContent = '请稍候，正在上传录音并评分';
        this.el.mockNextBtn.disabled = true;

        await this.stopRecordingAndUpload();
        await this.transcribeAndScore();
        await this.submitToServer();
        this.renderReport();
    }

    async stopRecordingAndUpload() {
        if (!this.recorder) return;
        return new Promise((resolve) => {
            this.recorder.onstop = async () => {
                const blob = new Blob(this.recordedChunks, { type: 'audio/webm' });
                this.fullAudioBlob = blob;
                this.el.mockRecordDot.classList.remove('recording');
                if (this.micStream) {
                    this.micStream.getTracks().forEach(t => t.stop());
                }
                if (this.audioCtx) {
                    await this.audioCtx.close();
                }
                resolve();
            };
            this.recorder.stop();
        });
    }

    /* 分段转写 + 逐题 AI 评分 */
    async transcribeAndScore() {
        if (!this.fullAudioBlob) return;
        // MVP：先整段转写，再按题切分文本（不够精确，但先跑通）
        // 后续可用 OfflineAudioContext 按 segments 的时间戳切音频再分别转写
        let fullText = '';
        try {
            const form = new FormData();
            form.append('file', this.fullAudioBlob, 'mock-speaking.webm');
            const res = await fetch(this.config.transcribePath, {
                method: 'POST',
                body: form,
                credentials: 'include'
            });
            if (!res.ok) throw new Error('ASR 失败');
            const data = await res.json();
            fullText = (data.recognizedText || data.text || data.transcript || '').trim();
        } catch (e) {
            console.warn('整段转写失败', e);
        }

        // 按题目数均分文本（MVP）
        const per = Math.ceil(fullText.length / Math.max(this.segments.length, 1));
        this.segments.forEach((seg, i) => {
            seg.transcript = fullText.slice(i * per, (i + 1) * per);
        });

        // 逐题调 AI 评分
        for (const seg of this.segments) {
            if (!seg.transcript || seg.transcript.length < 5) continue;
            try {
                const prompt = this.buildPrompt(seg);
                const aiRes = await fetch('/api/ai/messages', {
                    method: 'POST',
                    credentials: 'include',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        max_tokens: 2000,
                        messages: [{ role: 'user', content: prompt }],
                        system: this.getSystemPrompt(),
                        temperature: 0.3
                    })
                });
                if (!aiRes.ok) continue;
                const aiData = await aiRes.json();
                const text = (aiData.content && aiData.content[0] && aiData.content[0].text)
                    || (aiData.choices && aiData.choices[0] && aiData.choices[0].message && aiData.choices[0].message.content)
                    || aiData.output || aiData.text || '';
                seg.score = this.parseScore(text);
            } catch (e) {
                console.warn('AI 评分失败', seg.part, seg.qid, e);
            }
        }

        // 汇总总分（四项平均）
        const scored = this.segments.filter(s => s.score && s.score.overall);
        if (scored.length) {
            const avg = (key) => {
                const vals = scored.map(s => Number(s.score[key] || 0)).filter(n => n > 0);
                return vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length * 10) / 10 : 0;
            };
            this.overall = {
                fc: avg('fc'),
                lr: avg('lr'),
                gra: avg('gra'),
                pron: avg('pron'),
                overall: avg('overall')
            };
            // P2 少于 90 秒封顶 5.5
            const p2seg = this.segments.find(s => s.part === 'p2');
            if (p2seg && p2seg.durationS < 90 && this.overall.overall > 5.5) {
                this.overall.overall = 5.5;
                this.overall.durationCapped = true;
            }
        }
    }

    buildPrompt(seg) {
        const partLabel = seg.part === 'p1' ? 'Part 1' : seg.part === 'p2' ? 'Part 2' : 'Part 3';
        const durationNote = seg.part === 'p2' && seg.durationS < 90
            ? `\n【硬性规则】该 Part 2 录音仅 ${seg.durationS} 秒，不足 90 秒，overall 不得超过 5.5。`
            : '';
        return `你是一位资深雅思口语考官。请评估以下 ${partLabel} 回答。

题目：${seg.q || seg.title}
学生回答（ASR 转写）：
${seg.transcript}

请按四项评分（1–9 整数）：Fluency & Coherence (FC)、Lexical Resource (LR)、Grammatical Range & Accuracy (GRA)、Pronunciation (Pron)。
Overall 为四项平均，可保留 0.5。
输出 JSON：{"fc":x,"lr":x,"gra":x,"pron":x,"overall":x,"comment":"一句话点评"}
${durationNote}`;
    }

    getSystemPrompt() {
        return '你是一位资深雅思口语考官，严格按四项评分标准打分，输出 JSON。';
    }

    parseScore(text) {
        try {
            const m = text.match(/\{[\s\S]*\}/);
            if (!m) return null;
            const obj = JSON.parse(m[0]);
            return {
                fc: Number(obj.fc) || 0,
                lr: Number(obj.lr) || 0,
                gra: Number(obj.gra) || 0,
                pron: Number(obj.pron) || 0,
                overall: Number(obj.overall) || 0,
                comment: String(obj.comment || '')
            };
        } catch {
            return null;
        }
    }

    async submitToServer() {
        if (!this.examId) return;
        try {
            // 先传音频
            if (this.fullAudioBlob) {
                const audioForm = new FormData();
                audioForm.append('file', this.fullAudioBlob, 'exam.webm');
                await fetch(`${this.config.examApiBase}/${this.examId}/audio`, {
                    method: 'POST',
                    body: audioForm,
                    credentials: 'include'
                });
            }
            // 再传结果
            await fetch(`${this.config.examApiBase}/${this.examId}/submit`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    segments: this.segments,
                    overall: this.overall || null,
                    duration_seconds: Math.round((Date.now() - this.startedAt) / 1000),
                    ended_at: new Date().toISOString()
                })
            });
        } catch (e) {
            console.warn('提交模考结果失败', e);
        }
    }

    /* ---------- 报告 ---------- */
    renderReport() {
        this.state = 'report';
        this.el.mockExamView.classList.add('mock-hidden');
        this.el.mockExamView.style.display = 'none';
        this.el.mockReportView.classList.remove('mock-hidden');
        this.el.mockReportView.style.display = 'flex';
        this.el.mockReportView.style.flexDirection = 'column';

        const p2seg = this.segments.find(s => s.part === 'p2');
        const p2Short = p2seg && p2seg.durationS < 90;

        const overallHtml = this.overall ? `
            <div class="mock-overall">
                <div class="mock-band">总 Band：${this.overall.overall}</div>
                <div class="mock-subscores">
                    <span>FC ${this.overall.fc}</span>
                    <span>LR ${this.overall.lr}</span>
                    <span>GRA ${this.overall.gra}</span>
                    <span>Pron ${this.overall.pron}</span>
                </div>
                ${this.overall.durationCapped ? `<p class="mock-warn">⚠️ Part 2 仅 ${p2seg.durationS} 秒，少于 90 秒，总分封顶 5.5</p>` : ''}
            </div>
        ` : '<p>本场未生成有效评分</p>';

        let rows = this.segments.map(seg => `
            <tr>
                <td>${seg.part.toUpperCase()}</td>
                <td>${this.escape(seg.title || seg.q || '')}</td>
                <td>${seg.durationS}s</td>
                <td>${seg.score ? seg.score.overall : '—'}</td>
                <td>${seg.score && seg.score.comment ? this.escape(seg.score.comment) : '—'}</td>
            </tr>
        `).join('');

        this.el.mockReportBody.innerHTML = `
            <h2>口语模考报告</h2>
            <p>总时长：${Math.round((Date.now() - this.startedAt) / 1000)} 秒</p>
            ${overallHtml}
            <table>
                <thead><tr><th>Part</th><th>题目</th><th>时长</th><th>Band</th><th>点评</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
            <p class="mock-note">录音已保存，老师可在后台下载复查。</p>
        `;
    }

    downloadAudio() {
        if (!this.fullAudioBlob) return;
        const url = URL.createObjectURL(this.fullAudioBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `口语模考_${new Date().toISOString().slice(0, 10)}.webm`;
        a.click();
        URL.revokeObjectURL(url);
    }

    abortExam() {
        if (!window.confirm('确定弃考？本场记录将标记为未完成。')) return;
        this.clearTick();
        if (this.recorder && this.recorder.state !== 'inactive') {
            this.recorder.stop();
        }
        if (this.micStream) {
            this.micStream.getTracks().forEach(t => t.stop());
        }
        window.location.href = '/jianyazhenti/student/mock?embed=1';
    }

    /* ---------- 计时工具 ---------- */
    startCountdown(seconds, onDone, onTick) {
        this.clearTick();
        this.deadlineTs = Date.now() + seconds * 1000;
        let finished = false;
        const tick = () => {
            const left = Math.max(0, Math.ceil((this.deadlineTs - Date.now()) / 1000));
            if (onTick) onTick(left);
            if (left <= 0 && !finished) {
                finished = true;
                this.clearTick();
                if (onDone) onDone();
            }
        };
        tick();
        this.tickTimer = window.setInterval(tick, 200);
    }

    clearTick() {
        if (this.tickTimer) {
            window.clearInterval(this.tickTimer);
            this.tickTimer = null;
        }
    }

    escape(s) {
        return String(s || '').replace(/[&<>"]/g, c => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'
        }[c]));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.mockSpeakingExam = new MockSpeakingExam();
});

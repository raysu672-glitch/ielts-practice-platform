// P3：追问链练习（逐题录音 + AI 评分）
class P3Practice {
    constructor() {
        this.data = typeof P3_DATA !== 'undefined' ? P3_DATA : { materials: [], topics: [] };
        this.topicIndex = 0;
        this.questionIndex = 0;
        this.evalByKey = {}; // `${topicId}:${qId}` -> session
        this.bestScores = {};

        this.isRecording = false;
        this.isTranscribing = false;
        this.mediaRecorder = null;
        this.recordingStream = null;
        this.recordedChunks = [];
        this.recordingBlob = null;
        this.recordingStartedAt = null;
        this.lastRecordingDurationS = 0;
        this.transcript = '';
        this.lastAsrResult = null;
        this._recordingKey = null;
        this._ttsToken = 0;
        this._ttsAudio = null;
        this._ttsUtter = null;

        this.bindUI();
        this.renderTopicList();
        this.updateProgressLabel();
        this.loadBestScoresFromServer();
    }

    p1() {
        return window.p1Practice || null;
    }

    topics() {
        return this.data.topics || [];
    }

    currentTopic() {
        return this.topics()[this.topicIndex] || null;
    }

    currentQuestion() {
        const t = this.currentTopic();
        if (!t) return null;
        return (t.questions || [])[this.questionIndex] || null;
    }

    evalKey(topic, q) {
        if (!topic || !q) return '';
        return `${topic.id}:${q.id}`;
    }

    escapeHtml(s) {
        return String(s || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    formatBestScore(score) {
        const p1 = this.p1();
        if (p1 && typeof p1.formatBestScore === 'function') return p1.formatBestScore(score);
        const n = Number(score);
        if (!n || isNaN(n)) return '';
        return (Math.round(n * 2) / 2).toFixed(1);
    }

    scoreKeyForQuestion(q) {
        const p1 = this.p1();
        if (p1 && typeof p1.scoreKeyForQuestion === 'function') return p1.scoreKeyForQuestion(q);
        const raw = String((q && (q.q || q.title)) || '').toLowerCase();
        return raw.replace(/[^a-z0-9]+/g, '') || '';
    }

    canRecord() {
        const p1 = this.p1();
        if (p1 && typeof p1.canRecord === 'function') return p1.canRecord();
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);
    }

    bindUI() {
        document.getElementById('p3TopicList')?.addEventListener('click', (e) => {
            const item = e.target.closest('[data-topic-index]');
            if (!item) return;
            this.selectTopic(Number(item.dataset.topicIndex));
        });
        document.getElementById('p3ChainProgress')?.addEventListener('click', (e) => {
            const btn = e.target.closest('[data-q-index]');
            if (!btn) return;
            this.selectQuestion(Number(btn.dataset.qIndex));
        });
        document.getElementById('p3PrevQBtn')?.addEventListener('click', () => {
            if (this.questionIndex > 0) this.selectQuestion(this.questionIndex - 1);
        });
        document.getElementById('p3NextQBtn')?.addEventListener('click', () => {
            const t = this.currentTopic();
            const n = (t && t.questions && t.questions.length) || 0;
            if (this.questionIndex < n - 1) this.selectQuestion(this.questionIndex + 1);
        });
        document.getElementById('p3SpeakQBtn')?.addEventListener('click', () => {
            const q = this.currentQuestion();
            this.speakText(q?.q || '', document.getElementById('p3SpeakQBtn'));
        });
        document.getElementById('p3StartRecordBtn')?.addEventListener('click', () => this.toggleRecording());
        document.getElementById('p3AiEvaluateBtn')?.addEventListener('click', () => this.evaluateWithAI());
    }

    onShow() {
        this.renderTopicList();
        this.updateProgressLabel();
        if (this.topics().length) {
            this.selectTopic(this.topicIndex || 0);
        }
    }

    updateProgressLabel() {
        const el = document.getElementById('p3ProgressText');
        if (!el) return;
        const total = this.topics().length;
        let done = 0;
        this.topics().forEach((t) => {
            const qs = t.questions || [];
            if (!qs.length) return;
            const all = qs.every((q) => {
                const s = this.evalByKey[this.evalKey(t, q)];
                return s && s.overall != null;
            });
            if (all) done += 1;
        });
        el.textContent = `话题 ${done} / ${total}`;
    }

    async loadBestScoresFromServer() {
        try {
            const res = await fetch('/api/student/speaking-best-scores', { credentials: 'include' });
            if (!res.ok) return;
            const payload = await res.json();
            const scores = (payload && payload.data && payload.data.scores) || {};
            Object.keys(scores).forEach((k) => {
                const n = Number(scores[k]);
                if (k && n && !isNaN(n)) this.bestScores[k] = n;
            });
            const p1 = this.p1();
            if (p1 && p1.bestScores) {
                Object.keys(p1.bestScores).forEach((k) => {
                    const n = Number(p1.bestScores[k]);
                    if (!k || !n || isNaN(n)) return;
                    const prev = Number(this.bestScores[k]);
                    if (!prev || n > prev) this.bestScores[k] = n;
                });
            }
            this.renderTopicList();
        } catch (_) { /* 未登录 */ }
    }

    bestScoreBadgeHtml(q) {
        const key = this.scoreKeyForQuestion(q);
        const best = Number(this.bestScores[key]);
        if (!key || !best || isNaN(best)) return '';
        return `<span class="p1-best-score" title="历史最高分（账号记录）">Band ${this.escapeHtml(this.formatBestScore(best))}</span>`;
    }

    topicBestLabel(topic) {
        const qs = topic.questions || [];
        const bands = qs.map((q) => {
            const saved = this.evalByKey[this.evalKey(topic, q)];
            const fromSession = saved && Number(saved.overall);
            const fromBest = Number(this.bestScores[this.scoreKeyForQuestion(q)]);
            const n = fromSession || fromBest;
            return n && !isNaN(n) ? n : null;
        }).filter((n) => n != null);
        if (!bands.length) return '';
        const avg = bands.reduce((a, b) => a + b, 0) / bands.length;
        return `均 ${this.formatBestScore(avg)}`;
    }

    renderTopicList() {
        const box = document.getElementById('p3TopicList');
        if (!box) return;
        box.innerHTML = '';
        this.topics().forEach((t, idx) => {
            const div = document.createElement('div');
            div.className = 'question-item p2-q-item' + (idx === this.topicIndex ? ' active' : '');
            div.dataset.topicIndex = String(idx);
            const heat = [];
            if (t.relatedP2Title) heat.push(`P2·${t.relatedP2Title}`);
            if (t.heatRank != null) heat.push(`#${t.heatRank}`);
            const nq = (t.questions || []).length;
            heat.push(`${nq}问`);
            const best = this.topicBestLabel(t);
            div.innerHTML = `
                <div class="question-item-title">${idx + 1}. ${this.escapeHtml(t.titleZh || t.titleEn)}${best ? ` <span class="p1-best-score">${this.escapeHtml(best)}</span>` : ''}</div>
                <div class="p2-q-meta">
                    <span class="p2-side-type">${this.escapeHtml(heat.join(' · '))}</span>
                </div>
            `;
            box.appendChild(div);
        });
    }

    selectTopic(index) {
        if (index < 0 || index >= this.topics().length) return;
        if (this.isRecording) this.stopRecording();
        this.topicIndex = index;
        this.questionIndex = 0;
        this.renderTopicList();
        this.renderCard();
        this.updateProgressLabel();
    }

    selectQuestion(index) {
        const t = this.currentTopic();
        if (!t || index < 0 || index >= (t.questions || []).length) return;
        if (this.isRecording) this.stopRecording();
        this.questionIndex = index;
        this.renderCard();
    }

    qTypeMeta(qType) {
        const map = (this.data.answerFrame && this.data.answerFrame.qTypes) || {};
        return map[qType] || { zh: qType || '讨论', tip: '' };
    }

    renderCard() {
        const t = this.currentTopic();
        const empty = document.getElementById('p3Empty');
        const card = document.getElementById('p3Card');
        if (!t) {
            if (empty) empty.style.display = '';
            if (card) card.style.display = 'none';
            return;
        }
        if (empty) empty.style.display = 'none';
        if (card) card.style.display = 'block';

        const q = this.currentQuestion();
        const qs = t.questions || [];
        document.getElementById('p3TopicTitle').textContent = t.titleZh || t.titleEn || '';
        document.getElementById('p3TopicEn').textContent = t.titleEn || '';
        const meta = document.getElementById('p3TopicMeta');
        if (meta) {
            const bits = ['Part 3 追问链'];
            if (t.relatedP2Title) bits.push(`关联 P2：${t.relatedP2Title}`);
            if (t.sourceNote) bits.push(t.sourceNote);
            meta.textContent = bits.join(' · ');
        }

        const progress = document.getElementById('p3ChainProgress');
        if (progress) {
            progress.innerHTML = qs.map((item, i) => {
                const saved = this.evalByKey[this.evalKey(t, item)];
                const scored = saved && saved.overall != null;
                const active = i === this.questionIndex ? ' active' : '';
                const done = scored ? ' scored' : '';
                const band = scored ? ` · ${this.formatBestScore(saved.overall)}` : '';
                return `<button type="button" class="p3-chain-step${active}${done}" data-q-index="${i}">Q${i + 1}${band}</button>`;
            }).join('');
        }

        if (!q) return;
        document.getElementById('p3QuestionText').textContent = q.q || '';
        document.getElementById('p3QuestionTip').textContent = q.tipZh || this.qTypeMeta(q.qType).tip || '';
        const badge = document.getElementById('p3QTypeBadge');
        if (badge) {
            const qt = this.qTypeMeta(q.qType);
            badge.textContent = qt.zh || '';
        }

        const frameSteps = document.getElementById('p3FrameSteps');
        if (frameSteps) {
            const steps = (this.data.answerFrame && this.data.answerFrame.steps) || [];
            frameSteps.innerHTML = `<div class="p3-frame-label">结构提醒</div><ol>${steps.map((s) => `<li>${this.escapeHtml(s)}</li>`).join('')}</ol>`;
        }

        const anglesBox = document.getElementById('p3Angles');
        if (anglesBox) {
            const angles = Array.isArray(q.angles) ? q.angles : [];
            if (angles.length) {
                anglesBox.innerHTML = `<ol class="p3-angle-list">${angles.map((a, i) => `
                    <li>
                        <div class="p3-mat-zh"><strong>角度 ${i + 1}：</strong>${this.escapeHtml(a.zh || '')}</div>
                        <div class="p3-mat-en">${this.escapeHtml(a.en || '')}</div>
                    </li>
                `).join('')}</ol>`;
            } else {
                anglesBox.innerHTML = `<p class="p3-angle-note">${this.escapeHtml(q.tipZh || '围绕题干给两个具体理由即可。')}</p>`;
            }
        }

        const matsBox = document.getElementById('p3Materials');
        const optionalBox = document.getElementById('p3OptionalMatsBox');
        if (matsBox) {
            // 不再按题强推模块；仅展示总库供偶尔借用
            const mats = this.data.materials || [];
            matsBox.innerHTML = mats.map((m) => `
                <div class="p3-mat-card">
                    <div class="p3-mat-title">${this.escapeHtml(m.name)} <span class="p3-mat-hint">${this.escapeHtml(m.typeHint || '')}</span></div>
                    <ul>${(m.bullets || []).map((b) => `
                        <li>
                            <div class="p3-mat-zh">${this.escapeHtml(b.zh || '')}</div>
                            <div class="p3-mat-en">${this.escapeHtml(b.en || '')}</div>
                        </li>
                    `).join('')}</ul>
                </div>
            `).join('');
        }
        if (optionalBox) optionalBox.open = false;

        const sampleBox = document.getElementById('p3SampleBox');
        const sampleText = document.getElementById('p3SampleText');
        if (q.sampleEn && sampleBox && sampleText) {
            sampleBox.style.display = '';
            sampleText.textContent = q.sampleEn;
        } else if (sampleBox) {
            sampleBox.style.display = 'none';
        }

        const prev = document.getElementById('p3PrevQBtn');
        const next = document.getElementById('p3NextQBtn');
        if (prev) prev.disabled = this.questionIndex <= 0;
        if (next) next.disabled = this.questionIndex >= qs.length - 1;

        this.restoreEvalForCurrent();
        this.renderChainSummary();
    }

    setRecordButtonMode(mode) {
        const label = document.getElementById('p3RecordBtnLabel');
        const btn = document.getElementById('p3StartRecordBtn');
        if (!btn) return;
        if (mode === 'recording') {
            if (label) label.textContent = '停止录音';
            btn.classList.add('is-recording');
            btn.style.background = '#ef4444';
        } else if (mode === 'again') {
            if (label) label.textContent = '再练一次';
            btn.classList.remove('is-recording');
            btn.style.background = '';
        } else {
            if (label) label.textContent = '开始练习';
            btn.classList.remove('is-recording');
            btn.style.background = '';
        }
    }

    resetEvalUI({ clearResult = true } = {}) {
        const status = document.getElementById('p3RecordingStatus');
        const evalBtn = document.getElementById('p3AiEvaluateBtn');
        const result = document.getElementById('p3AiResult');
        const content = document.getElementById('p3ResultContent');
        const preview = document.getElementById('p3TranscriptPreview');
        const indicator = document.getElementById('p3StatusIndicator');
        if (status) status.style.display = 'none';
        if (evalBtn) evalBtn.disabled = true;
        if (clearResult) {
            if (result) result.style.display = 'none';
            if (content) content.innerHTML = '';
        }
        if (preview) preview.textContent = '';
        if (indicator) indicator.textContent = '🎙️ 正在录音...';
        this.setRecordButtonMode('start');
    }

    restoreEvalForCurrent() {
        const t = this.currentTopic();
        const q = this.currentQuestion();
        const key = this.evalKey(t, q);
        const saved = key ? this.evalByKey[key] : null;
        const status = document.getElementById('p3RecordingStatus');
        const preview = document.getElementById('p3TranscriptPreview');
        const indicator = document.getElementById('p3StatusIndicator');
        const evalBtn = document.getElementById('p3AiEvaluateBtn');
        const result = document.getElementById('p3AiResult');
        const content = document.getElementById('p3ResultContent');
        if (!saved || !saved.transcript) {
            this.transcript = '';
            this.lastAsrResult = null;
            this.resetEvalUI({ clearResult: true });
            return;
        }
        this.transcript = saved.transcript;
        this.lastAsrResult = saved.lastAsrResult || null;
        this.lastRecordingDurationS = saved.durationS || 0;
        if (status) status.style.display = 'block';
        if (indicator) indicator.textContent = '✅ 识别完成';
        if (preview) preview.textContent = saved.transcript;
        if (evalBtn) evalBtn.disabled = saved.transcript.length <= 5;
        this.setRecordButtonMode('again');
        if (saved.aiHtml && content && result) {
            content.innerHTML = saved.aiHtml;
            result.style.display = 'block';
        } else if (result) {
            result.style.display = 'none';
            if (content) content.innerHTML = '';
        }
    }

    renderChainSummary() {
        const box = document.getElementById('p3ChainSummary');
        const t = this.currentTopic();
        if (!box || !t) return;
        const qs = t.questions || [];
        const rows = qs.map((q, i) => {
            const saved = this.evalByKey[this.evalKey(t, q)];
            const overall = saved && saved.overall != null ? this.formatBestScore(saved.overall) : '—';
            return `<li><strong>Q${i + 1}</strong> Band ${this.escapeHtml(overall)} <span class="p3-sum-q">${this.escapeHtml(q.q || '')}</span></li>`;
        });
        const scored = qs.map((q) => {
            const saved = this.evalByKey[this.evalKey(t, q)];
            return saved && Number(saved.overall);
        }).filter((n) => n && !isNaN(n));
        if (!scored.length) {
            box.style.display = 'none';
            box.innerHTML = '';
            return;
        }
        const avg = scored.reduce((a, b) => a + b, 0) / scored.length;
        const min = Math.min(...scored);
        box.style.display = 'block';
        box.innerHTML = `
            <h4>本话题评分汇总</h4>
            <p>已评 ${scored.length}/${qs.length} 问 · 均分 <strong>${this.escapeHtml(this.formatBestScore(avg))}</strong> · 最低 <strong>${this.escapeHtml(this.formatBestScore(min))}</strong></p>
            <ul>${rows.join('')}</ul>
        `;
    }

    async toggleRecording() {
        if (!this.canRecord()) {
            alert('你的浏览器不支持录音，请使用 Chrome 或 Edge');
            return;
        }
        if (this.isTranscribing) return;
        if (!this.isRecording) await this.startRecording();
        else this.stopRecording();
    }

    stopSpeak() {
        this._ttsToken += 1;
        if (window.speechSynthesis) {
            try { speechSynthesis.cancel(); } catch (_) {}
        }
        this._ttsUtter = null;
        if (this._ttsAudio) {
            try { this._ttsAudio.pause(); this._ttsAudio.src = ''; } catch (_) {}
            this._ttsAudio = null;
        }
        document.querySelectorAll('#part3View .btn-speak.playing').forEach((btn) => {
            btn.classList.remove('playing');
            const label = btn.querySelector('.speak-label');
            if (label) label.textContent = label.dataset.defaultLabel || '听';
        });
    }

    speakText(text, btn) {
        const t = (text || '').trim();
        if (!t) return;
        if (btn && btn.classList.contains('playing')) {
            this.stopSpeak();
            return;
        }
        this.stopSpeak();
        const token = this._ttsToken;
        if (btn) {
            btn.classList.add('playing');
            const label = btn.querySelector('.speak-label');
            if (label) {
                label.dataset.defaultLabel = label.dataset.defaultLabel || label.textContent;
                label.textContent = '停止';
            }
        }
        if (!window.speechSynthesis) {
            if (btn) btn.classList.remove('playing');
            return;
        }
        const utter = new SpeechSynthesisUtterance(t);
        utter.lang = 'en-GB';
        utter.rate = 1.0;
        const voices = speechSynthesis.getVoices() || [];
        const v = voices.find((x) => /en-GB/i.test(x.lang)) || voices.find((x) => /^en/i.test(x.lang));
        if (v) utter.voice = v;
        const clear = () => {
            if (token !== this._ttsToken || !btn) return;
            btn.classList.remove('playing');
            const label = btn.querySelector('.speak-label');
            if (label) label.textContent = label.dataset.defaultLabel || '听';
        };
        utter.onend = clear;
        utter.onerror = clear;
        this._ttsUtter = utter;
        try { speechSynthesis.resume(); } catch (_) {}
        setTimeout(() => {
            if (token !== this._ttsToken) return;
            try { speechSynthesis.speak(utter); } catch (_) {}
        }, 120);
    }

    async startRecording() {
        this.stopSpeak();
        try {
            this.recordingStream = await navigator.mediaDevices.getUserMedia({
                audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }
            });
            const t = this.currentTopic();
            const q = this.currentQuestion();
            this._recordingKey = this.evalKey(t, q);
            this.recordedChunks = [];
            this.recordingBlob = null;
            this.transcript = '';
            this.lastAsrResult = null;

            const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
                ? 'audio/webm;codecs=opus'
                : (MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : '');
            this.mediaRecorder = mimeType
                ? new MediaRecorder(this.recordingStream, { mimeType })
                : new MediaRecorder(this.recordingStream);
            this.mediaRecorder.ondataavailable = (e) => {
                if (e.data && e.data.size > 0) this.recordedChunks.push(e.data);
            };
            this.mediaRecorder.onstop = () => {
                const type = (this.mediaRecorder && this.mediaRecorder.mimeType) || 'audio/webm';
                this.recordingBlob = new Blob(this.recordedChunks, { type });
                if (this.recordingStream) {
                    this.recordingStream.getTracks().forEach((tr) => tr.stop());
                    this.recordingStream = null;
                }
                this.uploadAndTranscribe();
            };

            this.isRecording = true;
            this.recordingStartedAt = Date.now();
            this.mediaRecorder.start(200);
            this.setRecordButtonMode('recording');
            const status = document.getElementById('p3RecordingStatus');
            const indicator = document.getElementById('p3StatusIndicator');
            const preview = document.getElementById('p3TranscriptPreview');
            const evalBtn = document.getElementById('p3AiEvaluateBtn');
            const result = document.getElementById('p3AiResult');
            const content = document.getElementById('p3ResultContent');
            if (status) status.style.display = 'block';
            if (indicator) indicator.textContent = '🎙️ 正在录音... 请说英语（Part 3 建议 30–60 秒）';
            if (preview) preview.textContent = '（录音中，停止后上传识别）';
            if (evalBtn) evalBtn.disabled = true;
            if (result) result.style.display = 'none';
            if (content) content.innerHTML = '';
        } catch (err) {
            console.error('P3 录音失败:', err);
            alert('无法访问麦克风，请检查浏览器权限设置');
            this.isRecording = false;
            this.resetEvalUI();
        }
    }

    stopRecording() {
        if (!this.isRecording) return;
        this.isRecording = false;
        if (this.recordingStartedAt) {
            this.lastRecordingDurationS = Math.max(0, (Date.now() - this.recordingStartedAt) / 1000);
            this.recordingStartedAt = null;
        }
        this.setRecordButtonMode('again');
        const indicator = document.getElementById('p3StatusIndicator');
        const preview = document.getElementById('p3TranscriptPreview');
        if (indicator) indicator.textContent = '⏳ 录音结束，正在上传识别...';
        if (preview) preview.textContent = '上传到 P4 ASR，请稍候...';
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
        }
    }

    async uploadAndTranscribe() {
        const indicator = document.getElementById('p3StatusIndicator');
        const preview = document.getElementById('p3TranscriptPreview');
        const evalBtn = document.getElementById('p3AiEvaluateBtn');
        const p1 = this.p1();
        if (!p1 || typeof p1.transcribeAudioBlob !== 'function') {
            if (indicator) indicator.textContent = '⚠️ 评分模块未就绪，请刷新页面';
            return;
        }
        this.isTranscribing = true;
        try {
            const { transcript, data } = await p1.transcribeAudioBlob(this.recordingBlob);
            this.isTranscribing = false;
            this.lastAsrResult = data;
            const t = this.currentTopic();
            const q = this.currentQuestion();
            const key = this.evalKey(t, q);
            const same = key && key === this._recordingKey;
            if (key) {
                this.evalByKey[key] = {
                    ...(this.evalByKey[key] || {}),
                    transcript,
                    lastAsrResult: data,
                    durationS: this.lastRecordingDurationS,
                    aiHtml: '',
                    overall: null
                };
            }
            if (same) {
                this.transcript = transcript;
                if (indicator) {
                    indicator.textContent = transcript.length > 5 ? '✅ 识别完成' : '⚠️ 未识别到有效内容，请重试';
                }
                if (preview) preview.textContent = transcript || '（未识别到文字）';
                if (evalBtn) evalBtn.disabled = transcript.length <= 5;
                this.setRecordButtonMode('again');
            }
        } catch (err) {
            this.isTranscribing = false;
            console.error(err);
            if (indicator) indicator.textContent = '⚠️ 识别失败：' + (err.message || '请重试');
            if (preview) preview.textContent = '';
            if (evalBtn) evalBtn.disabled = true;
        }
    }

    async evaluateWithAI() {
        const p1 = this.p1();
        if (!p1 || typeof p1.evaluateSpeakingAnswer !== 'function') {
            alert('评分模块未就绪，请刷新页面');
            return;
        }
        const t = this.currentTopic();
        const q = this.currentQuestion();
        if (!q) return;
        const fullTranscript = String(this.transcript || '').trim();
        if (fullTranscript.length < 5) {
            alert('录音内容太短，请先完成练习');
            return;
        }
        const resultDiv = document.getElementById('p3AiResult');
        const loadingDiv = document.getElementById('p3AiLoading');
        const contentDiv = document.getElementById('p3ResultContent');
        const qForEval = {
            ...q,
            title: t ? (t.titleZh || t.titleEn) : '',
            topicTitle: t ? (t.titleZh || t.titleEn) : ''
        };
        try {
            const parsed = await p1.evaluateSpeakingAnswer({
                part: 'p3',
                question: qForEval,
                categoryName: t ? `Part 3 · ${t.titleZh || t.titleEn}` : 'Part 3',
                transcript: fullTranscript,
                asrResult: this.lastAsrResult,
                durationS: this.lastRecordingDurationS,
                mount: { result: resultDiv, loading: loadingDiv, content: contentDiv }
            });
            const key = this.scoreKeyForQuestion(q);
            const overall = Number(parsed.overall);
            if (key && overall && !isNaN(overall)) {
                const prev = Number(this.bestScores[key]);
                if (!prev || overall > prev) this.bestScores[key] = overall;
            }
            const ek = this.evalKey(t, q);
            this.evalByKey[ek] = {
                ...(this.evalByKey[ek] || {}),
                transcript: fullTranscript,
                lastAsrResult: this.lastAsrResult,
                durationS: this.lastRecordingDurationS,
                aiHtml: contentDiv ? contentDiv.innerHTML : '',
                overall: overall || null
            };
            this.setRecordButtonMode('again');
            this.renderTopicList();
            this.renderChainSummary();
            this.updateProgressLabel();
            // refresh chain step badges
            const progress = document.getElementById('p3ChainProgress');
            if (progress) {
                const qs = t.questions || [];
                progress.innerHTML = qs.map((item, i) => {
                    const saved = this.evalByKey[this.evalKey(t, item)];
                    const scored = saved && saved.overall != null;
                    const active = i === this.questionIndex ? ' active' : '';
                    const done = scored ? ' scored' : '';
                    const band = scored ? ` · ${this.formatBestScore(saved.overall)}` : '';
                    return `<button type="button" class="p3-chain-step${active}${done}" data-q-index="${i}">Q${i + 1}${band}</button>`;
                }).join('');
            }
        } catch (error) {
            if (loadingDiv) loadingDiv.style.display = 'none';
            if (contentDiv) {
                contentDiv.innerHTML = `
                    <div class="feedback-section">
                        <h4>评分失败</h4>
                        <p class="feedback-text">${this.escapeHtml(error.message || '请稍后重试')}</p>
                    </div>`;
            }
            if (resultDiv) resultDiv.style.display = 'block';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.p3Practice = new P3Practice();
    // p2-app 可能先执行 showPart('p3')，此时本实例尚未创建；在此补一次
    try {
        const params = new URLSearchParams(window.location.search);
        if (params.get('part') === 'p3') {
            if (window.p2Practice && typeof window.p2Practice.showPart === 'function') {
                window.p2Practice.showPart('p3');
            } else {
                window.p3Practice.onShow();
            }
        }
    } catch (_) {}
});

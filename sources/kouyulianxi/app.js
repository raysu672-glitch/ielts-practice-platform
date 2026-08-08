// P1 练习核心逻辑

// 复合句参考：对齐《口语复合句专练》7 句型 + 4 实战公式，按五大题型步骤挂到每题
// 句型：1A It is adj for sb to do / 1B I find it adj to do / 2 I find sth adj /
//       3 for the reason that|since|as / 4 which / 5 to do / 6 Whenever|As long as / 7 be seen as
const COMPLEX_FRAMES_BY_CAT = {
    // 事实陈述：正面回答 -> 来源或举例 -> 频次 -> 感受
    shishi: {
        1: {
            name: '句型4 which / 句型5 to do',
            pattern: 'I ______ (举例/地点), which ______. / I ______ to ______.',
            tip: '第2步：举例后用 which 补结果，或用 to do 交代目的'
        },
        2: {
            name: '句型6 Whenever / As long as',
            pattern: 'Whenever / As long as I ______, I ______.',
            tip: '第3步：时间/条件状语，交代什么时候会做'
        },
        3: {
            name: '句型1B / 句型2 I find',
            pattern: 'I find it ______ to ______. / I find this ______.',
            tip: '第4步：形式宾语或宾补，收束感受'
        }
    },
    // 喜好类 ≈ 实战练习1：Whenever + to do + I find + which
    xihao: {
        1: {
            name: '句型6 Whenever / 句型3 for the reason that',
            pattern: 'Whenever I ______, I ______. / I am keen on ______ for the reason that ______.',
            tip: '第2步：有时间用 Whenever；讲原因用 for the reason that / since（少用 because）'
        },
        2: {
            name: '句型5 to do 目的状语',
            pattern: 'I am crazy about ______ to ______.',
            tip: '第3步：行为举例时用 to do 交代目的（去哪/做什么）'
        },
        3: {
            name: '句型2 + 句型4 I find..., which',
            pattern: 'I find this activity ______, which ______.',
            tip: '第4步：宾补写感受，再用 which 补放松/收获'
        }
    },
    // 行为习惯类 ≈ 实战练习2：原因 + It is...for me to do + can be seen as
    xingwei: {
        1: {
            name: '句型3 for the reason that / since / as',
            pattern: 'For the reason that / Since ______, I ______.',
            tip: '第2步：高级原因状语，替换普通 because'
        },
        2: {
            name: '句型1A It is + adj. + for me to do',
            pattern: 'It is ______ for me to ______.',
            tip: '第3步：形式主语描述时间线里的行为'
        },
        3: {
            name: '句型7 can be seen / regarded as',
            pattern: '______ can be seen / regarded as ______.',
            tip: '第4步：被动语态收束影响，更客观'
        }
    },
    // 观点类 ≈ 实战练习3：since + to do / which + find it adj to do
    guandian: {
        1: {
            name: '句型3 since + 句型5 to do',
            pattern: 'Since ______, people / I ______ to ______.',
            tip: '第2步：since/for the reason that 给原因，to do 表目的'
        },
        2: {
            name: '句型4 which 补充说明',
            pattern: '..., which ______.',
            tip: '第3步：非限定定语从句，补作用或影响'
        },
        3: {
            name: '句型1B I find it + adj. + to do',
            pattern: 'I / they find it ______ to ______.',
            tip: '第4步：形式宾语收束感受或普遍看法'
        }
    },
    // 对比类 ≈ 实战练习4：regarded as + to do / find it adj to do
    duibi: {
        1: {
            name: '句型7 regarded as + 句型5 to do',
            pattern: 'As for A, ______ is regarded as ______ to ______.',
            tip: '第2步：选项1用被动 + 目的状语写特点与作用'
        },
        2: {
            name: '句型1B find it + adj. + to do',
            pattern: 'By contrast, regarding B, they find it ______ to ______.',
            tip: '第3步：选项2用形式宾语对比难点/偏好'
        },
        3: {
            name: '句型2 I find + 句型4 which',
            pattern: 'I find ______ more ______, which ______.',
            tip: '第4步：个人偏好 + which 补一句理由'
        }
    }
};

class P1Practice {
    constructor() {
        this.data = P1_DATA;
        this.mode = 'sequential';
        this.currentCategoryIndex = 0;
        this.currentQuestionIndex = 0;
        this.practiceHistory = [];
        this.usedQuestions = new Set();
        this.totalRecordingMs = 0;      // 仅累加录音时长
        this.recordingStartedAt = null;
        this.isRecording = false;
        this.isTranscribing = false;
        this.mediaRecorder = null;
        this.recordingStream = null;
        this.recordedChunks = [];
        this.recordingBlob = null;
        this.transcript = '';
        this.currentInterim = '';
        this.apiKey = localStorage.getItem('global_deepseek_key') || localStorage.getItem('deepseek_api_key') || '';
        this.aiBaseUrl = 'https://api.deepseek.com';
        this.aiModel = 'deepseek-v4-flash';
        this._sessionStartedAt = Date.now();
        this._reportedCompleted = 0;
        this._reportedRecordingMs = 0;
        this._reportedP2Done = 0;
        this._studyReportBound = false;
        // 与 P4 跟读同款识别接口（主站 local_server 会转发到 P4 ASR）
        this.transcribeUrl = this.resolveTranscribeUrl();
        this._ttsUtterance = null;
        this._ttsAudio = null;
        this._preferredVoice = null;
        this._ttsToken = 0;
        this._ttsSpeakTimer = null;
        this._ttsWatchdog = null;
        this._ttsStarted = false;
        this._ttsUserStop = false;
        
        this.init();
    }
    
    init() {
        this.renderCategories();
        this.bindEvents();
        this.loadFromStorage();
        this.resetStudyReportBaseline();
        this.bindParentStudySave();
        this.updateProgress();
        this.updateApiStatus();
        this.requestApiKeyFromParent();
        this.warmupVoices();
    }
    
    resolveTranscribeUrl() {
        // 优先同源 /api/p4/transcribe（主站/local_server 转发）
        // 本地纯静态服务时回退到线上 ASR
        const configured = (window.API_CONFIG && window.API_CONFIG.TRANSCRIBE_PATH) || '/api/p4/transcribe';
        if (/^https?:\/\//i.test(configured)) return configured;
        return configured;
    }
    
    // 向主站请求 API Key（优先 /api/config，备用 localStorage）
    async requestApiKeyFromParent() {
        // 先尝试从主站 /api/config 获取（环境变量配置）
        try {
            const res = await fetch('/api/config');
            if (res.ok) {
                const data = await res.json();
                if (data.ai_base_url) this.aiBaseUrl = String(data.ai_base_url).replace(/\/$/, '');
                if (data.ai_model) this.aiModel = data.ai_model;
                if (data.deepseek_key && !this.apiKey) {
                    this.apiKey = data.deepseek_key;
                    this.updateApiStatus();
                    return;
                }
            }
        } catch (e) {
            console.log('无法从 /api/config 获取 key，尝试 localStorage');
        }
        
        // 同域名下直接读取主站配置的 key
        const globalKey = localStorage.getItem('global_deepseek_key');
        if (globalKey && !this.apiKey) {
            this.apiKey = globalKey;
            this.updateApiStatus();
            return;
        }
        
        // 跨域 iframe 才用 postMessage
        if (window.parent !== window) {
            window.parent.postMessage({ type: 'request_deepseek_key' }, '*');
            
            window.addEventListener('message', (event) => {
                if (event.data.type === 'deepseek_key_response' && event.data.key) {
                    this.apiKey = event.data.key;
                    this.updateApiStatus();
                }
            });
        }
    }
    
    // 录音能力检测（改用 MediaRecorder + 阿里云 P4 ASR）
    canRecord() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);
    }
    
    // 渲染左侧类别列表
    renderCategories() {
        const container = document.getElementById('categoryList');
        container.innerHTML = '';
        
        this.data.categories.forEach((cat, catIndex) => {
            const catDiv = document.createElement('div');
            catDiv.className = 'category-item';
            
            const completedCount = cat.questions.filter(q => 
                this.usedQuestions.has(`${catIndex}-${q.id}`)
            ).length;
            
            catDiv.innerHTML = `
                <div class="category-header" data-category="${catIndex}">
                    <span class="category-name">${cat.name}</span>
                    <span class="category-count">${completedCount}/${cat.questions.length}</span>
                </div>
                <div class="question-list" id="questions-${catIndex}">
                    ${cat.questions.map(q => `
                        <div class="question-item ${this.usedQuestions.has(`${catIndex}-${q.id}`) ? 'completed' : ''}" 
                             data-category="${catIndex}" 
                             data-question="${q.id}">
                            ${this.escapeHtml(q.title)}
                        </div>
                    `).join('')}
                </div>
            `;
            
            container.appendChild(catDiv);
        });
        
        const firstList = document.getElementById('questions-0');
        if (firstList) firstList.classList.add('expanded');
    }
    
    // 绑定事件（左侧用事件委托，避免 renderCategories 后点击失效）
    bindEvents() {
        const categoryList = document.getElementById('categoryList');
        if (categoryList && !categoryList.dataset.bound) {
            categoryList.dataset.bound = '1';
            categoryList.addEventListener('click', (e) => {
                const header = e.target.closest('.category-header');
                if (header) {
                    const catIndex = header.dataset.category;
                    const list = document.getElementById(`questions-${catIndex}`);
                    if (list) list.classList.toggle('expanded');
                    return;
                }
                const item = e.target.closest('.question-item');
                if (item) {
                    const catIndex = parseInt(item.dataset.category, 10);
                    const qId = parseInt(item.dataset.question, 10);
                    this.selectQuestion(catIndex, qId);
                }
            });
        }
        
        // 模式切换
        document.getElementById('modeToggle')?.addEventListener('click', () => {
            this.toggleMode();
        });
        
        // 数据面板
        document.getElementById('showDataBtn')?.addEventListener('click', () => {
            document.getElementById('dataPanel').style.display = 'flex';
        });
        
        document.getElementById('closePanel')?.addEventListener('click', () => {
            document.getElementById('dataPanel').style.display = 'none';
        });
        
        // 开始练习
        document.getElementById('startRecordBtn')?.addEventListener('click', () => {
            this.toggleRecording();
        });
        
        // 下一题
        document.getElementById('nextQuestionBtn')?.addEventListener('click', () => {
            this.nextQuestion();
        });
        
        // AI 评分
        document.getElementById('aiEvaluateBtn')?.addEventListener('click', () => {
            this.evaluateWithAI();
        });

        // 听题目
        document.getElementById('speakQuestionBtn')?.addEventListener('click', () => {
            this.toggleSpeakQuestion();
        });
    }
    
    // 选择题目
    selectQuestion(catIndex, qId) {
        const cat = this.data.categories[catIndex];
        if (!cat) return;
        const qIndex = cat.questions.findIndex(q => Number(q.id) === Number(qId));
        if (qIndex < 0) return;
        
        this.currentCategoryIndex = catIndex;
        this.currentQuestionIndex = qIndex;
        
        this.renderQuestion();
        this.updateActiveQuestion();
    }
    
    // 渲染当前题目
    renderQuestion() {
        const cat = this.data.categories[this.currentCategoryIndex];
        const q = cat && cat.questions[this.currentQuestionIndex];
        if (!cat || !q) return;
        
        document.getElementById('emptyState').style.display = 'none';
        document.getElementById('practiceCard').style.display = 'block';
        document.getElementById('feedbackArea').style.display = 'none';
        document.getElementById('aiSection').style.display = 'block';
        document.getElementById('aiResult').style.display = 'none';
        document.getElementById('recordingStatus').style.display = 'none';
        
        document.getElementById('currentCategory').textContent = cat.name;
        // 只保留大字题目（完整题干）
        document.getElementById('currentTitle').textContent = q.q || q.title;
        this.stopSpeakQuestion();
        
        // 渲染步骤
        const stepsContainer = document.getElementById('stepsContainer');
        stepsContainer.innerHTML = '';
        
        cat.steps.forEach((step, stepIndex) => {
            const words = (q.words && q.words[step]) || [];
            const frame = this.getComplexFrame(cat, stepIndex);
            const stepDiv = document.createElement('div');
            stepDiv.className = 'step-item';
            const frameHtml = frame ? `
                <div class="complex-frame">
                    <div class="complex-frame-label">复合句参考 · ${this.escapeHtml(frame.name)}</div>
                    <div class="complex-frame-pattern">${this.escapeHtml(frame.pattern)}</div>
                    <div class="complex-frame-tip">${this.escapeHtml(frame.tip)}</div>
                </div>` : '';
            stepDiv.innerHTML = `
                <div class="step-header">
                    <div class="step-number">${stepIndex + 1}</div>
                    <div class="step-title">${this.escapeHtml(step)}</div>
                </div>
                <div class="step-words">
                    ${words.map(w => `
                        <span class="word-chip" data-word="${this.escapeHtml(w)}">${this.escapeHtml(w)}</span>
                    `).join('') || '<span class="tip-empty">本题此步暂无线索词块</span>'}
                </div>
                ${frameHtml}
            `;
            stepsContainer.appendChild(stepDiv);
        });
        
        // 绑定词块点击
        stepsContainer.querySelectorAll('.word-chip').forEach(chip => {
            chip.addEventListener('click', (e) => {
                e.currentTarget.classList.toggle('used');
            });
        });
        
        // 重置录音状态
        this.transcript = '';
        this.currentInterim = '';
        this.isRecording = false;
        document.getElementById('startRecordBtn').innerHTML = '<span>🎙️</span> 开始练习';
        document.getElementById('startRecordBtn').style.background = '';
        document.getElementById('aiEvaluateBtn').disabled = true;
    }

    getComplexFrame(cat, stepIndex) {
        // 第2–4步（index 1–3）挂《口语复合句专练》对应句型；第1步正面回答用简单句
        if (stepIndex < 1 || stepIndex > 3) return null;
        const byId = COMPLEX_FRAMES_BY_CAT[cat && cat.id];
        if (byId && byId[stepIndex]) return byId[stepIndex];
        // 兜底：通用三句（句型4 / 6 / 1B）
        const fallback = {
            1: {
                name: '句型4 which / 句型3 since',
                pattern: 'I ______, which ______. / Since ______, I ______.',
                tip: '第2步：延伸举例或原因'
            },
            2: {
                name: '句型6 Whenever / As long as',
                pattern: 'Whenever / As long as I ______, I ______.',
                tip: '第3步：时间或条件状语从句'
            },
            3: {
                name: '句型1B I find it + adj. + to do',
                pattern: 'I find it ______ to ______.',
                tip: '第4步：形式宾语收束感受'
            }
        };
        return fallback[stepIndex] || null;
    }
    
    // 更新题目高亮
    updateActiveQuestion() {
        document.querySelectorAll('.question-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const currentQ = this.data.categories[this.currentCategoryIndex].questions[this.currentQuestionIndex];
        const activeItem = document.querySelector(
            `.question-item[data-category="${this.currentCategoryIndex}"][data-question="${currentQ.id}"]`
        );
        if (activeItem) activeItem.classList.add('active');
    }
    
    // 切换顺序/随机模式
    toggleMode() {
        this.mode = this.mode === 'sequential' ? 'random' : 'sequential';
        const icon = document.getElementById('modeIcon');
        const text = document.getElementById('modeText');
        
        if (this.mode === 'random') {
            icon.textContent = '🎲';
            text.textContent = '随机模式';
        } else {
            icon.textContent = '📋';
            text.textContent = '顺序模式';
        }
    }
    
    // 下一题
    nextQuestion() {
        // 若本题已录音则已计入；未录音点下一题不计入已练
        this.saveToStorage();
        this.updateProgress();
        this.renderCategories();
        
        if (this.mode === 'sequential') {
            this.currentQuestionIndex++;
            if (this.currentQuestionIndex >= this.data.categories[this.currentCategoryIndex].questions.length) {
                this.currentQuestionIndex = 0;
                this.currentCategoryIndex++;
                if (this.currentCategoryIndex >= this.data.categories.length) {
                    this.currentCategoryIndex = 0;
                    alert('恭喜！已完成所有题目一遍，可以切换随机模式复习了！');
                }
            }
        } else {
            const allQuestions = [];
            this.data.categories.forEach((cat, catIdx) => {
                cat.questions.forEach((q, qIdx) => {
                    if (!this.usedQuestions.has(`${catIdx}-${q.id}`)) {
                        allQuestions.push({ catIdx, qIdx });
                    }
                });
            });
            
            if (allQuestions.length === 0) {
                const catIdx = Math.floor(Math.random() * this.data.categories.length);
                const qIdx = Math.floor(Math.random() * this.data.categories[catIdx].questions.length);
                this.currentCategoryIndex = catIdx;
                this.currentQuestionIndex = qIdx;
            } else {
                const randomPick = allQuestions[Math.floor(Math.random() * allQuestions.length)];
                this.currentCategoryIndex = randomPick.catIdx;
                this.currentQuestionIndex = randomPick.qIdx;
            }
        }
        
        this.renderQuestion();
        this.updateActiveQuestion();
    }

    // —— 题目朗读：优先本地英音；处理 cancel 竞态 / Online 音失败 / 假启动 ——
    warmupVoices() {
        if (!window.speechSynthesis) return;
        const pick = () => {
            this._preferredVoice =
                this.pickNaturalVoice({ localOnly: true }) || this.pickNaturalVoice();
        };
        pick();
        if (typeof speechSynthesis.addEventListener === 'function') {
            speechSynthesis.addEventListener('voiceschanged', pick);
        } else {
            speechSynthesis.onvoiceschanged = pick;
        }
        try { speechSynthesis.getVoices(); } catch (_) {}
        // 部分浏览器首次 getVoices 为空，稍后重试
        setTimeout(pick, 250);
        setTimeout(pick, 1000);
    }

    pickNaturalVoice(options = {}) {
        if (!window.speechSynthesis) return null;
        const localOnly = !!options.localOnly;
        let voices = [];
        try { voices = speechSynthesis.getVoices() || []; } catch (_) { voices = []; }
        if (!voices.length) return null;

        const score = (v) => {
            const name = (v.name || '').toLowerCase();
            const lang = (v.lang || '').toLowerCase();
            let s = 0;
            if (lang.startsWith('en-gb')) s += 40;
            else if (lang.startsWith('en-us')) s += 28;
            else if (lang.startsWith('en')) s += 12;
            else return -100;

            const isRemote = v.localService === false;
            if (localOnly && isRemote) return -100;

            // 本地自然音最稳；Online Natural 国内易失败，默认大幅降权
            if (/natural|neural/.test(name) && !isRemote) s += 60;
            else if (/online/.test(name) && !localOnly) s += 8;
            else if (/natural|neural/.test(name) && !localOnly) s += 10;
            if (/sonia|libby|aria|jenny|guy|ryan|hazel|susan|george|google uk|google us|emma|michelle|catherine/.test(name)) s += 18;
            if (/microsoft david|microsoft zira|microsoft mark|espeak|compact/.test(name)) s -= 45;
            if (!isRemote) s += 20;
            return s;
        };

        return voices
            .map(v => ({ v, s: score(v) }))
            .filter(x => x.s > 0)
            .sort((a, b) => b.s - a.s)[0]?.v || null;
    }

    setSpeakButtonPlaying(playing) {
        const btn = document.getElementById('speakQuestionBtn');
        if (!btn) return;
        btn.classList.toggle('playing', !!playing);
        const label = btn.querySelector('.speak-label');
        if (label) label.textContent = playing ? '停止' : '听题目';
        const icon = btn.querySelector('.speak-icon');
        if (icon) icon.textContent = playing ? '⏹' : '🔊';
    }

    _clearTtsTimers() {
        if (this._ttsSpeakTimer) {
            clearTimeout(this._ttsSpeakTimer);
            this._ttsSpeakTimer = null;
        }
        if (this._ttsWatchdog) {
            clearTimeout(this._ttsWatchdog);
            this._ttsWatchdog = null;
        }
    }

    stopSpeakQuestion() {
        this._ttsUserStop = true;
        this._clearTtsTimers();
        this._ttsToken = (this._ttsToken || 0) + 1;
        this._ttsStarted = false;
        if (window.speechSynthesis) {
            try { speechSynthesis.cancel(); } catch (_) {}
        }
        this._ttsUtterance = null;
        if (this._ttsAudio) {
            try {
                this._ttsAudio.onerror = null;
                this._ttsAudio.onended = null;
                this._ttsAudio.pause();
                this._ttsAudio.src = '';
            } catch (_) {}
            this._ttsAudio = null;
        }
        this.setSpeakButtonPlaying(false);
    }

    toggleSpeakQuestion() {
        const btn = document.getElementById('speakQuestionBtn');
        if (btn && btn.classList.contains('playing')) {
            this.stopSpeakQuestion();
            return;
        }
        this.speakCurrentQuestion();
    }

    getPrebuiltAudioUrl(cat, q) {
        if (!cat || !q) return '';
        const manifest = (typeof P1_AUDIO_MANIFEST !== 'undefined' && P1_AUDIO_MANIFEST) || {};
        const key = `${cat.id}:${q.id}`;
        const rel = manifest[key] || `audio/${cat.id}/${q.id}.mp3`;
        // 相对当前模块页面路径，兼容主站 iframe
        try {
            return new URL(rel, window.location.href).href;
        } catch (_) {
            return rel;
        }
    }

    speakCurrentQuestion() {
        const cat = this.data.categories[this.currentCategoryIndex];
        const q = cat && cat.questions[this.currentQuestionIndex];
        const text = (q && q.q || '').trim();
        if (!text) return;

        // 先停旧播，再开新 token（避免 cancel 竞态吞掉新 utterance）
        this.stopSpeakQuestion();
        this._ttsUserStop = false;
        this._ttsStarted = false;
        const token = this._ttsToken;

        // 优先播放预生成的神经英音（流畅、稳定）
        const prebuilt = this.getPrebuiltAudioUrl(cat, q);
        if (prebuilt) {
            this._playPrebuiltAudio(prebuilt, text, token);
            return;
        }

        this._speakWithBrowserFallback(text, token);
    }

    _playPrebuiltAudio(url, text, token) {
        if (token !== this._ttsToken) return;
        const audio = new Audio();
        audio.preload = 'auto';
        this._ttsAudio = audio;
        this.setSpeakButtonPlaying(true);

        let settled = false;
        const failToBrowser = () => {
            if (settled || token !== this._ttsToken || this._ttsUserStop) return;
            settled = true;
            this._ttsAudio = null;
            this._speakWithBrowserFallback(text, token);
        };

        audio.onended = () => {
            if (token !== this._ttsToken) return;
            this.setSpeakButtonPlaying(false);
        };
        audio.onerror = () => failToBrowser();
        audio.onloadedmetadata = () => {
            if (token !== this._ttsToken) return;
            if (!isFinite(audio.duration) || audio.duration === 0) failToBrowser();
        };
        audio.src = url;
        audio.play().then(() => {
            this._ttsStarted = true;
        }).catch(() => failToBrowser());
    }

    _speakWithBrowserFallback(text, token) {
        if (token !== this._ttsToken) return;
        if (!window.speechSynthesis) {
            this.speakViaNetworkFallback(text, token);
            return;
        }
        // cancel 后立刻 speak：Edge/Chrome 常会空失败或误报 canceled
        this._ttsSpeakTimer = setTimeout(() => {
            if (token !== this._ttsToken) return;
            const voice =
                this.pickNaturalVoice({ localOnly: true }) ||
                this._preferredVoice ||
                this.pickNaturalVoice();
            this._speakWithVoice(text, token, voice, false);
        }, 180);
    }

    _clearWatchdog() {
        if (this._ttsWatchdog) {
            clearTimeout(this._ttsWatchdog);
            this._ttsWatchdog = null;
        }
    }

    _speakWithVoice(text, token, voice, isRetry) {
        if (token !== this._ttsToken) return;
        if (!window.speechSynthesis) {
            this.speakViaNetworkFallback(text, token);
            return;
        }

        this._clearWatchdog();
        this._ttsStarted = false;
        let failingOver = false;

        // 引擎卡在 paused 时先 resume；仍卡住再清
        try {
            if (speechSynthesis.paused) speechSynthesis.resume();
        } catch (_) {}

        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = (voice && voice.lang) || 'en-GB';
        if (voice) {
            try { utter.voice = voice; } catch (_) {}
        }
        utter.rate = 0.92;
        utter.pitch = 1.02;
        utter.volume = 1;

        const failOver = (forceNetwork) => {
            if (token !== this._ttsToken || this._ttsUserStop || failingOver) return;
            failingOver = true;
            this._clearWatchdog();
            try { speechSynthesis.cancel(); } catch (_) {}
            if (!forceNetwork && !isRetry) {
                const localVoice = this.pickNaturalVoice({ localOnly: true });
                if (localVoice && (!voice || localVoice.name !== voice.name || voice.localService === false)) {
                    this._ttsSpeakTimer = setTimeout(() => {
                        if (token !== this._ttsToken) return;
                        this._speakWithVoice(text, token, localVoice, true);
                    }, 220);
                    return;
                }
            }
            this.speakViaNetworkFallback(text, token);
        };

        utter.onstart = () => {
            if (token !== this._ttsToken) return;
            this._ttsStarted = true;
            this._clearWatchdog();
            this.setSpeakButtonPlaying(true);
        };
        utter.onend = () => {
            if (token !== this._ttsToken) return;
            this._clearWatchdog();
            this.setSpeakButtonPlaying(false);
        };
        utter.onerror = (e) => {
            if (token !== this._ttsToken) return;
            const err = (e && e.error) || '';

            // 用户主动停止
            if (this._ttsUserStop) {
                this._clearWatchdog();
                this.setSpeakButtonPlaying(false);
                return;
            }

            // cancel 后立刻 speak 的假错误：尚未真正开始 → 重试本地音
            if ((err === 'canceled' || err === 'interrupted') && !this._ttsStarted) {
                failOver(false);
                return;
            }
            if (err === 'canceled' || err === 'interrupted') {
                this._clearWatchdog();
                this.setSpeakButtonPlaying(false);
                return;
            }

            // network / synthesis / not-allowed 等
            failOver(err === 'not-allowed');
        };

        this._ttsUtterance = utter;
        this.setSpeakButtonPlaying(true);

        // 若一直不 onstart，判定假启动
        this._ttsWatchdog = setTimeout(() => {
            if (token !== this._ttsToken || this._ttsUserStop) return;
            if (this._ttsStarted) return;
            try { speechSynthesis.cancel(); } catch (_) {}
            failOver(false);
        }, 900);

        const doSpeak = () => {
            if (token !== this._ttsToken) return;
            try {
                speechSynthesis.speak(utter);
                // Chrome/Edge 偶发 stuck paused
                this._ttsSpeakTimer = setTimeout(() => {
                    if (token !== this._ttsToken) return;
                    if (speechSynthesis.speaking && speechSynthesis.paused) {
                        try { speechSynthesis.resume(); } catch (_) {}
                    }
                }, 280);
            } catch (_) {
                failOver(true);
            }
        };

        // 若上面刚 cancel，再留一点空隙
        this._ttsSpeakTimer = setTimeout(doSpeak, isRetry ? 200 : 40);
    }

    // 网络兜底：有道英音 → Google TTS（按句切分，避免超长 URL）
    speakViaNetworkFallback(text, token) {
        if (token != null && token !== this._ttsToken) return;
        if (window.speechSynthesis) {
            try { speechSynthesis.cancel(); } catch (_) {}
        }
        const chunks = this._splitSpeakChunks(text);
        this._playAudioQueue(chunks, 0, token != null ? token : this._ttsToken);
    }

    _splitSpeakChunks(text) {
        const maxLen = 160;
        const parts = text.split(/(?<=[.?!;:])\s+/).map(s => s.trim()).filter(Boolean);
        const chunks = [];
        let buf = '';
        for (const p of parts) {
            if ((buf + ' ' + p).trim().length <= maxLen) {
                buf = (buf + ' ' + p).trim();
            } else {
                if (buf) chunks.push(buf);
                if (p.length <= maxLen) buf = p;
                else {
                    for (let i = 0; i < p.length; i += maxLen) chunks.push(p.slice(i, i + maxLen));
                    buf = '';
                }
            }
        }
        if (buf) chunks.push(buf);
        return chunks.length ? chunks : [text.slice(0, maxLen)];
    }

    _playAudioQueue(chunks, index, token) {
        if (token !== this._ttsToken) return;
        if (index >= chunks.length) {
            this.setSpeakButtonPlaying(false);
            return;
        }
        const chunk = chunks[index];
        const sources = [
            'https://dict.youdao.com/dictvoice?type=2&audio=' + encodeURIComponent(chunk),
            'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=' + encodeURIComponent(chunk)
        ];
        this._tryPlaySources(sources, 0, () => {
            this._playAudioQueue(chunks, index + 1, token);
        }, () => {
            this.setSpeakButtonPlaying(false);
            if (index === 0) {
                alert('朗读失败：浏览器语音不可用，且在线朗读被拦截。请检查网络，或到系统设置里启用英语语音包。');
            }
        }, token);
    }

    _tryPlaySources(sources, i, onDone, onFail, token) {
        if (token !== this._ttsToken) return;
        if (i >= sources.length) {
            onFail();
            return;
        }
        const audio = new Audio();
        audio.preload = 'auto';
        this._ttsAudio = audio;
        this.setSpeakButtonPlaying(true);
        let settled = false;
        const next = () => {
            if (settled) return;
            settled = true;
            this._tryPlaySources(sources, i + 1, onDone, onFail, token);
        };
        audio.onended = () => {
            if (token !== this._ttsToken) return;
            onDone();
        };
        audio.onerror = () => next();
        // 有些环境 play 成功但实际 0 时长 → 当失败
        audio.onloadedmetadata = () => {
            if (token !== this._ttsToken) return;
            if (audio.duration === 0) next();
        };
        audio.src = sources[i];
        audio.play().then(() => {
            // playing
        }).catch(() => next());
    }
    
    // 开始/停止录音（MediaRecorder → P4 ASR）
    async toggleRecording() {
        if (!this.canRecord()) {
            alert('你的浏览器不支持录音，请使用 Chrome 或 Edge');
            return;
        }
        if (this.isTranscribing) return;
        
        if (!this.isRecording) {
            await this.startRecording();
        } else {
            this.stopRecording();
        }
    }
    
    async startRecording() {
        this.stopSpeakQuestion();
        const btn = document.getElementById('startRecordBtn');
        try {
            this.recordingStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });
            
            this.recordedChunks = [];
            this.recordingBlob = null;
            this.transcript = '';
            this.currentInterim = '';
            
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
                    this.recordingStream.getTracks().forEach(t => t.stop());
                    this.recordingStream = null;
                }
                this.uploadAndTranscribe();
            };
            
            this.isRecording = true;
            this.recordingStartedAt = Date.now();
            this.mediaRecorder.start(200);
            
            btn.innerHTML = '<span>⏹️</span> 停止';
            btn.style.background = '#ef4444';
            document.getElementById('recordingStatus').style.display = 'block';
            document.getElementById('statusIndicator').textContent = '🎙️ 正在录音... 请说英语';
            document.getElementById('transcriptPreview').textContent = '（录音中，停止后上传 P4 识别）';
            document.getElementById('aiEvaluateBtn').disabled = true;
            document.getElementById('feedbackArea').style.display = 'none';
            document.getElementById('aiResult').style.display = 'none';
        } catch (err) {
            console.error('录音失败:', err);
            alert('无法访问麦克风，请检查浏览器权限设置');
            this.resetRecordingUI();
        }
    }
    
    stopRecording() {
        if (!this.isRecording) return;
        this.isRecording = false;
        
        // 累加本次录音时长
        if (this.recordingStartedAt) {
            const elapsed = Math.max(0, Date.now() - this.recordingStartedAt);
            if (elapsed >= 1000) {
                this.totalRecordingMs += elapsed;
                this.markCurrentAsPracticed(elapsed);
                this.saveToStorage();
                this.updateProgress();
                this.renderCategories();
                this.updateActiveQuestion();
            }
            this.recordingStartedAt = null;
        }
        
        const btn = document.getElementById('startRecordBtn');
        btn.innerHTML = '<span>🎙️</span> 开始练习';
        btn.style.background = '';
        
        document.getElementById('statusIndicator').textContent = '⏳ 录音结束，正在上传识别...';
        document.getElementById('transcriptPreview').textContent = '上传到 P4 ASR，请稍候...';
        
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
        } else {
            this.resetRecordingUI();
        }
    }
    
    // 录音结束后记为已练
    markCurrentAsPracticed(elapsedMs) {
        const cat = this.data.categories[this.currentCategoryIndex];
        const q = cat && cat.questions[this.currentQuestionIndex];
        if (!cat || !q) return;
        
        const key = `${this.currentCategoryIndex}-${q.id}`;
        this.usedQuestions.add(key);
        
        this.practiceHistory.unshift({
            category: cat.name,
            title: q.title,
            durationMs: elapsedMs || 0,
            time: new Date().toISOString(),
            mode: this.mode
        });
        // 只保留最近 50 条
        if (this.practiceHistory.length > 50) {
            this.practiceHistory = this.practiceHistory.slice(0, 50);
        }
    }
    
    async uploadAndTranscribe() {
        if (!this.recordingBlob || this.recordingBlob.size < 1000) {
            document.getElementById('statusIndicator').textContent = '⚠️ 录音太短，请重试';
            setTimeout(() => {
                document.getElementById('recordingStatus').style.display = 'none';
            }, 2000);
            return;
        }
        
        this.isTranscribing = true;
        const urls = [this.transcribeUrl];
        if (this.transcribeUrl === '/api/p4/transcribe') {
            urls.push('https://p4.oyenglish.com.cn/transcribe');
        }
        
        let lastError = null;
        for (const url of urls) {
            try {
                const form = new FormData();
                form.append('file', this.recordingBlob, 'recording.webm');
                
                const res = await fetch(url, { method: 'POST', body: form });
                if (!res.ok) {
                    const errText = await res.text();
                    throw new Error('HTTP ' + res.status + ': ' + errText.substring(0, 200));
                }
                
                const data = await res.json();
                if (data && data.error) throw new Error(data.error);
                
                this.transcript = (data.recognizedText || data.text || '').trim();
                this.currentInterim = '';
                this.isTranscribing = false;
                
                console.log('P4 ASR 识别结果:', data);
                document.getElementById('statusIndicator').textContent = '✅ 识别完成';
                document.getElementById('transcriptPreview').textContent = this.transcript || '（未识别到文字）';
                
                if (this.transcript.length > 5) {
                    document.getElementById('aiEvaluateBtn').disabled = false;
                    this.showFeedback();
                } else {
                    document.getElementById('statusIndicator').textContent = '⚠️ 未识别到有效内容，请重试';
                }
                return;
            } catch (err) {
                console.warn('识别失败，尝试下一个地址:', url, err);
                lastError = err;
            }
        }
        
        this.isTranscribing = false;
        document.getElementById('statusIndicator').textContent = '❌ 识别失败';
        document.getElementById('transcriptPreview').textContent = lastError
            ? String(lastError.message || lastError)
            : '请确认主站 P4 ASR 服务可用';
        alert('语音识别失败：' + (lastError && lastError.message ? lastError.message : '未知错误') +
              '\n请用主站服务打开页面（带 /api/p4/transcribe 代理），或确认 p4.oyenglish.com.cn 可访问。');
    }
    
    resetRecordingUI() {
        this.isRecording = false;
        this.isTranscribing = false;
        const btn = document.getElementById('startRecordBtn');
        if (btn) {
            btn.innerHTML = '<span>🎙️</span> 开始练习';
            btn.style.background = '';
        }
        if (this.recordingStream) {
            this.recordingStream.getTracks().forEach(t => t.stop());
            this.recordingStream = null;
        }
    }
    
    updateTranscriptPreview() {
        const preview = document.getElementById('transcriptPreview');
        const displayText = this.transcript + (this.currentInterim || '');
        preview.textContent = displayText;
        preview.scrollTop = preview.scrollHeight;
    }
    
    // 显示基础反馈
    showFeedback() {
        const feedbackArea = document.getElementById('feedbackArea');
        const feedbackContent = document.getElementById('feedbackContent');
        
        const fullTranscript = this.transcript + (this.currentInterim || '');
        const usedWords = document.querySelectorAll('.word-chip.used').length;
        const totalWords = document.querySelectorAll('.word-chip').length;
        const coverage = Math.round((usedWords / totalWords) * 100);
        
        let feedback = `📝 转录文本：${fullTranscript.substring(0, 200)}${fullTranscript.length > 200 ? '...' : ''}\n\n`;
        feedback += `📊 词块使用：${usedWords}/${totalWords} (${coverage}%)\n`;
        feedback += `⏱️ 文本长度：${fullTranscript.split(' ').length} 词\n\n`;
        
        if (coverage >= 80) {
            feedback += '✅ 很好！词块覆盖率高，继续保持。';
        } else if (coverage >= 50) {
            feedback += '⚠️ 还可以，尝试使用更多提示词块。';
        } else {
            feedback += '💡 建议多使用给出的词块，逐步提高覆盖率。';
        }
        
        feedbackContent.textContent = feedback;
        feedbackArea.style.display = 'block';
    }
    
    updateApiStatus() {
        // Key 由主站 /api/config（config/ai.env）统一下发，页面不再展示手动配置
    }
    
    // DeepSeek AI 评分
    async evaluateWithAI() {
        if (!this.apiKey) {
            await this.requestApiKeyFromParent();
        }
        if (!this.apiKey) {
            alert('AI 未配置：请在服务器 config/ai.env 中设置 AI_API_KEY 后重启服务');
            return;
        }
        
        const fullTranscript = this.transcript + (this.currentInterim || '');
        if (!fullTranscript || fullTranscript.trim().length < 5) {
            alert('录音内容太短，请先完成练习');
            return;
        }
        
        const resultDiv = document.getElementById('aiResult');
        const loadingDiv = document.getElementById('aiLoading');
        const contentDiv = document.getElementById('resultContent');
        
        resultDiv.style.display = 'block';
        loadingDiv.style.display = 'block';
        contentDiv.innerHTML = '';
        
        const cat = this.data.categories[this.currentCategoryIndex];
        const q = cat.questions[this.currentQuestionIndex];
        this._evalContext = { cat, q };
        
        // 构建提示词
        const prompt = this.buildEvaluationPrompt(cat, q, fullTranscript);
        
        try {
            // 使用 Anthropic 兼容格式
            const base = (this.aiBaseUrl || 'https://api.deepseek.com').replace(/\/$/, '');
            const response = await fetch(base + '/anthropic/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.apiKey,
                    'anthropic-version': '2023-06-01'
                },
                body: JSON.stringify({
                    model: this.aiModel || 'deepseek-v4-flash',
                    max_tokens: 2500,
                    messages: [
                        {
                            role: 'user',
                            content: prompt
                        }
                    ],
                    system: '你是一位专业的雅思口语考官。评分要公平，但内容过短必须低分：不足约 10 个英文词、只有短语/半句、几乎无法展开，总体通常 3.0-4.0，不要给到 5。句子完整、意思清楚、偶有小错的充分回答通常在 Band 5.5-6.5。Pronunciation 依据语音识别完整度判断。每个维度评语必须只谈本维度，并引用学生原话例子与改写。你必须只输出一个合法 JSON 对象，不要输出 Markdown。',
                    temperature: 0.3
                })
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`API 错误 ${response.status}: ${errorText.substring(0, 200)}`);
            }
            
            const data = await response.json();
            console.log('API 返回数据:', data);
            
            // 尝试多种可能的返回格式
            let aiResponse = '';
            if (data.content && data.content[0] && data.content[0].text) {
                aiResponse = data.content[0].text;  // Anthropic 格式
            } else if (data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content) {
                aiResponse = data.choices[0].message.content;  // OpenAI 格式
            } else if (data.output) {
                aiResponse = data.output;
            } else if (data.text) {
                aiResponse = data.text;
            } else if (data.result) {
                aiResponse = data.result;
            } else {
                aiResponse = JSON.stringify(data);
            }
            
            loadingDiv.style.display = 'none';
            this.renderAIResult(aiResponse);
            
        } catch (error) {
            loadingDiv.style.display = 'none';
            contentDiv.innerHTML = `
                <div class="feedback-section">
                    <h4>❌ 评分失败</h4>
                    <p class="feedback-text">${error.message}</p>
                    <p class="feedback-text">请检查 API Key 是否正确，或稍后重试。</p>
                </div>
            `;
        }
    }
    
    // 构建评分提示词
    buildEvaluationPrompt(cat, q, transcript) {
        const stepsInfo = cat.steps.map((step, idx) => {
            const words = q.words[step] || [];
            return `${idx + 1}. ${step}: 建议词块 [${words.slice(0, 3).join(', ')}]`;
        }).join('\n');
        
        // 计算识别质量指标
        const words = transcript.trim().split(/\s+/).filter(w => w.length > 0);
        const wordCount = words.length;
        
        // 识别碎片化程度：短句多、断句多 = 可能发音不连贯
        const sentenceCount = transcript.split(/[.!?]+/).filter(s => s.trim().length > 0).length;
        const avgSentenceLength = sentenceCount > 0 ? wordCount / sentenceCount : wordCount;
        
        // 识别质量评估
        let recognitionQuality = '高';
        let pronunciationHint = '识别完整，推测发音清晰';
        
        if (avgSentenceLength < 3 || wordCount < 10) {
            recognitionQuality = '低';
            pronunciationHint = '识别碎片化严重，推测发音不连贯或停顿过多';
        } else if (avgSentenceLength < 5) {
            recognitionQuality = '中';
            pronunciationHint = '识别基本完整，但句子较短，推测发音可能缺乏连贯性';
        }
        
        return `请评估以下雅思口语 Part 1 回答：

【题目】${q.q}
【题目类型】${cat.name}

【学生回答转录】
"${transcript}"

【语音识别质量分析】
- 识别完整度：${recognitionQuality}
- 总词数：${wordCount}
- 平均句长：${avgSentenceLength.toFixed(1)} 词/句
- 发音推测：${pronunciationHint}

【评分要求】

【校准标准——务必遵守】
- Band 3：只有几个词/半句，几乎没有展开
- Band 4：经常说不完整、难以理解，错误很多；或回答过短（大约少于 12 词）
- Band 5：意思基本能懂，有一定展开，但错误较明显，句式简单
- Band 6：意思清楚、句子基本完整，偶有小错也可；简单但清楚有效就能到 6
- Band 7：表达灵活，错误很少

硬性长度门槛（优先于“简单清楚给 5-6”）：
- 少于约 8 个英文词：Overall 不得超过 3.5，各单项通常 3
- 约 8-15 词且只有一句很短：Overall 不得超过 4.5
- 必须有较完整展开（通常 20+ 词、至少两句）才考虑 5.5 及以上

校准例句（充分回答，总体约 6.0）：
"Yes, absolutely. I used to have a puppy. Every day I walked him to the park, and it really lifted my mood."
→ Fluency 6 / Vocabulary 6 / Grammar 6 / Pronunciation 6-7 / Overall 6.0

过短例句（不得给 5）：
"Yes, I had a dog."
→ 各项约 3-4，Overall 约 3.5-4.0

不要因为词汇简单就打 4（在回答充分时）；但内容过短绝不能虚高到 5。

请只输出一个 JSON 对象（不要 Markdown，不要代码块），字段如下：
{
  "fluency": 6,
  "vocabulary": 6,
  "grammar": 6,
  "pronunciation": 6,
  "reasons": {
    "fluency": "只谈流利度/连贯。问题例子：「原话」→ 更好：「改写」",
    "vocabulary": "只谈词汇/搭配。问题例子：「原话」→ 更好：「改写」",
    "grammar": "只谈语法/时态/结构。问题例子：「原话」→ 更好：「改写」",
    "pronunciation": "只谈识别清晰度/完整度。例子：……"
  },
  "strengths": ["优点1", "优点2"],
  "weaknesses": ["问题1（含原话例子）", "问题2（含原话例子）"],
  "suggestions": ["建议1（含改写例子）", "建议2（含改写例子）"],
  "sample_answer": "可忽略；前端会用题目提示词块生成示范"
}

硬性规则：
1. fluency/vocabulary/grammar/pronunciation 必须是 1-9 的整数，四个都要有，不能缺。
2. 每个 reason 只谈本维度，禁止串台；必须带「原话 → 改写」例子。
3. 例子里的「原话」必须逐字来自学生转录，禁止编造学生没说过的词。
4. 评分公平：清楚有效的简单回答通常 5.5-6.5；不要轻易打到 4.5。
5. 不要因为没用词块扣分。
6. 只输出 JSON。`;
    }
    
    // 渲染 AI 评分结果（优先 JSON）
    renderAIResult(aiResponse) {
        const contentDiv = document.getElementById('resultContent');
        const parsed = this.parseAIEvaluation(aiResponse);
        contentDiv.innerHTML = this.renderScoreHTML(parsed);
        this.reportScoreToParent(parsed);
    }

    reportScoreToParent(parsed) {
        if (!parsed || window.parent === window) return;
        const params = new URLSearchParams(window.location.search);
        const moduleType = params.get('module_type') || 'speaking';
        // 学习/测试模式均上报 AI Band；学习时长仍由主站 iframe 关闭时统计
        const overall = Number(parsed.overall);
        if (!overall || isNaN(overall)) return;
        const endedAt = new Date().toISOString();
        const durationSeconds = Math.max(0, Math.round((Date.now() - (this._sessionStartedAt || Date.now())) / 1000));
        window.parent.postMessage({
            type: 'genericTestComplete',
            completed: true,
            moduleType: moduleType,
            testType: 'speaking_ai_score',
            score: overall,
            scorePercent: overall,
            correctCount: 0,
            totalCount: 0,
            durationSeconds: durationSeconds,
            startedAt: new Date(Date.now() - durationSeconds * 1000).toISOString(),
            endedAt: endedAt,
            details: [{
                fluency: parsed.fluency,
                vocabulary: parsed.vocabulary,
                grammar: parsed.grammar,
                pronunciation: parsed.pronunciation,
                overall: parsed.overall,
                question: (this._evalContext && this._evalContext.q && this._evalContext.q.q) || '',
                transcript: parsed.transcript || this.transcript || ''
            }]
        }, '*');
    }
    
    // 从 AI 返回中提取结构化评分
    parseAIEvaluation(aiResponse) {
        let raw = aiResponse;
        if (typeof raw !== 'string') raw = JSON.stringify(raw);
        raw = String(raw || '').trim();
        
        let data = null;
        // 直接 JSON
        try { data = JSON.parse(raw); } catch (e) {}
        // 从代码块/夹杂文本中抠 JSON
        if (!data) {
            const m = raw.match(/\{[\s\S]*\}/);
            if (m) {
                try { data = JSON.parse(m[0]); } catch (e) {}
            }
        }
        
        const transcript = this.transcript || '';
        const pickInt = (v, fallback) => {
            const n = Math.round(Number(v));
            return (!isNaN(n) && n >= 1 && n <= 9) ? n : fallback;
        };
        
        let fluency = null, vocabulary = null, grammar = null, pronunciation = null;
        let reasons = { fluency: '', vocabulary: '', grammar: '', pronunciation: '' };
        let strengths = [], weaknesses = [], suggestions = [], sampleAnswer = '';
        
        if (data && typeof data === 'object') {
            fluency = data.fluency ?? data.Fluency ?? (data.scores && data.scores.fluency);
            vocabulary = data.vocabulary ?? data.Vocabulary ?? data.lexical ?? (data.scores && (data.scores.vocabulary || data.scores.lexical));
            grammar = data.grammar ?? data.Grammar ?? (data.scores && data.scores.grammar);
            pronunciation = data.pronunciation ?? data.Pronunciation ?? (data.scores && data.scores.pronunciation);
            
            const r = data.reasons || data.reason || {};
            reasons.fluency = r.fluency || r.Fluency || '';
            reasons.vocabulary = r.vocabulary || r.Vocabulary || r.lexical || '';
            reasons.grammar = r.grammar || r.Grammar || '';
            reasons.pronunciation = r.pronunciation || r.Pronunciation || '';
            
            strengths = Array.isArray(data.strengths) ? data.strengths : [];
            weaknesses = Array.isArray(data.weaknesses) ? data.weaknesses : [];
            suggestions = Array.isArray(data.suggestions) ? data.suggestions : [];
            sampleAnswer = data.sample_answer || data.sampleAnswer || data.improved_answer || '';
        } else {
            // Markdown 兜底
            const extractScore = (patterns) => {
                for (const p of patterns) {
                    const m = raw.match(p);
                    if (m) {
                        const n = parseFloat(m[1]);
                        if (!isNaN(n) && n >= 1 && n <= 9) return n;
                    }
                }
                return null;
            };
            fluency = extractScore([/Fluency(?:\s*&\s*Coherence)?[^\d]{0,20}([\d.]+)/i, /流利度[^\d]{0,10}([\d.]+)/i]);
            vocabulary = extractScore([/Vocabulary[^\d]{0,20}([\d.]+)/i, /Lexical[^\d]{0,20}([\d.]+)/i, /词汇[^\d]{0,10}([\d.]+)/i]);
            grammar = extractScore([/Grammar[^\d]{0,20}([\d.]+)/i, /Grammatical[^\d]{0,30}([\d.]+)/i, /语法[^\d]{0,10}([\d.]+)/i]);
            pronunciation = extractScore([/Pronunciation[^\d]{0,20}([\d.]+)/i, /发音[^\d]{0,10}([\d.]+)/i]);
        }
        
        const lengthFallback = this.estimateLengthFallbackScore(transcript);
        const pronFallback = Math.min(this.estimatePronunciationScore(transcript), lengthFallback);
        fluency = pickInt(fluency, lengthFallback);
        vocabulary = pickInt(vocabulary, lengthFallback);
        grammar = pickInt(grammar, lengthFallback);
        pronunciation = pickInt(pronunciation, pronFallback);

        // 内容过短时强制压分，避免默认 5 分虚高
        const capped = this.clampScoresForShortAnswer(transcript, {
            fluency, vocabulary, grammar, pronunciation
        });
        fluency = capped.fluency;
        vocabulary = capped.vocabulary;
        grammar = capped.grammar;
        pronunciation = capped.pronunciation;
        
        // 四个维度评语：必须基于本次转录；AI 评语若引用了学生没说过的内容则丢弃
        reasons.fluency = this.pickGroundedReason('fluency', reasons.fluency, transcript, fluency);
        reasons.vocabulary = this.pickGroundedReason('lexical', reasons.vocabulary, transcript, vocabulary);
        reasons.grammar = this.pickGroundedReason('grammar', reasons.grammar, transcript, grammar);
        reasons.pronunciation = this.pickGroundedReason('pronunciation', reasons.pronunciation, transcript, pronunciation);
        
        strengths = this.filterGroundedList(strengths, transcript);
        weaknesses = this.filterGroundedList(weaknesses, transcript);
        suggestions = this.filterGroundedList(suggestions, transcript);
        
        const avg = (fluency + vocabulary + grammar + pronunciation) / 4;
        let overallNum = Math.round(avg * 2) / 2;
        const maxOverall = this.maxOverallForTranscript(transcript);
        if (overallNum > maxOverall) overallNum = maxOverall;
        const overall = overallNum.toFixed(1);
        
        // 改进示例：固定用本题提示词块 + 至少一句复合句（不依赖 AI，避免照抄）
        const tipSample = this.buildSampleFromTips(
            (this._evalContext && this._evalContext.cat) || this.data.categories[this.currentCategoryIndex],
            (this._evalContext && this._evalContext.q) || this.data.categories[this.currentCategoryIndex].questions[this.currentQuestionIndex]
        );
        sampleAnswer = tipSample.text;
        const tipMeta = tipSample;
        
        return {
            fluency: String(fluency),
            vocabulary: String(vocabulary),
            grammar: String(grammar),
            pronunciation: String(pronunciation),
            overall,
            reasons,
            strengths,
            weaknesses,
            suggestions,
            sampleAnswer,
            tipMeta,
            transcript
        };
    }
    
    // 从评语中抽出「引用片段」
    extractQuotedSnippets(text) {
        const s = String(text || '');
        const out = [];
        const re = /[「"“]([^」"”]{2,80})[」"”]/g;
        let m;
        while ((m = re.exec(s))) out.push(m[1].trim());
        return out;
    }
    
    // 评语是否扎根于本次转录（引用必须能在转录里找到）
    isReasonGrounded(reason, transcript, requireQuote = true) {
        const r = this.cleanReasonText(reason);
        if (!r) return false;
        if (/[{}]/.test(r) || /standard/i.test(r)) return false;
        const t = (transcript || '').toLowerCase();
        if (!t) return false;
        
        const quotes = this.extractQuotedSnippets(r);
        if (quotes.length) {
            return quotes.every(q => {
                const qq = q.toLowerCase().replace(/\s+/g, ' ').trim();
                // 允许短片段模糊：去掉省略号后检查
                const core = qq.replace(/[.…]+/g, ' ').replace(/\s+/g, ' ').trim();
                if (core.length < 2) return true;
                // 若引用里超过一半实词能在转录找到，算通过
                const words = core.split(/\s+/).filter(w => /[a-z]/i.test(w) && w.length > 2);
                if (!words.length) return t.includes(core);
                const hit = words.filter(w => t.includes(w.toLowerCase())).length;
                return hit / words.length >= 0.6;
            });
        }
        
        if (requireQuote) return false; // 有评语但没引用原话 → 不可靠，改用本地
        
        // 无引用时：禁止出现转录里没有的典型编造词
        const bannedIfAbsent = ['dog', 'dogs', 'happy', 'and i feel', 'job', 'gift from'];
        for (const w of bannedIfAbsent) {
            if (r.toLowerCase().includes(w) && !t.includes(w)) return false;
        }
        return true;
    }
    
    pickGroundedReason(dim, aiReason, transcript, score) {
        const cleaned = this.cleanReasonText(aiReason);
        if (cleaned && this.isReasonGrounded(cleaned, transcript, true)) {
            // 仍做串台检查
            const rules = this.dimensionForbidden()[dim] || [];
            if (!rules.some(re => re.test(cleaned))) return cleaned;
        }
        return this.localDimensionReason(dim, transcript || '', score);
    }
    
    filterGroundedList(arr, transcript) {
        if (!Array.isArray(arr)) return [];
        return arr
            .map(x => String(x || '').trim())
            .filter(x => x && this.isReasonGrounded(x, transcript, false))
            .slice(0, 4);
    }
    
    // 收集学生原话中的典型错误片段
    extractStudentErrorPatterns(transcript) {
        const t = String(transcript || '');
        const patterns = [];
        const checks = [
            /\breally liked my mood\b/i,
            /\bliked my mood\b/i,
            /\blike my mood\b/i,
            /\bwalked to him\b/i,
            /\bwalk to him\b/i,
            /\ba pub\b/i,
            /\bat the dogs\b/i,
            /\ba puppy at\b/i,
            /\bin my\.\s*/i,
            /\bWas [A-Z]/,
            /\bHow about\?/i
        ];
        for (const re of checks) {
            const m = t.match(re);
            if (m) patterns.push(m[0]);
        }
        // 过短残缺句（3 词以内且不像完整答句）
        t.split(/[.!?]+/).map(s => s.trim()).filter(Boolean).forEach(s => {
            const n = s.split(/\s+/).length;
            if (n > 0 && n <= 3 && !/^(yes|no|absolutely|sure|of course)\b/i.test(s)) {
                patterns.push(s);
            }
        });
        return patterns;
    }
    
    sampleStillHasErrors(sample, transcript) {
        const errors = this.extractStudentErrorPatterns(transcript);
        const s = String(sample || '').toLowerCase();
        return errors.some(err => err && s.includes(String(err).toLowerCase()));
    }
    
    isBadImprovementSample(sample, transcript) {
        if (!sample || String(sample).trim().length < 20) return true;
        if (this.isTooSimilarToTranscript(sample, transcript)) return true;
        if (this.sampleStillHasErrors(sample, transcript)) return true;
        return false;
    }
    
    // 改进示例若几乎照抄原话，则判定无效
    isTooSimilarToTranscript(sample, transcript) {
        const norm = (s) => String(s || '')
            .toLowerCase()
            .replace(/[^a-z0-9\s]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
        const a = norm(sample);
        const b = norm(transcript);
        if (!a || !b) return true;
        if (a === b) return true;
        const wa = a.split(' ').filter(Boolean);
        const wb = new Set(b.split(' ').filter(Boolean));
        if (wa.length < 8) return a.includes(b) || b.includes(a);
        const hit = wa.filter(w => wb.has(w)).length;
        return (hit / wa.length) >= 0.72; // 更严：超过 72% 相同词就算太像
    }
    
    // 统一纠错替换（保留原意，去掉错误表达）
    applyCommonFixes(text) {
        return String(text || '')
            .replace(/\breally liked my mood\b/gi, 'it really lifted my mood')
            .replace(/\bliked my mood\b/gi, 'lifted my mood')
            .replace(/\blike my mood\b/gi, 'lifts my mood')
            .replace(/\bwalked to him to the park\b/gi, 'walked him to the park')
            .replace(/\bwalked to him\b/gi, 'walked him')
            .replace(/\bwalk to him\b/gi, 'walk him')
            .replace(/\ba pub\b/gi, 'a puppy')
            .replace(/\bat the dogs\b/gi, 'as a pet')
            .replace(/\bHow about\?/gi, '')
            .replace(/\s+/g, ' ')
            .trim();
    }
    
    buildSampleFromTranscript(transcript) {
        const cat = (this._evalContext && this._evalContext.cat) || this.data.categories[this.currentCategoryIndex];
        const q = (this._evalContext && this._evalContext.q) || cat.questions[this.currentQuestionIndex];
        return this.buildSampleFromTips(cat, q).text;
    }
    
    buildForcedImprovement(transcript) {
        return this.buildSampleFromTranscript(transcript);
    }
    
    // 用本题四步提示词块写示范；复合句按题型套《口语复合句专练》实战公式
    buildSampleFromTips(cat, q) {
        const steps = (cat && cat.steps) || [];
        const wordsMap = (q && q.words) || {};
        const chunksOf = (i) => (wordsMap[steps[i]] || []).map(w => String(w).trim()).filter(Boolean);
        const catId = (cat && cat.id) || 'shishi';

        const s0 = chunksOf(0);
        const s1 = chunksOf(1);
        const s2 = chunksOf(2);
        const s3 = chunksOf(3);

        const open = s0.find(w => /^(yes|yeah|sure|absolutely|of course|definitely|exactly|recently)/i.test(w))
            || s0[0]
            || 'Yes, absolutely';
        const usedTo = s0.find(w => /used to/i.test(w));
        const example = s1[0] || 'this';
        const reasonBit = s1.find(w => w !== example) || s1[1] || 'it helps me relax';
        const placeFromS1 = s1.find(w => /home|dorm|school|office|park|city|campus|house|mall|cinema/i.test(w) && w !== example) || '';
        const freq = s2.find(w => /every|once|twice|week|day|often|usually|sometimes|always|spare|free|weekend/i.test(w)) || s2[0] || 'in my spare time';
        const actionBit = s2.find(w => w !== freq) || s2[0] || 'hang out with my friends';
        const placeFromS2 = s2.find(w => /park|home|mall|cinema|gym|school|city/i.test(w)) || '';
        const activityPlace = placeFromS2 || placeFromS1 || '';
        const feelMain = s3.find(w => /mood|happy|enjoy|love|relax|unwind|fun|fascinating|helpful|stress|pleasant/i.test(w)) || s3[0] || 'helps me chill out';
        const feelSub = s3.find(w => w !== feelMain) || 'unwind';
        const opt2 = s2[0] || 'the other option';
        const opt2Feel = s2[1] || s3[0] || 'difficult';

        const usedChunks = [...new Set([
            open, usedTo, example, reasonBit, placeFromS1, freq, actionBit, placeFromS2, feelMain, feelSub, opt2
        ].filter(Boolean))];

        let line1 = String(open).replace(/\.$/, '');
        if (!/yes|sure|absolutely|of course|definitely|exactly|recently|usually|i\b/i.test(line1)) {
            line1 = 'Yes. ' + line1;
        }
        if (!/\.$/.test(line1)) line1 += '.';

        const where = activityPlace ? ` in ${activityPlace}` : '';
        const feelPhrase = /^(really |just )?(lifts?|lifted|makes?|made|helps?|helped|offers?)/i.test(feelMain)
            ? feelMain
            : (/unwind|relax|chill/i.test(feelMain) ? `helps me ${feelMain}` : feelMain);

        let line2 = '';
        let line3 = '';
        let line4 = '';
        let complexType = 'which';
        let complexSentence = '';

        if (catId === 'xihao') {
            // 实战1：Whenever + to do + I find..., which
            line2 = `Whenever I have spare time, I am keen on ${example}${where ? ' ' + where.trim() : ''}.`;
            line3 = `I am crazy about ${actionBit || example} to enjoy myself${where}.`;
            line4 = `I find this activity fascinating, which ${feelPhrase} and offers me a great time to ${feelSub}.`;
            complexType = 'Whenever + to do + I find/which';
            complexSentence = `${line2} ${line4}`;
        } else if (catId === 'xingwei') {
            // 实战2：for the reason that + It is...for me to do + can be seen as
            line2 = `For the reason that ${reasonBit}, I usually choose to ${example}.`;
            line3 = `It is cheerful and enjoyable for me to ${actionBit}${where}.`;
            line4 = `Doing this can be seen as the best way to relieve stress and lift my mood.`;
            complexType = 'for the reason that + It is...for me to do + can be seen as';
            complexSentence = `${line2} ${line3}`;
        } else if (catId === 'guandian') {
            // 实战3：since + to do / which + find it adj to do
            line2 = `Since ${reasonBit}, many people ${example} to ${actionBit || 'take some exercise'}.`;
            line3 = `Besides, people often do this with family or friends, which ${feelPhrase}.`;
            line4 = `They find it relaxing to ${feelSub || 'escape the hustle and bustle of the city'}.`;
            complexType = 'since + which + find it adj to do';
            complexSentence = `${line2} ${line3}`;
        } else if (catId === 'duibi') {
            // 实战4：regarded as + to do / find it adj to do
            line2 = `As for the first option, ${example} is regarded as an easy way to save time and effort.`;
            line3 = `By contrast, regarding the other side, people find it ${opt2Feel} to deal with ${opt2}.`;
            line4 = `Personally, I find ${example} more practical, which ${feelPhrase}.`;
            complexType = 'regarded as + find it adj to do';
            complexSentence = `${line2} ${line3}`;
        } else {
            // 事实陈述：举例 + which / Whenever + I find it
            if (usedTo) {
                if (/^(have|keep|raise|own|go|play|watch|visit)\b/i.test(example)) {
                    line2 = `I ${usedTo} ${example}${placeFromS1 ? ' at ' + placeFromS1 : ''}, which ${feelPhrase}.`;
                } else {
                    line2 = `I ${usedTo} have ${example}${placeFromS1 ? ' at ' + placeFromS1 : ''}, which ${feelPhrase}.`;
                }
            } else if (/^a |^an |^the /i.test(example)) {
                line2 = `For example, I have ${example}${placeFromS1 ? ' at ' + placeFromS1 : ''}, which ${feelPhrase}.`;
            } else {
                line2 = `For example, ${example}${placeFromS1 ? ' at ' + placeFromS1 : ''}, which ${feelPhrase}.`;
            }
            line3 = `Whenever I am free, I usually do this ${freq}${where}.`;
            line4 = `I find it quite enjoyable to keep this habit, which also makes my daily life more colorful.`;
            complexType = 'which + Whenever + I find it';
            complexSentence = line2;
        }

        const tidy = (s) => String(s || '').replace(/\s+/g, ' ').replace(/ at at /g, ' at ').replace(/\s+\./g, '.').trim();
        line2 = tidy(line2); if (line2 && !/\.$/.test(line2)) line2 += '.';
        line3 = tidy(line3); if (line3 && !/\.$/.test(line3)) line3 += '.';
        line4 = tidy(line4); if (line4 && !/\.$/.test(line4)) line4 += '.';

        const text = [line1, line2, line3, line4].filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();

        return {
            text,
            usedChunks,
            complexType,
            complexSentence: tidy(complexSentence)
        };
    }
    
    cleanReasonText(s) {
        let t = String(s || '').trim();
        // 清掉 JSON 残片
        if (!t) return '';
        if (/[{}]/.test(t) || /"standard"/i.test(t) || t.length < 4) return '';
        t = t.replace(/^["'`]+|["'`]+$/g, '').trim();
        return t;
    }
    
    escapeHtml(s) {
        return String(s || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }
    
    renderScoreHTML(p) {
        const getBandClass = (score) => {
            const s = parseFloat(score);
            if (isNaN(s)) return 'band-4';
            if (s >= 6.5) return 'band-6';
            if (s >= 5.5) return 'band-5';
            return 'band-4';
        };
        const row = (name, score, reason) => `
            <tr>
                <td style="padding:8px; border-bottom:1px solid #e0d6c6;">${name}</td>
                <td style="padding:8px; border-bottom:1px solid #e0d6c6;"><strong>${score}</strong></td>
                <td style="padding:8px; border-bottom:1px solid #e0d6c6;">${this.escapeHtml(reason)}</td>
            </tr>`;
        
        const listHtml = (arr) => {
            if (!arr || !arr.length) return '';
            return `<ul>${arr.map(x => `<li>${this.escapeHtml(x)}</li>`).join('')}</ul>`;
        };
        
        let html = `
            <div class="overall-score">
                <div class="overall-label">总体 Band 分数</div>
                <div class="overall-value">${p.overall}</div>
            </div>
            <div class="score-card">
                <div class="score-item"><div class="score-label">Fluency</div><div class="score-value ${getBandClass(p.fluency)}">${p.fluency}</div></div>
                <div class="score-item"><div class="score-label">Vocabulary</div><div class="score-value ${getBandClass(p.vocabulary)}">${p.vocabulary}</div></div>
                <div class="score-item"><div class="score-label">Grammar</div><div class="score-value ${getBandClass(p.grammar)}">${p.grammar}</div></div>
                <div class="score-item"><div class="score-label">Pronunciation</div><div class="score-value ${getBandClass(p.pronunciation)}">${p.pronunciation}</div></div>
            </div>
            <div class="band-note" style="margin-top:12px;padding:12px;background:#e7efe9;border-radius:4px;font-size:14px;color:#243029;">
                <strong>评分说明：</strong>四个单项为整数；总体 Band = 四项平均后按 0.5 取整。Pronunciation 依据识别完整度估算。
            </div>
            <div class="feedback-section" style="margin-top:14px;">
                <h4>📌 为什么是这个分数</h4>
                <div style="overflow-x:auto;">
                    <table style="width:100%;border-collapse:collapse;font-size:14px;">
                        <tr style="background:#f3eee4;text-align:left;">
                            <th style="padding:8px;border-bottom:1px solid #e0d6c6;width:110px;">维度</th>
                            <th style="padding:8px;border-bottom:1px solid #e0d6c6;width:50px;">分数</th>
                            <th style="padding:8px;border-bottom:1px solid #e0d6c6;">原因（含例子）</th>
                        </tr>
                        ${row('Fluency', p.fluency, p.reasons.fluency)}
                        ${row('Vocabulary', p.vocabulary, p.reasons.vocabulary)}
                        ${row('Grammar', p.grammar, p.reasons.grammar)}
                        ${row('Pronunciation', p.pronunciation, p.reasons.pronunciation)}
                        <tr>
                            <td style="padding:8px;">总体 Band</td>
                            <td style="padding:8px;"><strong>${p.overall}</strong></td>
                            <td style="padding:8px;">(${p.fluency}+${p.vocabulary}+${p.grammar}+${p.pronunciation})/4 → ${p.overall}</td>
                        </tr>
                    </table>
                </div>
            </div>
        `;
        
        if (p.strengths.length) {
            html += `<div class="feedback-section"><h4>✅ 优点</h4><div class="feedback-text">${listHtml(p.strengths)}</div></div>`;
        }
        if (p.weaknesses.length) {
            html += `<div class="feedback-section"><h4>⚠️ 需要改进</h4><div class="feedback-text">${listHtml(p.weaknesses)}</div></div>`;
        }
        if (p.suggestions.length) {
            html += `<div class="feedback-section"><h4>💡 改进建议</h4><div class="feedback-text">${listHtml(p.suggestions)}</div></div>`;
        }
        html += `
            <div class="sample-answer">
                <h4>🎯 改进示例（用本题提示词块 + 复合句）</h4>
                <div style="margin-bottom:8px;font-size:13px;color:#6b655c;">
                    使用词块：${(p.tipMeta && p.tipMeta.usedChunks || []).map(c => `<code style="background:#f6efd2;padding:1px 6px;border-radius:2px;margin-right:4px;">${this.escapeHtml(c)}</code>`).join('') || '—'}
                </div>
                <div style="margin-bottom:8px;font-size:13px;color:#1e3f36;">
                    复合句：${this.escapeHtml((p.tipMeta && p.tipMeta.complexSentence) || '')}
                </div>
                <div style="padding:10px;background:#e6f2ea;border-radius:4px;">
                    <p style="margin:0;">${this.escapeHtml(p.sampleAnswer)}</p>
                </div>
            </div>`;
        return html;
    }
    
    // 各维度禁止串台的关键词
    dimensionForbidden() {
        return {
            fluency: [/词汇/, /用词/, /搭配/, /词义/, /时态/, /主谓/, /残缺/, /语法/, /发音/, /识别清晰/, /vocabulary/i, /grammar/i, /pronunciation/i],
            lexical: [/时态/, /主谓/, /残缺句/, /句子结构/, /流利/, /停顿/, /卡顿/, /连贯/, /发音/, /识别完整/, /fluency/i, /grammar/i, /pronunciation/i],
            grammar: [/用词/, /搭配/, /词义/, /词汇量/, /流利/, /停顿/, /卡顿/, /连贯/, /发音/, /识别/, /vocabulary/i, /fluency/i, /pronunciation/i],
            pronunciation: [/时态/, /主谓/, /语法/, /用词/, /搭配/, /词汇/, /逻辑跳跃/, /衔接/, /fluency/i, /vocabulary/i, /grammar/i]
        };
    }
    
    sanitizeDimensionReason(dim, reason, transcript, score) {
        return this.pickGroundedReason(dim, reason, transcript, score);
    }
    
    localDimensionReason(dim, transcript, score) {
        const t = (transcript || '').trim();
        const lower = t.toLowerCase();
        const s = Number(score);
        const clip = (re) => {
            const m = t.match(re);
            return m ? m[0].trim() : '';
        };
        const has = (re) => re.test(lower);
        const sentences = t.split(/[.!?]+/).map(x => x.trim()).filter(x => x.length > 3);
        const firstSent = sentences[0] || '';
        const lastSent = sentences[sentences.length - 1] || '';
        
        if (dim === 'fluency') {
            if (sentences.length >= 3 && sentences.every(x => x.split(/\s+/).length <= 8)) {
                return '句子偏短、推进一般。你说了「' + firstSent + '」和「' + lastSent + '」→ 更好：合成一句，用 and / so 连接。';
            }
            const hardAnd = clip(/\bAnd\b[^.!?]{5,60}/);
            if (hardAnd) {
                return '衔接偏硬。你说「' + hardAnd + '」→ 更好：并入前句，如 “..., and ...”。';
            }
            if (s <= 5) {
                const snippet = t.length > 90 ? t.slice(0, 90) + '...' : t;
                return '整体能听懂，但连贯一般。你的原话：「' + snippet + '」。可把短句连起来。';
            }
            return '根据你的识别文本，表达基本连贯。';
        }
        
        if (dim === 'lexical') {
            const likedMood = clip(/\breally liked my mood\b|\bliked my mood\b|\blike my mood\b/i);
            if (likedMood) {
                return '搭配不够自然。你说了「' + likedMood + '」→ 更好：「it really lifted my mood」。你已用 mood，问题在搭配。';
            }
            const walkedToHim = clip(/\bwalked to him\b|\bwalk(?:ed)?(?:\s+\w+){0,3}\s+to him\b/i);
            if (walkedToHim) {
                return '搭配不当。你说了「' + walkedToHim + '」→ 更好：「walked him to the park」。';
            }
            const bad = clip(/\bat the dogs\b|\ba puppy at\b|\ba pub\b|\bin my\.\b/i);
            if (bad) {
                return '有用词不当。你说了「' + bad + '」→ 换成更准确的词。';
            }
            if (has(/\bpuppy\b/) && has(/\bmood\b/)) {
                return '你已经用了 puppy 和 mood，用词方向对。主要检查搭配是否自然（例如 liked my mood → lifted my mood）。';
            }
            if (has(/\bpuppy\b/)) {
                return '你用了 puppy，这很好。只改说得别扭的搭配，不要换掉已经用对的词。';
            }
            const piece = lastSent || firstSent || t.slice(0, 60);
            return '用词基本能表意。针对你说的「' + piece + '」，可把其中一处搭配说得更地道。';
        }
        
        if (dim === 'grammar') {
            const frag = clip(/\bIn my [^.?!]+\./i) || clip(/\bWas [^.?!]+\./);
            if (frag) {
                return '结构不完整。你说了「' + frag + '」→ 更好：补全主语和动词。';
            }
            if (has(/\bused to\b/) && has(/\bi (walk|feel|go|run|like)\b/)) {
                const bit = clip(/\bI (walk|feel|go|run|like)\b[^.?]*/i) || firstSent;
                return '时态可能不一致。你前面用了 used to，后面有「' + bit + '」→ 讲过去时更稳：walked / felt / liked。';
            }
            if (firstSent) {
                return '语法大体可读。以你的原句「' + firstSent + '」为例，可尝试合并短句。';
            }
            return '语法整体可控；请结合你的原话检查时态和完整句。';
        }
        
        const words = t.split(/\s+/).filter(Boolean).length;
        const avgLen = sentences.length ? words / sentences.length : words;
        const snip = t.length > 80 ? t.slice(0, 80) + '...' : t;
        if (avgLen < 3 || words < 10) {
            return '本次识别偏碎（约 ' + words + ' 词），推测清晰度一般。识别结果：「' + snip + '」。';
        }
        if (s <= 5) return '本次识别基本完整。识别文本：「' + snip + '」。';
        return '本次识别较完整，推测发音清晰。识别文本：「' + snip + '」。';
    }

    // 生成「为什么是这个分数」解读（严格按维度）
    buildScoreAnalysis(s) {
        const lines = [];
        lines.push('总体 Band ' + s.overallBand + '：四项平均后按 0.5 取整（简单但清楚有效通常应在 5.5-6.5，不应轻易给 4.5）。');
        lines.push('Fluency ' + s.fluency + '：' + s.fluencyReason);
        lines.push('Vocabulary ' + s.lexical + '：' + s.lexicalReason);
        lines.push('Grammar ' + s.grammar + '：' + s.grammarReason);
        lines.push('Pronunciation ' + s.pronunciation + '：' + s.pronunciationReason);
        lines.push('参考：像 “I used to have a puppy. Every day I walked him to the park, and it really lifted my mood.” 这种清楚完整的回答，总体大约 Band 6。');
        return lines.map(l => '- ' + l).join('\n');
    }

    countTranscriptWords(transcript) {
        return String(transcript || '').trim().split(/\s+/).filter(w => /[A-Za-z]/.test(w)).length;
    }

    estimateLengthFallbackScore(transcript) {
        const n = this.countTranscriptWords(transcript);
        if (n < 5) return 3;
        if (n < 10) return 3;
        if (n < 16) return 4;
        if (n < 25) return 5;
        return 5;
    }

    maxOverallForTranscript(transcript) {
        const n = this.countTranscriptWords(transcript);
        if (n < 5) return 3.0;
        if (n < 8) return 3.5;
        if (n < 12) return 4.0;
        if (n < 16) return 4.5;
        if (n < 22) return 5.0;
        return 9.0;
    }

    clampScoresForShortAnswer(transcript, scores) {
        const maxOverall = this.maxOverallForTranscript(transcript);
        const maxDim = Math.max(1, Math.min(9, Math.round(maxOverall)));
        const clamp = (v) => Math.min(maxDim, Math.max(1, Number(v) || 1));
        return {
            fluency: clamp(scores.fluency),
            vocabulary: clamp(scores.vocabulary),
            grammar: clamp(scores.grammar),
            pronunciation: clamp(scores.pronunciation)
        };
    }

    // 按识别文本质量估算发音分（方案 B）
    estimatePronunciationScore(transcript) {
        const t = (transcript || '').trim();
        if (!t) return 3;
        const words = t.split(/\s+/).filter(w => w.length > 0);
        const wordCount = words.length;
        const sentenceCount = Math.max(1, t.split(/[.!?]+/).filter(s => s.trim().length > 0).length);
        const avgSentenceLength = wordCount / sentenceCount;
        if (wordCount < 8) return 3;
        if (avgSentenceLength < 3 || wordCount < 10) return 4;
        if (avgSentenceLength < 5) return 5;
        if (avgSentenceLength < 8) return 6;
        return 7;
    }
    
    // 简单 Markdown 解析
    parseMarkdown(text) {
        if (typeof text !== 'string') {
            text = String(text || '');
        }
        
        const extractScore = (patterns) => {
            for (const p of patterns) {
                const m = text.match(p);
                if (m) {
                    const n = parseFloat(m[1]);
                    if (!isNaN(n) && n >= 1 && n <= 9) return n;
                }
            }
            return null;
        };
        
        let overallBand = extractScore([
            /总体\s*Band\s*分数[^\d]*([\d.]+)/i,
            /Overall\s*Band[^\d]*([\d.]+)/i,
            /##\s*总体[^\n]*\n+\s*([\d.]+)/i
        ]);
        
        let fluency = extractScore([
            /Fluency(?:\s*&\s*Coherence)?\**\s*[:：]\s*\**\s*([\d.]+)/i,
            /流利度[^\d]*([\d.]+)/i
        ]);
        let lexical = extractScore([
            /Lexical(?:\s*Resource)?\**\s*[:：]\s*\**\s*([\d.]+)/i,
            /Vocabulary\**\s*[:：]\s*\**\s*([\d.]+)/i,
            /词汇[^\d]*([\d.]+)/i
        ]);
        let grammar = extractScore([
            /Grammatical(?:\s*Range(?:\s*&\s*Accuracy)?)?\**\s*[:：]\s*\**\s*([\d.]+)/i,
            /Grammar\**\s*[:：]\s*\**\s*([\d.]+)/i,
            /语法[^\d]*([\d.]+)/i
        ]);
        let pronunciation = extractScore([
            /Pronunciation\**\s*[:：]\s*\**\s*([\d.]+)/i,
            /发音[^\d]*([\d.]+)/i
        ]);
        
        if (pronunciation == null) {
            pronunciation = this.estimatePronunciationScore(this.transcript || '');
        }
        
        const toInt = (v) => (v == null || isNaN(v) ? '-' : Math.round(v).toString());
        fluency = toInt(fluency);
        lexical = toInt(lexical);
        grammar = toInt(grammar);
        pronunciation = toInt(pronunciation);
        
        // 总体分：优先用四项平均（官方逻辑），AI 文本仅作备用
        const scoreNums = [fluency, lexical, grammar, pronunciation].map(Number).filter(n => !isNaN(n));
        if (scoreNums.length === 4) {
            const avg = scoreNums.reduce((a, b) => a + b, 0) / 4;
            overallBand = (Math.round(avg * 2) / 2).toFixed(1);
        } else if (overallBand != null && !isNaN(Number(overallBand))) {
            overallBand = Number(overallBand).toFixed(1);
        } else {
            overallBand = '-';
        }
        
        // 提取分项评语
        const extractReason = (labelPatterns) => {
            for (const p of labelPatterns) {
                const m = text.match(p);
                if (m && m[1]) return m[1].trim().replace(/^[\-—–]\s*/, '');
            }
            return '';
        };
        let fluencyReason = extractReason([
            /Fluency(?:\s*&\s*Coherence)?\**\s*[:：]\s*\**\s*[\d.]+\s*[-—–:]\s*([^\n]+)/i,
            /流利度[^\n]*[-—–:]\s*([^\n]+)/i
        ]);
        let lexicalReason = extractReason([
            /Lexical(?:\s*Resource)?\**\s*[:：]\s*\**\s*[\d.]+\s*[-—–:]\s*([^\n]+)/i,
            /Vocabulary\**\s*[:：]\s*\**\s*[\d.]+\s*[-—–:]\s*([^\n]+)/i,
            /词汇[^\n]*[-—–:]\s*([^\n]+)/i
        ]);
        let grammarReason = extractReason([
            /Grammatical(?:\s*Range(?:\s*&\s*Accuracy)?)?\**\s*[:：]\s*\**\s*[\d.]+\s*[-—–:]\s*([^\n]+)/i,
            /Grammar\**\s*[:：]\s*\**\s*[\d.]+\s*[-—–:]\s*([^\n]+)/i,
            /语法[^\n]*[-—–:]\s*([^\n]+)/i
        ]);
        let pronunciationReason = extractReason([
            /Pronunciation\**\s*[:：]\s*\**\s*[\d.]+\s*[-—–:]\s*([^\n]+)/i,
            /发音[^\n]*[-—–:]\s*([^\n]+)/i
        ]);
        
        // 从「分数解读」里按维度再抽一遍
        const extractLabeledReason = (label) => {
            const re = new RegExp('(?:^|\n)\s*[-*]?\s*' + label + '\s*[:：]\s*([^\n]+)', 'i');
            const m = text.match(re);
            return m ? m[1].trim() : '';
        };
        fluencyReason = this.sanitizeDimensionReason(
            'fluency',
            fluencyReason || extractLabeledReason('Fluency(?:\s*&\s*Coherence)?'),
            this.transcript,
            fluency
        );
        lexicalReason = this.sanitizeDimensionReason(
            'lexical',
            lexicalReason || extractLabeledReason('(?:Vocabulary|Lexical(?:\s*Resource)?)'),
            this.transcript,
            lexical
        );
        grammarReason = this.sanitizeDimensionReason(
            'grammar',
            grammarReason || extractLabeledReason('(?:Grammar|Grammatical(?:\s*Range(?:\s*&\s*Accuracy)?)?)'),
            this.transcript,
            grammar
        );
        pronunciationReason = this.sanitizeDimensionReason(
            'pronunciation',
            pronunciationReason || extractLabeledReason('Pronunciation'),
            this.transcript,
            pronunciation
        );
        
        // 始终按四维度生成解读，避免串台段落直接展示
        const scoreAnalysis = this.buildScoreAnalysis({
            fluency, lexical, grammar, pronunciation, overallBand,
            fluencyReason, lexicalReason, grammarReason, pronunciationReason,
            transcript: this.transcript || ''
        });
        
        const extractSection = (title) => {
            const regex = new RegExp('### ' + title + '\\s*\\n+([\\s\\S]*?)(?=###|##|$)', 'i');
            const match = text.match(regex);
            return match ? match[1].trim() : '';
        };
        
        const strengths = extractSection('优点');
        const weaknesses = extractSection('需要改进');
        const suggestions = extractSection('改进建议');
        
        const sampleMatch = text.match(/##\s*(?:改进示例|示范回答)\s*\n+([\s\S]*?)(?=##|$)/);
        const sampleAnswer = sampleMatch ? sampleMatch[1].trim() : '';
        
        const getBandClass = (score) => {
            const s = parseFloat(score);
            if (isNaN(s)) return 'band-4';
            if (s >= 6.5) return 'band-6';
            if (s >= 5.5) return 'band-5';
            return 'band-4';
        };
        
        let html = `
            <div class="overall-score">
                <div class="overall-label">总体 Band 分数</div>
                <div class="overall-value">${overallBand}</div>
            </div>
            
            <div class="score-card">
                <div class="score-item">
                    <div class="score-label">Fluency</div>
                    <div class="score-value ${getBandClass(fluency)}">${fluency}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Vocabulary</div>
                    <div class="score-value ${getBandClass(lexical)}">${lexical}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Grammar</div>
                    <div class="score-value ${getBandClass(grammar)}">${grammar}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Pronunciation</div>
                    <div class="score-value ${getBandClass(pronunciation)}">${pronunciation}</div>
                </div>
            </div>
            
            <div class="band-note" style="margin-top: 12px; padding: 12px; background: #e7efe9; border-radius: 4px; font-size: 14px; color: #243029;">
                <strong>评分说明：</strong>四个单项分为整数（1-9），总体 Band = 四项平均后按 0.5 取整。Pronunciation 依据语音识别完整度估算。
            </div>
            
            <div class="feedback-section" style="margin-top: 14px;">
                <h4>📌 为什么是这个分数</h4>
                <div class="score-analysis-table" style="overflow-x:auto;">
                    <table style="width:100%; border-collapse:collapse; font-size:14px;">
                        <tr style="background:#f3eee4; text-align:left;">
                            <th style="padding:8px; border-bottom:1px solid #e0d6c6; width:110px;">维度</th>
                            <th style="padding:8px; border-bottom:1px solid #e0d6c6; width:50px;">分数</th>
                            <th style="padding:8px; border-bottom:1px solid #e0d6c6;">原因</th>
                        </tr>
                        <tr>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;">Fluency</td>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;"><strong>${fluency}</strong></td>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;">${fluencyReason || '见下方解读'}</td>
                        </tr>
                        <tr>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;">Vocabulary</td>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;"><strong>${lexical}</strong></td>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;">${lexicalReason || '见下方解读'}</td>
                        </tr>
                        <tr>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;">Grammar</td>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;"><strong>${grammar}</strong></td>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;">${grammarReason || '见下方解读'}</td>
                        </tr>
                        <tr>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;">Pronunciation</td>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;"><strong>${pronunciation}</strong></td>
                            <td style="padding:8px; border-bottom:1px solid #e0d6c6;">${pronunciationReason || '依据识别完整度估算'}</td>
                        </tr>
                        <tr>
                            <td style="padding:8px;">总体 Band</td>
                            <td style="padding:8px;"><strong>${overallBand}</strong></td>
                            <td style="padding:8px;">四项平均后按 0.5 取整</td>
                        </tr>
                    </table>
                </div>
                <div class="feedback-text" style="margin-top:10px;">${this.formatList(scoreAnalysis)}</div>
            </div>
        `;
        
        if (strengths) {
            html += `
                <div class="feedback-section">
                    <h4>✅ 优点</h4>
                    <div class="feedback-text">${this.formatList(strengths)}</div>
                </div>
            `;
        }
        
        if (weaknesses) {
            html += `
                <div class="feedback-section">
                    <h4>⚠️ 需要改进</h4>
                    <div class="feedback-text">${this.formatList(weaknesses)}</div>
                </div>
            `;
        }
        
        if (suggestions) {
            html += `
                <div class="feedback-section">
                    <h4>💡 改进建议</h4>
                    <div class="feedback-text">${this.formatList(suggestions)}</div>
                </div>
            `;
        }
        
        if (sampleAnswer) {
            html += `
                <div class="sample-answer">
                    <h4>🎯 改进示例（约 Band 6）</h4>
                    <p>${sampleAnswer.replace(/\n/g, '<br>')}</p>
                </div>
            `;
        }
        
        return html;
    }
    
    formatList(text) {
        const lines = text.split('\n').filter(l => l.trim());
        if (lines.length <= 1) return `<p>${text}</p>`;
        return `<ul>${lines.map(l => `<li>${l.replace(/^[-•*]\s*/, '')}</li>`).join('')}</ul>`;
    }
    
    // 更新进度与右侧练习数据
    updateProgress() {
        let total = 0;
        let completed = 0;
        
        this.data.categories.forEach((cat, catIdx) => {
            total += cat.questions.length;
            completed += cat.questions.filter(q => this.usedQuestions.has(`${catIdx}-${q.id}`)).length;
        });
        
        const progressEl = document.getElementById('progressText');
        if (progressEl) progressEl.textContent = `${completed} / ${total} 题`;
        
        const completedEl = document.getElementById('statCompleted');
        if (completedEl) completedEl.textContent = `${completed} / ${total}`;
        
        const timeEl = document.getElementById('statTime');
        if (timeEl) timeEl.textContent = this.formatDuration(this.totalRecordingMs);
        
        this.renderHistoryList();
    }
    
    formatDuration(ms) {
        const totalSec = Math.floor(Math.max(0, ms) / 1000);
        const h = Math.floor(totalSec / 3600);
        const m = Math.floor((totalSec % 3600) / 60);
        const s = totalSec % 60;
        if (h > 0) return `${h}小时${m}分${s}秒`;
        if (m > 0) return `${m}分${s}秒`;
        return `${s}秒`;
    }
    
    renderHistoryList() {
        const list = document.getElementById('historyList');
        if (!list) return;
        
        if (!this.practiceHistory.length) {
            list.innerHTML = '<div class="empty-history" style="color:#94a3b8;font-size:13px;padding:8px 0;">暂无练习记录（完成录音后计入）</div>';
            return;
        }
        
        list.innerHTML = this.practiceHistory.slice(0, 20).map(item => {
            const dur = item.durationMs != null ? this.formatDuration(item.durationMs) : '';
            const time = item.time ? new Date(item.time).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) : '';
            return `<div class="history-item" style="padding:8px 0;border-bottom:1px solid #e0d6c6;font-size:13px;">
                <div style="font-weight:600;">${item.title || '未命名'}</div>
                <div style="color:#6b655c;">${item.category || ''} · ${dur}${time ? ' · ' + time : ''}</div>
            </div>`;
        }).join('');
    }
    
    getP2MaterialsDone() {
        try {
            if (window.p2Practice && typeof window.p2Practice.totalMaterialsDone === 'function') {
                return Number(window.p2Practice.totalMaterialsDone()) || 0;
            }
            const raw = localStorage.getItem('p2_practice_progress');
            if (!raw) return 0;
            const progress = JSON.parse(raw);
            const doneSteps = (progress && progress.doneSteps) || {};
            const materials = (typeof P2_DATA !== 'undefined' && P2_DATA.materials) ? P2_DATA.materials : [];
            let n = 0;
            materials.filter(m => !m.optional).forEach(m => {
                const need = (m.steps || []).length;
                let got = 0;
                for (let i = 0; i < need; i++) {
                    if (doneSteps[`${m.id}:${i}`]) got++;
                }
                if (need > 0 && got >= need) n++;
            });
            return n;
        } catch (e) {
            return 0;
        }
    }

    getTotalQuestionCount() {
        const p1 = (this.data.categories || []).reduce((sum, cat) => sum + (cat.questions || []).length, 0);
        return p1;
    }

    resetStudyReportBaseline() {
        this._reportedCompleted = this.usedQuestions.size;
        this._reportedRecordingMs = this.totalRecordingMs;
        this._reportedP2Done = this.getP2MaterialsDone();
        this._sessionStartedAt = Date.now();
    }

    bindParentStudySave() {
        if (this._studyReportBound) return;
        this._studyReportBound = true;
        window.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'requestSave') {
                this.reportStudyToParent(true);
            }
        });
        window.addEventListener('beforeunload', () => {
            this.reportStudyToParent(true);
        });
    }

    reportStudyToParent(force) {
        if (window.parent === window) return false;
        const p2Done = this.getP2MaterialsDone();
        const completedDelta = Math.max(0, this.usedQuestions.size - (this._reportedCompleted || 0));
        const p2Delta = Math.max(0, p2Done - (this._reportedP2Done || 0));
        const practicedDelta = completedDelta + p2Delta;
        const recordingDeltaMs = Math.max(0, this.totalRecordingMs - (this._reportedRecordingMs || 0));
        const durationSeconds = Math.max(0, Math.round(recordingDeltaMs / 1000));
        if (!force && practicedDelta <= 0 && durationSeconds <= 0) return false;

        const endedAt = new Date().toISOString();
        const startedAt = new Date(Date.now() - Math.max(durationSeconds, 1) * 1000).toISOString();
        window.parent.postMessage({
            type: 'genericStudyComplete',
            moduleType: 'speaking',
            totalWords: practicedDelta,
            wordsTested: practicedDelta,
            totalCorrect: practicedDelta,
            correctCount: practicedDelta,
            wrongCount: 0,
            durationSeconds: durationSeconds,
            startedAt: startedAt,
            endedAt: endedAt,
            details: [{
                kind: 'speaking_practice',
                p1Completed: this.usedQuestions.size,
                p2MaterialsDone: p2Done,
                practicedDelta: practicedDelta,
                totalQuestions: this.getTotalQuestionCount(),
                cumulativeRecordingMs: this.totalRecordingMs,
                recordingDeltaMs: recordingDeltaMs
            }]
        }, '*');

        this._reportedCompleted = this.usedQuestions.size;
        this._reportedRecordingMs = this.totalRecordingMs;
        this._reportedP2Done = p2Done;
        return true;
    }

    // 本地存储
    saveToStorage() {
        const data = {
            usedQuestions: Array.from(this.usedQuestions),
            history: this.practiceHistory,
            mode: this.mode,
            totalRecordingMs: this.totalRecordingMs
        };
        localStorage.setItem('p1_practice_data', JSON.stringify(data));
        this.reportStudyToParent(false);
    }
    
    loadFromStorage() {
        const saved = localStorage.getItem('p1_practice_data');
        if (saved) {
            const data = JSON.parse(saved);
            this.usedQuestions = new Set(data.usedQuestions || []);
            this.practiceHistory = data.history || [];
            this.mode = data.mode || 'sequential';
            this.totalRecordingMs = Number(data.totalRecordingMs) || 0;
            
            const icon = document.getElementById('modeIcon');
            const text = document.getElementById('modeText');
            if (this.mode === 'random') {
                if (icon) icon.textContent = '🎲';
                if (text) text.textContent = '随机模式';
            }
            
            this.renderCategories();
        }
    }
}

// 启动
document.addEventListener('DOMContentLoaded', () => {
    window.p1Practice = new P1Practice();
});
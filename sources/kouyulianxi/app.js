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
        this.lastAsrResult = null;
        this.lastRecordingDurationS = 0;
        // 按题目缓存练习结果（切换题目时保留，再点回来可看）
        this.questionSessions = Object.create(null);
        this._loadedQuestionKey = null;
        this._recordingQuestionKey = null;
        this.aiConfigured = false;
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
        this.loadPublicConfig();
        this.warmupVoices();
    }
    
    resolveTranscribeUrl() {
        // 优先同源 /api/p4/transcribe（主站/local_server 转发）
        // 本地纯静态服务时回退到线上 ASR
        const configured = (window.API_CONFIG && window.API_CONFIG.TRANSCRIBE_PATH) || '/api/p4/transcribe';
        if (/^https?:\/\//i.test(configured)) return configured;
        return configured;
    }
    
    // 读取主站公开配置（不含 API Key；AI 调用走 /api/ai/messages 服务端代理）
    async loadPublicConfig() {
        try {
            const res = await fetch('/api/config', { credentials: 'include' });
            if (!res.ok) return;
            const data = await res.json();
            this.aiConfigured = !!data.ai_configured;
            if (data.ai_model) this.aiModel = data.ai_model;
            this.updateApiStatus();
        } catch (e) {
            console.log('无法从 /api/config 获取配置', e);
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

        const study = this.isStudyMode();
        if (study) {
            const entry = document.createElement('div');
            entry.className = 'category-item complex-entry';
            entry.innerHTML = `
                <div class="category-header complex-entry-header" id="complexSentenceEntry" role="button" tabindex="0">
                    <span class="category-name">📗 复合句闯关</span>
                    <span class="category-count">专练</span>
                </div>
            `;
            container.appendChild(entry);
        }
        
        const season = (this.data.meta && this.data.meta.season) || '';
        this.data.categories.forEach((cat, catIndex) => {
            const catDiv = document.createElement('div');
            catDiv.className = 'category-item';
            
            const completedCount = cat.questions.filter(q => 
                this.usedQuestions.has(`${catIndex}-${q.id}`)
            ).length;

            let lastTopic = null;
            const qHtml = cat.questions.map(q => {
                let topicHead = '';
                if (q.topicEn && q.topicEn !== lastTopic) {
                    lastTopic = q.topicEn;
                    const heat = q.recentCount != null
                        ? `热度#${q.heatRank || '-'} · ${this.formatHeatCount(q.recentCount)}人`
                        : '';
                    topicHead = `
                        <div class="p1-topic-head">
                            <span class="p1-topic-name">${this.escapeHtml(q.topicZh || q.topicEn)}</span>
                            <span class="p1-topic-meta">${this.escapeHtml(q.tag || '')}${heat ? ' · ' + heat : ''}</span>
                        </div>`;
                }
                return `
                    ${topicHead}
                    <div class="question-item ${this.usedQuestions.has(`${catIndex}-${q.id}`) ? 'completed' : ''}"
                         data-category="${catIndex}"
                         data-question="${q.id}">
                        ${this.escapeHtml(q.title)}
                    </div>`;
            }).join('');
            
            catDiv.innerHTML = `
                <div class="category-header" data-category="${catIndex}">
                    <span class="category-name">${this.escapeHtml(cat.name)}</span>
                    <span class="category-count">${completedCount}/${cat.questions.length}</span>
                </div>
                <div class="question-list" id="questions-${catIndex}">
                    ${season && catIndex === 0 ? `<div class="p1-season-note">${this.escapeHtml(season)}在考 · 同类按热度排序</div>` : ''}
                    ${qHtml}
                </div>
            `;
            
            container.appendChild(catDiv);
        });
        
        const firstList = document.getElementById('questions-0');
        if (firstList) firstList.classList.add('expanded');
    }

    isStudyMode() {
        try {
            const params = new URLSearchParams(window.location.search);
            return (params.get('mode') || 'study') !== 'test';
        } catch (_) {
            return true;
        }
    }
    
    // 绑定事件（左侧用事件委托，避免 renderCategories 后点击失效）
    bindEvents() {
        const categoryList = document.getElementById('categoryList');
        if (categoryList && !categoryList.dataset.bound) {
            categoryList.dataset.bound = '1';
            categoryList.addEventListener('click', (e) => {
                const complexEntry = e.target.closest('#complexSentenceEntry, .complex-entry-header');
                if (complexEntry) {
                    if (window.p2Practice && typeof window.p2Practice.setP1Mode === 'function') {
                        window.p2Practice.setP1Mode('complex');
                    }
                    return;
                }
                const header = e.target.closest('.category-header');
                if (header) {
                    if (window.p2Practice && typeof window.p2Practice.setP1Mode === 'function') {
                        window.p2Practice.setP1Mode('questions');
                    }
                    const catIndex = header.dataset.category;
                    if (catIndex === undefined || catIndex === '') return;
                    const list = document.getElementById(`questions-${catIndex}`);
                    if (list) list.classList.toggle('expanded');
                    return;
                }
                const item = e.target.closest('.question-item');
                if (item) {
                    if (window.p2Practice && typeof window.p2Practice.setP1Mode === 'function') {
                        window.p2Practice.setP1Mode('questions');
                    }
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
    
    currentQuestionKey(catIndex = this.currentCategoryIndex, qIndex = this.currentQuestionIndex) {
        const cat = this.data.categories[catIndex];
        const q = cat && cat.questions[qIndex];
        if (!cat || !q) return null;
        return `${catIndex}-${q.id}`;
    }

    setPracticeButtonMode(mode) {
        const btn = document.getElementById('startRecordBtn');
        if (!btn) return;
        if (mode === 'recording') {
            btn.innerHTML = '<span>⏹️</span> 停止';
            btn.style.background = '#ef4444';
            return;
        }
        btn.style.background = '';
        if (mode === 'again') {
            btn.innerHTML = '<span>🎙️</span> 再练一次';
        } else {
            btn.innerHTML = '<span>🎙️</span> 开始练习';
        }
    }

    // 把当前页上的练习结果写入缓存（切换题目前调用）
    persistLoadedQuestionSession() {
        const key = this._loadedQuestionKey;
        if (!key || this.isRecording) return;
        const transcript = String(this.transcript || '').trim();
        const aiHtml = (document.getElementById('resultContent')?.innerHTML || '').trim();
        const feedbackText = (document.getElementById('feedbackContent')?.textContent || '').trim();
        if (!transcript && !aiHtml && !feedbackText) return;

        const usedChips = Array.from(document.querySelectorAll('.word-chip.used'))
            .map(el => (el.getAttribute('data-word') || el.textContent || '').trim())
            .filter(Boolean);
        const aiResultEl = document.getElementById('aiResult');
        const feedbackEl = document.getElementById('feedbackArea');
        const statusEl = document.getElementById('recordingStatus');
        this.questionSessions[key] = {
            transcript,
            lastAsrResult: this.lastAsrResult,
            lastRecordingDurationS: this.lastRecordingDurationS || 0,
            usedChips,
            feedbackText,
            feedbackVisible: !!(feedbackEl && feedbackEl.style.display !== 'none' && feedbackText),
            aiHtml,
            aiVisible: !!(aiResultEl && aiResultEl.style.display !== 'none' && aiHtml),
            statusVisible: !!(statusEl && statusEl.style.display !== 'none' && transcript),
            statusText: document.getElementById('statusIndicator')?.textContent || '✅ 识别完成',
            aiEvaluateEnabled: transcript.length > 5
        };
    }

    applyQuestionSession(session) {
        if (!session) return;
        this.transcript = session.transcript || '';
        this.currentInterim = '';
        this.lastAsrResult = session.lastAsrResult || null;
        this.lastRecordingDurationS = session.lastRecordingDurationS || 0;

        const chipSet = new Set((session.usedChips || []).map(x => String(x).toLowerCase()));
        document.querySelectorAll('.word-chip').forEach(chip => {
            const word = (chip.getAttribute('data-word') || chip.textContent || '').trim();
            chip.classList.toggle('used', chipSet.has(word.toLowerCase()));
        });
        if (this.transcript) this.syncWordChipsWithTranscript(this.transcript);

        const statusEl = document.getElementById('recordingStatus');
        const statusInd = document.getElementById('statusIndicator');
        const preview = document.getElementById('transcriptPreview');
        if (statusEl) {
            statusEl.style.display = (session.statusVisible || !!this.transcript) ? 'block' : 'none';
        }
        if (statusInd) statusInd.textContent = session.statusText || (this.transcript ? '✅ 识别完成' : '');
        if (preview) preview.textContent = this.transcript || '';

        const aiBtn = document.getElementById('aiEvaluateBtn');
        if (aiBtn) aiBtn.disabled = !(session.aiEvaluateEnabled || this.transcript.length > 5);

        if (session.feedbackVisible || this.transcript) {
            this.showFeedback();
        } else {
            const feedbackArea = document.getElementById('feedbackArea');
            if (feedbackArea) feedbackArea.style.display = 'none';
        }

        const aiResult = document.getElementById('aiResult');
        const loadingDiv = document.getElementById('aiLoading');
        const contentDiv = document.getElementById('resultContent');
        if (aiResult && contentDiv) {
            if (session.aiHtml) {
                contentDiv.innerHTML = session.aiHtml;
                aiResult.style.display = 'block';
                if (loadingDiv) loadingDiv.style.display = 'none';
            } else {
                contentDiv.innerHTML = '';
                aiResult.style.display = 'none';
            }
        }

        this.setPracticeButtonMode(this.transcript || session.aiHtml ? 'again' : 'start');
    }

    resetPracticeUiForFreshQuestion() {
        this.transcript = '';
        this.currentInterim = '';
        this.lastAsrResult = null;
        this.lastRecordingDurationS = 0;
        this.setPracticeButtonMode('start');
        const aiBtn = document.getElementById('aiEvaluateBtn');
        if (aiBtn) aiBtn.disabled = true;
        const feedbackArea = document.getElementById('feedbackArea');
        if (feedbackArea) feedbackArea.style.display = 'none';
        const aiResult = document.getElementById('aiResult');
        if (aiResult) aiResult.style.display = 'none';
        const contentDiv = document.getElementById('resultContent');
        if (contentDiv) contentDiv.innerHTML = '';
        const statusEl = document.getElementById('recordingStatus');
        if (statusEl) statusEl.style.display = 'none';
        const preview = document.getElementById('transcriptPreview');
        if (preview) preview.textContent = '';
    }

    // 选择题目
    selectQuestion(catIndex, qId) {
        const cat = this.data.categories[catIndex];
        if (!cat) return;
        const qIndex = cat.questions.findIndex(q => Number(q.id) === Number(qId));
        if (qIndex < 0) return;

        if (this.isRecording) this.stopRecording();
        
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

        // 切换前先保存上一题结果
        this.persistLoadedQuestionSession();
        
        document.getElementById('emptyState').style.display = 'none';
        document.getElementById('practiceCard').style.display = 'block';
        document.getElementById('aiSection').style.display = 'block';
        
        const heatBits = [];
        if (q.topicZh || q.topicEn) heatBits.push(q.topicZh || q.topicEn);
        if (q.tag) heatBits.push(q.tag);
        if (q.heatRank != null) heatBits.push(`热度#${q.heatRank}`);
        if (q.recentCount != null) heatBits.push(`近${this.formatHeatCount(q.recentCount)}人考过`);
        document.getElementById('currentCategory').textContent =
            heatBits.length ? `${cat.name} · ${heatBits.join(' · ')}` : cat.name;
        // 只保留大字题目（完整题干）
        document.getElementById('currentTitle').textContent = q.q || q.title;
        this.stopSpeakQuestion();

        const tipBox = document.getElementById('p1TipBanner');
        if (tipBox) {
            const tipText = q.tip || q.logic || '';
            if (tipText) {
                tipBox.style.display = '';
                tipBox.innerHTML = `<strong>答题思路</strong><span>${this.escapeHtml(tipText)}</span>`;
            } else {
                tipBox.style.display = 'none';
                tipBox.innerHTML = '';
            }
        }
        
        // 渲染步骤
        const stepsContainer = document.getElementById('stepsContainer');
        stepsContainer.innerHTML = '';
        
        cat.steps.forEach((step, stepIndex) => {
            const words = (q.words && q.words[step]) || [];
            const frame = this.getComplexFrame(cat, stepIndex, q);
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

        const sampleBox = document.getElementById('p1SampleBox');
        const sampleText = document.getElementById('p1SampleText');
        if (sampleBox && sampleText) {
            if (q.sample) {
                sampleBox.style.display = '';
                sampleText.textContent = q.sample;
                sampleBox.open = false;
            } else {
                sampleBox.style.display = 'none';
                sampleText.textContent = '';
            }
        }

        const key = this.currentQuestionKey();
        this._loadedQuestionKey = key;
        this.isRecording = false;

        const cached = key ? this.questionSessions[key] : null;
        if (cached && (cached.transcript || cached.aiHtml)) {
            this.applyQuestionSession(cached);
        } else {
            this.resetPracticeUiForFreshQuestion();
        }
    }

    getComplexFrame(cat, stepIndex, q) {
        // 第2–4步（index 1–3）挂《口语复合句专练》对应句型；第1步正面回答用简单句
        if (stepIndex < 1 || stepIndex > 3) return null;
        const qFrames = q && q.frames;
        if (qFrames && qFrames[String(stepIndex)]) return qFrames[String(stepIndex)];
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
        if (this.isRecording) this.stopRecording();
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
        try {
            this.recordingStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });

            // 再练一次：清空当前题展示，结果会在新识别完成后覆盖缓存
            this._recordingQuestionKey = this.currentQuestionKey();
            this.recordedChunks = [];
            this.recordingBlob = null;
            this.transcript = '';
            this.currentInterim = '';
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
                    this.recordingStream.getTracks().forEach(t => t.stop());
                    this.recordingStream = null;
                }
                this.uploadAndTranscribe();
            };
            
            this.isRecording = true;
            this.recordingStartedAt = Date.now();
            this.mediaRecorder.start(200);
            
            this.setPracticeButtonMode('recording');
            document.getElementById('recordingStatus').style.display = 'block';
            document.getElementById('statusIndicator').textContent = '🎙️ 正在录音... 请说英语';
            document.getElementById('transcriptPreview').textContent = '（录音中，停止后上传 P4 识别）';
            document.getElementById('aiEvaluateBtn').disabled = true;
            document.getElementById('feedbackArea').style.display = 'none';
            document.getElementById('aiResult').style.display = 'none';
            const contentDiv = document.getElementById('resultContent');
            if (contentDiv) contentDiv.innerHTML = '';
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
        let elapsed = 0;
        if (this.recordingStartedAt) {
            elapsed = Math.max(0, Date.now() - this.recordingStartedAt);
            this.lastRecordingDurationS = elapsed / 1000;
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
        
        // 练完后按钮改为「再练一次」（识别中也保持此文案）
        this.setPracticeButtonMode('again');
        
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
                
                const res = await fetch(url, {
                    method: 'POST',
                    body: form,
                    credentials: url.startsWith('/') ? 'include' : 'omit'
                });
                if (!res.ok) {
                    const errText = await res.text();
                    throw new Error('HTTP ' + res.status + ': ' + errText.substring(0, 200));
                }
                
                const data = await res.json();
                if (data && data.error) throw new Error(data.error);
                
                const transcript = (data.recognizedText || data.text || data.transcript || '').trim();
                this.lastAsrResult = data;
                this.currentInterim = '';
                this.isTranscribing = false;

                const targetKey = this._recordingQuestionKey || this.currentQuestionKey();
                const viewingSame = targetKey && targetKey === this.currentQuestionKey();
                if (viewingSame) {
                    this.transcript = transcript;
                }

                // 无论是否已切题，都把结果写入对应题目缓存
                if (targetKey) {
                    const prev = this.questionSessions[targetKey] || {};
                    this.questionSessions[targetKey] = {
                        ...prev,
                        transcript,
                        lastAsrResult: data,
                        lastRecordingDurationS: this.lastRecordingDurationS || prev.lastRecordingDurationS || 0,
                        feedbackVisible: transcript.length > 5,
                        statusVisible: true,
                        statusText: transcript.length > 5 ? '✅ 识别完成' : '⚠️ 未识别到有效内容，请重试',
                        aiEvaluateEnabled: transcript.length > 5,
                        // 再练覆盖旧评分
                        aiHtml: '',
                        aiVisible: false
                    };
                }
                
                console.log('P4 ASR 识别结果:', data);
                if (viewingSame) {
                    document.getElementById('statusIndicator').textContent =
                        transcript.length > 5 ? '✅ 识别完成' : '⚠️ 未识别到有效内容，请重试';
                    document.getElementById('transcriptPreview').textContent = transcript || '（未识别到文字）';
                    this.setPracticeButtonMode('again');
                    if (transcript.length > 5) {
                        document.getElementById('aiEvaluateBtn').disabled = false;
                        this.showFeedback();
                        this.persistLoadedQuestionSession();
                    }
                }
                return;
            } catch (err) {
                console.warn('识别失败，尝试下一个地址:', url, err);
                lastError = err;
            }
        }
        
        this.isTranscribing = false;
        const viewingSame = !this._recordingQuestionKey || this._recordingQuestionKey === this.currentQuestionKey();
        if (viewingSame) {
            document.getElementById('statusIndicator').textContent = '❌ 识别失败';
            document.getElementById('transcriptPreview').textContent = lastError
                ? String(lastError.message || lastError)
                : '请确认主站 P4 ASR 服务可用';
            this.setPracticeButtonMode('again');
        }
        alert('语音识别失败：' + (lastError && lastError.message ? lastError.message : '未知错误') +
              '\n请用主站服务打开页面（带 /api/p4/transcribe 代理），或确认 p4.oyenglish.com.cn 可访问。');
    }
    
    resetRecordingUI() {
        this.isRecording = false;
        this.isTranscribing = false;
        const hasResult = !!(this.transcript && this.transcript.trim())
            || !!(this._loadedQuestionKey && this.questionSessions[this._loadedQuestionKey]
                && this.questionSessions[this._loadedQuestionKey].transcript);
        this.setPracticeButtonMode(hasResult ? 'again' : 'start');
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
    
    normalizeChunkText(s) {
        return String(s || '')
            .toLowerCase()
            .replace(/[’']/g, "'")
            .replace(/[^a-z0-9'\s]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    // 词块是否出现在口述转录里（不依赖是否点选芯片）
    chunkAppearsInTranscript(chunk, transcript) {
        const t = this.normalizeChunkText(transcript);
        const c = this.normalizeChunkText(chunk);
        if (!t || !c) return false;
        if (t.includes(c)) return true;
        // “a puppy” 可匹配口述里的 puppy；多词短语要求核心词都出现
        const withoutArticle = c.replace(/^(a|an|the)\s+/, '');
        if (withoutArticle && withoutArticle !== c && t.includes(withoutArticle)) return true;
        const parts = c.split(' ').filter(w => w.length > 1 && !/^(a|an|the|to|of|in|on|at|for|my|your)$/.test(w));
        if (parts.length >= 2) {
            return parts.every(w => t.includes(w));
        }
        return false;
    }

    // 按转录匹配词块，并同步点亮芯片；返回 { matched, total, chips }
    syncWordChipsWithTranscript(transcript) {
        const chips = Array.from(document.querySelectorAll('.word-chip'));
        const matched = [];
        chips.forEach(chip => {
            const word = (chip.getAttribute('data-word') || chip.textContent || '').trim();
            const hit = this.chunkAppearsInTranscript(word, transcript);
            chip.classList.toggle('used', hit);
            if (hit) matched.push(word);
        });
        return { matched, total: chips.length, chips: matched };
    }

    // 显示基础反馈
    showFeedback() {
        const feedbackArea = document.getElementById('feedbackArea');
        const feedbackContent = document.getElementById('feedbackContent');
        
        const fullTranscript = this.transcript + (this.currentInterim || '');
        const { matched, total } = this.syncWordChipsWithTranscript(fullTranscript);
        const usedWords = matched.length;
        const totalWords = total || document.querySelectorAll('.word-chip').length;
        const coverage = totalWords > 0 ? Math.round((usedWords / totalWords) * 100) : 0;
        
        let feedback = `📝 转录文本：${fullTranscript.substring(0, 200)}${fullTranscript.length > 200 ? '...' : ''}\n\n`;
        feedback += `📊 词块使用：${usedWords}/${totalWords} (${coverage}%)\n`;
        if (matched.length) {
            feedback += `✅ 已识别词块：${matched.join('、')}\n`;
        }
        feedback += `⏱️ 文本长度：${fullTranscript.trim().split(/\s+/).filter(Boolean).length} 词\n\n`;
        
        if (coverage >= 80) {
            feedback += '✅ 很好！词块覆盖率高，继续保持。';
        } else if (coverage >= 50) {
            feedback += '⚠️ 还可以，尝试使用更多提示词块。';
        } else if (usedWords > 0) {
            feedback += '💡 已用到部分词块，可再覆盖更多步骤里的提示词。';
        } else {
            feedback += '💡 建议多使用给出的词块，逐步提高覆盖率。';
        }
        
        feedbackContent.textContent = feedback;
        feedbackArea.style.display = 'block';
    }
    
    updateApiStatus() {
        // AI Key 仅在服务端；前端通过 /api/ai/messages 代理调用
    }
    
    // DeepSeek AI 评分（经主站 /api/ai/messages 代理，需登录）
    async evaluateWithAI() {
        await this.loadPublicConfig();
        if (!this.aiConfigured) {
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
        const evalKey = this.currentQuestionKey();
        this._evalContext = { cat, q, key: evalKey };
        
        const metrics = this.extractSpeakingMetrics(
            fullTranscript,
            this.lastAsrResult,
            this.lastRecordingDurationS
        );
        const prompt = this.buildEvaluationPrompt(cat, q, fullTranscript, metrics);
        
        try {
            const response = await fetch('/api/ai/messages', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    max_tokens: 4000,
                    messages: [
                        {
                            role: 'user',
                            content: prompt
                        }
                    ],
                    system: this.getSpeakingSystemPrompt(),
                    temperature: 0.3
                })
            });
            
            if (response.status === 401) {
                throw new Error('请先登录主站后再使用 AI 评分');
            }
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
            this.renderAIResult(aiResponse, evalKey);
            
        } catch (error) {
            loadingDiv.style.display = 'none';
            if (evalKey === this.currentQuestionKey()) {
                contentDiv.innerHTML = `
                    <div class="feedback-section">
                        <h4>❌ 评分失败</h4>
                        <p class="feedback-text">${error.message}</p>
                        <p class="feedback-text">请检查 API Key 是否正确，或稍后重试。</p>
                    </div>
                `;
            }
        }
    }
    
    getSpeakingSystemPrompt() {
        return `你是一位资深雅思口语考官，拥有15年阅卷经验。你正在评估一位中国学生的雅思口语回答。

你将收到：
1. 学生的口语转录文本（由语音识别系统生成）
2. 语音量化指标（语速、停顿、填充词、词时长等）

你需要根据这些数据，对四个维度进行评分（每项必须是 1–9 的整数，禁止 0.5），并给出具体反馈。总分 overall 可以是 0.5 间隔（由四项平均后按规则进位）。

## 评分标准

### 流利度与连贯性 (Fluency & Coherence, FC)
- 9分：极其流畅，几乎无重复/自我修正；犹豫仅因思考内容；衔接自然；话题展开充分
- 8分：流畅，偶尔重复；犹豫主要与内容相关；话题展开连贯且恰当
- 7分：能不费力说长段落；犹豫/重复不影响连贯；灵活使用连接词
- 6分：愿意说长段落但偶尔失去连贯；连接词使用不总恰当
- 5分：依赖重复/自我修正/慢速维持；过度使用某些连接词
- 4分及以下：明显停顿，语速慢，频繁重复；连贯性断裂

### 词汇资源 (Lexical Resource, LR)
- 9分：词汇量极大，精准使用；习语自然准确
- 8分：词汇丰富灵活；熟练使用不常见词和习语；有效释义
- 7分：词汇灵活；使用不常见词和习语；有搭配意识
- 6分：词汇足够；用词偶尔不当但意思清楚；基本能释义
- 5分：词汇有限；尝试释义但不总成功
- 4分及以下：词汇匮乏；频繁用词错误

### 语法范围与准确性 (Grammatical Range & Accuracy, GRA)
- 9分：结构精确准确，仅偶有口误
- 8分：广泛使用多种结构；大多数句子无错误
- 7分：使用多种复杂结构；无错误句子频繁
- 6分：混合简单和复杂句型；复杂结构常出错但不影响沟通
- 5分：基本句型准确；尝试复杂结构但总出错
- 4分及以下：基本句型；从句罕见；结构重复

### 发音 (Pronunciation, P)
注意：你无法直接听到发音。你需要根据以下间接证据推断发音水平：
- 语音识别系统对文本的识别结果（识别异常可能暗示发音问题）
- 词时长数据（异常拖长或吞音可能暗示发音问题）
- 语速数据（过快可能影响清晰度，过慢可能不自信）
- 套话/背稿感（开场复述题目、模板句堆砌、回答不像临场思考）会显得不自然
- 发音可以是四项里的强项：无明显硬伤、表达较自然时，应敢于给 7（真实考官对 6.0 档考生常把 Pron 打到 7）
- 只有在明显模板堆砌、开场复述题目、或听起来过度准备时，才把 Pron 压在 6
- 下一阶段（冲更高）：对问题自然反应；把较长信息用轻微语调起伏串起来，体现对不同部分的态度（靠多练即兴作答即可）

评分规则：
- 9分：全部语音特征精确；听者毫不费力
- 8分：广泛语音特征；口音影响极小
- 7分：整体清晰；偶有小错；听起来自然、可作强项
- 6分：基本清晰；个别发音错误不影响理解；或明显背稿/不自然
- 5分及以下：发音问题较多；听者需努力理解

## 真实考官校准（必须遵守）
综合多份模考书面反馈（含无音频报告），按档位锚定：

**6.0 档 · Jiang Yu Pei**：FC6 LR6 GRA6 **Pron7** — 发音可为强项；时态/情态/条件句小错仍 GRA6；跑题段比切题段更流利会被注意。

**6.0 档 · Yi Ru**：FC6 **LR7** GRA6 Pron6 — LR7 来自话题精准词 + 地道/native 表达（P2/P3），但整体仍以 Band6 词汇为主；GRA 有嵌入从句、偶发主谓一致错误，Part1 也说长复杂句才可冲 GRA7。

**6.0 档 · Yang Taoyi**：四项均 6 — 大量 um/uh 开场、Part2 偏短、重组/停顿正常；词形小错（complicate→complicated）不减 LR6；关系从句/嵌入从句是 GRA 强项，反身代词等基础错要清理。

**5.5 档 · Ji Peng Hao**：FC6 LR6 **GRA5** Pron6 — 「假关系从句」套话（He told me that / I remember clearly that / I wish that）会被识破；Part2 本可用定语从句却拆成两句简单句 → 典型 Band5 语法；偶发跑题一次不大幅扣 LR。

**5.5 档 · Zhang Xin Yu**：FC6 LR6 **GRA5** Pron6 — Part1/2 几乎全是 SVO + 反复 and 连接，错误少是因为句子太简单 → GRA5；LR 因搭配自然、少 Chinglish 最接近 7（不是靠高级词）。

### 分项规则（跨档位）
1. **FC**：慢但可 FC6；um/uh 每轮开头多、Part2 明显偏短 → 维持 6 难上 7。跑题/答非所问若流利度反而更好，必须点名并压住冲高。
2. **LR**：用词顺眼/很好仍常 LR6。冲 LR7：精准话题词 + 自然搭配/习语贯穿全篇，少中式英语。2–3 处难懂中式表达 → LR5。词形小错若不影响理解，通常仍 LR6。
3. **GRA**：**GRA5 强信号** — 假关系从句套话；大量 SVO+and 堆砌、几乎无 that/which/who/从句；该用定语从句却只用并列简单句。偶发时态/情态/条件句错误、结构多样且沟通清楚 → 仍可 GRA6。冲更高：第二条件句、情态动词、真关系从句/嵌入从句。
4. **Pron**：清晰自然可 Pron7；缺乏语调层次/重音提示通常仍 Pron6（非硬伤）。仅复述题目或明显背稿时封顶 6。
5. **总分**：5.5 常见 GRA 拖后腿；6.0 常见四项均衡或 Pron/LR 单项突出。反馈：肯定档位 + 点明冲高必改项。

## 反馈原则
1. 用中文反馈，涉及英文表达时保留原文
2. 每个问题说清"为什么"和"怎么改"
3. 改写建议要地道自然，像母语者说话
4. 语气温和但专业，像一个好老师/考官
5. 最终目标：帮学生提分（尤其说清 6→6.5 的卡点：切题作答 + 时态/动词清理 + 自然语调）
6. 反馈要具体，不要泛泛而谈
7. 每个分数必须有数据支撑，不要拍脑袋
8. 只输出一个合法 JSON 对象，不要 Markdown 或其它说明文字
9. FC/LR/GRA/Pron 的 band 必须是 1–9 的整数，禁止 0、禁止 0.5；overall 可以是 x.5

## 语用层面检测（重要）
除四项分数外，必须单独检测语用问题（这些问题往往决定能否从 6 冲到 6.5）：
1. **重复问题**：回答开头是否复述题目大部分内容（Band 4–5 习惯，极不自然）
2. **背诵/模板痕迹**：过于工整、书面腔、模板开头、缺少即兴口语特征
3. **中式英语（Chinglish）**：中文直译、母语者难懂、语法未必错但搭配怪
4. **切题与真实作答**：是否真正回答了题目（而非跑题闲聊）；是否听起来像在“说准备好的内容”而不是根据问题即时反应。跑题时若流利度反而更好，必须点名。
这些写入 detailed_analysis.naturalness / chinglish_flags，以及顶层 pragmatic_issues。

## 语法分析要求（重点）
语法必须单独完整列出错误清单。你必须做到：
1. **逐句扫描**，找出所有语法错误。注意：ASR 常因停顿误标问号/句号（如 Which? Was a gift. From my parents.）；若语义上可连成 which was a gift from my parents，不要当成多个残缺句，应先回拼再判断
2. 每个错误必须标注：错误类型、原文、正确形式、中文解释
3. 错误类型归类：tense / subject_verb_agreement / article / plural / preposition / word_form / sentence_structure / non_finite / subjunctive / comparative / other
4. **优先盯**：时态与问题时间是否一致；情态动词是否犹豫/误用；条件句等复杂结构是否说完整
5. **GRA5 必查**：假关系从句（He told me that / I remember clearly that / I wish that）；SVO+and 反复连接、缺少 that/which/who/从句；该合并为定语从句却用两句简单句
6. 分析句式多样性（简单句/并列句/复合句、复杂结构、均长）
7. 综合评估：水平、最大短板、最快提分方法（5.5→6 优先：真从句+第二条件句+情态动词；6→更高：时态+动词+自然语调）
8. 有错误时 errors 不得为空；**错误少但结构过于简单仍可能是 GRA5**，不要因“错得少”就给 6`;
    }

    // 语法结构预检（对齐 Ji Peng Hao / Zhang Xin Yu 等 GRA5 案例）
    analyzeGrammarStructureSignals(transcript) {
        const t = String(transcript || '');
        const sents = t.split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 4);
        const fakeRelativePatterns = [
            [/\b(he|she) told me that\b/i, 'He/She told me that（假关系从句）'],
            [/\bi remember clearly that\b/i, 'I remember clearly that（假关系从句）'],
            [/\bi wish that\b/i, 'I wish that（假关系从句）'],
            [/\bi (think|feel|guess) that\b/i, 'I think/feel that（套话式 that）']
        ];
        const fake_relative = [];
        fakeRelativePatterns.forEach(([re, label]) => {
            if (re.test(t)) fake_relative.push(label);
        });
        const realRelative = (t.match(/\b(which|who|whom|whose)\b/gi) || []).length;
        const realThatClause = (t.match(/\b(cake|thing|place|person|food|book|movie|city|country|friend|teacher)\s+that\b/gi) || []).length;
        const subordinators = (t.match(/\b(because|although|while|when|if|unless|since|whereas|even though)\b/gi) || []).length;
        const secondConditional = /\bif\s+i\s+were\b/i.test(t) || /\bwould\s+\w+/i.test(t);
        const modals = (t.match(/\b(can|could|would|should|might|must|may)\b/gi) || []).length;
        const andCount = (t.match(/\band\b/gi) || []).length;
        const sentCount = Math.max(1, sents.length);
        const andPerSent = andCount / sentCount;
        const svo_and_dominant = andCount >= 4 && andPerSent >= 1.0
            && subordinators + realRelative + realThatClause <= 1
            && sentCount >= 3;
        let simple_split = false;
        let simple_split_example = '';
        for (let i = 0; i < sents.length - 1; i++) {
            const a = sents[i];
            const b = sents[i + 1];
            const aw = a.split(/\s+/).length;
            const bw = b.split(/\s+/).length;
            if (aw <= 9 && bw <= 9 && !/\b(which|who|that)\b/i.test(a)) {
                if (/\b(it'?s|they|he|she|made|prepared|built|located)\b/i.test(b)
                    || /\bmade of\b/i.test(b)) {
                    simple_split = true;
                    simple_split_example = `${a}. ${b}`;
                    break;
                }
            }
        }
        return {
            fake_relative,
            fake_relative_count: fake_relative.length,
            realRelative,
            realThatClause,
            subordinators,
            secondConditional,
            modals,
            andCount,
            sentCount,
            svo_and_dominant,
            simple_split,
            simple_split_example
        };
    }

    // 从腾讯云 ASR（若有词级时间戳）或转录文本提取评分指标
    extractSpeakingMetrics(transcript, asrResult, durationS) {
        const detail = (asrResult && (asrResult.ResultDetail || asrResult.resultDetail
            || (asrResult.data && asrResult.data.ResultDetail))) || null;
        const allWords = [];
        const speechSpeeds = [];
        let textFromDetail = '';

        if (Array.isArray(detail) && detail.length) {
            for (const sentence of detail) {
                textFromDetail += (sentence.FinalSentence || sentence.finalSentence || '') + ' ';
                const spd = Number(sentence.SpeechSpeed ?? sentence.speechSpeed ?? 0);
                if (spd) speechSpeeds.push(spd);
                const words = sentence.Words || sentence.words || [];
                for (const w of words) {
                    const start = Number(w.OffsetStartMs ?? w.offsetStartMs ?? w.start_ms ?? 0);
                    const end = Number(w.OffsetEndMs ?? w.offsetEndMs ?? w.end_ms ?? 0);
                    allWords.push({
                        word: String(w.Word ?? w.word ?? ''),
                        start_ms: start,
                        end_ms: end,
                        duration_ms: Math.max(0, end - start)
                    });
                }
            }
        }

        const transcriptText = (transcript || textFromDetail || '').trim();
        const plainWords = transcriptText
            .split(/\s+/)
            .map(w => w.replace(/^[^A-Za-z']+|[^A-Za-z']+$/g, ''))
            .filter(Boolean);

        if (!allWords.length && plainWords.length) {
            for (const w of plainWords) {
                allWords.push({ word: w, start_ms: 0, end_ms: 0, duration_ms: 0 });
            }
        }

        let totalDurationS = Number(durationS) || 0;
        if (allWords.length && allWords[0].end_ms) {
            const fromTs = (allWords[allWords.length - 1].end_ms - allWords[0].start_ms) / 1000;
            if (fromTs > 0.5) totalDurationS = fromTs;
        }
        if ((!totalDurationS || totalDurationS < 0.5) && this.lastRecordingDurationS > 0.5) {
            totalDurationS = this.lastRecordingDurationS;
        }

        const totalWords = allWords.length || plainWords.length;
        const wpm = totalDurationS > 0 ? Math.round((totalWords / (totalDurationS / 60)) * 10) / 10 : 0;

        const longPauses = [];
        for (let i = 1; i < allWords.length; i++) {
            if (!allWords[i].start_ms && !allWords[i - 1].end_ms) continue;
            const gap = allWords[i].start_ms - allWords[i - 1].end_ms;
            if (gap > 1500) {
                longPauses.push({
                    after_word: allWords[i - 1].word,
                    before_word: allWords[i].word,
                    gap_ms: gap
                });
            }
        }

        const fillerSet = new Set(['um', 'uh', 'er', 'ah', 'eh', 'hmm', 'like', 'you know', 'i mean']);
        const wordsLower = allWords.map(w => String(w.word || '').toLowerCase().replace(/[.,!?]/g, ''));
        let fillerCount = 0;
        for (let i = 0; i < wordsLower.length; i++) {
            const w = wordsLower[i];
            const two = `${w} ${wordsLower[i + 1] || ''}`;
            if (fillerSet.has(w) || fillerSet.has(two.trim())) fillerCount += 1;
        }
        const fillerPerMin = totalDurationS > 0 ? Math.round((fillerCount / (totalDurationS / 60)) * 10) / 10 : 0;

        const skipRepeat = new Set(['the', 'a', 'an', 'is', 'was', 'and', 'to', 'of']);
        const repetitions = [];
        for (let i = 1; i < wordsLower.length; i++) {
            if (wordsLower[i] && wordsLower[i] === wordsLower[i - 1] && !skipRepeat.has(wordsLower[i])) {
                repetitions.push(wordsLower[i]);
            }
        }

        const wordDurationIssues = [];
        for (const w of allWords) {
            const charCount = String(w.word || '').length;
            if (!charCount || !w.duration_ms) continue;
            const msPerChar = w.duration_ms / charCount;
            if (msPerChar > 300) wordDurationIssues.push(`'${w.word}' 发音拖长(${w.duration_ms}ms)`);
            else if (msPerChar < 30 && charCount > 3) wordDurationIssues.push(`'${w.word}' 可能吞音(${w.duration_ms}ms)`);
        }

        const connectives = [
            'however', 'therefore', 'furthermore', 'moreover', 'in addition',
            'on the other hand', 'for example', 'for instance', 'in contrast',
            'as a result', 'in conclusion', 'firstly', 'secondly', 'finally',
            'although', 'despite', 'because', 'since', 'so', 'but', 'and',
            'well', 'actually', 'basically', 'honestly', 'generally'
        ];
        const lower = transcriptText.toLowerCase();
        const foundConnectives = connectives.filter(c => lower.includes(c));

        const commonHomophones = {
            their: ['there', "they're"], there: ['their', "they're"],
            think: ['sink', 'thing'], sink: ['think'],
            beach: ['bitch', 'peach'], sheet: ['shit'],
            walk: ['work'], work: ['walk'],
            bad: ['bed', 'bat'], bed: ['bad', 'bat'],
            very: ['vary', 'berry'], really: ['rarely']
        };
        const suspiciousWords = [];
        for (const w of wordsLower) {
            if (commonHomophones[w]) {
                suspiciousWords.push(`'${w}' 可能是 ${commonHomophones[w].join('/')} 的误识别`);
            }
        }

        return {
            transcript: transcriptText,
            total_words: totalWords,
            total_duration_s: Math.round(totalDurationS * 10) / 10,
            wpm,
            avg_speech_speed: speechSpeeds.length
                ? Math.round((speechSpeeds.reduce((a, b) => a + b, 0) / speechSpeeds.length) * 10) / 10
                : 0,
            long_pauses: longPauses,
            long_pause_count: longPauses.length,
            filler_count: fillerCount,
            filler_per_min: fillerPerMin,
            repetitions,
            word_duration_issues: wordDurationIssues,
            connectives_found: foundConnectives,
            connectives_count: foundConnectives.length,
            suspicious_words: suspiciousWords,
            has_word_timestamps: !!(Array.isArray(detail) && detail.length && allWords.some(w => w.duration_ms > 0))
        };
    }

    getUsedWordChips() {
        try {
            const transcript = this.transcript + (this.currentInterim || '');
            if (transcript.trim()) {
                return this.syncWordChipsWithTranscript(transcript).chips;
            }
            return Array.from(document.querySelectorAll('.word-chip.used'))
                .map(el => (el.getAttribute('data-word') || el.textContent || '').trim())
                .filter(Boolean);
        } catch (e) {
            return [];
        }
    }

    // 考官习惯信号：复述题目 / 模板感 / 中式英语（对齐真实考官反馈）
    buildExaminerSignals(question, transcript) {
        const qNorm = this.normalizeChunkText(question).replace(/^(have you|do you|did you|are you|is there|what|where|when|why|how|would you|can you)\s+/i, '');
        const tNorm = this.normalizeChunkText(transcript);
        const firstSent = (String(transcript || '').split(/[.!?]+/).map(s => s.trim()).find(Boolean) || '');
        const firstNorm = this.normalizeChunkText(firstSent);

        let question_echo = false;
        let echo_excerpt = '';
        if (qNorm.length >= 12 && firstNorm.length >= 10) {
            const qTokens = qNorm.split(' ').filter(w => w.length > 2 && !/^(the|and|you|your|have|ever|before|about|with|from|this|that|what|when|where|why|how)$/.test(w));
            const hit = qTokens.filter(w => firstNorm.includes(w)).length;
            const ratio = qTokens.length ? hit / qTokens.length : 0;
            if (ratio >= 0.55 && hit >= 3) {
                question_echo = true;
                echo_excerpt = firstSent.slice(0, 120);
            }
        }

        const formulaic_hits = [];
        const formulaPatterns = [
            [/for the reason that/i, 'for the reason that（模板感强）'],
            [/i am a big fan of/i, 'I am a big fan of'],
            [/it is cheerful and enjoyable for me to/i, 'It is cheerful and enjoyable for me to'],
            [/can be seen as the best way/i, 'can be seen as the best way'],
            [/whenever i have (some days off|spare time)/i, 'Whenever I have spare time/days off'],
            [/yes,?\s+absolutely,?\s+absolutely/i, 'Yes, absolutely 重复']
        ];
        formulaPatterns.forEach(([re, label]) => {
            if (re.test(transcript || '')) formulaic_hits.push(label);
        });
        const formulaic = formulaic_hits.length >= 2 || (question_echo && formulaic_hits.length >= 1);

        const chinglish = [];
        const chinglishPatterns = [
            [/\bhonest food\b/i, 'honest food（疑似中式直译）'],
            [/\bmake people fun\b/i, 'make people fun'],
            [/\bfeel loose\b/i, 'feel loose'],
            [/\bsome happy\b/i, 'some happy'],
            [/\bgave me some happy\b/i, 'gave me some happy'],
            [/\bopen the eyes?\b/i, 'open the eye(s)'],
            [/\blisten a\b/i, 'listen a（缺 to）'],
            [/\bwith the development of\b/i, 'with the development of（套话）']
        ];
        chinglishPatterns.forEach(([re, label]) => {
            if (re.test(transcript || '')) chinglish.push(label);
        });

        const grammar_structure = this.analyzeGrammarStructureSignals(transcript);
        const heavyUmStart = /^(um+|uh+|er+)\b/i.test(String(transcript || '').trim())
            || (String(transcript || '').match(/\b(um|uh|er)\b/gi) || []).length >= 5;

        let scoring_hint = '按实际表现评分；锚定：6.0 常见 FC/LR/GRA 6（Pron 或 LR 可单项到 7）；5.5 常见 GRA5';
        if (grammar_structure.svo_and_dominant || grammar_structure.fake_relative_count >= 2) {
            scoring_hint = 'SVO+and 堆砌或假关系从句：GRA 倾向 5（Zhang/Ji 模考案例）；FC/LR 仍可 6';
        } else if (grammar_structure.fake_relative_count >= 1 || grammar_structure.simple_split) {
            scoring_hint = '假关系从句或回避真定语从句：GRA 倾向 5；建议第二条件句+情态动词+that/which/who';
        } else if (question_echo && chinglish.length >= 2) {
            scoring_hint = '复述题目+多处中式表达：FC 可 6 但点名不自然；LR 倾向 5；Pron 因复述题目封顶 6';
        } else if (question_echo) {
            scoring_hint = '开场复述题目：FC 可给 6，但必须指出这是冲 6.5 障碍；Pron 因不自然封顶 6';
        } else if (chinglish.length >= 2) {
            scoring_hint = '多处疑似中式英语：LR 应给 5；Pron 仍可按清晰度给 6–7';
        } else if (chinglish.length === 0 && !formulaic && (transcript || '').split(/\s+/).length >= 35) {
            scoring_hint = '搭配较自然、少中式英语：LR 可冲 7（Yi Ru 模考路径），但勿因词多就抬分';
        } else if (formulaic && formulaic_hits.length >= 3) {
            scoring_hint = '模板感很强：Pron 倾向 6；反馈要求更自然/即兴、对问题即时反应';
        } else if (formulaic) {
            scoring_hint = '略有模板痕迹：Pron 仍可给 7（若整体清晰自然）；提醒用真实细节与自然语调';
        }
        if (heavyUmStart) {
            scoring_hint += '；大量 um/uh 开场（Yang 模考）：FC 维持 6，难上 7';
        }

        return {
            question_echo,
            echo_excerpt,
            formulaic,
            formulaic_hits,
            chinglish,
            grammar_structure,
            heavy_um_start: heavyUmStart,
            scoring_hint
        };
    }

    // 构建评分提示词（对齐 ielts-speaking-prompt.md）
    buildEvaluationPrompt(cat, q, transcript, metrics) {
        const m = metrics || this.extractSpeakingMetrics(transcript, this.lastAsrResult, this.lastRecordingDurationS);
        let pauseLines = '';
        if (m.long_pauses && m.long_pauses.length) {
            pauseLines = m.long_pauses.slice(0, 5).map(p =>
                `  · '${p.after_word}' → '${p.before_word}' 之间停顿${(p.gap_ms / 1000).toFixed(1)}秒`
            ).join('\n') + '\n';
        }
        let durationIssues = '';
        if (m.word_duration_issues && m.word_duration_issues.length) {
            durationIssues = '\n### 发音相关信号（词时长异常）\n'
                + m.word_duration_issues.slice(0, 5).map(x => `- ${x}`).join('\n') + '\n';
        }
        let suspicious = '';
        if (m.suspicious_words && m.suspicious_words.length) {
            suspicious = '\n### 发音相关信号（可能的语音识别异常）\n'
                + m.suspicious_words.slice(0, 5).map(x => `- ${x}`).join('\n') + '\n';
        }
        const repLine = m.repetitions && m.repetitions.length
            ? `- 连续重复词: ${m.repetitions.slice(0, 5).join(', ')}\n`
            : '';
        const tsNote = m.has_word_timestamps
            ? ''
            : '\n（说明：当前 ASR 未返回词级时间戳，长停顿/词时长信号可能为空；请主要依据转录、语速、填充词与连接词评分。）\n';
        const usedChips = this.getUsedWordChips();
        const chipNote = usedChips.length
            ? `\n## 学生勾选的提示词块（练习辅助，不是扣分项）\n学生练习时点选了这些词块：${usedChips.join(', ')}\n评分时：若转录中确实用到了这些表达，可在 LR/FC 中认可；不要因为“没用词块”扣分；也不要仅因点选了词块就抬高分数，以实际说出的话为准。\n`
            : '\n## 学生勾选的提示词块\n（未勾选或未记录）评分只看实际口述转录，不要因为没用词块扣分。\n';
        const examSignals = this.buildExaminerSignals(q.q || q.title || '', m.transcript || transcript);

        return `请评估以下学生的雅思口语 PART1 回答。
重要：
- FC/LR/GRA/Pron 的 band 必须是 1–9 的整数（禁止 0，禁止 0.5）
- overall 可以是 0.5 间隔（四项平均后 .25进.5，.75进整）
- 按真实考官多份模考校准（6.0：Jiang/Yi Ru/Yang；5.5：Ji Peng Hao/Zhang Xin Yu）：GRA5 强信号=假关系从句、SVO+and 堆砌、回避定语从句；LR7=自然搭配+话题精准词；Pron 可 7；um/uh 多 FC 难上 7
- 语法错误必须列入 errors；错误少但结构过简仍可能是 GRA5；冲 5.5→6 优先：that/which/who、第二条件句、情态动词
- 禁止照抄示例数字

## 考试题目
${q.q}
题目类型：${cat.name}
${chipNote}
## 学生回答转录
${m.transcript || transcript}

## 考官习惯信号（本地预检，请重点核验）
- 开场复述题目: ${examSignals.question_echo ? '是（不自然，类似 Band 4 习惯）' : '否'}
${examSignals.echo_excerpt ? `  · 疑似复述片段: 「${examSignals.echo_excerpt}」\n` : ''}- 模板/背稿感: ${examSignals.formulaic ? '偏强' : '不明显'}
${examSignals.formulaic_hits.length ? `  · 信号: ${examSignals.formulaic_hits.join('；')}\n` : ''}- 疑似中式英语/怪搭配: ${examSignals.chinglish.length ? examSignals.chinglish.join('；') : '未检出'}
- 语法结构预检: 假关系从句=${examSignals.grammar_structure && examSignals.grammar_structure.fake_relative_count ? examSignals.grammar_structure.fake_relative.join('；') : '无'}；SVO+and 堆砌=${examSignals.grammar_structure && examSignals.grammar_structure.svo_and_dominant ? '是（GRA 倾向 5）' : '否'}；真关系从句(which/who)=${examSignals.grammar_structure ? examSignals.grammar_structure.realRelative : 0}；第二条件句=${examSignals.grammar_structure && examSignals.grammar_structure.secondConditional ? '有' : '无'}
${examSignals.grammar_structure && examSignals.grammar_structure.simple_split ? `  · 简单句拆分（可合并为定语从句）: 「${examSignals.grammar_structure.simple_split_example}」\n` : ''}- um/uh 偏多: ${examSignals.heavy_um_start ? '是（FC 难上 7）' : '否'}
- 预检建议: ${examSignals.scoring_hint}

## 语音量化指标

### 基础数据
- 总词数: ${m.total_words}
- 总时长: ${m.total_duration_s}秒
- 语速: ${m.wpm} WPM（参考：100-140为正常，<90偏慢，>160偏快）
${tsNote}
### 流利度信号
- 超过1.5秒的长停顿: ${m.long_pause_count}次
${pauseLines}- 填充词(um/uh/er等): ${m.filler_count}次，每分钟${m.filler_per_min}次
${repLine}
### 连贯性信号
- 检测到的连接词: ${m.connectives_found.length ? m.connectives_found.join(', ') : '无'}
- 连接词种类数: ${m.connectives_count}
${durationIssues}${suspicious}
## 请你完成以下任务

### 1. 四项评分（每项 1–9 整数；禁止 0.5）

**流利度与连贯性 (FC)**：
- 流利度：语速、长停顿、填充词、重复；慢但可 FC6
- 大量 um/uh 每轮开头、Part2 明显偏短 → FC6 难上 7（Yang Taoyi）
- 连贯性：连接词、逻辑、话题展开、是否真正答到题目
- 若开场复述题目：指出不自然；FC 可给 6，但要说明这是冲 6.5 的障碍
- 若跑题段落比切题段落更流利：点名并保持 FC≤6

**词汇资源 (LR)**：
- 多样性、搭配、习语、释义
- 冲 LR7：自然搭配/习语 + 话题精准词贯穿全篇（Yi Ru），不是靠堆高级词
- 搭配自然、少 Chinglish 可最接近 7（Zhang Xin Yu）；用词顺眼仍常 LR6
- 严查中式直译/奇怪搭配；2–3 处难懂表达应给 5；词形小错通常仍 LR6

**语法范围与准确性 (GRA)**：
- 逐句找错并列入 errors（含残缺句）
- **GRA5 强信号**：假关系从句（He told me that / I remember clearly that / I wish that）；大量 SVO+and、几乎无 that/which/who；该用定语从句却两句简单句（Ji Peng Hao）
- 时态/情态/条件句小错、结构多样且沟通清楚 → 仍可 GRA6
- 冲 5.5→6：第二条件句、情态动词、真关系从句/嵌入从句

**发音 (P)**：
- 间接证据 + 是否像背稿/不自然
- 清晰自然可作为强项给 7（对齐真实模考 Pron7）
- 开场复述题目或明显模板堆砌 → 封顶 6；仅轻微模板痕迹不自动压分

### 2. 总分
四项整数平均后，.25进.5，.75进整（总分可以是 x.5）

### 3. 每个单项的详细解析
每个维度除了分数，还要有完整的 detailed_analysis。
FC 必须含 naturalness；LR 必须含 chinglish_flags；语法 errors 单独完整列出。
每个维度 justification 请写清：当前为何是这个整数分，以及若想更高最该改什么。

### 4. 语用问题 pragmatic_issues（必须输出）
单独汇总：repeats_question / sounds_rehearsed / chinglish_expressions；并检查是否切题、是否像真实作答。

### 5. 主要问题（最多5个，按影响程度排序）
优先列入：假关系从句、SVO+and 堆砌、答非所问/跑题、复述题目、时态与题干不符、中式英语、背稿不自然等考官最常抓的点。

### 6. 7分改写版本
把学生回答改写成7分水平的地道英文口语，保持原意；开场不要复述题目；时态与问题时间对齐

## 输出格式（严格JSON，不要输出其他内容）
注意：下面 JSON 里的数字只是字段示意；band 填整数；按真实表现评分。

{
  "scores": {
    "fluency_coherence": {
      "band": 6,
      "justification": "中文，引用具体数据",
      "detailed_analysis": {
        "fluency": {
          "wpm": 0,
          "wpm_assessment": "语速评价",
          "long_pauses": 0,
          "pause_assessment": "停顿评价",
          "filler_words_per_min": 0,
          "filler_assessment": "填充词评价",
          "repetitions_found": ["重复词1"],
          "repetition_assessment": "重复评价"
        },
        "coherence": {
          "connectives_used": ["连接词1"],
          "connectives_count": 0,
          "connectives_assessment": "连接词评价",
          "topic_development": "话题展开",
          "coherence_issues": ["问题1"]
        },
        "naturalness": {
          "repeats_question": false,
          "repetition_evidence": "复述证据或空字符串",
          "sounds_rehearsed": false,
          "rehearsal_evidence": "背稿/模板证据或空字符串",
          "assessment": "自然度评价：是否像即兴"
        },
        "summary": "FC综合诊断"
      }
    },
    "lexical_resource": {
      "band": 6,
      "justification": "中文",
      "detailed_analysis": {
        "vocabulary_diversity": {
          "assessment": "多样性评价",
          "overused_words": [{"word": "词", "count": 0, "alternatives": ["替1"]}],
          "basic_words_overused": ["good"]
        },
        "collocation": {
          "errors": [{"wrong": "错搭配", "correct": "正确", "explanation": "中文"}],
          "assessment": "搭配评价"
        },
        "idiomatic_language": {
          "idioms_found": [],
          "assessment": "习语评价"
        },
        "chinglish_flags": [
          {
            "expression": "中式英语原文",
            "likely_intended": "学生可能想表达的意思",
            "natural_alternative": "地道英文",
            "severity": "high|medium|low"
          }
        ],
        "paraphrase_ability": "释义能力",
        "summary": "LR综合诊断"
      }
    },
    "grammar": {
      "band": 6,
      "justification": "中文",
      "detailed_analysis": {
        "errors": [
          {
            "original": "错误原文",
            "correction": "正确形式",
            "type": "tense|subject_verb_agreement|article|plural|preposition|word_form|sentence_structure|non_finite|subjunctive|comparative|other",
            "explanation": "中文解释",
            "severity": "high|medium|low"
          }
        ],
        "error_statistics": {
          "total_errors": 0,
          "most_frequent_error": "",
          "error_density_per_100_words": 0.0
        },
        "sentence_variety": {
          "simple_sentences": 0,
          "compound_sentences": 0,
          "complex_sentences": 0,
          "complex_sentence_ratio": 0.0,
          "avg_sentence_length_words": 0.0,
          "structures_used": [],
          "structures_missing": [],
          "assessment": "句式多样性评价"
        },
        "summary": "GRA综合诊断"
      }
    },
    "pronunciation": {
      "band": 6,
      "justification": "中文，说明推断依据",
      "detailed_analysis": {
        "signals_found": [],
        "word_duration_issues": [],
        "asr_anomalies": [],
        "intonation_note": "若无音频语调数据，根据模板感/自然度间接说明",
        "assessment": "发音综合评估"
      }
    },
    "overall": 6.0
  },
  "pragmatic_issues": {
    "repeats_question": {
      "detected": false,
      "evidence": "",
      "impact": "对分数/冲高的影响",
      "fix": "怎么改"
    },
    "sounds_rehearsed": {
      "detected": false,
      "evidence": "",
      "impact": "",
      "fix": ""
    },
    "chinglish_expressions": [
      {
        "expression": "",
        "intended_meaning": "",
        "natural_alternative": "",
        "severity": "high|medium|low"
      }
    ]
  },
  "problems": [
    {
      "rank": 1,
      "category": "fluency|vocabulary|grammar|pronunciation|pragmatic",
      "issue": "问题描述（中文）",
      "why_it_matters": "为什么影响分数（中文）",
      "how_to_fix": "怎么改（中文）",
      "example": "更好的英文示例"
    }
  ],
  "improved_answer": {
    "original_summary": "学生原意的一句话概括（中文）",
    "rewritten_version": "7分水平的地道英文改写",
    "improvements_made": ["改进点1", "改进点2", "改进点3"]
  }
}`;
    }
    
    // 渲染 AI 评分结果（优先 JSON）
    renderAIResult(aiResponse, evalKey = null) {
        const parsed = this.parseAIEvaluation(aiResponse);
        const html = this.renderScoreHTML(parsed);
        const key = evalKey || this.currentQuestionKey();
        if (key) {
            const prev = this.questionSessions[key] || {};
            this.questionSessions[key] = {
                ...prev,
                transcript: parsed.transcript || prev.transcript || this.transcript || '',
                aiHtml: html,
                aiVisible: true,
                aiEvaluateEnabled: true,
                feedbackVisible: true
            };
        }
        // 已切到别的题：只写入缓存，不覆盖当前页
        if (key && key !== this.currentQuestionKey()) {
            this.reportScoreToParent(parsed);
            return;
        }
        const contentDiv = document.getElementById('resultContent');
        const resultDiv = document.getElementById('aiResult');
        if (contentDiv) contentDiv.innerHTML = html;
        if (resultDiv) resultDiv.style.display = 'block';
        this.reportScoreToParent(parsed);
        this.setPracticeButtonMode('again');
        this.persistLoadedQuestionSession();
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
    
    // 单项分：1–9 整数；0/空/0.5 视为无效后取整或回落
    pickBandScore(v, fallback = 5) {
        const toInt = (x) => Math.max(1, Math.min(9, Math.round(Number(x))));
        const n = Number(v);
        if (!isNaN(n) && n > 0) return toInt(n);
        const f = Number(fallback);
        if (!isNaN(f) && f > 0) return toInt(f);
        return 5;
    }

    // 雅思 overall：四项平均后 .25 进 .5，.75 进整
    ieltsOverallRound(avg) {
        const n = Number(avg);
        if (isNaN(n)) return 0;
        const floored = Math.floor(n);
        const decimal = n - floored;
        if (decimal < 0.25) return floored;
        if (decimal < 0.75) return floored + 0.5;
        return floored + 1;
    }

    bandScoreFromNode(node) {
        if (node == null) return null;
        if (typeof node === 'number' || typeof node === 'string') return Number(node);
        if (typeof node === 'object') {
            return Number(node.band ?? node.score ?? node.value ?? NaN);
        }
        return null;
    }

    justificationFromNode(node, extraKeys = []) {
        if (!node || typeof node !== 'object') return '';
        const parts = [];
        if (node.justification) parts.push(String(node.justification));
        for (const k of extraKeys) {
            if (node[k]) parts.push(String(node[k]));
        }
        return parts.filter(Boolean).join(' ');
    }

    // 从 AI 返回中提取结构化评分（兼容新旧 JSON）
    parseAIEvaluation(aiResponse) {
        let raw = aiResponse;
        if (typeof raw !== 'string') raw = JSON.stringify(raw);
        raw = String(raw || '').trim();
        
        let data = null;
        try { data = JSON.parse(raw); } catch (e) {}
        if (!data) {
            const m = raw.match(/\{[\s\S]*\}/);
            if (m) {
                try { data = JSON.parse(m[0]); } catch (e) {}
            }
        }
        
        const transcript = this.transcript || '';
        let fluency = null, vocabulary = null, grammar = null, pronunciation = null;
        let reasons = { fluency: '', vocabulary: '', grammar: '', pronunciation: '' };
        let strengths = [], weaknesses = [], suggestions = [], sampleAnswer = '';
        let problems = [];
        let improvedMeta = null;
        let aiOverall = null;
        let detailed = { fluency: null, vocabulary: null, grammar: null, pronunciation: null };
        let pragmaticIssues = null;
        
        if (data && typeof data === 'object') {
            const scores = data.scores || data;
            const fc = scores.fluency_coherence || scores.fluency || scores.Fluency;
            const lr = scores.lexical_resource || scores.vocabulary || scores.Vocabulary || scores.lexical;
            const gra = scores.grammar || scores.Grammar || scores.grammatical_range;
            const pron = scores.pronunciation || scores.Pronunciation;

            fluency = this.bandScoreFromNode(fc);
            vocabulary = this.bandScoreFromNode(lr);
            grammar = this.bandScoreFromNode(gra);
            pronunciation = this.bandScoreFromNode(pron);
            aiOverall = scores.overall ?? data.overall ?? null;

            detailed.fluency = (fc && fc.detailed_analysis) || null;
            detailed.vocabulary = (lr && lr.detailed_analysis) || null;
            detailed.grammar = (gra && gra.detailed_analysis) || null;
            detailed.pronunciation = (pron && pron.detailed_analysis) || null;
            pragmaticIssues = data.pragmatic_issues || data.pragmaticIssues || null;

            if (fc && typeof fc === 'object') {
                reasons.fluency = this.summarizeFcReason(fc);
            }
            if (lr && typeof lr === 'object') {
                reasons.vocabulary = this.summarizeLrReason(lr);
            }
            if (gra && typeof gra === 'object') {
                reasons.grammar = this.summarizeGrammarReason(gra);
            }
            if (pron && typeof pron === 'object') {
                reasons.pronunciation = this.summarizePronReason(pron);
            }

            const legacyReasons = data.reasons || data.reason || {};
            reasons.fluency = reasons.fluency || legacyReasons.fluency || legacyReasons.Fluency || '';
            reasons.vocabulary = reasons.vocabulary || legacyReasons.vocabulary || legacyReasons.Vocabulary || legacyReasons.lexical || '';
            reasons.grammar = reasons.grammar || legacyReasons.grammar || legacyReasons.Grammar || '';
            reasons.pronunciation = reasons.pronunciation || legacyReasons.pronunciation || legacyReasons.Pronunciation || '';

            strengths = Array.isArray(data.strengths) ? data.strengths : [];
            weaknesses = Array.isArray(data.weaknesses) ? data.weaknesses : [];
            suggestions = Array.isArray(data.suggestions) ? data.suggestions : [];
            problems = Array.isArray(data.problems) ? data.problems : [];

            const improved = data.improved_answer || data.improvedAnswer;
            if (improved && typeof improved === 'object') {
                improvedMeta = improved;
                sampleAnswer = improved.rewritten_version || improved.rewrittenVersion || '';
                if (Array.isArray(improved.improvements_made)) {
                    suggestions = suggestions.length ? suggestions : improved.improvements_made;
                }
            } else {
                sampleAnswer = data.sample_answer || data.sampleAnswer || '';
            }
        } else {
            const extractScore = (patterns) => {
                for (const p of patterns) {
                    const m = raw.match(p);
                    if (m) {
                        const n = parseFloat(m[1]);
                        if (!isNaN(n) && n >= 0 && n <= 9) return n;
                    }
                }
                return null;
            };
            fluency = extractScore([/Fluency(?:\s*&\s*Coherence)?[^\d]{0,20}([\d.]+)/i, /流利度[^\d]{0,10}([\d.]+)/i]);
            vocabulary = extractScore([/Vocabulary[^\d]{0,20}([\d.]+)/i, /Lexical[^\d]{0,20}([\d.]+)/i, /词汇[^\d]{0,10}([\d.]+)/i]);
            grammar = extractScore([/Grammar[^\d]{0,20}([\d.]+)/i, /Grammatical[^\d]{0,30}([\d.]+)/i, /语法[^\d]{0,10}([\d.]+)/i]);
            pronunciation = extractScore([/Pronunciation[^\d]{0,20}([\d.]+)/i, /发音[^\d]{0,10}([\d.]+)/i]);
        }

        // 无论 AI 是否返回，都补本地可检出语法错误，并单独列出
        const graNode = (data && data.scores && data.scores.grammar) || (data && data.grammar) || null;
        detailed.grammar = this.mergeGrammarDetailedAnalysis(detailed.grammar, graNode, transcript);
        reasons.grammar = this.summarizeGrammarReason({
            ...(graNode && typeof graNode === 'object' ? graNode : {}),
            detailed_analysis: detailed.grammar
        });
        
        const lengthFallback = this.estimateLengthFallbackScore(transcript);
        const pronFallback = Math.min(this.estimatePronunciationScore(transcript), Math.max(lengthFallback, 6));
        fluency = this.pickBandScore(fluency, lengthFallback);
        vocabulary = this.pickBandScore(vocabulary, lengthFallback);
        grammar = this.pickBandScore(grammar, lengthFallback);
        pronunciation = this.pickBandScore(pronunciation, pronFallback);

        // 对齐真实考官：残缺句很多才压到 ≤5；偶发错误且结构够用仍可 6
        const grammarErrorCount = this.countGrammarErrors(detailed.grammar);
        const highSeverityGrammar = (detailed.grammar && Array.isArray(detailed.grammar.errors))
            ? detailed.grammar.errors.filter(e => String(e.severity || '').toLowerCase() === 'high' || e.type === 'sentence_structure').length
            : 0;
        if (grammarErrorCount >= 4 || highSeverityGrammar >= 3) grammar = Math.min(grammar, 5);
        else if (grammarErrorCount >= 3) grammar = Math.min(grammar, 6);

        const qText = (this._evalContext && this._evalContext.q && (this._evalContext.q.q || this._evalContext.q.title)) || '';
        const examSignals = this.buildExaminerSignals(qText, transcript);
        const gs = examSignals.grammar_structure || {};
        // GRA5：假关系从句 / SVO+and 堆砌 / 回避定语从句（Ji Peng Hao、Zhang Xin Yu 模考）
        if (gs.svo_and_dominant || gs.fake_relative_count >= 2) {
            grammar = Math.min(grammar, 5);
        } else if (gs.fake_relative_count >= 1 || gs.simple_split) {
            grammar = Math.min(grammar, 5);
        } else if (gs.andCount >= 3 && gs.realRelative + gs.realThatClause + gs.subordinators === 0 && gs.sentCount >= 2) {
            grammar = Math.min(grammar, 5);
        }
        // 复述题目：不直接打到 4，但封顶 6（考官：OK for 6，但挡更高）
        if (examSignals.question_echo) fluency = Math.min(fluency, 6);
        // um/uh 偏多：FC 难上 7
        if (examSignals.heavy_um_start) fluency = Math.min(fluency, 6);
        // 多处中式英语：LR 5（考官明确阈值）
        if (examSignals.chinglish.length >= 2) vocabulary = Math.min(vocabulary, 5);
        // 模板/背稿感：仅复述题目或模板信号很强时压 Pron；轻微模板不阻止 Pron7
        const heavyFormulaic = examSignals.formulaic && (examSignals.formulaic_hits || []).length >= 3;
        if (examSignals.question_echo || heavyFormulaic) pronunciation = Math.min(pronunciation, 6);

        const capped = this.clampScoresForShortAnswer(transcript, {
            fluency, vocabulary, grammar, pronunciation
        });
        fluency = capped.fluency;
        vocabulary = capped.vocabulary;
        grammar = capped.grammar;
        pronunciation = capped.pronunciation;
        
        // 优先保留 AI 本维评语；仅在空/过短/明显串台时才用本地兜底
        reasons.fluency = this.resolveDimensionReason('fluency', reasons.fluency, transcript, fluency);
        reasons.vocabulary = this.resolveDimensionReason('lexical', reasons.vocabulary, transcript, vocabulary);
        reasons.grammar = this.resolveDimensionReason('grammar', reasons.grammar, transcript, grammar);
        reasons.pronunciation = this.resolveDimensionReason('pronunciation', reasons.pronunciation, transcript, pronunciation);

        // 语用层：合并 AI + 本地预检；并写入 problems（若未覆盖）
        pragmaticIssues = this.mergePragmaticIssues(pragmaticIssues, examSignals, detailed);
        problems = this.mergeExaminerProblems(problems, examSignals, transcript);
        // 把 FC naturalness / LR chinglish 补进 detailed（本地检出而 AI 缺失时）
        detailed.fluency = this.ensureNaturalnessInFc(detailed.fluency, examSignals, pragmaticIssues);
        detailed.vocabulary = this.ensureChinglishInLr(detailed.vocabulary, examSignals, pragmaticIssues);
        reasons.fluency = this.appendPragmaticToFcReason(reasons.fluency, pragmaticIssues);
        reasons.vocabulary = this.appendPragmaticToLrReason(reasons.vocabulary, pragmaticIssues);
        
        strengths = this.filterGroundedList(strengths, transcript);
        weaknesses = this.filterGroundedList(weaknesses, transcript);
        suggestions = Array.isArray(suggestions)
            ? suggestions.map(x => String(x || '').trim()).filter(Boolean).slice(0, 5)
            : [];

        // 从 problems 补 weaknesses / suggestions
        if (problems.length) {
            if (!weaknesses.length) {
                weaknesses = problems.slice(0, 4).map(p => {
                    if (!p || typeof p !== 'object') return String(p);
                    return p.issue || '';
                }).filter(Boolean);
            }
            if (!suggestions.length) {
                suggestions = problems.slice(0, 4).map(p => {
                    if (!p || typeof p !== 'object') return '';
                    return p.how_to_fix || '';
                }).filter(Boolean);
            }
        }
        
        const avg = (fluency + vocabulary + grammar + pronunciation) / 4;
        let overallNum = this.ieltsOverallRound(avg);
        if (aiOverall != null && !isNaN(Number(aiOverall))) {
            // 优先用我们按官方规则重算，避免模型 overall 与单项不一致
            overallNum = this.ieltsOverallRound(avg);
        }
        const maxOverall = this.maxOverallForTranscript(transcript);
        if (overallNum > maxOverall) overallNum = maxOverall;
        const overall = overallNum.toFixed(1);
        
        // 示范：优先 AI 7 分改写；没有则用本题词块示范
        const tipSample = this.buildSampleFromTips(
            (this._evalContext && this._evalContext.cat) || this.data.categories[this.currentCategoryIndex],
            (this._evalContext && this._evalContext.q) || this.data.categories[this.currentCategoryIndex].questions[this.currentQuestionIndex]
        );
        if (!sampleAnswer) sampleAnswer = tipSample.text;
        const tipMeta = tipSample;
        
        return {
            fluency: String(fluency),
            vocabulary: String(vocabulary),
            grammar: String(grammar),
            pronunciation: String(pronunciation),
            overall,
            reasons,
            detailed,
            pragmaticIssues,
            strengths,
            weaknesses,
            suggestions,
            problems,
            improvedMeta,
            sampleAnswer,
            tipMeta,
            transcript
        };
    }

    mergePragmaticIssues(aiPragmatic, examSignals, detailed) {
        const base = (aiPragmatic && typeof aiPragmatic === 'object') ? { ...aiPragmatic } : {};
        const nat = detailed && detailed.fluency && detailed.fluency.naturalness;
        const chFromLr = detailed && detailed.vocabulary && Array.isArray(detailed.vocabulary.chinglish_flags)
            ? detailed.vocabulary.chinglish_flags : [];

        const repeats = base.repeats_question && typeof base.repeats_question === 'object'
            ? { ...base.repeats_question } : {};
        if (examSignals.question_echo || (nat && nat.repeats_question)) {
            repeats.detected = true;
            repeats.evidence = repeats.evidence
                || (nat && nat.repetition_evidence)
                || examSignals.echo_excerpt
                || '开场疑似复述题目';
            repeats.impact = repeats.impact
                || '考官认为这极不自然；FC 可仍是 6，但会挡住 6.5+';
            repeats.fix = repeats.fix
                || '直接作答，不要把题目整句说回去。';
        } else {
            repeats.detected = !!repeats.detected;
            repeats.evidence = repeats.evidence || '';
            repeats.impact = repeats.impact || '';
            repeats.fix = repeats.fix || '';
        }

        const rehearsed = base.sounds_rehearsed && typeof base.sounds_rehearsed === 'object'
            ? { ...base.sounds_rehearsed } : {};
        if (examSignals.formulaic || (nat && nat.sounds_rehearsed)) {
            rehearsed.detected = true;
            rehearsed.evidence = rehearsed.evidence
                || (nat && nat.rehearsal_evidence)
                || (examSignals.formulaic_hits && examSignals.formulaic_hits.join('；'))
                || '模板/背稿感偏强';
            rehearsed.impact = rehearsed.impact
                || '听起来过度准备会拉低自然度，发音项难以上 6.5–7';
            rehearsed.fix = rehearsed.fix
                || '减少套句，用真实细节即兴回答；答完后练追问。';
        } else {
            rehearsed.detected = !!rehearsed.detected;
            rehearsed.evidence = rehearsed.evidence || '';
            rehearsed.impact = rehearsed.impact || '';
            rehearsed.fix = rehearsed.fix || '';
        }

        let chinglish = Array.isArray(base.chinglish_expressions) ? base.chinglish_expressions.slice() : [];
        chFromLr.forEach(f => {
            if (!f || !f.expression) return;
            if (!chinglish.some(x => String(x.expression || '').toLowerCase() === String(f.expression).toLowerCase())) {
                chinglish.push({
                    expression: f.expression,
                    intended_meaning: f.likely_intended || f.intended_meaning || '',
                    natural_alternative: f.natural_alternative || '',
                    severity: f.severity || 'medium'
                });
            }
        });
        (examSignals.chinglish || []).forEach(label => {
            const expr = String(label).split('（')[0].trim();
            if (!expr) return;
            if (!chinglish.some(x => String(x.expression || '').toLowerCase().includes(expr.toLowerCase()))) {
                chinglish.push({
                    expression: expr,
                    intended_meaning: '可能来自中文直译',
                    natural_alternative: '换成地道搭配',
                    severity: 'medium'
                });
            }
        });

        return {
            repeats_question: repeats,
            sounds_rehearsed: rehearsed,
            chinglish_expressions: chinglish
        };
    }

    ensureNaturalnessInFc(fcDetailed, examSignals, pragmatic) {
        const d = (fcDetailed && typeof fcDetailed === 'object') ? { ...fcDetailed } : {};
        const nat = (d.naturalness && typeof d.naturalness === 'object') ? { ...d.naturalness } : {};
        const rq = pragmatic && pragmatic.repeats_question;
        const sr = pragmatic && pragmatic.sounds_rehearsed;
        nat.repeats_question = !!(nat.repeats_question || (rq && rq.detected) || examSignals.question_echo);
        nat.repetition_evidence = nat.repetition_evidence || (rq && rq.evidence) || examSignals.echo_excerpt || '';
        nat.sounds_rehearsed = !!(nat.sounds_rehearsed || (sr && sr.detected) || examSignals.formulaic);
        nat.rehearsal_evidence = nat.rehearsal_evidence || (sr && sr.evidence)
            || ((examSignals.formulaic_hits || []).join('；')) || '';
        if (!nat.assessment) {
            if (nat.repeats_question || nat.sounds_rehearsed) {
                nat.assessment = '流利度或可到 6，但自然度不足：存在复述题目和/或模板感，冲 6.5 需先改掉。';
            } else {
                nat.assessment = '未检出明显复述题目或强模板感。';
            }
        }
        d.naturalness = nat;
        return d;
    }

    ensureChinglishInLr(lrDetailed, examSignals, pragmatic) {
        const d = (lrDetailed && typeof lrDetailed === 'object') ? { ...lrDetailed } : {};
        let flags = Array.isArray(d.chinglish_flags) ? d.chinglish_flags.slice() : [];
        const fromPrag = (pragmatic && pragmatic.chinglish_expressions) || [];
        fromPrag.forEach(c => {
            if (!c || !c.expression) return;
            if (!flags.some(f => String(f.expression || '').toLowerCase() === String(c.expression).toLowerCase())) {
                flags.push({
                    expression: c.expression,
                    likely_intended: c.intended_meaning || '',
                    natural_alternative: c.natural_alternative || '',
                    severity: c.severity || 'medium'
                });
            }
        });
        d.chinglish_flags = flags;
        return d;
    }

    appendPragmaticToFcReason(reason, pragmatic) {
        let text = String(reason || '').trim();
        const rq = pragmatic && pragmatic.repeats_question;
        const sr = pragmatic && pragmatic.sounds_rehearsed;
        const bits = [];
        if (rq && rq.detected && !/复述题目|重复问题|echo/i.test(text)) {
            bits.push('开场有复述题目，自然度不足，FC 可到 6 但难冲更高');
        }
        if (sr && sr.detected && !/背稿|模板|rehears/i.test(text)) {
            bits.push('听起来偏模板/背稿');
        }
        if (!bits.length) return text;
        return text ? (text + ' ' + bits.join('；') + '。') : (bits.join('；') + '。');
    }

    appendPragmaticToLrReason(reason, pragmatic) {
        let text = String(reason || '').trim();
        const ch = (pragmatic && pragmatic.chinglish_expressions) || [];
        if (!ch.length || /中式英语|chinglish/i.test(text)) return text;
        const bits = ch.slice(0, 3).map(c => `「${c.expression || ''}」`).filter(x => x !== '「」');
        if (!bits.length) return text;
        const note = `中式英语：${bits.join('、')}` + (ch.length >= 2 ? '（多处→LR 倾向 5）' : '');
        return text ? (text + ' ' + note) : note;
    }

    summarizeFcReason(fc) {
        const da = fc && fc.detailed_analysis;
        const parts = [];
        if (fc && fc.justification) parts.push(String(fc.justification));
        if (da && da.summary) parts.push(String(da.summary));
        else {
            if (fc && fc.fluency_evidence) parts.push(String(fc.fluency_evidence));
            if (fc && fc.coherence_evidence) parts.push(String(fc.coherence_evidence));
            if (da && da.fluency && da.fluency.wpm_assessment) parts.push(String(da.fluency.wpm_assessment));
            if (da && da.coherence && da.coherence.topic_development) parts.push(String(da.coherence.topic_development));
        }
        const nat = da && da.naturalness;
        if (nat) {
            if (nat.assessment) parts.push(String(nat.assessment));
            else if (nat.repeats_question || nat.sounds_rehearsed) {
                const bits = [];
                if (nat.repeats_question) bits.push('复述题目');
                if (nat.sounds_rehearsed) bits.push('模板/背稿感');
                parts.push('自然度：' + bits.join('、'));
            }
        }
        return parts.filter(Boolean).join(' ');
    }

    summarizeLrReason(lr) {
        const da = lr && lr.detailed_analysis;
        const parts = [];
        if (lr && lr.justification) parts.push(String(lr.justification));
        if (da && da.summary) parts.push(String(da.summary));
        if (Array.isArray(lr && lr.issues_found) && lr.issues_found.length) {
            parts.push('问题：' + lr.issues_found.slice(0, 3).join('；'));
        }
        if (da && da.collocation && Array.isArray(da.collocation.errors) && da.collocation.errors.length) {
            const bits = da.collocation.errors.slice(0, 2).map(e =>
                `「${e.wrong || ''}」→「${e.correct || ''}」`
            );
            parts.push('搭配：' + bits.join('；'));
        }
        const ch = da && Array.isArray(da.chinglish_flags) ? da.chinglish_flags : [];
        if (ch.length) {
            const bits = ch.slice(0, 3).map(f => {
                const alt = f.natural_alternative ? `→「${f.natural_alternative}」` : '';
                return `「${f.expression || ''}」${alt}`;
            });
            parts.push('中式英语：' + bits.join('；'));
        }
        return parts.filter(Boolean).join(' ');
    }

    summarizeGrammarReason(gra) {
        const da = gra && gra.detailed_analysis;
        const parts = [];
        if (gra && gra.justification) parts.push(String(gra.justification));
        if (da && da.summary) parts.push(String(da.summary));
        const errors = (da && Array.isArray(da.errors) && da.errors)
            || (Array.isArray(gra && gra.errors) && gra.errors)
            || [];
        if (errors.length) {
            parts.push(`共检出 ${errors.length} 处语法问题（见下方「语法错误」清单）`);
            const bits = errors.slice(0, 2).map(e => {
                if (!e || typeof e !== 'object') return String(e);
                return `「${e.original || ''}」→「${e.correction || ''}」`;
            });
            parts.push(bits.join('；'));
        } else {
            parts.push('未检出明显语法错误条目（若回答偏短，仍可能句式单一）。');
        }
        if (da && da.error_statistics && da.error_statistics.most_frequent_error) {
            parts.push('最常见错误：' + da.error_statistics.most_frequent_error);
        }
        if (da && da.sentence_variety && da.sentence_variety.assessment) {
            parts.push(String(da.sentence_variety.assessment));
        }
        return parts.filter(Boolean).join(' ');
    }

    countGrammarErrors(grammarDetailed) {
        if (!grammarDetailed || !Array.isArray(grammarDetailed.errors)) return 0;
        return grammarDetailed.errors.length;
    }

    stripSentencePunct(s) {
        return String(s || '').replace(/[.?!]+$/g, '').trim();
    }

    splitTranscriptSentences(text) {
        const raw = String(text || '').trim();
        if (!raw) return [];
        const parts = raw.match(/[^.?!]+[.?!]+|[^.?!]+$/g) || [raw];
        return parts.map(x => x.trim()).filter(Boolean);
    }

    // ASR 常因停顿把一句拆成 Which? / Was a gift. / From my parents.
    restitchAsrTranscript(transcript) {
        const parts = this.splitTranscriptSentences(transcript);
        if (!parts.length) return { text: '', merges: [], sentences: [] };

        const merges = [];
        const out = [];
        const strip = (s) => this.stripSentencePunct(s);
        const punct = (s) => {
            const m = String(s || '').match(/[.?!]+$/);
            return (m && m[0]) || '.';
        };
        const isRelAlone = (s) => /^(which|that|who|whom|whose)$/i.test(strip(s));
        const isCoordAlone = (s) => /^(and|but|or|so)$/i.test(strip(s));
        const startsPrep = (s) => /^(from|with|to|for|in|at|of|about|by|on)\b/i.test(strip(s));
        const startsPredicate = (s) => /^(been|being|was|were|is|are|am|have|has|had|gave|made|got|went|go|going|done|given)\b/i.test(strip(s));
        const endsOpen = (s) => /\b(i(?:'ve| have) often|used to|gave me|it was a gift|it is a gift|was a gift|is a gift)$/i.test(strip(s));
        const lowerContinue = (b) => {
            if (/^i\b|^i'/i.test(b)) return b;
            return b.charAt(0).toLowerCase() + b.slice(1);
        };

        for (let i = 0; i < parts.length; i++) {
            let cur = parts[i];
            while (i + 1 < parts.length) {
                const next = parts[i + 1];
                const a = strip(cur);
                const b = strip(next);
                let joined = null;

                if (isRelAlone(cur) && startsPredicate(next)) {
                    joined = `${a} ${lowerContinue(b)}`;
                } else if (isCoordAlone(cur) && b.split(/\s+/).length >= 2) {
                    joined = `${a} ${lowerContinue(b)}`;
                } else if (/\bi(?:'ve| have) often$/i.test(a) && /^(been|gone|going|go|went)\b/i.test(b)) {
                    joined = `${a} ${lowerContinue(b)}`;
                } else if (startsPrep(next) && b.split(/\s+/).length <= 6 && a.split(/\s+/).length >= 2) {
                    // It was a gift. From my parents. → 介词短语续接
                    joined = `${a} ${lowerContinue(b)}`;
                } else if (endsOpen(cur) && startsPredicate(next) && b.split(/\s+/).length <= 8) {
                    joined = `${a} ${lowerContinue(b)}`;
                }

                if (!joined) break;
                merges.push({ from: [cur, next], to: joined });
                cur = joined + punct(next);
                i++;
            }
            out.push(cur);
        }

        return { text: out.join(' '), merges, sentences: out };
    }

    looksLikeCompleteClause(sentence) {
        const s = this.stripSentencePunct(sentence);
        if (!s) return false;
        const words = s.split(/\s+/).filter(Boolean);
        if (words.length >= 3 && /^(i|you|he|she|it|we|they|this|that)\b/i.test(s)
            && /\b(was|were|is|are|am|have|has|had|went|go|going|used|gave|made|feel|felt|been|like|liked|love|loved|want|wanted|do|did|does)\b/i.test(s)) {
            return true;
        }
        // 回拼后的关系从句：which was a gift from my parents
        if (words.length >= 4 && /^(which|that|who)\b/i.test(s)
            && /\b(was|were|is|are|have|has|had|gave|made)\b/i.test(s)) {
            return true;
        }
        return false;
    }

    isLikelyTrueFragment(sentence) {
        const s = this.stripSentencePunct(sentence);
        if (!s || this.looksLikeCompleteClause(s)) return false;
        const words = s.split(/\s+/).filter(Boolean);
        if (words.length === 0 || words.length > 8) return false;
        if (/^(yes|yeah|yep|no|nope|sure|absolutely|exactly|okay|ok|of course|definitely)\b/i.test(s)) return false;
        // 仅句首介词/分词/光杆谓语才可能是真残缺；不再用全文匹配 To，避免误伤 went to park
        // Where's... 是完整疑问句，不算残缺
        if (/^(from|with|for|in|at|of|about|by|on|been|being)\b/i.test(s)) return true;
        if (/^(and|but|or|so)$/i.test(s)) return true;
        if (/^(was|were|is|are|am|gave|made)\b/i.test(s) && !/^(it|this|that|he|she|they|i|we|you)\b/i.test(s)) return true;
        if (/^to\b/i.test(s) && words.length <= 4) return true; // 独立短句 To park. 才算
        if (/^i(?:'ve| have) often$/i.test(s)) return true;
        // It gave me / And it gave me：交给专门规则报缺宾语，这里不整句当残缺
        return false;
    }

    filterAsrFalseFragmentErrors(errors, stitch) {
        const list = Array.isArray(errors) ? errors : [];
        const rest = String(stitch && stitch.text || '').toLowerCase().replace(/\s+/g, ' ');
        const mergeBlob = (stitch && stitch.merges || [])
            .map(m => (m.from || []).concat(m.to || '').join(' '))
            .join(' ')
            .toLowerCase();

        return list.filter(e => {
            if (!e || typeof e !== 'object') return true;
            const typ = String(e.type || '').toLowerCase();
            if (typ !== 'sentence_structure' && typ !== 'fragment') return true;
            const orig = this.stripSentencePunct(e.original).toLowerCase();
            if (!orig) return true;

            // Which? / And? 单独成“句”：几乎肯定是 ASR 停顿
            if (/^(which|that|who|whom|whose|and|but|or|so)$/.test(orig)) return false;

            // 已被回拼进完整小句的 From my parents / Was a gift 等才丢弃
            // （And it gave me 虽回拼但仍缺宾语，不能丢）
            if (mergeBlob.includes(orig) && rest.includes(orig)) {
                const parent = (stitch.sentences || []).find(sent =>
                    this.stripSentencePunct(sent).toLowerCase().includes(orig)
                );
                if (parent && this.looksLikeCompleteClause(parent)) return false;
                if (parent && /^(from|with|for|in|at|of|about|by|on|which|that|who)\b/i.test(orig)
                    && orig.split(/\s+/).length <= 5
                    && !this.isLikelyTrueFragment(parent)) {
                    return false;
                }
            }

            // 完整句里的 to park 不是残缺句（冠词问题另报）
            if (/^(to )?park$/.test(orig) || /^to park$/.test(orig)) return false;
            if (/went to park|been to park|go to park|going to park/.test(orig)
                && /残缺|半截|完整主谓|sentence fragment/i.test(String(e.explanation || ''))) {
                return false;
            }

            // 回拼后已是完整小句，不再保留对该碎片的结构错误
            if (stitch && Array.isArray(stitch.sentences)) {
                const covered = stitch.sentences.some(sent => {
                    const s = this.stripSentencePunct(sent).toLowerCase();
                    return s.includes(orig) && this.looksLikeCompleteClause(sent);
                });
                if (covered && orig.split(/\s+/).length <= 5) return false;
            }
            return true;
        });
    }

    detectLocalGrammarIssues(transcript) {
        const stitch = this.restitchAsrTranscript(transcript);
        const t = stitch.text || String(transcript || '').trim();
        if (!t) return [];
        const errors = [];
        const push = (original, correction, type, explanation, severity = 'high') => {
            if (!original) return;
            const key = original.toLowerCase();
            if (errors.some(e => String(e.original || '').toLowerCase() === key)) return;
            errors.push({ original, correction, type, explanation, severity, source: 'local' });
        };

        // 残缺句：只在回拼后仍不完整的独立短句上判定
        (stitch.sentences.length ? stitch.sentences : this.splitTranscriptSentences(t)).forEach(raw => {
            if (!this.isLikelyTrueFragment(raw)) return;
            const original = this.stripSentencePunct(raw);
            push(
                original,
                '补成完整句（含主语和谓语）',
                'sentence_structure',
                '回拼停顿断句后仍缺少完整主谓结构。',
                'high'
            );
        });

        // I've often. 单独成句（回拼后仍孤立才报）
        (stitch.sentences || []).forEach(raw => {
            const s = this.stripSentencePunct(raw);
            if (/^i(?:'ve| have) often$/i.test(s)) {
                push(
                    s,
                    "I've often been to the park",
                    'sentence_structure',
                    '频次副词后缺少主要动词和宾语，句子不完整。',
                    'high'
                );
            }
        });

        // been/go/went to park 缺冠词（完整句也要报，但类型是 article）
        if (/\b(?:been|go|went|going)\s+to park\b/i.test(t) || /\bto park\b/i.test(t)) {
            const m = t.match(/\b(?:been|go|went|going)\s+to park\b/i) || t.match(/\bto park\b/i);
            push(
                (m && m[0]) || 'to park',
                String(m && m[0] || 'to park').replace(/\bto park\b/i, 'to the park'),
                'article',
                'park 前通常需要定冠词 the；这不是残缺句。',
                'medium'
            );
        }

        // It gave me. 宾语残缺（回拼后仍无后续宾语）
        (stitch.sentences || []).forEach(raw => {
            const s = this.stripSentencePunct(raw);
            if (/\bit gave me$/i.test(s)) {
                push(
                    'It gave me',
                    'It made me feel very happy / It gave me a lot of happiness',
                    'sentence_structure',
                    'gave me 后缺少宾语，句子不完整。',
                    'high'
                );
            }
        });

        // some happy / gave me some happy
        if (/\b(some|a|an)\s+happy\b/i.test(t)) {
            const m = t.match(/\b(?:gave me )?(?:some|a|an)\s+happy\b/i);
            push(
                (m && m[0]) || 'some happy',
                'made me happy / some happiness',
                'word_form',
                'happy 是形容词，不能直接当名词宾语。',
                'high'
            );
        }

        return this.filterAsrFalseFragmentErrors(errors, stitch);
    }

    mergeGrammarDetailedAnalysis(existingDetailed, graNode, transcript) {
        const base = (existingDetailed && typeof existingDetailed === 'object')
            ? { ...existingDetailed }
            : {};
        const stitch = this.restitchAsrTranscript(transcript);
        let errors = [];
        if (Array.isArray(base.errors)) errors = errors.concat(base.errors);
        if (graNode && Array.isArray(graNode.errors)) errors = errors.concat(graNode.errors);
        // 去掉 AI 把 ASR 停顿断句误标成的残缺句
        errors = this.filterAsrFalseFragmentErrors(errors, stitch);
        const local = this.detectLocalGrammarIssues(transcript);
        local.forEach(e => {
            const key = String(e.original || '').toLowerCase();
            if (!errors.some(x => String(x.original || '').toLowerCase().includes(key) || key.includes(String(x.original || '').toLowerCase()))) {
                errors.push(e);
            }
        });
        errors = this.filterAsrFalseFragmentErrors(errors, stitch);
        // 去重
        const seen = new Set();
        errors = errors.filter(e => {
            const k = String(e && e.original || '').toLowerCase().replace(/\s+/g, ' ').trim();
            if (!k || seen.has(k)) return false;
            seen.add(k);
            return true;
        });

        const byType = {};
        errors.forEach(e => {
            const typ = String(e.type || 'other').toLowerCase();
            byType[typ] = (byType[typ] || 0) + 1;
        });
        let most = '';
        let mostN = 0;
        Object.keys(byType).forEach(k => {
            if (byType[k] > mostN) { mostN = byType[k]; most = k; }
        });
        const wordCount = Math.max(1, this.countTranscriptWords(transcript));
        const density = Math.round((errors.length / wordCount) * 1000) / 10;

        base.errors = errors;
        base.error_statistics = {
            ...(base.error_statistics || {}),
            total_errors: errors.length,
            by_type: { ...(base.error_statistics && base.error_statistics.by_type || {}), ...byType },
            most_frequent_error: most || (base.error_statistics && base.error_statistics.most_frequent_error) || '',
            error_density_per_100_words: density
        };
        if (!base.summary) {
            base.summary = errors.length
                ? `检出 ${errors.length} 处语法问题，短板主要在句型完整度/准确性；先把残缺句补全再谈复杂句。`
                : '未检出明显残缺句或基础语法硬伤；可继续增加复杂句式。';
        }
        return base;
    }

    summarizePronReason(pron) {
        const da = pron && pron.detailed_analysis;
        const parts = [];
        if (pron && pron.justification) parts.push(String(pron.justification));
        if (da && da.assessment) parts.push(String(da.assessment));
        const signals = (da && da.signals_found)
            || (Array.isArray(pron && pron.signals) && pron.signals)
            || [];
        if (Array.isArray(signals) && signals.length) {
            parts.push('信号：' + signals.slice(0, 3).join('；'));
        }
        return parts.filter(Boolean).join(' ');
    }

    grammarTypeLabel(type) {
        const map = {
            tense: '时态',
            subject_verb_agreement: '主谓一致',
            article: '冠词',
            plural: '单复数',
            preposition: '介词',
            word_form: '词性',
            sentence_structure: '句型结构',
            non_finite: '非谓语',
            subjunctive: '虚拟语气',
            comparative: '比较级',
            other: '其他'
        };
        return map[String(type || '').toLowerCase()] || (type || '其他');
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

    formatHeatCount(n) {
        const num = Number(n) || 0;
        if (num >= 10000) return `${(num / 10000).toFixed(num >= 100000 ? 0 : 1).replace(/\.0$/, '')}万`;
        if (num >= 1000) return `${(num / 1000).toFixed(1).replace(/\.0$/, '')}k`;
        return String(num);
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

        const problemsHtml = (arr) => {
            if (!arr || !arr.length) return '';
            return arr.slice(0, 5).map((item, idx) => {
                if (!item || typeof item !== 'object') {
                    return `<li>${this.escapeHtml(String(item))}</li>`;
                }
                const rank = item.rank || (idx + 1);
                const cat = item.category ? `（${this.escapeHtml(item.category)}）` : '';
                return `<li style="margin-bottom:10px;">
                    <strong>#${rank}${cat} ${this.escapeHtml(item.issue || '')}</strong>
                    ${item.why_it_matters ? `<div style="margin-top:4px;">为什么：${this.escapeHtml(item.why_it_matters)}</div>` : ''}
                    ${item.how_to_fix ? `<div>怎么改：${this.escapeHtml(item.how_to_fix)}</div>` : ''}
                    ${item.example ? `<div style="margin-top:4px;padding:6px 8px;background:#f6efd2;border-radius:4px;">示例：${this.escapeHtml(item.example)}</div>` : ''}
                </li>`;
            }).join('');
        };
        
        let html = `
            <div class="overall-score">
                <div class="overall-label">总体 Band 分数</div>
                <div class="overall-value">${p.overall}</div>
            </div>
            <div class="score-card">
                <div class="score-item"><div class="score-label">FC</div><div class="score-value ${getBandClass(p.fluency)}">${p.fluency}</div></div>
                <div class="score-item"><div class="score-label">LR</div><div class="score-value ${getBandClass(p.vocabulary)}">${p.vocabulary}</div></div>
                <div class="score-item"><div class="score-label">GRA</div><div class="score-value ${getBandClass(p.grammar)}">${p.grammar}</div></div>
                <div class="score-item"><div class="score-label">Pron</div><div class="score-value ${getBandClass(p.pronunciation)}">${p.pronunciation}</div></div>
            </div>
            <div class="band-note" style="margin-top:12px;padding:12px;background:#e7efe9;border-radius:4px;font-size:14px;color:#243029;">
                <strong>评分说明：</strong>FC/LR/GRA/Pron 为 1–9 整数；总分可 x.5。已按多份考官模考校准：5.5 常见 GRA5（假关系从句、SVO+and 堆砌）；6.0 常见四项 6，Pron 或 LR 可单项到 7。语法错误单独列表。
            </div>
            <div class="feedback-section" style="margin-top:14px;">
                <h4>📌 为什么是这个分数</h4>
                <div style="overflow-x:auto;">
                    <table style="width:100%;border-collapse:collapse;font-size:14px;">
                        <tr style="background:#f3eee4;text-align:left;">
                            <th style="padding:8px;border-bottom:1px solid #e0d6c6;width:110px;">维度</th>
                            <th style="padding:8px;border-bottom:1px solid #e0d6c6;width:50px;">分数</th>
                            <th style="padding:8px;border-bottom:1px solid #e0d6c6;">依据</th>
                        </tr>
                        ${row('FC 流利连贯', p.fluency, p.reasons.fluency)}
                        ${row('LR 词汇', p.vocabulary, p.reasons.vocabulary)}
                        ${row('GRA 语法', p.grammar, p.reasons.grammar)}
                        ${row('Pron 发音', p.pronunciation, p.reasons.pronunciation)}
                        <tr>
                            <td style="padding:8px;">总体 Band</td>
                            <td style="padding:8px;"><strong>${p.overall}</strong></td>
                            <td style="padding:8px;">(${p.fluency}+${p.vocabulary}+${p.grammar}+${p.pronunciation})/4 → ${p.overall}</td>
                        </tr>
                    </table>
                </div>
            </div>
        `;
        
        // 语用层（复述题目 / 背稿感 / 中式英语）先于语法与主要问题
        html += this.renderPragmaticIssuesHTML(p.pragmaticIssues);
        // 语法错误单独置顶展示
        html += this.renderGrammarErrorsHTML(p.detailed && p.detailed.grammar);
        html += this.renderDetailedAnalysisHTML(p.detailed, { skipGrammarErrors: true });

        if (p.problems && p.problems.length) {
            html += `<div class="feedback-section"><h4>⚠️ 主要问题</h4><ul style="padding-left:18px;margin:0;">${problemsHtml(p.problems)}</ul></div>`;
        } else {
            if (p.strengths && p.strengths.length) {
                html += `<div class="feedback-section"><h4>✅ 优点</h4><div class="feedback-text">${listHtml(p.strengths)}</div></div>`;
            }
            if (p.weaknesses && p.weaknesses.length) {
                html += `<div class="feedback-section"><h4>⚠️ 需要改进</h4><div class="feedback-text">${listHtml(p.weaknesses)}</div></div>`;
            }
            if (p.suggestions && p.suggestions.length) {
                html += `<div class="feedback-section"><h4>💡 改进建议</h4><div class="feedback-text">${listHtml(p.suggestions)}</div></div>`;
            }
        }

        const improved = p.improvedMeta;
        const rewritten = (improved && improved.rewritten_version) || p.sampleAnswer || '';
        const summary = improved && improved.original_summary
            ? `<div style="margin-bottom:8px;font-size:13px;color:#6b655c;">原意：${this.escapeHtml(improved.original_summary)}</div>`
            : '';
        const improvList = improved && Array.isArray(improved.improvements_made) && improved.improvements_made.length
            ? `<div style="margin-top:8px;font-size:13px;">改进点：${improved.improvements_made.map(x => this.escapeHtml(x)).join('；')}</div>`
            : '';
        const tipChunks = !(improved && improved.rewritten_version) ? `
                <div style="margin-bottom:8px;font-size:13px;color:#6b655c;">
                    使用词块：${(p.tipMeta && p.tipMeta.usedChunks || []).map(c => `<code style="background:#f6efd2;padding:1px 6px;border-radius:2px;margin-right:4px;">${this.escapeHtml(c)}</code>`).join('') || '—'}
                </div>
                <div style="margin-bottom:8px;font-size:13px;color:#1e3f36;">
                    复合句：${this.escapeHtml((p.tipMeta && p.tipMeta.complexSentence) || '')}
                </div>` : '';

        html += `
            <div class="sample-answer">
                <h4>🎯 ${improved && improved.rewritten_version ? '7分改写版本' : '改进示例（本题词块 + 复合句）'}</h4>
                ${summary}
                ${tipChunks}
                <div style="padding:10px;background:#e6f2ea;border-radius:4px;">
                    <p style="margin:0;">${this.escapeHtml(rewritten)}</p>
                </div>
                ${improvList}
            </div>`;
        return html;
    }

    renderPragmaticIssuesHTML(pragmatic) {
        if (!pragmatic || typeof pragmatic !== 'object') return '';
        const rq = pragmatic.repeats_question || {};
        const sr = pragmatic.sounds_rehearsed || {};
        const ch = Array.isArray(pragmatic.chinglish_expressions) ? pragmatic.chinglish_expressions : [];
        const hasRq = !!rq.detected;
        const hasSr = !!sr.detected;
        const hasCh = ch.length > 0;
        if (!hasRq && !hasSr && !hasCh) return '';

        let html = `<div class="feedback-section" style="border:1px solid #c5d4c8;background:#f3f7f4;border-radius:6px;padding:12px;">
            <h4 style="margin:0 0 8px;">🧭 语用问题（冲 6.5 关键卡点）</h4>
            <p style="margin:0 0 10px;font-size:13px;color:#3a433d;">流利度到 6 仍可能因复述题目、模板感或中式英语卡住更高分。</p>`;

        const card = (title, node) => {
            if (!node || !node.detected) return '';
            return `<div style="margin-bottom:10px;padding:8px 10px;background:#fff;border-radius:4px;border-left:3px solid #5a7d6a;">
                <strong style="font-size:14px;">${title}</strong>
                ${node.evidence ? `<div style="margin-top:4px;font-size:13px;">证据：${this.escapeHtml(node.evidence)}</div>` : ''}
                ${node.impact ? `<div style="font-size:13px;">影响：${this.escapeHtml(node.impact)}</div>` : ''}
                ${node.fix ? `<div style="font-size:13px;">怎么改：${this.escapeHtml(node.fix)}</div>` : ''}
            </div>`;
        };
        html += card('复述题目', rq);
        html += card('听起来像背稿/模板', sr);

        if (hasCh) {
            html += `<div style="margin-top:4px;"><strong style="font-size:14px;">中式英语表达</strong>
                <ul style="margin:6px 0 0;padding-left:18px;font-size:13px;">`;
            ch.slice(0, 6).forEach(c => {
                if (!c || typeof c !== 'object') return;
                const meaning = c.intended_meaning ? `（想说：${this.escapeHtml(c.intended_meaning)}）` : '';
                const alt = c.natural_alternative
                    ? ` → 「${this.escapeHtml(c.natural_alternative)}」`
                    : '';
                html += `<li>「${this.escapeHtml(c.expression || '')}」${meaning}${alt}</li>`;
            });
            html += `</ul></div>`;
        }
        html += `</div>`;
        return html;
    }

    renderGrammarErrorsHTML(grammarDetailed) {
        const g = grammarDetailed;
        if (!g || typeof g !== 'object') return '';
        const errors = Array.isArray(g.errors) ? g.errors : [];
        const stats = g.error_statistics || {};
        let html = `<div class="feedback-section" style="border:1px solid #e8c4a8;background:#fff8f2;border-radius:6px;padding:12px;">
            <h4 style="margin:0 0 8px;">📝 语法错误</h4>`;
        if (g.summary) {
            html += `<p style="margin:0 0 10px;font-size:14px;">${this.escapeHtml(g.summary)}</p>`;
        }
        html += `<div style="font-size:13px;margin-bottom:10px;color:#3a433d;">
            共 ${this.escapeHtml(String(stats.total_errors ?? errors.length))} 处
            ${stats.most_frequent_error ? `；最常见：${this.escapeHtml(this.grammarTypeLabel(stats.most_frequent_error))}` : ''}
            ${stats.error_density_per_100_words != null ? `；密度：${this.escapeHtml(String(stats.error_density_per_100_words))}/100词` : ''}
        </div>`;
        if (!errors.length) {
            html += `<p style="margin:0;font-size:13px;color:#5a635c;">未列出具体错误条目。</p></div>`;
            return html;
        }
        html += `<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:13px;">
            <tr style="background:#f8ebe0;text-align:left;">
                <th style="padding:6px;border-bottom:1px solid #e0d6c6;width:88px;">类型</th>
                <th style="padding:6px;border-bottom:1px solid #e0d6c6;">原文 → 正确</th>
                <th style="padding:6px;border-bottom:1px solid #e0d6c6;">解释</th>
            </tr>`;
        errors.slice(0, 15).forEach(e => {
            if (!e || typeof e !== 'object') return;
            const sev = e.severity ? ` <span style="color:#8a6d3b;">(${this.escapeHtml(e.severity)})</span>` : '';
            html += `<tr>
                <td style="padding:6px;border-bottom:1px solid #f0e4d8;white-space:nowrap;">${this.escapeHtml(this.grammarTypeLabel(e.type))}${sev}</td>
                <td style="padding:6px;border-bottom:1px solid #f0e4d8;">「${this.escapeHtml(e.original || '')}」→「${this.escapeHtml(e.correction || '')}」</td>
                <td style="padding:6px;border-bottom:1px solid #f0e4d8;">${this.escapeHtml(e.explanation || '')}</td>
            </tr>`;
        });
        html += `</table></div></div>`;
        return html;
    }

    renderDetailedAnalysisHTML(detailed, options = {}) {
        if (!detailed || typeof detailed !== 'object') return '';
        let html = '';
        const g = detailed.grammar;
        if (g && typeof g === 'object') {
            const variety = g.sentence_variety || {};
            if (!options.skipGrammarErrors) {
                html += this.renderGrammarErrorsHTML(g);
            }
            if (variety.assessment || variety.complex_sentence_ratio != null) {
                html += `<div class="feedback-section"><h4>🔎 语法·句式多样性</h4>
                <div style="font-size:13px;padding:8px 10px;background:#f7f3ea;border-radius:4px;">
                    ${variety.simple_sentences != null ? `简单句 ${this.escapeHtml(String(variety.simple_sentences))}，` : ''}
                    ${variety.compound_sentences != null ? `并列句 ${this.escapeHtml(String(variety.compound_sentences))}，` : ''}
                    ${variety.complex_sentences != null ? `复合句 ${this.escapeHtml(String(variety.complex_sentences))}；` : ''}
                    ${variety.complex_sentence_ratio != null ? `复合句比例 ${this.escapeHtml(String(variety.complex_sentence_ratio))}；` : ''}
                    ${variety.avg_sentence_length_words != null ? `均长 ${this.escapeHtml(String(variety.avg_sentence_length_words))} 词。` : ''}
                    ${variety.assessment ? `<div style="margin-top:4px;">${this.escapeHtml(variety.assessment)}</div>` : ''}
                    ${Array.isArray(variety.structures_missing) && variety.structures_missing.length
                        ? `<div style="margin-top:4px;">可补充结构：${variety.structures_missing.map(x => this.escapeHtml(String(x))).join('、')}</div>`
                        : ''}
                </div></div>`;
            }
        }

        const fc = detailed.fluency;
        if (fc && typeof fc === 'object' && (fc.summary || fc.fluency || fc.coherence || fc.naturalness)) {
            html += `<div class="feedback-section"><h4>🔎 流利度与连贯详细解析</h4>`;
            if (fc.summary) html += `<p style="margin:0 0 8px;font-size:14px;">${this.escapeHtml(fc.summary)}</p>`;
            const f = fc.fluency || {};
            const c = fc.coherence || {};
            const lines = [
                f.wpm_assessment, f.pause_assessment, f.filler_assessment, f.repetition_assessment,
                c.connectives_assessment, c.topic_development
            ].filter(Boolean);
            if (lines.length) {
                html += `<ul style="margin:0;padding-left:18px;font-size:13px;">${lines.map(x => `<li>${this.escapeHtml(String(x))}</li>`).join('')}</ul>`;
            }
            const nat = fc.naturalness;
            if (nat && typeof nat === 'object' && (nat.assessment || nat.repeats_question || nat.sounds_rehearsed)) {
                html += `<div style="margin-top:10px;padding:8px 10px;background:#eef4f0;border-radius:4px;font-size:13px;">
                    <strong>自然度</strong>
                    ${nat.assessment ? `<div style="margin-top:4px;">${this.escapeHtml(String(nat.assessment))}</div>` : ''}
                    ${nat.repeats_question ? `<div>复述题目：${this.escapeHtml(nat.repetition_evidence || '是')}</div>` : ''}
                    ${nat.sounds_rehearsed ? `<div>背稿/模板感：${this.escapeHtml(nat.rehearsal_evidence || '是')}</div>` : ''}
                </div>`;
            }
            html += `</div>`;
        }

        const lr = detailed.vocabulary;
        if (lr && typeof lr === 'object' && (lr.summary || lr.collocation || lr.vocabulary_diversity || (lr.chinglish_flags && lr.chinglish_flags.length))) {
            html += `<div class="feedback-section"><h4>🔎 词汇详细解析</h4>`;
            if (lr.summary) html += `<p style="margin:0 0 8px;font-size:14px;">${this.escapeHtml(lr.summary)}</p>`;
            const collErr = lr.collocation && Array.isArray(lr.collocation.errors) ? lr.collocation.errors : [];
            if (collErr.length) {
                html += `<ul style="margin:0;padding-left:18px;font-size:13px;">${collErr.slice(0, 6).map(e =>
                    `<li>「${this.escapeHtml(e.wrong || '')}」→「${this.escapeHtml(e.correct || '')}」${e.explanation ? '：' + this.escapeHtml(e.explanation) : ''}</li>`
                ).join('')}</ul>`;
            } else if (lr.vocabulary_diversity && lr.vocabulary_diversity.assessment) {
                html += `<p style="margin:0;font-size:13px;">${this.escapeHtml(lr.vocabulary_diversity.assessment)}</p>`;
            }
            const chFlags = Array.isArray(lr.chinglish_flags) ? lr.chinglish_flags : [];
            if (chFlags.length) {
                html += `<div style="margin-top:10px;font-size:13px;"><strong>中式英语标记</strong>
                    <ul style="margin:6px 0 0;padding-left:18px;">${chFlags.slice(0, 6).map(f =>
                        `<li>「${this.escapeHtml(f.expression || '')}」${f.natural_alternative ? '→「' + this.escapeHtml(f.natural_alternative) + '」' : ''}${f.likely_intended ? '（' + this.escapeHtml(f.likely_intended) + '）' : ''}</li>`
                    ).join('')}</ul></div>`;
            }
            html += `</div>`;
        }

        const pr = detailed.pronunciation;
        if (pr && typeof pr === 'object' && (pr.assessment || (pr.signals_found && pr.signals_found.length))) {
            html += `<div class="feedback-section"><h4>🔎 发音详细解析</h4>`;
            if (pr.assessment) html += `<p style="margin:0 0 8px;font-size:14px;">${this.escapeHtml(pr.assessment)}</p>`;
            const sig = [].concat(pr.signals_found || [], pr.word_duration_issues || [], pr.asr_anomalies || []).filter(Boolean);
            if (sig.length) {
                html += `<ul style="margin:0;padding-left:18px;font-size:13px;">${sig.slice(0, 6).map(x => `<li>${this.escapeHtml(String(x))}</li>`).join('')}</ul>`;
            }
            html += `</div>`;
        }

        return html;
    }
    
    // 各维度禁止串台（仅强串台才丢弃；语法评语允许提「错误用词形式」）
    dimensionForbidden() {
        return {
            fluency: [/词汇资源/, /lexical resource/i, /pronunciation/i, /发音清晰/, /发音问题/],
            lexical: [/流利度与连贯/, /fluency & coherence/i, /pronunciation/i, /发音清晰/, /长停顿/],
            grammar: [/流利度与连贯/, /fluency & coherence/i, /pronunciation/i, /发音清晰/, /语速 WPM/i],
            pronunciation: [/时态不一致/, /主谓一致/, /lexical resource/i, /词汇资源/, /复杂句型/]
        };
    }

    resolveDimensionReason(dim, aiReason, transcript, score) {
        const cleaned = this.cleanReasonText(aiReason);
        if (cleaned && cleaned.length >= 12) {
            const rules = this.dimensionForbidden()[dim] || [];
            const heavilyCross = rules.filter(re => re.test(cleaned)).length >= 2;
            if (!heavilyCross) return cleaned;
        }
        // 有实质内容但略串台：仍优先 AI，去掉明显他维标签后返回
        if (cleaned && cleaned.length >= 20) {
            return cleaned
                .replace(/\b(Fluency|Vocabulary|Lexical|Grammar|Pronunciation)\b[:：]?\s*/gi, '')
                .trim();
        }
        return this.localDimensionReason(dim, transcript || '', score);
    }
    
    sanitizeDimensionReason(dim, reason, transcript, score) {
        return this.resolveDimensionReason(dim, reason, transcript, score);
    }

    // 跳过 Yes/Absolutely 这类开场，找更适合点评的句子
    pickContentSentence(transcript) {
        const sentences = String(transcript || '')
            .split(/[.!?]+/)
            .map(x => x.trim())
            .filter(x => x.length > 2);
        const opener = /^(yes|yeah|sure|absolutely|of course|definitely|exactly|ok|okay)\b/i;
        const content = sentences.find(s => {
            const words = s.split(/\s+/).filter(Boolean);
            if (words.length < 3) return false;
            if (opener.test(s) && words.length <= 4) return false;
            return true;
        });
        return content || sentences.find(s => s.split(/\s+/).length >= 3) || sentences[0] || '';
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
        const contentSent = this.pickContentSentence(t) || firstSent || lastSent;
        
        if (dim === 'fluency') {
            if (sentences.length >= 3 && sentences.every(x => x.split(/\s+/).length <= 8)) {
                return '句子偏短、推进一般。你说了「' + (contentSent || firstSent) + '」和「' + lastSent + '」→ 更好：合成一句，用 and / so 连接。';
            }
            const hardAnd = clip(/\bAnd\b[^.!?]{5,60}/);
            if (hardAnd) {
                return '衔接偏硬。你说「' + hardAnd + '」→ 更好：并入前句，如 “..., and ...”。';
            }
            if (s <= 5) {
                const snippet = t.length > 90 ? t.slice(0, 90) + '...' : t;
                return '整体能听懂，但连贯一般。你的原话：「' + snippet + '」。可把短句连起来。';
            }
            return '根据你的识别文本，表达基本连贯。可继续用 and / because / which 把想法连起来。';
        }
        
        if (dim === 'lexical') {
            const likedMood = clip(/\breally liked my mood\b|\bliked my mood\b|\blike my mood\b/i);
            if (likedMood) {
                return '搭配不够自然。你说了「' + likedMood + '」→ 更好：「it really lifted my mood」。你已用 mood，问题在搭配。';
            }
            const someHappy = clip(/\bsome happy\b|\bgave me some happy\b|\bmake me happy is\b/i);
            if (someHappy) {
                return '词性/搭配不对。你说了「' + someHappy + '」→ 更好：「made me happy」或「gave me some happiness」。';
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
            if (contentSent) {
                return '用词基本能表意。针对「' + contentSent + '」，可把其中一处搭配说得更地道（不要只重复 Yes/Absolutely）。';
            }
            return '用词基本能表意；可把一处搭配说得更地道。';
        }
        
        if (dim === 'grammar') {
            const adjAsNoun = clip(/\b(some|a|an|much|more)\s+(happy|sad|exciting|interesting|relaxing)\b/i);
            if (adjAsNoun) {
                return '词性当语法用错了。你说「' + adjAsNoun + '」→ 形容词不能直接当名词：改成 “made me happy” 或 “some happiness”。';
            }
            const gaveHappy = clip(/\bgave me (some )?happy\b|\bmade? me some happy\b/i);
            if (gaveHappy) {
                return '结构不成立。你说「' + gaveHappy + '」→ 更好：「It made me happy」或「It gave me a lot of happiness」。';
            }
            const frag = clip(/\bIn my [^.?!]{0,40}\./i) || clip(/\bWas [^.?!]{0,40}\./);
            if (frag) {
                return '结构不完整。你说了「' + frag + '」→ 更好：补全主语和动词，写成完整句。';
            }
            if (has(/\bused to\b/) && has(/\bi (walk|feel|go|run|like)\b/)) {
                const bit = clip(/\bI (walk|feel|go|run|like)\b[^.?]*/i) || contentSent;
                return '时态可能不一致。你前面用了 used to，后面有「' + bit + '」→ 讲过去时更稳：walked / felt / liked。';
            }
            const missingPast = clip(/\bI (go|have|feel|walk|play) (?:to |a |the )?[^.!?]{0,40}/i);
            if (missingPast && has(/\b(yesterday|last|ago|used to|when i was)\b/)) {
                return '过去时间线里动词可能没变位。你说「' + missingPast + '」→ 检查是否该用过去式（went / had / felt / walked）。';
            }
            if (contentSent && contentSent.split(/\s+/).length >= 4) {
                if (s >= 6) {
                    return '语法整体可控。以「' + contentSent + '」为例，可再加一个从句（because / which / when）提升句式范围。';
                }
                return '语法大体可读，但句式偏简单。以「' + contentSent + '」为例：保留原意，补全时态/主谓，或改成带 because/which 的复杂句。';
            }
            return '语法整体可控；请结合完整叙述句检查时态、主谓和词性，不要只盯着开场的 Yes/Absolutely。';
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
        if (n < 10) return 4;
        if (n < 16) return 5;
        if (n < 25) return 5;
        return 6;
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
        const clamp = (v) => Math.min(maxDim, this.pickBandScore(v, 4));
        return {
            fluency: clamp(scores.fluency),
            vocabulary: clamp(scores.vocabulary),
            grammar: clamp(scores.grammar),
            pronunciation: clamp(scores.pronunciation)
        };
    }

    // 发音兜底：无明显硬伤默认 6；清晰自然时 AI 可给 7（模考锚定 Pron7）
    estimatePronunciationScore(transcript) {
        const t = (transcript || '').trim();
        if (!t) return 3;
        const words = t.split(/\s+/).filter(w => w.length > 0);
        const wordCount = words.length;
        const sentenceCount = Math.max(1, t.split(/[.!?]+/).filter(s => s.trim().length > 0).length);
        const avgSentenceLength = wordCount / sentenceCount;
        if (wordCount < 8) return 4;
        if (avgSentenceLength < 3 || wordCount < 10) return 5;
        return 6;
    }

    mergeExaminerProblems(problems, examSignals, transcript) {
        const list = Array.isArray(problems) ? problems.slice() : [];
        const hasTopic = (re) => list.some(p => re.test(String((p && (p.issue || p.how_to_fix)) || '')));
        const push = (item) => {
            if (list.length >= 5) return;
            list.push(item);
        };
        if (examSignals.question_echo && !hasTopic(/复述题目|重复.*题目|repeat the question/i)) {
            push({
                rank: 1,
                category: 'fluency',
                issue: '开场复述题目，听起来极不自然',
                why_it_matters: '真实考官认为这是 Band 4 学生没话说时的习惯；即使流利度勉强到 6，也会挡住 6.5+',
                how_to_fix: '直接回答，不要把题目整句说回去。用 Yes/Well/Actually 一带而过即可。',
                example: examSignals.echo_excerpt
                    ? `不要说「${examSignals.echo_excerpt}」；直接说自己的观点/经历。`
                    : 'Q: Have you ever had a pet? → “Yes, I used to have a puppy when I was little.”'
            });
        }
        if (examSignals.chinglish.length >= 1 && !hasTopic(/中式|直译|Chinglish|搭配怪/i)) {
            push({
                rank: list.length + 1,
                category: 'vocabulary',
                issue: '出现疑似中式英语或怪搭配：' + examSignals.chinglish.slice(0, 3).join('；'),
                why_it_matters: '考官反馈：2–3 处难懂表达词汇会掉到 5；搭配自然、少 Chinglish 才最接近 LR7（Zhang Xin Yu）。',
                how_to_fix: '先想地道英文搭配，不要从中文逐字翻译；说不清就换简单但准确的词。',
                example: '不要 “honest food”；改说 “homemade / fresh / authentic food”。'
            });
        }
        const gs = examSignals.grammar_structure || {};
        if (gs.fake_relative_count >= 1 && !hasTopic(/假关系|fake relative|told me that|remember clearly/i)) {
            push({
                rank: list.length + 1,
                category: 'grammar',
                issue: '使用假关系从句套话：' + gs.fake_relative.slice(0, 2).join('；'),
                why_it_matters: '考官会识破 He told me that / I remember clearly that 等“装复杂”的写法，仍按 Band5 语法处理（Ji Peng Hao 模考 GRA5）。',
                how_to_fix: '改用真关系从句（which/who/that 修饰名词）或第二条件句、情态动词展示语法范围。',
                example: '不说 “I remember clearly that it was nice”；改说 “The cake, which was made of ice cream, was amazing.”'
            });
        }
        if (gs.svo_and_dominant && !hasTopic(/SVO|and 连接|简单句堆砌/i)) {
            push({
                rank: list.length + 1,
                category: 'grammar',
                issue: '大量 SVO 句用 and 连接，缺少 that/which/who 等从句',
                why_it_matters: '错误少不代表语法好：几乎全是 and 连接简单句会被判 GRA5（Zhang Xin Yu 模考）。',
                how_to_fix: '每 2–3 句至少加入一个 that/which/who 从句，或第二条件句（If I were…, I would…）。',
                example: '“I like it and it is fun and I go there and…” → “I like it because it’s relaxing, which is why I go there often.”'
            });
        }
        if (gs.simple_split && gs.simple_split_example && !hasTopic(/定语从句|两句简单句/i)) {
            push({
                rank: list.length + 1,
                category: 'grammar',
                issue: '本可合并为定语从句，却拆成两句简单句',
                why_it_matters: 'Part2 有机会展示复杂结构时只用简单句，会被视为典型 Band5 语法（Ji Peng Hao）。',
                how_to_fix: '把后句改成 which/that 定语从句接在前句名词后。',
                example: gs.simple_split_example + ' → 合并为 “…a cake which was made of ice cream.”'
            });
        }
        if ((examSignals.formulaic && (examSignals.formulaic_hits || []).length >= 3) || examSignals.question_echo) {
            if (!hasTopic(/背稿|模板|不自然|over-prepared|套话|复述题目/i)) {
                push({
                    rank: list.length + 1,
                    category: 'pronunciation',
                    issue: examSignals.question_echo
                        ? '开场复述题目，听起来不自然'
                        : '回答听起来偏模板/准备过，缺少临场思考感',
                    why_it_matters: '考官：发音可以是强项到 7；但复述题目或明显背稿会把自然度压回 6，并挡住冲高。',
                    how_to_fix: '不准备稿子也能答：仔细听/读题，用真实细节即兴说；用轻微语调起伏把较长信息串起来。',
                    example: '少用整段套句；答完让人追问细节，练自然反应。'
                });
            }
        }
        // 重新编号
        return list.slice(0, 5).map((p, i) => ({ ...p, rank: i + 1 }));
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
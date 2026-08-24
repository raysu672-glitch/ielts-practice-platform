// P2：背素材 + 套题练习（第一期无录音评分）
class P2Practice {
    constructor() {
        this.data = typeof P2_DATA !== 'undefined' ? P2_DATA : { materials: [], questions: [] };
        this.mode = 'memorize'; // memorize | apply
        this.p1Mode = 'questions'; // questions | complex
        this._complexFrameLoaded = false;
        this.materialId = null;
        this.variantId = 'a';
        this.questionIndex = 0;
        this.applyMaterialChoice = {}; // questionId -> materialId（小熊/篮球等）
        this.hideEn = {}; // `${materialId}:${stepIndex}` -> true
        this.hideOpening = false;
        this.expandedMaterial = false;
        this.returnQuestionIndex = null;
        this._ttsToken = 0;
        this._ttsAudio = null;
        this._ttsUtter = null;

        this.progress = this.loadProgress();
        this.bindShell();
        this.bindMemorize();
        this.bindApply();
        this.renderMaterialList();
        this.renderQuestionList();
        this.updateProgressLabel();
    }

    mainMaterials() {
        return (this.data.materials || []).filter(m => !m.optional);
    }

    getMaterial(id) {
        return (this.data.materials || []).find(m => m.id === id) || null;
    }

    loadProgress() {
        try {
            const raw = localStorage.getItem('p2_practice_progress');
            if (!raw) return { doneSteps: {}, openedMaterial: false, guideDismissed: false };
            return Object.assign({ doneSteps: {}, openedMaterial: false, guideDismissed: false }, JSON.parse(raw));
        } catch (_) {
            return { doneSteps: {}, openedMaterial: false, guideDismissed: false };
        }
    }

    saveProgress() {
        localStorage.setItem('p2_practice_progress', JSON.stringify(this.progress));
        try {
            if (window.p1Practice && typeof window.p1Practice.reportStudyToParent === 'function') {
                window.p1Practice.reportStudyToParent(false);
            }
        } catch (e) {}
    }

    stepKey(mid, stepIndex) {
        return `${mid}:${stepIndex}`;
    }

    materialDoneCount(mid) {
        const m = this.getMaterial(mid);
        if (!m) return 0;
        let n = 0;
        for (let i = 0; i < (m.steps || []).length; i++) {
            if (this.progress.doneSteps[this.stepKey(mid, i)]) n++;
        }
        return n;
    }

    totalMaterialsDone() {
        return this.mainMaterials().filter(m => this.materialDoneCount(m.id) >= (m.steps || []).length).length;
    }

    updateProgressLabel() {
        const el = document.getElementById('p2ProgressText');
        if (!el) return;
        const total = this.mainMaterials().length;
        el.textContent = `素材 ${this.totalMaterialsDone()} / ${total}`;
    }

    // —— Part / Mode shell ——
    bindShell() {
        document.getElementById('partTabP1')?.addEventListener('click', () => this.showPart('p1'));
        document.getElementById('partTabP2')?.addEventListener('click', () => this.showPart('p2'));
        document.getElementById('p2ModeMemorize')?.addEventListener('click', () => this.setMode('memorize'));
        document.getElementById('p2ModeApply')?.addEventListener('click', () => this.setMode('apply'));
        document.getElementById('p2GuideClose')?.addEventListener('click', () => {
            this.progress.guideDismissed = true;
            this.saveProgress();
            const b = document.getElementById('p2GuideBanner');
            if (b) b.style.display = 'none';
        });
    }

    isStudyMode() {
        try {
            const params = new URLSearchParams(window.location.search);
            return (params.get('mode') || 'study') !== 'test';
        } catch (_) {
            return true;
        }
    }

    showPart(part) {
        const p1 = document.getElementById('part1View');
        const p2 = document.getElementById('part2View');
        const p1Nav = document.getElementById('p1NavRight');
        const p2Nav = document.getElementById('p2NavRight');
        const title = document.getElementById('navTitle');
        const progress = document.getElementById('progressText');

        document.querySelectorAll('.part-tab').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.part === part);
        });

        if (part === 'p2') {
            if (p1) p1.style.display = 'none';
            if (p2) p2.style.display = 'flex';
            if (p1Nav) p1Nav.style.display = 'none';
            if (p2Nav) p2Nav.style.display = 'flex';
            if (title) title.textContent = '口语 P2 练习';
            if (progress) progress.style.display = 'none';
            this.setMode(this.mode || 'memorize');
            this.updateProgressLabel();
        } else {
            if (p1) p1.style.display = 'flex';
            if (p2) p2.style.display = 'none';
            if (p1Nav) p1Nav.style.display = 'flex';
            if (p2Nav) p2Nav.style.display = 'none';
            if (title) title.textContent = '口语 P1 练习';
            if (progress) progress.style.display = '';
            this.stopSpeak();
            const study = this.isStudyMode();
            this.setP1Mode(study ? (this.p1Mode || 'questions') : 'questions');
        }
    }

    setP1Mode(mode) {
        const study = this.isStudyMode();
        this.p1Mode = study && mode === 'complex' ? 'complex' : 'questions';
        const practiceArea = document.getElementById('practiceArea');
        const dataPanel = document.getElementById('dataPanel');
        const complex = document.getElementById('p1ComplexPane');
        const p1Nav = document.getElementById('p1NavRight');
        const progress = document.getElementById('progressText');
        const complexEntry = document.getElementById('complexSentenceEntry');

        if (practiceArea) practiceArea.style.display = this.p1Mode === 'questions' ? '' : 'none';
        if (dataPanel) dataPanel.style.display = this.p1Mode === 'questions' ? '' : 'none';
        if (complex) complex.style.display = this.p1Mode === 'complex' ? 'flex' : 'none';
        if (p1Nav) p1Nav.style.display = this.p1Mode === 'questions' ? 'flex' : 'none';
        if (progress) progress.style.display = this.p1Mode === 'questions' ? '' : 'none';
        if (complexEntry) complexEntry.classList.toggle('active', this.p1Mode === 'complex');

        if (this.p1Mode === 'complex') {
            if (window.p1Practice && typeof window.p1Practice.stopSpeakQuestion === 'function') {
                try { window.p1Practice.stopSpeakQuestion(); } catch (_) {}
            }
            const frame = document.getElementById('p1ComplexFrame');
            if (frame && !this._complexFrameLoaded) {
                frame.src = 'complex-sentences.html?v=20260824d';
                this._complexFrameLoaded = true;
            }
        }
    }

    setMode(mode) {
        this.mode = mode;
        document.querySelectorAll('.p2-mode-tab').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.p2Mode === mode);
        });
        const mem = document.getElementById('p2MemorizePane');
        const apply = document.getElementById('p2ApplyPane');
        if (mem) mem.style.display = mode === 'memorize' ? 'flex' : 'none';
        if (apply) apply.style.display = mode === 'apply' ? 'flex' : 'none';

        if (mode === 'apply') {
            this.maybeShowGuide();
            if (this.data.questions.length && !document.getElementById('p2ApplyCard')?.style.display) {
                // keep current if already open
            }
            this.renderQuestionList();
            if (this.data.questions[this.questionIndex]) {
                this.selectQuestion(this.questionIndex);
            }
        } else {
            this.renderMaterialList();
            if (this.materialId) this.selectMaterial(this.materialId);
        }
    }

    maybeShowGuide() {
        const banner = document.getElementById('p2GuideBanner');
        if (!banner) return;
        const show = !this.progress.openedMaterial && !this.progress.guideDismissed;
        banner.style.display = show ? 'flex' : 'none';
    }

    // —— TTS ——
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
        document.querySelectorAll('#part2View .btn-speak.playing').forEach(btn => {
            btn.classList.remove('playing');
            const label = btn.querySelector('.speak-label');
            if (label) label.textContent = label.dataset.defaultLabel || '听';
        });
    }

    getP2AudioUrl(key) {
        const manifest = (typeof P2_AUDIO_MANIFEST !== 'undefined' && P2_AUDIO_MANIFEST)
            || (window.P2_AUDIO_MANIFEST || {});
        const rel = manifest[key];
        if (!rel) return '';
        try { return new URL(rel, window.location.href).href; } catch (_) { return rel; }
    }

    speakText(text, btn, audioKey) {
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
        const prebuilt = audioKey ? this.getP2AudioUrl(audioKey) : '';
        if (prebuilt) {
            this._playPrebuiltP2(prebuilt, t, btn, token);
            return;
        }
        this._speakBrowserP2(t, btn, token);
    }

    _clearSpeakBtn(btn, token) {
        if (token !== this._ttsToken) return;
        if (!btn) return;
        btn.classList.remove('playing');
        const label = btn.querySelector('.speak-label');
        if (label) label.textContent = label.dataset.defaultLabel || '听';
    }

    _playPrebuiltP2(url, text, btn, token) {
        const audio = new Audio();
        audio.preload = 'auto';
        this._ttsAudio = audio;
        let settled = false;
        const fail = () => {
            if (settled || token !== this._ttsToken) return;
            settled = true;
            this._ttsAudio = null;
            this._speakBrowserP2(text, btn, token);
        };
        audio.onended = () => this._clearSpeakBtn(btn, token);
        audio.onerror = () => fail();
        audio.src = url;
        audio.play().catch(() => fail());
    }

    _speakBrowserP2(t, btn, token) {
        if (!window.speechSynthesis) {
            this._clearSpeakBtn(btn, token);
            return;
        }
        const utter = new SpeechSynthesisUtterance(t);
        utter.lang = 'en-GB';
        utter.rate = 0.92;
        const voices = speechSynthesis.getVoices() || [];
        // Prefer male British when available
        const v = voices.find(x => /en-GB/i.test(x.lang) && /male|ryan|thomas|daniel/i.test(x.name))
            || voices.find(x => /en-GB/i.test(x.lang))
            || voices.find(x => /^en/i.test(x.lang));
        if (v) utter.voice = v;
        utter.onend = () => this._clearSpeakBtn(btn, token);
        utter.onerror = () => this._clearSpeakBtn(btn, token);
        this._ttsUtter = utter;
        try { speechSynthesis.resume(); } catch (_) {}
        setTimeout(() => {
            if (token !== this._ttsToken) return;
            try { speechSynthesis.speak(utter); } catch (_) {}
        }, 120);
    }

    escapeHtml(s) {
        return String(s || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // —— 背素材 ——
    bindMemorize() {
        document.getElementById('p2MaterialList')?.addEventListener('click', (e) => {
            const item = e.target.closest('[data-material-id]');
            if (!item) return;
            this.selectMaterial(item.dataset.materialId);
        });
    }

    renderMaterialList() {
        const box = document.getElementById('p2MaterialList');
        if (!box) return;
        const mains = this.mainMaterials();
        const optional = (this.data.materials || []).filter(m => m.optional);
        box.innerHTML = '';

        const renderItem = (m) => {
            const done = this.materialDoneCount(m.id);
            const total = (m.steps || []).length;
            const div = document.createElement('div');
            div.className = 'category-item' + (m.id === this.materialId ? ' active' : '');
            div.dataset.materialId = m.id;
            div.innerHTML = `
                <div class="category-header">
                    <span class="category-name">${this.escapeHtml(m.name)}</span>
                    <span class="category-count">${done}/${total}</span>
                </div>
                <div class="p2-side-type">${this.escapeHtml(m.type || '')}${m.audience === 'boy' ? ' · 男生向' : m.audience === 'girl' ? ' · 女生向' : ''}${m.optional ? ' · 补充' : ''}</div>
            `;
            return div;
        };

        mains.forEach(m => box.appendChild(renderItem(m)));
        if (optional.length) {
            const sep = document.createElement('div');
            sep.className = 'p2-side-label';
            sep.style.marginTop = '12px';
            sep.textContent = '补充素材';
            box.appendChild(sep);
            optional.forEach(m => box.appendChild(renderItem(m)));
        }
    }

    selectMaterial(id) {
        const m = this.getMaterial(id);
        if (!m) return;
        this.materialId = id;
        this.progress.openedMaterial = true;
        this.saveProgress();
        if (m.variants && m.variants.length && !m.variants.some(v => v.id === this.variantId)) {
            this.variantId = m.variants[0].id;
        }
        this.renderMaterialList();
        this.renderMaterialCard();
    }

    currentStepBody(m, stepIndex) {
        const step = m.steps[stepIndex];
        if (!step) return { label: '', zh: '', en: '' };
        // yumeng step1 (主体) uses variant
        if (stepIndex === 1 && m.variants && m.variants.length) {
            const v = m.variants.find(x => x.id === this.variantId) || m.variants[0];
            return { label: step.label, zh: v.zh, en: v.en, variantLabel: v.label };
        }
        return { label: step.label, zh: step.zh, en: step.en };
    }

    renderMaterialCard() {
        const m = this.getMaterial(this.materialId);
        const empty = document.getElementById('p2MemEmpty');
        const card = document.getElementById('p2MemCard');
        if (!m) {
            if (empty) empty.style.display = '';
            if (card) card.style.display = 'none';
            return;
        }
        if (empty) empty.style.display = 'none';
        if (card) card.style.display = 'block';

        document.getElementById('p2MemType').textContent = m.type || '素材';
        document.getElementById('p2MemTitle').textContent = m.name;
        const summaryEl = document.getElementById('p2MemSummary');
        const returnHint = this.returnQuestionIndex != null
            ? `<button type="button" class="btn btn-sm btn-primary" id="p2ReturnApply">返回套题</button>`
            : '';
        summaryEl.innerHTML = `${this.escapeHtml(m.summary || '')}${returnHint ? ` ${returnHint}` : ''}`;
        document.getElementById('p2ReturnApply')?.addEventListener('click', () => {
            const idx = this.returnQuestionIndex;
            this.returnQuestionIndex = null;
            this.setMode('apply');
            if (idx != null) this.selectQuestion(idx);
        });
        const done = this.materialDoneCount(m.id);
        document.getElementById('p2MemStepProgress').textContent = `${done} / ${(m.steps || []).length} 段已过`;

        const varBar = document.getElementById('p2VariantBar');
        if (m.variants && m.variants.length) {
            varBar.style.display = 'flex';
            varBar.innerHTML = m.variants.map(v => `
                <button type="button" class="p2-variant-btn${v.id === this.variantId ? ' active' : ''}" data-variant="${this.escapeHtml(v.id)}">
                    ${this.escapeHtml(v.label)}
                </button>
            `).join('');
            varBar.querySelectorAll('[data-variant]').forEach(btn => {
                btn.addEventListener('click', () => {
                    this.variantId = btn.dataset.variant;
                    this.renderMaterialCard();
                });
            });
        } else {
            varBar.style.display = 'none';
            varBar.innerHTML = '';
        }

        const stepsBox = document.getElementById('p2MemSteps');
        stepsBox.innerHTML = '';
        (m.steps || []).forEach((_, i) => {
            const body = this.currentStepBody(m, i);
            const key = this.stepKey(m.id, i);
            const hidden = !!this.hideEn[key];
            const passed = !!this.progress.doneSteps[key];
            const div = document.createElement('div');
            div.className = 'step-item p2-step-item' + (passed ? ' passed' : '');
            div.innerHTML = `
                <div class="step-header">
                    <div class="step-number">${i + 1}</div>
                    <div class="step-title">${this.escapeHtml(body.label)}${body.variantLabel ? ` · ${this.escapeHtml(body.variantLabel)}` : ''}</div>
                </div>
                <div class="p2-step-zh">${this.escapeHtml(body.zh)}</div>
                <div class="p2-step-en${hidden ? ' is-hidden' : ''}" data-en-block="${i}">
                    ${hidden ? '<span class="p2-en-placeholder">英文已遮挡 · 试着自己说出来</span>' : this.escapeHtml(body.en)}
                </div>
                <div class="p2-step-actions">
                    <button type="button" class="btn btn-sm btn-secondary p2-listen-step" data-step="${i}">听本段</button>
                    <button type="button" class="btn btn-sm btn-secondary p2-toggle-en" data-step="${i}">${hidden ? '显示英文' : '遮挡英文'}</button>
                    <button type="button" class="btn btn-sm ${passed ? 'btn-secondary' : 'btn-primary'} p2-mark-done" data-step="${i}">
                        ${passed ? '已过 ✓' : '已过'}
                    </button>
                </div>
            `;
            stepsBox.appendChild(div);
        });

        stepsBox.querySelectorAll('.p2-listen-step').forEach(btn => {
            btn.addEventListener('click', () => {
                const i = Number(btn.dataset.step);
                const body = this.currentStepBody(m, i);
                const mid = this.materialId;
                let akey = mid != null ? `material:${mid}:${i}` : '';
                // yumeng step1 may use variant
                if (mid && i === 1 && this.variantId) {
                    const vkey = `material:${mid}:1:${this.variantId}`;
                    if (this.getP2AudioUrl(vkey)) akey = vkey;
                }
                this.speakText(body.en, btn, akey);
            });
        });
        stepsBox.querySelectorAll('.p2-toggle-en').forEach(btn => {
            btn.addEventListener('click', () => {
                const i = Number(btn.dataset.step);
                const key = this.stepKey(m.id, i);
                this.hideEn[key] = !this.hideEn[key];
                this.renderMaterialCard();
            });
        });
        stepsBox.querySelectorAll('.p2-mark-done').forEach(btn => {
            btn.addEventListener('click', () => {
                const i = Number(btn.dataset.step);
                const key = this.stepKey(m.id, i);
                if (this.progress.doneSteps[key]) delete this.progress.doneSteps[key];
                else this.progress.doneSteps[key] = true;
                this.saveProgress();
                this.updateProgressLabel();
                this.renderMaterialList();
                this.renderMaterialCard();
            });
        });
    }

    // —— 套题 ——
    bindApply() {
        document.getElementById('p2QuestionList')?.addEventListener('click', (e) => {
            const item = e.target.closest('[data-q-index]');
            if (!item) return;
            this.selectQuestion(Number(item.dataset.qIndex));
        });
        document.getElementById('p2NextQBtn')?.addEventListener('click', () => {
            if (this.questionIndex < this.data.questions.length - 1) {
                this.selectQuestion(this.questionIndex + 1);
            }
        });
        document.getElementById('p2PrevQBtn')?.addEventListener('click', () => {
            if (this.questionIndex > 0) {
                this.selectQuestion(this.questionIndex - 1);
            }
        });
        document.getElementById('p2SpeakQBtn')?.addEventListener('click', () => {
            const q = this.data.questions[this.questionIndex];
            const qid = q && q.id;
            this.speakText(q?.q || q?.title, document.getElementById('p2SpeakQBtn'), qid != null ? `question:${qid}:q` : '');
        });
    }

    applyMaterialIds(q) {
        if (!q) return [];
        if (q.materialOptions && q.materialOptions.length) return q.materialOptions;
        if (q.materialIds && q.materialIds.length) return q.materialIds;
        return q.materialId ? [q.materialId] : [];
    }

    selectedApplyMaterialId(q) {
        const ids = this.applyMaterialIds(q);
        if (!ids.length) return null;
        const saved = this.applyMaterialChoice[q.id];
        if (saved && ids.includes(saved)) return saved;
        return q.materialId && ids.includes(q.materialId) ? q.materialId : ids[0];
    }

    audienceLabel(m) {
        if (!m) return '';
        if (m.audience === 'boy') return '男生向';
        if (m.audience === 'girl') return '女生向';
        return '';
    }

    renderQuestionList() {
        const box = document.getElementById('p2QuestionList');
        if (!box) return;
        box.innerHTML = '';
        (this.data.questions || []).forEach((q, idx) => {
            const mid = this.selectedApplyMaterialId(q) || q.materialId;
            const mat = this.getMaterial(mid);
            const opts = this.applyMaterialIds(q);
            const sideNote = opts.length > 1
                ? `${this.escapeHtml(mat ? mat.name : mid || '')}（可换）`
                : this.escapeHtml(mat ? mat.name : q.materialId || '');
            const div = document.createElement('div');
            div.className = 'question-item' + (idx === this.questionIndex ? ' active' : '');
            div.dataset.qIndex = String(idx);
            div.innerHTML = `
                <div class="question-item-title">${idx + 1}. ${this.escapeHtml(q.title || q.q)}</div>
                <div class="p2-side-type">${sideNote}</div>
            `;
            box.appendChild(div);
        });
    }

    selectQuestion(index) {
        if (index < 0 || index >= (this.data.questions || []).length) return;
        this.questionIndex = index;
        this.hideOpening = false;
        this.expandedMaterial = false;
        this.renderQuestionList();
        this.renderApplyCard();
    }

    renderApplyCard() {
        const q = this.data.questions[this.questionIndex];
        const empty = document.getElementById('p2ApplyEmpty');
        const card = document.getElementById('p2ApplyCard');
        if (!q) {
            if (empty) empty.style.display = '';
            if (card) card.style.display = 'none';
            return;
        }
        if (empty) empty.style.display = 'none';
        if (card) card.style.display = 'block';

        document.getElementById('p2ApplyTitle').textContent = q.title || q.q;
        document.getElementById('p2ApplyQ').textContent = q.q || '';

        const matIds = this.applyMaterialIds(q);
        const selectedId = this.selectedApplyMaterialId(q);
        const primary = this.getMaterial(selectedId);
        const ending = q.endingTip || (primary && primary.endingTip) || '用素材第三步感受收尾';
        const hint = (q.materialHintById && q.materialHintById[selectedId]) || q.materialHint || '';
        const openingOverride = q.openingById && q.openingById[selectedId];
        const openingEn = (openingOverride && openingOverride.en) || q.openingEn || '';
        const openingZh = (openingOverride && openingOverride.zh) || q.openingZh || '';

        const blocks = document.getElementById('p2ApplyBlocks');
        const switcher = matIds.length > 1
            ? `<div class="p2-mat-switch" role="group" aria-label="选择物品素材版本">
                ${matIds.map(id => {
                    const m = this.getMaterial(id);
                    const label = this.audienceLabel(m) || (m ? m.name : id);
                    const short = m ? (m.id === 'basketball' ? '篮球' : m.id === 'bear' ? '小熊' : m.name) : id;
                    const active = id === selectedId ? ' active' : '';
                    return `<button type="button" class="p2-mat-opt${active}" data-apply-mat="${this.escapeHtml(id)}">${this.escapeHtml(label)} · ${this.escapeHtml(short)}</button>`;
                }).join('')}
               </div>`
            : '';

        const matTag = primary ? primary.name : (selectedId || '');

        const stepSummaries = (primary?.steps || []).map((s, i) => {
            const body = primary ? this.currentStepBodyForApply(primary, i) : s;
            const short = (body.zh || '').slice(0, 36);
            return `<li><strong>${this.escapeHtml(s.label)}</strong>：${this.escapeHtml(short)}${(body.zh || '').length > 36 ? '…' : ''}</li>`;
        }).join('');

        const fullSteps = (primary?.steps || []).map((s, i) => {
            const body = this.currentStepBodyForApply(primary, i);
            return `
                <div class="p2-full-step">
                    <div class="p2-full-label">${i + 1}. ${this.escapeHtml(s.label)}</div>
                    <div class="p2-step-zh">${this.escapeHtml(body.zh)}</div>
                    <div class="p2-step-en">${this.escapeHtml(body.en)}</div>
                </div>
            `;
        }).join('');

        blocks.innerHTML = `
            <div class="step-item p2-apply-block">
                <div class="step-header">
                    <div class="step-number">1</div>
                    <div class="step-title">开头 · 扣题过渡（约 15 秒）</div>
                </div>
                ${openingZh ? `<div class="p2-step-zh">${this.escapeHtml(openingZh)}</div>` : ''}
                <div class="p2-step-en${this.hideOpening ? ' is-hidden' : ''}">
                    ${this.hideOpening ? '<span class="p2-en-placeholder">过渡句已遮挡 · 试着自己说</span>' : this.escapeHtml(openingEn)}
                </div>
                <div class="p2-step-actions">
                    <button type="button" class="btn btn-sm btn-secondary" id="p2ListenOpening">听过渡句</button>
                    <button type="button" class="btn btn-sm btn-secondary" id="p2ToggleOpening">${this.hideOpening ? '显示英文' : '遮挡英文'}</button>
                </div>
            </div>

            <div class="step-item p2-apply-block">
                <div class="step-header">
                    <div class="step-number">2</div>
                    <div class="step-title">中间 · 套素材（约 1 分 30 秒）</div>
                </div>
                ${switcher}
                <div class="p2-material-tag">套用素材：【${this.escapeHtml(matTag)}】</div>
                <div class="p2-material-hint">${this.escapeHtml(hint)}</div>
                <ul class="p2-step-summary-list">${stepSummaries}</ul>
                <div class="p2-step-actions">
                    <button type="button" class="btn btn-sm btn-secondary" id="p2ExpandMat">${this.expandedMaterial ? '收起完整素材' : '展开完整素材'}</button>
                    <button type="button" class="btn btn-sm btn-primary" id="p2GoMemorize">去背这篇</button>
                </div>
                <div class="p2-full-material" id="p2FullMaterial" style="display:${this.expandedMaterial ? 'block' : 'none'}">
                    ${fullSteps || '<p class="tip-empty">暂无素材正文</p>'}
                </div>
            </div>

            <div class="step-item p2-apply-block">
                <div class="step-header">
                    <div class="step-number">3</div>
                    <div class="step-title">结尾 · 感受收尾（约 15 秒）</div>
                </div>
                <div class="p2-ending-tip">${this.escapeHtml(ending)}</div>
                <p class="p2-ending-note">不必另编故事，用素材第三步感受自然收住即可。</p>
            </div>
        `;

        document.getElementById('p2ListenOpening')?.addEventListener('click', (e) => {
            const q = this.data.questions[this.questionIndex];
            const qid = q && q.id;
            let okey = qid != null ? `question:${qid}:opening` : '';
            const choice = qid != null ? this.applyMaterialChoice[qid] : null;
            if (choice) {
                const ckey = `question:${qid}:opening:${choice}`;
                if (this.getP2AudioUrl(ckey)) okey = ckey;
            }
            this.speakText(openingEn, e.currentTarget, okey);
        });
        document.getElementById('p2ToggleOpening')?.addEventListener('click', () => {
            this.hideOpening = !this.hideOpening;
            this.renderApplyCard();
        });
        document.getElementById('p2ExpandMat')?.addEventListener('click', () => {
            this.expandedMaterial = !this.expandedMaterial;
            this.renderApplyCard();
        });
        blocks.querySelectorAll('[data-apply-mat]').forEach(btn => {
            btn.addEventListener('click', () => {
                const mid = btn.getAttribute('data-apply-mat');
                if (!mid || mid === selectedId) return;
                this.applyMaterialChoice[q.id] = mid;
                this.hideOpening = false;
                this.expandedMaterial = false;
                this.renderQuestionList();
                this.renderApplyCard();
            });
        });
        document.getElementById('p2GoMemorize')?.addEventListener('click', () => {
            this.returnQuestionIndex = this.questionIndex;
            const mid = selectedId || q.materialId || matIds[0];
            this.setMode('memorize');
            this.selectMaterial(mid);
        });

        const prev = document.getElementById('p2PrevQBtn');
        const next = document.getElementById('p2NextQBtn');
        if (prev) prev.disabled = this.questionIndex <= 0;
        if (next) next.disabled = this.questionIndex >= this.data.questions.length - 1;
    }

    currentStepBodyForApply(m, stepIndex) {
        // In apply mode, always show default step (variant A for yumeng)
        const step = m.steps[stepIndex];
        if (!step) return { zh: '', en: '' };
        if (stepIndex === 1 && m.variants && m.variants.length) {
            const v = m.variants.find(x => x.id === 'a') || m.variants[0];
            return { zh: v.zh, en: v.en };
        }
        return { zh: step.zh, en: step.en };
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.p2Practice = new P2Practice();
    // 默认仍在 P1；URL ?part=p2 时打开 P2
    const params = new URLSearchParams(window.location.search);
    if (params.get('part') === 'p2') {
        window.p2Practice.showPart('p2');
        window.p2Practice.setMode('memorize');
    } else {
        window.p2Practice.showPart('p1');
        if (params.get('p1') === 'complex' && window.p2Practice.isStudyMode()) {
            window.p2Practice.setP1Mode('complex');
        }
    }
});

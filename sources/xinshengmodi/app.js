/**
 * 入学摸底 · 流程状态机（听 → 读 → 词伙 → 翻译 → 口语 → 报告）
 */
(function () {
  var SECTIONS = [
    { id: 'listening', name: '听力听写', minutes: 10 },
    { id: 'reading', name: '阅读同义', minutes: 10 },
    { id: 'phrase', name: '写作词伙', minutes: 4 },
    { id: 'translate', name: '写作翻译', minutes: 6 },
    { id: 'speaking', name: '口语录音', minutes: 8 }
  ];

  var state = {
    form: null,
    debug: false,
    sectionIndex: -1,
    sectionEndsAt: 0,
    timerId: null,
    startedAt: 0,
    reportSent: false,
    answers: {
      listening: [],
      reading: [],
      phrase: [],
      translate: [],
      speaking: []
    },
    meta: {
      listening: { timedOut: false },
      reading: { timedOut: false },
      phrase: { timedOut: false },
      translate: { timedOut: false },
      speaking: { timedOut: false }
    },
    speaking: {
      index: 0,
      recorder: null,
      stream: null,
      chunks: [],
      blob: null,
      recording: false,
      results: []
    },
    report: null,
    listenAudio: {
      cache: {},
      current: null,
      ready: false
    },
    guest: false,
    guestProfile: {
      name: '',
      contact: '',
      targetScore: 6.5
    },
    guestSavedId: null,
    guestSaveError: ''
  };

  function qs(name) {
    return new URLSearchParams(window.location.search).get(name);
  }

  function isGuestMode() {
    if (qs('guest') === '1' || qs('mode') === 'guest') return true;
    // 独立打开且无学号 → 访客
    if (!qs('student_id') && window.parent === window) return true;
    return false;
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function normalizeDictation(s) {
    if (window.PlacementScoring && PlacementScoring.normalizeDictationText) {
      return PlacementScoring.normalizeDictationText(s);
    }
    return String(s || '')
      .toLowerCase()
      .replace(/[''']/g, "'")
      .replace(/[""]/g, '"')
      .replace(/[—–-]/g, '-')
      .replace(/[^\w\s'-]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function gradeListeningAnswer(user, answer) {
    if (window.PlacementScoring && PlacementScoring.gradeDictation) {
      return PlacementScoring.gradeDictation(user, answer);
    }
    var a = normalizeDictation(answer);
    var b = normalizeDictation(user);
    var full = !!(a && b && a === b);
    return { coverage: full ? 1 : 0, hit: full ? 1 : 0, need: 1, correct: full, empty: !b };
  }

  function sliceForm(form) {
    if (!state.debug) return form;
    return {
      form: form.form,
      listening: form.listening.slice(0, 2),
      reading: form.reading.slice(0, 4),
      phrase: form.phrase.slice(0, 2),
      translate: form.translate.slice(0, 1),
      speaking: form.speaking.slice(0, 1)
    };
  }

  function currentSection() {
    return SECTIONS[state.sectionIndex] || null;
  }

  function stopTimer() {
    if (state.timerId) {
      clearInterval(state.timerId);
      state.timerId = null;
    }
  }

  function startSectionTimer(minutes) {
    stopTimer();
    var ms = state.debug ? Math.min(minutes, 2) * 60 * 1000 : minutes * 60 * 1000;
    state.sectionEndsAt = Date.now() + ms;
    updateTimerUi();
    state.timerId = setInterval(function () {
      updateTimerUi();
      if (Date.now() >= state.sectionEndsAt) {
        stopTimer();
        onSectionTimeout();
      }
    }, 250);
  }

  function updateTimerUi() {
    var el = document.getElementById('sectionTimer');
    if (!el) return;
    var left = Math.max(0, state.sectionEndsAt - Date.now());
    var sec = Math.ceil(left / 1000);
    var m = Math.floor(sec / 60);
    var s = sec % 60;
    el.textContent = m + ':' + (s < 10 ? '0' : '') + s;
    el.classList.toggle('urgent', sec <= 60);
  }

  function onSectionTimeout() {
    var sec = currentSection();
    if (!sec) return;
    state.meta[sec.id].timedOut = true;
    if (sec.id === 'listening') collectListening(true);
    else if (sec.id === 'reading') collectReading(true);
    else if (sec.id === 'phrase') collectPhrase(true);
    else if (sec.id === 'translate') collectTranslate(true);
    else if (sec.id === 'speaking') finishSpeakingSection(true);
  }

  function renderShell(inner) {
    var sec = currentSection();
    var progress = state.sectionIndex < 0 ? 0 : Math.round(((state.sectionIndex) / SECTIONS.length) * 100);
    var app = document.getElementById('app');
    app.innerHTML =
      '<div class="topbar">' +
        '<div class="brand">入学摸底 · 套别 ' + escapeHtml((state.form && state.form.form) || 'A') +
          (state.debug ? ' · DEBUG' : '') + '</div>' +
        '<div class="top-meta">' +
          (sec ? '<span class="sec-name">' + escapeHtml(sec.name) + '</span>' : '') +
          '<span class="timer" id="sectionTimer">—</span>' +
        '</div>' +
      '</div>' +
      '<div class="progress-wrap"><div class="progress-bar"><div class="progress-fill" style="width:' + progress + '%"></div></div>' +
      '<div class="progress-text">' + Math.max(0, state.sectionIndex + 1) + ' / ' + SECTIONS.length + ' 科</div></div>' +
      '<div class="body">' + inner + '</div>';
  }

  function renderIntro() {
    stopTimer();
    state.sectionIndex = -1;
    var app = document.getElementById('app');
    var guestBlock = '';
    if (state.guest) {
      guestBlock =
        '<div class="guest-form">' +
          '<p class="guest-tag">临时访客入口 · 无需学号</p>' +
          '<label class="field"><span>姓名 <em>*</em></span>' +
            '<input id="guestName" class="text-input" maxlength="40" placeholder="怎么称呼你" autocomplete="name" /></label>' +
          '<label class="field"><span>手机 / 微信</span>' +
            '<input id="guestContact" class="text-input" maxlength="80" placeholder="选填，方便老师联系" autocomplete="tel" /></label>' +
          '<label class="field"><span>目标分</span>' +
            '<select id="guestTarget" class="text-input">' +
              '<option value="5">5.0</option>' +
              '<option value="5.5">5.5</option>' +
              '<option value="6">6.0</option>' +
              '<option value="6.5" selected>6.5</option>' +
              '<option value="7">7.0</option>' +
              '<option value="7.5">7.5</option>' +
            '</select></label>' +
        '</div>';
    }
    app.innerHTML =
      '<div class="intro">' +
        '<h1>雅思入学能力摸底</h1>' +
        '<p class="sub">约 40 分钟 · 听 / 读 / 写 / 口 分科预估 · 试卷套别 A' +
          (state.guest ? ' · 访客模式' : '') + '</p>' +
        guestBlock +
        '<div class="rules">' +
          '<p><strong>流程</strong>：听力听写 10 分钟 → 阅读同义 10 分钟 → 写作词伙+翻译 10 分钟 → 口语现场录 8 分钟 → 查看报告</p>' +
          '<p><strong>注意</strong>：每科独立计时，到点自动交卷；中途请勿刷新页面。口语需允许麦克风。</p>' +
          '<p><strong>用途</strong>：给助教排基础训练与课程参考，<em>不是</em>官方雅思成绩。' +
            (state.guest ? '完成后结果会提交给老师查看。' : '') + '</p>' +
        '</div>' +
        '<button class="btn primary block" id="startBtn">开始摸底</button>' +
      '</div>';
    document.getElementById('startBtn').onclick = function () {
      if (state.guest) {
        var nameEl = document.getElementById('guestName');
        var contactEl = document.getElementById('guestContact');
        var targetEl = document.getElementById('guestTarget');
        var name = nameEl ? String(nameEl.value || '').trim() : '';
        if (!name) {
          alert('请先填写姓名');
          if (nameEl) nameEl.focus();
          return;
        }
        state.guestProfile = {
          name: name,
          contact: contactEl ? String(contactEl.value || '').trim() : '',
          targetScore: targetEl ? Number(targetEl.value) || 6.5 : 6.5
        };
      }
      state.startedAt = Date.now();
      state.reportSent = false;
      state.guestSavedId = null;
      state.guestSaveError = '';
      goSection(0);
    };
  }

  function goSection(index) {
    stopSpeakingMedia();
    stopListeningAudio();
    state.sectionIndex = index;
    var sec = currentSection();
    if (!sec) {
      buildAndShowReport();
      return;
    }
    startSectionTimer(sec.minutes);
    if (sec.id === 'listening') renderListening();
    else if (sec.id === 'reading') renderReading();
    else if (sec.id === 'phrase') renderPhrase();
    else if (sec.id === 'translate') renderTranslate();
    else if (sec.id === 'speaking') renderSpeaking();
  }

  function nextSection() {
    goSection(state.sectionIndex + 1);
  }

  // —— 听力 ——
  function listeningAudioUrl(q) {
    if (!q) return '';
    if (q.audio) {
      try {
        return new URL(q.audio, window.location.href).href;
      } catch (e) {
        return q.audio;
      }
    }
    return '';
  }

  function stopListeningAudio() {
    try {
      if (window.speechSynthesis) window.speechSynthesis.cancel();
    } catch (e) {}
    if (state.listenAudio.current) {
      try {
        state.listenAudio.current.pause();
        state.listenAudio.current.currentTime = 0;
      } catch (e) {}
      state.listenAudio.current = null;
    }
  }

  function preloadListeningAudio() {
    var items = state.form.listening || [];
    state.listenAudio.cache = {};
    state.listenAudio.ready = false;
    var pending = 0;
    var done = 0;
    items.forEach(function (q) {
      var url = listeningAudioUrl(q);
      if (!url) return;
      pending += 1;
      var audio = new Audio();
      audio.preload = 'auto';
      audio.playbackRate = 0.9;
      audio.src = url;
      var finish = function () {
        done += 1;
        if (done >= pending) state.listenAudio.ready = true;
      };
      audio.addEventListener('canplaythrough', finish, { once: true });
      audio.addEventListener('error', finish, { once: true });
      try { audio.load(); } catch (e) { finish(); }
      state.listenAudio.cache[q.id] = audio;
    });
    if (!pending) state.listenAudio.ready = true;
  }

  function playListeningItem(index) {
    var items = state.form.listening;
    var q = items[index];
    if (!q) return;
    stopListeningAudio();
    var cached = state.listenAudio.cache[q.id];
    var playNode = cached;
    if (!playNode || playNode.error) {
      var url = listeningAudioUrl(q);
      if (url) {
        playNode = new Audio(url);
        state.listenAudio.cache[q.id] = playNode;
      }
    }
    if (playNode) {
      try {
        playNode.currentTime = 0;
      } catch (e) {}
      try {
        playNode.playbackRate = 0.9;
      } catch (e) {}
      state.listenAudio.current = playNode;
      var p = playNode.play();
      if (p && typeof p.then === 'function') {
        p.catch(function () {
          // 预生成音频缺失时回退浏览器 TTS
          playTtsFallback(q.text);
        });
      }
      return;
    }
    playTtsFallback(q.text);
  }

  function playTtsFallback(text) {
    try {
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-GB';
      u.rate = 0.9;
      window.speechSynthesis.speak(u);
    } catch (e) {
      alert('无法播放音频，请确认已生成 mp3，或换 Chrome/Edge。');
    }
  }

  function renderListening() {
    var items = state.form.listening;
    preloadListeningAudio();
    var rows = items.map(function (q, i) {
      return (
        '<div class="q-card" data-i="' + i + '">' +
          '<div class="q-head"><span>第 ' + (i + 1) + ' 句</span>' +
          '<button type="button" class="btn sm play-btn" data-i="' + i + '">▶ 播放</button></div>' +
          '<input class="text-input listen-input" data-i="' + i + '" placeholder="尽量写全句；写不全也可先写听到的关键词…" autocomplete="off" />' +
        '</div>'
      );
    }).join('');
    renderShell(
      '<p class="hint">点击播放预生成录音（进入本科时预加载）；<strong>写不全也请写关键词</strong>（按关键词覆盖给分）。可重复播放。共 ' +
        items.length + ' 句。</p>' +
      rows +
      '<button class="btn primary block" id="submitListening">提交听力，进入阅读</button>'
    );
    updateTimerUi();
    Array.prototype.forEach.call(document.querySelectorAll('.play-btn'), function (btn) {
      btn.onclick = function () {
        playListeningItem(Number(btn.getAttribute('data-i')));
      };
    });
    document.getElementById('submitListening').onclick = function () { collectListening(false); };
  }

  function collectListening(fromTimeout) {
    var items = state.form.listening;
    state.answers.listening = items.map(function (q, i) {
      var input = document.querySelector('.listen-input[data-i="' + i + '"]');
      var user = input ? String(input.value).trim() : '';
      var grade = gradeListeningAnswer(user, q.text);
      return {
        id: q.id,
        user: user,
        correct: !!grade.correct,
        coverage: grade.coverage,
        hit: grade.hit,
        need: grade.need,
        answer: q.text
      };
    });
    stopListeningAudio();
    if (!fromTimeout) stopTimer();
    nextSection();
  }

  // —— 阅读 ——
  function renderReading() {
    var items = state.form.reading;
    var rows = items.map(function (q, i) {
      var opts = q.options.map(function (op, oi) {
        return (
          '<label class="opt">' +
            '<input type="radio" name="r' + i + '" value="' + oi + '" />' +
            '<span>' + escapeHtml(op) + '</span>' +
          '</label>'
        );
      }).join('');
      return (
        '<div class="q-card">' +
          '<div class="q-head">第 ' + (i + 1) + ' 题 · 与 <strong>' + escapeHtml(q.stem) + '</strong> 同义的是？</div>' +
          '<div class="opts">' + opts + '</div>' +
        '</div>'
      );
    }).join('');
    renderShell(
      '<p class="hint">限时选择同义词。共 ' + items.length + ' 题。</p>' +
      rows +
      '<button class="btn primary block" id="submitReading">提交阅读，进入写作</button>'
    );
    updateTimerUi();
    document.getElementById('submitReading').onclick = function () { collectReading(false); };
  }

  function collectReading(fromTimeout) {
    var items = state.form.reading;
    state.answers.reading = items.map(function (q, i) {
      var checked = document.querySelector('input[name="r' + i + '"]:checked');
      var idx = checked ? Number(checked.value) : -1;
      return {
        id: q.id,
        user_idx: idx,
        correct: idx === q.correct_idx,
        answered: idx >= 0
      };
    });
    if (!fromTimeout) stopTimer();
    nextSection();
  }

  // —— 词伙 ——
  function renderPhrase() {
    var items = state.form.phrase;
    var rows = items.map(function (q, i) {
      return (
        '<div class="q-card">' +
          '<div class="q-head">第 ' + (i + 1) + ' 题</div>' +
          '<div class="prompt-zh">' + escapeHtml(q.zh) + '</div>' +
          '<input class="text-input phrase-input" data-i="' + i + '" placeholder="写出英文词伙…" autocomplete="off" />' +
        '</div>'
      );
    }).join('');
    renderShell(
      '<p class="hint">根据中文写出对应英文词伙。共 ' + items.length + ' 题。</p>' +
      rows +
      '<button class="btn primary block" id="submitPhrase">提交词伙，进入翻译</button>'
    );
    updateTimerUi();
    document.getElementById('submitPhrase').onclick = function () { collectPhrase(false); };
  }

  function collectPhrase(fromTimeout) {
    var items = state.form.phrase;
    var checker = window.phraseIsCorrect;
    state.answers.phrase = items.map(function (q, i) {
      var input = document.querySelector('.phrase-input[data-i="' + i + '"]');
      var user = input ? input.value : '';
      var ok = typeof checker === 'function' ? checker(user, q.en) : normalizeDictation(user) === normalizeDictation(q.en);
      return { id: q.id, user: String(user).trim(), correct: !!ok, answer: q.en };
    });
    if (!fromTimeout) stopTimer();
    nextSection();
  }

  // —— 翻译 ——
  function renderTranslate() {
    var items = state.form.translate;
    var rows = items.map(function (q, i) {
      return (
        '<div class="q-card">' +
          '<div class="q-head">第 ' + (i + 1) + ' 题 · 看英文，写中文</div>' +
          '<div class="prompt-en">' + escapeHtml(q.en) + '</div>' +
          '<textarea class="text-area translate-input" data-i="' + i + '" placeholder="输入中文…" rows="3"></textarea>' +
        '</div>'
      );
    }).join('');
    renderShell(
      '<p class="hint">写出对应中文。共 ' + items.length + ' 句。</p>' +
      rows +
      '<button class="btn primary block" id="submitTranslate">提交翻译，进入口语</button>'
    );
    updateTimerUi();
    document.getElementById('submitTranslate').onclick = function () { collectTranslate(false); };
  }

  function collectTranslate(fromTimeout) {
    var items = state.form.translate;
    var gradeFn = window.TranslateMatch && window.TranslateMatch.gradeChinese;
    state.answers.translate = items.map(function (q, i) {
      var input = document.querySelector('.translate-input[data-i="' + i + '"]');
      var user = input ? input.value : '';
      var ok = false;
      if (typeof gradeFn === 'function') {
        ok = !!(gradeFn(user, q.zh) || {}).ok;
      } else {
        ok = String(user).replace(/\s+/g, '') === String(q.zh).replace(/\s+/g, '');
      }
      return { id: q.id, user: String(user).trim(), correct: ok, answer: q.zh };
    });
    if (!fromTimeout) stopTimer();
    nextSection();
  }

  // —— 口语 ——
  function renderSpeaking() {
    state.speaking.index = 0;
    state.speaking.results = [];
    showSpeakingQuestion();
  }

  function showSpeakingQuestion() {
    var items = state.form.speaking;
    var i = state.speaking.index;
    var q = items[i];
    renderShell(
      '<p class="hint">Part 1 · 现场录音。每题建议说 30–45 秒，共 ' + items.length + ' 题。</p>' +
      '<div class="q-card">' +
        '<div class="q-head">口语第 ' + (i + 1) + ' / ' + items.length + ' 题</div>' +
        '<div class="speak-q">' + escapeHtml(q.q) + '</div>' +
        '<div class="speak-hint">' + escapeHtml(q.hint || '') + '</div>' +
        '<div class="speak-status" id="speakStatus">点击下方按钮开始录音</div>' +
        '<div class="speak-transcript" id="speakTranscript"></div>' +
        '<div class="speak-actions">' +
          '<button class="btn danger" id="recBtn">开始录音</button>' +
          '<button class="btn" id="skipSpeakBtn" type="button">跳过本题</button>' +
        '</div>' +
      '</div>' +
      '<button class="btn primary block" id="nextSpeakBtn" disabled>下一题</button>'
    );
    updateTimerUi();
    var recBtn = document.getElementById('recBtn');
    var nextBtn = document.getElementById('nextSpeakBtn');
    recBtn.onclick = function () {
      if (state.speaking.recording) stopRecording();
      else startRecording();
    };
    document.getElementById('skipSpeakBtn').onclick = function () {
      pushSpeakingResult({ id: q.id, q: q.q, transcript: '', overall: null, failed: true, skipped: true });
      advanceSpeaking();
    };
    nextBtn.onclick = function () { advanceSpeaking(); };
  }

  function pushSpeakingResult(row) {
    state.speaking.results.push(row);
  }

  function advanceSpeaking() {
    stopSpeakingMedia();
    if (state.speaking.index + 1 >= state.form.speaking.length) {
      finishSpeakingSection(false);
    } else {
      state.speaking.index += 1;
      showSpeakingQuestion();
    }
  }

  function finishSpeakingSection(fromTimeout) {
    if (!fromTimeout) stopTimer();
    // 若当前题还没写入结果，补空
    while (state.speaking.results.length < state.form.speaking.length) {
      var q = state.form.speaking[state.speaking.results.length];
      pushSpeakingResult({ id: q.id, q: q.q, transcript: '', overall: null, failed: true, timedOut: !!fromTimeout });
    }
    state.answers.speaking = state.speaking.results.slice();
    // 异步估分后出报告
    renderShell('<p class="hint">正在汇总口语评分，请稍候…</p><div class="speak-status" id="speakStatus">处理中</div>');
    evaluateAllSpeaking().then(function () {
      buildAndShowReport();
    }).catch(function () {
      buildAndShowReport();
    });
  }

  function stopSpeakingMedia() {
    try {
      if (state.speaking.recorder && state.speaking.recording) {
        state.speaking.recorder.stop();
      }
    } catch (e) {}
    state.speaking.recording = false;
    if (state.speaking.stream) {
      state.speaking.stream.getTracks().forEach(function (t) { t.stop(); });
      state.speaking.stream = null;
    }
  }

  async function startRecording() {
    var status = document.getElementById('speakStatus');
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('当前浏览器不支持录音');
      }
      state.speaking.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      state.speaking.chunks = [];
      var mime = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : (MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : '');
      state.speaking.recorder = mime
        ? new MediaRecorder(state.speaking.stream, { mimeType: mime })
        : new MediaRecorder(state.speaking.stream);
      state.speaking.recorder.ondataavailable = function (e) {
        if (e.data && e.data.size > 0) state.speaking.chunks.push(e.data);
      };
      state.speaking.recorder.onstop = function () {
        state.speaking.blob = new Blob(state.speaking.chunks, { type: (state.speaking.recorder && state.speaking.recorder.mimeType) || 'audio/webm' });
        onRecordingStopped();
      };
      state.speaking.recorder.start();
      state.speaking.recording = true;
      var btn = document.getElementById('recBtn');
      if (btn) btn.textContent = '停止录音';
      if (status) status.textContent = '录音中… 说完后点击停止';
    } catch (err) {
      if (status) status.textContent = '无法打开麦克风：' + (err.message || err);
      alert('无法打开麦克风，请检查权限后重试，或跳过本题。');
    }
  }

  function stopRecording() {
    if (!state.speaking.recorder || !state.speaking.recording) return;
    try { state.speaking.recorder.stop(); } catch (e) {}
    state.speaking.recording = false;
    var btn = document.getElementById('recBtn');
    if (btn) btn.textContent = '开始录音';
    var status = document.getElementById('speakStatus');
    if (status) status.textContent = '正在识别…';
  }

  async function onRecordingStopped() {
    if (state.speaking.stream) {
      state.speaking.stream.getTracks().forEach(function (t) { t.stop(); });
      state.speaking.stream = null;
    }
    var status = document.getElementById('speakStatus');
    var transcriptEl = document.getElementById('speakTranscript');
    var nextBtn = document.getElementById('nextSpeakBtn');
    try {
      var transcript = await transcribeBlob(state.speaking.blob);
      if (transcriptEl) transcriptEl.textContent = transcript || '（未识别到文字）';
      if (status) status.textContent = transcript.length > 5 ? '识别完成，可进入下一题（交卷后统一 AI 估分）' : '识别内容过短，可重录或跳过';
      var q = state.form.speaking[state.speaking.index];
      // 覆盖同题旧结果
      state.speaking.results = state.speaking.results.filter(function (r) { return r.id !== q.id; });
      pushSpeakingResult({
        id: q.id,
        q: q.q,
        transcript: transcript,
        overall: null,
        failed: transcript.length < 5
      });
      if (nextBtn) nextBtn.disabled = false;
    } catch (err) {
      if (status) status.textContent = '识别失败：' + (err.message || err);
      if (nextBtn) nextBtn.disabled = false;
      var q2 = state.form.speaking[state.speaking.index];
      state.speaking.results = state.speaking.results.filter(function (r) { return r.id !== q2.id; });
      pushSpeakingResult({ id: q2.id, q: q2.q, transcript: '', overall: null, failed: true, error: String(err.message || err) });
    }
  }

  async function transcribeBlob(blob) {
    if (!blob || blob.size < 800) throw new Error('录音太短');
    var urls = state.guest
      ? ['/api/placement/guest-transcribe', 'https://p4.oyenglish.com.cn/transcribe']
      : ['/api/p4/transcribe', 'https://p4.oyenglish.com.cn/transcribe'];
    var lastErr = null;
    for (var i = 0; i < urls.length; i++) {
      try {
        var form = new FormData();
        form.append('file', blob, 'recording.webm');
        var res = await fetch(urls[i], {
          method: 'POST',
          body: form,
          credentials: urls[i].startsWith('/') ? 'include' : 'omit'
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        var data = await res.json();
        if (data && data.error) throw new Error(typeof data.error === 'string' ? data.error : (data.error.message || '识别失败'));
        return String(data.recognizedText || data.text || data.transcript || '').trim();
      } catch (e) {
        lastErr = e;
      }
    }
    throw lastErr || new Error('识别失败');
  }

  async function evaluateAllSpeaking() {
    var results = state.answers.speaking || [];
    for (var i = 0; i < results.length; i++) {
      var row = results[i];
      if (!row.transcript || row.transcript.length < 5) {
        row.overall = null;
        row.confidence = '低';
        continue;
      }
      try {
        var parsed = await evaluateSpeakingAi(row.q, row.transcript);
        row.overall = parsed.overall;
        row.subscores = {
          fluency: parsed.fluency,
          vocabulary: parsed.vocabulary,
          grammar: parsed.grammar,
          pronunciation: parsed.pronunciation
        };
        row.confidence = '中';
        row.aiSummary = parsed.summary || '';
      } catch (e) {
        row.overall = heuristicSpeaking(row.transcript);
        row.confidence = '低';
        row.failed = true;
        row.error = String(e.message || e);
      }
    }
  }

  function heuristicSpeaking(transcript) {
    var t = String(transcript || '').trim();
    var words = t.split(/\s+/).filter(Boolean).length;
    if (words < 8) return 4.5;
    if (words < 20) return 5.0;
    if (words < 40) return 5.5;
    return 6.0;
  }

  async function evaluateSpeakingAi(question, transcript) {
    var prompt =
      '你是雅思口语考官。根据学生 Part 1 回答，只输出一个 JSON 对象，不要其它文字。\n' +
      '字段：fluency, vocabulary, grammar, pronunciation（均为 1-9 整数），overall（可为 x.5），summary（中文一句短评）。\n' +
      '题目：' + question + '\n' +
      '回答转写：' + transcript;
    var aiUrl = state.guest ? '/api/placement/guest-ai' : '/api/ai/messages';
    var response = await fetch(aiUrl, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        max_tokens: 800,
        temperature: 0.3,
        messages: [{ role: 'user', content: prompt }],
        system: 'You score IELTS Speaking briefly. Output JSON only.'
      })
    });
    if (response.status === 401) throw new Error('请先登录主站');
    if (!response.ok) throw new Error('AI HTTP ' + response.status);
    var data = await response.json();
    var text = '';
    if (data.content && data.content[0] && data.content[0].text) text = data.content[0].text;
    else if (data.choices && data.choices[0] && data.choices[0].message) text = data.choices[0].message.content;
    else if (data.output) text = data.output;
    else if (data.text) text = data.text;
    else text = JSON.stringify(data);
    var m = String(text).match(/\{[\s\S]*\}/);
    if (!m) throw new Error('AI 未返回 JSON');
    var parsed = JSON.parse(m[0]);
    var overall = Number(parsed.overall);
    if (!isFinite(overall)) {
      var parts = [parsed.fluency, parsed.vocabulary, parsed.grammar, parsed.pronunciation]
        .map(Number).filter(function (n) { return isFinite(n); });
      overall = parts.length ? parts.reduce(function (a, b) { return a + b; }, 0) / parts.length : NaN;
    }
    if (!isFinite(overall)) throw new Error('无有效分数');
    overall = Math.round(overall * 2) / 2;
    return {
      fluency: Number(parsed.fluency) || null,
      vocabulary: Number(parsed.vocabulary) || null,
      grammar: Number(parsed.grammar) || null,
      pronunciation: Number(parsed.pronunciation) || null,
      overall: overall,
      summary: parsed.summary || ''
    };
  }

  // —— 报告 ——
  function summarizeSections() {
    var L = state.answers.listening;
    var R = state.answers.reading;
    var P = state.answers.phrase;
    var T = state.answers.translate;
    var S = state.answers.speaking;
    var speakOveralls = S.filter(function (r) { return r.overall != null; }).map(function (r) { return Number(r.overall); });
    var speakAvg = speakOveralls.length
      ? speakOveralls.reduce(function (a, b) { return a + b; }, 0) / speakOveralls.length
      : null;
    var anyTranscript = S.some(function (r) { return (r.transcript || '').length > 5; });
    var speakConf = '低';
    if (speakOveralls.length && S.every(function (r) { return r.confidence !== '低' || r.skipped; })) speakConf = '中';
    if (speakOveralls.length === S.length && S.every(function (r) { return !r.failed; })) speakConf = '中';

    return {
      form: state.form.form,
      targetScore: state.guest
        ? (Number(state.guestProfile.targetScore) || 6.5)
        : (Number(qs('target_score')) || 6.5),
      listening: (function () {
        var coverages = L.map(function (x) { return Number(x.coverage) || 0; });
        var coveragePct = L.length
          ? Math.round((coverages.reduce(function (a, b) { return a + b; }, 0) / L.length) * 100)
          : 0;
        return {
          correct: L.filter(function (x) { return x.correct; }).length,
          total: L.length,
          answered: L.filter(function (x) { return x.user; }).length,
          coveragePct: coveragePct,
          timedOut: !!(state.meta.listening && state.meta.listening.timedOut)
        };
      })(),
      reading: {
        correct: R.filter(function (x) { return x.correct; }).length,
        total: R.length,
        answered: R.filter(function (x) { return x.answered; }).length,
        timedOut: !!(state.meta.reading && state.meta.reading.timedOut)
      },
      writing: {
        phraseCorrect: P.filter(function (x) { return x.correct; }).length,
        phraseTotal: P.length,
        phraseAnswered: P.filter(function (x) { return x.user; }).length,
        translateCorrect: T.filter(function (x) { return x.correct; }).length,
        translateTotal: T.length,
        translateAnswered: T.filter(function (x) { return x.user; }).length
      },
      speaking: {
        overall: speakAvg,
        confidence: speakConf,
        transcriptLen: anyTranscript ? 80 : 0,
        items: S
      }
    };
  }

  function buildAndShowReport() {
    stopTimer();
    state.sectionIndex = SECTIONS.length;
    var input = summarizeSections();
    state.report = window.PlacementScoring.buildReport(input);
    renderReport('<p class="hint">正在保存结果…</p>');
    sendTestComplete().then(function () {
      renderReport();
    }).catch(function () {
      renderReport();
    });
  }

  function renderReport(extraTop) {
    var r = state.report;
    if (!r) return;
    var b = r.bands;
    var t = r.tiers;
    var studentName = state.guest ? (state.guestProfile.name || '访客') : (qs('student_name') || '');
    var studentId = state.guest
      ? (state.guestProfile.contact ? ('联系 ' + state.guestProfile.contact) : '访客')
      : (qs('student_id') || '');
    var durationSec = Math.max(0, Math.round((Date.now() - (state.startedAt || Date.now())) / 1000));
    var mins = Math.floor(durationSec / 60);
    var secs = durationSec % 60;
    var saveNote = '';
    if (state.guest) {
      if (state.guestSavedId) {
        saveNote = '<p class="save-ok">已提交给老师（编号 #' + escapeHtml(String(state.guestSavedId)) + '）</p>';
      } else if (state.guestSaveError) {
        saveNote = '<p class="save-err">提交失败：' + escapeHtml(state.guestSaveError) + '。请截图报告发给老师。</p>';
      }
    }

    function row(label, band, tier) {
      return (
        '<tr>' +
          '<td>' + escapeHtml(label) + '</td>' +
          '<td><strong>' + escapeHtml(band.label) + '</strong></td>' +
          '<td>' + escapeHtml(band.confidence || '—') + '</td>' +
          '<td class="left">' + escapeHtml(band.comment || '') + '</td>' +
          '<td>' + escapeHtml(tier.label) + '</td>' +
        '</tr>'
      );
    }

    var app = document.getElementById('app');
    app.innerHTML =
      '<div class="report">' +
        '<h1>入学能力摸底报告</h1>' +
        (extraTop || '') +
        saveNote +
        '<p class="sub">' +
          escapeHtml(studentName || '学生') +
          (studentId ? ' · ' + escapeHtml(studentId) : '') +
          ' · 目标分 ' + escapeHtml(String(r.targetScore)) +
          ' · 套别 ' + escapeHtml(r.form) +
          ' · 用时 ' + mins + ' 分 ' + secs + ' 秒' +
        '</p>' +
        '<div class="overall-card">' +
          '<div class="overall-label">综合预估</div>' +
          '<div class="overall-band">' + escapeHtml(r.overall.label) + '</div>' +
          '<p>' + escapeHtml(r.summary) + '</p>' +
        '</div>' +
        '<table class="report-table">' +
          '<thead><tr><th>科目</th><th>预估区间</th><th>置信度</th><th>短评</th><th>分档</th></tr></thead>' +
          '<tbody>' +
            row('听力', b.listening, t.listening) +
            row('阅读', b.reading, t.reading) +
            row('写作', b.writing, t.writing) +
            row('口语', b.speaking, t.speaking) +
          '</tbody>' +
        '</table>' +
        '<div class="plan-box">' +
          '<h3>排课方向</h3>' +
          '<p>' + escapeHtml(r.planHint) + '</p>' +
          '<ul>' +
            '<li>听力 · ' + escapeHtml(t.listening.label) + '：' + escapeHtml(t.listening.advice) + '</li>' +
            '<li>阅读 · ' + escapeHtml(t.reading.label) + '：' + escapeHtml(t.reading.advice) + '</li>' +
            '<li>写作 · ' + escapeHtml(t.writing.label) + '：' + escapeHtml(t.writing.advice) + '</li>' +
            '<li>口语 · ' + escapeHtml(t.speaking.label) + '：' + escapeHtml(t.speaking.advice) + '</li>' +
          '</ul>' +
        '</div>' +
        '<p class="disclaimer">本报告为入学摸底预估，不是官方成绩，不能保证提分结果。写作、口语题量有限，以区间和分档为准；入学后 3–5 天学习与阶段测会用于校准。</p>' +
        '<button class="btn primary block" id="doneBtn">' +
          (state.guest ? '完成' : '完成并返回') +
        '</button>' +
      '</div>';

    var doneBtn = document.getElementById('doneBtn');
    if (doneBtn) {
      doneBtn.onclick = function () {
        sendTestComplete();
        if (window.parent && window.parent !== window) {
          window.parent.postMessage({ type: 'requestCloseModule' }, '*');
        }
      };
    }
  }

  function buildReportDetails() {
    var r = state.report;
    return {
      form: r.form,
      bands: r.bands,
      tiers: r.tiers,
      overall: r.overall,
      summary: r.summary,
      planHint: r.planHint,
      guest: state.guest ? state.guestProfile : null,
      sections: {
        listening: state.answers.listening,
        reading: state.answers.reading.map(function (x) {
          return { id: x.id, correct: x.correct, answered: x.answered, coverage: x.coverage };
        }),
        phrase: state.answers.phrase.map(function (x) {
          return { id: x.id, correct: x.correct };
        }),
        translate: state.answers.translate.map(function (x) {
          return { id: x.id, correct: x.correct };
        }),
        speaking: state.answers.speaking
      }
    };
  }

  async function submitGuestResult() {
    var r = state.report;
    var durationSeconds = Math.max(0, Math.round((Date.now() - (state.startedAt || Date.now())) / 1000));
    var res = await fetch('/api/placement/guest-submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        guest_name: state.guestProfile.name,
        contact: state.guestProfile.contact,
        target_score: state.guestProfile.targetScore,
        form: r.form,
        overall_label: r.overall && r.overall.label,
        score_percent: r.scorePercent,
        duration_seconds: durationSeconds,
        summary: r.summary,
        report: buildReportDetails()
      })
    });
    var data = await res.json().catch(function () { return {}; });
    if (!res.ok || (data && data.error)) {
      var msg = (data && data.error && data.error.message) || ('HTTP ' + res.status);
      throw new Error(msg);
    }
    state.guestSavedId = data.data && data.data.id;
    return data.data;
  }

  function sendTestComplete() {
    if (!state.report) return Promise.resolve();
    if (state.reportSent && !state.guest) return Promise.resolve();
    if (state.guest && state.guestSavedId) return Promise.resolve();

    var r = state.report;
    var durationSeconds = Math.max(0, Math.round((Date.now() - (state.startedAt || Date.now())) / 1000));

    if (state.guest) {
      return submitGuestResult().then(function () {
        state.reportSent = true;
        state.guestSaveError = '';
      }).catch(function (err) {
        state.guestSaveError = String(err.message || err);
        console.warn('guest submit failed', err);
      });
    }

    state.reportSent = true;
    var L = state.answers.listening || [];
    var R = state.answers.reading || [];
    var P = state.answers.phrase || [];
    var T = state.answers.translate || [];
    var correctCount =
      L.filter(function (x) { return x.correct; }).length +
      R.filter(function (x) { return x.correct; }).length +
      P.filter(function (x) { return x.correct; }).length +
      T.filter(function (x) { return x.correct; }).length;
    var totalCount = L.length + R.length + P.length + T.length;
    var payload = {
      type: 'genericTestComplete',
      completed: true,
      moduleType: qs('module_type') || 'placement',
      testType: 'placement',
      scorePercent: r.scorePercent,
      score: r.scorePercent,
      correctCount: correctCount,
      totalCount: totalCount,
      durationSeconds: durationSeconds,
      startedAt: new Date(state.startedAt || Date.now()).toISOString(),
      endedAt: new Date().toISOString(),
      passThreshold: 0,
      isPassed: true,
      details: buildReportDetails()
    };
    try {
      if (window.parent && window.parent !== window) {
        window.parent.postMessage(payload, '*');
      }
    } catch (e) {
      console.warn('postMessage failed', e);
    }
    return Promise.resolve();
  }

  window.addEventListener('message', function (event) {
    if (event.data && event.data.type === 'requestSave') sendTestComplete();
  });

  function init() {
    if (!window.PLACEMENT_FORM_A) {
      document.getElementById('app').innerHTML = '<p class="error">题库加载失败</p>';
      return;
    }
    state.debug = qs('debug') === '1';
    state.guest = isGuestMode();
    state.form = sliceForm(window.PLACEMENT_FORM_A);
    renderIntro();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

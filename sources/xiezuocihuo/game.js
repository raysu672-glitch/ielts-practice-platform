/* ── 规范化字符串：去除空格和标点符号 ── */
function normalize(str) {
  return str.toLowerCase().replace(/[\s\.,!?;:'"()\-]/g, '');
}

/* ── 基础词伙（原始数据）── */
const foundationVocab = [
  { zh: "一系列的问题", en: "a barrage of problems" },
  { zh: "一个产生影响的因素", en: "a contributing factor" },
  { zh: "关注的焦点", en: "a focus of attention" },
  { zh: "越来越多的证据", en: "a growing body of evidence" },
  { zh: "一件备受关注的事", en: "a matter of heightened concern" },
  { zh: "一个更可行的方法", en: "a more feasible approach" },
  { zh: "满足感", en: "a sense of fulfillment" },
  { zh: "一个非常短视的观点", en: "a very shortsighted view" },
  { zh: "重要的组成部分", en: "a vital component" },
  { zh: "大量的信息", en: "a wealth of information" },
  { zh: "一个众所周知的事实", en: "a well-known fact" },
  { zh: "各种各样的选择", en: "a wide range of options" },
  { zh: "大量的证据", en: "ample evidence" },
  { zh: "主要的原因", en: "primary cause" },
  { zh: "一个问题的症结", en: "the crux of a problem" },
  { zh: "迫在眉睫的危机", en: "the looming crisis" },
  { zh: "最主要的障碍", en: "the major barrier" },
  { zh: "自我满足感", en: "a sense of self-fulfillment" },
  { zh: "令人信服的证据", en: "compelling evidence" },
  { zh: "令人信服的理由", en: "compelling reasons" }
];

/* ── 语义连线模板（基础词伙）── */
const synthesisTemplates = {
  'a barrage of problems': {
    plain: 'There are <span class="syn-blank">_______</span> in this area.',
    upgraded: 'There are <span class="syn-phrase-used">a barrage of problems</span> in this area.'
  },
  'a contributing factor': {
    plain: 'This serves as <span class="syn-blank">_______</span> to the broader issue.',
    upgraded: 'This serves as <span class="syn-phrase-used">a contributing factor</span> to the broader issue.'
  },
  'a focus of attention': {
    plain: 'This has become <span class="syn-blank">_______</span> for policymakers.',
    upgraded: 'This has become <span class="syn-phrase-used">a focus of attention</span> for policymakers.'
  },
  'a growing body of evidence': {
    plain: '<span class="syn-blank">_______</span> suggests this phenomenon is widespread.',
    upgraded: '<span class="syn-phrase-used">A growing body of evidence</span> suggests this phenomenon is widespread.'
  },
  'a matter of heightened concern': {
    plain: 'This has become <span class="syn-blank">_______</span> in modern society.',
    upgraded: 'This has become <span class="syn-phrase-used">a matter of heightened concern</span> in modern society.'
  },
  'a more feasible approach': {
    plain: 'Policymakers should adopt <span class="syn-blank">_______</span> to address it.',
    upgraded: 'Policymakers should adopt <span class="syn-phrase-used">a more feasible approach</span> to address it.'
  },
  'a sense of fulfillment': {
    plain: 'Volunteer work can provide <span class="syn-blank">_______</span> for participants.',
    upgraded: 'Volunteer work can provide <span class="syn-phrase-used">a sense of fulfillment</span> for participants.'
  },
  'a very shortsighted view': {
    plain: 'This represents <span class="syn-blank">_______</span> of long-term development.',
    upgraded: 'This represents <span class="syn-phrase-used">a very shortsighted view</span> of long-term development.'
  },
  'a vital component': {
    plain: 'Education is <span class="syn-blank">_______</span> of any effective solution.',
    upgraded: 'Education is <span class="syn-phrase-used">a vital component</span> of any effective solution.'
  },
  'a wealth of information': {
    plain: 'The internet provides <span class="syn-blank">_______</span> at our fingertips.',
    upgraded: 'The internet provides <span class="syn-phrase-used">a wealth of information</span> at our fingertips.'
  },
  'a well-known fact': {
    plain: 'It is <span class="syn-blank">_______</span> that smoking causes serious health issues.',
    upgraded: 'It is <span class="syn-phrase-used">a well-known fact</span> that smoking causes serious health issues.'
  },
  'a wide range of options': {
    plain: 'Consumers now have <span class="syn-blank">_______</span> in the marketplace.',
    upgraded: 'Consumers now have <span class="syn-phrase-used">a wide range of options</span> in the marketplace.'
  },
  'ample evidence': {
    plain: 'There is <span class="syn-blank">_______</span> that regular exercise improves mental health.',
    upgraded: 'There is <span class="syn-phrase-used">ample evidence</span> that regular exercise improves mental health.'
  },
  'primary cause': {
    plain: 'Unemployment remains <span class="syn-blank">_______</span> of social unrest in the region.',
    upgraded: 'Unemployment remains <span class="syn-phrase-used">primary cause</span> of social unrest in the region.'
  },
  'the crux of a problem': {
    plain: '<span class="syn-blank">_______</span> often lies in miscommunication between groups.',
    upgraded: '<span class="syn-phrase-used">The crux of a problem</span> often lies in miscommunication between groups.'
  },
  'the looming crisis': {
    plain: 'Climate change represents <span class="syn-blank">_______</span> of our generation.',
    upgraded: 'Climate change represents <span class="syn-phrase-used">the looming crisis</span> of our generation.'
  },
  'the major barrier': {
    plain: 'Funding shortages remain <span class="syn-blank">_______</span> to innovation.',
    upgraded: 'Funding shortages remain <span class="syn-phrase-used">the major barrier</span> to innovation.'
  },
  'a sense of self-fulfillment': {
    plain: 'Career advancement often brings <span class="syn-blank">_______</span>.',
    upgraded: 'Career advancement often brings <span class="syn-phrase-used">a sense of self-fulfillment</span>.'
  },
  'compelling evidence': {
    plain: 'There is <span class="syn-blank">_______</span> that early intervention is highly effective.',
    upgraded: 'There is <span class="syn-phrase-used">compelling evidence</span> that early intervention is highly effective.'
  },
  'compelling reasons': {
    plain: 'There are <span class="syn-blank">_______</span> to invest in renewable energy now.',
    upgraded: 'There are <span class="syn-phrase-used">compelling reasons</span> to invest in renewable energy now.'
  }
};

/* ══════════════════════════════════════════════════
   分类选择页面逻辑
══════════════════════════════════════════════════ */
var currentCategoryId = null;
var vocab = [];  // 当前分类词伙（动态设置）
var phraseStartTime = 0; // 学习开始时间

function createTextElement(tagName, className, text) {
  var el = document.createElement(tagName);
  if (className) el.className = className;
  el.textContent = text;
  return el;
}

function appendSynthesisMarkup(target, markup) {
  var pattern = /<span class="(syn-blank|syn-phrase-used)">([^<]*)<\/span>/g;
  var lastIndex = 0;
  var match;
  while ((match = pattern.exec(markup)) !== null) {
    if (match.index > lastIndex) {
      target.appendChild(document.createTextNode(markup.slice(lastIndex, match.index)));
    }
    target.appendChild(createTextElement('span', match[1], match[2]));
    lastIndex = pattern.lastIndex;
  }
  if (lastIndex < markup.length) {
    target.appendChild(document.createTextNode(markup.slice(lastIndex)));
  }
}

function buildCategoryPage() {
  var gridXiao = document.getElementById('gridXiaoZuoWen');
  var gridDa   = document.getElementById('gridDaZuoWen');

  allCategories.forEach(function(cat, idx) {
    var card = document.createElement('button');
    card.className = 'cat-card';
    card.style.animationDelay = (0.05 * idx) + 's';
    card.appendChild(createTextElement('div', 'cat-card-icon', cat.icon));
    card.appendChild(createTextElement('div', 'cat-card-name', cat.name));
    card.appendChild(createTextElement('div', 'cat-card-count', cat.vocab.length + ' 条词伙'));
    card.appendChild(createTextElement('div', 'cat-card-arrow', '开始练习 '));
    card.onclick = function() { selectCategory(cat.id); };

    if (cat.group === '小作文') {
      gridXiao.appendChild(card);
    } else {
      gridDa.appendChild(card);
    }
  });
}

function selectCategory(catId) {
  var catName, catVocab;

  if (catId === '__foundation__') {
    catName  = '⭐ 基础必背词伙';
    catVocab = foundationVocab;
  } else {
    var cat = allCategories.find(function(c) { return c.id === catId; });
    if (!cat) return;
    catName  = cat.icon + ' ' + cat.name;
    catVocab = cat.vocab;
  }

  currentCategoryId = catId;
  vocab = catVocab.slice();   // 副本，shuffle不影响原数组
  phraseStartTime = Date.now(); // 记录学习开始时间

  // 更新 header 徽章
  document.getElementById('headerCatBadge').textContent = catName;

  // 更新学习页标题
  document.getElementById('studyTitle').textContent = ' 课前学习 — ' + catName;
  document.getElementById('studySubtitle').textContent =
    '学习每个词伙的正确拼写，共 ' + vocab.length + ' 个词伙';

  // 隐藏分类页，显示学习页
  document.getElementById('categoryPage').style.display = 'none';
  document.getElementById('studyOverlay').style.display = 'flex';

  // 重置学习状态
  resetStudyState();
  populateStudyPage();
  showStudyCard(studyIndex);
}

function reportPhraseStudy(minSeconds) {
  if (phraseStartTime > 0 && window.parent !== window) {
    var elapsed = Math.floor((Date.now() - phraseStartTime) / 1000);
    if (elapsed >= (minSeconds || 0)) {
      window.parent.postMessage({
        type: 'phraseStudyComplete',
        moduleType: 'writing_phrase',
        categoryId: currentCategoryId,
        durationSeconds: elapsed,
        totalCorrect: totalCorrect,
        totalWords: vocab.length
      }, '*');
      phraseStartTime = 0;
      return true;
    }
  }
  return false;
}

function backToCategory() {
  // 发送学习时长给父页面（中途退出也记录）
  reportPhraseStudy(5);
  
  // 停止 Fever 计时器
  if (feverTimer) clearInterval(feverTimer);
  feverMode  = false;
  document.body.classList.remove('fever');

  // 隐藏游戏，显示分类页
  document.getElementById('gameContent').style.display = 'none';
  document.getElementById('studyOverlay').style.display = 'none';
  document.getElementById('categoryPage').style.display = 'flex';

  // 移除 finish overlay（如有）
  var fo = document.querySelector('.finish-overlay');
  if (fo) fo.remove();
}

/* ══════════════════════════════════════════════════
   语义连线（动态：优先用模板，无模板则生成通用句）
══════════════════════════════════════════════════ */
var recentPhrases = [];
var synthesisFired = false;

/* ══════════════════════════════════════════════════
   游戏状态
══════════════════════════════════════════════════ */
var currentIndex = 0;
var energy = 0;
var combo = 0;
var maxCombo = 0;
var totalAnswered = 0;
var totalCorrect = 0;
var selectedWords = [];
var isProcessing = false;
var fogMode = false;
var feverMode = false;
var feverTimer = null;
var feverTimeLeft = 0;
var audioCtx = null;
var clearedFogWords = new Set();
var questionFailed = false;

var studyTimer = null;
var studyTimeLeft = 300;

/* ── 学习页状态 ── */
var studyIndex = 0;
var studyRound = 1;
var studySkipped = new Set();

function resetStudyState() {
  studyIndex   = 0;
  studyRound   = 1;
  studySkipped = new Set();
  document.getElementById('studySkipBtn').style.display = '';
  document.getElementById('studyFinishBtn').style.display = 'none';
  document.getElementById('studyCard').classList.remove('active');
  document.getElementById('studyFeedback').textContent = '';
  document.getElementById('studyInput').value = '';
}

function resetGameState() {
  currentIndex   = 0;
  energy         = 0;
  combo          = 0;
  maxCombo       = 0;
  totalAnswered  = 0;
  totalCorrect   = 0;
  selectedWords  = [];
  isProcessing   = false;
  fogMode        = false;
  recentPhrases  = [];
  synthesisFired = false;
  clearedFogWords = new Set();
  questionFailed  = false;

  // 清除 Fever 残留
  if (feverTimer) clearInterval(feverTimer);
  feverTimer  = null;
  feverMode   = false;
  feverTimeLeft = 0;
  document.body.classList.remove('fever');

  var oldTimer = document.getElementById('feverTimerDisplay');
  if (oldTimer) oldTimer.remove();

  document.getElementById('feverInput').value = '';
  document.getElementById('feverProgress').textContent = '';
  document.getElementById('questionHint').textContent = ' 点击英文单词组成答案 ';
  document.getElementById('questionHint').style.color = '';

  updateEnergyBar();
  updateStats();
}

/* ══════════════════════════════════════════════════
   学习页面
══════════════════════════════════════════════════ */
function populateStudyPage() {
  var grid = document.getElementById('studyGrid');
  grid.replaceChildren();
  vocab.forEach(function(item, idx) {
    var card = document.createElement('div');
    card.className = 'study-card';
    card.id = 'studyCard_' + idx;
    card.appendChild(createTextElement('div', 'study-card-zh', item.zh));
    card.appendChild(createTextElement('div', 'study-card-en', item.en));
    card.onclick = function() { jumpToStudyItem(idx); };
    grid.appendChild(card);
  });
}

function jumpToStudyItem(idx) {
  studyIndex = idx;
  studyRound = 1;
  studySkipped.delete(idx);
  showStudyCard(idx);
}

function showStudyCard(idx) {
  if (idx >= vocab.length) {
    finishStudy();
    return;
  }
  var item = vocab[idx];
  document.getElementById('studyProgress').textContent = (studyIndex + 1) + ' / ' + vocab.length;

  var card = document.getElementById('studyCard');
  card.classList.add('active');

  document.getElementById('studyLearnZh').textContent = item.zh;
  document.getElementById('studyLearnEnRef').textContent = item.en;

  var roundLabel = document.getElementById('studyRoundLabel');
  roundLabel.textContent = '第 ' + studyRound + ' 遍（共需2遍）';
  roundLabel.className = 'study-learn-round' + (studyRound === 2 ? ' round2' : '');

  document.getElementById('studyHint').textContent = '';
  document.getElementById('studyFeedback').textContent = '';
  document.getElementById('studyFeedback').style.color = '';

  var input = document.getElementById('studyInput');
  input.value = '';
  input.className = 'study-learn-input';
  input.placeholder = '输入英文词伙（第 ' + studyRound + ' 遍）...';
  input.focus();
}

document.getElementById('studyInput').onkeydown = function(e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    submitStudyInput();
  }
};

function submitStudyInput() {
  var val      = document.getElementById('studyInput').value.trim().toLowerCase();
  var item     = vocab[studyIndex];
  var input    = document.getElementById('studyInput');
  var hint     = document.getElementById('studyHint');
  var feedback = document.getElementById('studyFeedback');

  if (normalize(val) === normalize(item.en)) {
    input.classList.add('correct');
    feedback.style.color = '#3fb950';
    if (studyRound === 1) {
      feedback.textContent = ' 第一遍正确！请再输入第二遍加深印象。';
      hint.textContent = '';
      studyRound = 2;
      var roundLabel = document.getElementById('studyRoundLabel');
      roundLabel.textContent = '第 2 遍（共需2遍）';
      roundLabel.className = 'study-learn-round round2';
      input.value = '';
      input.className = 'study-learn-input';
      input.placeholder = '再输入一遍（闭眼或回忆）...';
      setTimeout(function() { input.focus(); }, 100);
    } else {
      feedback.textContent = ' 两遍全部正确！';
      var sc = document.getElementById('studyCard_' + studyIndex);
      if (sc) { sc.classList.add('study-card-done'); }
      setTimeout(function() {
        studyIndex++;
        studyRound = 1;
        showStudyCard(studyIndex);
      }, 800);
    }
  } else {
    input.classList.add('wrong');
    hint.textContent = ' 再试一次，参考英文：' + item.en;
    hint.style.color = '#f85149';
    feedback.textContent = '';
    setTimeout(function() {
      input.classList.remove('wrong');
      input.value = '';
      input.focus();
    }, 600);
  }
}

document.getElementById('studySkipBtn').onclick = function() {
  studySkipped.add(studyIndex);
  var sc = document.getElementById('studyCard_' + studyIndex);
  if (sc) {
    sc.style.opacity = '0.35';
    sc.style.borderColor = '#f85149';
  }
  studyIndex++;
  studyRound = 1;
  showStudyCard(studyIndex);
};

function finishStudy() {
  document.getElementById('studyCard').classList.remove('active');
  document.getElementById('studyProgress').textContent = ' 全部学习完毕';
  document.getElementById('studyFeedback').textContent = '';
  document.getElementById('studySkipBtn').style.display = 'none';
  var finishBtn = document.getElementById('studyFinishBtn');
  finishBtn.style.display = '';
  finishBtn.onclick = startGame;
}

function startGame() {
  document.getElementById('studyOverlay').style.display = 'none';
  document.getElementById('gameContent').style.display = '';
  resetGameState();
  createBgParticles();
  shuffleVocab();
  loadQuestion();
  initAudio();
}

function shuffleVocab() {
  for (var i = vocab.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = vocab[i]; vocab[i] = vocab[j]; vocab[j] = tmp;
  }
}

/* ── Web Audio ── */
function initAudio() {
  try {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  } catch(e) { audioCtx = null; }
}
function playKeySound() {
  if (!audioCtx) return;
  try {
    var osc = audioCtx.createOscillator();
    var gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = 'square';
    osc.frequency.setValueAtTime(2800 + Math.random()*1200, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.04);
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);
    osc.start(audioCtx.currentTime); osc.stop(audioCtx.currentTime + 0.05);
  } catch(e) {}
}
function playCorrectSound() {
  if (!audioCtx) return;
  try {
    [523, 659, 784].forEach(function(freq, i) {
      var osc = audioCtx.createOscillator();
      var gain = audioCtx.createGain();
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.type = 'sine'; osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.1, audioCtx.currentTime + i*0.1);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + i*0.1 + 0.2);
      osc.start(audioCtx.currentTime + i*0.1); osc.stop(audioCtx.currentTime + i*0.1 + 0.25);
    });
  } catch(e) {}
}
function playWrongSound() {
  if (!audioCtx) return;
  try {
    var osc = audioCtx.createOscillator();
    var gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(200, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(80, audioCtx.currentTime + 0.2);
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.25);
    osc.start(audioCtx.currentTime); osc.stop(audioCtx.currentTime + 0.25);
  } catch(e) {}
}
function playFeverStartSound() {
  if (!audioCtx) return;
  try {
    [523, 659, 784, 1047].forEach(function(freq, i) {
      var osc = audioCtx.createOscillator();
      var gain = audioCtx.createGain();
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.type = 'sine'; osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.12, audioCtx.currentTime + i*0.08);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + i*0.08 + 0.15);
      osc.start(audioCtx.currentTime + i*0.08); osc.stop(audioCtx.currentTime + i*0.08 + 0.2);
    });
  } catch(e) {}
}
function playCorrectTick() {
  if (!audioCtx) return;
  try {
    var osc = audioCtx.createOscillator();
    var gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(880, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(1100, audioCtx.currentTime + 0.06);
    gain.gain.setValueAtTime(0.09, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
    osc.start(audioCtx.currentTime); osc.stop(audioCtx.currentTime + 0.12);
  } catch(e) {}
}

/* ── 迷雾模式 ── */
function generateFogWord(word) {
  if (word.length <= 2) return word;
  var arr = word.split('');
  var hideCount = Math.max(1, Math.floor(arr.length * (0.3 + Math.random()*0.2)));
  var indices = [];
  for (var i = 1; i < arr.length - 1; i++) indices.push(i);
  for (var i = indices.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = indices[i]; indices[i] = indices[j]; indices[j] = tmp;
  }
  var hideIdx = new Set(indices.slice(0, Math.min(hideCount, indices.length)));
  return arr.map(function(ch, i) { return hideIdx.has(i) ? '_' : ch; }).join('');
}

function showFogModal(word) {
  if (clearedFogWords.has(word)) {
    selectWordAfterFog(word);
    return;
  }
  var fogDisplay = generateFogWord(word);
  var overlay = document.createElement('div');
  overlay.className = 'fog-modal-overlay';
  overlay.id = 'fogModal';
  var modal = document.createElement('div');
  modal.className = 'fog-modal';
  modal.appendChild(createTextElement('h3', '', '迷雾模式 — 补全单词'));

  var display = document.createElement('div');
  display.className = 'fog-word-display';
  fogDisplay.split('').forEach(function(ch) {
    if (ch === '_') {
      var hiddenChar = document.createElement('span');
      hiddenChar.style.color = '#f85149';
      hiddenChar.textContent = '_';
      display.appendChild(hiddenChar);
    } else {
      display.appendChild(document.createTextNode(ch));
    }
  });
  modal.appendChild(display);

  var inputEl = document.createElement('input');
  inputEl.className = 'fog-input';
  inputEl.id = 'fogInput';
  inputEl.placeholder = '输入完整单词...';
  inputEl.autocomplete = 'off';
  inputEl.spellcheck = false;
  modal.appendChild(inputEl);

  var resultEl = document.createElement('div');
  resultEl.className = 'fog-result';
  resultEl.id = 'fogResult';
  modal.appendChild(resultEl);

  var buttonRow = document.createElement('div');
  buttonRow.className = 'fog-btns';
  var confirmButton = createTextElement('button', 'fog-btn fog-btn-confirm', '确认');
  confirmButton.id = 'fogConfirmBtn';
  var cancelButton = createTextElement('button', 'fog-btn fog-btn-cancel', '取消');
  cancelButton.id = 'fogCancelBtn';
  buttonRow.append(confirmButton, cancelButton);
  modal.appendChild(buttonRow);
  overlay.appendChild(modal);
  document.body.appendChild(overlay);

  var input = document.getElementById('fogInput');
  var result = document.getElementById('fogResult');
  input.focus();

  var fogCloseCalled = false;
  function close(success) {
    if (fogCloseCalled) return;
    fogCloseCalled = true;
    overlay.remove();
    if (success) {
      clearedFogWords.add(word);
      selectWordAfterFog(word);
    }
  }

  document.getElementById('fogConfirmBtn').onclick = function() {
    if (fogCloseCalled) return;
    if (normalize(input.value) === normalize(word)) {
      result.className = 'fog-result success';
      result.textContent = ' 正确！';
      setTimeout(function() { close(true); }, 400);
    } else {
      result.className = 'fog-result fail';
      result.textContent = ' 再试试';
      input.value = '';
      input.focus();
    }
  };
  document.getElementById('fogCancelBtn').onclick = function() { close(false); };
  input.onkeydown = function(e) {
    if (e.key === 'Enter') { e.preventDefault(); e.stopPropagation(); document.getElementById('fogConfirmBtn').click(); }
    if (e.key === 'Escape') { e.preventDefault(); close(false); }
    if (audioCtx && e.key.length === 1) playKeySound();
  };
}

function selectWordAfterFog(word) {
  if (!selectedWords.includes(word)) {
    selectedWords.push(word);
  }
  document.querySelectorAll('.word-btn').forEach(function(btn) {
    if (btn.dataset.word === word) {
      btn.classList.remove('fogged');
      btn.classList.add('fog-cleared');
      btn.classList.add('selected');
      btn.textContent = word;
      btn.onclick = function() { toggleWord(word, btn); };
    }
  });
  updateAnswerSlots();

  var slotsEl = document.getElementById('answerSlots');
  if (feverMode) {
    slotsEl.style.setProperty('display', 'flex', 'important');
    setTimeout(function() { slotsEl.style.removeProperty('display'); }, 1200);
  }
  slotsEl.style.boxShadow = '0 0 18px rgba(63,185,80,0.6)';
  setTimeout(function(){ slotsEl.style.boxShadow = ''; }, 800);
}

/* ── Fever Mode ── */
function enterFeverMode() {
  feverMode = true;
  document.body.classList.add('fever');
  playFeverStartSound();

  document.getElementById('questionHint').textContent = ' FEVER MODE — 直接打字输入！';
  document.getElementById('questionHint').style.color = '#ffd700';

  feverTimeLeft = 50;
  updateFeverTimer();
  feverTimer = setInterval(function() {
    feverTimeLeft--;
    updateFeverTimer();
    if (feverTimeLeft <= 0) {
      clearInterval(feverTimer);
      handleWrong(vocab[currentIndex].en);
      exitFeverMode();
    }
  }, 1000);

  setTimeout(function() { document.getElementById('feverInput').focus(); }, 300);
}

function exitFeverMode() {
  feverMode = false;
  clearInterval(feverTimer);
  document.body.classList.remove('fever');
  document.getElementById('feverInput').value = '';
  document.getElementById('questionHint').textContent = ' 点击英文单词组成答案 ';
  document.getElementById('questionHint').style.color = '';
}

function updateFeverTimer() {
  var timerEl = document.getElementById('feverTimerDisplay');
  if (!timerEl) {
    timerEl = document.createElement('div');
    timerEl.id = 'feverTimerDisplay';
    timerEl.className = 'fever-timer';
    document.getElementById('questionBox').appendChild(timerEl);
  }
  timerEl.textContent = feverTimeLeft;
  timerEl.classList.toggle('urgent', feverTimeLeft <= 4);
  document.getElementById('feverProgress').textContent = feverTimeLeft <= 4 ? '⏰ 快！' : '剩余 ' + feverTimeLeft + ' 秒';
}

/* ── 加载题目 ── */
function loadQuestion() {
  if (currentIndex >= vocab.length) {
    showFinish();
    return;
  }
  var oldTimer = document.getElementById('feverTimerDisplay');
  if (oldTimer) oldTimer.remove();

  var q = vocab[currentIndex];
  document.getElementById('questionNum').textContent = String(currentIndex+1).padStart(2,'0') + ' / ' + vocab.length;
  document.getElementById('questionChinese').textContent = q.zh;
  document.getElementById('progress').textContent = currentIndex + '/' + vocab.length;
  document.getElementById('feverInput').value = '';
  document.getElementById('feverProgress').textContent = '';

  clearedFogWords = new Set();
  questionFailed  = false;
  selectedWords   = [];
  buildWordPool(q);
  updateAnswerSlots();

  if (feverMode) {
    setTimeout(function() { document.getElementById('feverInput').focus(); }, 100);
    updateFeverTimer();
  }
}

/* ── 构建选词池 ── */
function buildWordPool(q) {
  var pool = document.getElementById('wordPool');
  pool.replaceChildren();

  var correctWords = q.en.split(' ');
  var allWords = correctWords.slice();

  var otherWords = [];
  vocab.forEach(function(v, i) {
    if (i !== currentIndex) {
      v.en.split(' ').forEach(function(w) { otherWords.push(w); });
    }
  });
  otherWords.sort(function() { return Math.random() - 0.5; });

  var targetCount = Math.max(correctWords.length + 4, 8);
  for (var i = 0; allWords.length < targetCount && i < otherWords.length; i++) {
    if (allWords.indexOf(otherWords[i]) === -1) {
      allWords.push(otherWords[i]);
    }
  }
  allWords.sort(function() { return Math.random() - 0.5; });

  allWords.forEach(function(word) {
    var btn = document.createElement('button');
    btn.className = 'word-btn';
    btn.dataset.word = word;

    if (fogMode && !clearedFogWords.has(word)) {
      btn.classList.add('fogged');
      var fogged = generateFogWord(word);
      btn.appendChild(createTextElement('span', 'fog-text', fogged));
      btn.onclick = function() {
        if (isProcessing) return;
        showFogModal(word);
      };
    } else {
      btn.textContent = word;
      btn.onclick = function() { toggleWord(word, btn); };
    }
    pool.appendChild(btn);
  });
}

function toggleWord(word, btn) {
  if (isProcessing) return;
  var idx = selectedWords.indexOf(word);
  if (idx >= 0) {
    selectedWords.splice(idx, 1);
    btn.classList.remove('selected');
  } else {
    selectedWords.push(word);
    btn.classList.add('selected');
  }
  updateAnswerSlots();
}

function updateAnswerSlots() {
  var slotsEl = document.getElementById('answerSlots');
  slotsEl.replaceChildren();
  if (selectedWords.length === 0) {
    var hint = document.createElement('span');
    hint.style.color = '#484f58';
    hint.style.fontSize = '15px';
    hint.textContent = feverMode ? '输入答案后按 Enter ' : '点击上方单词组成答案 ';
    slotsEl.appendChild(hint);
    return;
  }
  selectedWords.forEach(function(word) {
    var slot = document.createElement('div');
    slot.className = 'slot filled';
    slot.textContent = word;
    slotsEl.appendChild(slot);
  });
}

function clearSelection() {
  if (isProcessing) return;
  selectedWords = [];
  document.querySelectorAll('.word-btn').forEach(function(b) { b.classList.remove('selected'); });
  updateAnswerSlots();
}

function removeLastWord() {
  if (isProcessing || selectedWords.length === 0) return;
  var word = selectedWords.pop();
  var btns = [];
  document.querySelectorAll('.word-btn.selected').forEach(function(b) { btns.push(b); });
  for (var i = btns.length - 1; i >= 0; i--) {
    if (btns[i].textContent === word) {
      btns[i].classList.remove('selected');
      break;
    }
  }
  updateAnswerSlots();
}

function checkAnswer() {
  if (isProcessing) return;
  isProcessing = true;

  var q = vocab[currentIndex];
  if (feverMode) {
    var userAnswer = document.getElementById('feverInput').value.trim().replace(/\s+/g, ' ');
    if (normalize(userAnswer) === normalize(q.en)) {
      handleCorrect();
    } else {
      handleWrong(q.en);
    }
  } else {
    if (selectedWords.length === 0) { isProcessing = false; return; }
    var userSorted = selectedWords.map(function(w) { return normalize(w); }).sort().join(' ');
    var ansSorted  = q.en.split(' ').map(function(w) { return normalize(w); }).sort().join(' ');
    if (userSorted === ansSorted) {
      handleCorrect();
    } else {
      handleWrong(q.en);
    }
  }
}

/* ── 答对 ── */
function handleCorrect() {
  combo++;
  totalCorrect++;
  totalAnswered++;
  if (combo > maxCombo) maxCombo = combo;

  var justAnswered = vocab[currentIndex];
  if (justAnswered) {
    recentPhrases.push({ zh: justAnswered.zh, en: justAnswered.en });
    if (recentPhrases.length > 3) recentPhrases.shift();
  }

  if (!questionFailed) {
    var gain = Math.min(20 + (combo - 1) * 5, 35);
    energy = Math.min(energy + gain, 100);
  }
  updateEnergyBar();
  updateStats();
  playCorrectSound();
  questionFailed = false;

  if (feverMode) {
    showFeverCorrectEffect();
    spawnFeverParticles();
    feverTimeLeft = Math.min(feverTimeLeft + 5, 50);
    updateFeverTimer();
  } else {
    showCorrectEffect();
    spawnParticles();
    if (combo >= 3) {
      spawnFireworks();
      flashScreen('#3fb950');
    }
  }

  var delay = feverMode ? 600 : (combo >= 3 ? 1200 : 800);
  setTimeout(function() {
    currentIndex++;
    isProcessing = false;
    if (!feverMode && (energy >= 100 || combo >= 5)) {
      enterFeverMode();
    }
    if (recentPhrases.length === 3 && !synthesisFired) {
      synthesisFired = true;
      var phrasesToShow = recentPhrases.slice();
      recentPhrases = [];
      showSynthesisModal(phrasesToShow);
      return;
    }
    loadQuestion();
  }, delay);
}

/* ── 答错 ── */
function showWrongEffect(correctAnswer, callback) {
  var box = document.getElementById('questionBox');
  box.classList.add('shake');
  var hint = document.createElement('div');
  hint.id = 'wrongHint';
  hint.style.cssText = 'margin-top:16px;font-size:20px;color:#f85149;animation:fadeIn 0.3s;';
  hint.appendChild(document.createTextNode(' 正确答案：'));
  var answer = document.createElement('span');
  answer.style.color = '#3fb950';
  answer.style.fontSize = '22px';
  answer.textContent = correctAnswer;
  hint.appendChild(answer);
  box.appendChild(hint);
  document.querySelectorAll('.word-btn.selected').forEach(function(btn) {
    btn.classList.add('wrong-flash');
  });
  flashScreen('#f85149');
  setTimeout(function() {
    box.classList.remove('shake');
    var oldHint = document.getElementById('wrongHint');
    if (oldHint) oldHint.remove();
    document.querySelectorAll('.word-btn.wrong-flash').forEach(function(b) { b.classList.remove('wrong-flash'); });
    if (callback) callback();
  }, 3000);
}

function handleWrong(correctAnswer) {
  combo = 0;
  totalAnswered++;
  energy = Math.max(energy - 20, 0);
  questionFailed = true;
  updateEnergyBar();
  updateStats();
  playWrongSound();

  if (feverMode) {
    energy = Math.max(energy - 30, 0);
    updateEnergyBar();
    flashScreen('#f85149');
    exitFeverMode();
    showWrongEffect(correctAnswer, function() {
      currentIndex++;
      isProcessing = false;
      loadQuestion();
    });
    return;
  }

  shakeScreen();
  showWrongEffect(correctAnswer, function() {
    selectedWords = [];
    document.querySelectorAll('.word-btn').forEach(function(b) { b.classList.remove('selected'); });
    updateAnswerSlots();
    isProcessing = false;
  });
}

/* ── 特效 ── */
function showCorrectEffect() {
  var overlay = document.createElement('div');
  overlay.className = 'correct-overlay';
  var msgs = ['正确!', '太棒了!', '完美!', '厉害!', 'Nice!'];
  var text = document.createElement('div');
  text.className = 'correct-text';
  if (combo >= 2) text.classList.add('combo-' + Math.min(combo, 5));
  text.textContent = msgs[Math.floor(Math.random() * msgs.length)];
  overlay.appendChild(text);
  document.body.appendChild(overlay);
  setTimeout(function() { overlay.remove(); }, 900);
}

function showFeverCorrectEffect() {
  var overlay = document.createElement('div');
  overlay.className = 'fever-correct-overlay';
  var text = document.createElement('div');
  text.className = 'fever-correct-text';
  var msgs = ['PERFECT!', 'AMAZING!', 'BRILLIANT!', 'YES!'];
  text.textContent = msgs[Math.floor(Math.random() * msgs.length)];
  overlay.appendChild(text);
  document.body.appendChild(overlay);
  setTimeout(function() { overlay.remove(); }, 700);
  document.getElementById('centerPanel').classList.add('fever-shake');
  setTimeout(function() { document.getElementById('centerPanel').classList.remove('fever-shake'); }, 500);
}

function spawnParticles() {
  var colors = ['#3fb950', '#58a6ff', '#bc8cff', '#f778ba', '#ffd700'];
  for (var i = 0; i < 18; i++) {
    var p = document.createElement('div');
    p.className = 'particle';
    p.style.background = colors[Math.floor(Math.random() * colors.length)];
    p.style.left = (window.innerWidth / 2 + (Math.random() - 0.5) * 200) + 'px';
    p.style.top  = (window.innerHeight / 2) + 'px';
    p.style.setProperty('--tx', (Math.random() - 0.5) * 400 + 'px');
    p.style.setProperty('--ty', (Math.random() - 1) * 300 + 'px');
    document.body.appendChild(p);
    setTimeout(function() { p.remove(); }, 1000);
  }
}

function spawnFeverParticles() {
  var colors = ['#ffd700', '#ff6b35', '#ff0080', '#00c8ff', '#bc8cff'];
  for (var i = 0; i < 12; i++) {
    var p = document.createElement('div');
    p.className = 'fever-particle';
    p.style.color = colors[Math.floor(Math.random() * colors.length)];
    p.style.left  = (window.innerWidth / 2 + (Math.random() - 0.5) * 300) + 'px';
    p.style.top   = (window.innerHeight / 2) + 'px';
    p.style.setProperty('--tx', (Math.random() - 0.5) * 300 + 'px');
    p.style.setProperty('--ty', (Math.random() - 1) * 250 + 'px');
    p.textContent = ['', '', '', '', ''][Math.floor(Math.random()*5)];
    document.body.appendChild(p);
    setTimeout(function() { p.remove(); }, 700);
  }
}

function spawnFeverKeyParticle() {
  var input = document.getElementById('feverInput');
  var rect  = input.getBoundingClientRect();
  var p = document.createElement('div');
  p.className = 'fever-particle';
  p.style.color = ['#ffd700','#ff6b35','#00c8ff'][Math.floor(Math.random()*3)];
  p.style.left  = (rect.left + Math.random()*rect.width) + 'px';
  p.style.top   = (rect.top - 10) + 'px';
  p.style.setProperty('--tx', (Math.random()-0.5)*80+'px');
  p.style.setProperty('--ty', (-20 - Math.random()*40)+'px');
  p.textContent = ['·','','•'][Math.floor(Math.random()*3)];
  document.body.appendChild(p);
  setTimeout(function(){ p.remove(); }, 700);
}

function spawnFireworks() {
  var colors = ['#ffd700', '#ff6b35', '#bc8cff', '#3fb950', '#58a6ff'];
  var cx = window.innerWidth / 2;
  var cy = window.innerHeight / 2;
  for (var i = 0; i < 30; i++) {
    (function(i) {
      var fw = document.createElement('div');
      fw.className = 'firework';
      fw.style.background = colors[Math.floor(Math.random() * colors.length)];
      fw.style.left = cx + 'px';
      fw.style.top  = cy + 'px';
      var angle = (Math.PI * 2 / 30) * i;
      var dist  = 100 + Math.random() * 200;
      fw.style.transition = 'all 0.8s ease-out';
      document.body.appendChild(fw);
      requestAnimationFrame(function() {
        fw.style.transform = 'translate(' + Math.cos(angle)*dist + 'px, ' + Math.sin(angle)*dist + 'px)';
        fw.style.opacity = '0';
      });
      setTimeout(function() { fw.remove(); }, 900);
    })(i);
  }
}

function flashScreen(color) {
  var cls   = feverMode ? 'fever-flash' : 'flash-overlay';
  var flash = document.createElement('div');
  flash.className  = cls;
  flash.style.background = color;
  document.body.appendChild(flash);
  setTimeout(function() { flash.remove(); }, feverMode ? 300 : 600);
}

function shakeScreen() {
  document.getElementById('centerPanel').classList.add('shake');
  setTimeout(function() { document.getElementById('centerPanel').classList.remove('shake'); }, 500);
}

/* ── 更新能量槽 ── */
function updateEnergyBar() {
  var bar    = document.getElementById('energyBar');
  var val    = document.getElementById('energyValue');
  var emojis = document.getElementById('energyEmojis');
  var comboEl = document.getElementById('comboValue');

  bar.style.height = energy + '%';
  val.textContent  = energy;

  bar.classList.remove('mid', 'high', 'max');
  if (energy >= 80) bar.classList.add('max');
  else if (energy >= 50) bar.classList.add('high');
  else if (energy >= 25) bar.classList.add('mid');

  if (energy >= 50 && !fogMode) {
    fogMode = true;
    var hint = document.getElementById('questionHint');
    if (hint && !feverMode) {
      hint.textContent = ' 迷雾模式激活！点击残缺单词补全字母';
      hint.style.color = '#58a6ff';
      setTimeout(function() {
        if (!feverMode) {
          hint.textContent = ' 点击英文单词组成答案 ';
          hint.style.color = '';
        }
      }, 3000);
    }
    var q = vocab[currentIndex];
    if (q) buildWordPool(q);
  }

  if (feverMode) {
    emojis.textContent = '';
  } else if (energy >= 80) {
    emojis.textContent = '';
  } else if (energy >= 50) {
    emojis.textContent = '';
  } else if (energy >= 25) {
    emojis.textContent = '';
  } else {
    emojis.textContent = '';
  }

  comboEl.textContent = 'x' + combo;
  comboEl.classList.remove('hot');
  if (combo >= 3) comboEl.classList.add('hot');
}

function updateStats() {
  document.getElementById('correctCount').textContent = totalCorrect;
  var acc = totalAnswered > 0 ? Math.round(totalCorrect / totalAnswered * 100) : 0;
  document.getElementById('accuracy').textContent = acc + '%';
}

/* ── 完成画面 ── */
function showFinish() {
  exitFeverMode();
  
  // 发送学习时长给父页面（iframe 通信）
  reportPhraseStudy(0);
  
  var overlay = document.createElement('div');
  overlay.className = 'finish-overlay';
  var pct = Math.round(totalCorrect / vocab.length * 100);
  var msg;
  if (totalCorrect === vocab.length) msg = ' 完美通关！你是词伙大师！';
  else if (totalCorrect >= vocab.length * 0.8) msg = ' 很棒！继续加油！';
  else msg = ' 多多练习，下次更好！';

  overlay.appendChild(createTextElement('h2', '', '全部完成！'));
  overlay.appendChild(createTextElement('p', '', '答对：' + totalCorrect + ' / ' + vocab.length));
  overlay.appendChild(createTextElement('p', '', '正确率：' + pct + '%'));
  overlay.appendChild(createTextElement('p', '', '最大连击：x' + maxCombo));

  var message = createTextElement('p', '', msg);
  message.style.marginTop = '20px';
  message.style.fontSize = '16px';
  message.style.color = '#58a6ff';
  overlay.appendChild(message);

  var buttons = document.createElement('div');
  buttons.className = 'finish-btns';
  var backButton = createTextElement('button', 'btn-back-to-cat', '返回分类');
  backButton.onclick = backToCategory;
  var restartButton = createTextElement('button', 'btn-restart', '再来一次');
  restartButton.onclick = restartCurrentCat;
  buttons.append(backButton, restartButton);
  overlay.appendChild(buttons);
  document.body.appendChild(overlay);
  spawnFireworks();
  setTimeout(spawnFireworks, 300);
}

function restartCurrentCat() {
  var overlay = document.querySelector('.finish-overlay');
  if (overlay) overlay.remove();
  // 重新进入当前分类的学习页
  selectCategory(currentCategoryId);
}

/* ── 背景粒子 ── */
function createBgParticles() {
  for (var i = 0; i < 30; i++) {
    var p = document.createElement('div');
    p.className = 'bg-particle';
    p.style.left    = Math.random() * 100 + 'vw';
    p.style.top     = Math.random() * 100 + 'vh';
    p.style.opacity = (0.1 + Math.random() * 0.3).toString();
    document.body.appendChild(p);
  }
}

/* ── 键盘事件 ── */
document.addEventListener('keydown', function(e) {
  if (feverMode && document.activeElement === document.getElementById('feverInput')) {
    if (e.key.length === 1 && !e.ctrlKey && !e.metaKey) {
      playKeySound();
      spawnFeverKeyParticle();
    }
    if (e.key === 'Enter') {
      e.preventDefault();
      checkAnswer();
    }
    return;
  }
  if (e.key === 'Enter' && !document.getElementById('fogModal') && !document.getElementById('synthesisOverlay')) checkAnswer();
  var activeEl = document.activeElement;
  var isTypingInInput = activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA');
  if (e.key === 'Backspace' && selectedWords.length > 0 && !feverMode && !isTypingInInput) {
    e.preventDefault();
    removeLastWord();
  }
});

/* Fever 输入框实时反馈 */
document.getElementById('feverInput').addEventListener('input', function() {
  var q = vocab[currentIndex];
  if (!q) return;
  var val = this.value.toLowerCase();
  var ans = q.en.toLowerCase();
  this.style.borderColor = ans.indexOf(val) === 0
    ? 'rgba(255,215,0,0.6)'
    : 'rgba(248,81,73,0.6)';
});

/* ── 语义连线弹窗 ── */
function showSynthesisModal(phrases) {
  var overlay = document.createElement('div');
  overlay.className = 'synthesis-overlay';
  overlay.id = 'synthesisOverlay';

  var modal = document.createElement('div');
  modal.className = 'synthesis-modal';
  modal.style.maxWidth = '680px';
  modal.appendChild(createTextElement('div', 'synthesis-badge', 'CONTEXTUAL SYNTHESIS · 语义连线'));
  modal.appendChild(createTextElement('div', 'synthesis-title', '用刚学过的词伙升级句子 — 点击正确选项填空'));

  var cardsContainer = document.createElement('div');
  cardsContainer.className = 'syn-cards-container';
  cardsContainer.id = 'synCardsContainer';

  phrases.forEach(function(phrase, i) {
    // 尝试从 synthesisTemplates 取模板，否则生成通用句
    var tpl = synthesisTemplates[phrase.en] || {
      plain: 'This can be described as <span class="syn-blank">_______</span>.',
      upgraded: 'This can be described as <span class="syn-phrase-used">' + phrase.en + '</span>.'
    };

    var wrongOptions = phrases
      .filter(function(p) { return p.en !== phrase.en; })
      .map(function(p) { return p.en; });

    if (wrongOptions.length < 1) {
      var allEnKeys = Object.keys(synthesisTemplates);
      for (var k = 0; k < allEnKeys.length; k++) {
        if (allEnKeys[k] !== phrase.en && wrongOptions.indexOf(allEnKeys[k]) === -1) {
          wrongOptions.push(allEnKeys[k]);
          break;
        }
      }
    }

    var options = [phrase.en].concat(wrongOptions).sort(function() { return Math.random() - 0.5; });

    var card = document.createElement('div');
    card.className = 'syn-card';
    card.id = 'synCard' + i;
    card.appendChild(createTextElement('div', 'syn-card-phrase', phrase.zh));

    var sentenceBox = document.createElement('div');
    sentenceBox.className = 'syn-sentence-box';
    sentenceBox.id = 'synSentence' + i;
    sentenceBox.appendChild(createTextElement('span', 'syn-label syn-label-orig', '原句'));
    sentenceBox.appendChild(document.createTextNode(' '));
    var plainText = document.createElement('span');
    plainText.className = 'syn-plain-text';
    plainText.id = 'synPlain' + i;
    appendSynthesisMarkup(plainText, tpl.plain);
    sentenceBox.appendChild(plainText);
    card.appendChild(sentenceBox);

    var upgradedBox = document.createElement('div');
    upgradedBox.className = 'syn-upgraded-box';
    upgradedBox.id = 'synUpgraded' + i;
    upgradedBox.style.display = 'none';
    upgradedBox.appendChild(createTextElement('span', 'syn-label syn-label-good', '升级版'));
    upgradedBox.appendChild(document.createTextNode(' '));
    var upgradedText = document.createElement('span');
    upgradedText.className = 'syn-upgraded-text';
    appendSynthesisMarkup(upgradedText, tpl.upgraded);
    upgradedBox.appendChild(upgradedText);
    card.appendChild(upgradedBox);

    var optionsRow = document.createElement('div');
    optionsRow.className = 'syn-options-row';
    optionsRow.id = 'synOptions' + i;
    optionsRow.appendChild(createTextElement('span', 'syn-option-hint', '用刚练过的词伙填空：'));
    options.forEach(function(opt) {
      var optionButton = createTextElement('button', 'syn-option-btn', opt);
      optionButton.dataset.phrase = opt;
      optionsRow.appendChild(optionButton);
    });
    card.appendChild(optionsRow);

    var feedback = document.createElement('div');
    feedback.className = 'syn-feedback';
    feedback.id = 'synFeedback' + i;
    card.appendChild(feedback);
    cardsContainer.appendChild(card);
  });

  modal.appendChild(cardsContainer);
  var progress = createTextElement('div', 'syn-progress', '已解决 0 / ' + phrases.length);
  progress.id = 'synProgress';
  modal.appendChild(progress);
  var resultMessage = document.createElement('div');
  resultMessage.className = 'syn-result-msg';
  resultMessage.id = 'synResultMsg';
  modal.appendChild(resultMessage);
  var skipButton = createTextElement('button', 'synthesis-skip-btn', '跳过，继续练习');
  skipButton.id = 'synSkipBtn';
  modal.appendChild(skipButton);
  overlay.appendChild(modal);

  document.body.appendChild(overlay);

  var solved = 0;

  phrases.forEach(function(phrase, i) {
    var optionBtns = document.querySelectorAll('#synCard' + i + ' .syn-option-btn');
    optionBtns.forEach(function(btn) {
      btn.onclick = function() {
        var chosen     = btn.dataset.phrase;
        var card       = document.getElementById('synCard' + i);
        var feedback   = document.getElementById('synFeedback' + i);
        var optionsRow = document.getElementById('synOptions' + i);
        var upgradedBox  = document.getElementById('synUpgraded' + i);
        var sentenceBox  = document.getElementById('synSentence' + i);

        if (chosen === phrase.en) {
          btn.classList.add('syn-opt-correct');
          playCorrectTick();
          sentenceBox.style.display  = 'none';
          upgradedBox.style.display  = 'block';
          optionBtns.forEach(function(b) { b.disabled = true; });
          solved++;
          document.getElementById('synProgress').textContent = '已解决 ' + solved + ' / ' + phrases.length;

          if (solved === phrases.length) {
            document.getElementById('synResultMsg').className = 'syn-result-msg success';
            document.getElementById('synResultMsg').textContent = ' 全部正确！词伙已深度掌握！';
            document.getElementById('synSkipBtn').textContent = '继续练习 ';
            spawnParticles();
            playCorrectSound();
            setTimeout(closeModal, 2200);
          }
        } else {
          btn.classList.add('syn-opt-wrong');
          card.classList.add('syn-card-shake');
          playWrongSound();
          feedback.className = 'syn-feedback syn-feedback-wrong';
          feedback.textContent = ' 不对，再试试！';
          setTimeout(function() {
            btn.classList.remove('syn-opt-wrong');
            card.classList.remove('syn-card-shake');
            feedback.textContent = '';
          }, 800);
        }
      };
    });
  });

  function closeModal() {
    synthesisFired = false;
    overlay.remove();
    loadQuestion();
  }

  document.getElementById('synSkipBtn').onclick = closeModal;
}

/* ══════════════════════════════════════════════════
   初始化：构建分类页（不自动开始游戏）
══════════════════════════════════════════════════ */
buildCategoryPage();

/* ── 监听父页面请求保存（主页面返回时触发） ── */
window.addEventListener('message', function(e) {
  if (e.data && e.data.type === 'requestSave') {
    reportPhraseStudy(5);
  }
});

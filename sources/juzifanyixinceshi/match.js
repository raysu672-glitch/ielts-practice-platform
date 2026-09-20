(function (root) {
  /**
   * 写作句子翻译的判分（2026-09-20 重写）。
   *
   * 旧实现是「去标点后逐字全等」（`isChineseMatch`），线上 11 次提交全部 0.0 分：
   * 题目是「看英文，写中文」，学生必须把参考译文一字不差默写出来才算对，
   * 换个说法（哪怕意思完全正确）一律 0 分。这不是学生的问题，是判分方式的问题。
   *
   * 新实现走「规则四径」，四道闸全过才算对（见 gradeChinese）：
   *   ① 内容覆盖  bag 命中字符 / 参考长度        —— 治漏译、只写半句
   *   ② 语序一致  LCS / bag 命中                 —— 治「词都对但语序颠倒」
   *   ③ 逻辑关系  参考里的连接词，答案里必须有同组词  —— 治把因果/转折关系丢了
   *   ④ 关键信息  数字、百分比、英文专名必须出现   —— 治漏掉硬信息点
   * 另加长度比下限，防止「只写开头几个字」靠内容覆盖蒙分。
   *
   * 已知边界（产品已确认接受）：细粒度语法（缺「的/了/着」、量词错、搭配错）
   * 以及幅度较大的同义改写，规则法挡不住也放不过；语序颠倒、漏译、逻辑丢失能挡住。
   */

  /** 去掉空白、零宽字符与标点，得到可比对的字符串（保留中英文与数字）。 */
  function normalizeChinese(s) {
    var t = String(s || '').toLowerCase();
    t = t.replace(/[\s\u00a0\u3000]/g, '');
    t = t.replace(/[\u200b-\u200d\ufeff]/g, '');
    try {
      t = t.replace(/[\p{P}]/gu, '');
    } catch (e) {
      t = t.replace(/[!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~，。！？；：、…—－·•“”‘’「」『』【】《》〈〉（）]/g, '');
    }
    return t;
  }

  /**
   * 逻辑关系词（同义归组）。参考译文命中某组 → 学生答案必须命中**同组中任一词**。
   * 用同组任意词命中即可，所以「因为」写成「由于」不算错。
   */
  var LOGIC_GROUPS = [
    ['因为', '由于', '因'],
    ['所以', '因此', '因而', '从而', '故'],
    ['但是', '但', '然而', '可是', '不过'],
    ['虽然', '尽管', '即使', '纵然', '固然'],
    ['如果', '若', '假如', '倘若', '要是'],
    ['而且', '并且', '不仅', '以及', '同时', '况且'],
    ['例如', '比如', '譬如', '举个例子'],
    ['首先', '第一', '其一'],
    ['其次', '第二', '其二'],
    ['最后', '总之', '综上所述', '总而言之'],
    ['而是', '反而', '反之', '相反'],
    ['为了', '以便', '以免'],
    ['尤其', '特别是', '特别是'],
    ['一方面', '另一方面']
  ];

  /** 参考译文里出现的逻辑组（按在参考中的首次出现位置排序）。 */
  function logicGroupsIn(text) {
    var hits = [];
    for (var i = 0; i < LOGIC_GROUPS.length; i++) {
      var group = LOGIC_GROUPS[i];
      var best = -1;
      for (var j = 0; j < group.length; j++) {
        var pos = text.indexOf(group[j]);
        if (pos >= 0 && (best < 0 || pos < best)) best = pos;
      }
      if (best >= 0) hits.push({ pos: best, group: group });
    }
    hits.sort(function (a, b) { return a.pos - b.pos; });
    return hits.map(function (h) { return h.group; });
  }

  /** 学生答案是否命中该逻辑组（任一同义词即可）。 */
  function hitsGroup(text, group) {
    for (var j = 0; j < group.length; j++) {
      if (text.indexOf(group[j]) >= 0) return true;
    }
    return false;
  }

  /**
   * 硬信息点：阿拉伯数字、百分比、英文专有名词。
   * 在**原始文本**（未去标点）上抽取，这样 `2.5%`、`FaceTime` 都能识别；
   * 只看数字本体，`2.5%` 与 `2.5 %` 视为同一个点。
   */
  function hardTokens(raw) {
    var out = [];
    var seen = {};
    var re = /[A-Za-z][A-Za-z'\-]*|\d+(?:\.\d+)?/g;
    var m;
    var text = String(raw || '');
    while ((m = re.exec(text)) !== null) {
      var tok = m[0].toLowerCase().replace(/'/g, '');
      if (!tok || seen[tok]) continue;
      seen[tok] = 1;
      out.push({ token: tok, display: m[0] });
    }
    return out;
  }

  /** 不看顺序的命中字符数（多重集交集大小）。 */
  function bagHit(ref, ans) {
    var counts = {};
    var i, c;
    for (i = 0; i < ref.length; i++) {
      c = ref.charAt(i);
      counts[c] = (counts[c] || 0) + 1;
    }
    var hit = 0;
    for (i = 0; i < ans.length; i++) {
      c = ans.charAt(i);
      if (counts[c]) {
        counts[c] -= 1;
        hit += 1;
      }
    }
    return hit;
  }

  /** 最长公共子序列长度（滚动数组，句子很短，够用）。 */
  function lcsLen(ref, ans) {
    if (!ref.length || !ans.length) return 0;
    var prev = new Array(ans.length + 1);
    var cur = new Array(ans.length + 1);
    var i, j;
    for (j = 0; j <= ans.length; j++) prev[j] = 0;
    for (i = 1; i <= ref.length; i++) {
      cur[0] = 0;
      for (j = 1; j <= ans.length; j++) {
        cur[j] = ref.charAt(i - 1) === ans.charAt(j - 1)
          ? prev[j - 1] + 1
          : Math.max(prev[j], cur[j - 1]);
      }
      var tmp = prev;
      prev = cur;
      cur = tmp;
    }
    return prev[ans.length];
  }

  // 四道闸的门槛（集中在此，便于教研调参）
  var MIN_COVERAGE = 0.75;  // ① 内容覆盖
  var MIN_ORDER = 0.85;     // ② 语序一致
  var MIN_LEN_RATIO = 0.6;  // 长度下限（防「只写几个字」靠覆盖蒙分）

  /**
   * 判一句中文翻译。
   * @returns {{ok:boolean, score:number, coverage:number, order:number,
   *            lenRatio:number, missingLogic:Array, missingHard:Array,
   *            reasons:Array<string>}}
   */
  function gradeChinese(user, answer) {
    var rawUser = String(user || '');
    var rawRef = String(answer || '');
    var ans = normalizeChinese(rawUser);
    var ref = normalizeChinese(rawRef);

    if (!ref) {
      return {
        ok: false, score: 0, coverage: 0, order: 0, lenRatio: 0,
        missingLogic: [], missingHard: [], reasons: ['题目缺少参考译文']
      };
    }
    if (!ans) {
      return {
        ok: false, score: 0, coverage: 0, order: 0, lenRatio: 0,
        missingLogic: [], missingHard: [], reasons: ['没有作答']
      };
    }
    // 防御：学生粘进来一大段，截断避免 LCS 变大
    if (ans.length > ref.length * 3) ans = ans.slice(0, ref.length * 3);

    var bag = bagHit(ref, ans);
    var lcs = lcsLen(ref, ans);
    var coverage = bag / ref.length;
    var order = bag ? lcs / bag : 0;
    var lenRatio = ans.length / ref.length;

    // ③ 逻辑关系：参考里有的，答案里必须有同组词
    var missingLogic = [];
    var refGroups = logicGroupsIn(ref);
    for (var i = 0; i < refGroups.length; i++) {
      if (!hitsGroup(ans, refGroups[i])) missingLogic.push(refGroups[i][0]);
    }

    // ④ 关键信息点：数字 / 百分比 / 英文专名
    var missingHard = [];
    var hard = hardTokens(rawRef);
    var userHard = {};
    var userToks = hardTokens(rawUser);
    for (var k = 0; k < userToks.length; k++) userHard[userToks[k].token] = 1;
    for (var h = 0; h < hard.length; h++) {
      if (!userHard[hard[h].token]) missingHard.push(hard[h].display);
    }

    var reasons = [];
    if (lenRatio < MIN_LEN_RATIO) {
      reasons.push('答得太短，只写了参考译文约 ' + Math.round(lenRatio * 100) + '% 的内容，疑似漏译');
    }
    if (coverage < MIN_COVERAGE) {
      reasons.push('内容覆盖只有 ' + Math.round(coverage * 100) + '%，漏译较多');
    }
    if (order < MIN_ORDER) {
      reasons.push('用词大部分对，但语序与参考译文不一致');
    }
    if (missingLogic.length) {
      reasons.push('少了逻辑关系词：' + missingLogic.join('、'));
    }
    if (missingHard.length) {
      reasons.push('漏了关键信息：' + missingHard.join('、'));
    }

    return {
      ok: reasons.length === 0,
      // 展示用的连续分：内容 × 语序，让人一眼看出「词写对多少、顺序对不对」
      score: Math.round(coverage * order * 100),
      coverage: coverage,
      order: order,
      lenRatio: lenRatio,
      missingLogic: missingLogic,
      missingHard: missingHard,
      reasons: reasons
    };
  }

  /** 兼容旧接口：逐字全等。保留给错题本等只想做严格比对的地方。 */
  function isChineseMatch(user, answer) {
    var ua = normalizeChinese(user);
    var ca = normalizeChinese(answer);
    return ua.length > 0 && ua === ca;
  }

  var api = {
    normalizeChinese: normalizeChinese,
    isChineseMatch: isChineseMatch,
    gradeChinese: gradeChinese,
    MIN_COVERAGE: MIN_COVERAGE,
    MIN_ORDER: MIN_ORDER,
    MIN_LEN_RATIO: MIN_LEN_RATIO
  };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }
  root.TranslateMatch = api;
})(typeof window !== 'undefined' ? window : globalThis);

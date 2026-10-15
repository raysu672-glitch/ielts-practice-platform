/**
 * 入学摸底 · 正确率 / AI 档 → 雅思区间、分档、综合预估
 * 映射表写死；后续可用真实学生成绩校准数字，不必改流程。
 */
(function (root) {
  function clampPct(n) {
    var x = Number(n);
    if (!isFinite(x)) return 0;
    return Math.max(0, Math.min(100, x));
  }

  /** 功能词：不计入听力关键词覆盖（写不全时仍看实词命中） */
  var DICTATION_STOP = {
    a: 1, an: 1, the: 1, and: 1, or: 1, but: 1, if: 1, to: 1, of: 1, in: 1, on: 1,
    for: 1, at: 1, by: 1, as: 1, with: 1, from: 1, into: 1, about: 1, than: 1, then: 1,
    is: 1, are: 1, was: 1, were: 1, be: 1, been: 1, being: 1, am: 1,
    it: 1, its: 1, "it's": 1, you: 1, your: 1, they: 1, them: 1, their: 1,
    this: 1, that: 1, these: 1, those: 1, there: 1, "there's": 1, here: 1,
    not: 1, no: 1, so: 1, too: 1, very: 1, just: 1, also: 1, only: 1,
    can: 1, could: 1, would: 1, should: 1, will: 1, shall: 1, may: 1, might: 1,
    have: 1, has: 1, had: 1, do: 1, does: 1, did: 1,
    "don't": 1, "doesn't": 1, "didn't": 1,
    i: 1, we: 1, he: 1, she: 1, my: 1, our: 1, his: 1, her: 1,
    who: 1, whom: 1, which: 1, what: 1, when: 1, where: 1, how: 1, why: 1,
    own: 1, both: 1, few: 1, most: 1, more: 1, some: 1, any: 1, all: 1,
    before: 1, after: 1, while: 1, during: 1, out: 1, up: 1, down: 1, off: 1
  };

  function normalizeDictationText(s) {
    return String(s || '')
      .toLowerCase()
      .replace(/[''']/g, "'")
      .replace(/[""]/g, '"')
      .replace(/[—–-]/g, '-')
      .replace(/[^\w\s'-]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function contentTokens(text) {
    var tokens = normalizeDictationText(text).split(/\s+/).filter(Boolean);
    var out = [];
    for (var i = 0; i < tokens.length; i++) {
      var w = tokens[i].replace(/^'+|'+$/g, '');
      if (!w || DICTATION_STOP[w]) continue;
      if (w.length <= 1 && !/^\d+$/.test(w)) continue;
      out.push(w);
    }
    return out;
  }

  /**
   * 整句听写 · 关键词覆盖打分（写不全也能得分）
   * @returns {{coverage:number, hit:number, need:number, correct:boolean, empty:boolean}}
   */
  function gradeDictation(user, answer) {
    var needTokens = contentTokens(answer);
    var userNorm = normalizeDictationText(user);
    if (!userNorm) {
      return { coverage: 0, hit: 0, need: needTokens.length, correct: false, empty: true };
    }
    if (!needTokens.length) {
      var full = userNorm === normalizeDictationText(answer);
      return { coverage: full ? 1 : 0, hit: full ? 1 : 0, need: 1, correct: full, empty: false };
    }
    var bag = {};
    contentTokens(user).forEach(function (w) {
      bag[w] = (bag[w] || 0) + 1;
    });
    var hit = 0;
    needTokens.forEach(function (w) {
      if (bag[w] > 0) {
        bag[w] -= 1;
        hit += 1;
      }
    });
    var coverage = hit / needTokens.length;
    return {
      coverage: coverage,
      hit: hit,
      need: needTokens.length,
      correct: coverage >= 0.85,
      empty: false
    };
  }

  /** @returns {{low:number, high:number, label:string}} */
  function bandFromListeningPct(pct) {
    pct = clampPct(pct);
    if (pct < 50) return makeBand(4.5, 5.0);
    if (pct < 70) return makeBand(5.0, 5.5);
    if (pct < 85) return makeBand(5.5, 6.0);
    return makeBand(6.0, 6.5);
  }

  function bandFromReadingPct(pct) {
    pct = clampPct(pct);
    if (pct < 50) return makeBand(4.5, 5.0);
    if (pct < 70) return makeBand(5.0, 5.5);
    if (pct < 85) return makeBand(5.5, 6.0);
    return makeBand(6.0, 6.5);
  }

  /**
   * 写作：词伙 40% + 翻译 60%；词伙 <40% 时下沿再压 0.5
   */
  function bandFromWriting(phrasePct, translatePct) {
    var p = clampPct(phrasePct);
    var t = clampPct(translatePct);
    var mixed = p * 0.4 + t * 0.6;
    var band;
    if (mixed < 45) band = makeBand(4.5, 5.0);
    else if (mixed < 65) band = makeBand(5.0, 5.5);
    else if (mixed < 80) band = makeBand(5.5, 6.0);
    else band = makeBand(6.0, 6.5);
    if (p < 40 && band.low > 4.5) {
      band = makeBand(Math.max(4.5, band.low - 0.5), Math.max(band.low, band.high - 0.5));
    }
    return band;
  }

  /** 有效作答过少 → 不给雅思区间（避免空卷落到 4.5–5.5 假分） */
  function insufficientBand(reason) {
    return {
      low: null,
      high: null,
      label: '作答不足',
      insufficient: true,
      reason: reason || '有效作答过少'
    };
  }

  function answerRatio(answered, total) {
    var a = Number(answered) || 0;
    var t = Number(total) || 0;
    if (t <= 0) return 0;
    return a / t;
  }

  /** 至少作答约四成，才用正确率映射分数 */
  function hasEnoughAnswers(answered, total, minRatio) {
    var ratio = minRatio == null ? 0.4 : minRatio;
    var t = Number(total) || 0;
    if (t <= 0) return false;
    return answerRatio(answered, t) >= ratio && (Number(answered) || 0) >= 1;
  }

  /** AI overall 或启发式分数 → 半档宽区间，如 5.5 → 5.5–6.0 */
  function bandFromSpeakingOverall(overall) {
    if (overall == null || !isFinite(Number(overall))) {
      return { low: null, high: null, label: '—' };
    }
    var o = Math.round(Number(overall) * 2) / 2;
    o = Math.max(4.0, Math.min(8.0, o));
    return makeBand(o, Math.min(8.0, o + 0.5));
  }

  function fmtBand(n) {
    var x = Math.round(Number(n) * 2) / 2;
    return x === Math.floor(x) ? x.toFixed(1) : String(x);
  }

  function makeBand(low, high) {
    low = Math.round(Number(low) * 2) / 2;
    high = Math.round(Number(high) * 2) / 2;
    if (high < low) high = low;
    return {
      low: low,
      high: high,
      label: low === high ? fmtBand(low) : fmtBand(low) + '–' + fmtBand(high)
    };
  }

  /** 分档：重补 / 轻补 / 可上正课（相对目标分） */
  function tierFromBand(band, targetScore) {
    if (!band || band.low == null) return { id: 'unknown', label: '待定', advice: '数据不足，建议重测或人工面谈' };
    var target = Number(targetScore) || 6.5;
    var mid = (band.low + band.high) / 2;
    var gap = target - mid;
    if (gap >= 1.0) {
      return { id: 'heavy', label: '重补', advice: '基础优先排清单前段，阶段测插密' };
    }
    if (gap >= 0.5) {
      return { id: 'light', label: '轻补', advice: '少排基础单元，与正课穿插，用阶段测校准' };
    }
    return { id: 'ready', label: '可上正课', advice: '按正常单元推进，不必重补入口' };
  }

  function overallFromBands(bands) {
    var lows = [];
    var highs = [];
    ['listening', 'reading', 'writing', 'speaking'].forEach(function (k) {
      var b = bands[k];
      if (b && b.low != null) {
        lows.push(b.low);
        highs.push(b.high);
      }
    });
    if (!lows.length) {
      return { low: null, high: null, label: '—', insufficient: true };
    }
    // 短板偏向下沿：综合用最低下沿与平均上沿收束
    var minLow = Math.min.apply(null, lows);
    var avgHigh = highs.reduce(function (a, b) { return a + b; }, 0) / highs.length;
    var high = Math.max(minLow, Math.min(avgHigh, minLow + 0.5));
    high = Math.round(high * 2) / 2;
    return makeBand(minLow, high);
  }

  function commentListening(pct, correct, total) {
    pct = clampPct(pct);
    if (pct >= 85) return '关键词覆盖高，关键信息抓取稳';
    if (pct >= 70) return '大意能跟上；句子写不全或拼写偶有错，不影响档位';
    if (pct >= 50) return '能听出部分关键词，完整度不足，需继续练听写';
    if (pct > 0) return '只抓到少量词，建议先补听力基础与答案句';
    return '几乎未写出有效内容，听力区间仅供参考（置信度低）';
  }

  function commentReading(pct) {
    pct = clampPct(pct);
    if (pct >= 85) return '同义反应快，阅读可跟正课节奏';
    if (pct >= 70) return '同义识别尚可，速度或准确率仍有提升空间';
    if (pct >= 50) return '同义不够稳，阅读提分会受拖累';
    return '同义基础偏弱，建议先重补阅读同义';
  }

  function commentWriting(phrasePct, translatePct) {
    var p = clampPct(phrasePct);
    var t = clampPct(translatePct);
    if (p < 40 && t < 50) return '搭配不稳；译文偏弱，语法与表达需系统补';
    if (p < 50) return '词伙掌握不足，写作词汇需优先补';
    if (t < 50) return '词伙尚可，译文完成度不足，句法需加强';
    if (p >= 70 && t >= 70) return '词伙与翻译表现较好，可逐步加大作文比重';
    return '写作中等，建议词伙与翻译继续轻补';
  }

  function commentSpeaking(overall, conf, transcriptLen) {
    if (overall == null) {
      if (transcriptLen > 20) return '已录音但未能完成 AI 估分，仅作分档参考';
      return '口语录音无效或过短，置信度低';
    }
    if (overall >= 6.0) return '基本连贯，错误不影响理解；可继续扩展词汇';
    if (overall >= 5.5) return '能答完，停顿或词汇偏窄，需轻补输出';
    if (overall >= 5.0) return '能组织简单回答，流利与语法仍不稳';
    return '输出偏短或难懂，建议口语基础重补';
  }

  function confidenceForRules(answered, total, timedOut) {
    if (total <= 0) return '低';
    if (answered < total * 0.5) return '低';
    if (timedOut && answered < total) return '中';
    return '高';
  }

  function scorePercentFromBands(bands) {
    var mids = [];
    ['listening', 'reading', 'writing', 'speaking'].forEach(function (k) {
      var b = bands[k];
      if (b && b.low != null) mids.push((b.low + b.high) / 2);
    });
    if (!mids.length) return 0;
    var avg = mids.reduce(function (a, b) { return a + b; }, 0) / mids.length;
    return Math.round(avg * 10); // 5.5 → 55，便于记录页展示
  }

  function buildReport(input) {
    var target = Number(input.targetScore) || 6.5;
    var L = input.listening || {};
    var R = input.reading || {};
    var W = input.writing || {};
    var S = input.speaking || {};

    // 听力优先用关键词覆盖率；无覆盖字段时回退「整句全对」口径
    var lPct = L.coveragePct != null
      ? clampPct(L.coveragePct)
      : (L.total ? Math.round((L.correct / L.total) * 100) : 0);
    var rPct = R.total ? Math.round((R.correct / R.total) * 100) : 0;
    var pPct = W.phraseTotal ? Math.round((W.phraseCorrect / W.phraseTotal) * 100) : 0;
    var tPct = W.translateTotal ? Math.round((W.translateCorrect / W.translateTotal) * 100) : 0;

    var lAnswered = L.answered != null ? L.answered : L.total;
    var rAnswered = R.answered != null ? R.answered : R.total;
    var wAnswered = (Number(W.phraseAnswered) || 0) + (Number(W.translateAnswered) || 0);
    var wTotal = (Number(W.phraseTotal) || 0) + (Number(W.translateTotal) || 0);
    // 未传作答数时：正确率为 0 且无覆盖 → 视为未作答
    if (W.phraseAnswered == null && W.translateAnswered == null) {
      wAnswered = (pPct > 0 || tPct > 0) ? wTotal : 0;
    }

    var listeningBand = hasEnoughAnswers(lAnswered, L.total)
      ? bandFromListeningPct(lPct)
      : insufficientBand('听力有效作答过少');
    var readingBand = hasEnoughAnswers(rAnswered, R.total)
      ? bandFromReadingPct(rPct)
      : insufficientBand('阅读有效作答过少');
    var writingBand = hasEnoughAnswers(wAnswered, wTotal)
      ? bandFromWriting(pPct, tPct)
      : insufficientBand('写作有效作答过少');
    var speakingOk = S.overall != null && isFinite(Number(S.overall)) && (Number(S.transcriptLen) || 0) >= 20;
    var speakingBand = speakingOk
      ? bandFromSpeakingOverall(S.overall)
      : insufficientBand('口语未有效作答或录音过短');

    var speakingConf = speakingOk
      ? (S.confidence || '中')
      : '低';
    var bands = {
      listening: Object.assign({}, listeningBand, {
        confidence: listeningBand.insufficient
          ? '低'
          : confidenceForRules(lAnswered, L.total, L.timedOut),
        comment: listeningBand.insufficient
          ? '几乎未作答，无法估听力分数，请重测'
          : commentListening(lPct, L.correct, L.total),
        pct: lPct,
        correct: L.correct || 0,
        total: L.total || 0
      }),
      reading: Object.assign({}, readingBand, {
        confidence: readingBand.insufficient
          ? '低'
          : confidenceForRules(rAnswered, R.total, R.timedOut),
        comment: readingBand.insufficient
          ? '几乎未作答，无法估阅读分数，请重测'
          : commentReading(rPct),
        pct: rPct,
        correct: R.correct || 0,
        total: R.total || 0
      }),
      writing: Object.assign({}, writingBand, {
        confidence: writingBand.insufficient ? '低' : '中',
        comment: writingBand.insufficient
          ? '几乎未作答，无法估写作分数，请重测'
          : commentWriting(pPct, tPct),
        phrasePct: pPct,
        translatePct: tPct,
        phraseCorrect: W.phraseCorrect || 0,
        phraseTotal: W.phraseTotal || 0,
        translateCorrect: W.translateCorrect || 0,
        translateTotal: W.translateTotal || 0
      }),
      speaking: Object.assign({}, speakingBand, {
        confidence: speakingConf,
        comment: speakingBand.insufficient
          ? '未有效录音，无法估口语分数，请重测'
          : commentSpeaking(S.overall, speakingConf, S.transcriptLen || 0),
        overall: S.overall,
        subscores: S.subscores || null
      })
    };

    var tiers = {
      listening: tierFromBand(bands.listening, target),
      reading: tierFromBand(bands.reading, target),
      writing: tierFromBand(bands.writing, target),
      speaking: tierFromBand(bands.speaking, target)
    };

    var overall = overallFromBands(bands);
    var scoredCount = ['listening', 'reading', 'writing', 'speaking'].filter(function (k) {
      return bands[k] && bands[k].low != null;
    }).length;
    var summary;
    if (scoredCount === 0) {
      summary = '有效作答过少，无法给出雅思预估区间。请认真完成四科后再测；当前结果仅供确认已打开测试。';
      overall = { low: null, high: null, label: '作答不足', insufficient: true };
    } else if (scoredCount < 3) {
      summary =
        '仅 ' + scoredCount + ' 科有有效作答，综合仅供参考（约 ' + overall.label +
        '）。未作答科目请重测后再排课。';
    } else {
      var weak = [];
      Object.keys(tiers).forEach(function (k) {
        if (tiers[k].id === 'heavy') weak.push(subjectLabel(k));
        else if (tiers[k].id === 'light') weak.push(subjectLabel(k) + '（轻）');
      });
      summary =
        '整体大约 ' + overall.label +
        (weak.length ? '，' + weak.join('、') + '偏弱' : '，四科较均衡') +
        '；建议先按分档排基础与正课比重。';
    }

    return {
      form: input.form || 'A',
      targetScore: target,
      overall: overall,
      summary: summary,
      bands: bands,
      tiers: tiers,
      scorePercent: scoredCount ? scorePercentFromBands(bands) : 0,
      planHint: scoredCount
        ? buildPlanHint(tiers)
        : '作答不足，暂不排课；请用完整摸底或当面诊断后再定清单。'
    };
  }

  function subjectLabel(k) {
    return { listening: '听力', reading: '阅读', writing: '写作', speaking: '口语' }[k] || k;
  }

  function buildPlanHint(tiers) {
    var order = [];
    ['writing', 'speaking', 'listening', 'reading'].forEach(function (k) {
      if (tiers[k] && tiers[k].id === 'heavy') order.push(subjectLabel(k) + '基础');
    });
    ['writing', 'speaking', 'listening', 'reading'].forEach(function (k) {
      if (tiers[k] && tiers[k].id === 'light') order.push(subjectLabel(k) + '轻补');
    });
    ['reading', 'listening', 'writing', 'speaking'].forEach(function (k) {
      if (tiers[k] && tiers[k].id === 'ready') order.push(subjectLabel(k) + '正课');
    });
    if (!order.length) return '第一周用阶段测校准后再定清单。';
    return order.join(' → ') + '；第一周结束后用阶段测修正写口区间。';
  }

  root.PlacementScoring = {
    gradeDictation: gradeDictation,
    contentTokens: contentTokens,
    normalizeDictationText: normalizeDictationText,
    bandFromListeningPct: bandFromListeningPct,
    bandFromReadingPct: bandFromReadingPct,
    bandFromWriting: bandFromWriting,
    bandFromSpeakingOverall: bandFromSpeakingOverall,
    tierFromBand: tierFromBand,
    buildReport: buildReport,
    scorePercentFromBands: scorePercentFromBands
  };
})(typeof window !== 'undefined' ? window : globalThis);

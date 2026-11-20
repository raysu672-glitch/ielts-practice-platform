/**
 * 作文批改训练：提交判分（浏览器 + Node 测试共用）
 *
 * 目标：学生写「改正后的词/短语」时，不要因为少写冠词、或多写/少写个别虚词就误判。
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.WritingPracticeScore = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var LIGHT_WORDS = {
    a: 1, an: 1, the: 1, it: 1, to: 1, of: 1, in: 1, on: 1, for: 1,
    and: 1, or: 1, as: 1, at: 1, by: 1, with: 1, from: 1
  };

  function normalizeForCompare(text) {
    return String(text || "")
      .replace(/\u00a0/g, " ")
      .replace(/[\u2018\u2019]/g, "'")
      .replace(/[\u201c\u201d]/g, '"')
      .replace(/\s+/g, " ")
      .trim()
      .replace(/[.。!！?？…]+$/g, "")
      .toLowerCase();
  }

  function stripQuotes(text) {
    return String(text || "").replace(/^["'“”‘’]+|["'“”‘’]+$/g, "");
  }

  function tokenizeForCompare(text) {
    return stripQuotes(normalizeForCompare(text))
      .split(/[^a-z0-9'’-]+/i)
      .filter(Boolean);
  }

  function containsAsWord(haystack, word) {
    var tokens = tokenizeForCompare(haystack);
    var w = stripQuotes(normalizeForCompare(word));
    if (!w) return false;
    return tokens.indexOf(w) >= 0 || stripQuotes(normalizeForCompare(haystack)) === w;
  }

  /** haystack 是否包含 needle 的连续词序列 */
  function containsPhrase(haystack, phrase) {
    var h = tokenizeForCompare(haystack);
    var p = tokenizeForCompare(phrase);
    if (!p.length) return false;
    if (p.length === 1) return h.indexOf(p[0]) >= 0;
    var i;
    var j;
    for (i = 0; i <= h.length - p.length; i++) {
      for (j = 0; j < p.length; j++) {
        if (h[i + j] !== p[j]) break;
      }
      if (j === p.length) return true;
    }
    return false;
  }

  /** needle 词是否按顺序出现在 haystack 中（允许间隔） */
  function tokensInOrder(haystackTokens, needleTokens) {
    var i = 0;
    var n;
    for (n = 0; n < needleTokens.length; n++) {
      while (i < haystackTokens.length && haystackTokens[i] !== needleTokens[n]) i++;
      if (i >= haystackTokens.length) return false;
      i++;
    }
    return true;
  }

  function stripLightWords(tokens) {
    return tokens.filter(function (t) { return !LIGHT_WORDS[t]; });
  }

  function getChangedCorrectTokens(errorPhrase, correctPhrase) {
    var errTokens = tokenizeForCompare(errorPhrase);
    var fixTokens = tokenizeForCompare(correctPhrase);
    var changed = [];
    var len = Math.max(errTokens.length, fixTokens.length);
    var i;
    for (i = 0; i < len; i++) {
      var e = errTokens[i] || "";
      var f = fixTokens[i] || "";
      if (f && f !== e) changed.push(f);
    }
    fixTokens.forEach(function (f) {
      if (f && errTokens.indexOf(f) < 0 && changed.indexOf(f) < 0) changed.push(f);
    });
    return changed;
  }

  function extractLocalReplacement(originalSentence, highlight, correctedSentence) {
    if (!originalSentence || !highlight || !correctedSentence) return null;
    var origLower = originalSentence.toLowerCase();
    var hiLower = String(highlight).toLowerCase();
    var idx = origLower.indexOf(hiLower);
    if (idx < 0) return null;
    var before = originalSentence.slice(0, idx);
    var after = originalSentence.slice(idx + highlight.length);
    var corrLower = correctedSentence.toLowerCase();
    if (corrLower.startsWith(before.toLowerCase()) && corrLower.endsWith(after.toLowerCase())) {
      var startIdx = before.length;
      var endIdx = correctedSentence.length - after.length;
      if (endIdx >= startIdx) {
        return correctedSentence.slice(startIdx, endIdx);
      }
    }
    // 标点插入：so they → , so they（before 因逗号对不齐时）
    return extractPunctuationLocalFix(originalSentence, highlight, correctedSentence);
  }

  /**
   * 仅在 highlight 前插入逗号/分号等：抽出「, so they dare not」这类局部修正。
   */
  function extractPunctuationLocalFix(originalSentence, highlight, correctedSentence) {
    var orig = String(originalSentence || "");
    var corr = String(correctedSentence || "");
    var hi = String(highlight || "");
    if (!orig || !corr || !hi) return null;
    var hiLower = hi.toLowerCase();
    var oi = orig.toLowerCase().indexOf(hiLower);
    var ci = corr.toLowerCase().indexOf(hiLower);
    if (oi < 0 || ci < 0) return null;

    var afterO = orig.slice(oi + hi.length);
    var afterC = corr.slice(ci + hi.length);
    if (normalizeForCompare(afterO) !== normalizeForCompare(afterC)) return null;

    // 修正句中 highlight 前的标点前缀
    var start = ci;
    while (start > 0 && /[\s,;:，；：]/.test(corr.charAt(start - 1))) {
      start -= 1;
    }
    var local = corr.slice(start, ci + hi.length);
    if (!local || normalizeForCompare(local) === normalizeForCompare(hi)) {
      // 可能只有空格差异
      if (local.replace(/\s+/g, " ") === hi.replace(/\s+/g, " ")) return null;
    }
    // 原文同一位置前不应已有相同标点前缀
    var origPrefixStart = oi;
    while (origPrefixStart > 0 && /[\s,;:，；：]/.test(orig.charAt(origPrefixStart - 1))) {
      origPrefixStart -= 1;
    }
    var origPrefix = orig.slice(origPrefixStart, oi + hi.length);
    if (normalizeForCompare(origPrefix) === normalizeForCompare(local) &&
        origPrefix.replace(/\s+/g, " ") === local.replace(/\s+/g, " ")) {
      return null;
    }
    // 必须真的多了标点（不能只是多空格）
    var localPunct = local.replace(/[A-Za-z0-9'’\s\-]/g, "");
    var hiPunct = hi.replace(/[A-Za-z0-9'’\s\-]/g, "");
    if (!localPunct || localPunct === hiPunct) return null;
    return local;
  }

  /**
   * 把检查点修正叠到当前基句上；禁止用整句 rawCorrected 回退已改好的前文。
   */
  function applyFixToBase(baseText, checkpoint) {
    var base = String(baseText || "");
    if (!checkpoint) return base;
    var highlight = String(checkpoint.highlight || "");
    var original = String(checkpoint.originalSentence || base);
    var fullCorrected = String(checkpoint.rawCorrected || checkpoint.answer || "");
    var replacement = null;
    if (highlight && fullCorrected) {
      replacement = extractLocalReplacement(original, highlight, fullCorrected);
    }
    if (
      replacement != null &&
      String(replacement).length > 0 &&
      highlight &&
      new RegExp(escapeRegex(highlight), "i").test(base)
    ) {
      // 插入前置标点时吃掉 highlight 前多余空白，避免 "knowledge , so"
      var pattern = /^[,;:，；：]/.test(String(replacement))
        ? new RegExp("\\s*(" + escapeRegex(highlight) + ")", "i")
        : new RegExp(escapeRegex(highlight), "i");
      return base.replace(pattern, replacement);
    }
    if (
      fullCorrected &&
      normalizeForCompare(base) === normalizeForCompare(original)
    ) {
      return fullCorrected;
    }
    return base;
  }

  function findHighlightRange(base, highlight) {
    var b = String(base || "");
    var h = String(highlight || "");
    if (!b || !h) return null;
    var idx = b.toLowerCase().indexOf(h.toLowerCase());
    if (idx < 0) return null;
    return { start: idx, end: idx + h.length };
  }

  function escapeRegex(str) {
    return String(str).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function getExpectedLocalFix(checkpoint) {
    if (!checkpoint) return "";
    var highlight = String(checkpoint.highlight || "").trim();
    var fullAnswer = String(checkpoint.answer || checkpoint.rawCorrected || "").trim();
    var base = String(checkpoint.baseText || checkpoint.originalSentence || "").trim();
    var original = String(checkpoint.originalSentence || checkpoint.baseText || "").trim();

    var local = extractLocalReplacement(original, highlight, checkpoint.rawCorrected || fullAnswer);
    if (local == null || !String(local).trim()) {
      local = extractLocalReplacement(base, highlight, fullAnswer);
    }
    if (local == null || !String(local).trim()) {
      local = extractPunctuationLocalFix(original, highlight, checkpoint.rawCorrected || fullAnswer);
    }
    if (local == null || !String(local).trim()) {
      local = extractPunctuationLocalFix(base, highlight, fullAnswer);
    }
    if (local != null && String(local).trim()) {
      return String(local).trim();
    }

    if (highlight && base && fullAnswer) {
      var range = findHighlightRange(base, highlight);
      if (range) {
        var before = base.slice(0, range.start);
        var after = base.slice(range.end);
        var beforeN = normalizeForCompare(before);
        var afterN = normalizeForCompare(after);
        var fullN = normalizeForCompare(fullAnswer);
        if (fullN.startsWith(beforeN) && fullN.endsWith(afterN)) {
          var startIdx = before.length;
          var endIdx = after.length === 0 ? fullAnswer.length : fullAnswer.length - after.length;
          if (endIdx >= startIdx) {
            var mid = fullAnswer.slice(startIdx, endIdx).trim();
            if (mid) return mid;
          }
        }
      }
    }

    // 基句已递进修正、整句参考仍是旧原文时：用「基句 + 标点插入」合成局部答案
    if (highlight && base && fullAnswer) {
      var punctOnFull = extractPunctuationLocalFix(original, highlight, fullAnswer);
      if (punctOnFull) return String(punctOnFull).trim();
    }

    if (fullAnswer && fullAnswer.length <= 40 && (!base || fullAnswer.length < base.length * 0.5)) {
      return fullAnswer;
    }
    return "";
  }

  /**
   * 局部作答是否足够接近期望修正（允许少虚词、交连续子短语）。
   */
  function isAcceptableLocalAnswer(studentNorm, localFix, errPhrase) {
    var fixN = stripQuotes(normalizeForCompare(localFix));
    var errN = stripQuotes(normalizeForCompare(errPhrase || ""));
    var a = studentNorm;
    if (!a || !fixN) return false;
    if (a === fixN) return true;

    var stuTok = tokenizeForCompare(a);
    var fixTok = tokenizeForCompare(fixN);
    var errTok = tokenizeForCompare(errN);
    // 仍带着错误侧独有词（except for → except 时的 for）→ 直接否
    var errExtra = errTok.filter(function (t) { return fixTok.indexOf(t) < 0; });
    if (errExtra.some(function (t) { return stuTok.indexOf(t) >= 0; })) return false;

    var changed = getChangedCorrectTokens(errN, fixN);
    var fixOnly = fixTok.filter(function (t) { return errTok.indexOf(t) < 0; });

    // 连续子短语：reason for ⊂ the main reason for；at low ⊂ at low prices
    if (containsPhrase(fixN, a) && !containsPhrase(errN, a)) {
      if (changed.some(function (c) {
        return stuTok.indexOf(c) >= 0 || containsPhrase(a, c) || a === c;
      })) return true;
      if (fixOnly.some(function (t) { return stuTok.indexOf(t) >= 0; })) return true;
      if (stuTok.length >= 2) return true;
    }

    // 去掉轻词后相等：experience in person ≈ experience it in person
    var stuCore = stripLightWords(stuTok);
    var fixCore = stripLightWords(fixTok);
    var errCore = stripLightWords(errTok);
    if (stuCore.length && fixCore.join(" ") === stuCore.join(" ")) return true;
    if (stuCore.length >= 2 && containsPhrase(fixCore.join(" "), stuCore.join(" "))) {
      if (stuCore.join(" ") !== errCore.join(" ")) return true;
    }

    // 学生词按序出现在修正里，且覆盖了至少一个「新增/改动」词
    if (stuTok.length >= 2 && tokensInOrder(fixTok, stuTok)) {
      if (fixOnly.some(function (t) { return stuTok.indexOf(t) >= 0; })) return true;
      if (changed.some(function (c) { return stuTok.indexOf(c) >= 0; })) return true;
    }

    return false;
  }

  function isAnswerCorrect(studentText, checkpoint) {
    var studentRaw = String(studentText || "").trim();
    if (!studentRaw || !checkpoint) return false;

    var a = stripQuotes(normalizeForCompare(studentRaw));
    var expectedFull = String(checkpoint.answer || "").trim();
    var b = stripQuotes(normalizeForCompare(expectedFull));
    if (a && b && a === b) return true;

    var localFix = getExpectedLocalFix(checkpoint);
    var fixN = stripQuotes(normalizeForCompare(localFix));
    var errN = stripQuotes(normalizeForCompare(checkpoint.highlight || ""));

    if (fixN && a === fixN) return true;
    // 标点局部：", so they dare not" 与学生多/少空格
    if (fixN && a.replace(/\s*,\s*/g, ", ") === fixN.replace(/\s*,\s*/g, ", ")) return true;
    if (fixN && isAcceptableLocalAnswer(a, localFix, checkpoint.highlight || "")) return true;

    // 无 localFix 时：学生写了「, + highlight」且参考整句含该写法
    if (errN && a && b) {
      var commaPrefixed = a.replace(/\s+/g, " ");
      if (/^[,，;；]\s*/.test(commaPrefixed)) {
        var rest = commaPrefixed.replace(/^[,，;；]\s*/, "");
        if (rest === errN || containsPhrase(errN, rest) || rest === errN) {
          var hi = String(checkpoint.highlight || "");
          if (b.indexOf(", " + errN) >= 0 || b.indexOf("," + errN) >= 0 ||
              (expectedFull && (expectedFull.indexOf(", " + hi) >= 0 || expectedFull.indexOf("," + hi) >= 0))) {
            return true;
          }
        }
      }
    }

    if (errN && fixN) {
      var changedTokens = getChangedCorrectTokens(errN, fixN);
      if (changedTokens.indexOf(a) >= 0) return true;
      if (changedTokens.length && a === changedTokens.join(" ")) return true;
      if (a && containsAsWord(fixN, a) && !containsAsWord(errN, a)) return true;
      if (a && containsPhrase(fixN, a) && !containsPhrase(errN, a) && tokenizeForCompare(a).length >= 1) {
        return true;
      }
    }

    if (a && b && containsAsWord(b, a) && errN && !containsAsWord(errN, a) && a.length >= 2) {
      return true;
    }
    if (a && b && containsPhrase(b, a) && errN && !containsPhrase(errN, a) && tokenizeForCompare(a).length >= 2) {
      return true;
    }

    if (fixN && a.indexOf(fixN) >= 0) {
      // 学生仍带着错误侧多出的词（如 except for 对 except）→ 不算对
      var errExtra = tokenizeForCompare(errN).filter(function (t) {
        return tokenizeForCompare(fixN).indexOf(t) < 0;
      });
      var stillHasError = errExtra.some(function (t) {
        return tokenizeForCompare(a).indexOf(t) >= 0;
      });
      if (!stillHasError) {
        if (a.length <= fixN.length + 8) return true;
        if (!errN) return true;
        if (errN === fixN) return true;
        if (a.indexOf(errN) < 0) return true;
        if (containsAsWord(a, fixN) && !containsAsWord(a, errN)) return true;
      }
    }

    var base = String(checkpoint.baseText || checkpoint.originalSentence || "");
    var highlight = String(checkpoint.highlight || "");
    if (localFix && highlight && base && findHighlightRange(base, highlight)) {
      var applied = base.replace(new RegExp(escapeRegex(highlight), "i"), localFix);
      if (stripQuotes(normalizeForCompare(applied)) === a) return true;
    }

    if (a && errN && fixN && tokenizeForCompare(errN).length >= 1) {
      var errTokens = tokenizeForCompare(errN);
      var fixTokens = tokenizeForCompare(fixN);
      if (errTokens.length === fixTokens.length) {
        var i;
        for (i = 0; i < errTokens.length; i++) {
          if (errTokens[i] !== fixTokens[i]) {
            var trial = errTokens.slice();
            trial[i] = a;
            if (trial.join(" ") === fixTokens.join(" ")) return true;
          }
        }
      }
    }

    return false;
  }

  /** 明显不可用的 AI 检查点（标点、空、与原文相同等） */
  function isUsableCheckpoint(cp) {
    if (!cp) return false;
    var highlight = String(cp.highlight || cp.matchedText || "").trim();
    var corrected = String(cp.answer || cp.rawCorrected || cp.corrected || "").trim();
    var original = String(cp.originalSentence || "").trim();
    if (!highlight) return false;
    if (!/[A-Za-z]/.test(highlight)) return false;
    if (highlight.length < 2) return false;
    if (/^[,.;:!?'"“”‘’\-—…]+$/.test(highlight)) return false;
    if (corrected && original && normalizeForCompare(corrected) === normalizeForCompare(original)) {
      return false;
    }
    return true;
  }

  function formatReferenceHtml(checkpoint, escapeHtmlFn) {
    var esc = escapeHtmlFn || function (s) {
      return String(s || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    };
    var local = getExpectedLocalFix(checkpoint);
    var full = String(checkpoint && checkpoint.answer || "").trim();
    var parts = [];
    if (local) {
      parts.push("<strong>应改成</strong><div>" + esc(local) + "</div>");
    }
    if (full && normalizeForCompare(full) !== normalizeForCompare(local)) {
      parts.push("<strong" + (local ? ' style="margin-top:8px;display:block;"' : "") + ">整句参考</strong><div>" + esc(full) + "</div>");
    } else if (full && !local) {
      parts.push("<strong>参考修改</strong><div>" + esc(full) + "</div>");
    }
    return parts.join("");
  }

  return {
    normalizeForCompare: normalizeForCompare,
    stripQuotes: stripQuotes,
    tokenizeForCompare: tokenizeForCompare,
    containsAsWord: containsAsWord,
    containsPhrase: containsPhrase,
    getChangedCorrectTokens: getChangedCorrectTokens,
    extractLocalReplacement: extractLocalReplacement,
    extractPunctuationLocalFix: extractPunctuationLocalFix,
    applyFixToBase: applyFixToBase,
    findHighlightRange: findHighlightRange,
    escapeRegex: escapeRegex,
    getExpectedLocalFix: getExpectedLocalFix,
    isAcceptableLocalAnswer: isAcceptableLocalAnswer,
    isAnswerCorrect: isAnswerCorrect,
    isUsableCheckpoint: isUsableCheckpoint,
    formatReferenceHtml: formatReferenceHtml
  };
});

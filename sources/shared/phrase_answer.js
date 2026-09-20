/**
 * 词伙/短语答案的「多写法」支持 —— 三个前端共用（词伙学习页、词伙测试页、主站模块练习）。
 *
 * 背景：词伙题库里有 11 条用 `/` 表示「两种说法都行」：
 *   climb steadily/solidly · continue to increase / soar · remain stable/steady
 *   in the final phase/stage · curb crime / deter crime · consumer goods /products
 *   digital/online dating · dip/drop to only 2.5% · a modest dip/drop over the last decade
 *   be ethically wrong / theoretically wrong · the elderly / the senior population
 *
 * 数据没有拆开，旧逻辑把整串当成唯一答案：「a/b」被规范化成「a b」，
 * 学生写 a 或 b **都判错** —— 这些题永远拿不到分（线上有 6 次 0 分提交）。
 *
 * 现在按 `/` 拆成多个可接受答案，**任一命中即算对**。这是纯放宽，不会误伤：
 * 原来能过的答案现在依然能过，只是多加了几种合法写法。
 *
 * 用法（浏览器）：本文件用 `<script>` 先于 modules.js / game.js 加载，
 * 直接挂 `phraseXxx` 全局函数；node 下用 `module.exports` 取同一套实现。
 */
(function (root) {
  var factory = function () {
    /** 规范化：小写、去标点、连字符与斜杠按空格处理、压缩空格。 */
    function phraseNormalize(s) {
      return String(s || '').toLowerCase()
        .replace(/\s+/g, ' ')
        .replace(/[\/\(\)]/g, ' ')
        .replace(/[.,;:!?'\u2018\u2019\u201c\u201d\u2026]/g, '')
        .replace(/[\-\u2013\u2014]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    }

    /**
     * 拆出题目的「主写法」——`/` 两侧各算一种说法。**未规范化**，用于展示。
     * 无 `/` 时返回 `[原串]`。
     *
     * `/` 在题库里有两种形态，都要支持：
     *   A. 贴在词里 —— `dip/drop to only 2.5%`、`climb steadily/solidly`、`consumer goods /products`
     *      → 把带 `/` 的词换成左右两侧，各生成一种写法（`/products` 这种单侧空的，
     *        就取「斜杠前那部分」与「省掉它前面那个词再接上」两种，
     *        `consumer goods /products` → `consumer goods` / `consumer products`）。
     *   B. 独立成词（两侧有空格）—— `curb crime / deter crime`、`the elderly / the senior population`
     *      → 左右两段各自就是一种写法。
     */
    function phraseVariants(answer) {
      var raw = String(answer || '');
      var tokens = raw.trim().split(/\s+/).filter(Boolean);
      var slashIdx = -1;
      for (var i = 0; i < tokens.length; i++) {
        if (tokens[i].indexOf('/') >= 0) { slashIdx = i; break; }
      }
      if (slashIdx < 0) return raw ? [raw] : [];

      var tok = tokens[slashIdx];
      var prefix = tokens.slice(0, slashIdx);
      var suffix = tokens.slice(slashIdx + 1);
      var out = [];
      var seen = {};
      function add(form) {
        form = String(form || '').replace(/\s+/g, ' ').trim();
        if (form && !seen[form]) { seen[form] = 1; out.push(form); }
      }

      if (tok === '/') {
        add(prefix.join(' '));   // 形态 B：`X / Y`
        add(suffix.join(' '));
        return out;
      }

      // 形态 A：`a/b`、`a/`、`/b`
      var halves = tok.split('/');
      var a = halves[0];
      var b = halves.slice(1).join('/');
      if (a && b) {
        add(prefix.concat([a], suffix).join(' '));
        add(prefix.concat([b], suffix).join(' '));
      } else if (!a && b) {
        add(prefix.join(' '));
        add(prefix.slice(0, -1).concat([b], suffix).join(' '));
      } else if (a && !b) {
        add(prefix.concat([a], suffix).join(' '));
        add(prefix.concat([a], suffix.slice(1)).join(' '));
      }
      return out;
    }

    /**
     * 一个标准答案可接受的全部写法（已规范化）。
     *
     * = 「主写法」+ 「整串去掉 `/` 原样」（免得惩罚照着题目打的学生）
     *   + 少量更宽松的补充（两侧词数不等时，把短的一侧接上长的一侧的引导词，
     *     如 `be ethically wrong / theoretically wrong` → `be theoretically wrong`）。
     * 生成过程只会**多**出可接受写法、不会收窄，所以是纯放宽。
     */
    function phraseAcceptList(answer) {
      var raw = String(answer || '');
      var out = [];
      var seen = {};

      function push(form) {
        [form, form.replace(/\([^)]*\)/g, ' ')].forEach(function (f) {
          var n = phraseNormalize(f);
          if (n && !seen[n]) { seen[n] = 1; out.push(n); }
        });
      }

      phraseVariants(raw).forEach(push);
      push(raw); // 老写法：整串原样

      // 两侧词数不等时补一个「带引导词」的写法，例：
      // `be ethically wrong / theoretically wrong` → `be theoretically wrong`
      // `continue to increase / soar`             → `continue to soar`
      var tokens = raw.trim().split(/\s+/).filter(Boolean);
      var slashIdx = tokens.indexOf('/');
      if (slashIdx > 0) {
        var leftW = tokens.slice(0, slashIdx);
        var rightW = tokens.slice(slashIdx + 1);
        var diff = leftW.length - rightW.length;
        var head, shortW;
        if (diff > 0) { head = leftW.slice(0, diff); shortW = rightW; }
        else if (diff < 0) { head = rightW.slice(0, -diff); shortW = leftW; }
        // 引导词已经出现在短侧开头时不补，避免 `the the elderly` 这种废话
        if (head && shortW.length && shortW[0] !== head[head.length - 1]) {
          push(head.concat(shortW).join(' '));
        }
      }
      return out;
    }

    /** 学生答案是否命中任一可接受写法。 */
    function phraseMatchesAny(user, answer) {
      var u = phraseNormalize(user);
      if (!u) return false;
      var list = phraseAcceptList(answer);
      for (var i = 0; i < list.length; i++) {
        if (list[i] === u) return true;
      }
      return false;
    }

    /** `phraseMatchesAny` 的别名，语义更直白。 */
    var phraseIsCorrect = phraseMatchesAny;

    /** 展示用：`a/b` → 「a 或 b」，让学生知道两种说法都算对。 */
    function phraseDisplayAnswer(answer) {
      var v = phraseVariants(answer);
      return v.length > 1 ? v.join(' 或 ') : String(answer || '');
    }

    /** 主答案（第一个写法）：选词题的词块只按它出，避免出现 `steadily/solidly` 这种块。 */
    function phrasePrimaryAnswer(answer) {
      var parts = String(answer || '').split('/')
        .map(function (s) { return s.trim(); })
        .filter(Boolean);
      return parts.length ? parts[0] : String(answer || '');
    }

    /** 每个写法拆词后排序去重的词集合（选词题按「词多集相等」判定）。 */
    function phraseAcceptedWordSets(answer) {
      var out = [];
      var seen = {};
      String(answer || '').split('/').forEach(function (part) {
        var ws = part.trim().split(/\s+/).map(phraseNormalize).filter(Boolean).sort();
        if (!ws.length) return;
        var key = ws.join(' ');
        if (seen[key]) return;
        seen[key] = 1;
        out.push(ws);
      });
      return out;
    }

    return {
      phraseNormalize: phraseNormalize,
      phraseVariants: phraseVariants,
      phraseAcceptList: phraseAcceptList,
      phraseMatchesAny: phraseMatchesAny,
      phraseIsCorrect: phraseIsCorrect,
      phraseDisplayAnswer: phraseDisplayAnswer,
      phrasePrimaryAnswer: phrasePrimaryAnswer,
      phraseAcceptedWordSets: phraseAcceptedWordSets
    };
  };

  var api = factory();
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }
  // 浏览器：挂全局，页面里的 `phraseXxx(...)` 直接可用（无构建步骤）
  var g = root || (typeof globalThis !== 'undefined' ? globalThis : {});
  for (var k in api) {
    if (Object.prototype.hasOwnProperty.call(api, k)) g[k] = api[k];
  }
  g.PhraseAnswer = api;
})(typeof window !== 'undefined' ? window : this);

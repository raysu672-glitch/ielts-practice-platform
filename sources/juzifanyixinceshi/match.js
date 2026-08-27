(function (root) {
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

  function isChineseMatch(user, answer) {
    var ua = normalizeChinese(user);
    var ca = normalizeChinese(answer);
    return ua.length > 0 && ua === ca;
  }

  var api = { normalizeChinese: normalizeChinese, isChineseMatch: isChineseMatch };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }
  root.TranslateMatch = api;
})(typeof window !== 'undefined' ? window : globalThis);

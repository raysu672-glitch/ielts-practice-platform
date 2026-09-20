(function () {
  var statusEl = document.getElementById("status");
  var appEl = document.getElementById("app");
  var catalogEl = document.getElementById("catalog");
  var playerBox = document.getElementById("playerBox");
  var playerPlaceholder = document.getElementById("playerPlaceholder");
  var player = document.getElementById("player");
  var watermark = document.getElementById("watermark");
  var nowPlaying = document.getElementById("nowPlaying");
  var who = document.getElementById("who");
  var homeLink = document.getElementById("homeLink");

  var subjects = [];
  var currentUserLabel = "";
  var currentCourseId = null;
  var collapsed = {};
  var toggleAllBtn = null;

  var isEmbed = new URLSearchParams(location.search).get("embed") === "1";
  if (isEmbed) {
    document.body.classList.add("embed");
    homeLink.hidden = true;
  }

  function showStatus(text, isError) {
    statusEl.hidden = false;
    statusEl.textContent = text;
    statusEl.className = "msg" + (isError ? " error" : "");
  }

  function api(path) {
    return fetch(path, { credentials: "include" }).then(function (res) {
      return res.json().then(function (body) {
        return { ok: res.ok, status: res.status, body: body };
      });
    });
  }

  function loadMe() {
    if (isEmbed) return api("/api/auth/me?role=student");
    return api("/api/auth/me?role=student").then(function (result) {
      if (result.status === 401) return api("/api/auth/me?role=teacher");
      return result;
    });
  }

  function viewerLabel(data) {
    if (!data) return "";
    if (data.role === "student" && data.student) {
      return (data.student.student_id || "") + " " + (data.student.name || "");
    }
    if (data.role === "teacher" && data.teacher) {
      return "教师 " + (data.teacher.teacher_id || data.teacher.name || "");
    }
    return "";
  }

  function renderCourses(nextSubjects) {
    subjects = nextSubjects || [];
    var hasAny = subjects.some(function (subject) { return (subject.courses || []).length; });
    if (!hasAny) {
      appEl.hidden = true;
      showStatus("暂时还没有录播课", false);
      return;
    }
    statusEl.hidden = true;
    appEl.hidden = false;
    renderCatalog();
  }

  function isCollapsed(subject) {
    if (Object.prototype.hasOwnProperty.call(collapsed, subject.id)) {
      return collapsed[subject.id];
    }
    // 没有课的科目默认收起，减少目录长度
    return !(subject.courses || []).length;
  }

  function refreshToggleAllLabel() {
    if (!toggleAllBtn) return;
    var anyExpanded = subjects.some(function (s) { return !isCollapsed(s); });
    toggleAllBtn.textContent = anyExpanded ? "全部收起" : "全部展开";
  }

  function renderCatalog() {
    catalogEl.innerHTML = "";

    var toolbar = document.createElement("div");
    toolbar.className = "catalog-toolbar";
    toggleAllBtn = document.createElement("button");
    toggleAllBtn.type = "button";
    toggleAllBtn.className = "toggle-all";
    toggleAllBtn.addEventListener("click", function () {
      var anyExpanded = subjects.some(function (s) { return !isCollapsed(s); });
      // anyExpanded 为真 → 按钮是「全部收起」→ 把所有科目设为收起
      subjects.forEach(function (s) { collapsed[s.id] = anyExpanded; });
      renderCatalog();
    });
    refreshToggleAllLabel();
    toolbar.appendChild(toggleAllBtn);
    catalogEl.appendChild(toolbar);

    subjects.forEach(function (subject) {
      var courses = subject.courses || [];
      var block = document.createElement("section");
      block.className = "subject-block" + (isCollapsed(subject) ? " collapsed" : "");

      var head = document.createElement("button");
      head.type = "button";
      head.className = "subject-head";
      var chevron = document.createElement("span");
      chevron.className = "chevron";
      var nameSpan = document.createElement("span");
      nameSpan.className = "name";
      nameSpan.textContent = subject.name || subject.id;
      var countSpan = document.createElement("span");
      countSpan.className = "count";
      countSpan.textContent = courses.length + " 节";
      head.appendChild(chevron);
      head.appendChild(nameSpan);
      head.appendChild(countSpan);
      head.addEventListener("click", function () {
        if (isCollapsed(subject)) {
          collapsed[subject.id] = false;
        } else {
          collapsed[subject.id] = true;
        }
        block.classList.toggle("collapsed", isCollapsed(subject));
        head.setAttribute("aria-expanded", String(!isCollapsed(subject)));
        refreshToggleAllLabel();
      });
      head.setAttribute("aria-expanded", String(!isCollapsed(subject)));
      block.appendChild(head);

      var list = document.createElement("div");
      list.className = "course-list";
      if (!courses.length) {
        var empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "暂无课程";
        list.appendChild(empty);
      }
      courses.forEach(function (course) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "card";
        btn.setAttribute("data-course-id", course.id || "");
        var body = document.createElement("div");
        var title = document.createElement("strong");
        title.textContent = course.title || course.id;
        body.appendChild(title);
        var meta = document.createElement("div");
        meta.className = "meta";
        meta.textContent = course.duration || "点击播放";
        body.appendChild(meta);
        if (course.summary) {
          var summary = document.createElement("div");
          summary.className = "summary";
          summary.textContent = course.summary;
          body.appendChild(summary);
        }
        var play = document.createElement("span");
        play.className = "play";
        play.textContent = course.id === currentCourseId ? "播放中" : "播放";
        btn.appendChild(body);
        btn.appendChild(play);
        btn.addEventListener("click", function () {
          playCourse(course, subject);
        });
        list.appendChild(btn);
      });
      block.appendChild(list);
      catalogEl.appendChild(block);
    });
  }

  function playCourse(course, subject) {
    var label = (subject && subject.name ? subject.name + " · " : "") + (course.title || "");
    currentCourseId = course.id;
    renderCatalog();
    playerPlaceholder.style.display = "none";
    playerBox.classList.add("on");
    nowPlaying.style.display = "block";
    nowPlaying.textContent = "正在加载：" + label;
    api("/api/luboke/courses/" + encodeURIComponent(course.id) + "/play-url").then(function (result) {
      var playUrl = result.body && result.body.data && result.body.data.play_url;
      if (!result.ok || !playUrl) {
        var err = (result.body && result.body.error && result.body.error.message) || "无法获取播放地址";
        nowPlaying.textContent = err;
        return;
      }
      watermark.textContent = currentUserLabel;
      player.src = playUrl;
      nowPlaying.innerHTML = "正在播放：<strong></strong>";
      nowPlaying.querySelector("strong").textContent = label;
      var playPromise = player.play();
      if (playPromise && playPromise.catch) playPromise.catch(function () {});
    }).catch(function () {
      nowPlaying.textContent = "网络异常，请稍后重试";
    });
  }

  player.addEventListener("contextmenu", function (event) {
    event.preventDefault();
  });

  loadMe().then(function (result) {
    if (result.status === 401 || !result.body || !result.body.data) {
      showStatus("请先用学号登录练习平台，然后打开录播课。", true);
      return;
    }
    currentUserLabel = viewerLabel(result.body.data).trim();
    if (who) who.textContent = currentUserLabel ? ("当前账号：" + currentUserLabel) : "已登录";
    return api("/api/luboke/courses").then(function (listResult) {
      if (listResult.status === 503) {
        showStatus((listResult.body && listResult.body.error && listResult.body.error.message) || "录播课尚未配置", true);
        return;
      }
      if (!listResult.ok) {
        showStatus((listResult.body && listResult.body.error && listResult.body.error.message) || "无法加载课表", true);
        return;
      }
      renderCourses((listResult.body && listResult.body.data && listResult.body.data.subjects) || []);
    });
  }).catch(function () {
    showStatus("网络异常，请刷新页面", true);
  });
})();

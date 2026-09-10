(function () {
  var statusEl = document.getElementById("status");
  var chipsEl = document.getElementById("chips");
  var listEl = document.getElementById("list");
  var subjects = [];
  var currentSubject = "all";
  var playerBox = document.getElementById("playerBox");
  var player = document.getElementById("player");
  var watermark = document.getElementById("watermark");
  var nowPlaying = document.getElementById("nowPlaying");
  var who = document.getElementById("who");
  var homeLink = document.getElementById("homeLink");
  var currentUserLabel = "";

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
      chipsEl.hidden = true;
      listEl.hidden = true;
      showStatus("暂时还没有录播课", false);
      return;
    }
    statusEl.hidden = true;
    chipsEl.hidden = false;
    listEl.hidden = false;
    renderChips();
    renderList();
  }

  function renderChips() {
    chipsEl.innerHTML = "";
    function addChip(id, label) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chip" + (currentSubject === id ? " active" : "");
      btn.textContent = label;
      btn.addEventListener("click", function () {
        currentSubject = id;
        renderChips();
        renderList();
      });
      chipsEl.appendChild(btn);
    }
    addChip("all", "全部");
    subjects.forEach(function (subject) {
      addChip(subject.id, subject.name || subject.id);
    });
  }

  function renderList() {
    listEl.innerHTML = "";
    var visible = currentSubject === "all"
      ? subjects
      : subjects.filter(function (subject) { return subject.id === currentSubject; });
    visible.forEach(function (subject) {
      var block = document.createElement("section");
      block.className = "subject-block";
      var heading = document.createElement("h2");
      heading.textContent = subject.name || subject.id;
      block.appendChild(heading);
      var courses = subject.courses || [];
      if (!courses.length) {
        var empty = document.createElement("p");
        empty.className = "empty";
        empty.textContent = "这个科目还没有课";
        block.appendChild(empty);
      }
      courses.forEach(function (course) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "card";
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
        play.textContent = "播放";
        btn.appendChild(body);
        btn.appendChild(play);
        btn.addEventListener("click", function () {
          Array.prototype.forEach.call(listEl.querySelectorAll(".card"), function (el) {
            el.classList.toggle("active", el === btn);
          });
          playCourse(course, subject);
        });
        block.appendChild(btn);
      });
      listEl.appendChild(block);
    });
  }

  function playCourse(course, subject) {
    var label = (subject && subject.name ? subject.name + " · " : "") + (course.title || "");
    nowPlaying.style.display = "block";
    nowPlaying.textContent = "正在加载：" + label;
    api("/api/luboke/courses/" + encodeURIComponent(course.id) + "/play-url").then(function (result) {
      var playUrl = result.body && result.body.data && result.body.data.play_url;
      if (!result.ok || !playUrl) {
        var err = (result.body && result.body.error && result.body.error.message) || "无法获取播放地址";
        nowPlaying.textContent = err;
        return;
      }
      playerBox.classList.add("on");
      watermark.textContent = currentUserLabel;
      player.src = playUrl;
      nowPlaying.textContent = "正在播放：" + label;
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

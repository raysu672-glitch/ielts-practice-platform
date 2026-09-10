(function () {
  var statusEl = document.getElementById("status");
  var appEl = document.getElementById("app");
  var subjectsEl = document.getElementById("subjects");
  var saveMsg = document.getElementById("saveMsg");
  var catalog = { subjects: [] };
  var files = [];

  function api(path, options) {
    return fetch(path, Object.assign({ credentials: "include" }, options || {})).then(function (res) {
      return res.json().then(function (body) {
        return { ok: res.ok, status: res.status, body: body };
      });
    });
  }

  function showStatus(text, isError) {
    statusEl.hidden = false;
    statusEl.textContent = text;
    statusEl.className = "msg" + (isError ? " error" : "");
  }

  function optionList(selected) {
    var html = '<option value="">请选择 OSS 里的视频</option>';
    files.forEach(function (key) {
      var picked = key === selected ? " selected" : "";
      html += "<option value=\"" + escapeAttr(key) + "\"" + picked + ">" + escapeHtml(key.replace(/^courses\//, "")) + "</option>";
    });
    if (selected && files.indexOf(selected) < 0) {
      html += "<option value=\"" + escapeAttr(selected) + "\" selected>" + escapeHtml(selected) + "（不在列表中）</option>";
    }
    return html;
  }

  function escapeHtml(text) {
    return String(text || "").replace(/[&<>"']/g, function (ch) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch];
    });
  }

  function escapeAttr(text) {
    return escapeHtml(text);
  }

  function readForm() {
    var next = { subjects: [] };
    Array.prototype.forEach.call(subjectsEl.querySelectorAll("[data-subject]"), function (block) {
      var nameInput = block.querySelector("[name=subject_name]");
      var subject = {
        id: block.getAttribute("data-subject") || "",
        name: (nameInput && nameInput.value.trim()) || block.getAttribute("data-name") || "",
        courses: []
      };
      Array.prototype.forEach.call(block.querySelectorAll("[data-course]"), function (row) {
        subject.courses.push({
          id: row.getAttribute("data-id") || "",
          title: row.querySelector("[name=title]").value.trim(),
          duration: row.querySelector("[name=duration]").value.trim(),
          summary: row.querySelector("[name=summary]").value.trim(),
          oss_key: row.querySelector("[name=oss_key]").value.trim()
        });
      });
      next.subjects.push(subject);
    });
    return next;
  }

  function addSubject() {
    var input = document.getElementById("newSubjectName");
    var name = (input && input.value.trim()) || "";
    if (!name) {
      saveMsg.textContent = "请先填写新科目名称";
      if (input) input.focus();
      return;
    }
    catalog = readForm();
    var exists = catalog.subjects.some(function (s) { return (s.name || "") === name; });
    if (exists) {
      saveMsg.textContent = "已有同名科目";
      return;
    }
    catalog.subjects.push({ id: "", name: name, courses: [] });
    if (input) input.value = "";
    saveMsg.textContent = "";
    render();
  }

  function removeSubject(index) {
    catalog = readForm();
    var subject = catalog.subjects[index];
    if (!subject) return;
    var count = (subject.courses || []).length;
    var tip = count
      ? "删除科目「" + (subject.name || "") + "」会一并去掉其中 " + count + " 节课，确定吗？"
      : "确定删除科目「" + (subject.name || "") + "」吗？";
    if (!window.confirm(tip)) return;
    catalog.subjects.splice(index, 1);
    render();
  }

  function removeLesson(subjectIndex, lessonIndex) {
    catalog = readForm();
    if (!catalog.subjects[subjectIndex]) return;
    catalog.subjects[subjectIndex].courses.splice(lessonIndex, 1);
    render();
  }

  function render() {
    subjectsEl.innerHTML = "";
    if (!catalog.subjects.length) {
      var empty = document.createElement("p");
      empty.className = "sub";
      empty.textContent = "还没有科目。上方输入名称后点「添加科目」。";
      subjectsEl.appendChild(empty);
      return;
    }
    catalog.subjects.forEach(function (subject, subjectIndex) {
      var block = document.createElement("section");
      block.className = "subject";
      block.setAttribute("data-subject", subject.id || "");
      block.setAttribute("data-name", subject.name || "");

      var head = document.createElement("div");
      head.className = "subject-head";
      head.innerHTML =
        "<div class=\"grow\"><label>科目名称</label><input name=\"subject_name\" placeholder=\"例如：听力 / 长难句\"></div>" +
        "<button class=\"danger\" type=\"button\" data-remove-subject>删除科目</button>";
      head.querySelector("[name=subject_name]").value = subject.name || "";
      head.querySelector("[data-remove-subject]").addEventListener("click", function () {
        removeSubject(subjectIndex);
      });
      block.appendChild(head);

      (subject.courses || []).forEach(function (course, index) {
        var row = document.createElement("div");
        row.className = "lesson";
        row.setAttribute("data-course", "1");
        row.setAttribute("data-id", course.id || "");
        row.innerHTML =
          "<label>课名</label><input name=\"title\" placeholder=\"例如：1-1 如何阅读长难句\">" +
          "<div class=\"row\"><div><label>时长</label><input name=\"duration\" placeholder=\"例如：35分钟\"></div>" +
          "<div><label>视频文件</label><select name=\"oss_key\"></select></div></div>" +
          "<label>课程明细</label><textarea name=\"summary\" placeholder=\"这节课讲什么、适合谁看\"></textarea>" +
          "<div class=\"actions\"><button class=\"danger\" type=\"button\" data-remove>删除这节课</button></div>";
        row.querySelector("[name=title]").value = course.title || "";
        row.querySelector("[name=duration]").value = course.duration || "";
        row.querySelector("[name=summary]").value = course.summary || "";
        row.querySelector("[name=oss_key]").innerHTML = optionList(course.oss_key || "");
        row.querySelector("[data-remove]").addEventListener("click", function () {
          removeLesson(subjectIndex, index);
        });
        block.appendChild(row);
      });

      var addBtn = document.createElement("button");
      addBtn.type = "button";
      addBtn.className = "ghost";
      addBtn.textContent = "给这个科目加一节课";
      addBtn.addEventListener("click", function () {
        catalog = readForm();
        var current = catalog.subjects[subjectIndex];
        if (!current) return;
        current.courses.push({ id: "", title: "", duration: "", summary: "", oss_key: "" });
        render();
      });
      block.appendChild(addBtn);
      subjectsEl.appendChild(block);
    });
  }

  document.getElementById("addSubjectBtn").addEventListener("click", addSubject);
  document.getElementById("newSubjectName").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      addSubject();
    }
  });

  document.getElementById("saveBtn").addEventListener("click", function () {
    saveMsg.textContent = "正在保存…";
    var payload = readForm();
    if (!payload.subjects.length) {
      saveMsg.textContent = "请至少添加一个科目";
      return;
    }
    var blank = payload.subjects.some(function (s) { return !(s.name || "").trim(); });
    if (blank) {
      saveMsg.textContent = "科目名称不能为空";
      return;
    }
    api("/api/luboke/catalog", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (result) {
      if (!result.ok) {
        saveMsg.textContent = (result.body && result.body.error && result.body.error.message) || "保存失败";
        return;
      }
      catalog = result.body.data;
      render();
      saveMsg.textContent = "已保存，学生刷新「录播课」就能看到。";
    }).catch(function () {
      saveMsg.textContent = "网络异常";
    });
  });

  api("/api/auth/me?role=teacher").then(function (result) {
    if (result.status === 401 || !result.body || !result.body.data) {
      showStatus("请先打开教师后台登录，再回到这个页面。", true);
      return;
    }
    return Promise.all([
      api("/api/luboke/courses"),
      api("/api/luboke/files")
    ]).then(function (pair) {
      var catalogResult = pair[0];
      var filesResult = pair[1];
      if (!catalogResult.ok) {
        showStatus((catalogResult.body && catalogResult.body.error && catalogResult.body.error.message) || "无法加载课表", true);
        return;
      }
      catalog = { subjects: (catalogResult.body.data && catalogResult.body.data.subjects) || [] };
      files = (filesResult.ok && filesResult.body.data && filesResult.body.data.files) || [];
      statusEl.hidden = true;
      appEl.hidden = false;
      render();
    });
  }).catch(function () {
    showStatus("网络异常，请刷新", true);
  });
})();

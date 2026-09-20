(function () {
  var statusEl = document.getElementById("status");
  var appEl = document.getElementById("app");
  var subjectsEl = document.getElementById("subjects");
  var saveMsg = document.getElementById("saveMsg");
  var catalog = { subjects: [] };
  var files = [];
  var batchSubjectIndex = null;
  var batchModalEl = document.getElementById("batchModal");
  var batchSearchEl = document.getElementById("batchSearch");
  var batchFilesEl = document.getElementById("batchFiles");
  var batchCountEl = document.getElementById("batchCount");
  var batchTargetNameEl = document.getElementById("batchTargetName");
  var batchMatchLineEl = document.getElementById("batchMatchLine");
  var batchChecked = {};
  var filesAlready = [];
  var collapsedSubjects = {};

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

  // 折叠状态用「科目 id（没有则用名称）」作 key，render 重绘后仍能保持
  function subjectKey(subject) {
    if (subject.id) return "id:" + subject.id;
    return "name:" + (subject.name || "");
  }

  function isSubjectCollapsed(subject) {
    var key = subjectKey(subject);
    if (Object.prototype.hasOwnProperty.call(collapsedSubjects, key)) {
      return collapsedSubjects[key];
    }
    return false;
  }

  function updateToggleAllLabel() {
    var btn = document.getElementById("toggleAllSubjectsBtn");
    if (!btn) return;
    var anyExpanded = catalog.subjects.some(function (s) { return !isSubjectCollapsed(s); });
    btn.textContent = anyExpanded ? "全部收起" : "全部展开";
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

  function refreshBatchMatch() {
    var q = (batchSearchEl.value || "").trim().toLowerCase();
    var matched = files.filter(function (key) {
      return !q || key.toLowerCase().indexOf(q) >= 0;
    });
    if (!matched.length) {
      batchMatchLineEl.className = "match-line warn";
      batchMatchLineEl.textContent = "没有匹配的视频，请确认视频已上传到 OSS 的 courses 文件夹。";
      batchFilesEl.innerHTML = "<div class=\"batch-empty\">没有可添加的视频</div>";
      batchCountEl.textContent = "已选 0 个";
      return;
    }
    batchMatchLineEl.className = "match-line";
    batchMatchLineEl.textContent = "已上传 " + matched.length + " 个视频，勾选后点「添加」。";
    batchFilesEl.innerHTML = "";

    var groups = {};
    var order = [];
    matched.forEach(function (key) {
      var rel = key.replace(/^courses\//, "");
      var idx = rel.lastIndexOf("/");
      var folder = idx >= 0 ? rel.slice(0, idx) : "(根目录)";
      var base = idx >= 0 ? rel.slice(idx + 1) : rel;
      if (!groups[folder]) {
        groups[folder] = [];
        order.push(folder);
      }
      groups[folder].push({ key: key, base: base });
    });

    order.forEach(function (folder) {
      var items = groups[folder];
      var head = document.createElement("label");
      head.className = "batch-group-head";
      var headCb = document.createElement("input");
      headCb.type = "checkbox";
      var headSpan = document.createElement("span");
      headSpan.textContent = folder;
      head.appendChild(headCb);
      head.appendChild(headSpan);
      var countSpan = document.createElement("span");
      countSpan.className = "group-count";
      countSpan.textContent = items.length + " 个视频";
      head.appendChild(countSpan);
      batchFilesEl.appendChild(head);

      var groupCbs = [];
      items.forEach(function (item) {
        var label = document.createElement("label");
        label.className = "batch-file";
        var cb = document.createElement("input");
        cb.type = "checkbox";
        cb.value = item.key;
        if (batchChecked[item.key]) cb.checked = true;
        var already = filesAlready.some(function (k) { return k === item.key; });
        var span = document.createElement("span");
        span.textContent = item.base;
        label.appendChild(cb);
        label.appendChild(span);
        if (already) {
          var tag = document.createElement("span");
          tag.className = "already-added";
          tag.textContent = "（已在课表中）";
          label.appendChild(tag);
        }
        cb.addEventListener("change", function () {
          if (cb.checked) {
            batchChecked[item.key] = true;
          } else {
            delete batchChecked[item.key];
          }
          syncGroupHead();
          updateBatchCount();
        });
        groupCbs.push(cb);
        batchFilesEl.appendChild(label);
      });

      function syncGroupHead() {
        var checkedCount = groupCbs.filter(function (cb) { return cb.checked; }).length;
        headCb.checked = checkedCount === groupCbs.length && groupCbs.length > 0;
        headCb.indeterminate = checkedCount > 0 && checkedCount < groupCbs.length;
      }

      headCb.addEventListener("change", function () {
        groupCbs.forEach(function (cb) {
          if (cb.checked !== headCb.checked) {
            cb.checked = headCb.checked;
            if (headCb.checked) {
              batchChecked[cb.value] = true;
            } else {
              delete batchChecked[cb.value];
            }
          }
        });
        updateBatchCount();
      });

      syncGroupHead();
    });

    updateBatchCount();
  }

  function updateBatchCount() {
    var n = Object.keys(batchChecked).length;
    batchCountEl.textContent = "已选 " + n + " 个";
  }

  function closeBatch() {
    batchModalEl.hidden = true;
    batchSubjectIndex = null;
    batchChecked = {};
  }

  function openBatch(subjectIndex) {
    catalog = readForm();
    var subject = catalog.subjects[subjectIndex];
    if (!subject) return;
    batchSubjectIndex = subjectIndex;
    filesAlready = [];
    subject.courses.forEach(function (course) {
      if (course.oss_key) filesAlready.push(course.oss_key);
    });
    batchTargetNameEl.textContent = subject.name || subject.id;
    batchSearchEl.value = "";
    batchChecked = {};
    batchModalEl.hidden = false;
    refreshBatchMatch();
    batchSearchEl.focus();
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
      block.className = "subject" + (isSubjectCollapsed(subject) ? " collapsed" : "");
      block.setAttribute("data-subject", subject.id || "");
      block.setAttribute("data-name", subject.name || "");

      var head = document.createElement("div");
      head.className = "subject-head";
      head.innerHTML =
        "<button class=\"collapse-toggle\" type=\"button\" data-toggle-subject aria-label=\"折叠或展开科目\"><span class=\"chevron\"></span></button>" +
        "<div class=\"grow\"><label>科目名称</label><input name=\"subject_name\" placeholder=\"例如：听力 / 长难句\"></div>" +
        "<span class=\"subject-count\"></span>" +
        "<button class=\"danger\" type=\"button\" data-remove-subject>删除科目</button>";
      head.querySelector("[name=subject_name]").value = subject.name || "";
      var countEl = head.querySelector(".subject-count");
      countEl.textContent = (subject.courses || []).length + " 节课";
      head.querySelector("[data-remove-subject]").addEventListener("click", function () {
        removeSubject(subjectIndex);
      });
      var toggleBtn = head.querySelector("[data-toggle-subject]");
      toggleBtn.setAttribute("aria-expanded", String(!isSubjectCollapsed(subject)));
      toggleBtn.addEventListener("click", function () {
        // 只切换样式，不整块重绘，避免丢失未保存的输入
        var next = !block.classList.contains("collapsed");
        collapsedSubjects[subjectKey(subject)] = next;
        block.classList.toggle("collapsed", next);
        toggleBtn.setAttribute("aria-expanded", String(!next));
        updateToggleAllLabel();
      });
      block.appendChild(head);

      var body = document.createElement("div");
      body.className = "subject-body";

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
        body.appendChild(row);
      });

      var addBtn = document.createElement("button");
      addBtn.type = "button";
      addBtn.className = "ghost";
      addBtn.textContent = "给这个科目加一节课";
      addBtn.addEventListener("click", function () {
        catalog = readForm();
        var current = catalog.subjects[subjectIndex];
        if (!current) return;
        collapsedSubjects[subjectKey(current)] = false;
        current.courses.push({ id: "", title: "", duration: "", summary: "", oss_key: "" });
        render();
      });
      body.appendChild(addBtn);

      var batchBtn = document.createElement("button");
      batchBtn.type = "button";
      batchBtn.className = "ghost";
      batchBtn.textContent = "批量添加";
      batchBtn.addEventListener("click", function () {
        openBatch(subjectIndex);
      });
      body.appendChild(batchBtn);

      block.appendChild(body);
      subjectsEl.appendChild(block);
    });
    updateToggleAllLabel();
  }

  document.getElementById("addSubjectBtn").addEventListener("click", addSubject);
  document.getElementById("newSubjectName").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      addSubject();
    }
  });

  document.getElementById("toggleAllSubjectsBtn").addEventListener("click", function () {
    catalog = readForm();
    var anyExpanded = catalog.subjects.some(function (s) { return !isSubjectCollapsed(s); });
    // anyExpanded 为真 → 按钮是「全部收起」→ 全部设为收起
    catalog.subjects.forEach(function (s) { collapsedSubjects[subjectKey(s)] = anyExpanded; });
    render();
  });

  document.getElementById("batchCancel").addEventListener("click", closeBatch);

  document.getElementById("batchCheckAll").addEventListener("click", function () {
    Array.prototype.forEach.call(batchFilesEl.querySelectorAll("input[type=checkbox]"), function (cb) {
      if (!filesAlready.some(function (k) { return k === cb.value; })) cb.checked = true;
      batchChecked[cb.value] = true;
    });
    updateBatchCount();
  });

  document.getElementById("batchCheckNone").addEventListener("click", function () {
    Array.prototype.forEach.call(batchFilesEl.querySelectorAll("input[type=checkbox]"), function (cb) {
      cb.checked = false;
    });
    batchChecked = {};
    updateBatchCount();
  });

  batchSearchEl.addEventListener("input", function () {
    refreshBatchMatch();
  });

  document.getElementById("batchConfirm").addEventListener("click", function () {
    if (batchSubjectIndex === null) return;
    var keys = Object.keys(batchChecked);
    if (!keys.length) {
      batchMatchLineEl.className = "match-line warn";
      batchMatchLineEl.textContent = "请先勾选要添加的视频";
      return;
    }
    catalog = readForm();
    var subject = catalog.subjects[batchSubjectIndex];
    if (!subject) {
      closeBatch();
      return;
    }
    var added = 0;
    var skipped = 0;
    keys.forEach(function (key) {
      var rel = key.replace(/^courses\//, "");
      var idx = rel.lastIndexOf("/");
      var base = idx >= 0 ? rel.slice(idx + 1) : rel;
      var title = base.replace(/\.[^.]+$/, "").trim() || base;
      if (filesAlready.some(function (k) { return k === key; })) {
        skipped += 1;
        return;
      }
      subject.courses.push({
        id: "",
        title: title,
        duration: "",
        summary: "",
        oss_key: key
      });
      added += 1;
    });
    closeBatch();
    render();
    saveMsg.textContent = "已加入 " + added + " 节课" + (skipped ? "，跳过 " + skipped + " 个已在课表中的视频" : "") + "，点「保存课表」后生效。";
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
    // 后端会丢弃没有视频文件的课程，这里先拦住，避免误删课程
    var missing = [];
    payload.subjects.forEach(function (s) {
      (s.courses || []).forEach(function (c) {
        if (!(c.oss_key || "").trim()) {
          missing.push((s.name || "") + " · " + (c.title || "（未命名）"));
        }
      });
    });
    if (missing.length) {
      saveMsg.textContent = "这些课没选视频文件，保存会丢失：" + missing.slice(0, 3).join("；")
        + (missing.length > 3 ? " 等 " + missing.length + " 节" : "");
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
      api("/api/luboke/catalog"),
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

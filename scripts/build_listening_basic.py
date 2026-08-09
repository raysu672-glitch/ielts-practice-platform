#!/usr/bin/env python3
"""Rebuild 听力基础词汇 module and patch shared listening UX (progress bars)."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCX = Path(r"d:/文档/听力/雅思听力基础词汇表1.docx")
LISTENING = ROOT / "sources" / "tinglidanciceshi" / "listening.html"
LISTENING_BASIC = ROOT / "sources" / "tinglidanciceshi" / "listening_basic.html"
INDEX = ROOT / "sources" / "tinglidanciceshi" / "index.html"
LOCAL_SERVER = ROOT / "scripts" / "local_server.py"

GROUP_BTN_CSS = """
        /* 分组按钮 */
        .group-btn {
            position: relative;
            overflow: hidden;
            background: var(--surface);
            border: 1.5px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 10px 6px;
            font-family: inherit;
            font-size: .85rem;
            font-weight: 600;
            color: var(--text-primary);
            cursor: pointer;
            transition: border-color var(--transition), transform var(--transition), box-shadow var(--transition);
            z-index: 0;
            min-height: 52px;
        }
        .group-btn:hover {
            border-color: var(--brand);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(92,107,192,.12);
        }
        .group-btn.completed {
            border-color: rgba(16,185,129,.55);
            color: #059669;
        }
        .group-btn .group-btn-fill {
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 0;
            background: rgba(92, 107, 192, 0.30);
            z-index: 0;
            transition: width .35s ease;
            pointer-events: none;
        }
        .group-btn.completed .group-btn-fill {
            background: rgba(16, 185, 129, 0.28);
        }
        .group-btn .group-btn-label {
            position: relative;
            z-index: 1;
            display: block;
            white-space: pre-line;
            line-height: 1.25;
        }
"""


def extract_words_from_docx(path: Path) -> list[dict]:
    z = zipfile.ZipFile(path)
    xml = z.read("word/document.xml").decode("utf-8")
    paras = re.findall(r"<w:p[\s\S]*?</w:p>", xml)
    rows: list[str] = []
    for p in paras:
        texts = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)
        if texts:
            rows.append("".join(texts).strip())
    i = 0
    while i < len(rows) and rows[i] != "1":
        i += 1
    words: list[dict] = []
    while i < len(rows):
        num = rows[i]
        if not re.fullmatch(r"\d+", num):
            i += 1
            continue
        if i + 3 >= len(rows):
            break
        words.append(
            {
                "word": rows[i + 1].strip(),
                "phonetic": re.sub(r"\s+", " ", rows[i + 2]).strip(),
                "pos": "",
                "meaning": re.sub(r"\s+", " ", rows[i + 3]).strip(),
            }
        )
        i += 4
    return words


def ensure_group_btn_css(html: str) -> str:
    if ".group-btn .group-btn-fill" in html:
        return html
    anchor = "        #group-info { color: var(--brand); font-weight: 600; margin-bottom: 14px; font-size: .95rem; }\n"
    if anchor not in html:
        raise SystemExit("group-info CSS anchor not found")
    return html.replace(anchor, anchor + "\n" + GROUP_BTN_CSS + "\n", 1)


def patch_progress_logic(html: str, storage_key: str) -> str:
    """Add first-dictation progress tracking + button fill rendering."""
    if "let currentGroupWords" not in html:
        html = html.replace(
            "        let currentStage = 0;\n"
            "        let currentWordIndex = 0;\n"
            "        let failedWords = [];\n"
            "        let masteredWords = [];",
            "        let currentStage = 0;\n"
            "        let currentWordIndex = 0;\n"
            "        let failedWords = [];\n"
            "        let currentGroupWords = [];\n"
            "        let masteredWords = [];",
            1,
        )

    if "function recordStage1Result()" in html and "group-btn-fill" in html:
        # Already patched; still ensure start button is gone
        html = re.sub(
            r'<button class="btn btn-primary" id="start-group-btn" onclick="startLearning\(\)">开始学习</button>',
            "",
            html,
            count=1,
        )
        return html

    # Ensure start button removed
    html = re.sub(
        r'<button class="btn btn-primary" id="start-group-btn" onclick="startLearning\(\)">开始学习</button>',
        "",
        html,
        count=1,
    )

    # Init arrays + load/save
    old_init = """        let groupStatus = [];  // 每组状态: 'pending' | 'completed'

        function initGroupStatus() {
            groupStatus = new Array(TOTAL_GROUPS).fill('pending');
            // Load from localStorage
            const saved = localStorage.getItem('%s');
            if (saved) {
                try {
                    const data = JSON.parse(saved);
                    if (data.groupStatus) {
                        groupStatus = data.groupStatus;
                    }
                } catch (e) {}
            }
        }

        function saveGroupStatus() {
            localStorage.setItem('%s', JSON.stringify({ groupStatus: groupStatus }));
        }""" % (
        storage_key,
        storage_key,
    )

    # More flexible match of current init
    init_pat = re.compile(
        r"let groupStatus = \[\];[\s\S]*?function saveGroupStatus\(\) \{\n"
        r"            localStorage\.setItem\('" + re.escape(storage_key) + r"', JSON\.stringify\(\{ groupStatus: groupStatus \}\)\);\n"
        r"        \}",
        re.M,
    )
    new_init = f"""        let groupStatus = [];  // 每组状态: 'pending' | 'completed'
        // 每组最近一次学习的首轮听写结果：{{correct, total}} | null
        let groupFirstDictation = [];
        let stage1FirstCorrect = 0;

        function initGroupStatus() {{
            groupStatus = new Array(TOTAL_GROUPS).fill('pending');
            groupFirstDictation = new Array(TOTAL_GROUPS).fill(null);
            const saved = localStorage.getItem('{storage_key}');
            if (saved) {{
                try {{
                    const data = JSON.parse(saved);
                    if (data.groupStatus) {{
                        groupStatus = data.groupStatus;
                    }}
                    if (Array.isArray(data.groupFirstDictation)) {{
                        groupFirstDictation = data.groupFirstDictation;
                        while (groupFirstDictation.length < TOTAL_GROUPS) groupFirstDictation.push(null);
                        if (groupFirstDictation.length > TOTAL_GROUPS) {{
                            groupFirstDictation = groupFirstDictation.slice(0, TOTAL_GROUPS);
                        }}
                    }}
                }} catch (e) {{}}
            }}
        }}

        function saveGroupStatus() {{
            localStorage.setItem('{storage_key}', JSON.stringify({{
                groupStatus: groupStatus,
                groupFirstDictation: groupFirstDictation
            }}));
        }}

        function recordStage1Result() {{
            stage1FirstCorrect = masteredWords.length;
            groupFirstDictation[currentGroupIndex] = {{
                correct: stage1FirstCorrect,
                total: currentGroupWords.length
            }};
            saveGroupStatus();
        }}"""
    if not init_pat.search(html):
        raise SystemExit(f"groupStatus init block not found for {storage_key}")
    html = init_pat.sub(new_init, html, count=1)

    # Reset stage1FirstCorrect in startLearning
    if "stage1FirstCorrect = 0;" not in html:
        html = html.replace(
            "            masteredWords = [];\n            failedWords = [];\n            allWrongWords = [];",
            "            masteredWords = [];\n            failedWords = [];\n            allWrongWords = [];\n            stage1FirstCorrect = 0;",
            1,
        )

    # Record when stage 1 finishes (two branches in submitDictation and skipWord)
    stage1_end_old = """            if (currentWordIndex >= currentGroupWords.length) {
                // 阶段1完成，进入阶段2
                if (failedWords.length > 0) {
                    currentGroup = [...failedWords];
                    setStage(2);
                } else {
                    setStage(5);
                }
            } else {
                updateStage1Progress();
                document.getElementById('dictation-input').value = '';
                document.getElementById('dictation-input').focus();
                setTimeout(() => playCurrentWord(), 300);
            }
            updateStats();
            saveProgress();
        }

        function skipWord() {
            addWord(failedWords, currentGroupWords[currentWordIndex]);
            addWord(allWrongWords, currentGroupWords[currentWordIndex]);
            currentWordIndex++;
            
            if (currentWordIndex >= currentGroupWords.length) {
                if (failedWords.length > 0) {
                    currentGroup = [...failedWords];
                    setStage(2);
                } else {
                    setStage(5);
                }
            } else {"""

    stage1_end_new = """            if (currentWordIndex >= currentGroupWords.length) {
                // 阶段1完成：记录首轮听写正确比例
                recordStage1Result();
                if (failedWords.length > 0) {
                    currentGroup = [...failedWords];
                    setStage(2);
                } else {
                    setStage(5);
                }
            } else {
                updateStage1Progress();
                document.getElementById('dictation-input').value = '';
                document.getElementById('dictation-input').focus();
                setTimeout(() => playCurrentWord(), 300);
            }
            updateStats();
            saveProgress();
        }

        function skipWord() {
            addWord(failedWords, currentGroupWords[currentWordIndex]);
            addWord(allWrongWords, currentGroupWords[currentWordIndex]);
            currentWordIndex++;
            
            if (currentWordIndex >= currentGroupWords.length) {
                recordStage1Result();
                if (failedWords.length > 0) {
                    currentGroup = [...failedWords];
                    setStage(2);
                } else {
                    setStage(5);
                }
            } else {"""
    if stage1_end_old not in html:
        raise SystemExit("stage1 end block not found")
    html = html.replace(stage1_end_old, stage1_end_new, 1)

    # renderGroupGrid with progress fill
    render_old = """        function renderGroupGrid() {
            const grid = document.getElementById('group-grid');
            grid.innerHTML = '';
            for (let i = 0; i < TOTAL_GROUPS; i++) {
                const btn = document.createElement('button');
                btn.className = 'group-btn';
                if (groupStatus[i] === 'completed') {
                    btn.classList.add('completed');
                }
                const startNum = i * WORDS_PER_GROUP + 1;
                const endNum = Math.min((i + 1) * WORDS_PER_GROUP, ALL_WORDS.length);
                btn.textContent = `${i + 1}\\n${startNum}-${endNum}`;
                btn.style.whiteSpace = 'pre-line';
                btn.onclick = () => startGroup(i);
                grid.appendChild(btn);
            }
            updateGroupInfo();
        }

        function selectGroup(index) {
            currentGroupIndex = index;
            updateGroupInfo();
        }

        function startGroup(index) {
            selectGroup(index);
            startLearning();
        }

        function updateGroupInfo() {
            const info = document.getElementById('group-info');
            const completedCount = groupStatus.filter(s => s === 'completed').length;
            info.textContent = `共 ${TOTAL_GROUPS} 组（已完成 ${completedCount}/${TOTAL_GROUPS} 组，共 ${ALL_WORDS.length} 词）· 点击小组开始学习`;
        }"""

    # Allow either startGroup or selectGroup in current file
    render_pat = re.compile(
        r"function renderGroupGrid\(\) \{[\s\S]*?function updateGroupInfo\(\) \{[\s\S]*?info\.textContent = `[^`]+`;\n        \}",
        re.M,
    )
    render_new = """        function renderGroupGrid() {
            const grid = document.getElementById('group-grid');
            grid.innerHTML = '';
            for (let i = 0; i < TOTAL_GROUPS; i++) {
                const btn = document.createElement('button');
                btn.className = 'group-btn';
                btn.type = 'button';
                if (groupStatus[i] === 'completed') {
                    btn.classList.add('completed');
                }
                const startNum = i * WORDS_PER_GROUP + 1;
                const endNum = Math.min((i + 1) * WORDS_PER_GROUP, ALL_WORDS.length);
                const fill = document.createElement('span');
                fill.className = 'group-btn-fill';
                const stats = groupFirstDictation[i];
                if (stats && stats.total > 0) {
                    const pct = Math.max(0, Math.min(100, Math.round((stats.correct / stats.total) * 100)));
                    fill.style.width = pct + '%';
                    btn.title = `最近一次首轮听写：${stats.correct}/${stats.total}（${pct}%）`;
                } else {
                    fill.style.width = '0%';
                    btn.title = '暂无最近一次首轮听写记录';
                }
                const label = document.createElement('span');
                label.className = 'group-btn-label';
                label.textContent = `${i + 1}\\n${startNum}-${endNum}`;
                btn.appendChild(fill);
                btn.appendChild(label);
                btn.onclick = () => startGroup(i);
                grid.appendChild(btn);
            }
            updateGroupInfo();
        }

        function selectGroup(index) {
            currentGroupIndex = index;
            updateGroupInfo();
        }

        function startGroup(index) {
            selectGroup(index);
            startLearning();
        }

        function updateGroupInfo() {
            const info = document.getElementById('group-info');
            const completedCount = groupStatus.filter(s => s === 'completed').length;
            info.textContent = `共 ${TOTAL_GROUPS} 组（已完成 ${completedCount}/${TOTAL_GROUPS} 组，共 ${ALL_WORDS.length} 词）· 点击小组开始学习`;
        }"""
    if not render_pat.search(html):
        raise SystemExit("renderGroupGrid block not found")
    html = render_pat.sub(render_new, html, count=1)

    # Ensure startGroup exists even if render replaced an older select-only version
    if "function startGroup(index)" not in html:
        html = html.replace(
            "        function selectGroup(index) {\n            currentGroupIndex = index;\n            updateGroupInfo();\n        }\n",
            "        function selectGroup(index) {\n            currentGroupIndex = index;\n            updateGroupInfo();\n        }\n\n"
            "        function startGroup(index) {\n            selectGroup(index);\n            startLearning();\n        }\n",
            1,
        )

    return html


def build_listening_basic(words: list[dict], base_html: str) -> str:
    src = base_html
    words_json = json.dumps(words, ensure_ascii=False, separators=(",", ":"))
    src = re.sub(
        r"const ALL_WORDS = \[.*?\];",
        "const ALL_WORDS = " + words_json + ";",
        src,
        count=1,
        flags=re.S,
    )
    replacements = [
        ("<title>听力单词学习系统</title>", "<title>听力基础词汇学习系统</title>"),
        ("<h1> 听力单词学习系统</h1>", "<h1>听力基础词汇学习系统</h1>"),
        ("<h1>听力单词学习系统</h1>", "<h1>听力基础词汇学习系统</h1>"),
        ("<h2>欢迎使用听力单词学习系统</h2>", "<h2>欢迎使用听力基础词汇学习系统</h2>"),
        ("listeningGroupStatus", "listeningBasicGroupStatus"),
        ("listeningWordsProgress", "listeningBasicWordsProgress"),
        ("audio/words/", "audio/basic_words/"),
        ("const WORDS_PER_GROUP = 20;", "const WORDS_PER_GROUP = 50;"),
    ]
    for old, new in replacements:
        if old in src:
            src = src.replace(old, new)
    # base_html already contains progress-bar logic; storage keys are renamed above
    if "listeningBasicGroupStatus" not in src:
        raise SystemExit("listening_basic missing renamed storage key")
    if "group-btn-fill" not in src:
        raise SystemExit("listening_basic missing progress fill markup")
    return src


def patch_index(words: list[dict]) -> None:
    html = INDEX.read_text(encoding="utf-8")
    words_js = json.dumps([w["word"] for w in words], ensure_ascii=False)

    if "const allWordsListeningBasic" not in html:
        m = re.search(r"const allWords = \[.*?\];", html, flags=re.S)
        if not m:
            raise SystemExit("allWords not found in index.html")
        insert = (
            m.group(0)
            + "\n        const allWordsListeningBasic = "
            + words_js
            + ";\n"
            + "        const BUILTIN_DICTATION = {\n"
            + "            dictation: { id: 'dictation', name: '听力1000词', words: allWords, studyPage: 'listening.html', audioBase: 'audio/words/' },\n"
            + "            listening_basic: { id: 'listening_basic', name: '听力基础词汇', words: allWordsListeningBasic, studyPage: 'listening_basic.html', audioBase: 'audio/basic_words/' }\n"
            + "        };\n"
            + "        let currentDictationModuleId = 'dictation';\n"
            + "        function getBuiltinDictation(moduleId) {\n"
            + "            const key = normalizeModuleType(moduleId || currentDictationModuleId);\n"
            + "            return BUILTIN_DICTATION[key] || BUILTIN_DICTATION.dictation;\n"
            + "        }\n"
            + "        function isBuiltinDictationModule(moduleId) {\n"
            + "            return !!BUILTIN_DICTATION[normalizeModuleType(moduleId)];\n"
            + "        }\n"
        )
        html = html[: m.start()] + insert + html[m.end() :]
    else:
        html = re.sub(
            r"const allWordsListeningBasic = \[.*?\];",
            "const allWordsListeningBasic = " + words_js + ";",
            html,
            count=1,
            flags=re.S,
        )

    if "{ id: 'listening_basic', name: '听力基础词汇'" not in html:
        html = html.replace(
            "{ id: 'dictation', name: '听力1000词', target_type: 'dynamic', targets: { 6: 70, 6.5: 80, 7: 90 }, unit: '%', url: '', icon: 'headphones' },",
            "{ id: 'dictation', name: '听力1000词', target_type: 'dynamic', targets: { 6: 70, 6.5: 80, 7: 90 }, unit: '%', url: '', icon: 'headphones' },\n"
            "            { id: 'listening_basic', name: '听力基础词汇', target_type: 'dynamic', targets: { 6: 70, 6.5: 80, 7: 90 }, unit: '%', url: '', icon: 'headphones' },",
        )

    if "listening_basic_learn" not in html:
        html = html.replace(
            "dictation_learn: 'dictation',",
            "dictation_learn: 'dictation',\n"
            "                listening_basic_learn: 'listening_basic',",
        )

    html = html.replace(
        "return m.id === 'dictation' || !!m.url || !!m.test_url;",
        "return isBuiltinDictationModule(m.id) || !!m.url || !!m.test_url;",
    )
    html = html.replace(
        "const testableModules = availableModules.filter(function(m) { return m.id === 'dictation' || m.test_url; });",
        "const testableModules = availableModules.filter(function(m) { return isBuiltinDictationModule(m.id) || m.test_url; });",
    )
    html = html.replace(
        "const isTestable = m.id === 'dictation' || !!m.test_url;",
        "const isTestable = isBuiltinDictationModule(m.id) || !!m.test_url;",
    )

    old_btn = (
        "if (m.id === 'dictation') {\n"
        "                    html += '<button class=\"btn btn-sm\" style=\"margin-right:5px;\" onclick=\"startTest(\\'random\\')\">测试</button>';\n"
        "                    html += '<button class=\"btn btn-sm btn-secondary\" style=\"margin-right:5px;\" onclick=\"openListeningIframe()\">学习</button>';\n"
        "                    html += '<button class=\"btn btn-sm btn-success\" onclick=\"switchStudentTab(\\'history\\')\">历史</button>';\n"
        "                }"
    )
    new_btn = (
        "if (isBuiltinDictationModule(m.id)) {\n"
        "                    html += '<button class=\"btn btn-sm\" style=\"margin-right:5px;\" onclick=\"startTest(\\'random\\', \\'' + m.id + '\\')\">测试</button>';\n"
        "                    html += '<button class=\"btn btn-sm btn-secondary\" style=\"margin-right:5px;\" onclick=\"openListeningIframe(\\'' + m.id + '\\')\">学习</button>';\n"
        "                    html += '<button class=\"btn btn-sm btn-success\" onclick=\"switchStudentTab(\\'history\\')\">历史</button>';\n"
        "                }"
    )
    if old_btn in html:
        html = html.replace(old_btn, new_btn)

    old_start = """        async function startTest(mode) {
            // 用户点击了开始测试，解锁音频
            unlockAudio();
            testStartTime = Date.now(); // 记录测试开始时间
            
            currentTestMode = mode;
            document.getElementById('testModeLabel').textContent = mode === 'random' ? '随机测试' : '错题测试';
            document.getElementById('testModeLabel').style.background = mode === 'random' ? '#e9ecef' : '#d4edda';
            if (mode === 'random') {
                testWords = shuffleArray(allWords.slice()).slice(0, 50);
            } else {
                const result = await db.from('wrong_words').select('*').eq('student_id', currentStudent.student_id).eq('is_mastered', false);
                if (!result.data || result.data.length === 0) {
                    showToast('暂无错题可练习', 'info');
                    return;
                }
                testWords = result.data.map(function(w) { return w.word; });
                if (testWords.length < 50) {
                    const more = shuffleArray(allWords.filter(function(w) { return testWords.indexOf(w) === -1; })).slice(0, 50 - testWords.length);
                    testWords = testWords.concat(more);
                }
            }
            testResults = [];
            currentTestIndex = 0;
            showScreen('testScreen');
            showQuestion();
        }"""
    new_start = """        async function startTest(mode, moduleId) {
            // 用户点击了开始测试，解锁音频
            unlockAudio();
            testStartTime = Date.now(); // 记录测试开始时间
            currentDictationModuleId = normalizeModuleType(moduleId || currentDictationModuleId || 'dictation');
            const dictation = getBuiltinDictation(currentDictationModuleId);
            const bank = dictation.words;
            
            currentTestMode = mode;
            document.getElementById('testModeLabel').textContent = mode === 'random' ? '随机测试' : '错题测试';
            document.getElementById('testModeLabel').style.background = mode === 'random' ? '#e9ecef' : '#d4edda';
            if (mode === 'random') {
                testWords = shuffleArray(bank.slice()).slice(0, 50);
            } else {
                const result = await db.from('wrong_words').select('*').eq('student_id', currentStudent.student_id).eq('module_type', currentDictationModuleId).eq('is_mastered', false);
                if (!result.data || result.data.length === 0) {
                    showToast('暂无错题可练习', 'info');
                    return;
                }
                testWords = result.data.map(function(w) { return w.word; });
                if (testWords.length < 50) {
                    const more = shuffleArray(bank.filter(function(w) { return testWords.indexOf(w) === -1; })).slice(0, 50 - testWords.length);
                    testWords = testWords.concat(more);
                }
            }
            testResults = [];
            currentTestIndex = 0;
            showScreen('testScreen');
            showQuestion();
        }"""
    if old_start in html:
        html = html.replace(old_start, new_start)

    old_finish = """            const threshold = await getPassThreshold('dictation', currentStudent);
            const isPassed = score >= threshold;

            const durationSeconds = testStartTime > 0 ? Math.max(0, Math.floor((Date.now() - testStartTime) / 1000)) : 0;
            const insertResult = await saveModuleTestRecord({
                student_id: currentStudent.student_id,
                module_type: 'dictation',
                module_name: '听力1000词',
                test_type: currentTestMode,
                score_percent: score,
                correct_count: correctCount,
                total_count: testResults.length,
                is_passed: isPassed,
                pass_threshold: threshold,
                duration_seconds: durationSeconds,
                started_at: testStartTime > 0 ? new Date(testStartTime).toISOString() : null,
                ended_at: new Date().toISOString(),
                details: testResults
            });
            
            if (insertResult.error) {
                console.error('保存测试记录失败:', insertResult.error);
                showToast('保存测试记录失败: ' + insertResult.error.message, 'error');
            }
            
            let newWrongCount = 0;
            for (let i = 0; i < testResults.length; i++) {
                const result = testResults[i];
                if (!result.isCorrect && !result.skipped) {
                    const existingResult = await db.from('wrong_words').select('*').eq('student_id', currentStudent.student_id).eq('word', result.word).single();
                    if (existingResult.data) {
                        if (existingResult.data.correct_streak >= 2) {
                            await db.from('wrong_words').update({ is_mastered: true }).eq('id', existingResult.data.id);
                        } else {
                            await db.from('wrong_words').update({ wrong_count: existingResult.data.wrong_count + 1, correct_streak: 0, last_tested: new Date().toISOString() }).eq('id', existingResult.data.id);
                        }
                    } else {
                        await db.from('wrong_words').insert({
                            student_id: currentStudent.student_id,
                            word: result.word,
                            wrong_count: 1,
                            correct_streak: 0
                        });
                        newWrongCount++;
                    }
                } else if (result.isCorrect) {
                    const existingResult = await db.from('wrong_words').select('*').eq('student_id', currentStudent.student_id).eq('word', result.word).single();
                    if (existingResult.data && !existingResult.data.is_mastered) {
                        const newStreak = existingResult.data.correct_streak + 1;
                        if (newStreak >= 2) {
                            await db.from('wrong_words').update({ correct_streak: newStreak, is_mastered: true, last_tested: new Date().toISOString() }).eq('id', existingResult.data.id);
                        } else {
                            await db.from('wrong_words').update({ correct_streak: newStreak, last_tested: new Date().toISOString() }).eq('id', existingResult.data.id);
                        }
                    }
                }
            }
            
            showScreen('resultScreen');
            document.getElementById('resultStudentInfo').textContent = currentStudent.name + ' - 听力1000词';"""
    new_finish = """            const dictation = getBuiltinDictation(currentDictationModuleId);
            const threshold = await getPassThreshold(dictation.id, currentStudent);
            const isPassed = score >= threshold;

            const durationSeconds = testStartTime > 0 ? Math.max(0, Math.floor((Date.now() - testStartTime) / 1000)) : 0;
            const insertResult = await saveModuleTestRecord({
                student_id: currentStudent.student_id,
                module_type: dictation.id,
                module_name: dictation.name,
                test_type: currentTestMode,
                score_percent: score,
                correct_count: correctCount,
                total_count: testResults.length,
                is_passed: isPassed,
                pass_threshold: threshold,
                duration_seconds: durationSeconds,
                started_at: testStartTime > 0 ? new Date(testStartTime).toISOString() : null,
                ended_at: new Date().toISOString(),
                details: testResults
            });
            
            if (insertResult.error) {
                console.error('保存测试记录失败:', insertResult.error);
                showToast('保存测试记录失败: ' + insertResult.error.message, 'error');
            }
            
            let newWrongCount = 0;
            for (let i = 0; i < testResults.length; i++) {
                const result = testResults[i];
                if (!result.isCorrect && !result.skipped) {
                    const existingResult = await db.from('wrong_words').select('*').eq('student_id', currentStudent.student_id).eq('module_type', dictation.id).eq('word', result.word).single();
                    if (existingResult.data) {
                        if (existingResult.data.correct_streak >= 2) {
                            await db.from('wrong_words').update({ is_mastered: true }).eq('id', existingResult.data.id);
                        } else {
                            await db.from('wrong_words').update({ wrong_count: existingResult.data.wrong_count + 1, correct_streak: 0, last_tested: new Date().toISOString() }).eq('id', existingResult.data.id);
                        }
                    } else {
                        await db.from('wrong_words').insert({
                            student_id: currentStudent.student_id,
                            module_type: dictation.id,
                            word: result.word,
                            wrong_count: 1,
                            correct_streak: 0
                        });
                        newWrongCount++;
                    }
                } else if (result.isCorrect) {
                    const existingResult = await db.from('wrong_words').select('*').eq('student_id', currentStudent.student_id).eq('module_type', dictation.id).eq('word', result.word).single();
                    if (existingResult.data && !existingResult.data.is_mastered) {
                        const newStreak = existingResult.data.correct_streak + 1;
                        if (newStreak >= 2) {
                            await db.from('wrong_words').update({ correct_streak: newStreak, is_mastered: true, last_tested: new Date().toISOString() }).eq('id', existingResult.data.id);
                        } else {
                            await db.from('wrong_words').update({ correct_streak: newStreak, last_tested: new Date().toISOString() }).eq('id', existingResult.data.id);
                        }
                    }
                }
            }
            
            showScreen('resultScreen');
            document.getElementById('resultStudentInfo').textContent = currentStudent.name + ' - ' + dictation.name;"""
    if old_finish in html:
        html = html.replace(old_finish, new_finish)

    old_hist = """        async function startWrongWordsTestFromHistory(wordListStr) {
            if (!wordListStr) {
                showToast('没有错题可练习', 'info');
                return;
            }
            const words = wordListStr.split(',').filter(function(w) { return w.trim(); });
            if (words.length === 0) {
                showToast('没有错题可练习', 'info');
                return;
            }
            currentTestMode = 'wrong_words';
            document.getElementById('testModeLabel').textContent = '历史错题测试';
            document.getElementById('testModeLabel').style.background = '#f8d7da';
            testWords = words;
            testResults = [];
            currentTestIndex = 0;
            showScreen('testScreen');
            showQuestion();
        }"""
    new_hist = """        async function startWrongWordsTestFromHistory(wordListStr, moduleId) {
            if (!wordListStr) {
                showToast('没有错题可练习', 'info');
                return;
            }
            const words = wordListStr.split(',').filter(function(w) { return w.trim(); });
            if (words.length === 0) {
                showToast('没有错题可练习', 'info');
                return;
            }
            unlockAudio();
            testStartTime = Date.now();
            currentDictationModuleId = normalizeModuleType(moduleId || currentDictationModuleId || 'dictation');
            currentTestMode = 'wrong_words';
            document.getElementById('testModeLabel').textContent = '历史错题测试';
            document.getElementById('testModeLabel').style.background = '#f8d7da';
            testWords = words;
            testResults = [];
            currentTestIndex = 0;
            showScreen('testScreen');
            showQuestion();
        }"""
    if old_hist in html:
        html = html.replace(old_hist, new_hist)

    old_hist_btn = "onclick=\"event.stopPropagation();startWrongWordsTestFromHistory(\\'' + escapeJsString(wrongWordList) + '\\')\""
    new_hist_btn = "onclick=\"event.stopPropagation();startWrongWordsTestFromHistory(\\'' + escapeJsString(wrongWordList) + '\\', \\'' + escapeJsString(normalizeModuleType(r.module_type || 'dictation')) + '\\')\""
    if old_hist_btn in html:
        html = html.replace(old_hist_btn, new_hist_btn)

    old_open = """        function openListeningIframe() {
            window._currentModule = {
                id: 'dictation',
                name: '听力1000词',
                mode: 'study',
                startedAt: Date.now(),
                reported: false
            };
            showScreen('listeningScreen');
            document.getElementById('listeningIframe').src = appendModuleParams('listening.html', {
                student_id: currentStudent && currentStudent.student_id,
                module_type: 'dictation',
                module_name: '听力1000词',
                mode: 'study'
            });
        }"""
    new_open = """        function openListeningIframe(moduleId) {
            const dictation = getBuiltinDictation(moduleId || 'dictation');
            currentDictationModuleId = dictation.id;
            window._currentModule = {
                id: dictation.id,
                name: dictation.name,
                mode: 'study',
                startedAt: Date.now(),
                reported: false
            };
            showScreen('listeningScreen');
            const listeningTitle = document.querySelector('#listeningScreen h2');
            if (listeningTitle) listeningTitle.textContent = dictation.name + '学习';
            document.getElementById('listeningIframe').src = appendModuleParams(dictation.studyPage, {
                student_id: currentStudent && currentStudent.student_id,
                module_type: dictation.id,
                module_name: dictation.name,
                mode: 'study'
            });
        }"""
    if old_open in html:
        html = html.replace(old_open, new_open)

    html = html.replace(
        "const iframeId = current.id === 'dictation' && current.mode === 'study'\n"
        "                ? 'listeningIframe'\n"
        "                : 'genericIframe';",
        "const iframeId = isBuiltinDictationModule(current.id) && current.mode === 'study'\n"
        "                ? 'listeningIframe'\n"
        "                : 'genericIframe';",
    )

    INDEX.write_text(html, encoding="utf-8")
    print(f"patched {INDEX}")


def patch_local_server() -> None:
    text = LOCAL_SERVER.read_text(encoding="utf-8")
    if "migrate_wrong_words_module_type" not in text:
        migrate_fn = '''
def migrate_wrong_words_module_type(conn: sqlite3.Connection) -> None:
    """Ensure wrong_words is scoped by module_type for parallel dictation banks."""
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='wrong_words'"
    ).fetchone()
    if not row:
        return
    columns = [r[1] for r in conn.execute("PRAGMA table_info(wrong_words)").fetchall()]
    if "module_type" in columns:
        return
    conn.executescript(
        f"""
        ALTER TABLE wrong_words RENAME TO wrong_words_legacy;
        CREATE TABLE wrong_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            module_type TEXT NOT NULL DEFAULT 'dictation',
            word TEXT NOT NULL,
            wrong_count INTEGER DEFAULT 1,
            correct_streak INTEGER DEFAULT 0,
            last_tested TEXT DEFAULT ({now_sql()}),
            is_mastered INTEGER DEFAULT 0,
            UNIQUE(student_id, module_type, word)
        );
        INSERT INTO wrong_words (
            id, student_id, module_type, word, wrong_count,
            correct_streak, last_tested, is_mastered
        )
        SELECT
            id, student_id, 'dictation', word, wrong_count,
            correct_streak, last_tested, is_mastered
        FROM wrong_words_legacy;
        DROP TABLE wrong_words_legacy;
        CREATE INDEX IF NOT EXISTS idx_wrong_words_student_id ON wrong_words(student_id);
        CREATE INDEX IF NOT EXISTS idx_wrong_words_module_type ON wrong_words(module_type);
        """
    )


'''
        text = text.replace(
            "def init_db(db_path: Path) -> None:\n",
            migrate_fn + "def init_db(db_path: Path) -> None:\n",
            1,
        )

    old_wrong = """            CREATE TABLE IF NOT EXISTS wrong_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL REFERENCES students(student_id),
                word TEXT NOT NULL,
                wrong_count INTEGER DEFAULT 1,
                correct_streak INTEGER DEFAULT 0,
                last_tested TEXT DEFAULT ({now_sql()}),
                is_mastered INTEGER DEFAULT 0,
                UNIQUE(student_id, word)
            );"""
    new_wrong = """            CREATE TABLE IF NOT EXISTS wrong_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL REFERENCES students(student_id),
                module_type TEXT NOT NULL DEFAULT 'dictation',
                word TEXT NOT NULL,
                wrong_count INTEGER DEFAULT 1,
                correct_streak INTEGER DEFAULT 0,
                last_tested TEXT DEFAULT ({now_sql()}),
                is_mastered INTEGER DEFAULT 0,
                UNIQUE(student_id, module_type, word)
            );"""
    if old_wrong in text:
        text = text.replace(old_wrong, new_wrong)

    if "migrate_wrong_words_module_type(conn)" not in text:
        text = text.replace(
            '            CREATE INDEX IF NOT EXISTS idx_wrong_words_student_id ON wrong_words(student_id);\n'
            '            CREATE INDEX IF NOT EXISTS idx_word_mastery_student_id ON word_mastery(student_id);\n'
            '            """\n'
            "        )\n"
            "\n"
            "        conn.execute(",
            '            CREATE INDEX IF NOT EXISTS idx_wrong_words_student_id ON wrong_words(student_id);\n'
            '            CREATE INDEX IF NOT EXISTS idx_word_mastery_student_id ON word_mastery(student_id);\n'
            '            """\n'
            "        )\n"
            "\n"
            "        migrate_wrong_words_module_type(conn)\n"
            "        conn.execute(\n"
            '            "CREATE INDEX IF NOT EXISTS idx_wrong_words_module_type ON wrong_words(module_type)"\n'
            "        )\n"
            "\n"
            "        conn.execute(",
            1,
        )

    if '("listening_basic", "听力基础词汇"' not in text:
        text = text.replace(
            '("dictation", "听力1000词", 70, 80, 90),\n',
            '("dictation", "听力1000词", 70, 80, 90),\n'
            '            ("listening_basic", "听力基础词汇", 70, 80, 90),\n',
        )

    LOCAL_SERVER.write_text(text, encoding="utf-8")
    print(f"patched {LOCAL_SERVER}")


def main() -> None:
    if not DOCX.exists():
        raise SystemExit(f"docx not found: {DOCX}")
    words = extract_words_from_docx(DOCX)
    print(f"words: {len(words)}")

    listening = LISTENING.read_text(encoding="utf-8")
    listening = ensure_group_btn_css(listening)
    listening = patch_progress_logic(listening, "listeningGroupStatus")
    LISTENING.write_text(listening, encoding="utf-8")
    print(f"patched {LISTENING}")

    basic = build_listening_basic(words, listening)
    # build_listening_basic already calls patch_progress_logic; ensure css kept
    basic = ensure_group_btn_css(basic)
    # If patch_progress_logic ran twice on basic due to key replace order, verify markers
    if "group-btn-fill" not in basic:
        raise SystemExit("listening_basic missing progress fill")
    if "WORDS_PER_GROUP = 50" not in basic:
        raise SystemExit("listening_basic WORDS_PER_GROUP not 50")
    LISTENING_BASIC.write_text(basic, encoding="utf-8")
    print(f"wrote {LISTENING_BASIC}")

    patch_index(words)
    patch_local_server()
    print("done")


if __name__ == "__main__":
    main()

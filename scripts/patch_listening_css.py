"""
替换 listening.html 的 <style> 块，实现与主站一致的简约高级 UI
不改动任何 HTML 结构或 JS 逻辑
"""
import re
from pathlib import Path

STYLE_NEW = """<style>
        :root {
            --brand: #5c6bc0;
            --brand-deep: #3949ab;
            --brand-light: #e8eaf6;
            --accent: #7e57c2;
            --bg: #f4f5f9;
            --surface: #ffffff;
            --surface-2: #f8f9fc;
            --border: #e2e4ec;
            --text-primary: #1a1d2e;
            --text-secondary: #6b7280;
            --text-muted: #9ca3af;
            --success: #10b981;
            --success-bg: #ecfdf5;
            --danger: #ef4444;
            --danger-bg: #fef2f2;
            --radius-sm: 8px;
            --radius: 14px;
            --radius-lg: 20px;
            --shadow: 0 4px 16px rgba(92,107,192,.10), 0 1px 4px rgba(0,0,0,.06);
            --shadow-lg: 0 12px 40px rgba(92,107,192,.14), 0 2px 8px rgba(0,0,0,.06);
            --transition: 0.18s ease;
        }

        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei',
                         system-ui, -apple-system, sans-serif;
            background: var(--bg);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 24px 16px;
            color: var(--text-primary);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            background: var(--surface);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
            width: 100%;
            max-width: 620px;
            padding: 36px 40px;
            margin: auto;
        }

        h1 {
            text-align: center;
            color: var(--text-primary);
            font-size: 1.55rem;
            font-weight: 700;
            margin-bottom: 6px;
            letter-spacing: -.01em;
        }
        .subtitle {
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: 26px;
            font-size: .9rem;
        }

        /* 阶段指示器 */
        .stage-indicator {
            display: flex;
            gap: 8px;
            margin-bottom: 28px;
            justify-content: center;
        }
        .stage {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
            flex: 1;
            max-width: 90px;
        }
        .stage-dot {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--border);
            color: var(--text-muted);
            font-weight: 700;
            font-size: .85rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background var(--transition), color var(--transition);
            border: 2px solid transparent;
        }
        .stage.active .stage-dot {
            background: var(--brand);
            color: #fff;
            border-color: var(--brand-deep);
            box-shadow: 0 0 0 3px rgba(92,107,192,.18);
        }
        .stage.completed .stage-dot {
            background: var(--success-bg);
            color: var(--success);
            border-color: var(--success);
        }
        .stage-label {
            font-size: .72rem;
            color: var(--text-muted);
            text-align: center;
            font-weight: 500;
        }
        .stage.active .stage-label { color: var(--brand); font-weight: 700; }
        .stage.completed .stage-label { color: var(--success); }

        /* 内容区 */
        .content-area { position: relative; }
        .hidden { display: none !important; }

        /* 开始页 */
        .start-screen { text-align: center; }
        .start-screen h2 {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: var(--text-primary);
        }
        .start-screen p {
            color: var(--text-secondary);
            margin-bottom: 20px;
            font-size: .9rem;
        }
        .feature-list {
            list-style: none;
            margin: 0 0 24px;
            text-align: left;
            display: inline-block;
        }
        .feature-list li {
            padding: 6px 0 6px 22px;
            position: relative;
            color: var(--text-secondary);
            font-size: .88rem;
        }
        .feature-list li::before {
            content: '';
            position: absolute;
            left: 0;
            top: 12px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--brand);
            opacity: .6;
        }

        /* 分组格 */
        #group-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            margin-bottom: 20px;
        }
        #group-info { color: var(--brand); font-weight: 600; margin-bottom: 14px; font-size: .95rem; }

        /* 进度条 */
        .progress-bar {
            background: var(--border);
            border-radius: 999px;
            height: 5px;
            margin: 0 0 16px;
            overflow: hidden;
        }
        .progress-fill {
            background: linear-gradient(90deg, var(--brand), var(--accent));
            height: 100%;
            border-radius: 999px;
            transition: width .4s cubic-bezier(.4,0,.2,1);
        }
        .word-counter {
            text-align: center;
            color: var(--text-muted);
            font-size: .82rem;
            margin-bottom: 20px;
        }

        /* 音频按钮 */
        .audio-btn {
            display: block;
            margin: 0 auto 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--brand);
            border: none;
            cursor: pointer;
            transition: transform var(--transition), background var(--transition), box-shadow var(--transition);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .audio-btn:hover {
            transform: scale(1.07);
            background: var(--brand-deep);
            box-shadow: 0 6px 20px rgba(92,107,192,.35);
        }
        .audio-btn svg { width: 26px; height: 26px; fill: #fff; }

        /* 输入区 */
        .input-area { margin-bottom: 16px; }
        .word-input {
            width: 100%;
            padding: 12px 16px;
            font-size: 1.05rem;
            font-family: inherit;
            border: 1.5px solid var(--border);
            border-radius: var(--radius-sm);
            background: var(--surface-2);
            color: var(--text-primary);
            text-align: center;
            transition: border-color var(--transition), box-shadow var(--transition);
        }
        .word-input:focus {
            outline: none;
            border-color: var(--brand);
            box-shadow: 0 0 0 3px rgba(92,107,192,.12);
            background: var(--surface);
        }

        /* 反馈提示 */
        .feedback-area {
            min-height: 36px;
            text-align: center;
            font-weight: 600;
            font-size: .95rem;
            margin-bottom: 14px;
            padding: 8px;
            border-radius: var(--radius-sm);
        }
        .feedback-area.correct {
            background: var(--success-bg);
            color: #065f46;
        }
        .feedback-area.wrong {
            background: var(--danger-bg);
            color: #991b1b;
        }

        /* 单词展示（阶段2） */
        .word-display {
            text-align: center;
            margin: 20px 0 10px;
        }
        .word-text {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--brand-deep);
            letter-spacing: .02em;
            margin-bottom: 4px;
        }
        .word-phonetic { color: var(--text-muted); font-size: .9rem; margin-bottom: 4px; }
        .word-meaning  { color: var(--text-secondary); font-size: .9rem; }

        /* 按钮 */
        .btn {
            background: var(--brand);
            color: #fff;
            border: none;
            padding: 10px 26px;
            font-size: .95rem;
            font-family: inherit;
            font-weight: 600;
            border-radius: var(--radius);
            cursor: pointer;
            transition: background var(--transition), transform var(--transition), box-shadow var(--transition);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .btn-primary { background: var(--brand); }
        .btn-primary:hover { background: var(--brand-deep); transform: translateY(-1px); box-shadow: 0 6px 18px rgba(92,107,192,.28); }
        .btn-secondary {
            background: transparent;
            color: var(--text-secondary);
            border: 1.5px solid var(--border);
        }
        .btn-secondary:hover { background: var(--surface-2); color: var(--text-primary); }
        .btn:disabled { opacity: .5; cursor: not-allowed; transform: none; box-shadow: none; }
        .btn-group { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-top: 16px; }

        /* 完成页 */
        .complete-area { text-align: center; }
        .complete-area h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin: 20px 0;
        }
        .stat-box {
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 14px 10px;
            text-align: center;
        }
        .stat-value { font-size: 1.6rem; font-weight: 800; color: var(--brand); }
        .stat-label { color: var(--text-muted); font-size: .78rem; margin-top: 4px; }

        /* Toast */
        .toast {
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%) translateY(8px);
            background: var(--text-primary);
            color: #fff;
            padding: 10px 22px;
            border-radius: 999px;
            z-index: 2000;
            font-size: .88rem;
            font-weight: 500;
            opacity: 0;
            transition: opacity .25s, transform .25s;
            pointer-events: none;
            white-space: nowrap;
        }
        .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
        .toast.error   { background: var(--danger); }
        .toast.success { background: var(--success); }

        /* 响应式 */
        @media (max-width: 480px) {
            .container { padding: 22px 16px; }
            h1 { font-size: 1.3rem; }
            #group-grid { grid-template-columns: repeat(4, 1fr); }
            .word-text { font-size: 1.8rem; }
        }
    </style>"""

target = Path(r'F:/PythonTools/雅思练习/sources/tinglidanciceshi/listening.html')
html = target.read_text(encoding='utf-8')
html_new = re.sub(r'<style>.*?</style>', STYLE_NEW, html, count=1, flags=re.DOTALL)

if html_new == html:
    print("ERROR: style block not replaced")
else:
    target.write_text(html_new, encoding='utf-8')
    print(f"OK: listening.html updated ({len(html)} -> {len(html_new)} chars)")

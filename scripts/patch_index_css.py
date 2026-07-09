"""
替换 index.html 的 <style> 块，实现简约高级的 UI 设计
不改动任何 HTML 结构或 JS 逻辑
"""
import re
from pathlib import Path

STYLE_NEW = """<style>
        /* === 设计系统 === */
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
            --success-text: #065f46;
            --danger: #ef4444;
            --danger-bg: #fef2f2;
            --danger-text: #991b1b;
            --warning-bg: #fffbeb;
            --warning-text: #92400e;
            --info-bg: #eff6ff;
            --info-text: #1e40af;
            --radius-sm: 8px;
            --radius: 14px;
            --radius-lg: 20px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04);
            --shadow: 0 4px 16px rgba(92,107,192,.10), 0 1px 4px rgba(0,0,0,.06);
            --shadow-lg: 0 12px 40px rgba(92,107,192,.14), 0 2px 8px rgba(0,0,0,.06);
            --transition: 0.18s ease;
        }

        /* === 基础重置 === */
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei',
                         system-ui, -apple-system, sans-serif;
            background: var(--bg);
            min-height: 100vh;
            padding: 24px 16px;
            color: var(--text-primary);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }
        .container { max-width: 860px; margin: 0 auto; }

        /* === 品牌标题 === */
        .logo {
            text-align: center;
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: .02em;
            color: var(--brand-deep);
            margin-bottom: 6px;
        }

        /* === 卡片 === */
        .card {
            background: var(--surface);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow);
            padding: 36px 40px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
        }
        h1 {
            text-align: center;
            color: var(--text-primary);
            margin-bottom: 8px;
            font-size: 1.7rem;
            font-weight: 700;
            letter-spacing: -.01em;
        }
        .subtitle {
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: 28px;
            font-size: .95rem;
        }

        /* === 表单 === */
        .input-group { margin-bottom: 18px; }
        .input-group label {
            display: block;
            margin-bottom: 6px;
            color: var(--text-primary);
            font-weight: 500;
            font-size: .9rem;
        }
        .input-group input,
        .input-group select,
        .input-group textarea {
            width: 100%;
            padding: 10px 14px;
            font-size: .95rem;
            font-family: inherit;
            border: 1.5px solid var(--border);
            border-radius: var(--radius-sm);
            background: var(--surface-2);
            color: var(--text-primary);
            transition: border-color var(--transition), box-shadow var(--transition);
        }
        .input-group input:focus,
        .input-group select:focus,
        .input-group textarea:focus {
            outline: none;
            border-color: var(--brand);
            box-shadow: 0 0 0 3px rgba(92,107,192,.12);
            background: var(--surface);
        }
        .input-group textarea { resize: vertical; min-height: 100px; }

        /* === 按钮 === */
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
            letter-spacing: .01em;
        }
        .btn:hover {
            background: var(--brand-deep);
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(92,107,192,.28);
        }
        .btn:active { transform: translateY(0); }
        .btn:disabled {
            opacity: .5;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .btn-secondary {
            background: transparent;
            color: var(--text-secondary);
            border: 1.5px solid var(--border);
        }
        .btn-secondary:hover {
            background: var(--surface-2);
            color: var(--text-primary);
            border-color: #c5c8d6;
            box-shadow: none;
        }
        .btn-success { background: var(--success); }
        .btn-success:hover { background: #059669; }
        .btn-danger { background: var(--danger); }
        .btn-danger:hover { background: #dc2626; }
        .btn-sm { padding: 6px 14px; font-size: .85rem; border-radius: var(--radius-sm); }
        .btn-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 20px;
        }

        /* === 页面切换 === */
        .screen { display: none; }
        .screen.active { display: block; }

        /* === 后台页眉 === */
        .admin-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        .admin-header h2 {
            color: var(--brand-deep);
            font-size: 1.15rem;
            font-weight: 700;
        }

        /* === 表格 === */
        table { width: 100%; border-collapse: collapse; margin-top: 16px; }
        th, td {
            padding: 11px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            font-size: .9rem;
        }
        th {
            background: var(--surface-2);
            color: var(--brand-deep);
            font-weight: 600;
            font-size: .83rem;
            text-transform: uppercase;
            letter-spacing: .04em;
        }
        tr:hover td { background: var(--brand-light); }
        tr:last-child td { border-bottom: none; }

        /* === 徽章 === */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: .78rem;
            font-weight: 600;
            letter-spacing: .02em;
        }
        .badge-success { background: var(--success-bg); color: var(--success-text); }
        .badge-danger  { background: var(--danger-bg);  color: var(--danger-text); }
        .badge-warning { background: var(--warning-bg); color: var(--warning-text); }
        .badge-info    { background: var(--info-bg);    color: var(--info-text); }

        /* === 达标状态 === */
        .pass-status {
            font-size: 1rem;
            font-weight: 600;
            padding: 12px 18px;
            border-radius: var(--radius-sm);
            text-align: center;
            margin: 14px 0;
        }
        .pass-status.pass {
            background: var(--success-bg);
            color: var(--success-text);
            border: 1px solid #a7f3d0;
        }
        .pass-status.fail {
            background: var(--danger-bg);
            color: var(--danger-text);
            border: 1px solid #fca5a5;
        }

        /* === 进度条 === */
        .progress-bar {
            background: var(--border);
            border-radius: 999px;
            height: 6px;
            margin: 14px 0;
            overflow: hidden;
        }
        .progress-fill {
            background: linear-gradient(90deg, var(--brand), var(--accent));
            height: 100%;
            border-radius: 999px;
            transition: width .4s cubic-bezier(.4,0,.2,1);
        }

        /* === 统计格 === */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin: 18px 0;
        }
        .stat-box {
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 14px 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 1.45rem;
            font-weight: 700;
            color: var(--brand);
            line-height: 1.2;
        }
        .stat-label {
            color: var(--text-muted);
            font-size: .78rem;
            margin-top: 4px;
        }

        /* === 错题列表 === */
        .error-list { max-height: 280px; overflow-y: auto; margin-top: 14px; }
        .error-item {
            background: var(--warning-bg);
            border: 1px solid #fcd34d;
            padding: 9px 14px;
            border-radius: var(--radius-sm);
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
            font-size: .88rem;
        }

        /* === Tab 栏 === */
        .tab-bar {
            display: flex;
            gap: 2px;
            margin-bottom: 20px;
            border-bottom: 1.5px solid var(--border);
        }
        .tab {
            padding: 9px 18px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            margin-bottom: -1.5px;
            color: var(--text-secondary);
            font-size: .9rem;
            font-weight: 500;
            transition: color var(--transition), border-color var(--transition);
            border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        }
        .tab:hover { color: var(--brand); background: var(--brand-light); }
        .tab.active { border-bottom-color: var(--brand); color: var(--brand); font-weight: 700; }

        /* === 弹窗 === */
        .modal {
            display: none;
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(15,20,40,.45);
            backdrop-filter: blur(4px);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal.active { display: flex; }
        .modal-content {
            background: var(--surface);
            border-radius: var(--radius-lg);
            padding: 28px 30px;
            max-width: 480px;
            width: 92%;
            max-height: 82vh;
            overflow-y: auto;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border);
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            padding-bottom: 14px;
            border-bottom: 1px solid var(--border);
        }
        .modal-header h3 { font-size: 1.05rem; font-weight: 700; }
        .modal-close {
            background: none;
            border: none;
            font-size: 1.4rem;
            cursor: pointer;
            color: var(--text-muted);
            line-height: 1;
            padding: 2px 6px;
            border-radius: 6px;
            transition: color var(--transition), background var(--transition);
        }
        .modal-close:hover { color: var(--text-primary); background: var(--surface-2); }

        /* === Toast 通知 === */
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

        /* === 历史图表区 === */
        .history-chart { height: 180px; margin: 18px 0; }

        /* === 响应式 === */
        @media (max-width: 640px) {
            body { padding: 12px 8px; }
            .card { padding: 20px 18px; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            table { font-size: .82rem; }
            th, td { padding: 8px 10px; }
            .tab { padding: 8px 12px; font-size: .82rem; }
        }
    </style>"""

target = Path(r'F:/PythonTools/雅思练习/sources/tinglidanciceshi/index.html')
html = target.read_text(encoding='utf-8')

# 替换 <style>...</style> 块
html_new = re.sub(r'<style>.*?</style>', STYLE_NEW, html, count=1, flags=re.DOTALL)

if html_new == html:
    print("ERROR: style block not found or not replaced")
else:
    target.write_text(html_new, encoding='utf-8')
    print(f"OK: index.html updated ({len(html)} -> {len(html_new)} chars)")

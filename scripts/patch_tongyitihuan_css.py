"""
替换 tongyitihuan/index.html 的 <style> 块
原版是暗色游戏风格，改为简约高级的亮色风格，与主站保持统一
"""
import re
from pathlib import Path

STYLE_NEW = """<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

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
    --warning: #f59e0b;
    --warning-bg: #fffbeb;
    --warning-text: #92400e;
    --radius-sm: 8px;
    --radius: 14px;
    --radius-lg: 20px;
    --shadow: 0 4px 16px rgba(92,107,192,.10), 0 1px 4px rgba(0,0,0,.06);
    --shadow-lg: 0 12px 40px rgba(92,107,192,.14), 0 2px 8px rgba(0,0,0,.06);
    --transition: 0.18s ease;
  }

  body {
    font-family: 'Inter', 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei',
                 system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
    line-height: 1.6;
  }

  /* === 顶部导航 === */
  .top-bar {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }
  .top-bar .brand {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--brand-deep);
    letter-spacing: .01em;
  }
  .top-bar .stats-bar {
    display: flex;
    gap: 20px;
    font-size: .82rem;
    color: var(--text-secondary);
  }
  .top-bar .stats-bar span { font-weight: 600; color: var(--text-primary); }

  /* === 主体内容 === */
  .main-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 24px 16px;
  }

  /* === 卡片 === */
  .card {
    background: var(--surface);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    padding: 28px 30px;
    margin-bottom: 20px;
  }
  .card-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
  }

  /* === 学习卡片（单词展示） === */
  .word-card {
    background: var(--surface);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    padding: 36px 32px;
    text-align: center;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    position: relative;
  }
  .word-en {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: .02em;
    margin-bottom: 6px;
  }
  .word-phonetic {
    color: var(--text-muted);
    font-size: .9rem;
    margin-bottom: 8px;
  }
  .word-cn {
    color: var(--text-secondary);
    font-size: 1rem;
    font-weight: 500;
  }
  .word-pos {
    display: inline-block;
    padding: 2px 10px;
    background: var(--brand-light);
    color: var(--brand);
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 600;
    margin-bottom: 10px;
  }
  .word-example {
    font-size: .85rem;
    color: var(--text-secondary);
    line-height: 1.7;
    margin-top: 12px;
    padding: 10px 14px;
    background: var(--surface-2);
    border-radius: var(--radius-sm);
    border-left: 3px solid var(--brand);
    text-align: left;
    width: 100%;
  }

  /* 同义词对 */
  .synonym-pair {
    display: flex;
    align-items: center;
    gap: 18px;
    justify-content: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
  }
  .syn-item {
    background: var(--surface-2);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 20px;
    min-width: 140px;
    text-align: center;
  }
  .syn-item .word { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); }
  .syn-item .meaning { font-size: .8rem; color: var(--text-secondary); margin-top: 4px; }
  .syn-arrow { font-size: 1.4rem; color: var(--brand); font-weight: 700; }

  /* === 进度 === */
  .progress-bar {
    background: var(--border);
    border-radius: 999px;
    height: 5px;
    margin: 14px 0;
    overflow: hidden;
  }
  .progress-fill {
    background: linear-gradient(90deg, var(--brand), var(--accent));
    height: 100%;
    border-radius: 999px;
    transition: width .4s cubic-bezier(.4,0,.2,1);
  }
  .progress-text {
    display: flex;
    justify-content: space-between;
    font-size: .78rem;
    color: var(--text-muted);
    margin-bottom: 6px;
  }

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
  }
  .btn:hover {
    background: var(--brand-deep);
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(92,107,192,.28);
  }
  .btn:active { transform: translateY(0); }
  .btn:disabled { opacity: .5; cursor: not-allowed; transform: none; box-shadow: none; }
  .btn-secondary {
    background: transparent;
    color: var(--text-secondary);
    border: 1.5px solid var(--border);
  }
  .btn-secondary:hover { background: var(--surface-2); color: var(--text-primary); box-shadow: none; }
  .btn-success { background: var(--success); }
  .btn-success:hover { background: #059669; }
  .btn-danger  { background: var(--danger); }
  .btn-danger:hover  { background: #dc2626; }
  .btn-lg { padding: 13px 36px; font-size: 1.05rem; }
  .btn-sm { padding: 6px 14px; font-size: .82rem; border-radius: var(--radius-sm); }
  .btn-group { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-top: 16px; }
  .btn-block { width: 100%; justify-content: center; padding: 12px; }

  /* === 输入框 === */
  .input-group { margin-bottom: 16px; }
  .input-group label {
    display: block;
    margin-bottom: 6px;
    font-size: .88rem;
    font-weight: 500;
    color: var(--text-primary);
  }
  .input-group input,
  .input-group select {
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
  .input-group select:focus {
    outline: none;
    border-color: var(--brand);
    box-shadow: 0 0 0 3px rgba(92,107,192,.12);
    background: var(--surface);
  }

  /* 大型答题输入框 */
  .answer-input {
    width: 100%;
    padding: 14px 18px;
    font-size: 1.1rem;
    font-family: inherit;
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    background: var(--surface-2);
    color: var(--text-primary);
    text-align: center;
    transition: border-color var(--transition), box-shadow var(--transition);
  }
  .answer-input:focus {
    outline: none;
    border-color: var(--brand);
    box-shadow: 0 0 0 3px rgba(92,107,192,.12);
    background: var(--surface);
  }
  .answer-input.correct { border-color: var(--success); background: var(--success-bg); color: var(--success-text); }
  .answer-input.wrong   { border-color: var(--danger);  background: var(--danger-bg);  color: var(--danger-text); }

  /* === 徽章 === */
  .badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 600;
  }
  .badge-new      { background: var(--brand-light); color: var(--brand-deep); }
  .badge-learning { background: var(--warning-bg);  color: var(--warning-text); }
  .badge-mastered { background: var(--success-bg);  color: var(--success-text); }

  /* === 统计格 === */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 16px 0;
  }
  .stat-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px 8px;
    text-align: center;
  }
  .stat-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--brand);
    line-height: 1.2;
  }
  .stat-label { color: var(--text-muted); font-size: .75rem; margin-top: 4px; }

  /* === 词组列表 === */
  .word-list { list-style: none; }
  .word-list-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
    font-size: .9rem;
    transition: background var(--transition);
  }
  .word-list-item:last-child { border-bottom: none; }
  .word-list-item:hover { background: var(--surface-2); border-radius: var(--radius-sm); }
  .wli-en { font-weight: 700; color: var(--text-primary); min-width: 140px; }
  .wli-cn { color: var(--text-secondary); flex: 1; }
  .wli-status { flex-shrink: 0; }

  /* === 模态弹窗 === */
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
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
  }
  .modal-header h3 { font-size: 1rem; font-weight: 700; }
  .modal-close {
    background: none; border: none;
    font-size: 1.3rem; cursor: pointer;
    color: var(--text-muted);
    padding: 2px 6px; border-radius: 6px;
    transition: color var(--transition), background var(--transition);
  }
  .modal-close:hover { color: var(--text-primary); background: var(--surface-2); }

  /* === Toast === */
  .toast {
    position: fixed;
    bottom: 24px; left: 50%;
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

  /* === 结果页 === */
  .result-container { text-align: center; padding: 20px; }
  .result-score-big {
    font-size: 4.5rem;
    font-weight: 900;
    color: var(--brand);
    line-height: 1;
    margin: 20px 0 8px;
  }
  .result-label { color: var(--text-secondary); font-size: .92rem; margin-bottom: 20px; }

  /* === 分组/选择页 === */
  .group-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin: 18px 0;
  }
  .group-btn {
    background: var(--surface-2);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px 8px;
    cursor: pointer;
    text-align: center;
    font-family: inherit;
    font-size: .85rem;
    font-weight: 600;
    color: var(--text-primary);
    transition: border-color var(--transition), background var(--transition), transform var(--transition);
  }
  .group-btn:hover {
    border-color: var(--brand);
    background: var(--brand-light);
    transform: translateY(-1px);
  }
  .group-btn.active { border-color: var(--brand); background: var(--brand-light); color: var(--brand-deep); }
  .group-btn.done   { border-color: var(--success); background: var(--success-bg); color: var(--success-text); }

  /* === 反馈 === */
  .feedback {
    padding: 10px 16px;
    border-radius: var(--radius-sm);
    font-size: .9rem;
    font-weight: 600;
    margin: 12px 0;
    display: none;
  }
  .feedback.show { display: block; }
  .feedback.correct { background: var(--success-bg); color: var(--success-text); border: 1px solid #a7f3d0; }
  .feedback.wrong   { background: var(--danger-bg);  color: var(--danger-text);  border: 1px solid #fca5a5; }

  /* === 选项（选择题） === */
  .options-grid {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 16px 0;
  }
  .option-item {
    background: var(--surface-2);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 12px 18px;
    cursor: pointer;
    font-family: inherit;
    font-size: .9rem;
    color: var(--text-primary);
    text-align: left;
    transition: border-color var(--transition), background var(--transition);
  }
  .option-item:hover { border-color: var(--brand); background: var(--brand-light); }
  .option-item.selected { border-color: var(--brand); background: var(--brand-light); font-weight: 600; }
  .option-item.correct  { border-color: var(--success); background: var(--success-bg); color: var(--success-text); }
  .option-item.wrong    { border-color: var(--danger);  background: var(--danger-bg);  color: var(--danger-text); }
  .option-item:disabled { cursor: default; }

  /* === 导航/回退头 === */
  .nav-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 10;
  }
  .nav-back {
    background: none;
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 6px 12px;
    cursor: pointer;
    font-size: .85rem;
    font-family: inherit;
    color: var(--text-secondary);
    transition: background var(--transition), color var(--transition);
  }
  .nav-back:hover { background: var(--surface-2); color: var(--text-primary); }
  .nav-title { font-weight: 700; font-size: .95rem; flex: 1; }
  .nav-counter { font-size: .8rem; color: var(--text-muted); }

  /* === 响应式 === */
  @media (max-width: 560px) {
    .main-content { padding: 14px 10px; }
    .card { padding: 18px 14px; }
    .word-card { padding: 24px 16px; }
    .word-en { font-size: 1.7rem; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .group-grid { grid-template-columns: repeat(4, 1fr); }
  }
</style>"""

target = Path(r'F:/PythonTools/雅思练习/sources/tongyitihuan/index.html')
html = target.read_text(encoding='utf-8')

# tongyitihuan 有可能存在多个 style 块，只替换第一个
html_new = re.sub(r'<style>.*?</style>', STYLE_NEW, html, count=1, flags=re.DOTALL)

if html_new == html:
    print("ERROR: style block not replaced")
else:
    target.write_text(html_new, encoding='utf-8')
    print(f"OK: tongyitihuan/index.html updated ({len(html)} -> {len(html_new)} chars)")

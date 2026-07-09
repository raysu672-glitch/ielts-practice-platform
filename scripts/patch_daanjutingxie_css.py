"""
替换 daanjutingxie/index.html 的 <style> 块
保留原有功能完整性，只更新视觉样式
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
    --success-text: #065f46;
    --danger: #ef4444;
    --danger-bg: #fef2f2;
    --danger-text: #991b1b;
    --warning-bg: #fffbeb;
    --warning-text: #92400e;
    --radius-sm: 8px;
    --radius: 14px;
    --radius-lg: 20px;
    --shadow: 0 4px 16px rgba(92,107,192,.10), 0 1px 4px rgba(0,0,0,.06);
    --shadow-lg: 0 12px 40px rgba(92,107,192,.14), 0 2px 8px rgba(0,0,0,.06);
    --transition: 0.18s ease;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Inter', 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei',
                 system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
    line-height: 1.6;
  }

  /* ===== 首页 ===== */
  #home {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 48px 24px;
  }
  #home h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
    letter-spacing: -.01em;
  }
  #home p.sub {
    color: var(--text-secondary);
    margin-bottom: 36px;
    font-size: .92rem;
  }

  /* 分组格 */
  .group-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    max-width: 700px;
    width: 100%;
  }
  .group-btn {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 10px;
    cursor: pointer;
    text-align: center;
    transition: border-color var(--transition), transform var(--transition), box-shadow var(--transition);
    position: relative;
  }
  .group-btn:hover {
    border-color: var(--brand);
    background: var(--brand-light);
    transform: translateY(-2px);
    box-shadow: var(--shadow);
  }
  .group-btn .g-title {
    font-size: .9rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
  }
  .group-btn .g-count { font-size: .75rem; color: var(--text-muted); }
  .group-btn .g-score {
    margin-top: 6px;
    font-size: .78rem;
    font-weight: 600;
    color: var(--brand);
  }
  .group-btn.done { border-color: var(--success); }
  .group-btn.done .g-title { color: var(--success); }

  /* ===== 答题区 ===== */
  #quiz { display: none; }

  .quiz-header {
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
  .back-btn {
    background: none;
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 6px 12px;
    cursor: pointer;
    font-size: .88rem;
    color: var(--text-secondary);
    font-family: inherit;
    transition: background var(--transition), color var(--transition);
  }
  .back-btn:hover { background: var(--surface-2); color: var(--text-primary); }
  .quiz-title {
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-primary);
    flex: 1;
  }
  .progress-text { font-size: .82rem; color: var(--text-muted); }

  .progress-bar-wrap {
    height: 4px;
    background: var(--border);
    overflow: hidden;
  }
  .progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--brand), var(--accent));
    transition: width .4s cubic-bezier(.4,0,.2,1);
  }

  /* 题卡 */
  .card {
    background: var(--surface);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    padding: 28px 30px;
    max-width: 660px;
    margin: 24px auto;
  }

  /* 音频区 */
  .audio-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    margin-bottom: 22px;
  }
  .play-btn {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: var(--brand);
    color: #fff;
    border: none;
    font-size: 1.6rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background var(--transition), transform var(--transition), box-shadow var(--transition);
  }
  .play-btn:hover {
    background: var(--brand-deep);
    transform: scale(1.06);
    box-shadow: 0 6px 20px rgba(92,107,192,.35);
  }
  .play-btn.speaking {
    background: var(--accent);
    animation: pulse 1.2s infinite;
  }
  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(126,87,194,.4); }
    50%       { box-shadow: 0 0 0 10px rgba(126,87,194,.0); }
  }
  .audio-hint {
    font-size: .8rem;
    color: var(--text-muted);
    text-align: center;
    line-height: 1.5;
  }
  .audio-hint strong {
    color: var(--brand);
    font-size: .82rem;
    display: block;
    margin-bottom: 2px;
  }

  /* 原文显示 */
  #originalText {
    display: none;
    margin: 14px 0;
    padding: 12px 16px;
    background: var(--surface-2);
    border-radius: var(--radius-sm);
    border-left: 3px solid var(--brand);
    font-size: .9rem;
    color: var(--text-secondary);
    line-height: 1.7;
  }
  #originalText.show { display: block; }
  #originalText label {
    font-size: .75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: var(--brand);
    display: block;
    margin-bottom: 6px;
  }

  /* 填空题 */
  .blank-sentence {
    font-size: 1rem;
    line-height: 1.9;
    color: var(--text-primary);
    margin-bottom: 18px;
    padding: 14px 18px;
    background: var(--surface-2);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
  }
  .blank { color: var(--brand); font-weight: 700; }

  /* 选项 */
  .options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 16px; }
  .option-btn {
    background: var(--surface-2);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 11px 16px;
    text-align: left;
    cursor: pointer;
    font-size: .9rem;
    font-family: inherit;
    color: var(--text-primary);
    transition: border-color var(--transition), background var(--transition);
  }
  .option-btn:hover { border-color: var(--brand); background: var(--brand-light); }
  .option-btn.selected { border-color: var(--brand); background: var(--brand-light); color: var(--brand-deep); font-weight: 600; }
  .option-btn.correct  { border-color: var(--success); background: var(--success-bg); color: var(--success-text); }
  .option-btn.wrong    { border-color: var(--danger);  background: var(--danger-bg);  color: var(--danger-text); }
  .option-btn:disabled { cursor: default; }

  /* 反馈 */
  #feedback {
    min-height: 40px;
    padding: 10px 16px;
    border-radius: var(--radius-sm);
    font-size: .9rem;
    font-weight: 600;
    margin-bottom: 14px;
    display: none;
  }
  #feedback.show { display: block; }
  #feedback.correct { background: var(--success-bg); color: var(--success-text); border: 1px solid #a7f3d0; }
  #feedback.wrong   { background: var(--danger-bg);  color: var(--danger-text);  border: 1px solid #fca5a5; }

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
  .btn:hover { background: var(--brand-deep); transform: translateY(-1px); box-shadow: 0 6px 18px rgba(92,107,192,.28); }
  .btn:disabled { opacity: .5; cursor: not-allowed; transform: none; box-shadow: none; }
  .btn-next {
    background: var(--brand);
    display: block;
    width: 100%;
    padding: 12px;
    font-size: .95rem;
    text-align: center;
    margin-top: 6px;
  }
  .btn-next:hover { background: var(--brand-deep); }

  /* 结果页 */
  #result { display: none; }
  .result-card {
    background: var(--surface);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    padding: 36px 30px;
    max-width: 560px;
    margin: 40px auto;
    text-align: center;
  }
  .result-card h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 8px; }
  .result-score {
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--brand);
    line-height: 1;
    margin: 18px 0 6px;
  }
  .result-detail { color: var(--text-secondary); font-size: .9rem; margin-bottom: 20px; }
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 18px 0;
  }
  .stat-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px 8px;
  }
  .stat-value { font-size: 1.5rem; font-weight: 800; color: var(--brand); }
  .stat-label { font-size: .75rem; color: var(--text-muted); margin-top: 4px; }

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
  @media (max-width: 560px) {
    .card { padding: 20px 16px; margin: 14px 12px; }
    .group-grid { grid-template-columns: repeat(3, 1fr); }
    .result-card { margin: 20px 12px; padding: 24px 18px; }
    .stats-grid { grid-template-columns: repeat(3, 1fr); }
  }
</style>"""

target = Path(r'F:/PythonTools/雅思练习/sources/daanjutingxie/index.html')
html = target.read_text(encoding='utf-8')
html_new = re.sub(r'<style>.*?</style>', STYLE_NEW, html, count=1, flags=re.DOTALL)

if html_new == html:
    print("ERROR: style block not replaced")
else:
    target.write_text(html_new, encoding='utf-8')
    print(f"OK: daanjutingxie/index.html updated ({len(html)} -> {len(html_new)} chars)")

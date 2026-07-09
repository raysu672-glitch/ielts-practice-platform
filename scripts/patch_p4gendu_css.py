"""
替换 P4gendu/styles.css，实现简约高级风格
"""
from pathlib import Path

CSS_NEW = """/* 基础样式重置 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

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
    --warning: #f59e0b;
    --warning-bg: #fffbeb;
    --danger: #ef4444;
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
    background-color: var(--bg);
    color: var(--text-primary);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

.container {
    max-width: 880px;
    margin: 0 auto;
    padding: 24px 16px;
}

/* 头部样式 */
header {
    text-align: center;
    padding: 32px 24px;
    background: var(--surface);
    color: var(--text-primary);
    border-radius: var(--radius-lg);
    margin-bottom: 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
}

header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--text-primary);
    letter-spacing: -.01em;
}

.subtitle {
    font-size: .95rem;
    color: var(--text-secondary);
}

/* 区块样式 */
section {
    background: var(--surface);
    border-radius: var(--radius-lg);
    padding: 28px 30px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
}

section h2 {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 18px;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}

/* 按钮样式 */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 26px;
    background: var(--brand);
    color: white;
    border: none;
    border-radius: var(--radius);
    font-size: .95rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: background var(--transition), transform var(--transition), box-shadow var(--transition);
}

.btn:hover {
    background: var(--brand-deep);
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(92,107,192,.28);
}

.btn:disabled {
    opacity: 0.5;
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
    box-shadow: none;
}

.btn-success {
    background: var(--success);
}

.btn-success:hover {
    background: #059669;
}

/* 倍速控制 */
.speed-controls {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 16px 0;
}

.speed-btn {
    padding: 8px 18px;
    background: var(--surface-2);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: .9rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    color: var(--text-primary);
    transition: border-color var(--transition), background var(--transition);
}

.speed-btn:hover {
    border-color: var(--brand);
    background: var(--brand-light);
}

.speed-btn.active {
    border-color: var(--brand);
    background: var(--brand-light);
    color: var(--brand-deep);
}

/* 音频播放器 */
audio {
    width: 100%;
    margin: 14px 0;
    border-radius: var(--radius-sm);
}

/* 进度条 */
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

/* 统计信息 */
.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

.stat-item {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px 12px;
    text-align: center;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--brand);
    line-height: 1.2;
}

.stat-label {
    font-size: .75rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* 输入框 */
input, select {
    padding: 10px 14px;
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: .95rem;
    font-family: inherit;
    background: var(--surface-2);
    color: var(--text-primary);
    transition: border-color var(--transition), box-shadow var(--transition);
}

input:focus, select:focus {
    outline: none;
    border-color: var(--brand);
    box-shadow: 0 0 0 3px rgba(92,107,192,.12);
    background: var(--surface);
}

/* 文本区域 */
textarea {
    width: 100%;
    padding: 12px 14px;
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: .9rem;
    font-family: inherit;
    background: var(--surface-2);
    color: var(--text-primary);
    line-height: 1.7;
    resize: vertical;
    min-height: 100px;
    transition: border-color var(--transition), box-shadow var(--transition);
}

textarea:focus {
    outline: none;
    border-color: var(--brand);
    box-shadow: 0 0 0 3px rgba(92,107,192,.12);
    background: var(--surface);
}

/* 高亮文本 */
.highlight {
    background: var(--warning-bg);
    border: 1px solid var(--warning);
    padding: 10px 14px;
    border-radius: var(--radius-sm);
    margin: 12px 0;
    font-size: .9rem;
    color: var(--text-primary);
}

/* Toast 通知 */
.toast {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%) translateY(8px);
    background: var(--text-primary);
    color: white;
    padding: 10px 22px;
    border-radius: 999px;
    font-size: .88rem;
    font-weight: 500;
    opacity: 0;
    transition: opacity .25s, transform .25s;
    pointer-events: none;
    white-space: nowrap;
    z-index: 1000;
}

.toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

.toast.success {
    background: var(--success);
}

.toast.error {
    background: var(--danger);
}

/* 响应式 */
@media (max-width: 560px) {
    .container {
        padding: 14px 10px;
    }

    header {
        padding: 22px 16px;
    }

    header h1 {
        font-size: 1.4rem;
    }

    section {
        padding: 18px 14px;
    }

    .stats {
        grid-template-columns: repeat(2, 1fr);
    }
}
"""

target = Path(r'F:/PythonTools/雅思练习/sources/P4gendu/styles.css')
target.write_text(CSS_NEW, encoding='utf-8')
print(f"OK: P4gendu/styles.css updated")

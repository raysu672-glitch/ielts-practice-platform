/**
 * 前端（node 可跑）回归测试入口。
 *
 * 发布清单里的 `node tests/test_tracking_utils.js` 已升级为本脚本：
 * 自动跑 tests/ 下所有 `test_*.js`，新增前端测试不用再改文档命令。
 */
const fs = require('node:fs');
const path = require('node:path');

const dir = __dirname;
const files = fs.readdirSync(dir)
  .filter((f) => /^test_.*\.js$/.test(f))
  .sort();

if (!files.length) {
  console.error('tests/ 下没有找到 test_*.js');
  process.exit(1);
}

for (const f of files) {
  require(path.join(dir, f));
}

console.log(`\n${files.length} 个前端测试文件全部通过: ${files.join(', ')}`);

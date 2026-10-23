# 零任务日诊断：2026001 @ 2026-11-16

## 1) get_today 返回 items = 0 条

## 2) plan_items 中 pending 总数 = 122
  其中未完成（非 _item_done）= 9
  经 _gendu_aware + _item_available_on 后 = 121

## 3) 关键集合
  backlog_ids  = 6 个
  released_ids = 123 个
  quota_map    = {'dictation': 1, 'reading_synonym': 1, 'speaking_p1': 1, 'listening_synonym': 1, 'sentence': 1, 'listening_basic': 0, 'writing_phrase': 0, 'writing_translate': 0, 'speaking_complex': 0}
  活跃未完成    = 8 个

## 4) 分类（在 backlog / released / 两者都不在）
  backlog∩released = 6  → 走「积压」分支派发
  仅 backlog        = 0  → 走「积压」分支派发
  **仅 released      = 0  → 既不算积压、也不算新单元 → 永远不派发**
  仅 neither(真新)  = 2  → 走「新单元」分支派发

## 5) _units_pack_picks 结果 = 0 条

## 6) 逐模块拆解（预期能派的模块为何是 0）
  dictation              quota=1 模块内活跃=16 积压=0 新=0 → 派 0 条  ← 派 0 条
  reading_synonym        quota=1 模块内活跃=19 积压=0 新=0 → 派 0 条  ← 派 0 条
  speaking_p1            quota=1 模块内活跃=16 积压=0 新=0 → 派 0 条  ← 派 0 条
  listening_synonym      quota=1 模块内活跃=19 积压=0 新=0 → 派 0 条  ← 派 0 条
  sentence               quota=1 模块内活跃=11 积压=0 新=0 → 派 0 条  ← 派 0 条
  listening_basic        quota=0 模块内活跃=8 积压=1 新=0 → 派 0 条  ← 派 0 条
  writing_phrase         quota=0 模块内活跃=13 积压=1 新=1 → 派 0 条  ← 派 0 条
  writing_translate      quota=0 模块内活跃=11 积压=4 新=1 → 派 0 条  ← 派 0 条
  speaking_complex       quota=0 模块内活跃=8 积压=0 新=0 → 派 0 条  ← 派 0 条
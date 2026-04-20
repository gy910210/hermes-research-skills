# Versioning Policy

## 默认策略
- 新版本优先，不覆盖旧版本。
- 每次更新都应留下：
  - 新版本文件
  - 旧版提示
  - manifest 或 changelog 条目

## 推荐记录字段
- `timestamp`
- `version_note`
- `source_summary`
- `updated_files`
- `new_version_paths`
- `conflicts_or_open_questions`

## 何时必须创建新版本
- 主稿结构被修改
- 核心结论被新增或修正
- benchmark / dataset 表被批量补全
- 新增整章或专题并回主稿

## 何时可以只更新 manifest
- 只是做了本轮观察记录
- 新证据尚不足以改正文稿
- 只是在收集候选来源

## 推荐协作顺序
1. 监测 skill 产出增量摘要
2. 审校新证据
3. 创建版本快照
4. 更新知识库
5. 更新 manifest 与索引

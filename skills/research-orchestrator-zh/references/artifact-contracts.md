# Artifact Contracts

## `context_brief`
- `research_topic`
- `domain_summary`
- `user_constraints_and_preferences`
- `existing_files[]`
  - `path`
  - `role`：`索引/主稿/增量稿/专题稿/附录/图示版/笔记`
- `existing_conclusions[]`
- `open_questions[]`
- `seed_sources[]`
- `version_chain[]`

## `research_agenda`
- `goal`
- `time_window`
- `deliverable_type`
- `priority_directions[]`
- `search_scope`
- `evidence_policy`
- `selected_skills[]`

## `evidence_map`
- `sources[]`
  - `title`
  - `url`
  - `source_type`
  - `publication_time`
  - `venue_or_source`
  - `institution_or_company`
  - `direction`
  - `directness`：`direct/adjacent/background`
  - `sector`：`academic/industrial/official`
  - `data_status`：`public/private/unknown`
  - `stance`：`support/contradiction/open-gap`
- `clusters[]`
- `priority_reading_queue[]`
- `missing_evidence[]`
- `missing_from_catalog[]`
- `institution_clusters[]`
- `citation_frontier[]`
- `route_family_candidates[]`

## `paper_notes`
- `title`
- `source_type`
- `publication_time`
- `venue_or_source`
- `institution_or_company`
- `problem`
- `task_type`
- `method_or_system`
- `datasets_and_benchmarks[]`
- `release_status`
- `explicit_claims[]`
- `results[]`
- `limitations[]`
- `reusable_for_sections[]`
- `citations[]`

## `evidence_audit`
- `scope`
- `direct_claims[]`
- `synthesized_claims[]`
- `strongest_support[]`
- `strongest_contradiction[]`
- `weak_claims[]`
- `license_or_release_risks[]`
- `risky_wording_to_avoid[]`
- `rewrite_suggestions[]`

## `synthesis_packet`
- `target_output_type`
- `section_outline[]`
- `evidence_backed_claims[]`
- `support_vs_contradiction[]`
- `new_angles[]`
- `merge_ready_sections[]`
- `keep_as_exploratory[]`
- `critical_rounds[]`
- `route_family_summary[]`
- `catalog_sync_notes[]`

## `maintenance_packet`
- `new_files[]`
- `updated_indexes[]`
- `legacy_version_notes[]`
- `consistency_findings[]`
- `broken_links[]`
- `benchmark_metadata_gaps[]`
- `catalog_diff_findings[]`
- `normalization_fixes[]`
- `paired_doc_drift[]`

## `html_publication_packet`
- `source_report`
- `entry_html`
- `output_dir`
- `included_pages[]`
- `included_attachments[]`
- `omitted_links[]`
- `source_unchanged`
- `checks`：正文/表格/代码/引用、链接与锚点、桌面/手机、控制台、打印；注明未执行项。
- `deployment_status`：`local_only` 或 `published_verified`
- `public_url`：仅在线上回读验证成功时填写。
- `deployment_checks`

详细边界见 [HTML输出契约](../../report-html-publisher-zh/references/output-contract.md)。本地生成不自动授权公网部署或公开内部工件。

# Process improvements backlog — 261114 1735 contract upgrade ff0a16b 3f5b2c1

**Date:** 2026-11-15 01:03 +0300
**Source ref:** `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`
**Status:** Draft

Зачем этот файл: держать raw process-improvement suggestions отдельно от обычных follow-ups и канонических doc edits.

Правила:
- Truth surface = блоки `### PI-...` ниже; derived surfaces `index.md`, `deferred.md`, `promotion_surface.md` пересобираются helper'ом.
- Literal no-op `NO PROCESS IMPROVEMENTS — why: <reason_code>` не materialize-ится как backlog row.
- Wave 1 ограничен `collect + triage`: promotion paths фиксируются literal fields, но не auto-promote логикой.
- Owner-facing `urgency` хранится в existing `priority`; отдельное поле `urgency` не добавляется.
- Mature rows фиксируют non-`P?` `priority`, `target_canon_path`, `target_repo_scope`, `delivery_mode`, `execution_kind`, `execution_ref`, `delivery_refs`, `handled_ref`, `promoted_at`, `handled_at`.

## Suggestions (truth)
### PI-001
- status: `open`
- priority: `P?`
- role: `Architect`
- owner: `Architect`
- promotion_class: `prompt_change`
- target_canon_path: `null`
- target_repo_scope: `null`
- delivery_mode: `null`
- execution_kind: `null`
- execution_ref: `null`
- delivery_refs: `null`
- handled_ref: `null`
- promoted_at: `null`
- handled_at: `null`
- trigger_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`
- symptom: `После успешного non-login Python readback make test завершился 87/6/0: inherited PLANVEYOR_RUNTIME_ROOT указывал на другой checkout без принятого source pin, хотя control header явно задавал выбранный runtime.`
- process_gap: `Executable handoff предполагал равенство supplied selection и child environment; ранние facade/snapshot receipts не доказывали это равенство для последующих project commands.`
- suggested_fix: `В source-owned Planner/Coder prompts закрепить same-exec physical comparison runtime из текущего control header с root child command и literal command-scoped binding для make/helper calls; при несовпадении owning stop без fallback, PATH/PYBIN/home/global changes.`
- created_at: `2026-11-15 00:53 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-002
- status: `open`
- priority: `P?`
- role: `Architect`
- owner: `Planner`
- promotion_class: `prompt_change`
- target_canon_path: `null`
- target_repo_scope: `null`
- delivery_mode: `null`
- execution_kind: `null`
- execution_ref: `null`
- delivery_refs: `null`
- handled_ref: `null`
- promoted_at: `null`
- handled_at: `null`
- trigger_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`
- symptom: `Первый executable draft содержал два runtime_py review_target_snapshot.py calls, которые дали rc64 Unsupported runtime helper; существующий public planveyor_review_target_snapshot работал через тот же selected facade.`
- process_gap: `Planner handoff прошёл inventory/preflight checks без проверки допустимости конкретного helper entrypoint, поэтому Coder потребовался дополнительный Architect/Planner reroute.`
- suggested_fix: `В source-owned planner_status_driven.md потребовать до executable handoff сверять используемые helper entrypoints с публичными surfaces выбранного facade и проверять доступные read-only calls; не превращать raw script filename в runtime_py recipe по предположению и не запускать project/SQL actions для такой проверки.`
- created_at: `2026-11-15 00:53 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-003
- status: `open`
- priority: `P?`
- role: `Coder`
- owner: `Planner`
- promotion_class: `prompt_change`
- target_canon_path: `null`
- target_repo_scope: `null`
- delivery_mode: `null`
- execution_kind: `null`
- execution_ref: `null`
- delivery_refs: `null`
- handled_ref: `null`
- promoted_at: `null`
- handled_at: `null`
- trigger_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`
- symptom: `После исправления Python launch первый make db-build отказал setup-cache-missing: отсутствовали все шесть prerequisites, хотя executable handoff предполагал подготовленный cache.`
- process_gap: `Готовность tracked bundle и интерпретатора была проверена отдельно от наличия объявленных локальных prerequisites; предположение о сохранённом cache потребовало дополнительного Coder/Architect/Planner цикла.`
- suggested_fix: `В source-owned Planner completion для профилей с локальным cache фиксировать доступный read-only inventory объявленных prerequisites до executable handoff. Missing prerequisite направлять на согласование recovery authority; не запускать setup автоматически и не вводить универсальные project-specific пути.`
- created_at: `2026-11-15 00:59 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-004
- status: `open`
- priority: `P?`
- role: `Coder`
- owner: `Planner`
- promotion_class: `prompt_change`
- target_canon_path: `null`
- target_repo_scope: `null`
- delivery_mode: `null`
- execution_kind: `null`
- execution_ref: `null`
- delivery_refs: `null`
- handled_ref: `null`
- promoted_at: `null`
- handled_at: `null`
- trigger_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`
- symptom: `Для одной разрешённой setup attempt Planner CENSOR уточнил terminal-success reuse и запрет перезаписи before receipts; фактический запуск сначала вернул running session без terminal exit_code.`
- process_gap: `Первоначальный executable recipe недостаточно явно различал намерение, actual dispatch, running session, terminal success и неизвестный outcome при продолжении той же задачи.`
- suggested_fix: `Для Owner-authorized одноразовых команд закрепить компактные ветки: один actual dispatch, наблюдение того же session_id, reuse terminal rc0 без нового launch и baseline overwrite, stop при nonzero/interruption/unknown, затем отдельный post-check перед продолжением. Применять существующий receipt механизм без автоматического retry.`
- created_at: `2026-11-15 00:59 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-005
- status: `open`
- priority: `P?`
- role: `Planner`
- owner: `Architect`
- promotion_class: `helper_change`
- target_canon_path: `null`
- target_repo_scope: `null`
- delivery_mode: `null`
- execution_kind: `null`
- execution_ref: `null`
- delivery_refs: `null`
- handled_ref: `null`
- promoted_at: `null`
- handled_at: `null`
- trigger_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`
- symptom: `При Planner finalize plan_lint отказал с concrete child plan path in child-map/queue context: строка Command содержала literal child runtime binding и snapshot command с путём текущего плана. Замена слова child на command-scoped устранила отказ без изменения исполняемого контракта.`
- process_gap: `Source helper legacy_child_graph_drift_line в scripts/plan_lint.py считает совместное присутствие слова child и concrete plan path признаком child graph, не различая аргумент команды, указывающий на текущий план, и настоящую ссылку на дочерний план.`
- suggested_fix: `Уточнить source-owned detector и добавить парную regression fixture: обычная Command row с child environment binding и self-plan snapshot argument не вызывает child-graph отказ; настоящий concrete child ref в Child plan map или Execution queue продолжает давать существующий fail-closed результат. Lifecycle и admission authority сохранить.`
- created_at: `2026-11-15 01:03 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

## Notes
- Если suggestion уже promoted в live plan/canon/helper, triage helper должен обновить `status`, `target_canon_path`, `target_repo_scope`, `delivery_mode`, а не переписывать historical fields по памяти.
- `promoted`/`handled` rows должны хранить literal execution refs; `delivery_refs` допускает только `null` или `; `-separated literal refs.
- `triaged` rows требуют non-`P?` `priority`, literal target/delivery carrier и execution/delivery refs либо explicit `triage_note` decision.
- `deferred` rows должны хранить owner, reason/revisit trigger в `triage_note` и literal `delivery_refs` либо explicit null-delivery reason.
- `docs/followups/*` остаётся отдельной carrier family: process-improvement row не дублируется туда без отдельного явного follow-up decision.

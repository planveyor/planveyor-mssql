# Process improvements backlog — 261126 1137 mssql dotnet sdk 10 11

**Date:** 2026-11-27 01:11 +0300
**Source ref:** `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md`
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
- trigger_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md#Planner-Q&A`
- source_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md`
- symptom: `При Planner Q2 recipe потребовала отдельные only10, only11 и combined inventories, хотя AC1 требовала combined→10 и отсутствие подходящей10→11; дополнительная installation prerequisite потребовала semantic возврата к Architect.`
- process_gap: `Completion не отделила обязательные proof cases из acceptance от выбранной физической топологии установок, поэтому recipe неявно усилила предусловия задачи.`
- suggested_fix: `В source-owned Architect/Planner completion для compatibility matrices сопоставлять каждый обязательный case с конкретным AC и prepared input; явно определять допустимое переиспользование одного physical input. Дополнительный обязательный inventory согласовывать как Architect decision, не выводя наличие установки из принятия proof route и не разрешая автоматическую установку.`
- created_at: `2026-11-27 00:53 +0300`
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
- trigger_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md`
- symptom: `В Planner CENSOR 14:47 пришлось уточнить bootstrap readiness: local cache и SqlPackage должны проверяться после назначенного setup, тогда как SDK, Python и runtime проверяются до него.`
- process_gap: `Executable recipe смешивала заранее предоставляемые inputs с outputs, создаваемыми самим setup, оставляя циклическое требование готового кеша перед его подготовкой.`
- suggested_fix: `В source-owned Planner completion и code-draft template отдельно перечислять pre-setup inputs, outputs разрешённого setup и post-success checks перед использованием outputs. Missing input должен останавливать зависимый шаг; отсутствие ещё не созданного output не должно запрещать его согласованный bootstrap. Сохранить существующие лимиты attempts и stop при error, interruption или unknown outcome.`
- created_at: `2026-11-27 00:53 +0300`
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
- trigger_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md`
- symptom: `Продолжение SDK proof потребовало отдельного A4 о scoped загрузке пяти selectors из локального data file: прежний handoff ожидал передачу environment через следующий launch, не определяя фактический транспорт после facade.`
- process_gap: `Executable handoff не разделял готовность внешних project inputs и их доступность внутри sanitizing facade execution context; безопасный carrier и способ его потребления оставались неявными.`
- suggested_fix: `В source-owned Planner completion и code-draft template требовать явно согласованный транспорт несекретных private project selectors до зависимых checks. Для разрешённого local literal data carrier описывать regular/readable/non-symlink/ignored checks, exact allowlist без команд и подстановок, связывание проверки и загрузки с теми же bytes в одном scoped shell без xtrace и presence-only readback. Actual executable/version/inventory gates сохранять отдельно; facade sanitization не ослаблять, credentials оставлять wrapper-owned. Различие project Python и engine PYBIN повторно не материализовывать.`
- created_at: `2026-11-27 01:01 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-004
- status: `open`
- priority: `P?`
- role: `Planner`
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
- trigger_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md`
- symptom: `Planner CENSOR 14:47 добавил остановку при ошибке и exclusive run-directory creation в preparation recipes; прежние guard-команды сами по себе не обеспечивали прекращение блока до mkdir/clone. Фактическое перезаписывание данных не наблюдалось.`
- process_gap: `Syntax-only проверка shell recipe не доказывает fail-closed control flow; текстовое требование stop может расходиться с исполнением после nonzero guard.`
- suggested_fix: `В source-owned Planner completion и code-draft template требовать явную передачу отказа каждого guard до следующей мутации, guarded flow либо проверенную errexit boundary, symlink-parent checks и exclusive creation принадлежащих запуску directories/files. Ожидаемый negative rc захватывать отдельным if-блоком, сохраняя остальные guards. Syntax-only green не объявлять доказательством остановки.`
- created_at: `2026-11-27 01:06 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-005
- status: `open`
- priority: `P?`
- role: `Planner`
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
- trigger_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md`
- symptom: `Planner CENSOR 14:47 уточнил ambiguous cache identity: launcher/package/manifest hashes и physical cache root должны сохраняться, но штатная CLI диагностика вправе менять cache metadata. Фактический cache-drift failure этим evidence не доказан.`
- process_gap: `Proof contract не отделял immutable identity от допустимого изменения operational metadata, оставляя риск ложного отказа при требовании полной неизменности cache bytes.`
- suggested_fix: `В source-owned Planner reviewability guidance и code-draft template для stateful tool/cache proof явно перечислять immutable artifacts и hashes, physical identity, mutable metadata и допустимые изменения. Before/after assertions должны проверять этот объявленный набор; полную побайтную неизменность кеша требовать только при обоснованном contract. Сохранить actual runtime readback и отдельные authority gates.`
- created_at: `2026-11-27 01:06 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-006
- status: `open`
- priority: `P?`
- role: `Reviewer`
- owner: `Reviewer`
- promotion_class: `canon_update`
- target_canon_path: `null`
- target_repo_scope: `null`
- delivery_mode: `null`
- execution_kind: `null`
- execution_ref: `null`
- delivery_refs: `null`
- handled_ref: `null`
- promoted_at: `null`
- handled_at: `null`
- trigger_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md`
- symptom: `При Reviewer finalization bundle --check вернул rc0 с17 paths, но без обязательного Coder JUnit; explicit repo-relative refs восстановили полный набор18 paths.`
- process_gap: `Успешный bundle check проверил разрешённый inventory, но не обнаружил пропущенный обязательный asset. Reviewer-facing template не давал отдельного примера refs для non-visual proof artifacts.`
- suggested_fix: `В source-owned review template и reviewer checklist добавить пример полного repo-relative asset ref и требование сверять каждый объявленный обязательный artifact с inventory planveyor_plan_bundle --print/--check. Одного rc0 или общего количества paths недостаточно; существующие resolver, authority и lifecycle semantics сохранить.`
- created_at: `2026-11-27 01:11 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

## Notes
- Если suggestion уже promoted в live plan/canon/helper, triage helper должен обновить `status`, `target_canon_path`, `target_repo_scope`, `delivery_mode`, а не переписывать historical fields по памяти.
- `promoted`/`handled` rows должны хранить literal execution refs; `delivery_refs` допускает только `null` или `; `-separated literal refs.
- `triaged` rows требуют non-`P?` `priority`, literal target/delivery carrier и execution/delivery refs либо explicit `triage_note` decision.
- `deferred` rows должны хранить owner, reason/revisit trigger в `triage_note` и literal `delivery_refs` либо explicit null-delivery reason.
- `docs/followups/*` остаётся отдельной carrier family: process-improvement row не дублируется туда без отдельного явного follow-up decision.

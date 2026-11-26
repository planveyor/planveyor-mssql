# Process improvements backlog — 261125 0958 contract upgrade 3f5b2c1 bbf11a7

**Date:** 2026-11-26 03:33 +0300
**Source ref:** `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md`
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
- trigger_ref: `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md`
- symptom: `Первый дополнительный write-confinement guard завершился sandbox_apply rc71 до SDK execution; потребовались Architect triage и отдельное Owner решение Q5.`
- process_gap: `Первоначальная recipe не доказывала применимость дополнительного профиля в текущем tool execution context до SDK action; lookup equality не закрывала этот prerequisite.`
- suggested_fix: `В source-owned Planner prompt для объявленных recipes с write profile заранее фиксировать context однократного применения профиля и контрольные allow/deny проверки до SDK. Отказ применения классифицировать отдельно от SDK result; иной context запускать только после отдельного разрешения, без автоматического retry или ослабления границы записи.`
- created_at: `2026-11-26 03:23 +0300`
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
- trigger_ref: `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md#Architect-suggestions`
- source_ref: `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md`
- symptom: `При продолжении по Q8 canonical coder-proof.json уже содержал failed dotenv-missing outcome, а draft назначал тот же путь новому результату; сохранение истории пришлось отдельно уточнять Architect.`
- process_gap: `Recipe определяла canonical proof paths, но не определяла retention предыдущего failed carrier перед его обновлением после разрешённого same-contract продолжения.`
- suggested_fix: `В source-owned Planner completion и code-draft template для таких продолжений явно задавать immutable historical carrier и его hash, отдельный учёт новой попытки и правило обновления canonical результата. Existing same-hash history переиспользовать, mismatch останавливать без overwrite; retention не даёт разрешения на повтор execution.`
- created_at: `2026-11-26 03:23 +0300`
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
- trigger_ref: `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md#coder-qa`
- source_ref: `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md`
- symptom: `После успешного setup с make/wrapper rc0 и cache6/6 первый Coder db-proof остановился с dotenv-missing rc2/2 до Publish; для внешней подготовки конфигурации потребовались Q7/Q8.`
- process_gap: `Planner handoff учитывал доступный cache inventory, но готовность administrator-owned конфигурации для обязательной live lane оставалась неявной. Существующие PI о cache inventory, write profile и retention failed proof этот случай не покрывают.`
- suggested_fix: `В source-side Planner readiness для live lane явно учитывать внешнюю подготовку конфигурации как prerequisite, используя имеющееся уведомление Owner либо обозначая готовность как неподтверждённую с owning routing. Роль не читает и не проверяет файл; уведомление не заменяет фактические wrapper config/target guards и JUnit proof.`
- created_at: `2026-11-26 03:29 +0300`
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
- trigger_ref: `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md#planner-suggestions`
- source_ref: `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md`
- symptom: `На Planner finalize потребовалось отдельно уточнить, что профиль с записью только в .tmp применяется к preflight/setup/build, а обязательный durable JUnit под docs/code_reviews/assets создаётся через ранее согласованную Q1 project lane. Runtime write denial для JUnit не наблюдался.`
- process_gap: `Канон отдельно задаёт lane preconditions, allowed mutation inventory и retention artifacts, но не требует явного сопоставления каждой фазы, её разрешённых writable paths и обязательного artifact destination. Работоспособность профиля сама по себе эту совместимость не подтверждает.`
- suggested_fix: `В source-owned Planner completion для recipes с ограничением записи добавить проверку phase → authorized writable paths → mandatory artifact destination. До handoff явно закреплять применимый permission envelope каждой фазы; несовместимость направлять на owning triage без расширения разрешений. Уже согласованные разные lane boundaries сохранять.`
- created_at: `2026-11-26 03:33 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

## Notes
- Если suggestion уже promoted в live plan/canon/helper, triage helper должен обновить `status`, `target_canon_path`, `target_repo_scope`, `delivery_mode`, а не переписывать historical fields по памяти.
- `promoted`/`handled` rows должны хранить literal execution refs; `delivery_refs` допускает только `null` или `; `-separated literal refs.
- `triaged` rows требуют non-`P?` `priority`, literal target/delivery carrier и execution/delivery refs либо explicit `triage_note` decision.
- `deferred` rows должны хранить owner, reason/revisit trigger в `triage_note` и literal `delivery_refs` либо explicit null-delivery reason.
- `docs/followups/*` остаётся отдельной carrier family: process-improvement row не дублируется туда без отдельного явного follow-up decision.

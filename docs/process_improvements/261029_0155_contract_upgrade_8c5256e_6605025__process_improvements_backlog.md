# Process improvements backlog — 261029 0155 contract upgrade 8c5256e 6605025

**Date:** 2026-10-29 09:11 +0300
**Source ref:** `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md`
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
- trigger_ref: `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md`
- symptom: `Лишняя пустая строка EOF нового code draft обнаружилась только после первого stage и потребовала повторных final gates.`
- process_gap: `Reviewer hygiene проверяет tracked diff и новые файлы через rg на trailing whitespace/merge markers, но явно не покрывает лишние пустые строки EOF untracked Markdown.`
- suggested_fix: `Уточнить source-owned Reviewer hygiene: до положительного verdict проверять новые Markdown-файлы canonical exact bundle также на лишние пустые строки EOF, без предварительного stage; сохранять explicit receipt результата.`
- created_at: `2026-10-29 09:04 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-002
- status: `open`
- priority: `P?`
- role: `Coder`
- owner: `Coder`
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
- trigger_ref: `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md`
- symptom: `После успешных offline checks 74/0/0 и первого live SQL proof активные Problem/summary/Risks и draft preconditions продолжали утверждать current red67/1/0 и отсутствие SQL; исправление потребовалось в Coder CENSOR.`
- process_gap: `Primary Coder completion не выделяет явную проверку устаревших фактических предпосылок после закрытия blocker; конкретная stale-live-wording проверка находится в CENSOR.`
- suggested_fix: `В source-owned coder_status_driven.md добавить в completion pass ссылку на существующую stale-live-wording проверку coder_censor.md: согласовать активные Problem/summary/Scope/Risks и draft preconditions с фактическими receipts, сохраняя chronological evidence append-only.`
- created_at: `2026-10-29 09:08 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-003
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
- trigger_ref: `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md`
- symptom: `В первоначальной AC8 matrix negative fixtures могли отказываться только из-за byte-mismatch и оставаться зелёными после удаления independent no-override, forbidden-wording или UTF-8 guard.`
- process_gap: `Planner completion/CENSOR не требует явно проверить, что negative fixture изолирует заявленный guard, а отказ не обеспечивается другим условием.`
- suggested_fix: `Добавить в source-owned Planner completion/CENSOR bounded проверку независимости negative proof: назвать причину ожидаемого отказа и при маскировании guard через equality использовать paired одинаковые unsafe baseline/current inputs. Зафиксировать cases в plan и draft до Coder без навязывания production implementation.`
- created_at: `2026-10-29 09:11 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

## Notes
- Если suggestion уже promoted в live plan/canon/helper, triage helper должен обновить `status`, `target_canon_path`, `target_repo_scope`, `delivery_mode`, а не переписывать historical fields по памяти.
- `promoted`/`handled` rows должны хранить literal execution refs; `delivery_refs` допускает только `null` или `; `-separated literal refs.
- `triaged` rows требуют non-`P?` `priority`, literal target/delivery carrier и execution/delivery refs либо explicit `triage_note` decision.
- `deferred` rows должны хранить owner, reason/revisit trigger в `triage_note` и literal `delivery_refs` либо explicit null-delivery reason.
- `docs/followups/*` остаётся отдельной carrier family: process-improvement row не дублируется туда без отдельного явного follow-up decision.

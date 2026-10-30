# Process improvements backlog — 261030 0221 shared rules pinned source check

**Date:** 2026-10-30 08:55 +0300
**Source ref:** `docs/plans/261030_0221_shared_rules_pinned_source_check.md`
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
- trigger_ref: `docs/plans/261030_0221_shared_rules_pinned_source_check.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261030_0221_shared_rules_pinned_source_check.md`
- symptom: `Первый make db-state из login shell выбрал Python 3.15 и отказал до SQL; та же команда в подготовленной non-login launch environment с Python 3.12 завершилась успешно.`
- process_gap: `Shell-режим terminal tool первоначально не соответствовал выбранной launch environment; source-owned runbook требует Python 3.12 также в login shell, поэтому результаты этих контуров необходимо различать.`
- suggested_fix: `Уточнить в source-owned stack-sibling runbook выбор shell-режима согласно явно объявленной среде и проверку фактического project interpreter перед командой; отдельно запретить считать non-login success доказательством login readiness, автоматически менять PATH/home/config или подменять project interpreter engine PYBIN.`
- created_at: `2026-10-30 08:44 +0300`
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
- trigger_ref: `docs/plans/261030_0221_shared_rules_pinned_source_check.md#Coder-objections`
- source_ref: `docs/plans/261030_0221_shared_rules_pinned_source_check.md`
- symptom: `Отрицательное упоминание scope expansion в primary Coder completion вызвало plan_lint rc1 и дополнительный Coder intake при неизменных implementation targets и proof.`
- process_gap: `Правило об обоснованном route class в той же строке явно описано в coder_censor.md, но primary Coder completion не ссылается на него.`
- suggested_fix: `В source-owned coder_status_driven.md добавить ссылку на существующее правило CENSOR: описывать неизменность конкретных targets либо сопровождать неоднозначную scope-формулировку фактически обоснованным literal route class в той же строке; класс не выбирать автоматически, lint/runtime/status semantics не менять.`
- created_at: `2026-10-30 08:48 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-003
- status: `open`
- priority: `P?`
- role: `Planner`
- owner: `Architect`
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
- trigger_ref: `docs/code_reviews/261030_0221_shared_rules_pinned_source_check.md#Исправление-прежнего-обоснования-doctor`
- source_ref: `docs/plans/261030_0221_shared_rules_pinned_source_check.md`
- symptom: `Исторический review ошибочно признавал consumer doctor доказательством shared-byte integrity; текущий план потребовал отдельного comparator и явного исправления этого обоснования.`
- process_gap: `Source-owned stack-sibling runbook описывает успешный doctor и pin equality, но явно не обозначает отсутствие проверки равенства содержимого с pinned template, что оставляет возможность повторить ошибочное толкование.`
- suggested_fix: `В docs/guides/stack-sibling.md и docs/guides/stack-sibling.ru.md рядом с описанием doctor кратко указать его границы: pin/runtime equality, наличие managed paths и merge-state; content equality требует отдельно объявленного byte-comparison proof. Не менять CLI, runtime semantics или обязательные проверки.`
- created_at: `2026-10-30 08:51 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

### PI-004
- status: `open`
- priority: `P?`
- role: `Reviewer`
- owner: `Reviewer`
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
- trigger_ref: `docs/plans/261030_0221_shared_rules_pinned_source_check.md#Evidence-chronological-append-only`
- source_ref: `docs/plans/261030_0221_shared_rules_pinned_source_check.md`
- symptom: `Первый lint нового review без UI вернул missing_visual_receipt_fields из-за отсутствующего Visual env; явная строка N/A исправила report без изменения implementation или proof.`
- process_gap: `Профиль без UI в reviewer_status_driven.md сокращает visual noise, но недостаточно явно отделяет неприменимость visual acceptance от обязательного поля схемы review artifact.`
- suggested_fix: `В source-owned reviewer_status_driven.md рядом с профилем без UI явно потребовать Visual env: N/A (why=no UI change), сохранив текущие lint semantics и отсутствие screenshot/browser обязанностей для таких задач.`
- created_at: `2026-10-30 08:55 +0300`
- triage_note: `auto-collected from memory-finalize general lane`

## Notes
- Если suggestion уже promoted в live plan/canon/helper, triage helper должен обновить `status`, `target_canon_path`, `target_repo_scope`, `delivery_mode`, а не переписывать historical fields по памяти.
- `promoted`/`handled` rows должны хранить literal execution refs; `delivery_refs` допускает только `null` или `; `-separated literal refs.
- `triaged` rows требуют non-`P?` `priority`, literal target/delivery carrier и execution/delivery refs либо explicit `triage_note` decision.
- `deferred` rows должны хранить owner, reason/revisit trigger в `triage_note` и literal `delivery_refs` либо explicit null-delivery reason.
- `docs/followups/*` остаётся отдельной carrier family: process-improvement row не дублируется туда без отдельного явного follow-up decision.

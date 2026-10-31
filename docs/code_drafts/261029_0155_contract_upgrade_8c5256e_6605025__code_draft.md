# Code draft: Адаптация контракта Planveyor 8c5256e → 6605025

**Date:** 2026-10-29 03:11 +0300
**Cluster:** process
**Related plan:** `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md`
**Author role:** Planner
**Status:** draft

## Meta (machine-readable JSON)

```json
{
  "code_draft_meta": {
    "plan": "docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md",
    "cluster": "process",
    "targets": [
      {
        "path": ".agents/skills/planveyor-plan-draft/SKILL.md",
        "kind": "doc"
      },
      {
        "path": ".copier-answers.yml",
        "kind": "config"
      },
      {
        "path": "AGENTS.md",
        "kind": "doc"
      },
      {
        "path": "docs/_meta/planveyor_contract_authority.v1.json",
        "kind": "config"
      },
      {
        "path": "docs/adr/README.md",
        "kind": "doc"
      },
      {
        "path": "docs/code_drafts/_template.md",
        "kind": "doc"
      },
      {
        "path": "docs/plans/README.md",
        "kind": "doc"
      },
      {
        "path": "docs/plans/_template.md",
        "kind": "doc"
      },
      {
        "path": "docs/playbooks/review_docs_staged_or_commit.md",
        "kind": "doc"
      },
      {
        "path": "docs/playbooks/review_staged_or_commit.md",
        "kind": "doc"
      },
      {
        "path": "docs/roles/architect.md",
        "kind": "doc"
      },
      {
        "path": "docs/roles/planner.md",
        "kind": "doc"
      },
      {
        "path": "docs/roles/reviewer.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/architect_docs_finalize_general.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/architect_status_driven.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/architect_track_innovations.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/architect_track_process_collab.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/architect_track_process_roles.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/coder_docs_finalize_general.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/manager_collab_pipeline.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/planner_docs_finalize_general.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/planner_status_driven.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/reviewer_docs_finalize_general.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/reviewer_status_driven.md",
        "kind": "doc"
      },
      {
        "path": "scripts/test_sql.py",
        "kind": "py"
      }
    ],
    "deleted_paths": [],
    "machine_authority_decision_ref": {
      "applicability": "not_applicable",
      "reason_code": "unchanged_structured_consumer",
      "carrier_sha256": "a7146838187c8628e5d40e7b7340ec50d9032d99856aefcc5787fd1edba32f39"
    }
  }
}
```

## Provenance / session context

- Source plan provenance: `docs/plans/261029_0155_contract_upgrade_8c5256e_6605025.md#Plan-provenance--session-context`; draft создан отдельно в текущей Planner-сессии.
- Relation: `created-here`
- Thread ID: `<REDACTED>`
- Parent thread ID: `N/A (why=not exposed by env, wrapper receipts, or session stats)`
- Session SID: `N/A (why=.planveyor.session.planner is missing or empty)`
- Launch surface: `unknown (why=no env, wrapper receipt, or session stats origin identified the launch surface)`
- Captured from: `env`
- Captured at: `2026-10-29T00:10:36Z`

Источник — current planveyor_plan_provenance_context --session-key planner. Это origin audit, не Context source/rerun receipt и не rollout authority. Derived MAD ref взят штатным stub helper после current canonical oracle; semantic core не копируется. Admission baseline N/A (why=не checkpoint-V2 implementation).

## Purpose

Принять 24 уже доставленных upgrade paths и выполнить единственный дополнительно принятый Architect repair scripts/test_sql.py: убрать неверный shared-prefix==pre-upgrade-HEAD запрет при сохранении полного local-tail/override guards и добавить bounded regression coverage AC8. Current targets=25; прежний contract24 — historical anchor only. README/local bodies/SQL/production harness/runtime не меняются.

## Reviewability preflight receipt

- `proof-path class`: standard primitives — существующие make и trusted external facade.
- `mandatory primary lane`: consumer doctor, plan/doc lint, fresh strict bundle preflight на 25 targets; Coder/Reviewer независимо выполняют полные offline make цели после test repair, затем первые последовательные db-proof. До fresh make test green и doctor green SQL не запускается.
- `mandatory non-primary carrier / contextual lane`: байты README и 16 локальных секций восьми carriers относительно baseline; разные current JUnit Coder/Reviewer; make db-state — contextual-only, не SQL acceptance.
- `exact helper path + support files`: Makefile, scripts/sql.py (EXPECTED_TESTS, parse_junit, Stack.proof), scripts/test_sql.py; внешние scripts/consumer_contract.py, scripts/plan_lint.py, scripts/doc_lint.py, scripts/review_target_snapshot.py и scripts/planveyor.zsh выбранного runtime. Новый helper не создаётся.
- `dependent tests / dependent docs / known consumer paths`: writable scripts/test_sql.py::RepositoryContractTests (actual repository assertion и synthetic AC8 matrix) → existing scripts/sql.py test runner → Makefile make test → Coder/Reviewer offline gate. Pinned shared byte integrity отдельно удерживает mandatory canonical consumer_doctor; green make test его не заменяет. README, восемь local carriers, production scripts/sql.py, SQL и runtime read-only.
- `preconditions / seed-discovery`: Owner reset/env-copy уже выполнены; единственный Coder setup успешен 03:27 и не повторяется. Cache готов, offline без restore. Historical red67/1/0 закрыт Coder full suite74/0/0 и отдельным doctor green; first Coder live proof9/0/0/0/binding находятся в plan Evidence 04:02–04:05. Independent Reviewer proof остаётся следующим gate. Применяется только проверенный process-only Python3.12 prefix из plan Commands; каждый разрешённый live proof заново проверяет designated dev fresh guard, без чтения credential values ролью.
- `reroute rule`: любой red/missing lane блокирует handoff; доказанная update regression с необходимой правкой SQL/harness/docs требует Architect-owned scope решения до repair. При неизменном контракте — same-contract reroute, без повторного setup/SQL auto-retry.
- `perceptual truth-source split`: repo-backed bytes/helper JSON/strict JUnit — truth; UI/screenshot/OCR N/A (why=no UI change).
- Stateful proof: в каждом независимом запуске discovery-or-seed = fresh guard; Publish/RunAll/formatter = receipt-reuse-only одной удерживаемой конфигурации. Stable fields: designated dev identity без публикации значений, role, HEAD, canonical bundle_sha256 и relative JUNIT path. Потеря identity/context — hard-fail без reseed/auto-retry. Exact observer boundary = новый XML собственного RunAll/formatter; notice/success text != mutation truth; next canonical readback = strict parse того же JUnit и его SHA-256.
- Runtime-lineage preflight: HEAD и canonical target bundle_sha256 до/после каждого proof должны совпадать; target edit требует нового proof. Prerequisite/build failure возвращается owning Coder, не выдаётся за новый SQL defect.
- Retention: JUnit и immutable reviewer support под docs/code_reviews/assets/261029_0155_contract_upgrade_8c5256e_6605025/ — durable operator/review evidence; .tmp/ — transient local sanity only.

Truth-host fixture matrix: N/A (why=fan-in/readback helper не меняется).
Receipt schema emitter inventory: N/A (why=локальные validator/parser/schema fields не меняются; source-owned general PI contract уже доставлен без ручного порта).
Manager command fan-out: N/A (why=dispatch path unchanged; новый owner-facing command не добавляется).
API/payload parity: N/A (why=проектный API/payload не меняется).
Golden Path: N/A (why=отдельная golden-path lane не вводится; upgrade/closeout идут по явно назначенному source-owned stack-sibling guide).

## Targeted changes (by file)

Все 25 metadata targets существуют. Первые 24 — доставленный contract delta без ручного переписывания shared bytes; scripts/test_sql.py — единственный bounded repair target после доказанного upgrade failure и Architect triage. Нового implementation file нет.

- `.agents/skills/planveyor-plan-draft/SKILL.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `.copier-answers.yml`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `AGENTS.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/_meta/planveyor_contract_authority.v1.json`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/adr/README.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/code_drafts/_template.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/plans/README.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/plans/_template.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/playbooks/review_docs_staged_or_commit.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/playbooks/review_staged_or_commit.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/roles/architect.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/roles/planner.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/roles/reviewer.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/architect_docs_finalize_general.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/architect_status_driven.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/architect_track_innovations.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/architect_track_process_collab.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/architect_track_process_roles.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/coder_docs_finalize_general.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/manager_collab_pipeline.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/planner_docs_finalize_general.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/planner_status_driven.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/reviewer_docs_finalize_general.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `docs/tools/prompts/reviewer_status_driven.md`: принять уже доставленные upgrade bytes; сохранять существующие local bodies, если они есть.
- `scripts/test_sql.py`: только RepositoryContractTests local-tail/shared-upgrade assertion и AC8 regression fixtures; production SQL/parser/proof/JUnit/target/redaction/Git/secret behavior не менять.

Existing read-only baseline surfaces = README, Makefile, scripts/sql.py, весь sql/ и восемь local bodies. Target delta = existing scripts/test_sql.py; новое поведение ограничено его offline test assertions, нового production helper/file/schema нет. План, этот draft, единственный review и explicit evidence assets добавляются к финальному lifecycle bundle отдельно; origin plan/README/SQL/production harness/JUnit не входят в code_draft_meta.targets.

## Bounded regression cases (AC8)

Реальная RepositoryContractTests.test_shared_bytes_and_no_process_override и fixtures используют одну test-local assertion path; Coder выбирает внутреннюю реализацию в этом же файле, без второй логики только для fixtures. Для baseline/current требуется ровно по одному полному canonical H2 «Локальные правила стека» и H2 override, в этом порядке; inline/неполное совпадение не boundary. Heading распознаётся как полная строка без line ending; полный tail с первого H2 до EOF сравнивается byte-for-byte без нормализации. Actual repository baseline = git HEAD:path; shared prefix не сравнивается с HEAD и не фиксируется current-prefix константой. Pinned prefix truth остаётся только consumer_doctor. AC8 matrix в plan — полный контракт; здесь тот же closure map:

- AC8-P0: baseline/current без изменений — pass для каждого LOCAL_FILES; existing private-path/plan-specific/full-inventory/no-override guards сохранены.
- AC8-P1: synthetic changed shared prefix при byte-identical полном local tail — pass для каждого LOCAL_FILES; не synthetic SQL proof и не shared-source approval.
- AC8-N1: mutation stack local body при unchanged prefix/override — fail для каждого LOCAL_FILES.
- AC8-N2: mutation override body при unchanged stack body — fail для каждого LOCAL_FILES.
- AC8-N3: missing stack/override canonical H2 в baseline либо current, включая inline/неполное совпадение вместо boundary — fail.
- AC8-N4: duplicate stack H2, duplicate override H2 либо reversed order в baseline либо current — fail; first-match не выбирает green branch.
- AC8-N5: enabled/modified current override с оставленным N/A comment — fail; также baseline/current byte-identical с enabled override — fail. Independent guard принимает только единственную effective строку «Переопределение» с существующим disabled N/A status; substring N/A не разрешает override.
- AC8-N6: existing forbidden private-path/plan-specific pattern внедрён либо обязательное full-inventory wording удалено — fail; тот же fail обязателен для baseline/current с одинаковой unsafe mutation, чтобы equality не скрыла удалённый semantic guard.
- AC8-N7: trailing byte/текст в current после tail при unchanged baseline — fail; отдельно одинаковые baseline/current с invalid UTF-8 local body — fail. EOF continuity и strict decoding доказаны независимо.

Все mutations — transient in-memory/существующая temporary fixture, реальные carriers/README не меняются. Negative cases наблюдают отказ той же assertion path, не skip/xfail/bypass/mock verdict. Existing девять SQL identities, все parser/JUnit/guard/Git/redaction/secrets cases остаются. Coder связывает IDs matrix с фактическими testcase/subtests в plan Evidence, Reviewer проверяет карту и весь suite независимо. Количество будущих unittest не фиксируется на старых 67; red67/1/0 исторический до fresh full make test.

## Review route

- Primary artifact: `docs/code_reviews/261029_0155_contract_upgrade_8c5256e_6605025.md`
- Lane type: code review — mixed contract bundle, включая .copier-answers.yml и .agents carrier; один live host.
- Current review target: BUNDLE=current по canonical producer. Reviewer сохраняет полный immutable support и compact risk receipt по своему штатному prompt; XML и proof receipts должны быть явно названы в этом же review.

## Patch sketch (keep it small)

Bounded test repair материализован в scripts/test_sql.py, фактические offline/first Coder SQL receipts находятся в plan Evidence 04:02–04:06. Steps сохраняют согласованный порядок исполнения и независимый Reviewer gate:

1. Coder читает current plan/draft, Architect triage 03:38 и закрытые Q1/Q2; current inventory=25, первые 24 delivered, единственный repair target=scripts/test_sql.py. README и 16 local sections сверяются с baseline HEAD=9c445fd7d1f505ff761a3a2c1e86227fa1bad2f1. Source/runtime/SQL/production harness не исправлять.
2. Setup уже успешен и не повторяется. Coder реализует только bounded assertion/fixtures AC8 в scripts/test_sql.py, сохраняет existing guards, не копирует current shared prefix в expected-константу. После repair — consumer doctor, plan/doc lint и четыре full offline make цели с уже проверенным process-only Python3.12 prefix. Make/wrapper rc отдельно; red любого mandatory gate блокирует SQL. Приватные пути/argv/config/raw streams не сохраняются.
3. Все target bytes завершены до proof. Coder выполняет canonical snapshot + HEAD до proof, собственный make db-proof, затем snapshot + HEAD и JUnit SHA-256. Полный список девяти identities берётся из plan и scripts/sql.py::EXPECTED_TESTS, а не из исторической анкеты.
4. Reviewer независимо проверяет diff, local-body/README parity, offline цели, make db-state и свой make db-proof после Coder. Shared dev DB сериализована; Reviewer не запускает setup/Extract. В contracts/risk lanes только один designated Reviewer SQL proof; второй lane переиспользует current repo-backed evidence, не публикует повторно.
5. В единственном review явно связать оба JUnit, их SHA-256, команды, make/wrapper rc, HEAD и одинаковый canonical bundle_sha256. Строго проверить девять identities, все suite/root counters и отсутствие failure/error/skipped; totals сами по себе недостаточны.
6. После current review выполнить strict final --check и передать Architect. Он делает contextual make db-state и current native exact closeout только после Arch Review; semantic и docs commits — разные gates. Planner/Coder не stage/commit/Done writers.

Точные runnable команды и role order находятся в plan → Commands; это один контракт, не альтернативный harness.

## Critical invariants / traps / bypass paths

- Invariant: SQL proof относится к неизменным exact target bytes. Trap: одинаковые вручную напечатанные hash либо прежний XML. Closure: canonical producer до/после + HEAD + свежий JUnit собственного RunAll; target mutation делает proof stale.
- Invariant: текущий отчёт содержит T1–T8 и real-table canary. Trap: исторический single-test 1/0/0/0 или green totals при red/unknown/duplicate testcase. Closure: strict parse, девять exact identities, 9/0/0/0.
- Invariant: Coder/Reviewer используют разные Git-untracked JUNIT paths. Trap: staged Coder XML перед Reviewer proof либо reuse того же отчёта. Closure: разные literal paths; до своего db-proof каждый path достоверно untracked, без stage до review. Canary сохраняет dbo.Products типа U без FakeTable/NewTestClass/бизнес-данных.
- Invariant: prefix upgrade допустим только вместе с unchanged complete local tail и отдельным pinned-source doctor green. Trap: удалить весь test, сравнить только override, принять first-match boundary, оставить N/A substring рядом с enabled override либо отключить guard. Closure: AC8-P0/P1/N1–N7 и полные make test + consumer_doctor; один green не отменяет red другого.
- UI/bypass proof: N/A (why=no UI change). Synthetic additions ограничены AC8 внутри scripts/test_sql.py; новых production/helper/schema/corpus carriers нет.

## Assumptions / risks

Cache уже подготовлен единственным успешным setup; потеря cache — owning-role blocker, нового setup/restore автоматически нет. Missing/invalid dev prerequisites не исправляются серверными изменениями. Doctor/preflight/ready не закрывают red make test, SQL или review. README wording вынесено Owner в отдельный тред после Э6; режимы здесь не редактируются.

## Notes for Coder

Plan важнее draft. Scope widening до Architect решения запрещён. Credentials читает только scripts/sql.py. Reset/init/env-copy/Extract/модели, home/PATH, runtime edits и push не разрешены. Конкретный Owner native_existing override действует в этом окне; narrow разовые .git approvals сохраняются.

## Review stamps (append-only)

- [2026-10-29 03:11 +0300] (Planner) Финализированы metadata/24 targets, derived N-A ref, proof/retention/role-order contract; новый executable sketch не оставлен seed-only. NO SUGGESTIONS (reviewed; no changes required) — после этого completion pass.
- [2026-10-29 03:18 +0300] (Planner) NO SUGGESTIONS (повторно прочитаны 24 targets и steps 1–6; fresh guard, разные untracked JUnit, serial Reviewer proof и native Architect-only closeout уже literal; contract draft не меняется).
- [2026-10-29 03:48 +0300] (Planner) По repo-backed Architect triage выполнен current-plan refinement 24→25: добавлен только scripts/test_sql.py, restamp-нуты Purpose/receipt/steps/risks, AC8-P0/P1/N1–N7 и no-repeat setup. Прежние contract24 stamps — historical anchor only; repair/test/SQL в Planner не выполняются.
- [2026-10-29 03:55 +0300] (Planner) Повторно прочитаны metadata25/steps/AC8; N5/N6/UTF-8 ветка N7 теперь отдельно изолируют semantic guards при равных unsafe baseline/current bytes. NO SUGGESTIONS (после этого уточнения дополнительных правок contract не требуется; implementation/SQL не выполнялись).
- [2026-10-29 04:11 +0300] (Coder) Evidence-only restamp: stale preconditions/patch wording приведены к фактическим plan receipts 04:02–04:06 — full suite74/0/0 и first Coder live proof9/0/0/0 уже выполнены, independent Reviewer gate ещё открыт. Metadata25/AC8/execution order не менялись; implementation bytes и canonical bundle hash сохранены, нового SQL/setup не было.

# Code review: Адаптация sibling под SQL Server 2019 / Northwind

**Target:** BUNDLE=current bundle_sha256=51ebdc9ffdf974603e58538df1270ec68c3eb0e53e761c5d83ffb5705b6fbf08
**Spec:** docs/plans/261011_1523_stack_adaptation.md
**Date:** 11.10.2026 22:16
**Status:** ✅ OK

ОК: текущих S1/S2/S3 findings нет. Canonical B1/B2/B3 сохранены как historical-fixed; surviving contracts:C1 закрыт собственным повтором прежнего failing fixture. Собственные 56 offline tests и новый независимый Reviewer SQL proof прошли; target до и после proof совпадает.

## Rerun context

- Rerun mode: incremental.
- Baseline artifact: docs/code_reviews/261011_1523_stack_adaptation.md, previous same-file red review 11.10.2026 20:18/target 171833e40098d72075515cbbc29f20e0021325aea5b7479afe0111a872bf8302; pre-rewrite SHA-256=fe30158edcde30e0bc107428a0e8fbe1094cf8c22ab7a7c77229075cad12ca65.
- Это четвёртый same-file review cycle, закрывающий Coder rerun window 21:37; предыдущий red verdict 20:18 остаётся историей B3/contracts:C1.
- Rerun scope: actual plan/draft, Decisions/closed Coder Q1/current rerun window, helper-selected current Risk support, текущие scripts/sql.py/scripts/test_sql.py и собственные обязательные checks/proof.
- Target delta от предыдущей generation: только scripts/sql.py и scripts/test_sql.py; 58 остальных canonical file records совпали. Предыдущие source reads reused только для этих unchanged bytes, включая Imported, manifests, SQL projects/canary, Makefile, README/brief и восемь local carriers.
- Reused evidence: historical blocker/support lineage и unchanged source inspection. Прежние commands/JUnit не объявляются текущим acceptance; обязательные команды и Reviewer SQL proof выполнены заново.
- Исторические immutable supports сохранены: `docs/code_reviews/assets/261011_1523_stack_adaptation/reviewer_code_risk_20261011T145607Z_sol_ultra_v2.json`, SHA-256=8f7680e78721028b49dc77b82f34767d3167d2cdcbb65566efe847e03ff1bd86; `docs/code_reviews/assets/261011_1523_stack_adaptation/reviewer_code_risk_20261011T160014Z_sol_ultra_v3.json`, SHA-256=6502913dd611b007b79191f0b287a53e84e86a9b09eb873d3815f42dd3053255; `docs/code_reviews/assets/261011_1523_stack_adaptation/reviewer_code_risk_20261011T170108Z_sol_ultra_v4.json`, SHA-256=773759da73b91de29f01fe61eb4deb1e41e276b4d9fb11bfb0d60447d2e7a240. Compact supersession принадлежит Risk; Contracts её не редактировала.

## reviewer_code_risk - GPT-6.1 Sol ultra

- Lane status: complete
- Target snapshot: BUNDLE=current bundle_sha256=51ebdc9ffdf974603e58538df1270ec68c3eb0e53e761c5d83ffb5705b6fbf08
- run_id: risk:20261011T185929Z:sol_ultra_v5
- runner_id: codex_collab
- session_key: /root/reviewer_code_risk_sol_xhigh_v2
- sid: unknown
- profile: unknown
- model: gpt-6.1-sol
- reasoning_effort: ultra
- prompt_file: docs/tools/prompts/reviewer_status_driven.md
- written_at: 2026-10-11T18:59:29Z
- Coverage domains: correctness, tests quality, security/privacy, subprocess/timeouts, races/locks/atomicity, data/migrations, performance, observability, integrations, supply chain, failure semantics
- Findings: N/A (findings отсутствуют в текущей selected generation).
- No findings reason: прочитанный support подтверждает исходные B1/B2 refusals и B3 для existing/missing indexed leaf/ancestor, case-only index rename и NFD alias. Все negative cases дают отказ 2 до config/build/SQL, сохраняют index/старые bytes и не создают tracked XML. Genuine untracked neighbor/nested/literal positives, собственные 56 tests, девять independent fixtures и свежий guarded SQL proof прошли.
- Источник: самостоятельно helper-selected current carrier в `docs/plans/261011_1523_stack_adaptation.md::Evidence`; [current immutable support](assets/261011_1523_stack_adaptation/reviewer_code_risk_20261011T185929Z_sol_ultra_v5.json).
- Исходный артефакт: `docs/code_reviews/assets/261011_1523_stack_adaptation/reviewer_code_risk_20261011T185929Z_sol_ultra_v5.json`, 43257 bytes; SHA-256=320703ba7643ea72080aed1c55af20714a8b1040e54eeb4d46e8501c640be3cd.
- Независимая Risk reproduction matrix прочитана целиком: 9 tests/0 failures/0 errors, make/wrapper rc 0; real temporary Git/current filesystem и existing synthetic Fixture/FakeExecutor. Contracts эти девять fixtures заново не запускала, а выполнила свой original contracts:C1 fixture и current checked-in regressions.
- Limits: sid/profile unknown; setup/Extract не повторялись; SQL последовательный. Другие ОС/filesystems, concurrency и unsupported metadata tampering не проверялись.

## reviewer_code_contracts - GPT-6.1 Sol ultra

- Lane status: complete
- Target snapshot: BUNDLE=current bundle_sha256=51ebdc9ffdf974603e58538df1270ec68c3eb0e53e761c5d83ffb5705b6fbf08
- run_id: contracts:20261011T191652Z:sol_ultra_v5
- runner_id: codex_collab
- session_key: /root/reviewer_code_contracts_sol_xhigh_v2
- sid: unknown
- profile: unknown
- model: gpt-6.1-sol
- reasoning_effort: ultra
- prompt_file: docs/tools/prompts/reviewer_status_driven.md
- written_at: 2026-10-11T19:16:52Z
- Coverage domains: plan fidelity, architecture/design fit, maintainability, canon/materialization/build drift, API/schema, documentation/registry, integration semantics, config/deploy/rollout, review artifact truthfulness, accessibility/i18n, LLM/prompt/meta-review
- Uses plan lane-run artifact: `docs/plans/261011_1523_stack_adaptation.md::Evidence` → risk:20261011T185929Z:sol_ultra_v5.
- Finalizer proof: собственный selector selected/rc 0 при intake и непосредственно перед rewrite; current producer equality, собственные sequential make gates, db-state, original contracts:C1 rerun и свежий independent live proof.
- Findings: N/A (findings отсутствуют).
- No findings reason: actual scripts/sql.py теперь без раннего missing-leaf допуска читает полный trusted NUL-delimited index; NFD/casefold alias проверяется для отсутствующих и существующих путей, physical identity остаётся для existing files. Неизвестный inventory даёт отказ до config/actions. Original contracts:C1 теперь refusal=2/no recreation/config uncalled/non-Git actions=0/index retained; 56 checked-in tests и distinct untracked positives проходят. B1/B2 refusal baseline сохранён. Fresh SQL proof подтверждает текущий положительный путь на byte-equal target.
- Проверено: actual plan/draft/Decisions/closed Q1/current window, previous same-file review, selected support metadata/findings/reconciliation/proof, changed wrapper/tests и unchanged canonical target records. Shared prefix/override equal HEAD 8/8 независимо проверены. Pins, source/dev, stage order, redaction и постоянный formatter сохранены; новых process/API/schema/registry решений нет.
- Limits: credentials values читает только wrapper; setup/Extract/server/config/environment не менялись; sid/profile unknown. Mode=fresh-exec без semantic-review marker не активирует role-outcome/P/F writer. Последовательный canary не доказывает concurrency; GetReorderCandidates вне Scope.

## Lane synthesis / aggregate verdict

- Source lanes: reviewer_code_risk, reviewer_code_contracts
- Canonical mapping:
  - historical risk:R1 -> B1 (status=historical-fixed owner=Coder)
  - historical risk:R2 -> B2 (status=historical-fixed owner=Coder)
  - historical risk:R3 -> B3 (status=historical-fixed owner=Coder)
  - historical contracts:C1 -> B3 (status=historical-fixed owner=Coder; та же tracked-JUNIT alias family)
- Provenance records:
  - Finding: historical risk:R1
    - source_lane: reviewer_code_risk
    - lane_finding_id: risk:R1
    - synthesis_disposition: superseded
    - canonical_ref: docs/code_reviews/261011_1523_stack_adaptation.md#B1
    - audit_status: pending_post_merge_audit
    - followup_plan: N/A
  - Finding: historical risk:R2
    - source_lane: reviewer_code_risk
    - lane_finding_id: risk:R2
    - synthesis_disposition: superseded
    - canonical_ref: docs/code_reviews/261011_1523_stack_adaptation.md#B2
    - audit_status: pending_post_merge_audit
    - followup_plan: N/A
  - Finding: historical risk:R3
    - source_lane: reviewer_code_risk
    - lane_finding_id: risk:R3
    - synthesis_disposition: superseded
    - canonical_ref: docs/code_reviews/261011_1523_stack_adaptation.md#B3
    - audit_status: pending_post_merge_audit
    - followup_plan: N/A
  - Finding: historical contracts:C1
    - source_lane: reviewer_code_contracts
    - lane_finding_id: contracts:C1
    - synthesis_disposition: superseded
    - canonical_ref: docs/code_reviews/261011_1523_stack_adaptation.md#B3
    - audit_status: pending_post_merge_audit
    - followup_plan: N/A
  - Finding: N/A (findings отсутствуют)
    - source_lane: reviewer_code_risk+reviewer_code_contracts
    - lane_finding_id: N/A (no lane findings)
    - synthesis_disposition: no_findings
    - canonical_ref: docs/code_reviews/261011_1523_stack_adaptation.md#Lane-synthesis--aggregate-verdict
    - audit_status: pending_post_merge_audit
    - followup_plan: N/A
    - source_refs: current selected v5 support; scripts/sql.py:299, scripts/sql.py:310, scripts/sql.py:311, scripts/sql.py:321; scripts/test_sql.py:381, scripts/test_sql.py:411, scripts/test_sql.py:426; own commands/JUnit ниже.
    - target_snapshot: BUNDLE=current bundle_sha256=51ebdc9ffdf974603e58538df1270ec68c3eb0e53e761c5d83ffb5705b6fbf08
    - delta/outcome: два implementation targets изменены, 58 unchanged; missing indexed alias refusal исправлен и подтверждён собственным original fixture, checked-in tests и fresh proof; open blockers=[]; new findings=[].
- Aggregate status: ✅ OK
- Reconciliation: B1/B2 historical-fixed baseline сохранён по текущему code/tests и independent original repro. Existing-file B3 исправление сохранено; surviving missing indexed alias contracts:C1 теперь подтверждённо исправлен. Same-contract reroute завершён в прежних двух targets, B4 не создаётся; green основан на собственном synthesis, не только Risk no-findings.
- Loop signal: четвёртый review cycle, original B3 и contracts:C1 закрыты; текущих implementation blockers нет.
- Root cause class: same-contract reroute, устранён missing-indexed-alias gap; historical closed baseline сохранён, real scope expansion отсутствует.
- Why previous rerun did not break the loop: previous path.stat() FileNotFoundError возвращал до index inventory; существующего inode и literal spelling было недостаточно для missing tracked alias. Это историческая причина red 20:18, не текущий путь кода.
- Extraordinary action: Coder перенёс полный index inventory/NFD-caseless alias проверку до missing-path допуска, сохранив physical identity и positive untracked paths; Contracts повторила original failing fixture, а Risk независимо проверила девять fixtures. Новый helper/target/Owner choice/runtime contour не требовался.
- Next owner: Architect.

## S1 Blocker

### B1) Literal JUNIT filename интерпретируется как Git pathspec — historical-fixed

- Blocker ID: B1
- Current state: historical-fixed
- Classification: same-contract reroute
- Primary owner gap: Coder
- Evidence refs: `docs/code_reviews/261011_1523_stack_adaptation.md#B1`, `scripts/sql.py:289`, `scripts/test_sql.py:530`, current v5 support → predecessor_reconciliation; original immutable support v2.
- Исторический сценарий: target 62425925… принимал tracked `:(literal)canary.xml` как pathspec и заменял XML.
- Текущее исправление: ls-files получает --literal-pathspecs, check-ignore сохраняет literal arguments. Собственные checked-in matrices и selected independent original repro подтверждают refusal 2/old-byte preservation/config unread/build-SQL=0; valid untracked magic filename допустим. Fixed baseline не reopen-ится.

### B2) Ambient alternate index позволяет пропустить tracked JUNIT — historical-fixed

- Blocker ID: B2
- Current state: historical-fixed
- Classification: same-contract reroute
- Primary owner gap: Coder
- Evidence refs: `docs/code_reviews/261011_1523_stack_adaptation.md#B2`, `scripts/sql.py:279`, `scripts/sql.py:608`, `scripts/test_sql.py:543`, `docs/adr/010-trusted-local-git-metadata-boundary.md:41`, current v5 support → predecessor_reconciliation; original immutable support v2.
- Исторический сценарий: ambient GIT_INDEX_FILE выбирал отсутствующий alternate index, normal root readback проходил, tracked XML заменялся.
- Текущее исправление: presence любого из четырёх ambient overrides, включая empty value, даёт operational-red rc 2 до JUNIT/config/deletion. Собственные fixtures и selected original B2 repro подтверждают old bytes/config unread/child-processes=0; environment не нейтрализуется. Fixed baseline не reopen-ится.

### B3) Case-insensitive JUNIT alias для existing/missing tracked XML — historical-fixed

- Blocker ID: B3
- Current state: historical-fixed
- Classification: same-contract reroute
- Primary owner gap: Coder
- Evidence refs: `docs/code_reviews/261011_1523_stack_adaptation.md#B3`, `scripts/sql.py:299`, `scripts/sql.py:310`, `scripts/sql.py:311`, `scripts/sql.py:321`, `scripts/sql.py:499`, `scripts/test_sql.py:381`, `scripts/test_sql.py:411`, `scripts/test_sql.py:426`, `scripts/test_sql.py:442`, `scripts/test_sql.py:474`, `scripts/test_sql.py:496`, plan Owner fact 11/Acceptance, immutable support v3 → findings/reproductions, v4 → predecessor_reconciliation, v5 → reconciliation/reproductions.
- Исторический risk:R3: existing tracked TrackedCanary.xml принимался через lower-case leaf/ancestor alias на supported macOS filesystem; old XML заменялся после девяти non-Git actions. Это исправлено directory spelling/physical index identity и подтверждено текущими independent/checked-in refusals.
- Исторический contracts:C1 20:18: tracked TrackedCanary.xml удалён только из working tree при сохранённом index; JUNIT=trackedcanary.xml получил refusal=None/non-Git actions=9/tracked-file-recreated=true. Собственный temporary make harness тогда дал make 2/wrapper 1/tests=1/failures=1/errors=0; этот факт сохранён в plan Evidence/objections и historical v4-cycle lineage.
- Текущее исправление: missing leaf больше не возвращается до чтения полного trusted index; NFD/casefold comparison обнаруживает leaf/ancestor/index-rename/normalization aliases без inode, а existing physical identity сохранена. Invalid/unknown inventory отказывает; distinct canonical untracked neighbor/new nested XML проходит.
- Собственный original contracts:C1 rerun: real temporary Git/current filesystem, copied Makefile/current wrapper/existing Fixture/FakeExecutor, refusal=2/config-uncalled=true/non-Git actions=0/tracked-file-recreated=false/original-index-path-retained=true. Make/wrapper rc 0, tests=1/failures=0/errors=0. SQL/config synthetic; temporary corpus очищен, project implementation/index не менялись.
- Closure: own 56 checked-in tests/current source, собственный original negative rerun и прочитанные nine independent Risk fixtures подтверждают tracked/unknown refusal до любых config/build/SQL действий. Fresh positive SQL proof подтверждает distinct allowed path. Нового plan gap/Owner choice не возникло.

## S2 Risk

Новых самостоятельных S2 нет.

## S3 Nit

Новых самостоятельных S3 нет.

## Follow-ups

N/A (why=текущие B1/B2/B3 исправлены в Scope; GetReorderCandidates требует отдельного поручения Owner).

## Plan gaps (plan fixes needed)

Новых plan gaps нет. Owner fact 11/Acceptance не изменены; current refusal invariant и оба independent current JUnit подтверждены. Arch acceptance остаётся Architect-owned.

## Контекст / scope

Exact inventory: 60 current targets, два changed implementation files в прежнем Scope и 58 unchanged canonical records. Shared-prefix/override custody подтверждена независимо. Значения .env.local читает только wrapper; source/dev/role ownership, human_explicit и upstream N/A/ref сохранены.

## Команды / evidence

Собственные команды последовательно выполнены в unchanged launch environment, Python 3.12.14/Darwin; без PATH/home/runtime/server/config изменений.

| Команда | make rc | wrapper rc | Фактический результат |
| --- | --- | --- | --- |
| make db-build | 0 | 0 | Два SQL projects, prepared cache/no-restore |
| make lint | 0 | 0 | Authored/tests без нарушений |
| make test | 0 | 0 | tests=56/failures=0/errors=0, current checked-in regressions |
| make test (isolated temporary copied harness, original contracts:C1) | 0 | 0 | tests=1/failures=0/errors=0; refusal 2/config unread/build-SQL=0/index retained/no recreation |
| make check-secrets | 0 | 0 | До live proof |
| make db-state | 0 | 0 | schemas=2/objects=162/test-classes=1/last-results=1/Products-U=1; Success=1/Failure=0/Error=0, contextual-only |
| make db-proof JUNIT=docs/code_reviews/assets/261011_1523_stack_adaptation/canary.review.junit.xml | 0 | 0 | Новый собственный live canary tests=1/failures=0/errors=0/skipped=0 |
| make check-secrets | 0 | 0 | После live proof |

- HEAD: 167b56395c1bfd5fae8921d2cde12dd1a8295c42.
- Canonical producer: `planveyor_review_target_snapshot docs/plans/261011_1523_stack_adaptation.md --current-bundle`; before/after rc 0, review_target_snapshot.v2, 60 paths, stdout byte-equal и equality с самостоятельно selected current Risk snapshot.
- Bundle SHA до/после: 51ebdc9ffdf974603e58538df1270ec68c3eb0e53e761c5d83ffb5705b6fbf08.
- Explicit JUnit paths: `docs/code_reviews/assets/261011_1523_stack_adaptation/canary.junit.xml`, `docs/code_reviews/assets/261011_1523_stack_adaptation/canary.review.junit.xml`.
- [Reviewer JUnit](assets/261011_1523_stack_adaptation/canary.review.junit.xml): собственный новый execution, mtime UTC=2026-10-11T19:12:27.073206+00:00, 287 bytes/SHA-256=4729e734245305d7406005a240a451e5960d9951db2932d274d148c7f70c2863; tests=1/failures=0/errors=0/skipped=0, один testcase classname=StackAdaptationTests/name=test Products table exists. Hostname/properties/raw streams отсутствуют.
- [Coder JUnit](assets/261011_1523_stack_adaptation/canary.junit.xml): current Coder proof Evidence 21:37, mtime UTC=2026-10-11T18:34:49.143308+00:00, прочитанные 287 bytes/тот же deterministic SHA/1/0/0/0. Equal digest не доказывает reuse; независимая Reviewer freshness установлена собственным command execution и byte-equal before/after snapshot.
- Intake ordinary plan_lint rc 0. Pre-finalization strict bundle --check rc 1: 69 paths/1 root/3 issues только current_review_proof_projection_mismatch/needs_reviewer_rerun. Final post-materialization gates фиксируются append-only в PLAN_PATH::Evidence; pre-final red gate не объявлялся green.

## Exact bundle hygiene

- Exact bundle hygiene: `git diff --check` → rc 0; `git diff --cached --quiet` → rc 0, index пуст.
- Untracked files check: exact targets + plan/draft/review + four supports + two JUnit, 69 файлов; manual trailing whitespace=0, merge markers=0, symlinks=0. 40 generated source-whitespace строк в 12 Imported файлах сохранены без ручной правки.
- Все четыре immutable supports сохранены с прежними byte SHA/size; текущий support gate валиден. Shared prefix и N/A override 8/8 equal HEAD; implementation targets/credential values не редактировались.

## Визуальные доказательства

- Visual env: N/A (why=no UI change; SQL proof — JUnit и contextual db-state).

## Архитектурное ревью

Вердикт: принято.

Текущая адаптация соответствует 12 фактам Owner, Scope и acceptance: SQL Server 2019/Sql150, schema-only Northwind как readonly источник, один реальный canary dbo.Products типа U, pinned local dependencies и make-only команды. Authored пуст; 36 generated Imported файлов входят в 60 literal targets. Общие тела и override восьми carriers побайтно совпадают с HEAD. Новый SQL/business scope, server authority или machine-authority contract не появился.

Принят актуальный same-file aggregate ✅ OK: Risk v5 и Contracts v5 независимо проверили текущие bytes; B1/B2/B3 historical-fixed, open blockers=[]. Closed Coder Q1 и Decisions задавали только recovery routing; acceptance основан на завершённом independent rerun, не на Coder fixes или прежнем Risk no-findings. Current untracked gate проверяет literal index, ambient overrides и existing/missing filesystem aliases до config/actions; собственный Contracts original contracts:C1 rerun и 56 checked-in tests подтверждают missing indexed alias refusal. В immutable Risk support прочитана независимая nine-fixture matrix; Architect эти fixtures и project offline gates заново не запускал.

Оба explicit JUnit прочитаны: canary.junit.xml и canary.review.junit.xml — разные последовательные execution lanes, каждый 287 bytes/SHA-256=4729e734245305d7406005a240a451e5960d9951db2932d274d148c7f70c2863, tests=1/failures=0/errors=0/skipped=0, единственный StackAdaptationTests/test Products table exists. Freshness подтверждена Coder Evidence 21:37 и собственным Contracts execution 22:16 на неизменном canonical bundle 51ebdc9ffdf974603e58538df1270ec68c3eb0e53e761c5d83ffb5705b6fbf08; равный deterministic XML digest сам по себе не доказывает независимость. Hostname/properties/raw streams в XML отсутствуют.

- Собственный contextual `make db-state` (11.10.2026, текущий Architect pass): make rc 0 / wrapper rc 0; schemas=2/objects=162/test-classes=1/last-results=1/Products-U=1, Success=1/Failure=0/Error=0. Это readback, не замена двух independent canary proof.
- Canonical snapshot rc 0: review_target_snapshot.v2, 60 paths/current bundle 51ebdc9ffdf974603e58538df1270ec68c3eb0e53e761c5d83ffb5705b6fbf08; все file SHA/size равны selected immutable producer. Selector rc 0/state=selected/run_id=risk:20261011T185929Z:sol_ultra_v5; support SHA-256=320703ba7643ea72080aed1c55af20714a8b1040e54eeb4d46e8501c640be3cd.
- Собственные ordinary plan_lint, explicit-origin review_artifact_lint и canonical doc-lint — rc 0; exact bundle --check — rc 0, 69 paths/1 root/0 issues. Exact hygiene: manual trailing whitespace=0/merge markers=0/symlinks=0; 40 generated source-whitespace строк в 12 Imported файлах сохранены. Index пуст, HEAD=167b56395c1bfd5fae8921d2cde12dd1a8295c42. Final post-write checks зафиксированы в PLAN_PATH::Evidence.
- `runner_quality: row_status=not_applicable runner_id=codex_collab role=reviewer model=gpt-6.1-sol task_class=review-contracts source_ref=docs/code_reviews/261011_1523_stack_adaptation.md follow_up_ref=N/A notes=Текущие Risk/Contracts metadata показывают только native Codex; material contribution non-default runner отсутствует.`

Новых findings, deferred obligations или Owner questions нет; GetReorderCandidates остаётся отдельным прямым поручением после sibling ready. Sequential canary не доказывает concurrency или другие ОС/filesystems. Human policy оставляет статус Architect arch review для Owner preview через existing planveyor sibling close; semantic acceptance не разрешает stage/Done/commit/close --commit, docs-finalize, push или публикацию.

# Code draft: Адаптация контракта Planveyor 3f5b2c1 → bbf11a7

**Date:** 2026-11-25 17:06 +0300
**Cluster:** process
**Related plan:** `docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md`
**Author role:** Planner
**Status:** draft

## Meta (machine-readable JSON)

```json
{
  "code_draft_meta": {
    "plan": "docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md",
    "cluster": "process",
    "targets": [
      {"path": ".copier-answers.yml", "kind": "config"},
      {"path": "docs/_meta/planveyor_contract_authority.v1.json", "kind": "doc"},
      {"path": "docs/code_drafts/_template.md", "kind": "doc"},
      {"path": "docs/plans/README.md", "kind": "doc"},
      {"path": "docs/plans/_template.md", "kind": "doc"},
      {"path": "docs/rollout_packets/_template.md", "kind": "doc"}
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

- Source plan provenance: `reuse PLAN_PATH carrier unless this draft is created/imported/backfilled separately`
- Relation: `created-here`
- Thread ID: `<REDACTED>`
- Parent thread ID: `N/A (why=not exposed by env, wrapper receipts, or session stats)`
- Session SID: `N/A (why=.planveyor.session.planner is missing or empty)`
- Launch surface: `unknown (why=no env, wrapper receipt, or session stats origin identified the launch surface)`
- Captured from: `env`
- Captured at: `2026-11-25T14:00:26Z`

Источник — actual public `planveyor_plan_provenance_context --section code-draft --session-key planner --format markdown`; raw JSON/KV identities не копировались.

## Purpose

Принять уже доставленные шесть файлов, проверить bytes/privacy и прежний SQL harness. Новых product/test/SQL/helper targets нет. Plan/draft/current review и explicit proof assets — отдельные lifecycle members; origin plan не входит в mutable review targets.

## Reviewability preflight receipt

- `proof-path class`: standard primitives, existing public facade, read-only Git blobs и unchanged make harness; transient recipes ниже не являются новым checked-in helper или production implementation.
- `mandatory primary lane`: consumer doctor/doc lint; четыре pinned Copier blobs; finite AC3 capture; offline db-build/lint/test/check-secrets; plan lint и соответствующий bundle gate.
- `mandatory non-primary carrier / contextual lane`: AC3 JSON/env-source и полные absent-input N-A причины; восемь local tails; независимые Coder/Reviewer JUnit 9/0/0/0; contextual db-state.
- `exact helper path + support files`: external bin/planveyor, scripts/planveyor.zsh, scripts/codex_session_context.py; local Makefile, scripts/sql.py, scripts/test_sql.py, global.json, Directory.Build.props, NuGet.Config, requirements-dev.txt, .config/dotnet-tools.json и девять current SQL procedure declarations — existing read-only baseline.
- `dependent tests / dependent docs / known consumer paths`: четыре doc targets; plan/code-draft/packet provenance consumers; восемь matrix carriers из docs/README.md; source renderer/facade tests остаются external source context. JSON/KV emitter fields, validators/parsers, CLI/status/severity и Manager dispatch не меняются. Receipt schema emitter inventory / API field parity / Manager one-shot dispatch: N/A (why=эти интерфейсы не меняются).
- `preconditions / seed-discovery`: same physical project, exact selected facade ../runtime-bbf11a7 и full pin; Q5 уже terminal green, далее receipt-reuse-only. Synthetic seeds создаются отдельно для каждой роли в .tmp/contract-provenance-proof/<role>-ac3; missing fixture stats/receipt paths запрещают session-history lookup. Setup — только Coder один раз по Q2 после завершения Planner, под exact Q5 policy с отдельным tool approval.
- `reroute rule`: missing/hash-drift/red/unknown обязательного carrier, runtime/SDK/environment drift или out-of-six target — stop к Architect; source fallback, automatic setup/SQL retry, profile regeneration или silent seed rediscovery запрещены.
- `perceptual truth-source split`: bytes, parsed Markdown/JSON, actual native rc и strict JUnit — truth sources. UI/OCR/image proof N/A (why=UI отсутствует).

Stateful continuity: discovery-or-seed = fresh role fixture + before HEAD/current-bundle snapshot. Дальше receipt-reuse-only для тех же source pin, target snapshot, Q5 policy/common environment и role fixture. Exact observer boundary — terminal process result, затем следующий canonical snapshot/readback и новый strict JUnit того же path. Notice/success text != mutation truth. Same entity для SQL — назначенная dev-цель от guard до formatter внутри wrapper, без раскрытия значения. Concurrency proof N/A (why=последовательная проверка, concurrency contract не меняется).

Retention: все .tmp recipes/profiles/receipts/snapshots — transient local sanity only; raw captures не сохраняются. Durable current review использует coder.junit.xml, reviewer.junit.xml, coder-proof.json, reviewer-proof.json под docs/code_reviews/assets/261125_0958_contract_upgrade_3f5b2c1_bbf11a7/ и явно ссылается на каждый actual asset. Safe proof JSON содержит только role/command, make+wrapper rc, HEAD и canonical target/bundle SHA до/после, relative JUnit path/SHA и exact counts/identities. Credentials/server/private paths/raw streams отсутствуют. Missing transient carrier означает stop, не его восстановление по памяти.

Truth-host fixture matrix: N/A (why=fan-in/readback helper не меняется).

## Targeted changes (by file)

- .copier-answers.yml: _commit=bbf11a7; repository_id/source остаются прежними.
- docs/_meta/planveyor_contract_authority.v1.json: full source_commit=bbf11a7a2b7b8e473951c4052f749b251fc42578; target-local/root/API 5..5 прежние.
- docs/plans/README.md: public provenance rule masks present identity, сохраняет N-A/private ABI/passthrough.
- docs/plans/_template.md и docs/code_drafts/_template.md: три identity fields masked/N-A.
- docs/rollout_packets/_template.md: два identity fields masked/N-A.

Existing baseline surfaces = external renderer/facade и local SQL wrapper/tests/восемь tails. New implementation targets = N/A (why=принимаем доставленные existing files). Не переписывать старые plans/reviews/snapshots или source runtime. Если delivered bytes уже точны, сохранить их и добавить только фактические lifecycle evidence.

## Review route

- `Primary artifact`: `docs/code_reviews/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md`
- `Lane type`: code review (why=.copier-answers.yml вне docs/**); один current host, пока planned.

## Q5 terminal proof and exact reuse

Выполнен один новый отдельно одобренный request, один applied OS profile и один process chain. Terminal native rc0; allow/readback=true; deny=EPERM(1), negative_absent=true; lookup rc0/equality=true; actual SDK rc0/version=10.0.404. Setup не запускался. Исторический Q4 rc71 не переписан.

Все пути ниже — .tmp/contract-provenance-proof/preflight-q5/:

| Carrier | SHA-256 |
| --- | --- |
| write.sb | bc3c2b5a9afc89e09567483642e10477657588bebd287d969e33b863428b9a63 |
| control_sdk.py | dfaf4247e83d73bd62a5d756ab6a20c398662cb99863949260fc05b229a1e29b |
| before.json | 62ca54bbdd98bac4c57d6294472dd48adbcda7470899370a9ff80f831c9b47c9 |
| terminal.json | fb9eac9c4302a51addb0ff90f632ede558f107e6280204929a1b22694d524d14 |
| coder_setup.sh | f811ad988e0b22d6dd3a850cebd3902b34a630dd42edbb8560d84116cce830c8 |
| setup-envelope.json | 39bdabdf73195914b1aabc8a6549669e159a586989faa3eb444bd8f1a98dcdc1 |
| check_reuse.py | b201f5721486275a59cb19366f5dc3963edded856a19a3c91e3479b18a699150 |
| sdk_checks.sh | 1132775932b3f6eb137cc77ac6d5b9449ec65fef6054a2a67d2b76f9e300bc53 |
| sql_proof.sh | 3a1ff4714fd9a6f1dc126a1d1dd5432335de37f4e34de17e14e845f93c9df8ef |

Все role tool requests для этих SDK/envelope/reuse commands используют physical project workdir и login=false, сохраняя prepared launch context. Каждый make envelope до env-i, а read-only reuse checker до проверки carriers отклоняют наличие GIT_DIR/GIT_WORK_TREE/GIT_COMMON_DIR/GIT_INDEX_FILE, включая пустое значение. Make envelopes возвращают operational-red rc2; reuse checker возвращает rc1 и останавливает handoff до project action. Overrides не нейтрализуются для обхода штатного guard.

Common environment SHA-256=3d3e8279285e90bdd39314269d784262a271e2760468bdafac1f6497037a9e4a. Profile actual bytes use physical project .tmp only; raw policy остаётся transient. Before binds SDK directory/executable hashes и boundary hash; private SDK directory поступает Manager только как MSSQL_DOTNET_SDK_DIR и не записывается в tracked artifacts.

Coder сначала сверяет hashes/regular non-symlink carriers, затем вызывает read-only check_reuse.py с privately supplied MSSQL_DOTNET_SDK_DIR. Этот checker исполняет только hash-bound pure environment definition, не main/control/SDK/setup payload; он не является новым SDK preflight. Требуется Q5 REUSE PASS и прежняя common-environment equality. Он не печатает private inputs. Нельзя заново запускать control_sdk.py, выбирать новый profile или менять проверенное before/terminal.

```sh
python3 -B .tmp/contract-provenance-proof/preflight-q5/check_reuse.py
```

Единственный Coder setup request после Ready for Coder: sandbox_permissions=require_escalated, login=false, physical project workdir, без prefix_rule. Private SDK binding передаётся только в tool command context. Весь setup payload выполняется под одним profile; shell envelope делает env -i с ровно проверенными common bindings и exec неизменённого make setup, без повторения controls/version preflight:

```sh
/usr/bin/sandbox-exec -f .tmp/contract-provenance-proof/preflight-q5/write.sb /bin/sh .tmp/contract-provenance-proof/preflight-q5/coder_setup.sh
```

До request Coder создаёт immutable .tmp/contract-provenance-proof/setup/before.json: plan, HEAD, canonical snapshot, profile/common-env/setup-envelope hashes и state=prepared; без private values. Existing before/dispatch/terminal record не перезаписывается. Один actual dispatch фиксируется native tool receipt/session; running — только wait того же session_id. После native terminal сохранить отдельный setup/terminal.json с native make rc, safe wrapper rc и cache inventory; rc0 обязателен для обоих. Known terminal rc0 только reuse, без нового launch/baseline overwrite. Refusal/failure/interruption/unknown или missing cache — stop без retry.

Cache inventory — .tmp/setup.complete, .tmp/venv/bin/sqlfluff, .tmp/nuget/packages/microsoft.build.sql/2.3.0, .tmp/nuget/packages/tsqlt.dacpacs/1.0.8083.3529, .tmp/build/Northwind/obj/project.assets.json, .tmp/build/Northwind.Tests/obj/project.assets.json. Marker existence не заменяет native receipt. Make setup не устанавливает SDK, не читает SQL config и не выполняет Extract/Publish.

SDK build использует hash-pinned sdk_checks.sh: те же common env-i bindings, никакие arguments не допускаются, final argv ровно make db-build. Он запускается под exact Q5 profile после соответствующего точечного tool approval. SQL proof — прежняя Q1 target-local lane: hash-pinned sql_proof.sh получает только coder либо reviewer, сохраняет те же SDK/cache/TMPDIR bindings и exec штатного make db-proof с exact durable JUNIT. Он использует обычный project tool sandbox/permissions, который допускает запись согласованного очищенного XML в docs/code_reviews/assets; profile Q5 остаётся неизменным с границей .tmp. Это заранее выбранная Q1 proof lane, а не recovery после отказа profile/setup. SDK preflight повторно не запускается. Private MSSQL_DOTNET_SDK_DIR передаётся только в tool context, не печатается; все cache/build/TMPDIR по-прежнему .tmp, SQL цель защищает unchanged wrapper. Lint/test/check-secrets/db-state не получают SDK PATH prepend.

```sh
/usr/bin/sandbox-exec -f .tmp/contract-provenance-proof/preflight-q5/write.sb /bin/sh .tmp/contract-provenance-proof/preflight-q5/sdk_checks.sh
/bin/sh .tmp/contract-provenance-proof/preflight-q5/sql_proof.sh coder
/bin/sh .tmp/contract-provenance-proof/preflight-q5/sql_proof.sh reviewer
```

## Finite proof recipes

### Contract bytes and local tails

Transient recipe .tmp/contract-provenance-proof/verify_contract.py SHA-256=082d2cf2415b60711a4ef7bc5ed2e1699ddb3fc5cc3ca6ccd38992b3f757adea. Он читает full runtime HEAD, четыре exact copier_template/<doc path> blobs и local tails от literal stack heading до EOF против sibling HEAD; API/authority/pins проверяет отдельно. Git/root failures дают safe FAIL без raw stderr. Coder и Reviewer каждый повторяет:

```sh
python3 -B .tmp/contract-provenance-proof/verify_contract.py
../runtime-bbf11a7/bin/planveyor --project "$PWD" planveyor_consumer_doctor
../runtime-bbf11a7/bin/planveyor --project "$PWD" planveyor_doc_lint
```

### AC3: synthetic Markdown plus independent JSON/source

Transient recipe .tmp/contract-provenance-proof/ac3_capture.py SHA-256=1f19f4de9f294f37509ff7ffeba114481b3a6fbfbd57f6f8833a6f587a98535a. Только standard-library capture existing public helper; 4 cases × 4 calls = 16. Cases: own UUID triplet; own opaque triplet; missing inputs with empty session key; missing inputs with canonical role key. Каждый случай читает отдельный JSON и Markdown sections plan/code-draft/packet. Exact JSON dictionary проверяет все семь fields, raw synthetic identities и captured_from=env для present case; absent case manual-owner. Markdown: exact ordered identity labels/values 3/3/2, present только REDACTED, ни одного raw synthetic value, absent — полная прежняя N-A причина. Metadata/source/section headings проверены отдельно. --thread-id/--captured-from не применяются: они подменили бы env inference.

Fixture root — fresh <role>-ac3 под .tmp/contract-provenance-proof, explicit missing --stats-script/--run-receipt-path, no history lookup. Existing fixture — failure, не silent reseed. Все captures/seeds в памяти; exceptions/raw stdout/stderr не печатаются и не сохраняются. Наружу только safe PASS/FAIL stage/field names. Planner sanity не заменяет independent Coder/Reviewer runs:

```sh
python3 -B .tmp/contract-provenance-proof/ac3_capture.py coder
python3 -B .tmp/contract-provenance-proof/ac3_capture.py reviewer
```

## Snapshot and SQL proof sequence

1. Coder: fresh HEAD и canonical current-bundle snapshot до setup/proof, Q5 exact reuse, одна Q2 setup attempt; cache readback; offline gates; guarded db-proof в coder.junit.xml; after HEAD/snapshot и strict XML readback. Любой target edit требует нового applicable proof, но не повторного setup. Historical setup/SQL evidence не переиспользуется как current acceptance.
2. Reviewer: тот же six-target current snapshot; own contract/AC3/offline gates, contextual db-state; собственный sequential db-proof в reviewer.junit.xml; after HEAD/snapshot/XML. Setup/Extract Reviewer запрещены. Coder JUnit не заменяет Reviewer lane.
3. Native stdout snapshot capture хранится transient как .tmp/contract-provenance-proof/<role>.before.snapshot.json и <role>.after.snapshot.json; safe projection/HEAD/JUnit SHA/counts попадает в durable <role>-proof.json. Missing/nonzero snapshot producer — stop, manual SHA не заменяет его.

Canonical public snapshot command:

```sh
../runtime-bbf11a7/bin/planveyor --project "$PWD" planveyor_review_target_snapshot docs/plans/261125_0958_contract_upgrade_3f5b2c1_bbf11a7.md --current-bundle
```

| Role | Final SDK/make argv | Fresh JUnit |
| --- | --- | --- |
| Coder | make db-proof JUNIT=docs/code_reviews/assets/261125_0958_contract_upgrade_3f5b2c1_bbf11a7/coder.junit.xml | coder.junit.xml |
| Reviewer | make db-proof JUNIT=docs/code_reviews/assets/261125_0958_contract_upgrade_3f5b2c1_bbf11a7/reviewer.junit.xml | reviewer.junit.xml |

Остальные runnable project goals из root:

```sh
PLANVEYOR_RUNTIME_ROOT=../runtime-bbf11a7 make lint
PLANVEYOR_RUNTIME_ROOT=../runtime-bbf11a7 make test
PLANVEYOR_RUNTIME_ROOT=../runtime-bbf11a7 make check-secrets
PLANVEYOR_RUNTIME_ROOT=../runtime-bbf11a7 make db-state
```

Для db-build и двух db-proof rows применяется общий checked SDK envelope выше; PATH prepend только Q4, cache/TMPDIR только .tmp. Publish/tSQLt — лишь ранее согласованная dev-цель после existing one-query guard; missing config/target rejection → stop до Publish, server fixes запрещены. .env.local/SQL values читает только scripts/sql.py. Wrapper fixed return codes: 0 success; 1 test/JUnit; 2 config/path/Git/secrets; 3 target; 4 connection/read SQL; 5 build/lint; 6 Publish. Native make rc фиксируется отдельно; SQL retries отсутствуют.

Strict current set — GetReorderCandidatesTests: test T1 empty Products returns empty result; test T2 active shortage is returned; test T3 zero and negative shortage excluded; test T4 on order units cover shortage; test T5 discontinued products excluded; test T6 numeric nulls treated as zero; test T7 smallint arithmetic does not overflow; test T8 result metadata and ProductID order. Девятый — StackAdaptationTests.test Products table exists, real dbo.Products type U без FakeTable/NewTestClass. В каждом XML ровно эти девять unique identities, suite/root parity, tests=9/failures=0/errors=0/skipped=0; red testcase/unknown/duplicate/missing identity не перекрываются green totals.

## Critical invariants / traps / bypass paths

- SDK version green != setup/cache/SQL acceptance. Unspent setup attempt не разрешает retry после неизвестного результата.
- Profile name != policy identity; hashes/boundary/common environment обязательны, drift/lost carrier → stop.
- Doctor green != pinned document parity; synthetic Markdown green != JSON/source parity; Coder JUnit != Reviewer JUnit.
- Alternate carriers: plan, code-draft, packet; present UUID, opaque, absent inputs; source env vs explicit args. Все входят в finite recipe.

## Assumptions / risks

Private SDK input и prepared PATH/HOME/common locale не меняются между preflight и Coder reuse; это проверяется hash equality, а не предполагается. Runtime full pin и project physical root должны совпасть с текущим control header. SDK/profile/recipe/transient receipt потеряны — Architect reroute, не новый install/profile/control/version launch.

## Notes for Coder

Plan важнее draft; scope/authority противоречие возвращается Architect. Не менять шесть уже точных delivered files ради формального diff. Новые production/test/helper/sample corpus targets запрещены без triage. Before/terminal/profile сохраняются, raw captures и private paths не попадают в tracked assets. Done/commit не принадлежат Coder/Planner; после Ready for Review обычный Reviewer/Architect route остаётся полным.

## Review stamps (append-only)

- [2026-11-25 17:06 +0300] (Planner) Exact six-target contract и Q5 receipt/current environment прочитаны; code draft materialized после successful Q5, без setup/SQL.

- [2026-11-25 17:11 +0300] (Planner) NO SUGGESTIONS (reviewed; no changes required): current exact bundle, Q5 setup reuse, Q1 durable JUnit lane и finite proof recipes reconciled.

- [2026-11-25 17:15 +0300] (Planner) NO SUGGESTIONS (reviewed; no changes required): final common environment, ambient Git refusal, setup/build .tmp policy и Q1 durable SQL lane сверены с actual recipes/hashes.

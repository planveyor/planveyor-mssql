# Code draft: dbo.GetReorderCandidates — товары к дозаказу

**Date:** 2026-10-12 02:51 +0300
**Cluster:** data
**Related plan:** `docs/plans/261012_0141_get_reorder_candidates.md`
**Author role:** Planner
**Status:** draft

## Meta (machine-readable JSON)
```json
{
  "code_draft_meta": {
    "plan": "docs/plans/261012_0141_get_reorder_candidates.md",
    "cluster": "data",
    "targets": [
      {
        "path": "sql/Northwind/Authored/GetReorderCandidates.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/GetReorderCandidatesTests.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/test_T1_empty_Products_returns_empty_result.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/test_T2_active_shortage_is_returned.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/test_T3_zero_and_negative_shortage_excluded.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/test_T4_on_order_units_cover_shortage.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/test_T5_discontinued_products_excluded.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/test_T6_numeric_nulls_treated_as_zero.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/test_T7_smallint_arithmetic_does_not_overflow.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/GetReorderCandidatesTests/test_T8_result_metadata_and_ProductID_order.sql",
        "kind": "sql"
      },
      {
        "path": "scripts/sql.py",
        "kind": "py"
      },
      {
        "path": "scripts/test_sql.py",
        "kind": "py"
      },
      {
        "path": "README.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/architect_status_driven.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/planner_status_driven.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/coder_status_driven.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/coder_migrations_gate.md",
        "kind": "doc"
      },
      {
        "path": "docs/tools/prompts/reviewer_status_driven.md",
        "kind": "doc"
      },
      {
        "path": "docs/playbooks/review_staged_or_commit.md",
        "kind": "doc"
      },
      {
        "path": "docs/playbooks/review_merge_range.md",
        "kind": "doc"
      },
      {
        "path": "docs/playbooks/post_merge_audit.md",
        "kind": "doc"
      }
    ],
    "deleted_paths": [],
    "machine_authority_decision_ref": {
      "applicability": "not_applicable",
      "reason_code": "no_machine_authority_change",
      "carrier_sha256": "d435d5a496b546069ce71672025c9ead04a3366aa611afb39abdfe8e3480e204"
    }
  }
}
```

## Provenance / session context

- Source plan provenance: `docs/plans/261012_0141_get_reorder_candidates.md#Plan-provenance-session-context`; исходный origin сохранён, этот draft создан отдельно по текущему helper readback.
- Relation: `created-here`
- Thread ID: `<REDACTED>`
- Parent thread ID: `N/A (why=not exposed by env, wrapper receipts, or session stats)`
- Session SID: `N/A (why=.planveyor.session.planner is missing or empty)`
- Launch surface: `unknown (why=no env, wrapper receipt, or session stats origin identified the launch surface)`
- Captured from: `env`
- Captured at: `2026-10-11T23:50:41Z`

## Purpose

Закрепить exact 21 writable targets и воспроизводимый контракт T1–T8/canary/parser/proof. Исполняемый SQL и product changes реализует Coder; Planner создал только план, этот draft и десять comment-only path-tracking carriers с обязательной заменой до review. Единственный semantic source — связанный plan.

## Reviewability preflight receipt

- `proof-path class`: checked-in repo-local helper
- `mandatory primary lane`: make db-build, make lint, make test, make check-secrets; Coder и независимо Reviewer выполняют make db-proof, каждый получает свежий JUnit 9/0/0/0 на проверяемом bundle.
- `mandatory non-primary carrier / contextual lane`: make db-state у Reviewer и Architect; это чтение состояния, а не замена db-proof.
- `exact helper path + support files`: Makefile, scripts/sql.py, scripts/test_sql.py, sql/Northwind/Northwind.sqlproj, sql/tests/Northwind.Tests.sqlproj.
- `dependent tests / dependent docs / known consumer paths`: `scripts/sql.py:parse_junit` → `Stack.proof` → атомарный очищенный JUnit; `scripts/test_sql.py` (GOOD_XML/FakeExecutor, JUnitPathTests, ProofTests, RedactionTests, RepositoryContractTests), новые T1–T8 и постоянный canary; `README.md` и восемь synchronous doc targets; `Stack.secrets` и code review читают XML, `Stack.state` остаётся contextual-only. Изменяется проверяемый состав suite/testcase и итоговый счётчик успешного прогона; интерфейс make/JUNIT, коды выхода и SQL guard не меняются.
- `preconditions / seed-discovery`: адаптация закрыта; существующее окружение; свежая проверка имени dev-базы, наличия маркера и sysadmin=0 перед каждым Publish; новый Git-untracked relative .xml JUNIT. Старый proof не переиспользуется.
- `discovery-or-seed`: Coder и Reviewer каждый самостоятельно выполняют полный существующий `make db-proof`: текущая сборка → свежий guard → Publish в назначенную dev-базу → RunAll → formatter → очищенный JUnit. Setup/Extract, новое окружение и серверные изменения ради этой задачи не требуются.
- `receipt-reuse-only`: после каждого Publish тот же `Stack.proof` удерживает принятую конфигурацию dev-цели до RunAll/formatter и атомарной записи своего JUnit; последующая проверка читает этот exact report, не переиспользует XML адаптации или другой роли. Reviewer запускает собственный полный proof, а не принимает receipt Coder как своё доказательство.
- `stable identity fields`: роль прогона, portable make command и коды make/обвязки, HEAD и canonical bundle_sha256 до/после proof, relative JUnit path и SHA-256, полный набор девяти suite/class/test identities и counts. Идентичность принятой SQL-цели удерживается существующей обвязкой; значения подключения не записываются в evidence.
- `exact transient observer boundary`: XmlResultFormatter читает результаты того же непосредственно предшествующего RunAll до следующего Publish/RunAll в общей dev-базе; Coder/Reviewer выполняются последовательно. Потеря свежего report, несовпадение его SHA-256/bundle/состава или нарушение этой связи блокируют приёмку и требуют штатного нового proof, а не ручного исправления XML/receipt.
- `notice/success text != mutation truth`: успешное сообщение и synthetic fixture не закрывают SQL proof; closure даёт свежий formatter XML того же RunAll, строгий parse и атомарный очищенный JUnit, связанный с текущими target bytes. Следующий `make db-state` — canonical contextual readback тех же последних SQL-результатов, он не заменяет independent JUnit.
- `runtime-lineage preflight`: каждый db-proof собирает и публикует текущий test dacpac через существующий harness; до/после фиксируются текущие HEAD/bundle. Предыдущая схема/процедура в dev-базе не считается proof новых bytes. Ошибка build/cache/Publish остаётся у owning Coder/Reviewer lane; её не скрывают повторным setup/Extract, сменой среды или изменением server prerequisites.
- `reroute rule`: отсутствующий или красный обязательный proof блокирует acceptance; роли следуют штатному route без ручного исправления guards/receipts.
- `perceptual truth-source split`: N/A (why=no visual proof; SQL/JUnit and repository bytes are authoritative).
- Retention: docs/code_reviews/assets/ — durable operator/review evidence; .tmp/ — transient local sanity only.
- Truth-host fixture matrix для изменяемого parser/proof: authoritative host — текущий `tSQLt.XmlResultFormatter` XML после того же RunAll; derived summary — очищенный JUnit/counts и сообщение `Stack.proof`. Green fixture: точные девять testcase с согласованными suite/root totals и 9/0/0/0. Missing/ambiguous fixtures: missing canary/T1–T8, пустой/обрезанный XML, неизвестные или повторённые class/test identities; все дают отказ 1. Present-but-red/inconsistent fixture: девять имён и внешне зелёные totals при nested failure/error/skipped либо неверных suite/root counters; отказ 1, success не печатается. Старый одиночный canary не является green fixture нового proof.
- T8 proof: метаданные самой процедуры; `is_hidden=0`, column ordinal 1/2/3, `ProductID int`, `ProductName nvarchar(40)`, `Shortage int`; сведения ORDER BY определены и соответствуют только `ProductID ASC`. Это проверка объявленного контракта результата в tSQLt, а не новая внешняя CLI. Current Coder proof выполнен в Evidence связанного плана; независимые Reviewer proof/source review остаются обязательными.
- Synthetic proof carrier: существующие GOOD_XML/FakeExecutor и named unittest classes внутри `scripts/test_sql.py`; новые negative cases проверяют parser/proof без SQL/config/cache. Отдельный checked-in sample XML, новый review helper или historical backfill в этот bundle не добавляются.


### Точный parser/proof contract

Native formatter host — testsuites с двумя suites: GetReorderCandidatesTests (8) и StackAdaptationTests (1); suite/testcase order не является идентичностью. Канонический состав — ровно таблица ниже, case-sensitive. Существующие tSQLt варианты bare/bracketed class и plain/bracketed/class-qualified test name нормализуются только по literal известным идентичностям; неизвестные alias, несогласованные suite/classname, дубликаты после нормализации и посторонние classes/tests отвергаются. Один testsuite не доказывает полный двухклассовый набор.

Suite counters обязательны и пересчитываются из своих testcase; root totals, если присутствуют, сверяются с aggregate всех suites. Green — только tests=9, failures=0, errors=0, skipped=0 и exact unique set. Coherent red testcase сохраняет очищенный failure/error/skipped XML и код 1 без success; inconsistent/malformed/unknown/duplicate host даёт код 1 без ложного green артефакта. Сохраняются запреты DTD/entity/duplicate documents/unsupported structure/misplaced or duplicate result nodes; очищенный report содержит только доверенные names/counts и redacted results.

GOOD_XML/FakeExecutor в scripts/test_sql.py материализуют literal native двухклассовый XML независимо от production expected-inventory constant. Позитивы проверяют permutation suites/cases и поддержанные known tSQLt spellings. Негативы: удалить каждую из девяти identities; добавить unknown или wrong class/name; дублировать identity тем же или альтернативным spelling; старый canary-only; пустой suite/report; root/suite counters mismatch; nested/misplaced/duplicate failure/error/skipped и каждый red status при green totals; malformed/truncated/DTD/entity/extra document. ProofTests дополнительно проверяет atomic fresh report, nine real identities в success, no success на red, stage order и невозможность reuse old XML после Publish/RunAll/formatter failure. JUnitPathTests/ConfigTests/RedactionTests и существующие Git/target refusals сохраняют смысл и доказательства.

### Receipt schema emitter inventory

- Family: native tSQLt JUnit → очищенный JUnit; новый Planveyor schema/authority carrier не вводится.
- Validator/parser и clean XML emitter: scripts/sql.py:parse_junit — mutable target.
- Success/readback emitter: scripts/sql.py:Stack.proof — mutable target; вывод реальных 9 identities/counts, без hardcoded canary-only success.
- Synthetic emitter: scripts/test_sql.py:GOOD_XML/FakeExecutor — mutable target; отдельные stale-canary-only и unknown/duplicate fixtures.
- Native tSQLt.XmlResultFormatter — read-only external dependency; N/A (why=formatter and package pin unchanged).
- Consumers scripts/sql.py:Stack.secrets/Stack.state — read-only baseline implementations внутри того же файла, N/A (why=their existing inventory/redaction behavior does not depend on single-test acceptance); regression fixtures текущего файла сохраняются.
- Owner-facing consumers — README и восемь local doc targets; они описывают обязательный canary и полный exact набор текущего согласованного плана, не его transient basename.
- Manager/queue/dispatch emitter: N/A (why=local SQL/JUnit change; Planveyor surfaces unchanged).

## SQL / testcase inventory

| ID | Класс / suite | Literal testcase name | SQL-файл | Проверяемое ожидание |
| --- | --- | --- | --- | --- |
| T1 | `GetReorderCandidatesTests` | `test T1 empty Products returns empty result` | `sql/tests/GetReorderCandidatesTests/test_T1_empty_Products_returns_empty_result.sql` | Пустая FakeTable Products; пустой literal expected. |
| T2 | `GetReorderCandidatesTests` | `test T2 active shortage is returned` | `sql/tests/GetReorderCandidatesTests/test_T2_active_shortage_is_returned.sql` | Активный товар 10/4/2; literal Shortage=4. |
| T3 | `GetReorderCandidatesTests` | `test T3 zero and negative shortage excluded` | `sql/tests/GetReorderCandidatesTests/test_T3_zero_and_negative_shortage_excluded.sql` | Активные 10/8/2 и 10/9/2; обе строки исключены. |
| T4 | `GetReorderCandidatesTests` | `test T4 on order units cover shortage` | `sql/tests/GetReorderCandidatesTests/test_T4_on_order_units_cover_shortage.sql` | Активный 10/4/6: stock-only deficit покрыт UnitsOnOrder, строка исключена. |
| T5 | `GetReorderCandidatesTests` | `test T5 discontinued products excluded` | `sql/tests/GetReorderCandidatesTests/test_T5_discontinued_products_excluded.sql` | Discontinued=1 и 10/4/2; строка исключена. |
| T6 | `GetReorderCandidatesTests` | `test T6 numeric nulls treated as zero` | `sql/tests/GetReorderCandidatesTests/test_T6_numeric_nulls_treated_as_zero.sql` | Все семь непустых сочетаний NULL: 10/NULL/2→8; 10/4/NULL→6; 10/NULL/NULL→10; NULL/4/2, NULL/NULL/2, NULL/4/NULL, NULL/NULL/NULL исключены. |
| T7 | `GetReorderCandidatesTests` | `test T7 smallint arithmetic does not overflow` | `sql/tests/GetReorderCandidatesTests/test_T7_smallint_arithmetic_does_not_overflow.sql` | 32767/32767/32767; пустой результат без ошибки, математический дефицит -32767. |
| T8 | `GetReorderCandidatesTests` | `test T8 result metadata and ProductID order` | `sql/tests/GetReorderCandidatesTests/test_T8_result_metadata_and_ProductID_order.sql` | Metadata самой процедуры; int/nvarchar(40)/int, ordinals 1/2/3, единственный ProductID ASC; unsorted synthetic IDs 30/2/11 и literal expected 2/11/30 по содержимому. |
| Canary | `StackAdaptationTests` | `test Products table exists` | `sql/tests/StackAdaptationTests/test_Products_table_exists.sql` | Неизменённая real dbo.Products типа U, без FakeTable и чтения данных. |

Все T1–T8 — один класс GetReorderCandidatesTests, отдельный файл класса с CREATE SCHEMA и tSQLt.TestClass property по существующему class carrier, без NewTestClass. Каждый бизнес-тест самостоятельно изолирует dbo.Products через FakeTable до synthetic INSERT; identity/defaults не сохраняются, ProductID задаётся literal. Существующий real-table canary и его class file byte-unchanged. SQL SDK уже включает .sql по принятому проекту; sqlproj/Makefile/Imported не являются mutable targets.

T1–T7 сравнивают состав результата с independent literal expected table (без повторения формулы процедуры в expected). T8 дополнительно использует sys.dm_exec_describe_first_result_set_for_object над OBJECT_ID самой dbo.GetReorderCandidates типа P с include_browse_information=0: нет metadata error и zero-row result; ровно три is_hidden=0 строки; ordinals/names/system_type_name — (1,ProductID,int), (2,ProductName,nvarchar(40)), (3,Shortage,int). У ProductID ordinal_in_order_by_list=1, order_by_is_descending=0; order_by_list_length=1 определён; у остальных нет ORDER BY position. NULL/error/недоступность metadata — red, не skip или fallback. Reviewer читает внешний ORDER BY ProductID ASC и проверяет приведение каждого smallint операнда к int до арифметики; AssertEqualsTable не доказывает порядок, typed INSERT…EXEC не доказывает исходные metadata.

## Targeted changes (by file)

- sql/Northwind/Authored/GetReorderCandidates.sql: новая читающая dbo.GetReorderCandidates, без параметров, SET NOCOUNT ON, qualified dbo.Products, без SELECT *, int до арифметики, числовые NULL=0, Discontinued=0 и положительный Shortage, три колонки и внешний ProductID ASC.
- sql/tests/GetReorderCandidatesTests/GetReorderCandidatesTests.sql: class/schema marker; остальные восемь files этого класса — строго T1–T8 из inventory.
- scripts/sql.py: ограничить implementation diff parse_junit/Stack.proof и необходимым literal expected set; строгая двухклассовая проверка, aggregate counts, очищенный report и реальные success names. Guards/config/path/Git/atomic/timeout/formatter/кодовые категории сохраняются.
- scripts/test_sql.py: GOOD_XML/FakeExecutor, ProofTests/RedactionTests/RepositoryContractTests согласовать с exact девятью; current refusal regressions сохранить. Repository assertions отдельно проверяют canary без FakeTable/INSERT, бизнес-класс с 8 procedure names/FakeTable/synthetic INSERT и отсутствие NewTestClass/manual COMMIT/ROLLBACK/SELECT *; ноль markers во всех десяти new SQL targets.
- README.md: постоянный контракт полного согласованного набора и canary, separate Coder/Reviewer proof; historic 1/0/0/0 только для адаптации.
- docs/tools/prompts/architect_status_driven.md: только local sections; полный текущий набор с обязательным real canary; single-test wording не остаётся обязательным live rule.
- docs/tools/prompts/planner_status_driven.md: только local sections; полный текущий набор с обязательным real canary; single-test wording не остаётся обязательным live rule.
- docs/tools/prompts/coder_status_driven.md: только local sections; полный текущий набор с обязательным real canary; single-test wording не остаётся обязательным live rule.
- docs/tools/prompts/coder_migrations_gate.md: только local sections; полный текущий набор с обязательным real canary; single-test wording не остаётся обязательным live rule.
- docs/tools/prompts/reviewer_status_driven.md: только local sections; полный текущий набор с обязательным real canary; single-test wording не остаётся обязательным live rule.
- docs/playbooks/review_staged_or_commit.md: только local sections; полный текущий набор с обязательным real canary; single-test wording не остаётся обязательным live rule.
- docs/playbooks/review_merge_range.md: только local sections; полный текущий набор с обязательным real canary; single-test wording не остаётся обязательным live rule.
- docs/playbooks/post_merge_audit.md: только local sections; полный текущий набор с обязательным real canary; single-test wording не остаётся обязательным live rule.

## Steps / dependency handoff

1. Заменить все десять path-tracking carriers реальным SQL и создать exact testcase identities из таблицы. Никаких дополнительных тестовых процедур/setup hooks; девять testcase остаются точным составом.
2. Адаптировать parser/proof и независимые synthetic fixtures существующего test file; сохранить path/Git/config/target/redaction/custody regressions.
3. Согласовать девять permanent docs targets только в разрешённых sections; shared process bytes и local override N/A сохраняются. Все target edits завершаются до финального snapshot/proof.
4. Выполнить Coder offline gates и собственный proof по Commands; сохранить текущие portable facts и exact cleaned JUnit. Запись роли без actual proof не закрывает AC.
5. Reviewer отдельно проверяет текущие bytes, static SQL/T8/guard/refusal contract, повторяет offline gates и полный live proof со своим JUnit; единственный review host указан ниже. Общая dev-база сериализована: между RunAll и formatter другой Publish/RunAll запрещён.
6. Architect принимает current review и contextual db-state; human_explicit preview/отдельное разрешение close --commit сохраняются. Planner/Coder/Reviewer не получают commit authority.

## Commands

### Coder — после полной замены path-tracking carriers и синхронизации всех targets

```sh
make db-build
make lint
make test
make check-secrets
make db-proof JUNIT=docs/code_reviews/assets/261012_0141_get_reorder_candidates/reorder.junit.xml
make check-secrets
```

### Reviewer — независимо, после Coder и на том же final bundle

```sh
make db-build
make lint
make test
make check-secrets
make db-state
make db-proof JUNIT=docs/code_reviews/assets/261012_0141_get_reorder_candidates/reorder.review.junit.xml
make check-secrets
make db-state
```

Architect выполняет только contextual `make db-state` после Reviewer. Все команды из корня sibling; prepared Python 3.12 из PATH выбирает существующий Makefile. Офлайн gates: make/wrapper rc 0; test failures/errors 0; cache не восстанавливается. Каждый live proof: make/wrapper rc 0, exact девять identities, counts 9/0/0/0. Все target edits завершаются до proof. Снимки canonical bundle/HEAD снимаются непосредственно до и после собственного db-proof каждой роли и должны совпасть; target mutation после proof требует нового снимка и нового proof. JUnit/SHA-256 и counts/testcase фиксируются в Evidence. Snapshot и lint выполняются через действующий Planveyor facade по роли, без записи machine-specific PYBIN в проект. `setup`, `db-extract`, raw SQL и автоматическая смена среды не входят в этот handoff.

## Review route

- Primary artifact: `docs/code_reviews/261012_0141_get_reorder_candidates.md` — PLANNED до Reviewer.
- Lane type: code review; current BUNDLE proof через canonical producer.
- Review assets: Coder `docs/code_reviews/assets/261012_0141_get_reorder_candidates/reorder.junit.xml`; Reviewer `docs/code_reviews/assets/261012_0141_get_reorder_candidates/reorder.review.junit.xml`.
- Targets содержат только implementation/docs; plan, draft, live review и explicit assets — отдельные full-bundle members, не mutable current-review targets. Deletions отсутствуют.

## Critical invariants / traps / bypass paths

- Exact identities важнее totals: unknown/duplicate/missing canary/T1–T8 или nested red не превращаются в green при tests=9.
- Реальный canary сохранён отдельно от FakeTable; business fixtures не читают реальные данные. T6 покрывает все NULL masks, T7 удерживает int каждого операнда.
- Metadata/source proof T8 не подменяется table equality, implicit casts или SQL success text.
- Старый XML/чужой receipt/previous dev schema не доказывает current bytes. Fresh Publish → RunAll → formatter удерживает тот же target/config и observer; independent Reviewer proof обязателен.
- SQL guard/Git path refusal/redaction не ослабляются при адаптации XML. Stack.state/secrets остаются named contextual consumers.

## Assumptions / risks

Принятое окружение и cache подготовлены адаптацией. Current Coder SQL/tests proof и его binding описаны в Evidence связанного плана; независимая Reviewer проверка ещё обязательна. Любые target edits требуют нового current proof. Недоступная metadata/cache/connection — owning lane red; сервер, права и среда не чинятся молча. Новые Scope/правила/инструменты/приёмка требуют Architect-owned triage, semantic MAD Planner не меняет.

## Notes for Coder

PLAN_PATH важнее draft. Первоначальные SQL path-tracking carriers Planner полностью заменены реализацией Coder; RepositoryContractTests проверяет отсутствие markers во всех десяти SQL targets. Preflight не является db-build/live acceptance. Canonical ref заморожен из helper: applicability=not_applicable, reason_code=no_machine_authority_change, carrier_sha256=d435d5a496b546069ce71672025c9ead04a3366aa611afb39abdfe8e3480e204. Baseline files Makefile/sqlproj/canary/stack_brief/adaptation history/Planveyor runtime — read-only; новые baseline edits требуют штатного reroute.

## Review stamps (append-only)

- [2026-10-12 02:51] (Planner) Draft создан и конкретизирован: 21 exact targets, T1–T8/canary, emitter/fixture/consumer inventory, primary/contextual lanes и commands; реализация и живые proof пока не выполнены.
- [2026-10-12 03:01] (Planner) Post-handoff проверка уточнила Commands: target edits завершаются до proof, равенство canonical bundle/HEAD проверяется непосредственно до и после собственного db-proof каждой роли; смена targets после proof требует нового proof. Exact inventory и реализация не изменены.
- [2026-10-12 03:23] (Coder) Все 21 targets реализованы, десять SQL path-tracking carriers заменены полностью. Current Coder proof 9/0/0/0, одинаковый canonical bundle/HEAD до и после, offline gates и отдельный JUnit описаны в Evidence связанного плана. Targets/deleted_paths/derived authority ref/provenance не менялись; independent Reviewer proof и human_explicit closeout ещё обязательны.

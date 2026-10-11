# Code draft: Адаптация sibling под SQL Server 2019 / Northwind

**Date:** 2026-10-11 16:44
**Cluster:** data
**Related plan:** `docs/plans/261011_1523_stack_adaptation.md`
**Author role:** Planner
**Status:** draft

## Meta (machine-readable JSON)
```json
{
  "code_draft_meta": {
    "plan": "docs/plans/261011_1523_stack_adaptation.md",
    "cluster": "data",
    "targets": [
      {
        "path": "Makefile",
        "kind": "make"
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
        "path": "global.json",
        "kind": "json"
      },
      {
        "path": ".config/dotnet-tools.json",
        "kind": "json"
      },
      {
        "path": "requirements-dev.txt",
        "kind": "config"
      },
      {
        "path": ".sqlfluff",
        "kind": "config"
      },
      {
        "path": "NuGet.Config",
        "kind": "config"
      },
      {
        "path": "Directory.Build.props",
        "kind": "config"
      },
      {
        "path": "sql/Northwind/Northwind.sqlproj",
        "kind": "sqlproj"
      },
      {
        "path": "sql/Northwind/Imported/dbo/StoredProcedures/CustOrderHist.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/StoredProcedures/CustOrdersDetail.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/StoredProcedures/CustOrdersOrders.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/StoredProcedures/Employee Sales by Country.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/StoredProcedures/Sales by Year.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/StoredProcedures/SalesByCategory.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/StoredProcedures/Ten Most Expensive Products.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Categories.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/CustomerCustomerDemo.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/CustomerDemographics.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Customers.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/EmployeeTerritories.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Employees.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Order Details.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Orders.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Products.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Region.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Shippers.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Suppliers.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Tables/Territories.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Alphabetical list of products.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Category Sales for 1997.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Current Product List.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Customer and Suppliers by City.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Invoices.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Order Details Extended.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Order Subtotals.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Orders Qry.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Product Sales for 1997.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Products Above Average Price.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Products by Category.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Quarterly Orders.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Sales Totals by Amount.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Sales by Category.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Summary of Sales by Quarter.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Imported/dbo/Views/Summary of Sales by Year.sql",
        "kind": "sql"
      },
      {
        "path": "sql/Northwind/Authored/.gitkeep",
        "kind": "config"
      },
      {
        "path": "sql/tests/Northwind.Tests.sqlproj",
        "kind": "sqlproj"
      },
      {
        "path": "sql/tests/StackAdaptationTests/StackAdaptationTests.sql",
        "kind": "sql"
      },
      {
        "path": "sql/tests/StackAdaptationTests/test_Products_table_exists.sql",
        "kind": "sql"
      },
      {
        "path": "docs/stack_brief.md",
        "kind": "doc"
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

Derived binding скопирован только из validated canonical oracle upstream carrier; semantic decision core принадлежит Architect и не дублируется. Этот ref не является live SQL proof.

## Provenance / session context
- Source plan provenance: `reuse PLAN_PATH carrier unless this draft is created/imported/backfilled separately`
- Relation: `continued-here`
- Thread ID: `01a12b07-8170-75a0-9c4b-26e325bcc5b1`
- Parent thread ID: `N/A (why=not exposed by env, wrapper receipts, or session stats)`
- Session SID: `N/A (why=.planveyor.session.planner is missing or empty)`
- Launch surface: `unknown (why=no env, wrapper receipt, or session stats origin identified the launch surface)`
- Captured from: `env`
- Captured at: `2026-10-11T13:43:56Z`

## Purpose
Дать Coder exact paths и проверяемую последовательность для SQL-проектов, обвязки make и постоянных local rules. Draft фиксирует contract, а не реализацию. Свежая dev-проверка, реальный canary и независимые JUnit остаются обязательными будущими доказательствами.

## Reviewability preflight receipt
- `proof-path class`: checked-in repo-local helper — scripts/sql.py через Makefile.
- `mandatory primary lane`: make test, make db-build, make lint, make check-secrets; Coder и Reviewer отдельно make db-proof с разными JUnit.
- `mandatory non-primary carrier / contextual lane`: make db-state — Architect/Reviewer; читает schema/object/test-class/last-result catalogs, не объявляет canary success.
- `exact helper path + support files`: scripts/sql.py, scripts/test_sql.py, Makefile, global.json, .config/dotnet-tools.json, requirements-dev.txt, .sqlfluff, NuGet.Config, Directory.Build.props, обе .sqlproj и два SQL-файла единственного canary.
- `dependent tests / dependent docs / known consumer paths`: scripts/test_sql.py; README.md, docs/stack_brief.md и восемь exact local carriers ниже. Wrapper rc/phase — blocking verdict; XML/counters/testcase — live evidence; db-state — contextual evidence. Старый XML или derived success не перекрывают отказ.
- `preconditions / seed-discovery`: уже установленный macOS/Python 3.12/.NET SDK/go-sqlcmd; Coder выполняет setup один раз, затем schema-only Extract. Администратор уже готовит dev-базу/маркер/права; роли этого не делают.
- `reroute rule`: технический отказ остаётся у owning role; новое решение scope/прав/приёмки — Ready for Architect response. Нельзя обходить refusal серверной настройкой или другим инструментом.
- `perceptual truth-source split`: N/A (why=no visual proof); writable hosts — current tSQLt.TestResult и database/catalog/property/login state. Unchanged formatter XML и fresh guard result — canonical projections, не отдельная SQL authority; новых SQL steps не добавляется.
- `discovery-or-seed`: только make setup и make db-extract Coder; ни checked-in synthetic corpus, ни новый seed SQL не добавляются.
- `receipt-reuse-only`: один db-proof удерживает ту же настроенную dev-цель через guard → Publish → RunAll → formatter; не переключает базу и не переиспользует прежний XML. Отказ любого downstream шага означает отказ текущего proof.
- Stable identity: текущие HEAD/canonical bundle_sha256, отдельные относительные JUnit path/SHA-256, counts и единственный testcase StackAdaptationTests.[test Products table exists]. Connection values не сохраняются.
- Exact observer boundary: JUNIT/Git до любых действий; старый допустимый untracked XML удалён до build; один свежий SQL guard непосредственно перед Publish; formatter после RunAll того же запуска.
- Mutation truth / next readback: новый строго разобранный formatter XML, totals=1/0/0/0 и реальная dbo.Products типа U. Db-state читает текущие catalogs, но не заменяет JUnit. notice/success text != mutation truth.
- `runtime-lineage preflight`: обвязка проверяет инструменты/назначенную конфигурацию/цель; missing cache/env/permission — truthful refusal, не live product success. Reviewer не повторяет setup/Extract и не меняет сервер.
- Retention: .tmp и временные fixtures — transient local sanity only; docs/code_reviews/assets/261011_1523_stack_adaptation/*.xml — durable operator/review evidence; review.md — durable review carrier.
- Concurrency boundary: роли и SQL proof последовательно на общей dev-базе; true concurrent writer proof не заявляется.

### Truth-host fixture matrix
| authoritative_host | derived_summary_field | green_case | missing_case | ambiguous_case | present_but_red_or_inconsistent_case | expected_fail_closed_verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Текущий tSQLt.TestResult после RunAll; projection — unchanged formatter XML | XML counts/testcase/success | Один current successful canary, totals=1/0/0/0 | Нет текущего результата/пустой XML | Stale/duplicate results, два document/testcase, duplicate totals | Failure/error/skipped host отражён в XML, но derived totals/summary green или counters несовместимы | 1; old XML/summary не заменяют current host, RunAll nonzero не green |
| Текущие database identity, database-level sys.extended_properties marker и login sysadmin membership; writer=администратор | fresh guard SQL result / target accepted | DB_NAME=настройка, marker EXISTS=1, sysadmin=0, не Northwind | NULL/нет current readback | Несколько/обрезанная строка | Предыдущий projection green, current marker missing/sysadmin либо source-name variant | 3, ни одного Publish; connection failure отдельно 4 |
| Текущие sys.schemas/sys.objects/tSQLt catalogs | db-state inventory/results | Полный readback | Пустая база/нет tSQLt | Неоднозначный/неполный результат | Старый TestResult green, dbo.Products отсутствует/не U | Explicit empty/not-tested либо refusal 4; не canary verdict |

## Targeted changes (by file)
| Target | Назначение / граница |
| --- | --- |
| `Makefile` | Новый literal target; path-tracking stub заменяет Coder. |
| `scripts/sql.py` | Новый literal target; path-tracking stub заменяет Coder. |
| `scripts/test_sql.py` | Новый literal target; path-tracking stub заменяет Coder. |
| `global.json` | Новый literal target; path-tracking stub заменяет Coder. |
| `.config/dotnet-tools.json` | Новый literal target; path-tracking stub заменяет Coder. |
| `requirements-dev.txt` | Новый literal target; path-tracking stub заменяет Coder. |
| `.sqlfluff` | Новый literal target; path-tracking stub заменяет Coder. |
| `NuGet.Config` | Новый literal target; path-tracking stub заменяет Coder. |
| `Directory.Build.props` | Новый literal target; path-tracking stub заменяет Coder. |
| `sql/Northwind/Northwind.sqlproj` | Новый literal target; path-tracking stub заменяет Coder. |
| Generated Extract files | 36 literal file paths из фактического Extract перечислены только в authoritative targets выше. |
| `sql/Northwind/Authored/.gitkeep` | Сохранить пустой Authored без авторского SQL в адаптации. |
| `sql/tests/Northwind.Tests.sqlproj` | Новый literal target; path-tracking stub заменяет Coder. |
| `sql/tests/StackAdaptationTests/StackAdaptationTests.sql` | Новый literal target; path-tracking stub заменяет Coder. |
| `sql/tests/StackAdaptationTests/test_Products_table_exists.sql` | Новый literal target; path-tracking stub заменяет Coder. |
| `docs/stack_brief.md` | Уточнить технические пути manifest по этому handoff, сохранить факты Owner. |
| `README.md` | Постоянный runbook make, ownership и proof/refusal без имени текущего плана. |
| `docs/tools/prompts/architect_status_driven.md` | Изменяются только local bodies; shared prefix и override invariant сохраняются. |
| `docs/tools/prompts/planner_status_driven.md` | Изменяются только local bodies; shared prefix и override invariant сохраняются. |
| `docs/tools/prompts/coder_status_driven.md` | Изменяются только local bodies; shared prefix и override invariant сохраняются. |
| `docs/tools/prompts/coder_migrations_gate.md` | Изменяются только local bodies; shared prefix и override invariant сохраняются. |
| `docs/tools/prompts/reviewer_status_driven.md` | Изменяются только local bodies; shared prefix и override invariant сохраняются. |
| `docs/playbooks/review_staged_or_commit.md` | Изменяются только local bodies; shared prefix и override invariant сохраняются. |
| `docs/playbooks/review_merge_range.md` | Изменяются только local bodies; shared prefix и override invariant сохраняются. |
| `docs/playbooks/post_merge_audit.md` | Изменяются только local bodies; shared prefix и override invariant сохраняются. |

Coder заменил все path-tracking stubs текущей реализацией; Authored/.gitkeep пуст. Existing docs менялись только в разрешённых local bodies и synchronous carriers.

Generated-tree restamp выполнен после successful make db-extract: 36 literal generated paths в code_draft_meta.targets, без directory host. Имена взяты только из filesystem inventory; SQL names не разбирались, SQL files руками не правились. Это разрешённый bounded package-to-file restamp, real scope expansion отсутствует. План, draft, primary review и explicit assets — отдельные lifecycle/bundle members, не implementation targets. .tmp/.env.local не добавляются.

### Manifest / cache contract
- global.json: SDK 10.0.401, rollForward latestFeature. Microsoft.Build.Sql/2.3.0 и Sql150DatabaseSchemaProvider в обоих SQL projects; тестовый ProjectReference на ../Northwind/Northwind.sqlproj и tSQLt.Dacpacs 1.0.8083.3529 / DacpacName=tSQLt.2019, IncludeCompositeObjects на Publish.
- .config/dotnet-tools.json: локальный Microsoft.SqlPackage 170.5.96, не global tool; requirements-dev.txt: SQLFluff==3.4.2. .sqlfluff: dialect tsql, templater raw, max_line_length 120; lint только Authored и tests, Imported исключён.
- NuGet.Config / process environment: packages/caches только .tmp/nuget; DOTNET_CLI_HOME=.tmp/dotnet-home для supporting files/local resolver; Python venv/cache .tmp/venv и .tmp/pip-cache. Directory.Build.props задаёт отдельные .tmp/build/ subtrees obj/bin для каждого проекта и исключает output из SQL inputs. Все дочерние процессы получают согласованную cache environment.
- Только make setup делает dependency restore/install с сетью; db-build использует no-restore и подготовленные caches, lint/test/check-secrets офлайн. Нет home/shell/PATH/system tool изменений; существующий go-sqlcmd не ставить заново.
- make test — stdlib unittest на объявленном Python 3.12 из PATH, без настоящей .env.local/SQL/dependency restore. Остальные non-live цели не требуют credentials и не открывают .env.local; live connection читает только scripts/sql.py. Setup не является SQL-подключением.
- make экспортирует JUNIT как literal data в environment обвязки; не встраивает пользовательский path в shell command/argv interpolation. Ни Makefile, ни wrapper не печатают credential argv.

### Shared carrier consumer contract
Makefile — CLI consumer; scripts/test_sql.py — dependent tests. README/анкета и local sections восьми prompt/playbooks обязаны назвать make-only entrypoints, role ownership, source/dev distinction, guard/refusal codes, sequential independent proofs и portable evidence. В README/local rules нет имени текущего плана, machine-private interpreter, secrets или server address. За пределами двух local bodies каждого carrier байты совпадают с baseline HEAD; запрета/перепорядочения общего lifecycle через override нет. AGENTS.md, docs/README.md, .gitignore, общие prompt/playbook bodies и runtime — read-only context.
Owner-facing Manager command/one-shot dispatch surface: N/A (why=unchanged). Planveyor receipt schema parser/emitter inventory/API payload change: N/A (why=unchanged); SQL XML validator новый локальный Coder helper, единственный producer — существующий permanent tSQLt.XmlResultFormatter, которому не разрешены изменения.

## Review route
- `Primary artifact`: docs/code_reviews/261011_1523_stack_adaptation.md — materialized; live verdict принадлежит Reviewer, после Coder fixes требуется independent same-file rerun.
- `Lane type`: hybrid (code review, offline checks, live db-state/db-proof и synchronous docs); non-doc implementation bundle.
- Coder JUnit: docs/code_reviews/assets/261011_1523_stack_adaptation/canary.junit.xml.
- Reviewer JUnit: docs/code_reviews/assets/261011_1523_stack_adaptation/canary.review.junit.xml.
После появления reports Reviewer добавляет явные asset refs в review. Planned first-pass review допускает только preflight; post-review exact bundle требует штатный check.

## Patch sketch (keep it small)
1. Заменить stubs manifests/Makefile/wrapper/unit tests; сохранить точные pins и make-only role commands. Test harness использует recording fake executor, temporary Git/non-Git roots и synthetic tree/XML, без новых helpers или checked-in corpus.
2. Обвязка разделяет configuration/JUNIT/tool validation и stage execution; SQL execution/readback не прячутся за generic success. Offline goals не читают live config. Для live .env.local проверить regular/non-symlink 0600/ignored/untracked и четыре nonempty unique keys; не source как shell.
3. Extract только Northwind: /Action:Extract, /p:ExtractTarget=SchemaObjectType, /p:ExtractAllTableData=False, /p:ExtractReferencedServerScopedElements=False, /SourceEncryptConnection:True, /SourceTrustServerCertificate:True. Temporary tree после удаления Security/Users/Roles/Permissions и эквивалентов должен иметь ровно 13/16/7 отдельных SQL files и не содержать CREATE USER/ALTER ROLE/GRANT/INSERT. Категории/файлы считаются без разбора имён объектов; одночастный CustOrderHist допустим.
4. Swap Imported — настоящее атомарное directory replacement/exchange на macOS, включая непустую старую tree; последовательное rename old-away/new-in с окном отсутствующего дерева не считать atomic. Стандартная библиотека (включая bounded ctypes вызов штатной macOS directory-exchange API) допустима, дополнительный dependency/helper нет. Validation/swap failure сохраняет либо восстанавливает old Imported bytes; офлайн filesystem fixture доказывает actual nonempty-directory success и отказ, а не только fake SQL output.
5. Создать test schema и его штатный tSQLt test-class marker в SQL source, одну procedure [test Products table exists] только с проверкой OBJECT_ID(N'dbo.Products', N'U') и tSQLt failure при отсутствии. Не выполнять NewTestClass/FakeTable, не добавлять бизнес-SQL/data, не менять permanent formatter.
6. Db-proof принимает только safe mandatory relative .xml/non-symlink path с достоверным Git-untracked readback; отказ до удаления/setup/build/SQL. Удалить только old eligible XML, собрать проект, выполнить fresh one-query guard DB_NAME/EXISTS database-level planveyor.designated_dev/IS_SRVROLEMEMBER без значения свойства; Northwind как dev-target всегда rejected. Сохранить same connection до конца. Непосредственно затем Publish: IncludeCompositeObjects=True, DropObjectsNotInSource=True, ExcludeObjectTypes=Users;Logins;RoleMembership;Permissions, DropExtendedPropertiesNotInSource=False, ScriptDatabaseOptions=False, BlockOnPossibleDataLoss=True, /TargetEncryptConnection:True, /TargetTrustServerCertificate:True.
7. EXEC tSQLt.RunAll; без параметров → EXEC tSQLt.XmlResultFormatter;. go-sqlcmd всегда --encrypt-connection=mandatory -C -b; для XML дополнительно -h -1 -y 0 -w 65535. sqlcmd пароль только environment; SqlPackage password argument — явно принятый Owner contract, никогда в evidence/logs.
8. Строгий XML parse: complete single supported JUnit document, один test class/name canary, согласованные integer totals 1/0/0/0 и отсутствие failure/error/skipped. DTD/entity/extra/duplicate/malformed/truncated не green. Очистка hostname/server info и credentials/private paths на stdout/stderr, timeout/nonzero/exception и любом сохранённом JUnit; очистка не удаляет test failures. Новый очищенный XML пишется atomic file replacement; old proof не переживает failed run.
9. Db-state читает каталоги схем/объектов/tSQLt classes/last results, COLLATE DATABASE_DEFAULT для string expressions, пустая/без tSQLt база explicit empty/not-tested. Не RunAll/Publish и не canary acceptance. Check-secrets читает Git-known и untracked nonignored files плюс явные JUnit, исключая .git/.tmp/.env.local, и отказывает без вывода найденного значения.
10. После successful Extract restamp exact Imported files и завершить все оставшиеся implementation/doc targets, включая README/brief/local bodies, ДО canonical bundle snapshot/Coder gates/proof. Любые target edits после proof означают affected-check rerun, новый snapshot и новый proof до handoff. Reviewer независимо последовательно проверяет те же final target bytes; Architect делает только db-state и своё acceptance.

## Critical invariants / traps / bypass paths
- Invariant: dev-only write. Trap: прошлый guard/schema build/текст успеха выглядит green. Bypass: target Northwind, иной connection между guard и Publish, missing/ambiguous marker/sysadmin readback. Proof: TargetGuardTests/call sequence и текущий live proof.
- Invariant: current JUnit custody. Trap: old XML сохраняется после build/SQL failure. Bypass: tracked/unknown Git, symlink/ancestor escape, make interpolation, duplicated/truncated XML и summary green поверх host red. Proof: JUnitPathTests/ProofTests/RedactionTests плюс отдельные два live JUnit.
- Invariant: safe schema source/atomic Imported. Trap: файлы конкатенируются/имена анализируются либо two-rename window объявляется atomic. Bypass: security residual/category mismatch/swap failure. Proof: ExtractTests с реальным nonempty filesystem exchange и отказами; current 36-file source inventory перед snapshot.
- Invariant: contextual lane не исчезает. Trap: fake executor/one Coder report закрывает всё. Bypass: Reviewer использует прежний XML/делает setup или пропускает db-state. Proof: независимый review JUnit и явный текущий contextual readback.
- Alternate entrypoints: все project commands только make; scripts/sql.py — implementation support, роли не запускают его напрямую и не исполняют SQL через другой CLI. No automatic retry SQL/Publish; no permanent formatter mutation.

## Assumptions / risks
- Факты Owner и N/A admission не означают live readiness; SQL rights/CLR/dev marker заранее обеспечивает администратор.
- Bounded timeouts: setup 600 s; Extract/build/lint/Publish 300 s; guard/formatter/db-state 60 s; RunAll 120 s. timeout/launch failure redacted, category сохраняется, SQL не повторяется автоматически.
- Wrapper codes: 0 success; 1 test/JUnit; 2 configuration/path/Git/secrets/invalid source input; 3 target guard; 4 connection/read SQL; 5 build/lint/Extract artifact preparation; 6 Publish. Actual make rc записывается отдельно. Вывод только safe phase/category/rc, без raw stream/env/argv/exception repr.
- Shared dev/Imported — serialized ownership. Reviewer runtime/cache refusal нельзя скрыть повторным setup/Extract; это возврат owning role, новый semantic decision при необходимости через Architect.

## Tests / proof inventory
### Что написать / поправить
Все офлайн-тесты — в scripts/test_sql.py, стандартный unittest; вызываются только make test. Subprocess/SQL подменяются recording fake executor с явно заданными stdout/stderr/rc/TimeoutExpired; настоящие Git fixtures используют временный репозиторий, случаи unknown Git — отдельный non-Git temporary directory. Connection fixtures содержат только синтетические значения. Synthetic Extract fixture создаёт во временном каталоге 13/16/7 SQL-файлов, а не checked-in образец Northwind. .tmp/ и temporary directories — transient local sanity only; fixture corpus, данные и дополнительные helpers в repo не добавляются.

| Группа в scripts/test_sql.py | Обязательные случаи / наблюдаемый исход |
| --- | --- |
| ConfigTests | Для live db-extract/db-proof/db-state: missing/unreadable/non-regular/symlink/не-0600/неигнорируемая/отслеживаемая .env.local, отсутствующие/пустые/дублированные четыре ключа или неизвестный Git → 2 до удаления/build/SQL. Non-live setup/db-build/lint/test/check-secrets не открывают .env.local и работают без неё; отдельная fixture это доказывает. Неверные требуемые Python/платформа/инструмент → truthful config refusal 2. Не исполнять файл как shell; кавычки/$/semicolon остаются данными. Все connection fixtures синтетические. |
| SetupBuildTests | Точные версии manifest/provider/ProjectReference/DacpacName; все кэши/obj/bin/venv/tool files только в .tmp; setup единственный dependency restore/install. db-build использует cache и no-restore; missing cache/сбой/таймаут build/lint → 5 без сети/Publish. make не исполняет JUNIT как shell-текст, не печатает secret argv. |
| ExtractTests | Успех 13/16/7, одночастный CustOrderHist, сохранение отдельных файлов; удаление Security/Users/Roles/Permissions и эквивалентных каталогов независимо от регистра/вложенности. Оставшиеся CREATE USER, ALTER ROLE, GRANT, INSERT (регистр/пробелы/переносы), неправильные категории/количества, symlink/необычный file type или неудачный swap → отказ; старый Imported побайтно сохранён либо восстановлен, частичного нового дерева нет. Подсчёт по каталогам/файлам, без разбора имён SQL. |
| TargetGuardTests | Config target Northwind (включая northwind/NORTHWIND и padding variants), несовпадение DB_NAME, отсутствие свойства, sysadmin, NULL/неоднозначный/обрезанный guard result → 3, Publish отсутствует. Source rejection не зависит от регистра/паддинга имени. Ошибка/таймаут подключения → 4. Успех — один свежий запрос с именем базы, EXISTS database-level свойства и IS_SRVROLEMEMBER; значение свойства не выбирается. Recording sequence доказывает guard непосредственно перед Publish, те же значения подключения до formatter; flags Publish точные, маркер не удаляется. |
| JUnitPathTests | Missing/absolute/../outside/non-.xml, symlink leaf/ancestor, directory/non-regular leaf, tracked Git, Git error/malformed result/non-Git repo → 2 до удаления/setup/build/SQL. Строго untracked old XML удаляется до build; build failure не оставляет старый proof. Ошибка atomic write не даёт успеха или частичного XML; paths с пробелами/metacharacters остаются literal data. |
| ProofTests | Успех: build → guard → Publish → RunAll без параметров → formatter; ровно один testcase класса StackAdaptationTests с именем test Products table exists (допустима штатная bracket/schema форма tSQLt), totals=1/0/0/0. Пустой/обрезанный XML, DTD/entity, второй document, неверный root/counters, отрицательные/нецелые/несогласованные totals, duplicate/extra/wrong testcase, failure/error/skipped → 1. Test failure/error RunAll → 1, RunAll/formatter connection failure/timeout → 4, Publish failure/timeout → 6. RunAll nonzero не становится success даже при оставшемся green TestResult/formatter XML; connection failure не маскируется как failed canary. Постоянный formatter не менять; downstream стадия после отказа не объявляет success. |
| RedactionTests | На success, каждом nonzero, запуске с секретным argv, TimeoutExpired с bytes/text/None stdout/stderr, invalid XML и write failure: hostname/server/connection string/password/private path отсутствуют в stdout/stderr и любом сохранённом XML. Raw streams, env, argv и exception repr не публикуются. JUnit cleaning не удаляет failure/error/skipped и не меняет результат на success. |
| DbStateTests | Пустая база без tSQLt — явный empty/not-tested readback без RunAll/Publish; populated catalogs и последние результаты читаются независимо. Missing/incomplete/ambiguous/error catalogs не выдают green canary. Строковые выражения с COLLATE DATABASE_DEFAULT, без hostname/server identity/значения маркера. |
| RepositoryContractTests | Один SQL test procedure, реальный OBJECT_ID(N'dbo.Products', N'U'), без FakeTable/NewTestClass/бизнес-данных; lint только Authored/tests. check-secrets проверяет Git-known files + untracked неигнорируемые files и явные JUnit, никогда .git/.tmp/.env.local; leak fixture отказывает с 2 без вывода значения. В восьми carriers вне двух local bodies байты совпадают с baseline HEAD; local rules без имени текущего плана, engine path и process overrides. Нет path-tracking stub в final targets. |

Постоянные SQL-файлы: sql/tests/StackAdaptationTests/StackAdaptationTests.sql объявляет schema/test-class marker в исходнике; sql/tests/StackAdaptationTests/test_Products_table_exists.sql — единственная test procedure. Настоящий canary использует только каталог объектов и проверяет U; fake executor/синтетический XML не закрывают live acceptance.

### Что прогнать
1. Coder реализует обвязку/manifest/stubs, выполняет make test (offline, без настоящей конфигурации/SQL), make setup один раз и make db-extract из readonly Northwind. Только после успешного Extract restamp code_draft_meta.targets: заменить directory host Imported на 36 буквальных полученных SQL paths; package host и stubs в final inventory запрещены.
2. Coder завершает ВСЕ implementation/doc targets (включая README, brief и local bodies) и exact Imported restamp до canonical snapshot/live proof; затем make db-build, make lint, make test, make check-secrets и make db-proof JUNIT=docs/code_reviews/assets/261011_1523_stack_adaptation/canary.junit.xml. Success — обе offline/live lanes, wrapper rc 0, свежий 1/0/0/0 canary. После proof target edits требуют повторных affected checks, нового snapshot и нового proof до handoff; plan Evidence не входит в mutable targets.
3. Reviewer после Coder на неизменных target bytes independently выполняет make db-build, make lint, make test, make check-secrets, make db-state, canonical target snapshot и make db-proof JUNIT=docs/code_reviews/assets/261011_1523_stack_adaptation/canary.review.junit.xml; setup/Extract не повторяет. Потеря cache — stop, не скрытая сеть/второй Extract.
4. Architect после появления обвязки выполняет только make db-state и сверяет независимые JUnit/current review. Empty/diagnostic db-state или предыдущий XML не заменяют proof.
5. Для каждого real proof роль фиксирует HEAD и authoritative bundle_sha256 через existing planveyor_review_target_snapshot на final file inventory до и после прогона; mismatch требует нового proof, не reuse XML. HEAD получает read-only Git. В evidence только portable make command, отдельные rc make/обвязки, HEAD/bundle SHA, relative JUnit path/SHA, counters и testcase; raw logs/сведения подключения не сохраняются.


## Notes for Coder
- План приоритетнее sketch; новых Owner facts/approval не создавать. Technical decisions здесь остаются внутри утверждённого Scope; новый semantic blocker вернуть через Ready for Architect response.
- Перед Ready for Review заменить все stubs и restamp Imported host в exact 36 files; dependent docs все в targets. Не убирать обязательную lane из-за env drift.
- Реальные команды только make из PLAN_PATH. До/после каждого live proof после final target restamp использовать existing facade planveyor_review_target_snapshot PLAN_PATH --current-bundle и read-only git rev-parse HEAD. Bundle digest не вычислять собственной схемой.
- Evidence сохраняет make command, make/wrapper rc, HEAD, canonical bundle SHA до/после, относительный JUnit path/SHA-256, counts и testcase. Изменение targets между snapshot и proof/review означает новый proof; исходные журналы с private values не писать.
- .env.local — не target, роли values не читают. Не делать server changes/setup роли Reviewer, external models/MCP, stage/Done/commit/push/publication/close --commit.

## Review stamps (append-only)
- [2026-10-11 16:44] (Planner) CREATED: exact implementation inventory, derived machine-authority ref, proof/fixture/consumer contracts и separate review route materialized. Это planning artifact; stubs не объявляются implementation, offline/live SQL checks ещё не выполнялись.
- [2026-10-11 16:50] (Planner) REVIEWED/FINALIZED: ordinary lint, canonical preflight/doc-lint и derived ref readback зелёные; primary/contextual lanes и fail-closed fixtures explicit, upstream Owner facts/semantic carrier неизменны. New targets только stubs/empty generated host; все implementation/live acceptance checks остаются будущей работой ролей.
- [2026-10-11 17:04] (Planner) SECOND PASS FIXES: writable truth hosts отделены от projections, dotenv validation только live, source-name variants и RunAll refusal конкретны; все doc/code targets завершить до snapshot/proof. Восстановлен заголовок Targeted changes table. Target set/MAD/pins/Owner facts сохранены; исправления контракта отражены в plan, implementation/SQL не выполнялись.

- [2026-10-11 17:33] (Coder) MATERIALIZED: все final targets готовы, Imported restamped 36 literal Extract files; offline gates и current Coder JUnit зелёные. Canonical BUNDLE=current SHA-256=8f67cf082b72143b65fcc115e03b11a508376b74b720a598a7113710f418bedb before/after equal. Reviewer independently выполняет отдельный db-state/db-proof; no staging/commit.
- [2026-10-11 18:31] (Coder) SAME-CONTRACT REWORK: B1/B2 implementation и regression в scripts/sql.py/scripts/test_sql.py, synchronous existing docs уточнены; targets=60 и upstream N/A ref unchanged. Новый собственный canonical before/after bundle SHA-256=fe1be1e2ca75dbb05485dbd29d939169d46ab8f53c5dfcd3179e2b82b8cb3200, make gates/48 tests и live Coder proof зелёные. Current red review/support/compact не переписывались; Reviewer обязан independent same-file rerun, прежний Reviewer JUnit historical. Эта lifecycle route annotation не входит в implementation hash.
- [2026-10-11 19:37] (Coder) B3 SAME-CONTRACT REWORK: physical filesystem/index identity и leaf/ancestor refusal regressions в scripts/sql.py/scripts/test_sql.py; 58 other targets/metadata/ref unchanged, synchronous docs intentionally unchanged по existing tracked/unknown refusal contract. Own make gates/53 tests и новый live proof passed; canonical before/after bundle SHA-256=171833e40098d72075515cbbc29f20e0021325aea5b7479afe0111a872bf8302 byte-equal. Existing closed Q1 recovery направляет downstream Reviewer generation и independent same-file verdict; B3 open/red, B1/B2 historical-fixed/carriers untouched. No staging/commit/CENSOR.

- [2026-10-11 21:37] (Coder) B3 MISSING-INDEXED-ALIAS SAME-CONTRACT REWORK: scripts/sql.py проверяет полный trusted index до допуска missing JUNIT, NFD/caseless aliases fail closed без inode; scripts/test_sql.py добавляет actual before-config/no-recreation negatives и legitimate untracked positives. Targets=60/remaining 58 bytes/MAD/ref unchanged; synchronous docs intentionally unchanged по прежнему untracked/unknown refusal contract. make gates/56 tests и новый own live proof passed, canonical before/after bundle SHA-256=51ebdc9ffdf974603e58538df1270ec68c3eb0e53e761c5d83ffb5705b6fbf08 byte-equal. Reviewer-owned red B3/B1-B2 fixed lineage/carriers сохранены; existing closed Q1 generation recovery/independent same-file verdict mandatory. No setup/Extract repeat/staging/commit/CENSOR.

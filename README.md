# SQL Server / Northwind sibling

Проект ведёт схему SQL Server 2019, compatibility 150. Northwind служит только
читаемым источником схемы. Publish и tSQLt разрешены в отдельной назначенной
администратором dev-базе с database-level маркером `planveyor.designated_dev`.
Сервер, базы, логины, CLR и маркер роли не создают и не меняют. Бизнес-данные и
production вне объёма. Рабочий процесс Planveyor описан в [docs/README.md](docs/README.md).
Проход от пустого sibling до двух закрытых планов, обновление движка, требования
к серверу и к Codex описаны в [docs/tools/mssql_walkthrough.md](docs/tools/mssql_walkthrough.md).

## Среда и зависимости

Нужны подготовленные macOS, Python 3.12 первым в PATH, .NET SDK и go-sqlcmd.
`global.json` задаёт SDK 10.0.401 и latestFeature. Проекты закрепляют
Microsoft.Build.Sql 2.3.0 и Sql150DatabaseSchemaProvider; тестовый проект
использует tSQLt.Dacpacs 1.0.8083.3529, DacpacName tSQLt.2019 и ProjectReference.
SqlPackage 170.5.96 — local dotnet tool в `.config/dotnet-tools.json`.
SQLFluff 3.4.2 из `requirements-dev.txt`: tsql, raw, длина 120 в `.sqlfluff`.
Обновления пакетов автоматически не выполняются.

`make setup` один раз восстанавливает зависимости с сетью. Supporting files,
local tools, NuGet packages/cache, Python venv/cache и SQL obj/bin остаются в
`.tmp/`: `dotnet-home/`, `nuget/`, `venv/`, `pip-cache/`, `build/<project>/`.
`NuGet.Config` и `Directory.Build.props` закрепляют эти границы. Home, shell,
PATH, системные инструменты и настройки Codex не изменяются.
Последующие build/lint/test/check-secrets работают офлайн. Отсутствующий cache
означает отказ; Reviewer не повторяет setup или Extract автоматически.

## Конфигурация

Администратор кладёт `.env.local` в корень: regular file, без symlink, 0600,
ignored и untracked. Нужны четыре непустых уникальных ключа: SQLCMDSERVER,
SQLCMDDBNAME, SQLCMDUSER, SQLCMDPASSWORD. Файл читает только обвязка
`scripts/sql.py`; роли значения не открывают. Это данные, не shell script.
Offline цели файл не читают. Пароль sqlcmd передаётся через environment,
SqlPackage — аргументом по принятому контракту однопользовательского Mac.
Raw argv, SQL streams, ошибки, hostname и сведения сервера не выводятся.

Git lookup считает JUNIT буквальным именем, включая pathspec magic и metacharacters.
Ambient `GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_INDEX_FILE` (даже пустые)
дают rc 2 до JUNIT/config/deletion/build/SQL. Обвязка их не сбрасывает и не выбирает
другой index; [ADR 010](docs/adr/010-trusted-local-git-metadata-boundary.md) задаёт
эту operational-red границу для supported checkout.

## Код и источник

Основной проект — `sql/Northwind/Northwind.sqlproj`. `Imported/` получает только
результат Extract, без ручной правки, разбора имён объектов или конкатенации.
Авторский SQL живёт в `Authored/`; при первичной адаптации он оставался пустым.
Тестовый проект — `sql/tests/Northwind.Tests.sqlproj`; тесты — `sql/tests/<Class>/`.
Единственный canary `StackAdaptationTests.[test Products table exists]` проверяет
реальную `dbo.Products` типа U через OBJECT_ID, без FakeTable, NewTestClass и
чтения бизнес-данных. Class/schema marker объявлен в SQL source.

`dbo.GetReorderCandidates` без параметров возвращает активные товары с положительным
`Shortage = ReorderLevel - (UnitsInStock + UnitsOnOrder)`. Числовые NULL считаются
нулём; каждый операнд приводится к int до арифметики. Результат — `ProductID int`,
`ProductName nvarchar(40)`, `Shortage int`, сортировка по `ProductID ASC`.
Восемь `GetReorderCandidatesTests` используют FakeTable и синтетические данные;
T8 отдельно проверяет метаданные результата и ORDER BY самой процедуры.
Постоянный canary сохраняет проверку реальной таблицы без FakeTable.

Extract читает только Northwind во temporary tree с ExtractTarget=SchemaObjectType,
ExtractAllTableData=False, ExtractReferencedServerScopedElements=False,
SourceEncryptConnection=True и SourceTrustServerCertificate=True. Security,
Users, Roles, Permissions и эквивалентные каталоги удаляются целиком.
Residual CREATE USER, ALTER ROLE, GRANT, INSERT, unsafe file types или mismatch
13 таблиц / 16 представлений / 7 процедур дают отказ, сохраняя old Imported.
Полные 36 отдельных SQL файлов заменяют непустое дерево атомарным macOS exchange.

## Команды ролей

Все проектные действия — через make из корня; scripts/sql.py использует stdlib.

| Команда | Назначение | Роль / режим |
| --- | --- | --- |
| `make setup` | Local dependency restore/install | Coder, сеть, один раз |
| `make db-extract` | Readonly schema Extract из Northwind | Coder, live |
| `make db-build` | Сборка двух SQL projects, no-restore | Coder/Reviewer, offline |
| `make lint` | SQLFluff только Authored и tests | Coder/Reviewer, offline |
| `make test` | Pinned source и synthetic unittest fixtures; выбранный `PLANVEYOR_RUNTIME_ROOT` обязателен, без SQL/config/cache | Coder/Reviewer, offline |
| `make check-secrets` | Git-known/untracked nonignored и JUnit scan | Coder/Reviewer, offline |
| `make db-proof JUNIT=<relative.xml>` | Build, fresh guard, Publish, RunAll, JUnit | Coder, затем Reviewer, live |
| `make db-state` | Schema/object/class/last-result readback | Architect/Reviewer, readonly live |

Publish непосредственно предшествует один свежий guard-query: DB_NAME равен
настройке, marker EXISTS без чтения значения, IS_SRVROLEMEMBER(sysadmin)=0.
Northwind case/padding variants не допускаются как цель. Отказ — rc 3 и ноль
Publish. Та же конфигурация удерживается до formatter. Publish использует
IncludeCompositeObjects=True, DropObjectsNotInSource=True,
ExcludeObjectTypes=Users;Logins;RoleMembership;Permissions,
DropExtendedPropertiesNotInSource=False, ScriptDatabaseOptions=False,
BlockOnPossibleDataLoss=True, TargetEncryptConnection=True и
TargetTrustServerCertificate=True. Marker сохраняется.

RunAll вызывается без параметров, затем XmlResultFormatter; постоянный formatter
не меняется. go-sqlcmd использует --encrypt-connection=mandatory -C -b; XML
читается с -h -1 -y 0 -w 65535. Таймауты ограничены: setup 600 s,
Extract/build/lint/Publish 300 s, guard/formatter/db-state 60 s, RunAll 120 s.
SQL и Publish автоматически не повторяются.

## Proof и отказы

JUNIT обязателен: относительный .xml внутри проекта, без symlink leaf/ancestors.
Tracked path или неизвестный Git — отказ до удаления/setup/build/SQL. Только
достоверно untracked old XML удаляется до сборки. Strict parse отвергает
malformed/truncated/DTD/entity/duplicate documents, missing/unknown/duplicate testcase,
несогласованные suite/classname и suite/root счётчики. Известные tSQLt bracketed
имена нормализуются только по точному разрешённому составу; порядок suites/cases
не является идентичностью. Очищенный XML атомарно записывается; failure/error/skipped сохраняют
красный verdict. Старый XML, успешное сообщение и synthetic test не заменяют live proof.

Coder и Reviewer последовательно создают разные JUnit в
`docs/code_reviews/assets/<plan-stem>/`: `<name>.junit.xml` и
`<name>.review.junit.xml`. Каждый текущий отчёт содержит полный точный набор
согласованного плана и обязательный real canary. Для текущей процедуры это
восемь `GetReorderCandidatesTests` и один `StackAdaptationTests`:
tests=9/failures=0/errors=0/skipped=0. Девять уникальных известных identities
обязательны; зелёные totals при red testcase не принимаются. Исторические
1/0/0/0 относятся только к завершению адаптации. До/после proof нужны HEAD и
canonical bundle_sha256 штатного Planveyor snapshot, relative JUnit path/SHA-256,
command и отдельные make/wrapper rc. Изменение target bytes требует нового proof.
`db-state` показывает безопасные counts/Products-U/last-results, явные empty и
not-tested; catalog strings используют COLLATE DATABASE_DEFAULT. Readback не
объявляет canary success и не заменяет independent JUnit.

| Код обвязки | Категория |
| --- | --- |
| 0 | Success |
| 1 | Test/JUnit failure или malformed report |
| 2 | Configuration/path/Git/secrets/invalid Extract input |
| 3 | Dev target rejected, no Publish |
| 4 | Connection/read SQL failure |
| 5 | Build/lint/Extract artifact or atomic exchange failure |
| 6 | Publish failure |

Make может вернуть собственный nonzero; wrapper печатает только безопасные
phase/category/rc/reason. Credentials, private paths и SQL streams в evidence
не сохраняются. `check-secrets` не читает .git, .tmp или .env.local и не печатает
найденные значения. Missing prerequisites закрывают через owning role, без
изменения сервера/прав и без неявного альтернативного инструмента.

Автоматический commit запрещён. В ручном режиме в консоли (`human_explicit`)
commit выполняет только `close --commit` с явного разрешения человека на
показанный набор; close preview такого разрешения не даёт. В режиме TUI
(`planveyor sibling tui`) семантический commit и, если он нужен, commit закрытия
документов делает Architect в окне Manager (`native_existing`), только по прямому
разрешению Owner для конкретного плана. Каждый запрос записи в `.git` одобряется
разово; постоянных разрешений нет.
CI, другие ОС/версии SQL Server, внешние модели/MCP, push и публикация вне объёма.
Новые бизнес-задачи выполняются по отдельному прямому поручению после sibling ready.

## Лицензия

Репозиторий распространяется по лицензии Apache-2.0, см. [LICENSE](LICENSE).
Схема Northwind в `sql/Northwind/Imported/` взята из примеров Microsoft SQL Server
и распространяется по лицензии MIT, см.
[third_party/northwind/LICENSE.txt](third_party/northwind/LICENSE.txt). Указания
авторства, в том числе для стороннего кода, — в [NOTICE](NOTICE).

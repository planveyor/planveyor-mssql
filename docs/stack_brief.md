# Анкета стека: SQL Server 2019 / Northwind

Анкета фиксирует 12 согласованных вводных Owner.
Это входная запись адаптации, а не доказательство готовности среды. После адаптации
постоянные правила живут в локальных секциях восьми файлов из `docs/README.md`
и в корневом `README.md`; анкету не правят без нового плана изменения стека.
Значения подключения, адреса серверов и личные пути сюда не записываются.

## 1. Назначение и готовность стека

**Ответ:** Sibling ведёт схему Northwind на SQL Server 2019, compatibility 150.
Адаптация готовит SQL-проекты, обвязку за целями `make`, офлайн-проверки и постоянные правила ролей.
Наблюдаемый итог — реальная `dbo.Products` типа `U` в назначенной dev-базе и один
постоянный canary `StackAdaptationTests.[test Products table exists]` без `FakeTable` и `NewTestClass`.
Coder и Reviewer получают каждый свой свежий JUnit последовательными независимыми прогонами.
`GetReorderCandidates` — отдельное прямое поручение после адаптации и `sibling ready`.
Реальные findings проходят штатный capture; отсутствие findings допустимо.

## 2. Стек и версии

**Ответ:**

| Инструмент | Принятое ограничение | Закрепление |
| --- | --- | --- |
| Платформа | macOS | Постоянные правила и корневой `README.md` |
| SQL Server | 2019, compatibility 150 | `Sql150DatabaseSchemaProvider` в SQL-проектах |
| Python | Уже установленный 3.12, первым в `PATH`; новый не устанавливается | Выбор проектного интерпретатора в обвязке; `PYBIN` движка сюда не переносится |
| .NET SDK | 10.0.401, `rollForward: latestFeature` | `global.json` |
| go-sqlcmd | Уже установленный инструмент; `--encrypt-connection=mandatory -C -b` | Версию существующего инструмента фиксирует Coder в доказательстве; установка/обновление вне объёма |
| SqlPackage | 170.5.96, локальный dotnet tool | `.config/dotnet-tools.json`; кэш `.tmp/` |
| Microsoft.Build.Sql | 2.3.0 | SQL-проекты |
| tSQLt.Dacpacs | 1.0.8083.3529, `DacpacName=tSQLt.2019` | Тестовый SQL-проект |
| SQLFluff | 3.4.2, `tsql`, `raw`, длина 120 | `requirements-dev.txt`, `.sqlfluff` |

Версии пакетов не обновляются автоматически. Объявленный `rollForward` SDK сохраняется.
Другие версии SQL Server и их возможности в этот план не входят.

## 3. Среда разработчика

**Ответ:** macOS, Python 3.12, .NET SDK и go-sqlcmd уже подготовлены Owner.
`make setup` один раз с сетью готовит локальный SqlPackage, зависимости SQL-проектов
и SQLFluff; инструменты, окружения и кэши располагаются в `.tmp/`.
Supporting .NET files используют `.tmp/dotnet-home`, NuGet packages/cache — `.tmp/nuget/`,
Python venv/cache — `.tmp/venv/` и `.tmp/pip-cache/`. `NuGet.Config` закрепляет local packages,
`Directory.Build.props` разделяет obj/bin проектов в `.tmp/build/`.
После этого `make db-build`, `make lint`, `make test`, `make check-secrets` работают офлайн.
Системные инструменты, `HOME`, `PATH`, настройки сети и Codex автоматически не меняются.
Обвязка `scripts/sql.py` использует только стандартную библиотеку Python.

## 4. Живая цель

**Ответ:** `Northwind` — источник только схемы, только чтение. Публикация и tSQLt
выполняются в отдельной dev-базе, исходно пустой и подготовленной администратором.
Сервер, базы, логин, CLR и маркер `planveyor.designated_dev` роли не создают и не меняют.
Обвязка непосредственно перед Publish одним свежим запросом подтверждает совпадение
имени текущей базы с настройкой, наличие маркера без чтения его значения и отсутствие
`sysadmin` у логина. Отказ — код обвязки 3 и отсутствие публикации.
Наличие конфигурации само по себе не разрешает запись; успешный прошлый прогон
не заменяет свежую проверку. Сведения о сервере не попадают в вывод и доказательства.

## 5. Секреты и конфигурация

**Ответ:** Owner уже положил `.env.local` в корень: права 0600, файл игнорируется
Git и не отслеживается. Ключи: `SQLCMDSERVER`, `SQLCMDDBNAME`, `SQLCMDUSER`, `SQLCMDPASSWORD`.
Значения читает только обвязка; роли не открывают файл. Пароль sqlcmd передаётся
только переменной окружения. Передача пароля SqlPackage аргументом принята Owner
для однопользовательского Mac. Вывод, ошибки, таймауты и JUnit очищаются от hostname
и любых сведений о сервере; значения конфигурации не записываются в документы.

## 6. Команды

**Ответ:** Все проектные действия ролей выполняются объявленными целями `make`.
Прямые SQL-команды и абсолютные пути к интерпретатору в документах не используются.

| Цель | Что делает | Офлайн / сеть / живая | Кто запускает | Ожидаемый результат |
| --- | --- | --- | --- | --- |
| `setup` | Готовит зависимости в `.tmp/` | Сеть, один раз | Coder | Код обвязки 0 |
| `db-extract` | Извлекает только схему Northwind, проверяет и заменяет `Imported/` | Живая, только чтение | Coder | 36 SQL-файлов: 13 таблиц, 16 представлений, 7 процедур |
| `db-build` | Собирает основной и тестовый SQL-проекты | Офлайн после setup | Coder, Reviewer | Код обвязки 0 |
| `lint` | Проверяет `Authored/` и тесты SQLFluff | Офлайн | Coder, Reviewer | Код обвязки 0 |
| `test` | Выполняет `scripts/test_sql.py` | Офлайн | Coder, Reviewer | Код обвязки 0 |
| `check-secrets` | Проверяет отсутствие секретов в файлах репозитория | Офлайн | Coder, Reviewer | Код обвязки 0, без раскрытия значений |
| `db-proof JUNIT=<relative.xml>` | Сборка, проверка цели, Publish, RunAll и JUnit | Живая, запись только в проверенную dev-базу | Coder, затем независимо Reviewer | Свежий JUnit: tests=1, failures=0, errors=0, skipped=0 |
| `db-state` | Схемы, объекты, классы tSQLt, последние результаты | Живая, только чтение | Architect, Reviewer | Явный пустой отчёт на пустой базе; строковые выражения с `COLLATE DATABASE_DEFAULT` |

**Коды выхода обвязки:** 0 — успех; 1 — тесты; 2 — конфигурация;
3 — проверка цели; 4 — подключение; 5 — сборка или lint; 6 — публикация.
В доказательстве отдельно записываются фактический код `make` и код обвязки.

## 7. Доказательство для ревью

**Ответ:** После `EXEC tSQLt.RunAll;` без параметров выполняется
`EXEC tSQLt.XmlResultFormatter;`; постоянный formatter не меняется.
XML читается через sqlcmd с `-h -1 -y 0 -w 65535` и разбирается строго.
JUnit хранится в `docs/code_reviews/assets/<plan-stem>/`: Coder использует
`<name>.junit.xml`, Reviewer — собственный `<name>.review.junit.xml`.
Должен быть ровно один testcase указанного canary, без failures/errors/skipped.

`JUNIT` обязателен: относительный путь `.xml` внутри проекта, без symlink и выхода
из корня. Если путь отслеживается Git или ответ Git неизвестен, обвязка отказывает
до удаления, настройки, сборки и SQL. Только достоверно неотслеживаемый старый XML
удаляется до сборки; новый XML записывается атомарно.
Git проверяет буквальное имя JUNIT, а не pathspec. Ambient `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_COMMON_DIR`, `GIT_INDEX_FILE`, включая пустые значения, дают operational-red
отказ 2 до JUNIT/config/deletion/build/SQL, без переключения index или изменения окружения.
Каждая роль фиксирует команду, коды `make`/обвязки, `HEAD`, `bundle_sha256`,
относительный путь и SHA-256 JUnit, счётчики и имена testcase.
Текст успеха и старый XML не заменяют текущий отчёт того же прогона.
JUnit — постоянное доказательство ревью; `.tmp/` — локальные временные материалы.

## 8. Правила для ролей

**Ответ:** Coder переносит подтверждённые ограничения в локальные секции восьми
файлов матрицы `docs/README.md` и в корневой `README.md`. Общие lifecycle/authority
и статусные блоки не меняются; правила не зависят от имени текущего плана.

### Architect

**Ответ:** Различает схему-источник Northwind и назначенную dev-базу; сервер,
логины, CLR, маркер и production вне объёма ролей. Приёмка опирается на офлайн-проверки
и независимые JUnit Coder/Reviewer, а не на вводные Owner или наличие обвязки.
Из живых целей запускает только `make db-state` после реализации обвязки.

### Planner

**Ответ:** Формирует точные targets, версии/manifest и code draft в своей стадии.
Проверки и доказательства задаёт целями `make`; отдельно называет офлайн-тесты
отказов и реальный SQL-canary. Canary не использует `FakeTable`/`NewTestClass`
и не читает бизнес-данные. Для Coder и Reviewer предусмотрены разные JUnit и последовательность.

### Coder

**Ответ:** `sql/Northwind/Imported/` — только результат Extract, руками не правится;
авторский SQL — `sql/Northwind/Authored/`, тесты — `sql/tests/<Class>/`.
Основной проект — `sql/Northwind/Northwind.sqlproj`; тестовый —
`sql/tests/Northwind.Tests.sqlproj`, с ProjectReference на основной и tSQLt.Dacpacs.
Extract выполняется во временный каталог с `ExtractTarget=SchemaObjectType`,
`ExtractAllTableData=False`, `ExtractReferencedServerScopedElements=False`,
`SourceEncryptConnection=True`, `SourceTrustServerCertificate=True`.
Каталоги безопасности (`Security`, `Users`, `Roles`, `Permissions` и аналогичные)
удаляются целиком. Оставшиеся `CREATE USER`, `ALTER ROLE`, `GRANT`, `INSERT`
означают отказ с сохранением прежнего Imported. Проверенный Imported заменяется атомарно.
Одночастные имена допустимы; собственный разбор имён и объединение Imported запрещены.

Publish использует `IncludeCompositeObjects=True`, `DropObjectsNotInSource=True`,
`ExcludeObjectTypes=Users;Logins;RoleMembership;Permissions`,
`DropExtendedPropertiesNotInSource=False`, `ScriptDatabaseOptions=False`,
`BlockOnPossibleDataLoss=True`, `TargetEncryptConnection=True`,
`TargetTrustServerCertificate=True`; маркер сохраняется.
Проверки цели/JUNIT и очистку вывода не ослабляет; formatter временно не переключает.

### Reviewer

**Ответ:** Независимо проверяет текущий bundle офлайн, выполняет `make db-state`
и собственный `make db-proof` с другим JUnit. Проверяет реальные `dbo.Products`
типа `U`, ровно один testcase, счётчики, SHA-256 и связь с проверенными байтами.
Проверяет сохранение маркера, отказы без публикации, старый XML, Git/symlink-границы,
таймауты, строгий XML и очистку ошибок/вывода/JUnit.
В доказательстве нет пароля, адреса сервера и абсолютных путей.

## 9. Кто запускает живые цели

**Ответ:** Выбран вариант А: штатные роли в песочнице Codex с уже включённой сетью.
`make setup` и `make db-extract` — Coder; `make db-proof` — Coder и затем независимо
Reviewer, каждый со своим JUnit; `make db-state` — Architect и Reviewer.
Общая dev-база требует последовательных прогонов. Смена сетевого режима,
настроек Codex или переход к варианту Б автоматически не допускаются.
Заявленная готовность среды подтверждается только будущими фактическими проверками.

## 10. Вне объёма

**Ответ:** CI; другие ОС и версии SQL Server; production и бизнес-данные;
подготовка сервера, баз, логинов, CLR и маркера; правка движка Planveyor/Genesis;
изменения `HOME`, trust, сети и моделей; внешние модели и MCP; push и публикация
репозитория. SQL Publish в назначенную проверенную dev-базу входит в адаптацию.
Reset/init/env-copy/model-install не повторяются. Автоматический commit запрещён;
close preview не разрешает `close --commit`.
`GetReorderCandidates` согласуется отдельным поручением после `sibling ready`.

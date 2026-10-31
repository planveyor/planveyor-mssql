# SQL Server: от пустого sibling до двух закрытых планов

Руководство повторяет проход 11–12 октября 2026 года: адаптация sibling под
SQL Server 2019 и Northwind, затем процедура `dbo.GetReorderCandidates`. Оба
плана прошли в ручном режиме в консоли. 28–29 октября sibling обновили на новую
версию Planveyor, и план обновления прошёл в режиме TUI, в одном окне Manager
(раздел 10). 30 октября четвёртый план вернул проверку общей части файлов
правил, которую потеряла правка теста при обновлении (раздел 12). В руководстве
собраны требования к серверу и к Codex, порядок команд в обоих режимах, ответы
на вопросы ролей и признаки завершения каждого шага. Обычный процесс sibling
описан в [docs/README.md](../README.md), обвязка SQL и её коды — в корневом
[README.md](../../README.md).

`docs/README.md` ссылается на руководства движка по путям английских файлов.
Русская версия каждого лежит рядом, в файле с суффиксом `.ru.md`, и в начале
английской страницы на неё ведёт ссылка «Русский». Это руководство сразу
называет русские файлы.

## Что вы хотите сделать

**Повторить демонстрацию с нуля.** Создайте новый пустой sibling и пройдите
разделы 2–9 по порядку на отдельно подготовленной dev-базе. В этом репозитории
init, адаптацию и живые прогоны не повторяют: его планы уже закрыты, а
обвязка ждёт девять тестов второго плана.

**Продолжить работу в этом репозитории.** Клон `planveyor-mssql` уже прошёл оба
плана, обновление движка и четвёртый план. Сначала выберите версию движка, на
которой он закреплён: порядок описан в разделе «Вернуться к работе в существующем sibling»
руководства движка `"$PLANVEYOR_RUNTIME_ROOT/docs/guides/stack-sibling.ru.md"`.
Затем подготовьте сервер (раздел 3), `.env.local` и Codex (разделы 4 и 5, без
`init`) и начните новую задачу запросом скиллу, как в разделе 9.

## 1. Кто выполняет команды

Команды и ответы одни и те же, кто бы ни выполнял команды — вы сами или агент.
Это не режимы Planveyor: режим TUI или ручной режим в консоли выбирают отдельно
(раздел 7).

### Сам в терминале

Каждую команду `planveyor` вы выполняете в своём терминале и сами отвечаете
ролям. Чат Codex в каталоге sibling нужен только для сообщений скиллу
`$planveyor-plan-draft`. Ответ роли удобно передать блоком `<<'EOF'` … `EOF`
(раздел 6) или из файла через `<`. Можно ввести текст и прямо в `answer`,
закончив ввод клавишами Ctrl-D.
Работающий `run` останавливают клавишами Ctrl-C в его терминале (раздел 7). В
режиме TUI вы отвечаете Manager в его окне и там же одобряете запросы ролей.

### Поручаю агенту

Команды по одной выполняет агент Codex в чате, открытом в каталоге sibling. Он
читает вывод, выполняет напечатанный следующий шаг и отвечает ролям текстами из
[приложения А](#приложение-а-банк-ответов), если текст совпадает с вопросом и
постановкой. Каждый такой ответ агент начинает словами «Отвечаю по поручению
Owner». Остальные вопросы он возвращает вам. Их список приведён в разделе
«Типовые вопросы Architect» руководства движка
`"$PLANVEYOR_RUNTIME_ROOT/docs/guides/stack-sibling.ru.md"`.

Модель чата агента выбираете вы. На модели ролей она не влияет: в проходе чат
работал на другой модели, и все роли всё равно шли на `gpt-6.1-sol` / `ultra`.

Поручение агенту может выглядеть так:

```text
Проведите проход по руководству <каталог клона planveyor-mssql>/docs/tools/mssql_walkthrough.md как агент из раздела 1, начиная с раздела <номер>. Значения переменных раздела 2: PY312_BIN=<…>, PLANVEYOR_RUNTIME_ROOT=<…>, PASS_DIR=<…>. Команды planveyor выполняйте по одной в окружении из раздела 2 и после каждой выполняйте напечатанный следующий шаг. Перед каждым run и перед окном Manager выводите мне раздел «Как я понял задачу» плана. На вопросы ролей отвечайте текстами приложения А, только если текст совпадает с вопросом и постановкой. Вопрос вне приложения, расхождение с постановкой и каждую остановку из раздела 11 передавайте мне. Сервер, .env.local, Codex home, модели и доверие к папке не меняйте.
```

Руководство берите из клона этого репозитория: в новый sibling `init` его не
кладёт. Запросы скиллу в разделах 6 и 9 агент отправляет в этом же чате.

Режим работы с планом агент выбирает по разделу «Если проход ведёт агент»
руководства движка. Режим TUI подходит, если агент может всё время работы над
планом держать окно Manager открытым, читать его и вводить в него текст; иначе —
ручной режим в консоли. В обновлении 28–29 октября окном управлял агент Codex
через мультиплексор терминала.

### Что делаете вы сами

Кто бы ни выполнял команды и в каком бы режиме ни шёл план, за вами остаются:

- сервер: его готовит администратор, требования — в разделе 3;
- файл `.env.local` со значениями подключения; значения в чат не передаются;
- Codex home, конфигурация моделей и решение, доверять ли папке sibling
  (раздел 4);
- ответы на вопросы, которых нет в приложении А, и на вопросы о границах задачи,
  правах и приёмке;
- коммиты: в ручном режиме — разрешение каждого `close --commit` после
  просмотра набора; в режиме TUI — прямое разрешение для этого плана, чтобы
  Architect коммитил в окне. Каждый его запрос на запись в `.git` одобряете вы
  или агент, который ведёт окно, разово и только в пределах этого разрешения;
- решение, продолжать ли план после остановки `run` или закрытия окна Manager.

Push и публикация в это руководство не входят.

### Разрешения и песочница агента

Если команды выполняет агент, пишите разрешение прямо в чате до нужного действия.
Автоматическая проверка действий Codex в проходе отклонила сброс dev-базы и
копирование `.env.local`. Оба действия прошли после прямого ответа владельца в
чате.

В ручном режиме разрешайте каждый коммит отдельно, после просмотра его набора:
доставленный `AGENTS.md` требует явного разрешения человека на конкретный
показанный набор. В проходе 11–12 октября, на прежней версии движка, владелец
после первого просмотра одной фразой разрешил все локальные коммиты прохода; по
нынешнему `AGENTS.md` такое общее разрешение не подходит. Разрешение пишете вы
сами. Если после просмотра набор изменился, сначала нужен новый просмотр.

В режиме TUI Owner разрешает Architect коммитить для конкретного плана (раздел 7).
Каждый запрос записи в `.git` одобряете в окне вы или агент, который ведёт окно,
разово и только в пределах этого разрешения.

Песочница чата задаётся папкой, в которой чат открыт, и `cd` её не расширяет.
Поэтому до init откройте чат в `PASS_DIR`, после init — новый чат в
`SIBLING_DIR`. Команды `architect`, `run` и окно Manager запускают роли Codex,
а роли пишут свои сессии в Codex home вне sibling. Команды `init` и
`close --commit` пишут в `.git`. Песочница может защищать `.git`, `.agents` и
`.codex`. В проходе агент сразу запускал `architect` и `run` с повышенным
доступом. В обновлении `planveyor_manager_resume` и `sibling tui` агент вводил в
отдельный терминал через мультиплексор. Для остальных команд
повышенный доступ допустим, только если отказ доступа доказан на конкретной
операции и само действие уже разрешено. Код возврата 3 сам по себе отказом
доступа не считается.

## 2. Предпосылки на Mac

Нужны macOS, Git, zsh, rg, подготовленное окружение Python 3.12 с Copier и
PyYAML, .NET SDK 10, go-sqlcmd и авторизованный Codex CLI. Движок — обычный клон
Planveyor без незакоммиченных изменений, путь к нему не идёт через символические
ссылки. Как подготовить окружение и проверить установку, описано в руководстве
«Установка Planveyor», `docs/guides/install.ru.md` в клоне движка. Клон переключите
на версию, на которой закреплён этот репозиторий: она записана в поле
`source_commit` файла `docs/_meta/planveyor_contract_authority.v1.json`.

```sh
git clone https://github.com/planveyor/planveyor.git '<каталог копии Planveyor>'
git -C '<каталог копии Planveyor>' switch --detach '<версия из source_commit>'
```

Проход 11–12 октября шёл на коммите `8c5256e752cedafb4aa3c06cec97bef29d74f947`,
за проход движок не менялся. Обновление 28–29 октября перевело sibling на
`66050258bcb5cf6a86fc539b6e28b39d77941841` (раздел 10). Повтор на другой версии
требует проверки её собственного контракта.

Перед публикацией коммиты документации Planveyor объединили в один, поэтому
коммита `66050258bcb5cf6a86fc539b6e28b39d77941841` в публичной истории Planveyor
нет. Его заменил коммит `ff0a16bd3b9d035f4532c5f7d768a52e5914c59a` с тем же
деревом файлов: код и шаблон движка не изменились. Sibling перевели на
`ff0a16bd3b9d035f4532c5f7d768a52e5914c59a` отдельным коммитом. В нём изменились
только поле `_commit` в `.copier-answers.yml` и поле `source_commit` в
`docs/_meta/planveyor_contract_authority.v1.json`; ещё в руководство добавлены
это пояснение и отсылка к нему в разделе 10. В планах, отчётах ролей и в
описании обновления в этом руководстве остаётся `66050258`: на этом коммите
работали роли.

| Компонент | Версия в проходе 11–12 октября |
| --- | --- |
| macOS | 27.0.1; другие ОС этим проходом не проверены |
| Python / Copier / PyYAML | 3.12.14 / 9.18.2 / 6.0.3 |
| .NET SDK | 10.0.401; в проекте `rollForward: latestFeature` |
| go-sqlcmd / Codex CLI | 1.10.0 / 0.162.0 |
| SqlPackage | 170.5.96, локальный dotnet tool |
| Microsoft.Build.Sql | 2.3.0, `Sql150DatabaseSchemaProvider` |
| tSQLt.Dacpacs | 1.0.8083.3529, `DacpacName` tSQLt.2019 |
| SQLFluff | 3.4.2, tsql/raw, длина 120 |
| Manager и роли | `gpt-6.1-sol`, уровень `ultra` (раздел 4) |

В обновлении 28–29 октября стояли Python 3.12.14, Copier 9.18.2, .NET SDK
10.0.403, go-sqlcmd 1.10.0 и Codex CLI 0.165.0; Manager и роли тоже шли на
`gpt-6.1-sol` / `ultra`.

Работать удобно в двух вкладках терминала: в одной идёт чат Codex, в другой вы
выполняете команды. В каждой новой вкладке сначала задайте окружение. Значения в
угловых скобках замените своими полными путями: `~` в одинарных кавычках не
раскрывается. Пути и учётные данные остаются у вас, в планы, правила и отчёты их
не записывают.

```sh
PY312_BIN='<каталог bin подготовленного Python 3.12>'
PLANVEYOR_RUNTIME_ROOT='<каталог копии Planveyor>'
PASS_DIR='<новый каталог для sibling>'
SIBLING_DIR="$PASS_DIR/planveyor-mssql"
unset PLANVEYOR_CODEX_HOME
export PATH="$PY312_BIN:$PLANVEYOR_RUNTIME_ROOT/bin:$PATH"
```

Эти строки меняют только текущую вкладку и не трогают настройки оболочки и
установленный движок. Без `PLANVEYOR_CODEX_HOME` роли работают в обычном
`~/.codex`, как в проходе (раздел 4). Все команды `planveyor` ниже рассчитаны на
такую вкладку. Если команды выполняет агент, значения переменных вы передаёте ему
в поручении (раздел 1).

Один раз создайте каталог прохода и проверьте, что путь к нему не идёт через
символические ссылки:

```sh
mkdir -p "$PASS_DIR"
[ "$(cd "$PASS_DIR" && pwd -P)" = "$PASS_DIR" ] && echo 'путь без symlink'
```

Init требует, чтобы родитель нового каталога уже существовал. Последняя строка
печатает подтверждение, только если путь совпал с физическим. Если она ничего не
напечатала, выберите каталог без символических ссылок: на Mac, например, `/tmp`
ведёт в `/private/tmp`.

Чат Codex для скилла и для агента открывайте во вкладке с этим окружением,
после init — в корне sibling (раздел 5):

```sh
cd "$SIBLING_DIR"
env -u CODEX_HOME codex
```

Так скилл видит команду `planveyor`, а решение о доверии к папке Codex сохранит в
том же `~/.codex`, из которого запускаются роли. Чат агента до init открывают так
же, только в `PASS_DIR`: `cd "$PASS_DIR"`.

До первой команды в каждом новом терминале или чате проверьте версии и
окружение. Эти проверки ничего не устанавливают:

```sh
"$PY312_BIN/python3" --version
"$PY312_BIN/python3" -m copier --version
dotnet --list-sdks
sqlcmd --version
codex --version
codex login status
zsh -lc 'python3 --version'
[ -n "$TMPDIR" ] && [ -d "$TMPDIR" ] && echo 'TMPDIR на месте'
git -C "$TMPDIR" rev-parse --is-inside-work-tree
```

Особого внимания требуют две проверки.

- Команда `zsh -lc 'python3 --version'` должна напечатать Python 3.12. Роли
  запускают команды в login shell, а `Makefile` sibling вызывает голый `python3`. В
  проходе login shell ролей нашёл Python 3.14.8, и обвязка отказала с кодом 2
  (`reason=python-or-platform`). Сам Planveyor передаёт ролям свой интерпретатор
  через `PYBIN`, поэтому его это не задело. Строка `export PATH` из этого раздела
  действует только на вкладку и не доказывает, какой Python найдёт login shell
  ролей, поэтому эту проверку выполняют отдельно. Как поставить Python 3.12 первым
  и в login shell, решаете вы, например порядком `PATH` в `~/.zprofile`. В
  проходе роли обошли отказ сами, запуская команды без login shell; на это не
  рассчитывайте. В обновлении 28–29 октября login shell ролей нашёл Python
  3.15.2, и роли запускали `make` с временным префиксом `PATH` к Python 3.12.
  Владелец принял это задним числом и только для того прохода.
- `TMPDIR` должен существовать и лежать вне любого Git-репозитория. Последняя
  команда должна отказать с `fatal: not a git repository`. Отсутствующий каталог
  не подходит.

## 3. Сервер SQL Server

Сервер, базы, логин, CLR и маркер готовит администратор; роли их не создают и не
меняют. В `init` Planveyor это не входит: настройка относится к конкретному
стеку, и ниже даны рекомендации. В проходе сервер готовил отдельный набор
административных скриптов владельца стенда. Это одна из возможных реализаций, в
sibling он не входит.

### Что нужно на сервере

- SQL Server 2019 (основная версия 15) с проверкой подлинности SQL Server:
  обвязка входит логином и паролем.
- Уровень совместимости 150 у обеих баз. Код sibling пишется под SQL Server
  2019: проекты собираются с `Sql150DatabaseSchemaProvider`, возможности SQL
  Server 2022 и новее запрещены.
- CLR и подготовка сервера для tSQLt. Администратор с правами sysadmin один раз
  выполняет `PrepareServer.sql` из дистрибутива tSQLt 1.0.8083.3529. Скрипт
  включает `clr enabled` и ставит ключ подписи tSQLt (логин `tSQLtAssemblyKey`),
  `clr strict security` остаётся включённым. После этого tSQLt ставится в
  dev-базу от имени рабочего логина, без sysadmin и без `TRUSTWORTHY`.
- База с именем ровно `Northwind` на том же сервере: обвязка читает схему по
  этому имени. Источник — скрипт Microsoft `instnwnd.sql` из репозитория
  `microsoft/sql-server-samples`. В базе ровно 13 пользовательских таблиц,
  16 представлений и 7 хранимых процедур. При каждом Extract обвязка сверяет этот
  состав и отказывает с кодом 2 при другом числе файлов или файлах другой
  категории; прежний `Imported/` при этом остаётся. Демо-данные обвязке не нужны:
  Extract берёт только схему.
- Отдельная пустая dev-база, без пользовательских объектов и классов tSQLt.
  Остатки прошлых прогонов порождают ложные вопросы ролей; в одном из прошлых
  проходов они дали лишний набор тестов в `RunAll`. Перед каждым новым проходом
  администратор пересоздаёт dev-базу пустой.
- Маркер dev-базы — расширенное свойство уровня базы `planveyor.designated_dev`.
  Обвязка проверяет только его наличие и значение не читает. Без маркера
  публикация не начинается (код 3).
- Шифрованное соединение. sqlcmd и SqlPackage подключаются с шифрованием и
  доверяют сертификату сервера (`-C`, `TrustServerCertificate=True`), поэтому
  подходит и самоподписанный сертификат.
- Сеть с Mac до порта сервера, в том числе из песочницы ролей (раздел 4).
- Рабочий логин SQL Server без прав sysadmin. Логин с sysadmin обвязка
  отвергает перед каждой публикацией (код 3). Права логина приведены в таблице.

| База | Права рабочего логина |
| --- | --- |
| dev-база | пользователь базы, член `db_owner` |
| `Northwind` | пользователь базы, член `db_datareader`; `VIEW DEFINITION` на базу; `SELECT` на `sys.sql_expression_dependencies` |

Кроме того, у логина есть обычные права подключения: `CONNECT SQL` на сервере и
`CONNECT` в обеих базах. Писать в Northwind логин не может. В проходе у обеих баз была collation
`SQL_Latin1_General_CP1_CI_AS`. Права и маркер администратор выдавал так (`<…>` —
ваши имена; логин с паролем он создаёт заранее):

```sql
USE [<dev-база>];
CREATE USER [<пользователь>] FOR LOGIN [<логин>];
ALTER ROLE [db_owner] ADD MEMBER [<пользователь>];
EXEC sys.sp_addextendedproperty @name = N'planveyor.designated_dev', @value = N'<любая строка>';
GO
USE [Northwind];
CREATE USER [<пользователь>] FOR LOGIN [<логин>];
ALTER ROLE [db_datareader] ADD MEMBER [<пользователь>];
GRANT VIEW DEFINITION TO [<пользователь>];
GRANT SELECT ON sys.sql_expression_dependencies TO [<пользователь>];
GO
```

### Подключение

Параметры подключения лежат в `.env.local` в корне sibling, по строке
`КЛЮЧ=значение`. Нужны ровно четыре ключа: `SQLCMDSERVER`, `SQLCMDDBNAME`,
`SQLCMDUSER`, `SQLCMDPASSWORD`, каждый один раз и с непустым значением. Файл
обычный, без symlink, с правами 0600; Git его игнорирует и не отслеживает. В
`SQLCMDDBNAME` указывают dev-базу: имя `Northwind` обвязка отвергает с кодом 3.
Файл содержит данные, поэтому через `source` его не исполняют. Его читает только
обвязка; значения не попадают в чат, планы и отчёты.

### Проверка сервера только чтением

Перед каждым проходом администратор проверяет сервер запросами только на чтение.
Ожидаемые значения указаны в комментариях. Запрос к `sys.server_principals`
выполняет администратор: рабочему логину эти серверные метаданные не видны, и он
получит 0 при существующем ключе. Ноль пользовательских объектов ожидается только
в новой dev-базе до первой публикации: на стенде после прохода объекты есть.

```sql
-- 15, 0, 0
SELECT CAST(SERVERPROPERTY('ProductMajorVersion') AS int) AS major_version,
       CAST(SERVERPROPERTY('IsIntegratedSecurityOnly') AS int) AS windows_auth_only,
       IS_SRVROLEMEMBER(N'sysadmin', N'<логин>') AS login_is_sysadmin;
-- clr enabled = 1, clr strict security = 1
SELECT name, CAST(value_in_use AS int) AS value_in_use
FROM sys.configurations
WHERE name IN (N'clr enabled', N'clr strict security');
-- 1
SELECT COUNT(*) AS tsqlt_key_login
FROM sys.server_principals
WHERE name = N'tSQLtAssemblyKey';
-- 150 у обеих баз
SELECT name, compatibility_level
FROM sys.databases
WHERE name IN (N'Northwind', N'<dev-база>');
GO
USE [Northwind];
-- 13, 16, 7
SELECT (SELECT COUNT(*) FROM sys.tables) AS tables,
       (SELECT COUNT(*) FROM sys.views) AS views,
       (SELECT COUNT(*) FROM sys.procedures) AS procedures;
-- db_datareader
SELECT r.name AS role_name
FROM sys.database_role_members AS m
JOIN sys.database_principals AS r ON r.principal_id = m.role_principal_id
JOIN sys.database_principals AS u ON u.principal_id = m.member_principal_id
WHERE u.sid = SUSER_SID(N'<логин>');
-- CONNECT, VIEW DEFINITION, SELECT на sys.sql_expression_dependencies
SELECT p.state_desc, p.permission_name,
       OBJECT_SCHEMA_NAME(p.major_id) AS object_schema,
       OBJECT_NAME(p.major_id) AS object_name
FROM sys.database_permissions AS p
JOIN sys.database_principals AS u ON u.principal_id = p.grantee_principal_id
WHERE u.sid = SUSER_SID(N'<логин>');
GO
USE [<dev-база>];
-- 0 пользовательских объектов, маркер 1
SELECT (SELECT COUNT(*) FROM sys.objects WHERE is_ms_shipped = 0) AS user_objects,
       (SELECT COUNT(*) FROM sys.extended_properties
        WHERE class = 0 AND name = N'planveyor.designated_dev') AS marker;
-- db_owner
SELECT r.name AS role_name
FROM sys.database_role_members AS m
JOIN sys.database_principals AS r ON r.principal_id = m.role_principal_id
JOIN sys.database_principals AS u ON u.principal_id = m.member_principal_id
WHERE u.sid = SUSER_SID(N'<логин>');
GO
```

Расхождение исправляет администратор. Имя базы, маркер и отсутствие sysadmin
обвязка проверяет и сама: одним свежим запросом перед каждой публикацией.

## 4. Модели ролей и Codex home

Planveyor запускает роли через Codex CLI с Codex home из `PLANVEYOR_CODEX_HOME`,
а без этой переменной — из `~/.codex`. Настройки моделей Planveyor не создаёт и
не показывает, их задаёте вы. Полное описание — раздел «Настройка Codex» в
`"$PLANVEYOR_RUNTIME_ROOT/docs/guides/launch-and-role-modes.ru.md"`.

### Какие сессии запускаются

- `sibling architect` открывает сессию Architect на модели верхнего уровня
  `config.toml`.
- `sibling run` открывает главную сессию Manager на той же модели. В режиме TUI
  эту сессию заводит `planveyor_manager_init`, а `sibling tui` открывает её окно.
  Роли Manager поднимает субагентами Codex по `agent_type`: `architect`,
  `planner`, `coder`, `reviewer_code_risk`, `reviewer_code_contracts`.
- Роли могут поднимать встроенных субагентов `default`, `worker` и `explorer`.
  В проходе Architect несколько раз запускал `explorer`.
- Скилл `$planveyor-plan-draft` работает в вашем чате, на модели чата.

### Рекомендуемая настройка

Рекомендация движка — GPT-6.1 Sol (`gpt-6.1-sol`) с уровнем `ultra` или `max`, не
ниже `xhigh`, для Manager и всех ролей. Уровень задавайте явно: у `gpt-6.1-sol`
по умолчанию `low`. Верхний уровень `config.toml` задаёт главную сессию. Пять
ролей конвейера и три встроенных типа задаются записями `[agents.*]`:

```toml
model = "gpt-6.1-sol"
model_reasoning_effort = "ultra"

[agents]
enabled = true
max_concurrent_threads_per_session = 20

[agents.architect]
description = "Planveyor Architect"
config_file = "agents/architect.toml"

[agents.planner]
description = "Planveyor Planner"
config_file = "agents/planner.toml"

[agents.coder]
description = "Planveyor Coder"
config_file = "agents/coder.toml"

[agents.reviewer_code_risk]
description = "Planveyor Reviewer, risk lane"
config_file = "agents/reviewer_code_risk.toml"

[agents.reviewer_code_contracts]
description = "Planveyor Reviewer, contracts lane"
config_file = "agents/reviewer_code_contracts.toml"

[agents.default]
description = "Codex default agent"
config_file = "agents/default.toml"

[agents.worker]
description = "Codex worker agent"
config_file = "agents/worker.toml"

[agents.explorer]
description = "Codex explorer agent"
config_file = "agents/explorer.toml"
```

Файл `agents/architect.toml` лежит рядом с `config.toml`. Остальные семь файлов
такие же, со своими `name` и `description`:

```toml
name = "architect"
description = "Planveyor Architect"
model = "gpt-6.1-sol"
model_reasoning_effort = "ultra"
```

Движок требует `max_concurrent_threads_per_session` не меньше 6. Роли могут
поднимать своих субагентов, поэтому в примере, как и в проходе, стоит 20.

### Как это было в проходе

Все роли шли на `gpt-6.1-sol` / `ultra` через проектный `.codex/` в корне
sibling: `config.toml` и восемь файлов `agents/*.toml`. Общий `~/.codex` при этом
задавал Architect и обоим Reviewer другую модель. Проектный `.codex/` перекрыл её
только для этого sibling, а сеть и песочница ролей пришли из `~/.codex`. В
обновлении 28–29 октября проектный `.codex/` был тот же, и все шесть сессий,
Manager и пять ролей, шли на `gpt-6.1-sol` / `ultra`.

Файлы ролей в проходе были подробнее примера: служебные инструкции для субагентов
(`developer_instructions`), подробные сводки рассуждений и режим только чтения у
`explorer`. В пример они не входят: он задаёт только модели.

Каталог исключён из Git строкой `.codex/` в локальном файле исключений Git (`info/exclude`). Эта настройка
локальная и в коммиты не попадает. Init каталог `.codex/` не создаёт, его
кладёте вы (раздел 5).

Проектный `.codex/` Codex применяет только в доверенном проекте (trust). При
первом запуске Codex в новой папке он спрашивает «Trust this folder?» и
сохраняет ответ. В проходе владелец выбрал «Trust and continue».

### Требования к Codex home

- Вход выполнен: `codex login status` сообщает об этом.
- Сеть для варианта А, где живые цели `make` запускают сами роли. В `config.toml`
  выбранного Codex home нужны строки:

  ```toml
  [sandbox_workspace_write]
  network_access = true
  ```

  Сеть включаете вы, роли и агент её не включают. Код возврата 0 у такой команды
  означает, что из песочницы виден порт сервера. Вход в SQL и права она не
  проверяет:

  ```sh
  codex sandbox -c sandbox_mode=workspace-write -- /usr/bin/nc -z -G 3 '<адрес сервера>' '<порт>'
  ```

- Доверие к папке sibling, если модели заданы проектным `.codex/`.
- Память и глобальные правила. В проходе в `~/.codex` были включены память
  (`memories`) и глобальный `AGENTS.md`, и роли работали с ними. Такие настройки
  могут менять поведение ролей. Как вынести Planveyor в отдельный Codex home,
  описано в том же разделе руководства движка; этим проходом такой вариант не
  проверялся.

### Как проверить фактические модели

Имя роли модель не доказывает. Codex пишет каждую сессию файлом
`rollout-*.jsonl` в каталог `sessions/` своего Codex home. Запись `session_meta`
хранит каталог запуска, источник и роль субагента. Записи `turn_context` хранят
модель и уровень каждого хода. Это файлы самого Codex на вашей машине, другие
инструменты для проверки не нужны.

Перед первым `architect`, первым `run` и первым окном Manager отметьте время:

```sh
touch "$TMPDIR/planveyor-models.start"
```

Во время работы команды или после неё выполните из корня sibling:

```sh
python3 -I - "$(pwd -P)" "${PLANVEYOR_CODEX_HOME:-$HOME/.codex}/sessions" "$TMPDIR/planveyor-models.start" <<'PY'
import json, pathlib, sys
from datetime import datetime

project, sessions, marker = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
start = marker.stat().st_mtime
for path in sorted(sessions.rglob("rollout-*.jsonl")):
    if path.stat().st_mtime < start:
        continue
    meta, seen = None, set()
    with path.open(encoding="utf-8", errors="replace") as lines:
        for line in lines:
            try:
                item = json.loads(line)
            except ValueError:
                continue
            payload = item.get("payload") or {}
            if item.get("type") == "session_meta" and meta is None:
                meta = payload
            elif item.get("type") == "turn_context":
                try:
                    turn_time = datetime.fromisoformat(item.get("timestamp", "").replace("Z", "+00:00"))
                except (TypeError, ValueError, AttributeError):
                    continue
                if turn_time.tzinfo is not None and turn_time.timestamp() >= start:
                    seen.add(f"{payload.get('model')} / {payload.get('effort')}")
    if meta and meta.get("cwd") == project and seen:
        role = meta.get("agent_role") or ("main" if meta.get("source") == "exec" else "chat")
        print(role, ", ".join(sorted(seen)))
PY
```

Скрипт печатает по строке на сессию этого sibling: роль, модель и уровень.
Содержимое сессий он не выводит. Строка `main` — основная сессия `codex exec` в
этом проекте: в проходе это Architect в `sibling architect` и Manager в
`sibling run`. Сама метка не доказывает, что сессию запустил Planveyor. Роли и
встроенные субагенты названы по `agent_type`. Строка `chat` — ваш интерактивный чат в этой папке, у
него своя модель. Скрипт сам берёт `PLANVEYOR_CODEX_HOME`, если он задан, иначе `~/.codex`.

Если модель роли расходится с вашей настройкой, остановитесь. Вероятная причина:
Codex не применил проектную конфигурацию, например папка не доверена. Доверие и
модели меняете вы сами, обходной скрипт для этого не нужен.

Проверка нужна потому, что настройки из `~/.codex` действуют, даже если о них
забыли. В проходе общий Codex home задавал Architect и обоим Reviewer другую
модель. Без проектного `.codex/` и этой проверки роли работали бы на ней молча.

## 5. Создание sibling

```sh
planveyor sibling init "$SIBLING_DIR" \
  --author-name '<ваше имя>' --author-email '<ваш email>'
```

Ожидается код 0 и строки:

```text
Git identity: …
Sibling создан: …
Откройте его в рабочем чате и поручите $planveyor-plan-draft создать и выбрать план адаптации.
```

Init сам проверяет контракт и делает один начальный коммит. Проверьте это:

```sh
git -C "$SIBLING_DIR" rev-list --count HEAD
git -C "$SIBLING_DIR" status --short
```

Первая команда печатает 1, вторая ничего не печатает.

Положите `.env.local` в корень sibling сами. Можно скопировать файл, который
подготовил администратор, или создать заготовку с правами 0600 и вписать значения
в редакторе. Команда ниже ничего не перезаписывает, если файл уже есть:

```sh
cd "$SIBLING_DIR"
[ -e .env.local ] || (umask 077 && printf '%s\n' 'SQLCMDSERVER=<адрес сервера>,<порт>' 'SQLCMDDBNAME=<dev-база>' 'SQLCMDUSER=<логин>' 'SQLCMDPASSWORD=<пароль>' > .env.local)
```

Значения не выводите и в чат не передавайте. Затем проверьте файл:

```sh
chmod 600 "$SIBLING_DIR/.env.local"
stat -f '%HT %Lp' "$SIBLING_DIR/.env.local"
git -C "$SIBLING_DIR" check-ignore .env.local
git -C "$SIBLING_DIR" ls-files .env.local
```

Ожидается `Regular File 600`, затем `.env.local` (файл игнорируется), затем
пустой вывод (файл не отслеживается). Публичного примера значений здесь нет.

Если модели задаются проектным `.codex/`, создайте его одним блоком из корня
sibling. Блок пишет `config.toml` и восемь файлов `agents/*.toml` по примеру
раздела 4, исключает каталог из Git и ничего не трогает, если `.codex/` уже есть:

```sh
cd "$SIBLING_DIR"
if [ -e .codex ]; then
  echo 'Каталог .codex уже есть: проверьте его сами, файлы не созданы'
else
  mkdir -p .codex/agents
  printf '%s\n' 'model = "gpt-6.1-sol"' 'model_reasoning_effort = "ultra"' '' '[agents]' 'enabled = true' 'max_concurrent_threads_per_session = 20' > .codex/config.toml
  while IFS='|' read -r role description; do
    printf '\n[agents.%s]\ndescription = "%s"\nconfig_file = "agents/%s.toml"\n' "$role" "$description" "$role" >> .codex/config.toml
    printf 'name = "%s"\ndescription = "%s"\nmodel = "gpt-6.1-sol"\nmodel_reasoning_effort = "ultra"\n' "$role" "$description" > ".codex/agents/$role.toml"
  done <<'ROLES'
architect|Planveyor Architect
planner|Planveyor Planner
coder|Planveyor Coder
reviewer_code_risk|Planveyor Reviewer, risk lane
reviewer_code_contracts|Planveyor Reviewer, contracts lane
default|Codex default agent
worker|Codex worker agent
explorer|Codex explorer agent
ROLES
  printf '%s\n' '.codex/' >> "$(git rev-parse --git-path info/exclude)"
fi
git status --short
```

Последняя команда по-прежнему ничего не печатает. Создание `.codex/` общий Codex
config не меняет; сеть из раздела 4 вы включаете в нём отдельно. Откройте чат в
корне sibling командой из раздела 2 и на вопрос Codex о доверии к папке ответьте
«Trust and continue».

## 6. Первый план: адаптация стека

Скилл уже лежит в `.agents/skills/` sibling: Codex ищет навыки от папки чата к
корню репозитория. Если чат его не видит, проверьте, в какой папке открыт чат.
Глобальная копия, symlink и новый plugin не нужны.

Если хотите сами подтвердить раздел «Как я понял задачу» до перехода плана в
`Architect draft`, допишите в конец первой строки запроса: «До перевода плана в
Architect draft покажи мне раздел «Как я понял задачу» и дождись подтверждения».
Подробнее об этом — ниже в этом разделе.

Вставьте в чат весь блок ниже одним сообщением. Это сообщение скиллу, в терминале
его не выполняют. Перед отправкой сверьте с вашим сервером и средой пункты 1, 3,
5, 9 и 10. Это исходные факты стека, готовую анкету скилл и Architect составят
сами:

```text
$planveyor-plan-draft Создай и сделай текущим план адаптации sibling под мой стек по docs/_template_stack_brief.md. Создай docs/stack_brief.md как вход плана. Задай вопросы по неподтверждённым решениям. Следующую полезную задачу согласуем отдельно.

Факты о моём стеке:
1. Sibling ведёт код базы на SQL Server 2019 (compatibility 150) по схеме Northwind. Northwind — только источник схемы, только чтение. Публикация и тесты идут в отдельную пустую dev-базу с маркером назначенной dev-среды planveyor.designated_dev. Сервер, базы, логин и маркер готовит администратор; роли их не меняют.
2. Адаптация заканчивается одним постоянным тестом-canary: реальная таблица dbo.Products (тип U) существует. Класс StackAdaptationTests, тест "test Products table exists", без FakeTable и без NewTestClass. Следующая полезная задача, GetReorderCandidates, — отдельный обычный план после sibling ready.
3. Машина: macOS. Python 3.12 уже стоит первым в PATH; новый Python не ставить. .NET SDK 10.0.401 в global.json с rollForward latestFeature. go-sqlcmd с --encrypt-connection=mandatory -C -b. SqlPackage 170.5.96 — локальный dotnet tool. Microsoft.Build.Sql 2.3.0 с Sql150DatabaseSchemaProvider. tSQLt — пакет tSQLt.Dacpacs 1.0.8083.3529, DacpacName tSQLt.2019. SQLFluff 3.4.2: tsql, raw, длина 120. make setup один раз ставит зависимости в .tmp/; дальше всё офлайн, кроме живых целей.
4. Раскладка: sql/Northwind/Northwind.sqlproj; sql/Northwind/Imported/ — только результат Extract, руками не правится; sql/Northwind/Authored/ — код ролей; sql/tests/Northwind.Tests.sqlproj с ProjectReference на Northwind.sqlproj и tSQLt.Dacpacs; тесты в sql/tests/<Класс>/. Обвязка — scripts/sql.py на стандартной библиотеке Python за целями make, её офлайн-тесты — scripts/test_sql.py.
5. Extract: SqlPackage /Action:Extract из Northwind с /p:ExtractTarget=SchemaObjectType, /p:ExtractAllTableData=False, /p:ExtractReferencedServerScopedElements=False, /SourceEncryptConnection:True, /SourceTrustServerCertificate:True, во временный каталог. Файлы из каталогов безопасности (Security, Users, Roles, Permissions и т. п.) удаляются целиком. Если в оставшемся SQL есть CREATE USER, ALTER ROLE, GRANT или INSERT — отказ, старый Imported остаётся. Imported заменяется атомарно. Ожидаемо 36 файлов: 13 таблиц, 16 представлений, 7 процедур. Одночастные имена вроде CustOrderHist допустимы; имена объектов не разбираются, Imported в один файл не объединяется.
6. Publish — только в dev-базу и только после свежей проверки цели одним запросом: имя базы совпадает с настроенным, свойство planveyor.designated_dev есть (значение не читается), логин не sysadmin; иначе код 3 и ни одной публикации. Флаги: IncludeCompositeObjects=True, DropObjectsNotInSource=True, ExcludeObjectTypes=Users;Logins;RoleMembership;Permissions, DropExtendedPropertiesNotInSource=False (маркер сохраняется), ScriptDatabaseOptions=False, BlockOnPossibleDataLoss=True, /TargetEncryptConnection:True, /TargetTrustServerCertificate:True.
7. Тесты: EXEC tSQLt.RunAll; без параметров, затем EXEC tSQLt.XmlResultFormatter; — это JUnit. Постоянный formatter не менять. XML читается через sqlcmd с -h -1 -y 0 -w 65535, чтобы вывод не форматировался и не обрезался. JUnit разбирается строго. hostname и любые сведения о сервере вычищаются из вывода и из JUnit на всех путях, включая отказы и таймауты.
8. Цели make: setup; db-extract (живая, только чтение Northwind); db-build; lint (Authored и tests); test (офлайн scripts/test_sql.py); check-secrets; db-proof JUNIT=<относительный путь> (сборка, проверка цели, Publish, RunAll, JUnit); db-state (только чтение: схемы, объекты, классы tSQLt, последние результаты; на пустой базе — явный пустой отчёт; строковые выражения системного каталога с COLLATE DATABASE_DEFAULT). Коды выхода: 0 успех, 1 тесты, 2 конфигурация, 3 проверка цели, 4 подключение, 5 сборка или lint, 6 публикация.
9. Живые цели запускают роли в песочнице Codex с уже включённой сетью (вариант А): setup и db-extract — Coder; db-proof — Coder и независимо Reviewer, каждый со своим JUnit; db-state — Architect и Reviewer.
10. Подключение: .env.local в корне, права 0600, в .gitignore, не отслеживается; ключи SQLCMDSERVER, SQLCMDDBNAME, SQLCMDUSER, SQLCMDPASSWORD. Файл уже положен. Читает его только обвязка; пароль для sqlcmd — только через переменную окружения; SqlPackage получает пароль аргументом, для однопользовательского Mac это принято.
11. Доказательство: JUnit в docs/code_reviews/assets/<plan-stem>/ — у Coder <name>.junit.xml, у Reviewer свой прогон <name>.review.junit.xml. JUNIT обязателен; путь относительный, .xml, внутри проекта, без symlink и без выхода из корня. Если файл отслеживается Git или ответ Git неизвестен — отказ до удаления, настройки, сборки и SQL; только достоверно неотслеживаемый старый XML удаляется до сборки, новый пишется атомарно. В Evidence: команда, коды выхода, HEAD, bundle_sha256, путь и SHA-256 JUnit, tests/failures/errors/skipped, имена testcase. В документах только относительные пути и make <цель>.
12. Не делать: собственный разбор имён SQL, протокол временной смены formatter, внешние модели и MCP, вопросы владельцу по фактам из этого списка. Вне объёма: CI, другие ОС и версии SQL Server, production и бизнес-данные, сервер, логины, CLR и маркер, правка движка Planveyor, публикация и push.
```

Скилл создаёт план и анкету `docs/stack_brief.md` в статусе
`Architect initial draft`; черновика кода ещё нет. Запомните фактически
созданный путь из ответа скилла, дату исторического плана не копируйте. Затем
проверьте выбор плана:

```sh
planveyor sibling plan
```

Пока первый план не выбран, команда завершается с кодом 3 и сообщением:

```text
planveyor sibling: Текущий plan не выбран или pointer повреждён. Выполните planveyor sibling plan docs/plans/NAME.md.
```

Тогда выберите созданный план явно:

```sh
planveyor sibling plan "docs/plans/<план>.md"
```

Ожидается:

```text
План: docs/plans/<план>.md
Статус: architect initial draft
Следующий шаг: planveyor sibling architect
```

В режиме TUI можно начать и сразу с окна (раздел 7): если открытых вопросов к
Owner в плане нет, Manager сам начнёт с обсуждения задачи с Architect. Так прошло
обновление (раздел 10).

Иначе начните обсуждение с Architect:

```sh
planveyor sibling architect
```

`architect` печатает открытые вопросы с их id и следующий шаг. Вопросов может не
быть: если развилок для Owner нет, Architect сам переводит план в статус
`Architect draft`. Так и вышло на адаптации:

```text
План: docs/plans/<план>.md
Статус: architect draft
Следующий шаг: planveyor sibling run
```

Как и другие строки «Следующий шаг: …», эта называет команду ручного режима: в
режиме TUI вместо `run` откройте окно Manager по разделу 7. Вопросы, уже открытые
в плане, закройте до окна командой `answer` и шагом, который она напечатает. Если
это `planveyor sibling architect`, выполните его, а `planveyor sibling run` в
режиме TUI не выполняйте. С открытыми вопросами `sibling tui` окно не откроет.

Учтите условия прохода: черновик плана писал агент, которому были известны все
двенадцать фактов и банк ответов. С неполными фактами или с другим стеком ждите
вопросов по разделам анкеты.

Раздел `## Как я понял задачу` в плане есть всегда. Прочитайте его после
`architect` и до `run` или окна Manager, сверьте с фактами стека и анкетой.
Вывести раздел можно так:

```sh
awk '/^## Как я понял задачу/{p=1; print; next} p && /^## /{exit} p' "docs/plans/<план>.md"
```

Если команды выполняет агент, попросите его выводить этот раздел в чат перед
каждым `run` и перед окном Manager: так вы видите его до того, как работа
перейдёт к Planner. В режиме TUI вы говорите с Manager в его окне и можете
попросить его вывести раздел при переходе к Planner.

Если вы хотите подтвердить раздел сами до перехода в `Architect draft`, допишите в
запрос скиллу: «До перевода плана в Architect draft покажи мне раздел «Как я
понял задачу» и дождись подтверждения». Обычно Architect тогда открывает вопрос,
и вы подтверждаете раздел обычным `planveyor sibling answer`. Это поведение
модели, движок его не гарантирует.

Штатного способа поправить раздел после перехода в `Architect draft` в первой
версии нет: `answer` без открытого вопроса в этом статусе отказывает с кодом 3.
Если раздел расходится с вашим поручением, не запускайте ни `run`, ни окно
Manager: это остановка из раздела 11.

Если вопрос есть, передайте ответ с номером из вывода роли. Номер не
придумывают. Текст возьмите из приложения А и вставьте между строками `<<'EOF'`
и `EOF`:

```sh
planveyor sibling answer Q1 <<'EOF'
<текст ответа из приложения А>
EOF
```

Ответ можно передать и из файла: `planveyor sibling answer Q1 < <файл>`. Команда
печатает вопрос и затем строку:

```text
Ответ сохранён. Следующий шаг: planveyor sibling architect
```

Выполните напечатанный шаг. Пока план в статусе `Architect initial draft`, на
несколько вопросов отвечайте по одному: второй `answer` до следующего хода
Architect откажет с сообщением «Уже есть ожидающий Owner payload…». Если
открытого вопроса нет, а план ещё в статусе `Architect initial draft`, `answer`
без номера покажет текущий итог Architect и передаст ему ваше решение, например
подтверждение О1:

```sh
planveyor sibling answer <<'EOF'
<текст О1 из приложения А>
EOF
```

В других статусах без открытого вопроса команда отказывает с сообщением
«Открытых Owner вопросов нет.» и кодом 3.

Ответ применяется только к совпадающей постановке. Технические детали обвязки
роли решают по фактам стека и документации. Изменение границ задачи, прав или
приёмки требует вашего ответа. Статусы, журнал вопросов и квитанции вручную не
правьте.

## 7. Провести план и первый коммит

План проводят в одном из двух режимов Planveyor. Их описывает раздел «Два режима
работы с планом» руководства движка
`"$PLANVEYOR_RUNTIME_ROOT/docs/guides/stack-sibling.ru.md"`. Выберите режим до
первого запуска ролей.

| | Режим TUI | Ручной режим в консоли |
| --- | --- | --- |
| Запуск | `planveyor_manager_init`, шаг с одобрениями в `planveyor_manager_resume`, затем `planveyor sibling tui` | `planveyor sibling run`, затем `close` и `close --commit` |
| Коммиты | Architect в окне Manager, по прямому разрешению Owner на этот план; каждый запрос записи в `.git` одобряется разово | Вы, командой `close --commit` после просмотра через `close` |
| В этом sibling | обновление движка 28–29 октября (раздел 10) | оба плана 11–12 октября |

Правило коммитов записано в корневом [README.md](../../README.md) и в анкете
стека `docs/stack_brief.md`: автоматический коммит запрещён, а в режиме TUI
Architect коммитит только по прямому разрешению Owner для конкретного плана. Это
правило этого sibling, движок его не проверяет (раздел «Режим TUI» ниже).

### Что делают роли

В обоих режимах живые цели выполняют роли: свои SQL-проверки параллельно с ними
не запускайте. Эти команды роли записывают в журнал проверок плана
(`## Evidence`):

```text
make setup
make db-extract
make db-build
make lint
make test
make check-secrets
make db-proof JUNIT="docs/code_reviews/assets/<plan-stem>/canary.junit.xml"
```

`setup` и Extract выполняет Coder. Reviewer повторяет нужные офлайн-проверки сам
и выполняет собственный полный прогон:

```text
make db-proof JUNIT="docs/code_reviews/assets/<plan-stem>/canary.review.junit.xml"
make db-state
```

Значения в угловых скобках роли заменяют настоящими относительными путями.
Extract даёт 36 файлов схемы: 13 таблиц, 16 представлений, 7 процедур. Каждый
живой прогон собирает проекты, заново проверяет цель, публикует, запускает
`RunAll` с неизменённым formatter и атомарно пишет очищенный XML. Coder и
Reviewer работают с одной dev-базой по очереди. В обоих JUnit первого плана
ожидается **1 testcase, 0 failures, 0 errors, 0 skipped**: постоянный canary
реальной таблицы `dbo.Products`.

В журнале проверок нужны точная команда, отдельные коды `make` и обвязки, `HEAD`
и `bundle_sha256` до и после прогона, путь и SHA-256 XML, счётчики и имена
testcase. Одинаковые хеши XML сами по себе не доказывают независимость: нужны
отдельные фактические прогоны двух ролей. `db-state` показывает состояние базы
для контекста и JUnit не заменяет.

### Строка Provide PLAN_PATH

В выводе `architect`, `run` и `planveyor_manager_init` встречаются такие строки:

```text
- Next: Owner
- Open items: (to=Owner, needs_owner=yes) Provide `PLAN_PATH`
```

Это фиксированная концовка первого хода новой сессии. Заводя сессию, Planveyor
сначала даёт ей вводную без плана, а план передаёт следующим сообщением; Codex
печатает оба ответа. Поэтому строки появляются только при заведении сессии: на
первом запуске, после коммита, после обновления. Делать ничего не нужно: в
ручном режиме действует последняя строка «Следующий шаг: …».

### Режим TUI

Из корня sibling отметьте время для проверки моделей (раздел 4), заведите новую
сессию Manager, включите в ней запросы одобрения команд и откройте окно Manager
для выбранного плана:

```sh
touch "$TMPDIR/planveyor-models.start"
planveyor --project "$PWD" planveyor_manager_init
planveyor --project "$PWD" planveyor_manager_resume
planveyor sibling tui
```

`planveyor_manager_resume` открывает окно той же сессии, в нём только стартовый
ответ Manager. Введите в нём `/permissions`, выберите «Ask for approval» и
проверьте командой `/status`, что в строке «Permissions» стоит «Ask for
approval». Затем выйдите. Этот порядок нужен для каждой новой сессии Manager, а
между командами не меняйте файлы и индекс. Проверки команды `tui`, её отказы и
повторное открытие окна описаны в разделе «Провести план в режиме TUI»
руководства движка.

`planveyor_manager_init` печатает вывод первого хода новой сессии, в том числе
строки про `PLAN_PATH` (см. выше); это нормально. Если такой же вывод появился
после `planveyor sibling tui`, перед окном, значит `tui` сам завёл новую сессию
без запросов одобрения. Тогда дождитесь конца текущего хода, выйдите из окна и
начните заново с первых двух команд.

До окна в плане не должно быть открытых вопросов к Owner (раздел 6). Коммиты
Architect в окне по правилу этого sibling требуют прямого разрешения Owner на
конкретный план. В обновлении разрешение вошло в ответ на первый вопрос Architect
в окне, текст — О24 в приложении А. Если Architect не спросит, напишите
разрешение Manager в окне до приёмки тем же текстом. Движок такое разрешение не
проверяет: в окне политика коммитов всегда `native_existing`, и Architect
коммитит сам. Удержать коммит можно только отказом на запрос записи в `.git` в
окне, а такие запросы появляются лишь после шага с `/permissions`. Без
разрешения Owner на план ведите план в ручном режиме.

В окне Manager ведёт роли Architect, Planner, Coder и Reviewer по статусу плана,
а на вопросы вы отвечаете там же. Когда Architect примет работу, он коммитит
реализацию, те же роли закрывают документы, и, если закрытие требует коммита
документов, Architect коммитит и их. Паузы на просмотр через `close` нет, и
`close --commit` не нужен.

В песочнице ролей `.git` доступен только на чтение, поэтому для каждой записи
Architect запрашивает повышение прав. Окно показывает «Would you like to run the
following command?», причину и точную команду. Каждый раз выбирайте разовое «Yes,
proceed», а не пункт с «don't ask again»: он создаёт постоянное правило. В
обновлении окно отдельно спрашивало про подготовку набора файлов, предварительную
проверку закрытия, их повторы, коммит реализации и коммит документов, всего шесть
раз. Чтобы сначала посмотреть набор, выполните `planveyor sibling close` в другом
терминале: этот вызов только показывает состояние.

Тишина в окне — ещё не зависание: идущий ход не прерывайте. Если ход закончился
ошибкой модели, например «Selected model is at capacity», окно и роли остаются
прежними, а продолжать ли, решает Owner. В обновлении это случилось трижды, и
каждый раз по поручению владельца в том же окне писали «Продолжай». Держите окно
открытым, пока закрытие документов не закончится, затем выйдите командой
`/quit`. Если окно закрылось после коммита реализации, но раньше, чем
закончилось закрытие документов, это остановка из раздела 11. Окно обновления
было открыто 7 ч 41 мин; около 4 ч из них первый запрос записи в `.git` ждал,
пока владелец решал вопрос о префиксе `PATH` (раздел 12).

### Ручной режим в консоли

```sh
touch "$TMPDIR/planveyor-models.start"
planveyor sibling run
```

Первая строка нужна для проверки моделей из раздела 4. Следуйте последней строке
вывода «Следующий шаг: …». Вопросы ролей друг другу с `needs_owner=no` роли
решают сами. Если Manager остановился на лимите хода, повторите тот же `run`.
Ошибку или незнакомый отказ сначала разберите, слепо команду не повторяйте.
`run` идёт долго: в проходе адаптация заняла 11 ч 22 мин от init до закрытия
документов.

#### Пока run работает

Второй `run` не запускайте. Прерывать работающий `run` ради проверки прогресса
не нужно: статус плана и открытые вопросы видно чтением файла.

```sh
rg -n '^\*\*Status:|status=open' "docs/plans/<план>.md"
```

#### Остановить run и продолжить тот же план

Остановка нужна по правилам раздела 11. Например, ревью в третий раз возвращает
Coder тот же технический вопрос.

1. Остановите `run` одним сигналом SIGINT. В терминале нажмите Ctrl-C в окне
   `run`. Агент отправляет SIGINT группе процессов этого `run`. Принудительное
   завершение `kill -9` не используйте.
2. `run` завершится с ненулевым кодом, в проходе — с кодом 1. Роль могла не
   закончить ход: в проходе Manager успел запустить новый ход Coder, и его тоже
   прервали.
3. Зафиксируйте состояние, ничего не исправляя:

   ```sh
   planveyor sibling plan
   git diff --cached --name-status
   git status --short --untracked-files=all > "$TMPDIR/planveyor-stop.status"
   git ls-files -m -o --exclude-standard -z | xargs -0 shasum -a 256 > "$TMPDIR/planveyor-stop.sha256"
   ```

   Индекс Git должен быть пуст: `git diff --cached` ничего не выводит. Две
   последние строки сохраняют полный список изменённых и новых файлов и их
   контрольные суммы. Флаг `--untracked-files=all` перечисляет каждый новый файл,
   а не только его каталог.
4. Решите, оставить остановку или продолжить тот же план. Это решение Owner;
   агент сам не продолжает.
5. Перед продолжением убедитесь, что файлы не менялись:

   ```sh
   git status --short --untracked-files=all > "$TMPDIR/planveyor-continue.status"
   diff "$TMPDIR/planveyor-stop.status" "$TMPDIR/planveyor-continue.status"
   shasum -a 256 -c --quiet "$TMPDIR/planveyor-stop.sha256"
   planveyor sibling plan
   ```

   `diff` и `shasum` ничего не выводят, если ничего не изменилось. `plan`
   показывает прежний план и его следующий шаг, обычно тот же
   `planveyor sibling run`. Только после этого выполните этот шаг:

   ```sh
   planveyor sibling run
   ```

   В проходе продолжение тем же `run` довело план до приёмки Architect с кодом 0.

План, ревью, статусы и квитанции при остановке руками не правят, новый план ради
продолжения не создают.

#### Просмотр и коммит

После приёмки Architect посмотрите будущий коммит:

```sh
planveyor sibling close
```

Ожидается код 0 и первая строка «План принят. Следующий шаг: planveyor sibling
close --commit.». За ней идут список файлов и строка «Сообщение коммита: …».
Прочитайте **весь** набор и сообщение. Новые файлы набора откройте в редакторе:
`git diff` показывает только изменения уже отслеживаемых файлов. Без `--commit`
команда ничего не меняет.

`close` требует в файле ревью ровно один раздел `## Архитектурное ревью` (или
`## Arch review`), и его первая непустая строка должна быть «Вердикт: принято.».
Если Architect оставил заголовок шаблона с хвостом «(Architect; optional)»,
`close` ответит «Нужна одна секция «Архитектурное ревью» в review artifact.
Следующий шаг: planveyor sibling architect.». При другой первой строке он
ответит «Первый вердикт Architect не даёт однозначной приёмки…». В обоих случаях
выполните `planveyor sibling architect`, затем снова `close`. Это технический
возврат, вопрос Owner не нужен.
Если `architect` ответит «Текущий status не принадлежит Architect; используйте
planveyor sibling run.», выполните `run`.

Коммит разрешаете вы после просмотра (раздел 1). Если набор изменился, сначала
получите новый просмотр. Затем:

```sh
planveyor sibling close --commit
```

Ожидается код 0 и строка «План закоммичен. Следующий шаг: planveyor sibling run
для документов.», затем тот же список и сообщение. Сверьте фактический коммит с
просмотром:

```sh
git show --stat --format='%H%n%s' HEAD
```

Зелёное ревью, приёмка и `Done` не разрешают push или публикацию.

## 8. Документы и ready после каждого плана

В режиме TUI документы закрывают те же роли в том же окне, а коммит документов,
если он нужен, делает Architect (раздел 7). В обновлении закрытие записало
предложения по процессу (PI) — файл бэклога плана и три сводки, — и Architect
закоммитил их отдельным коммитом. После выхода из окна переходите сразу к `ready`
ниже.

В ручном режиме после коммита плана выполните по одной команде:

```sh
planveyor sibling run
planveyor sibling close
```

Дождитесь завершения `run` и прочитайте его вывод. Итоговое сообщение Manager о
закрытии документов печатает `run`: в проходе оно содержало
`final_docs_commit=no_op`, и отдельный коммит документов не понадобился.
Обычно последняя строка `run` — «Следующий шаг: planveyor sibling close». Строка
`general_pi_format_correction_state=retryable` или `=blocked` означает остановку:
следуйте строке таблицы «Если команда остановилась» руководства движка.

Если `close` показывает отдельный набор документов, прочитайте его и сообщение и
выполните `close --commit` после разрешения на этот набор. Этап закрыт только при
коде 0 и фразе:

```text
План и документы закрыты. Можно начать следующую задачу.
```

Теперь:

```sh
planveyor sibling ready
```

Нужны код 0 **и** точный итог:

```text
Consumer contract и выбранный план закрыты. Готовность отдельного release или SQL не проверялась.
```

Другой текст при коде 0 означает незавершённую задачу: выполните напечатанный
следующий шаг. `ready` не повторяет SQL и не проверяет готовность к выпуску. До
следующего плана проверьте свежие собственные JUnit обеих ролей: два XML в
`docs/code_reviews/assets/<plan-stem>/` и их записи в журнале проверок плана
(`## Evidence`) с числом testcase и нулём failures, errors и skipped.

## 9. Второй план: товары к дозаказу

Только после полного закрытия адаптации отправьте в чат прямое поручение:

```text
$planveyor-plan-draft Создай и сделай текущим обычный план по моему прямому поручению: Реализовать читающую процедуру dbo.GetReorderCandidates без параметров. Она возвращает товары только с Discontinued = 0 и Shortage = ReorderLevel - (UnitsInStock + UnitsOnOrder) > 0. Числовые NULL считаются 0, значения приводятся к int до арифметики. Колонки: ProductID int, ProductName nvarchar(40), Shortage int, сортировка по ProductID. Восемь содержательных бизнес-тестов tSQLt (T1–T8) и постоянный canary dbo.Products проходят в самостоятельных прогонах Coder и Reviewer в принятой dev-среде: девять testcase, ноль failures, errors и skipped. Покажи matching open follow-up, сохрани его неизменным и добавь source_ref#item_id в Context links.
```

Скилл ищет открытую отложенную задачу (follow-up) по той же теме. Найденную
запись он оставляет без изменений и добавляет её `source_ref#item_id` в контекст
плана. Если совпадения нет, скилл фиксирует это без искусственной записи. В проходе
совпадений не было.

Указатель плана скилл может оставить на прошлом плане: в проходе он ответил
«current pointer unchanged». Выберите новый план по фактическому пути:

```sh
planveyor sibling plan "docs/plans/<новый-план>.md"
planveyor sibling architect
```

В проходе Architect задал вопрос `Q1`: подтвердить постановку, тесты T1–T8 и
ограниченную адаптацию существующей обвязки под девять тестов. Ответом ушли
тексты О20 и Т из приложения А одним сообщением. При повторе id берите из
текущего вывода, а этот ответ отправляйте, только если вопрос совпадает:

```sh
planveyor sibling answer Q1 <<'EOF'
Отвечаю по поручению Owner. Подтверждаю раздел «Как я понял задачу»: читающая процедура dbo.GetReorderCandidates без параметров; только Discontinued = 0 и Shortage = ReorderLevel - (UnitsInStock + UnitsOnOrder) > 0; числовые NULL = 0; приведение к int до арифметики; колонки ProductID int, ProductName nvarchar(40), Shortage int; сортировка по ProductID. Восемь бизнес-тестов:
T1 — пустая Products, пустой результат;
T2 — активный товар 10/4/2, Shortage 4;
T3 — нулевой и отрицательный дефицит не попадают;
T4 — дефицит, покрытый заказами в пути, не попадает;
T5 — снятый с продажи товар с дефицитом исключён;
T6 — NULL в каждом числовом поле и их сочетаниях; NULL порога не создаёт кандидата;
T7 — ReorderLevel 32767 и оба остатка 32767 — без переполнения;
T8 — контракт результата: типы, порядок колонок, сортировка по ProductID.
Девятый — постоянный canary. Coder и Reviewer — самостоятельные последовательные прогоны, каждый со своим JUnit: девять testcase, ноль failures, errors и skipped. Подтверждаю переход в Architect draft. Это не разрешение на коммит.

Отвечаю по поручению Owner. Это технический вопрос обвязки, а не решение владельца: исправьте по документации инструмента и фактам стека из анкеты, не меняя Scope, права и приёмку. Если исправление требует изменить что-то из этого — верните вопрос с вариантами.
EOF
```

Затем по одной команде, каждую после результата предыдущей:

```sh
planveyor sibling architect
planveyor sibling run
```

В режиме TUI вместо `run` откройте окно Manager по разделу 7. В проходе `answer`
направил к Architect, тот закрыл Q1 и направил к `run`.
Ограниченную адаптацию существующего разбора XML, офлайн-тестов, README и
локальных правил под девять тестов Architect сам вписал в вопрос Q1 как уточнение
постановки и после ответа закрыл вопрос.

Coder и Reviewer выполняют каждый свой полный прогон на одном актуальном снимке
целевых файлов:

```text
make db-proof JUNIT="docs/code_reviews/assets/<новый-plan-stem>/reorder.junit.xml"
make db-proof JUNIT="docs/code_reviews/assets/<новый-plan-stem>/reorder.review.junit.xml"
```

Это **два разных последовательных запуска разных ролей**, общий запуск за них
вы не делаете. Каждый XML содержит T1–T8 и постоянный canary: **9/0/0/0**. T6
покрывает NULL в каждом числовом поле и их сочетания. T8 проверяет метаданные
самой процедуры и сортировку. Одних итоговых счётчиков без девяти уникальных
имён testcase недостаточно. Любое изменение целевых файлов требует нового
прогона.

После приёмки повторите разделы 7–8. В ручном режиме: `close`, прочитанный
просмотр, разрешённый `close --commit`, отдельный `run` для документов, `close`,
затем `ready` с точной фразой. В режиме TUI коммиты и закрытие документов идут в
окне, затем `ready`. Отслеживаемый Git исторический XML в `JUNIT` не передавайте:
обвязка отвергнет такой путь до удаления, сборки и SQL. Для новой задачи нужен
новый фактический plan-stem.

## 10. Обновление движка

Sibling закреплён на версии движка из `source_commit`. Новую версию выбираете вы,
а обновление проходит отдельным обычным планом. Порядок описан в разделе
«Получить новую версию Planveyor» руководства движка. Ниже — как обновление
прошло в этом sibling 28–29 октября: с `8c5256e7` на `66050258`.
Коммита `66050258` в публичной истории Planveyor нет: при объединении коммитов
документации его заменил `ff0a16b` с тем же деревом файлов, и sibling перевели
на этот коммит (раздел 2).

Перед обновлением текущая задача должна быть закрыта, изменения закоммичены, так
что `git status` ничего не показывает, а активные сессии завершены. Выйдите из
каталога sibling: `upgrade` меняет каталоги местами. Из внешнего каталога, с
копией Planveyor новой версии в `PATH`:

```sh
planveyor --project "$SIBLING_DIR" sibling upgrade
```

Ожидаются код 0 и такой вывод; путь резервной копии и имя плана у вас свои:

```text
Обновление использует выбранный runtime; existing upgrade сохранит backup и создаст план адаптации.
Backup: <родительский каталог>/.planveyor-mssql-before-<первые 12 знаков новой версии>
Контракт обновлён; адаптация ещё открыта.
План: docs/plans/<…>_contract_upgrade_<…>.md
Статус: architect initial draft
Следующий шаг: planveyor sibling architect
```

Резервная копия содержит весь проект, включая `.env.local`: храните её только у
себя и удалите сами, когда план обновления примут. План обновления команда
выбирает сама, `planveyor sibling plan` его показывает. В выводе `upgrade` он
назван планом адаптации.

Терминалы, открытые в sibling до обновления, после него оказываются в резервной
копии: `upgrade` переименовал прежний каталог, а под его именем теперь лежит
обновлённый sibling. Перед следующими командами снова выполните в них
`cd "$SIBLING_DIR"`, потому что команды без `--project` выбирают проект по
текущему каталогу.

В обновлении команда изменила 25 путей: 22 доставленных файла движка, сам план,
файл с закреплённой версией `docs/_meta/planveyor_contract_authority.v1.json` и
`.copier-answers.yml`. Локальные разделы восьми файлов правил сохранились
побайтно; в четырёх из них изменилась только часть шаблона выше локальных
разделов. Корневой `README.md`, анкету, обвязку и SQL команда не трогала.

Дальше план обновления проводят как любой другой (раздел 7). В обновлении он шёл
в режиме TUI:

1. `planveyor sibling plan` показал выбранный план без открытых вопросов к Owner,
   поэтому `architect` и `answer` до окна не понадобились.
2. `planveyor_manager_init`, затем `planveyor_manager_resume`, где включили
   запросы одобрения, и `planveyor sibling tui` открыли одно окно Manager на весь
   план.
3. В окне Architect составил черновик и задал два вопроса: Q1 — подтвердить
   постановку и переход в `Architect draft`, Q2 — разрешить `make setup` для
   восстановления кэшей. Ответ ушёл одним сообщением: О25, О24 и О26 из
   приложения А.
4. Coder один раз выполнил `make setup` с сетью: клон был свежим, без кэшей в
   `.tmp/`. Затем Coder и строго после него Reviewer выполнили каждый свой
   `make db-proof`; оба JUnit — 9/0/0/0.
5. Приёмка Architect, коммит реализации, закрытие документов и коммит
   документов прошли в том же окне. Каждую запись в `.git` агент, который вёл
   окно, одобрял разово по разрешению владельца, всего шесть раз. Затем окно
   закрыли командой `/quit`.
6. `planveyor sibling ready` завершился с кодом 0 и точным итогом из раздела 8.

Если план обновления ведёте в ручном режиме, начинайте с напечатанного
`planveyor sibling architect`.

Сессии, заведённые до обновления, к новой версии не переходят: после `upgrade`
роли начинают с новых сессий. В режиме TUI это получается само, потому что окно
открывают после нового `planveyor_manager_init`. В ручном режиме, если копию
Planveyor обновили на месте, `architect` и `run` заведут новые сессии сами. Если
новая версия лежит в другом каталоге, они откажут с сообщением «Receipt
принадлежит другому project/runtime; сессия не заменена.»; тогда заведите сессию
по таблице «Если команда остановилась» руководства движка.

## 11. Отказы и остановки

Для разбора отказов сохраняйте команду, вход, время начала и конца, рабочий
каталог, вывод без секретов и код возврата. Удобное место — `.tmp/` sibling.
Различайте код `make` и код обвязки. `make` возвращает 2 при любом упавшем
рецепте. Собственный код обвязка печатает строкой
`sql phase=… category=… rc=N`, при отказе с `reason=…`.

| Код обвязки | Смысл |
| --- | --- |
| 0 | Успех |
| 1 | Тесты или JUnit упали, отчёт повреждён |
| 2 | Конфигурация, путь, Git, секреты, неверный результат Extract |
| 3 | Цель dev не прошла проверку, публикации не было |
| 4 | Подключение или чтение SQL |
| 5 | Сборка, lint, выгрузка Extract или атомарная замена |
| 6 | Публикация |

Если `close` отказал с причиной в плане, следуйте его сообщению: это работа
ролей. Если сообщение не называет штатного шага, остановитесь.

Остановитесь и решите сами, если:

- предпосылка из разделов 2–4 не подтверждена;
- раздел «Как я понял задачу» расходится с поручением или анкетой;
- вопроса нет в приложении А и он не технический;
- модель роли не совпала с настройкой;
- в `RunAll` больше наборов тестов, чем ожидается, или в dev-базе чужие объекты;
- нужно изменить границы задачи, права или приёмку;
- Planveyor ведёт себя не так, как описано здесь;
- один и тот же технический возврат повторяется в третий раз;
- окно Manager закрылось после коммита реализации, раньше, чем закончилось
  закрытие документов;
- ход в окне закончился ошибкой модели, например «Selected model is at capacity».

Сохраните команду, вывод и состояние плана, затем выберите вариант. Работающий
`run` останавливайте по разделу 7. Контрольное время задайте себе заранее: в
проходе адаптация заняла 11 ч 22 мин от init до закрытия документов, вторая
задача — 3 ч 46 мин от поручения до закрытия, окно обновления было открыто
7 ч 41 мин, из них около 4 ч оно ждало решения владельца.

Если окно Manager закрылось после коммита реализации, раньше, чем закончилось
закрытие документов, не открывайте новое окно и не запускайте `run`
автоматически: новый вход не восстанавливает прежние роли или потраченную
попытку коррекции PI. Сохраните вывод, состояние плана и данные закрытия
документов; следующий шаг выбирает Owner. Если остался только коммит документов,
сначала посмотрите вывод `planveyor sibling close`, а `close --commit` выполняйте
только после отдельного разрешения Owner. Как снова открыть окно, закрытое до
коммита реализации, описывает раздел «Провести план в режиме TUI» руководства
движка.

Ради зелёного результата не правьте движок, закрытые план и ревью, квитанции,
счётчики, проверки цели и настройки среды. Технические замечания проходят
обычные роли. Свежая проверка цели, строгий разбор XML, очистка вывода, граница
Git для `JUNIT` и отказ от автоматических повторов SQL описаны в
[README.md](../../README.md) и сохраняются.

## 12. Что подтвердили проходы

Идентификаторы ниже относятся к 11–12, 28–29 и 30 октября 2026 года, в новый
запуск их не подставляют. Артефакты лежат в истории Git этих коммитов.

| План | Коммит плана | JUnit Coder и Reviewer |
| --- | --- | --- |
| [`261011_1523_stack_adaptation`](../plans/261011_1523_stack_adaptation.md) | `87d5a543b562c4f1db4d0ae22f7c837cd068c760` | каждый 1/0/0/0 |
| [`261012_0141_get_reorder_candidates`](../plans/261012_0141_get_reorder_candidates.md) | `be6bbbcdc679844e697382899321768a517b048d` | каждый 9/0/0/0 |
| [`261029_0155_contract_upgrade_8c5256e_6605025`](../plans/261029_0155_contract_upgrade_8c5256e_6605025.md) | `8cc3d044585032c0a35b2667db27f8033ee638cf`, документы — `ca4b6e4a0507dfde5be58cb824bfbabc0114871d` | каждый 9/0/0/0 |
| [`261030_0221_shared_rules_pinned_source_check`](../plans/261030_0221_shared_rules_pinned_source_check.md) | `783c208f2e6c47f5e633b0794a6fcbe3495abe1b`, документы — `e56789785e1f8a70cbfcd5e820ff3c669a2bf679` | каждый 9/0/0/0 |

Первые два плана достигли `Done`. У обоих закрытие документов прошло 8/8 линий:
followups `external_clean_noop`, PI `clean_noop`, `final_docs_commit=no_op`.
Отдельных коммитов документов не потребовалось. `close` и `ready` обоих планов
дали требуемые фразы с кодом 0. На финальной сверке `HEAD` указывал на второй
коммит, дерево было чистым. Первая версия этого руководства добавлена после
второго плана отдельным коммитом.

План обновления тоже достиг `Done`. Его закрытие документов записало
предложения по процессу (PI) — файл бэклога плана и три сводки, — и Architect
закоммитил их отдельным коммитом. Повторная проверка закрытия после этого коммита
дала `final_docs_commit=no_op`: документов плана, ждущих коммита, больше не было.
`ready` дал требуемую фразу с кодом 0. Эта версия руководства и тексты о двух
режимах коммита в README и анкете стека добавлены после обновления отдельным
коммитом.

Четвёртый план вернул в `scripts/test_sql.py` побайтную проверку общей части
восьми файлов правил, которую потеряла правка теста в плане обновления. Теперь
тест сравнивает эту часть с файлами шаблона Planveyor на том коммите, на котором
закреплён sibling. План прошёл в одном окне Manager и тоже достиг `Done`. Его
закрытие документов записало предложения по процессу — файл бэклога плана и три
сводки, — и их закоммитили отдельным коммитом документов.

Файлы JUnit лежат в `docs/code_reviews/assets/<исторический-plan-stem>/`: пара
`canary.junit.xml` / `canary.review.junit.xml` для адаптации, пара
`reorder.junit.xml` / `reorder.review.junit.xml` для второй задачи, пара
`upgrade.junit.xml` / `upgrade.review.junit.xml` для обновления и пара
`coder.junit.xml` / `reviewer.junit.xml` для четвёртого плана. Их
подтверждают записи о командах, кодах и снимках в планах и ревью. Проходы не
проверяли production, CI, другие ОС и версии SQL Server, публикацию и выпуск.

В адаптации вопросов Owner не было: Architect сам перевёл план в статус
`Architect draft`. Во второй задаче Architect задал один вопрос, ответом стали
О20 и Т. В обновлении Architect задал в окне два вопроса, ответом стали О25, О24
и О26. В обоих проходах Manager, все роли и встроенные субагенты шли на
`gpt-6.1-sol` / `ultra`. В четвёртом плане Architect задал два вопроса: Owner
подтвердил, как Architect понял задачу, и разрешил ему коммиты плана в том же
окне.

### Как шёл проход 11–12 октября

- Проход вёл агент Codex по заранее написанному сценарию: блок фактов, банк
  ответов из приложения А и правила остановки. Черновик плана адаптации этот
  агент создал сам по шагам скилла, зная все ответы. Поэтому ноль вопросов на
  адаптации — результат подготовленного входа, а не обещание для любого стека.
- Решения, которые сценарий оставлял владельцу, в двух местах принял координатор
  прохода: продолжить план после остановки и ответить на Q1 второго плана
  текстами О20 и Т. Перед продолжением координатор отдельно проверил исправление
  на другой модели; ролям эту проверку не передавали.
- На адаптации ревью в третий раз вернуло Coder защиту JUnit от перезаписи
  отслеживаемого файла: каждый круг находил ещё один обход проверки Git. По
  правилу остановки `run` прервали сигналом SIGINT, он завершился с кодом 1.
  Перед продолжением сверили 60 из 60 целевых файлов со снимком ревью: изменений
  не было. Тот же план продолжили тем же `run` без правок, и он дошёл до
  приёмки.
- Login shell ролей находил Python 3.14.8 вместо подготовленного 3.12.14, и
  обвязка отказывала с кодом 2. Роли запускали проектные команды без login shell
  и не меняли `PATH` и настройки. Отсюда предпосылка в разделе 2.
- Во второй задаче Coder на втором проходе по своим файлам (CENSOR) нашёл ошибку
  разбора длинного числового счётчика в XML. Он исправил разбор и
  отрицательные фикстуры и повторил полный прогон. Ранний снимок целевых файлов
  стал историческим, оба итоговых JUnit относятся к одному снимку.
- Автоматическая проверка действий Codex отклонила сброс dev-базы и копирование
  `.env.local`. Оба действия выполнили после прямого разрешения владельца в чате.
- Скилл работал в чате на модели чата; роли работали на моделях из проектного
  `.codex/`.

### Как шло обновление 28–29 октября

- Обновление тоже вёл агент Codex, с заранее подготовленными ответами и
  правилами остановки; в окне понадобились ответы О24–О26. Решения сверх
  подготовленного принимал владелец.
- Sibling взяли свежим клоном, без кэшей в `.tmp/`, поэтому Coder один раз
  выполнил `make setup` с сетью. Dev-базу перед проходом пересоздали пустой.
- Окно Manager было открыто 7 ч 41 мин. Трижды ход закончился ошибкой «Selected
  model is at capacity». Каждый раз по поручению владельца в том же окне писали
  «Продолжай», и Manager продолжал работу с теми же ролями.
- Architect заметил, что новый `AGENTS.md` различает два режима коммита, а
  корневой README говорил только о ручном. Владелец решил README в этом плане не
  менять, а тексты о двух режимах внести отдельным коммитом документации. Коммиты
  плана в окне Architect делал по прямому разрешению владельца на этот план (О24).
- Офлайн-тест `RepositoryContractTests.test_shared_bytes_and_no_process_override`
  из `scripts/test_sql.py` упал на первом прогоне Coder: он сравнивал общую часть
  восьми файлов правил с последним коммитом, а обновление изменило её в четырёх
  файлах. Роли исправили тест в этом же плане, до коммита, и `make test` прошёл
  74 теста. Но эта правка теста потеряла проверку общей части файлов; это нашли
  уже после закрытия плана. Проверку вернул четвёртый план 30 октября.
- Login shell ролей нашёл Python 3.15.2, а `Makefile` sibling вызывает голый
  `python3` (О7б), как и в первом проходе. Роли запускали `make` с временным
  префиксом `PATH` к Python 3.12. Владелец принял это задним числом и только для
  этого прохода. Пока он решал, первый запрос записи в `.git` около 4 ч ждал
  одобрения в окне. Решение владельца передали в окно, Architect дописал его в
  план ответом к Q2, и набор файлов пришлось подготовить заново.
- Codex CLI 0.165 на машине прохода не открыл окно через общий фоновый сервер
  Codex: ошибка `failed to load workspace requirements`, причина не установлена.
  Окно открыли в обход фонового сервера, с флагом Codex CLI `--no-daemon`; через
  Planveyor этот флаг не передаётся, у `planveyor sibling tui` флагов нет. Это
  исключение владельца для той среды, а не шаг руководства.

### Что осталось вне публичной истории

- **Ранняя попытка обновления.** 13–14 октября sibling уже обновляли: план
  `261013_1551_contract_upgrade_8c5256e_a9e83c4`, с `8c5256e7` на `a9e83c45`,
  дошёл до `Done`, его коммит — `fdc1a59`. Закрытие документов на нём
  остановилось: предложения по процессу пришли свободным текстом, закрытие
  перешло в `blocked`, а штатного повтора тогда не было. Из этой остановки
  выросли исправления движка, которые вошли в первую версию Planveyor. Попытку
  сохранили локально и не публиковали. Обновление 28–29 октября начали заново,
  со свежего клона от `9c445fd`, и перешли сразу на `66050258`.
- **Правка истории четвёртого плана.** Пока оператор прохода держал остановку,
  появился коммит `af9935dd`, а проверка нашла в новой строке плана ложное
  совпадение; его исправили коммитом `0cab865f`. Правка плана во время работы
  сменила его хэш. Поэтому после закрытия, по просьбе владельца, три коммита
  плана склеили в два — `783c208f` и `e5678978` — с теми же деревьями файлов.
  Прежние коммиты сохранены в локальной резервной ссылке Git и не публиковались.

## Приложение А. Банк ответов

Здесь собраны ответы на вопросы, которые роли задавали при настройке SQL Server
за пять проходов, ответы из обновления движка 28–29 октября (О24–О26) и несколько
ответов на случаи, которых в проходах не было: О16, О19, О21 и О23. Отправляйте
ответ, только если он совпадает с текущим вопросом и постановкой; если ваш стек
отличается, подставьте свои факты. Если роль
добавила неподтверждённое условие, верните ей конкретное расхождение. Вопрос о
границах задачи, правах или приёмке решает Owner.

Тексты начинаются словами «Отвечаю по поручению Owner»: так отвечает агент.
Отвечая сами, эти слова можно убрать. Номера О — нумерация этого приложения, у
ролей свои `Qn`. В проходе 11–12 октября понадобились только О20 и Т, в
обновлении 28–29 октября — О24, О25 и О26.

### Обсуждение адаптации

#### О1. Подтвердить «Как я понял задачу»

Только после сверки всего раздела и анкеты с фактами стека. В проходе Architect
этот вопрос не задал: развилок не было. Как попросить его задать вопрос, сказано
в разделе 6.

```text
Отвечаю по поручению Owner. Раздел «Как я понял задачу» и анкета прочитаны. Подтверждаю: sibling под SQL Server 2019 (compatibility 150); Northwind — только источник схемы; проекты и обвязка с целями make; импорт только схемы; один постоянный canary на реальную таблицу dbo.Products; корневой README.md и локальные секции восьми файлов правил. GetReorderCandidates — отдельный следующий план после закрытия документов адаптации и sibling ready. Подтверждаю переход в Architect draft. Это не разрешение на коммит.
```

#### О2. Назначение и первая полезная задача

```text
Отвечаю по поручению Owner. Sibling нужен, чтобы вести код базы данных на SQL Server 2019 по схеме Northwind: проекты, обвязка, проверки и правила ролей. Адаптация заканчивается одним постоянным тестом-canary: реальная таблица dbo.Products существует. Первая полезная задача — отдельный план после адаптации: процедура dbo.GetReorderCandidates, товары к дозаказу. Работает, если её восемь бизнес-тестов tSQLt и canary зелёные на dev-базе в самостоятельных прогонах Coder и Reviewer.
```

#### О3. Стек и версии

```text
Отвечаю по поручению Owner. SQL Server 2019, compatibility level 150. SDK-проекты Microsoft.Build.Sql 2.3.0 с Sql150DatabaseSchemaProvider. .NET SDK 10.0.401 в global.json с rollForward latestFeature, точное совпадение SDK не проверять. SqlPackage 170.5.96 — локальный dotnet tool. tSQLt.Dacpacs 1.0.8083.3529, DacpacName tSQLt.2019. go-sqlcmd с --encrypt-connection=mandatory -C -b. SQLFluff 3.4.2: tsql, raw, длина 120. Обвязка — Python 3.12, только стандартная библиотека. Возможности SQL Server 2022 и новее запрещены: Reviewer проверяет поиском (GREATEST, LEAST, DATETRUNC, DATE_BUCKET, GENERATE_SERIES, IS DISTINCT FROM, WINDOW, JSON_OBJECT, JSON_ARRAY и т. п.); TRIM(chars FROM s) допустим.
```

#### О4. Среда разработчика

```text
Отвечаю по поручению Owner. macOS. Уже стоят .NET SDK 10, go-sqlcmd и подготовленное окружение Python 3.12. make setup — его запускает Coder, нужна сеть — один раз восстанавливает локальный dotnet tool, пакеты обоих проектов и окружение SQLFluff в .tmp/. Кэши (DOTNET_CLI_HOME, NUGET_PACKAGES, временные файлы стека) тоже в .tmp/. Дальше сборка, lint, офлайн-тесты и проверка секретов работают без сети. Системные инструменты не устанавливать, HOME и настройки не менять.
```

#### О5. Живая цель и проверка цели

```text
Отвечаю по поручению Owner. Выделенную dev-базу и Northwind подготовил администратор; перед проходом dev-база пересоздана пустой. Логин не sysadmin: в dev-базе db_owner, в Northwind только чтение (db_datareader, VIEW DEFINITION, SELECT на sys.sql_expression_dependencies). Перед каждой публикацией обвязка заново проверяет цель одним запросом: имя базы совпадает с настроенным, свойство planveyor.designated_dev есть, логин не sysadmin. Иначе код 3 и ни одной публикации. Обвязка печатает имя базы и логин, адрес сервера и пароль — никогда. Роли не меняют сервер, логины, CLR и маркер.
```

#### О5б. Наличие маркера или конкретное значение, например `value=1`

```text
Отвечаю по поручению Owner. Только наличие свойства: EXISTS в sys.extended_properties WHERE class = 0 AND name = N'planveyor.designated_dev'. Значение задаёт администратор, обвязка его не читает; value=1 не вводить.
```

#### О6. Секреты и подключение

```text
Отвечаю по поручению Owner. Параметры подключения — в .env.local в корне sibling: права 0600, файл в .gitignore и не отслеживается. Ключи: SQLCMDSERVER, SQLCMDDBNAME, SQLCMDUSER, SQLCMDPASSWORD. Файл уже положен. Значения читает только обвязка, роли файл не открывают. Пароль для sqlcmd — только через переменную окружения; SqlPackage получает его аргументом, для однопользовательского Mac это принято. Адрес сервера, пароль и имя хоста вычищаются из любого показываемого вывода и из JUnit; check-secrets печатает только пути.
```

#### О7. Цели `make` и коды выхода

```text
Отвечаю по поручению Owner. Набор целей и коды выхода — как в фактах стека, пункт 8. make возвращает свой код; обвязка печатает собственный код и категорию; роль фиксирует оба.
```

#### О7б. Нужна ли отдельная офлайн-цель для `scripts/test_sql.py`

```text
Отвечаю по поручению Owner. Да: make test запускает офлайн-тесты scripts/test_sql.py без сети и живой базы. Анкету и план синхронизировать, реализация — за Coder.
```

В этом sibling `Makefile` вызывает голый `python3`; переменной `PYBIN`, как у
движка, в нём нет.

#### О8. Доказательство для ревью

```text
Отвечаю по поручению Owner. JUnit от tSQLt.XmlResultFormatter в docs/code_reviews/assets/<plan-stem>/: у Coder <name>.junit.xml, у Reviewer свой прогон на ревьюируемых байтах — <name>.review.junit.xml. Путь обязателен, относительный, .xml, внутри проекта, без symlink; отслеживаемый Git файл или неизвестный ответ Git — отказ до удаления, сборки и SQL; новый XML пишется атомарно. Роль, запустившая проверку, пишет в Evidence команду, коды выхода, HEAD, bundle_sha256, путь и SHA-256 JUnit, tests/failures/errors/skipped и имена testcase. Старые отчёты не принимаются. В документах только относительные пути и make <цель>.
```

#### О9. Правила ролей

```text
Отвечаю по поручению Owner. Architect: сервер, логины и маркер — вне scope ролей; поведение доказывается тестами tSQLt и живым прогоном. Planner: в шагах только цели make; каждый критерий приёмки называет свой тест. Coder: имена со схемой, SET NOCOUNT ON, без SELECT * в результатах, однозначный ORDER BY; приведение к int до арифметики над smallint; XACT_ABORT и THROW при транзакции; класс tSQLt — CREATE SCHEMA и сразу свойство tSQLt.TestClass, без NewTestClass; бизнес-тесты — FakeTable или ApplyConstraint и литеральные ожидания, без COMMIT и ROLLBACK; Imported меняет только Extract. Reviewer: свои офлайн-проверки и самостоятельный db-proof на ревьюируемых байтах со своим JUnit; db-state — отдельное чтение состояния, не замена proof; прогоны Coder и Reviewer последовательные. Поиск возможностей SQL Server 2022 даёт rc 1; в диффе нет пароля, адреса сервера и абсолютных путей. README и локальные секции постоянны: без имён текущего плана и личных путей.
```

#### О10. Кто запускает живые цели

```text
Отвечаю по поручению Owner. Вариант А: роли в существующей песочнице Codex с уже включённой сетью, только цели make. setup и db-extract — Coder; db-proof — Coder и независимо Reviewer, каждый со своим JUnit; db-state — Architect и Reviewer. Codex home, сеть и согласованную конфигурацию моделей ролей не менять; реальный отказ фиксировать, старым зелёным результатом не подменять.
```

#### О11. Что вне объёма

```text
Отвечаю по поручению Owner. Вне объёма: CI; Linux и Windows; другие версии SQL Server; production и бизнес-данные; данные Northwind в проекте, только схема; сервер, логины, CLR и маркер; правка движка Planveyor; публикация и push; производительность и планы выполнения. GetReorderCandidates — отдельный следующий план.
```

### Во время работы ролей

#### О12. Какой Python использовать

Так спрашивал Coder, когда `make setup` нашёл Python 3.14 вместо 3.12.

```text
Отвечаю по поручению Owner. Уже подготовленное окружение Python 3.12: его каталог bin стоит первым в PATH процесса, команды остаются make <цель>. Если login shell находит другой Python, запускайте команды без login shell. Python не устанавливать; HOME, shell и конфиг Codex не менять; личные пути в документы не записывать.
```

В обновлении 28–29 октября роли вместо запуска без login shell ставили перед
`make` временный префикс `PATH` к Python 3.12, и владелец принял это задним
числом и только для того прохода. Надёжнее заранее поставить Python 3.12 первым
и в login shell (раздел 2).

#### О13. Extract вернул `CREATE USER` или файлы безопасности

```text
Отвечаю по поручению Owner. ExtractTarget не менять: SchemaObjectType во временный каталог, файлы из каталогов безопасности удаляются целиком, остаточные CREATE USER, ALTER ROLE, GRANT или INSERT дают отказ, и старый Imported остаётся. SQL руками не править. Это решение уже в фактах стека, пункт 5; новое согласование не нужно.
```

#### О14. Одночастные имена в выгрузке

```text
Отвечаю по поручению Owner. Имена в Imported не разбирать и не переписывать: одночастное имя (например, CustOrderHist) относится к dbo. Если сборке нужно явно — DefaultSchema=dbo в обоих проектах.
```

#### О15. Как запускать тесты и получать JUnit

```text
Отвечаю по поручению Owner. EXEC tSQLt.RunAll; без параметров, затем EXEC tSQLt.XmlResultFormatter;, вывод XML — через sqlcmd с -h -1 -y 0 -w 65535. Постоянный formatter не менять, временную смену formatter и внешнюю транзакцию не вводить. Это факт стека, пункт 7.
```

#### О16. Параметры публикации

```text
Отвечаю по поручению Owner. Флаги как в фактах стека, пункт 6. DropObjectsNotInSource=True на проверенной dev-базе удаляет объекты, которых нет в публикуемом проекте, с учётом исключённых типов: пользователи, логины, членство в ролях и права не трогаются. DropExtendedPropertiesNotInSource=False сохраняет маркер.
```

#### О17. Переделать обвязку по-другому или «лучше»

```text
Отвечаю по поручению Owner. Нет: сохраняем решения из фактов стека и уже работающие части. Новое проектирование — только при доказанном отказе текущего способа, с причиной в плане.
```

#### О18. Открытая запись follow-up по той же теме

```text
Отвечаю по поручению Owner. Сослаться на source_ref#item_id в Context links, запись оставить без изменений. Продвижение записи не условие этого плана.
```

#### О19. Внешние модели или MCP как часть процесса

```text
Отвечаю по поручению Owner. Нет: процесс использует только штатные средства Planveyor. Требование внешних моделей и их квитанций снимается.
```

#### О21. Скилл спрашивает путь к движку Planveyor

Ответ — путь вашей копии Planveyor, тот же, что в `PLANVEYOR_RUNTIME_ROOT` из
раздела 2. В публичные планы и правила он не записывается.

```text
<каталог копии Planveyor>
```

#### О22. Лишние наборы тестов или чужие объекты в dev-базе

Такие вопросы возникали, когда в dev-базе оставались объекты прошлых прогонов.
Это остановка из раздела 11: dev-базу пересоздаёт администратор.

```text
Отвечаю по поручению Owner. Лишний набор тестов не принимать и не отфильтровывать: приёмка требует точного числа testcase. Такие наборы остаются от прошлых прогонов. Publish с DropObjectsNotInSource=True удаляет из проверенной dev-базы объекты, которых нет в проекте; этот флаг не менять, объекты руками не удалять. Если лишнее остаётся и после публикации, это остановка: dev-базу пересоздаст администратор.
```

#### О23. Роль просит разрешить коммит

Ответ для ручного режима в консоли. В режиме TUI коммиты делает Architect по
разрешению О24.

```text
Отвечаю по поручению Owner. Роли коммит не делают. Коммит выполняет только planveyor sibling close --commit после просмотра close с прочитанным набором файлов и сообщением. Push и публикация вне задачи.
```

### Вторая задача

#### О20. Подтвердить постановку `GetReorderCandidates`

Понадобился в проходе. Отправляйте только после сверки раздела «Как я понял
задачу» с поручением.

```text
Отвечаю по поручению Owner. Подтверждаю раздел «Как я понял задачу»: читающая процедура dbo.GetReorderCandidates без параметров; только Discontinued = 0 и Shortage = ReorderLevel - (UnitsInStock + UnitsOnOrder) > 0; числовые NULL = 0; приведение к int до арифметики; колонки ProductID int, ProductName nvarchar(40), Shortage int; сортировка по ProductID. Восемь бизнес-тестов:
T1 — пустая Products, пустой результат;
T2 — активный товар 10/4/2, Shortage 4;
T3 — нулевой и отрицательный дефицит не попадают;
T4 — дефицит, покрытый заказами в пути, не попадает;
T5 — снятый с продажи товар с дефицитом исключён;
T6 — NULL в каждом числовом поле и их сочетаниях; NULL порога не создаёт кандидата;
T7 — ReorderLevel 32767 и оба остатка 32767 — без переполнения;
T8 — контракт результата: типы, порядок колонок, сортировка по ProductID.
Девятый — постоянный canary. Coder и Reviewer — самостоятельные последовательные прогоны, каждый со своим JUnit: девять testcase, ноль failures, errors и skipped. Подтверждаю переход в Architect draft. Это не разрешение на коммит.
```

### Режим TUI и обновление движка

#### О24. Коммиты Architect в окне Manager

Разрешение Owner для конкретного плана: по правилу этого sibling без него
Architect в окне не коммитит (раздел 7). Этот текст агент отправляет только по
вашему прямому разрешению для этого плана; без него вопрос о коммитах
возвращается вам. Этот ответ понадобился в обновлении.

```text
Отвечаю по поручению Owner. Для этого плана Owner прямо разрешает Architect выполнить семантический коммит после Arch Review и необходимый коммит закрытия документов в том же окне Manager (native_existing). Одобряются только предусмотренные этим решением запросы записи в .git, каждый разовым выбором в окне; постоянных разрешений и push нет.
```

#### О25. Подтвердить план обновления движка

Понадобился в обновлении как ответ на Q1. Подставьте версии из имени своего
плана. В обновлении ответ содержал ещё ограничение: README в том плане не
менять, тексты о двух режимах коммита — отдельным коммитом документации. Теперь
эти тексты в README уже есть.

```text
Отвечаю по поручению Owner. Подтверждаю адаптацию <старая версия> → <новая версия> и переход в Architect draft. Принять доставленный контракт, сохранить стек, девять testcase и локальные секции восьми файлов правил и README, выполнить текущие офлайн-проверки и два последовательных независимых SQL proof Coder/Reviewer. Новых изменений обвязки, SQL-кода, тестов и документов sibling без доказанной поломки от обновления нет.
```

#### О26. `make setup` в свежем клоне

Понадобился в обновлении как ответ на Q2: Architect спрашивал, можно ли
восстановить кэши через `make setup`.

```text
Отвечаю по поручению Owner. Это свежий клон без кэшей .tmp (venv, dotnet, nuget), поэтому Coder один раз выполняет make setup с сетью. Правило анкеты «Reset/init/env-copy/model-install не повторяются» этим не нарушается: make setup в этом клоне ещё не выполнялся. Dev-базу Owner пересоздаёт, а .env.local кладёт до прохода; роли этого не повторяют.
```

### Технический вопрос

#### Т. Технический вопрос по обвязке: API, формат, сборка, разбор вывода

Понадобился в проходе.

```text
Отвечаю по поручению Owner. Это технический вопрос обвязки, а не решение владельца: исправьте по документации инструмента и фактам стека из анкеты, не меняя Scope, права и приёмку. Если исправление требует изменить что-то из этого — верните вопрос с вариантами.
```

В проходе О20 подтвердил постановку второй задачи, а Т ответил на её
техническую часть: адаптацию существующей обвязки под девять тестов. Оба текста
ушли одним ответом на вопрос Q1.

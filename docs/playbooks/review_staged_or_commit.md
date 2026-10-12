# Playbook: Code review — staged/current or single commit

Шаблон отчёта: `docs/code_reviews/_template_single_commit.md`.

Это не роль проекта, а плейбук для ревью одного declared commit/current
bundle. Роль Reviewer и обязательный старт задаёт выбранный role/profile source.
Общий процесс не предполагает конкретный язык, framework, UI toolkit, data
store или test runner.

Выбор шаблона и владение:

- общий шаблон по умолчанию находится в
  `docs/code_reviews/_template_single_commit.md`;
- optional repo-profile override находится в
  `docs/code_reviews/profiles/<repo_profile>/_template_single_commit.md`;
- repo-local mirrored defaults не становятся вторым каноном и не должны
  неявно создавать новый review artifact.

## Режим

Ты — строгий и объективный code reviewer. Анализируй только declared target и
фиксируй только problems. Для каждой finding объясни why и дай конкретную
краткую рекомендацию. Пиши по-русски, деловым тоном; английский оставляй для
команд, путей, кода и literal error strings.

- Review artifact Russian-first: heading, first summary line и prose в секциях
  по-русски. Legacy English headings не переименовывай только ради churn.
- Architect later дописывает `Архитектурное ревью` либо сохраняет `Arch review`;
  это не отменяет reviewer findings.
- Не придумывай facts, hidden scope или проверки: отсутствие declared harness
  — gap с owner/next step, не разрешение применить привычную продуктовую команду.

## Interim review contract

Один review-file может быть создан до visual review и жить через обе
reviewer-фазы. До закрытия visual lane допустим только interim status
`Черновик`. Если обязательный visual/runtime proof блокируется, тот же файл
получает `❌ S1 blocker(ы)` с причиной в `## Визуальные доказательства`.
Не создавай второй side-file и не вводи `BLOCKED`, `PARTIAL`, `FROZEN` или
`PAUSED` header statuses.

## Вход

- `COMMIT`: `<hash|current|staged|current bundle|staged bundle>`;
- `SPEC` (optional): source path, URL или heading;
- выбранный project/profile canon, Context links и declared validation harness.

Если `PLAN_PATH` уже есть, `current bundle`/`staged bundle` означают bounded
review explicit plan bundle. Dirty files вне bundle не являются blocker.

## Процесс

1. Получи diff:
   - `current`/`working`/`changed`: `git diff HEAD --patch --find-renames --find-copies --stat`;
   - `staged`: `git diff --staged --patch --find-renames --find-copies --stat`;
   - `current bundle`/`staged bundle`: сначала `planveyor_plan_bundle --check <PLAN_PATH>`, затем соответствующий diff с explicit bundle paths;
   - literal hash: `git show --patch --find-renames --find-copies --stat <COMMIT>`.
2. Зафиксируй short target id: first seven hash characters либо `current`,
   `staged`, `current_bundle` или `staged_bundle`; время artifact —
   `YYMMDD_HHMM` в declared local timezone.
3. Прочитай SPEC, plan и Context links. Сверь actual change с declared
   behavior, acceptance criteria, data/ownership constraints и current bundle.
4. Сначала проверь truth conditions:
   - live object/user/account/state требует repo-backed discovery или
     deterministic seed; historical placeholder не является live proof;
   - fixed HTML chunk или global string search — debug signal, а не verdict для
     shared fragment; используй declared DOM/subtree/anchor evidence;
   - красный helper при зелёном live path требует классификации `harness drift`
     versus `product regression` до открытия runtime/product scope.
5. Оформи только findings: `S1 Blocker`, `S2 Risk`, `S3 Nit` и follow-ups.
   Каждая finding содержит `file:line`, impact, evidence и concrete remedy.
6. Создай `docs/code_reviews/YYMMDD_HHMM_<SHORT>.md` по selected template.

## Checklist

Выбирай checks из объявленного project/profile canon и затронутых surfaces. Не
переноси framework, browser, database или transport requirements одного проекта в
другой по умолчанию.

- **Correctness and contracts:** входы/выходы, data invariants, error paths,
  concurrency/idempotency, access/scope и backwards compatibility, когда их
  затронул diff.
- **Security and privacy:** authorization, validation, secret/PII handling,
  external input and logging only where target contract makes them relevant.
- **Maintainability:** duplicated logic, hidden configuration, unstable
  coupling, missing tests and conflicts with existing abstractions.
- **UI/runtime:** semantic markup, accessibility, state transitions and visual
  behavior только если changed paths и declared harness подтверждают runtime
  UI. Выполни `docs/playbooks/post_merge_visual_review.md` как overlay, если
  visual lane required.
- **Integration and operations:** signatures, retry/timeout/idempotency,
  migration or deployment checks только по explicit contract. A command is
  runnable only when target profile/materialized plan declares its interpreter,
  environment and expected result.
- **Compatibility profile (если target его объявил):** apply only its explicitly
  declared checks, receipts and smoke scenarios. They remain named compatibility
  contracts, not universal reviewer defaults.

## Visual reviewability

Основная visual lane, launcher и receipt берутся из selected profile или plan.
Версионированный repo-local launcher может быть primary только когда это
объявлено contract и его literal copy-paste command находится в
`### How to run (Reviewer)`. Ad-hoc automation, inline run-code и
`.tmp/*_flow.js` — reviewability gap, а не замена. Required runner receipt без
объявленного supported status доказывает лишь current-host behavior.

Для каждого required screenshot используй assets под current review basename,
назови state и добавь `Proves:`. Historical assets, baseline-update commands и
несвязанные `.tmp/**` outputs остаются только diagnostics. Green helper никогда
не делает неподтверждённую contextual lane зелёной.

## Формат результата

Отчёт называет exact target, reviewed paths, source refs, commands/results,
current evidence и findings. Historical green report не является fresh proof
для current bytes. Если нужна правка, направь её в bounded follow-up;
review-only artifact не materialize-ит implementation scope неявно.

Создавай artifact по выбранному template без удаления required header,
dual-lane/synthesis, severity, exact-bundle hygiene, required visual-evidence
и Architect handoff sections. Template задаёт machine-consumed report grammar;
общий playbook не разрешает заменить её свободным prose. Same-contract rerun
обновляет тот же live artifact, а новый path требует real scope expansion или
independent contract.

## Данные для анализа (optional transport input)

<<SPEC_TEXT>>
$SPEC_TEXT
<<END_SPEC_TEXT>>

<<DIFF>>
$DIFF
<<END_DIFF>>

Если вызывающая сторона не materialize-ила один из blocks, это означает
отсутствие input, а не разрешение реконструировать историю или другой profile.

## Как заполнять локальные секции sibling

Две секции ниже имеют стабильные заголовки и initial fields. После
`planveyor_consumer_init` их тело принадлежит sibling: внесите target-local
команды, данные, критерии и proof только для этой фазы. Общие lifecycle
правила, статусы и authority остаются вне секций; изменение формата требует
отдельной явной адаптации, а не обычного upgrade.

При обновлении sibling укажи в локальном плане адаптации оба source commit и проверь сохранность bytes локальных секций до и после Copier.

## Локальные правила стека

- SQL review проверяет current offline gates и independent Reviewer proof по make целям, отдельный relative.review.xml и db-state. Проверка staging/commit сама SQL не запускает и не даёт server authority. При изменении review target bytes прежний SQL proof stale.
- SQL Server 2019, compatibility 150; Northwind — только readonly источник схемы. Запись разрешена только в отдельную назначенную dev-базу. Сервер, базы, логины, CLR и маркер planveyor.designated_dev готовит администратор; роли их не меняют.
- Проектные команды — только make из корня sibling. Python 3.12 из подготовленного PATH; SDK 10.0.401/latestFeature, SqlPackage 170.5.96, Microsoft.Build.Sql 2.3.0, tSQLt.Dacpacs 1.0.8083.3529/tSQLt.2019, SQLFluff 3.4.2/tsql/raw/120. Зависимости и build/cache — только .tmp; после setup offline цели ничего не восстанавливают.
- .env.local: regular/non-symlink, 0600, ignored/untracked; SQLCMDSERVER, SQLCMDDBNAME, SQLCMDUSER, SQLCMDPASSWORD читает только scripts/sql.py. Роли значения не читают. Пароль sqlcmd — environment, SqlPackage — принятый аргумент; raw streams/argv/ошибки/сведения сервера не публикуются.
- Publish требует непосредственно предшествующий свежий one-query guard: DB_NAME совпадает с настройкой, database-level marker существует без чтения значения, sysadmin=0. Northwind case/padding variants запрещены. Отказ цели — 3 без Publish; недостающие права не исправляют серверными изменениями.
- db-proof требует relative .xml JUNIT внутри проекта без symlink, достоверно Git-untracked. Path/Git/config отказ до удаления/build/SQL; допустимый old XML удалён до сборки. RunAll без параметров, затем unchanged XmlResultFormatter; go-sqlcmd --encrypt-connection=mandatory -C -b, XML -h -1 -y 0 -w 65535. Новый очищенный JUnit записывается атомарно; старый XML/текст успеха не доказательство.
- Коды обвязки: 0 success, 1 test/JUnit, 2 config/path/Git/secrets/invalid Extract, 3 target, 4 connection/read SQL, 5 build/lint/Extract artifact, 6 Publish. Код make фиксируется отдельно; auto-retry SQL нет.
- Evidence: portable make command, коды make/обвязки, HEAD, canonical bundle_sha256 до/после proof, relative JUnit path/SHA-256, counts/testcase. Coder и Reviewer последовательно получают разные JUnit: каждый содержит полный точный набор текущего согласованного плана и обязательный real-table canary StackAdaptationTests.[test Products table exists], failures/errors/skipped=0. Missing/unknown/duplicate identities, несогласованные suite/root counters и любой red testcase дают отказ 1; зелёные totals не перекрывают красный XML. Исторические 1/0/0/0 относятся только к завершению адаптации. db-state contextual-only. Любые target edits после proof требуют нового snapshot/proof.

- Git lookup JUNIT literal: pathspec magic/пробелы/metacharacters не являются pattern. Ambient GIT_DIR/GIT_WORK_TREE/GIT_COMMON_DIR/GIT_INDEX_FILE, даже пустые, дают operational-red отказ 2 до JUNIT/config/deletion/build/SQL; обвязка не сбрасывает overrides и не выбирает другой index.

## Разрешённое локальное переопределение процесса

- Переопределение: N/A (why=no local override)
- Причина и эквивалентный proof: N/A (why=no local override)

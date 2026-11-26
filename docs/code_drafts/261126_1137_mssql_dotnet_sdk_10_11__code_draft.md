# Code draft: Поддержать .NET SDK 10 и 11 в MSSQL sibling

**Date:** 2026-11-26 13:58 +0300
**Cluster:** infra
**Related plan:** `docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md`
**Author role:** Planner
**Status:** draft

**Handoff gate:** Q2 закрыт Architect A2/CLOSED. После обычного `Ready for Coder -> Coder intake` сначала допустим только описанный SDK-independent source/fixtures/static этап. Каждая последующая SDK-dependent команда требует собственных actual inputs; их отсутствие останавливает её до запуска и возвращает Architect. Наличие SDK, прохождение matrix и SQL этим handoff не подтверждаются.

## Meta (machine-readable JSON)

```json
{
  "code_draft_meta": {
    "plan": "docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md",
    "cluster": "infra",
    "targets": [
      {"path": "global.json", "kind": "config"},
      {"path": "scripts/sql.py", "kind": "py"},
      {"path": "scripts/test_sql.py", "kind": "py"},
      {"path": "README.md", "kind": "doc"},
      {"path": "docs/tools/prompts/architect_status_driven.md", "kind": "doc"},
      {"path": "docs/tools/prompts/planner_status_driven.md", "kind": "doc"},
      {"path": "docs/tools/prompts/coder_status_driven.md", "kind": "doc"},
      {"path": "docs/tools/prompts/coder_migrations_gate.md", "kind": "doc"},
      {"path": "docs/tools/prompts/reviewer_status_driven.md", "kind": "doc"},
      {"path": "docs/playbooks/review_staged_or_commit.md", "kind": "doc"},
      {"path": "docs/playbooks/review_merge_range.md", "kind": "doc"},
      {"path": "docs/playbooks/post_merge_audit.md", "kind": "doc"}
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

- Source plan provenance: `reuse PLAN_PATH carrier unless this draft is created/imported/backfilled separately`
- Relation: `created-here`
- Thread ID: `<REDACTED>`
- Parent thread ID: `N/A (why=not exposed by env, wrapper receipts, or session stats)`
- Session SID: `N/A (why=.planveyor.session.planner is missing or empty)`
- Launch surface: `unknown (why=no env, wrapper receipt, or session stats origin identified the launch surface)`
- Captured from: `env`
- Captured at: `2026-11-26T11:33:51Z`

Поля получены `planveyor_plan_provenance_context --section code-draft --session-key planner` через выбранный facade. Origin plan, этот draft, единственный review и его explicit assets входят в final bundle отдельно от 12 implementation targets. N-A ref получен из validated oracle/helper; semantic core не меняется. `Context source` описывает исполнение, этот блок — происхождение.

## Purpose

Реализовать принятый SDK-контракт и точную миграцию восьми SDK-фраз. Сделать различимыми synthetic filter tests, real resolver checks, три Coder preparations, два независимых SQL proof и их будущие разрешения.

## Reviewability preflight receipt

- `proof-path class`: standard primitives — существующие make harness, dotnet resolver, canonical snapshot и strict JUnit; новый checked-in product launcher/helper не создаётся. Transient lookup-only fixtures объявлены отдельно для static lane.
- `mandatory primary lane`: один 12-target snapshot; Coder preparation №1/current-root/SDK10 и №2/offline-copy/SDK11 с полными offline goals; после отдельного SQL approval Coder SDK10 proof, preparation №3/current-root/SDK11, затем Reviewer SDK11 offline и независимый proof без setup.
- `mandatory non-primary carrier / contextual lane`: actual combined10+11→10 на неизменном candidate, отсутствие подходящей10→11 и scoped no-compatible fixture; immutable SDK11 negative launcher без runtime10 и фактический missing-framework `/Version`; оба local-tail callers, все восемь новых фраз и pinned shared-prefix guard. SDK10 row может использовать тот же combined root; only10 inventory не обязателен.
- `exact helper path + support files`: `Makefile`, `global.json`, `scripts/sql.py`, `scripts/test_sql.py`, `.config/dotnet-tools.json`, `NuGet.Config`, `Directory.Build.props`; snapshot producer — source-owned `scripts/review_target_snapshot.py` через public `planveyor_review_target_snapshot`.
- `dependent tests / dependent docs / known consumer paths`: `ConfigTests`, `LocalContractAssertions`, `PinnedSourceContractTests.test_local_tails_match_head_and_guards`, `RepositoryContractTests.test_shared_bytes_and_no_process_override`, `PinnedSourceRegressionTests`; `README.md` и восемь literal doc targets из Meta. SDK-фильтр использует `Stack.setup/build/proof/extract`, но Extract здесь не исполняется; Makefile и остальные manifests — read-only baseline.
- `consumer contract semantics`: прежний SDK refusal `code=2, phase=environment, reason=sdk-version`; ошибка resolver сохраняет `command-failed/timeout`. Runtime `/Version` — operator precondition со своим actual rc, а не новый guard или код обвязки. Generic comparator допускает equality, отдельный current inventory требует миграции всех восьми файлов.
- `preconditions / seed-discovery`: source edits не требуют SDK selectors; static make goals имеют отдельные Python3.12/Darwin/Git/pinned-runtime/synthetic-lookup prerequisites. Runtime inputs проверяются только перед зависимым шагом. Coder — `discovery-or-seed` preparations №1–№3; Reviewer — `receipt-reuse-only` для preparation №3 и двух исходных rows. Потеря receipt continuity — stop, без silent reseed, переноса кеша или другого launcher.
- `stable identity / observer boundary`: captured HEAD, canonical bundle_sha256 и exact target paths одинаковы во всех rows и до/после proof. Physical root, launcher identity, SDK, manifests и cache provenance связываются с номером preparation. Closure SQL — следующий свежий atomic XML того же прогона с девятью exact identities; `notice/success text != mutation truth`.
- `runtime-lineage preflight`: до setup проверяются actual launcher/project Python/SDK/runtime; local cache и SqlPackage этого root проверяются после его успешного назначенного setup, а не как предусловие создания кеша. Positive `/Version` и два DACPAC завершают row. Перед SQL proof повторяются SDK/runtime/cache-lineage/SqlPackage checks. Negative launcher — тот же immutable SDK11, runtime10 отсутствует; его red не является SQL readiness.
- `receipt retention`: `.tmp/sdk-compat-261126/` — transient local sanity only, включая private roots, raw logs и receipts; один review и два очищенных XML в `docs/code_reviews/assets/261126_1137_mssql_dotnet_sdk_10_11/` — durable operator/review evidence. Сырые receipts не копируются в Git.
- `reroute rule`: missing prerequisite блокирует соответствующий зависимый шаг, не самостоятельные source edits. Coder записывает уже выполненный SDK-independent prefix и exact missing input, затем возвращает Architect до dependent command. Отказ/unknown outcome, drift или отсутствие approval — stop без SQL/setup retry. Static success не разрешает SQL-approval request или Ready for Review без двух полных rows и required real/negative proof. Новые implementation targets требуют reroute.
- `perceptual truth-source split`: структурный readback, bytes и XML; UI, OCR, template/pixel matching и image fallback — N/A (why=CLI-only contract).
- `receipt schema emitter inventory`: N/A (why=формат authority/receipt/parser не меняется).
- `truth-host fixture matrix`: N/A (why=не меняется fan-in/readback helper authoritative truth hosts).
- `Manager command-surface fan-out`: N/A (why=Manager commands и dispatch path не меняются).
- `API/payload field parity`: N/A (why=API/payload schema не меняется).

## Targeted changes (by file)

1. `global.json`: sdk object ровно `version=10.0.401`, `rollForward=major`, `allowPrerelease=false`; никаких `paths` в product config.
2. `scripts/sql.py::Stack.tools`: stable `10.0.x>=401` и `11.0.x>=100`, только minor0. Сохраняются platform/Python/tool/rc и все SQL/config/JUnit guards; runtime-check сюда не добавляется.
3. `scripts/test_sql.py`: SDK cases, exact config assertion, literal local-tail bridge, оба callers и current eight-file inventory; real make regression/52-case operational matrix сохраняются. Реализацию выбирает Coder внутри этих invariants.
4. `README.md::Среда и зависимости`: единый SDK/runtime контракт, предпочтение10/fallback11, prerelease/future отказ, prepared macOS ARM64 и runtime10.0.11+ для pinned SqlPackage. Версии пакетов не меняются.
5. Все восемь doc paths из Meta: ровно один literal `SDK 10.0.401/latestFeature` → `SDK — по README.md («Среда и зависимости»)` внутри local stack section. Остальные local bytes до EOF, disabled override и source-owned prefixes побайтно сохраняются. `docs/stack_brief.md` — historical input, read-only.

## Tests / fixtures

### SDK-filter fixtures в `ConfigTests`

При valid Python3.12/Darwin/which через существующий `FakeExecutor.overrides['version']`:

- Положительные: `10.0.401`, `10.0.404`, `11.0.100`, `11.0.101`, обычный trailing newline.
- Неподдерживаемые: `10.0.100`, `10.0.400`, `11.0.99`, `9.0.401`, `10.1.401`, `11.1.100`, `12.0.100`.
- Prerelease/malformed: `10.0.401-preview.1`, `11.0.100-rc.1`, `11.0.100+metadata`, empty, `garbage`, `11.0`, `11.0.100.1`, две строки версий.
- Проверять code/phase/reason, чтобы ранний `python-or-platform` не дал ложный green. Existing command-failed/timeout/redaction fixtures сохраняются; synthetic version output не закрывает real resolver.

### Local-tail fixtures и оба callers

На каждом из восьми `LOCAL_FILES` comparator принимает old→old equality, единственный old→new и new→new equality. Bridge требует baseline old=1/new=0, current old=0/new=1 и полное равенство literal replacement; обратный переход запрещён. Все guards исполняются после сравнения и для equality, без early return.

Negative fixtures: baseline old=0/2, current new=2, old+new вместе, partial wording, new→old, SDK replacement плюс другой byte/EOF change, path вне восьми, malformed/missing/duplicate/reversed headings, invalid UTF-8, forbidden wording, effective override. Bridged unsafe tails также отказывают. Existing AC8-N1…N7 и shared-prefix mutations сохраняются.

Отдельный current inventory assertion проверяет ровно 8 paths, old=0/new=1 в каждом current local tail. Fixture семь new/один old обязательно red, хотя generic comparator принимает equality старого файла. Проверить оба live callers при полном переходе и после committed new baseline, а не только comparator unit.

В `PinnedSourceRegressionTests.setUp` synthetic tail получает old SDK phrase; fixture suite явно упражняет оба callers и current inventory. Согласовать literal child-test count и full failure IDs в `fixture_make`; не расширять импортом всего `RepositoryContractTests` с чужими SQL/project prerequisites. Existing 52-case operational matrix и bounded deadlines остаются.

## Steps

1. После обычного Coder intake реализовать изменения только 12 exact targets и fixtures. Начало source/docs edits не зависит от SDK inputs; установка/SDK diagnostics/setup/SQL на этом этапе не выполняются.
2. Через отдельный static envelope ниже проверить actual project Python3.12/Darwin/Git/pinned runtime и выполнить `make test`, `make check-secrets`; выполнить plan/doc checks и `git diff --check`. Missing static prerequisite отмечает зависимый test как не выполненный; прочие выполненные независимые checks сохраняются. Source/static success не считается SDK acceptance.
3. До первого SDK-dependent шага проверить переданные inputs именно этого шага. Missing input — конкретный blocker к Architect с результатом prefix; не устанавливать/не искать SDK и не переоткрывать абстрактный Q2.
4. На итоговых implementation bytes зафиксировать snapshot, подготовить exact Git-копию без credentials/cache, выполнить preparations №1/№2 и обе полные offline rows. SDK10 root вправе быть combined10+11; mandatory actual combined diagnostic связывается с тем же launcher/root либо с отдельно предоставленным уже готовым combined root.
5. После required real resolver/negative-runtime proof и двух green rows вернуться Architect за отдельным SQL approval. Preparation №3 на этом запросе ещё planned.
6. Только после approval: Coder SDK10 proof в current sibling → Coder preparation №3/current SDK11/full offline → Reviewer независимый SDK11 offline без setup и собственный proof. Сохранить snapshot/receipt continuity и два разных JUnit.
7. Ready for Review/acceptance и конкретный local commit имеют прежние отдельные gates; никакого автоматического stage/Done/commit/push.

## Commands / private prerequisites

Все команды ниже — для Coder/Reviewer на указанной стадии; Planner не исполняет project tests/SDK/setup/SQL. Engine `PYBIN` используется только public Planveyor facade и в project recipes не переносится. Для static stage выбран уже существующий project-local Python, проверяемый отдельно; runtime stage использует собственный prepared project-Python selector. Единственный контракт SDK inputs — symbolic `MSSQL_*` ниже; `SDK_COMPAT_*` не является автоматическим alias/mapping. Private values передаются в launch context без записи абсолютных путей в Git.

| Переменная | Проверяемое значение |
| --- | --- |
| `MSSQL_STATIC_PYTHON_BIN` | для static stage только существующий `$PWD/.tmp/venv/bin`, actual Python3.12/Darwin проверяется перед make; среда не создаётся/не меняется |
| `MSSQL_PYTHON312_BIN` | для runtime stage отдельно подготовленный каталог с `python3` версии3.12; при setup interpreter не должен принадлежать перезаписываемой row/.tmp/venv |
| `MSSQL_DOTNET10_ROOT` | prepared ARM64 root; resolver в candidate выбирает10; root вправе уже содержать обе подходящие ветки10+11 |
| `MSSQL_DOTNET11_ROOT` | prepared ARM64 root с только SDK11 и runtime10.0.11+ |
| `MSSQL_DOTNET_BOTH_ROOT` | нужен только если actual SDK10 root не combined; уже coinstalled10+11 diagnostic input, без setup. Если SDK10 root combined, повторный selector не запрашивается; оба uses связываются с одной physical identity |
| `MSSQL_DOTNET11_NORT10_ROOT` | immutable root с той же SDK11, без Microsoft.NETCore.App10; diagnostic-only |
| `PLANVEYOR_RUNTIME_ROOT` | тот же выбранный trusted runtime/source pin |

Каждый selector требуется только перед его dependent command. До SDK/setup — physical regular executable, actual root/list-sdks/list-runtimes и project Python3.12 без чтения `.env.local`. Missing input возвращается Architect после сохранения independent prefix; поиска по диску, сборки root, symlink layout, установки/удаления runtime нет. macOS/arch — `sw_vers -productVersion`/`uname -m`, supported pair по Microsoft link плана. Read-only Planner проверил только existing project `.tmp/venv/bin/python3`: Python3.12.14/Darwin/arm64 и executable resolved regular file; это не тесты, cache acceptance или SDK proof. Ambient Git overrides, даже empty, не сбрасываются молча.

### SDK-independent static envelope (zsh)

Этот блок исполняется после source/fixture edits, до любого `dotnet` diagnostic. Он не читает SDK selectors, не выполняет setup/build/SqlPackage/SQL и не меняет existing venv. Отдельные fixtures используют настоящий `shutil.which`, поэтому нужны два regular lookup-only файла: версии/SQL outputs по-прежнему выдаёт existing FakeExecutor. Эти файлы — ignored synthetic proof carrier, не SDK installation или новый checked-in helper.

```sh
set -eu
MSSQL_CURRENT_ROOT="$(pwd -P)"
MSSQL_STATIC_PYTHON_BIN="$MSSQL_CURRENT_ROOT/.tmp/venv/bin"
test -x "$MSSQL_STATIC_PYTHON_BIN/python3"
"$MSSQL_STATIC_PYTHON_BIN/python3" -I -B -c \
 'import os,platform,sys; assert sys.version_info[:2]==(3,12); assert platform.system()=="Darwin"; assert not set(os.environ).intersection(("GIT_DIR","GIT_WORK_TREE","GIT_COMMON_DIR","GIT_INDEX_FILE"))'
test ! -L .tmp
test ! -L .tmp/sdk-static-261126
mkdir -p .tmp/sdk-static-261126
MSSQL_STATIC_ROOT="$PWD/.tmp/sdk-static-261126/$(date -u +%Y%m%dT%H%M%SZ)"
test ! -e "$MSSQL_STATIC_ROOT" && test ! -L "$MSSQL_STATIC_ROOT"
mkdir "$MSSQL_STATIC_ROOT"
MSSQL_STATIC_BIN="$MSSQL_STATIC_ROOT/lookup-bin"
MSSQL_STATIC_TMP="$MSSQL_STATIC_ROOT/temp"
MSSQL_STATIC_EXECUTION_MARKER="$MSSQL_STATIC_ROOT/lookup-executed"
mkdir "$MSSQL_STATIC_BIN" "$MSSQL_STATIC_TMP"
for mssql_lookup in dotnet sqlcmd; do
  printf '%s\n' '#!/bin/sh' \
    'printf "%s\n" invoked >> "$MSSQL_STATIC_EXECUTION_MARKER"' \
    'exit 97' > "$MSSQL_STATIC_BIN/$mssql_lookup"
  chmod 700 "$MSSQL_STATIC_BIN/$mssql_lookup"
done
```

Самостоятельный make envelope сохраняет HOME, помещает temporary Git fixtures внутрь project `.tmp` и не пропускает реальный SDK/sqlcmd из ambient PATH:

```sh
mssql_static() (
  set -eu
  mssql_goal="$1"
  case "$mssql_goal" in test|check-secrets) ;; *) return 2 ;; esac
  : "${PLANVEYOR_RUNTIME_ROOT:?selected pinned runtime required}"
  cd "$MSSQL_CURRENT_ROOT"
  export PATH="$MSSQL_STATIC_BIN:$MSSQL_STATIC_PYTHON_BIN:/usr/bin:/bin:/usr/sbin:/sbin"
  export TMPDIR="$MSSQL_STATIC_TMP" TMP="$MSSQL_STATIC_TMP" TEMP="$MSSQL_STATIC_TMP"
  export PYTHONDONTWRITEBYTECODE=1 MSSQL_STATIC_EXECUTION_MARKER
  test "$(command -v python3)" = "$MSSQL_STATIC_PYTHON_BIN/python3"
  test "$(command -v dotnet)" = "$MSSQL_STATIC_BIN/dotnet"
  test "$(command -v sqlcmd)" = "$MSSQL_STATIC_BIN/sqlcmd"
  python3 -I -B -c \
   'import os,platform,sys; assert sys.version_info[:2]==(3,12); assert platform.system()=="Darwin"; assert not set(os.environ).intersection(("GIT_DIR","GIT_WORK_TREE","GIT_COMMON_DIR","GIT_INDEX_FILE"))'
  command -v git >/dev/null
  command -v make >/dev/null
  make "$mssql_goal"
  test ! -e "$MSSQL_STATIC_EXECUTION_MARKER"
)
mssql_static test
mssql_static check-secrets
```

Каждую make-цель исполнять отдельно и сохранять actual make/wrapper/envelope rc, test counts, actual project Python/platform, HEAD/snapshot, stub hashes и отсутствие execution marker в create-only `MSSQL_STATIC_ROOT/source-static.json`; raw logs остаются рядом transient-only. Stub invocation/unknown result — не green. `make test` использует настоящий Git только в synthetic disposable repos; текущий index не меняется. План/doc checks и `git diff --check` остаются самостоятельными static checks. При missing Python/other static prerequisite test считается не выполненным, окружение не восстанавливается; source edits/другие независимые checks не превращаются в его success. Две полные SDK rows и real/negative acceptance остаются обязательными.

### SDK-dependent command-scoped envelope (zsh)

Определить один раз в локальном исполняющем сеансе; `mssql_row` — shell recipe, не новый checked-in helper. `MSSQL_BASE_PATH` — исходный PATH сеанса, HOME сохраняется. Не выводить private arguments/env в tracked evidence.

```sh
: "${PLANVEYOR_RUNTIME_ROOT:?selected runtime required}"
MSSQL_BASE_PATH="$PATH"
mssql_row() (
  set -eu
  : "${MSSQL_PYTHON312_BIN:?prepared project Python 3.12 required for this row}"
  mssql_row_root="$1"; mssql_sdk_root="$2"; shift 2
  cd "$mssql_row_root"
  export PATH="$mssql_sdk_root:$MSSQL_PYTHON312_BIN:$MSSQL_BASE_PATH"
  export DOTNET_ROOT="$mssql_sdk_root" DOTNET_ROOT_ARM64="$mssql_sdk_root"
  export DOTNET_CLI_HOME="$PWD/.tmp/dotnet-home"
  export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1 DOTNET_NOLOGO=1
  export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE=true
  export MSBuildEnableWorkloadResolver=false DOTNET_CLI_UI_LANGUAGE=en-US
  export NUGET_PACKAGES="$PWD/.tmp/nuget/packages"
  export NUGET_HTTP_CACHE_PATH="$PWD/.tmp/nuget/http-cache"
  export NUGET_PLUGINS_CACHE_PATH="$PWD/.tmp/nuget/plugins-cache"
  export PIP_CACHE_DIR="$PWD/.tmp/pip-cache" PYTHONDONTWRITEBYTECODE=1
  export TMPDIR="$PWD/.tmp/temp" TMP="$PWD/.tmp/temp" TEMP="$PWD/.tmp/temp"
  mkdir -p "$TMPDIR" "$DOTNET_CLI_HOME" "$NUGET_PACKAGES" "$PIP_CACHE_DIR"
  "$@"
)
```

Перед входом в runtime envelope проверить отсутствие `DOTNET_ROLL_FORWARD`, `DOTNET_ROLL_FORWARD_TO_PRERELEASE`, `DOTNET_HOST_PATH` и иных launch overrides, которые подменяют выбранный framework/host. При наличии — stop/Architect до dependent command, без автоматического очищения. Проверить actual Python3.12/Darwin и его prefix вне перезаписываемой row/.tmp/venv до setup; static interpreter не подставляется в setup автоматически. При каждом diagnostic actual executable/root сверяются с private selector; PATH token не доказывает identity.

### Git-копия и immutable receipts

После реализации и до подготовки №1 зафиксировать final snapshot и unique run directory. Ни setup, ни эта Git-копия не создаются Planner.

```sh
set -eu
MSSQL_CURRENT_ROOT="$PWD"
MSSQL_PLAN=docs/plans/261126_1137_mssql_dotnet_sdk_10_11.md
MSSQL_DRAFT=docs/code_drafts/261126_1137_mssql_dotnet_sdk_10_11__code_draft.md
MSSQL_RUN_STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
MSSQL_RUN_ROOT="$PWD/.tmp/sdk-compat-261126/$MSSQL_RUN_STAMP"
MSSQL_COPY_ROOT="$MSSQL_RUN_ROOT/offline-sdk11"
test ! -L .tmp
test ! -L .tmp/sdk-compat-261126
mkdir -p .tmp/sdk-compat-261126
test ! -e "$MSSQL_RUN_ROOT" && test ! -L "$MSSQL_RUN_ROOT"
mkdir "$MSSQL_RUN_ROOT"
mkdir "$MSSQL_RUN_ROOT/receipts"
MSSQL_HEAD="$(git rev-parse --verify HEAD)"
git clone --no-local --no-hardlinks --no-checkout --no-tags \
  "$MSSQL_CURRENT_ROOT" "$MSSQL_COPY_ROOT"
git -C "$MSSQL_COPY_ROOT" -c core.hooksPath=/dev/null checkout --detach "$MSSQL_HEAD"
```

Из `code_draft_meta.targets` standard JSON readback получает exact12 path list; это literal inventory, не `git status` heuristic. Для каждого path regular/non-symlink source/parent chain, существующий regular target и unchanged mode: `cp "$MSSQL_CURRENT_ROOT/$p" "$MSSQL_COPY_ROOT/$p"`, затем `cmp` двух файлов. Отдельно скопировать только этот plan и draft для snapshot resolution. `.env.local`, `.tmp`, `.git`, чужие untracked/WIP и кеши не overlay-ить. В копии `.env.local` должен быть лексически absent, Git HEAD равен captured HEAD; Git roots физически различны, objects independent/no alternates. Если non-target build/test input отличается от HEAD, stop и сохранить чужой WIP; не копировать его молча. Нельзя выполнять git checkout/restore/reset или staging в текущем sibling.

В каждом корне public facade с его literal project root:

```sh
"$PLANVEYOR_RUNTIME_ROOT/bin/planveyor" --project "$PWD" \
  planveyor_review_target_snapshot "$MSSQL_PLAN" --current-bundle
```

Полный JSON сохраняется standard output capture в `receipts/final-current.before.json`, `receipts/final-copy.before.json` и соответствующие `.after.json`; сравниваются canonical `bundle_sha256`, normalized target path set и все per-target hashes, не whole JSON с различными physical roots. HEAD и hashes обязательны до/после каждой row и обоих SQL proof. Origin plan/Evidence/review append не меняют target hash. Два DACPAC: `.tmp/build/Northwind/bin/Debug/Northwind.dacpac`, `.tmp/build/Northwind.Tests/bin/Debug/Northwind.Tests.dacpac`; записать SHA-256 обоих для каждой row.

Immutable local receipts: `receipts/prep-01-sdk10-current.json`, `prep-02-sdk11-copy.json`, `prep-03-sdk11-current.json`, `coder-sdk10-offline.json`, `coder-sdk11-offline.json`, `reviewer-sdk11-offline.json`, `resolver.json`, `runtime-negative.json`, `coder-sdk10-proof.json`, `reviewer-sdk11-proof.json`. Каждый создаётся один раз через exclusive file write; file exists/unknown outcome — stop, не перезаписывать. Поля: номер/stage/role, started/finished, actual private physical root/launcher+binary SHA, OS/arch, SDK/runtime readback, manifests SHA (`global.json`, tool manifest, NuGet.Config, props, requirements, оба sqlproj), HEAD/bundle до/после, terminal make и wrapper rc, safe phase/reason, cache6/6 и setup.complete SHA, local log refs; для rows — test counts и DACPAC hashes, для SQL — approval Q&A ref/JUnit/hash/counts/identities. `setup.complete` отдельно не доказывает происхождение кеша. Raw streams сохраняются под тем же run root, не печатаются в plan/review.

### Последовательные preparations / offline rows

Каждую команду выполнять отдельно, записывая фактический terminal rc в собственный receipt. Следующая команда разрешена только после green предыдущей. Setup — ровно три явно назначенные attempts; failure/interruption/unknown outcome — stop без повтора.

```sh
# Coder: preparation №1 и row SDK10 в текущем sibling.
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" dotnet --version
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" dotnet --list-runtimes
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" make setup
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" make db-build
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" make lint
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" make test
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" make check-secrets
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" dotnet tool run sqlpackage -- /Version
```

Preparation №2: тот же exact набор команд с `MSSQL_COPY_ROOT` и `MSSQL_DOTNET11_ROOT`; SQL из копии запрещён. Только после двух полных green rows, real resolver и negative runtime контроля Coder возвращает `Ready for Architect response` для предметного SQL approval. В запросе preparation №3 ещё planned.

После approval и Coder SDK10 proof preparation №3: тот же exact набор с `MSSQL_CURRENT_ROOT` и `MSSQL_DOTNET11_ROOT`. Это новый restore actual path, а не перенос кеша из копии. Существующие `.tmp` receipts/несвязанные материалы не удаляются. После green Coder ставит `Ready for Review`; Reviewer в том же current-root/SDK11 envelope повторяет `dotnet --version`, `--list-runtimes`, `make db-build`, `make lint`, `make test`, `make check-secrets`, `/Version` без setup и сверяет prep03+две исходные rows.

### Real resolver / negative runtime

`dotnet --list-sdks`, `--version` и `--list-runtimes` каждой положительной installation сверяются отдельно от synthetic tests. SDK10 row вправе использовать prepared combined10+11 root; отдельный only10 inventory не обязателен. SDK11 row требует отсутствия подходящей10, чтобы unchanged candidate выбрал11. Combined diagnostic из current sibling использует actual `MSSQL_DOTNET10_ROOT`, если его list-sdks показывает обе подходящие стабильные ветки в одном SDK root; тот же launcher должен выбрать10. Это одна physical identity/receipt linkage, без отдельной полной row/setup и без повторного запроса того же input. Только если SDK10 root isolated, нужен отдельно предоставленный готовый `MSSQL_DOTNET_BOTH_ROOT`. Missing input останавливает diagnostic и возвращается Architect, наличие roots не выводится из A2. `sdk.paths=[root10,root11]` не substitute both-case; product global.json без paths и launch overrides.

No-compatible case: отдельный ignored `MSSQL_RUN_ROOT/resolver-empty` с `global.json`, копирующим три final policy fields и добавляющим только `paths:["./empty"]`; создать пустой подкаталог. Запустить подготовленный dotnet11 из cwd fixture в том же local envelope, зафиксировать nonzero и missing compatible SDK. Это scoped real-resolver fixture, не unchanged candidate positive row, не SDK-filter rc2. Product global.json не меняется, SDK files не создаются/не копируются.

После positive SDK11 `/Version` rc0 в offline copy выполнить там же через `MSSQL_DOTNET11_NORT10_ROOT` `dotnet --version` и `--list-runtimes`, используя существующий local cache и без setup/restore/SQL. SDK11 version должна совпадать; runtime10 должен отсутствовать. Затем захватить ожидаемый `/Version` отказ отдельно, сохраняя fail-closed guards остальных шагов:

```sh
if mssql_row "$MSSQL_COPY_ROOT" "$MSSQL_DOTNET11_NORT10_ROOT" \
  dotnet tool run sqlpackage -- /Version; then
  MSSQL_NEGATIVE_RC=0
else
  MSSQL_NEGATIVE_RC=$?
fi
test "$MSSQL_NEGATIVE_RC" -ne 0
```

Local logs должны показать missing required `Microsoft.NETCore.App`10 framework; фактический nonzero сохраняется, исторический150 не фиксируется как ожидаемый. Иной/unknown failure не закрывает AC3. Не менять negative root/framework, не добавлять `--allow-roll-forward` или runtime override. До/после сохраняются launcher binary/manifest/SqlPackage DLL/runtimeconfig hashes и physical cache-root identity; изменяемые CLI cache metadata только наблюдаются в receipt, от них не требуется побайтная неизменность. Negative не расходует setup attempt.

### Будущий SQL этап — только после отдельного Q&A approval

Общий current HEAD/bundle должен совпадать с утверждёнными двумя rows. В текущем sibling Coder перед preparation №3, затем Reviewer после неё и своего offline readback:

```sh
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET10_ROOT" make db-proof \
  JUNIT=docs/code_reviews/assets/261126_1137_mssql_dotnet_sdk_10_11/sdk10.coder.junit.xml
# После Coder preparation №3 и независимых Reviewer offline checks:
mssql_row "$MSSQL_CURRENT_ROOT" "$MSSQL_DOTNET11_ROOT" make db-proof \
  JUNIT=docs/code_reviews/assets/261126_1137_mssql_dotnet_sdk_10_11/sdk11.reviewer.junit.xml
```

Непосредственно перед каждым proof — runtime-lineage preflight и snapshot; существующая обвязка сама читает `.env.local`, проверяет Git/JUNIT/config и fresh one-query target guard. Ни роль, ни diagnostic не читают credential values. Одна attempt на роль, строго последовательно; refusal/unknown output/drift — stop, повтор требует Architect решения. Никакого stage/Done/commit до отдельного разрешения Owner на конкретные review/exact bundle/message.

JUnit: `GetReorderCandidatesTests` ровно `test T1 empty Products returns empty result`, `test T2 active shortage is returned`, `test T3 zero and negative shortage excluded`, `test T4 on order units cover shortage`, `test T5 discontinued products excluded`, `test T6 numeric nulls treated as zero`, `test T7 smallint arithmetic does not overflow`, `test T8 result metadata and ProductID order`; `StackAdaptationTests` ровно `test Products table exists`. Каждый XML — 9 unique cases, failures/errors/skipped=0, согласованные suite/root counters, fresh SHA. Synthetic GOOD_XML, totals или previous JUnit не заменяют actual proof.

## Review route

- `Primary artifact`: `docs/code_reviews/261126_1137_mssql_dotnet_sdk_10_11.md`
- `Lane type`: code review
- Review получает safe summaries обеих исходных rows, preparation03/Reviewer checks, resolver/negative verdicts, actual counts/codes/digests и два explicit JUnit refs. Local private receipts/logs не являются публикуемыми assets.

## Critical invariants / traps / bypass paths

- Invariant: только stable SDK10/11 разрешены после resolver; trap — real resolver green не доказывает filter boundaries, fake version не доказывает resolver.
- Invariant: ровно восемь SDK-фраз и сохранённые guards; trap — equality старого восьмого tail при семи новых, bridge early return, один caller вместо двух.
- Invariant: SQL proof относится к одному implementation snapshot и actual prepared root/SDK; trap — cache marker, перенесённый toolResolverCache с absolute path, setup Reviewer, stale XML или setup03 receipt до SQL approval.
- UI invariants / screenshots / login: N/A (why=CLI-only task).

## Notes for Coder

Missing prerequisite останавливает соответствующий зависимый шаг: записать exact missing input, выполненный независимый prefix и blocker к Architect; static/source результаты не теряются и не превращаются в runtime proof. Conflicting baseline требует stop до опасного копирования/запуска. Contract не разрешает установку SDK/runtime, server repair, новый checked-in helper/цель, перенос чужих WIP/credentials, автоматический retry или смену runtime. Source/docs/policy checks не заявляют product/SQL green. Обычный Planner CENSOR запускает Manager отдельно после primary handoff.

## Review stamps (append-only)

- [2026-11-26 14:03 +0300] (Planner) Создан и прочитан exact executable draft: 12 targets, derived N-A ref, 8-file inventory, command/copy/receipt contract и отдельные будущие SQL/commit gates; implementation и runtime acceptance не заявлены.
- [2026-11-26 14:06 +0300] (Planner) Completion pass выявил real-resolver precondition gap Q2; combined selector quarantined как предложение. Related plan возвращён Architect, executable handoff не выполнен; structural lint/preflight green не снимает semantic blocker.
- [2026-11-26 14:39 +0300] (Planner) По A2/CLOSED Q2 обновлены current header/Steps/inputs/Real resolver и два отдельных envelopes. Source/static prefix не требует SDK roots; existing project Python read-only проверен3.12.14/Darwin/arm64, synthetic lookup carrier ограничен `.tmp`; engine PYBIN не стал project selector. Combined proof вправе reuse SDK10 physical root после actual observation, only10 inventory не обязателен. Все7 shell blocks прошли syntax-only `zsh -n`; plan lint/strict preflight/doc lint/whitespace green. Это первый executable contract handoff, не выполненные project tests/SDK/setup/SQL или product acceptance.
- [2026-11-26 14:47 +0300] (Planner) Post-handoff second opinion уточнил bootstrap readiness, fail-closed/exclusive static и Git-copy preparation, runnable expected-negative capture и immutable package vs mutable CLI-cache boundary. Exact12 targets/ref/status сохранены; syntax-only zsh -n всех8 blocks rc0. Отчёт и gates находятся в plan Evidence этого времени; runtime-команды не исполнялись.

# Code draft: Проверка восьми shared prefix по pinned source

**Date:** 2026-10-30 03:21 +0300
**Cluster:** quality
**Related plan:** `docs/plans/261030_0221_shared_rules_pinned_source_check.md`
**Author role:** Planner
**Status:** draft

## Meta (machine-readable JSON)

```json
{
  "code_draft_meta": {
    "plan": "docs/plans/261030_0221_shared_rules_pinned_source_check.md",
    "cluster": "quality",
    "targets": [
      {
        "path": "scripts/test_sql.py",
        "kind": "py"
      },
      {
        "path": "README.md",
        "kind": "doc"
      }
    ],
    "deleted_paths": [],
    "machine_authority_decision_ref": {
      "applicability": "not_applicable",
      "reason_code": "docs_or_tests_only",
      "carrier_sha256": "0269d242a243594c5a7f9e4d113e857cd49dcb6bbe5fe6f23cef2e2213119f54"
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
- Captured at: `2026-10-30T00:21:11Z`

Provenance описывает только происхождение draft. Plan provenance сохраняется; `Context source`, rerun receipt и rollout ownership — отдельные carriers. Derived N-A ref получен штатным stub helper после fresh canonical oracle; semantic core не копируется, admission_baseline неприменим.

## Purpose

Восстановить byte-exact source prefix и сохранить полный local tail baseline, не меняя production SQL/runtime authority. Doctor проверяет selection/pin/presence/merge, **не** equality shared content; прежнее обратное обоснование явно исправляется в новом review, historical bundle read-only.

## Reviewability preflight receipt

- `proof-path class`: repo-backed Git bytes + bounded temporary Git fixtures + текущие stack gates.
- `mandatory primary lane`: полный current `make test` вместе с runtime/doctor в одном вызове каждым Coder/Reviewer; обе независимые code review lanes на current snapshot.
- `mandatory non-primary carrier / contextual lane`: T2 старый sibling HEAD/новый pin; source worktree drift; T3–T6 реальные make failed IDs по exact fixture matrix ниже. Исторический doctor green не content proof.
- `exact helper path + support files`: mutable только `scripts/test_sql.py`; read-only `scripts/sql.py::main`, `Makefile`, marker, восемь LOCAL_FILES и pinned `copier_template/` blobs; external facade/consumer doctor из уже выбранного runtime.
- `dependent tests / dependent docs / known consumer paths`: `RepositoryContractTests`, новые `PinnedSourceContractTests`/`PinnedSourceRegressionTests`; строка `make test` в `README.md`; `scripts/sql.py` потребляет unittest failures/errors через `test.id()` и сохраняет прежние counts/rc.
- `preconditions / seed-discovery`: непустой selected runtime, physical regular executable facade, full source_commit и exact runtime HEAD, doctor state=ok, доступный sibling HEAD; prepared macOS/Python 3.12 PATH и dependencies без setup.
- `reroute rule`: missing runtime/prerequisite — fail closed без поиска/установки/skip; необходимость менять production wrapper/Makefile/runtime/rule files — Architect response до widening.
- `perceptual truth-source split`: N/A (why=no UI/visual lane; Git bytes, real make names/rc и canonical snapshot — truth sources).
- Truth-host fixture matrix: N/A (why=fan-in/readback helpers и authoritative schema не меняются).
- Receipt schema emitter inventory / changed payload fields: N/A (why=marker/receipt/API schema, validators и emitters не меняются).
- Manager command surface: N/A (why=dispatch path unchanged; новых owner-facing commands нет).
- `runtime-lineage preflight`: runtime/doctor и make test в одном вызове, полный runtime/source commit; stale runtime возвращается owning environment/Architect, без нового выбора checkout.
- `discovery-or-seed`: новый role-owned runtime/pin, sibling HEAD, canonical bundle_sha256 и отдельный Git-untracked relative JUnit в начале каждого независимого proof.
- `receipt-reuse-only`: guard → Publish → RunAll → unchanged formatter → strict XML parse → atomic sanitized JUnit → post-proof snapshot в том же выбранном контексте, без retry/reseed.
- Stable identity fields: PLAN_PATH, full runtime/source commit, sibling HEAD, canonical bundle_sha256, relative JUnit path/SHA-256, точные девять testcase; target config удерживает unchanged wrapper, роли credentials не читают.
- Exact observer boundary: fresh one-query target guard непосредственно перед Publish, HEAD/snapshot до и после; closure — fresh strict JUnit и post-proof readback того же bundle. `notice/success text != mutation truth`; db-state contextual-only.
- Retention: temp fixtures и `.tmp/n1-consumer-doctor.json` — transient local sanity only; `docs/code_reviews/261030_0221_shared_rules_pinned_source_check.md`, штатные explicit review support refs и два exact JUnit — durable operator/review evidence. Старые upgrade assets historical anchor only.

## Targeted changes (by file)

- `scripts/test_sql.py`: test-local acquisition/comparison path, distinct live refusal IDs, bounded real-Git regression fixtures; сохранить существующие local guards и остальные SQL wrapper tests. Нового production helper/manifest/cache/pin constant/checked-in corpus нет.
- `README.md`: изменить только существующую строку `make test` таблицы: обязательный уже выбранный `PLANVEYOR_RUNTIME_ROOT`, offline без SQL/config/cache. Остальные строки/документы неизменны.

Writable inventory = только два metadata targets; deleted_paths=[]; plan/draft/review/explicit support — отдельные lifecycle carriers. Восемь rules, marker/answers, Makefile, scripts/sql.py, sql/**, docs/stack_brief.md и внешний runtime — read-only; historical upgrade bundle не restamp-ить.

## Review route

- `Primary artifact`: `docs/code_reviews/261030_0221_shared_rules_pinned_source_check.md` — PLANNED, создаёт Reviewer.
- `Lane type`: code review, обязательны `reviewer_code_contracts` и `reviewer_code_risk`; новый review исправляет old doctor rationale отдельно от их verdict.
- Target: canonical current-bundle snapshot штатного producer, одинаковый для обеих lanes; final proof/readback и strict bundle --check обязательны после review.

## Patch sketch (keep it small)

### Steps

1. Развести source и local baselines: full marker SHA, commit existence/type и runtime HEAD equality; pinned Git blob для каждого `copier_template/<LOCAL_FILES path>`. Непустой runtime только из переменной; Git errors/boundary errors — refusals, без fallback/skip.
2. Выделить все bytes строго до единственной canonical stack H2 и сравнить с source blob; source boundary валидировать независимо. Не нормализовать line endings/whitespace/Unicode. Полный local tail от stack H2 до EOF сверять с `HEAD:<path>` sibling, сохранив exact headings/order/count, UTF-8, forbidden patterns, inventory и effective disabled override.
3. Оформить live gates и exact regression inventory ниже. Исправить комментарий о doctor и заменить arbitrary-prefix positive case согласованным uncommitted upgrade. Низкоуровневая реализация функций/fixtures остаётся Coder-owned; этот sketch фиксирует contract/proof.
4. Изменить одну разрешённую README row; завершить все targets до snapshot/proof. Выполнить Commands из plan с current bytes и оставить current review route.
5. Coder и Reviewer независимо выполняют полный offline lane и каждый собственный db-proof; reuse старого XML/receipt запрещён. Если target менялся после proof — новый snapshot/proof и review rerun.

### Exact regression inventory / fixture contract

Новые имена ниже — контракт будущих tests в `scripts/test_sql.py`, а не утверждение об уже выполненной реализации. Реальные gate tests вынести в `PinnedSourceContractTests`; regression fixtures — в отдельный `PinnedSourceRegressionTests`, чтобы subprocess lane не вызывал себя рекурсивно. Каждый gate использует тот же test-local acquisition/comparison path, что и fixture lane; вторая копия validator/parser запрещена. Внутренние функции/распределение реализации остаются Coder-owned.

| Live failed testcase suffix | Что доказывает / обязательный negative |
| --- | --- |
| `PinnedSourceContractTests.test_runtime_root_is_configured` | Переменная отсутствует или пустая — два отдельных fixture cases |
| `PinnedSourceContractTests.test_selected_runtime_is_available` | Несуществующий выбранный каталог и существующий не-Git каталог — два cases |
| `PinnedSourceContractTests.test_source_pin_is_full_sha` | Short SHA и full-length nonhex pin — два cases |
| `PinnedSourceContractTests.test_pinned_source_commit_exists` | Полный синтаксически корректный SHA, не существующий в fixture runtime; fail до использования blob |
| `PinnedSourceContractTests.test_runtime_head_matches_source_pin` | Другой существующий полный commit при неизменном runtime HEAD |
| `PinnedSourceContractTests.test_all_pinned_template_blobs_exist` | В новом runtime commit отсутствует один из восьми blobs; marker обновлён и HEAD равен pin |
| `PinnedSourceContractTests.test_pinned_source_boundaries_are_canonical` | Missing и duplicate stack H2 в source blob при корректном pin — два cases |
| `PinnedSourceContractTests.test_pinned_shared_bytes_match` | T3: удалённый и подменённый prefix каждого из восьми файлов, ровно 16 cases; local tail неизменён |
| `PinnedSourceContractTests.test_local_tails_match_head_and_guards` | T4: изменение stack body, effective override и EOF для каждого пути, ровно 24 cases; source prefix корректен |

Bounded regression names: `PinnedSourceRegressionTests.test_current_pinned_source_contract` (T1 acquisition), `test_uncommitted_upgrade_uses_new_pin_and_old_local_head` (T2), `test_pinned_blob_ignores_runtime_worktree_mutation`, `test_make_failure_ids_cover_source_and_local_refusals` (T3–T6 и source boundary). Существующие `RepositoryContractTests.test_local_contract_rejects_*` сохраняются, включая missing/noncanonical/duplicate/reversed headings, equal-unsafe override/forbidden wording, inventory wording, trailing bytes и equal-invalid-UTF8. Старый positive произвольного prefix заменяется согласованным T2.

Fixture setup: один `TemporaryDirectory` вне реального sibling/runtime, два изолированных Git root — synthetic sibling и synthetic runtime. Только stdlib/Git/make; network/credentials/config/cache/SQL отсутствуют. Для runtime материализовать восемь `copier_template/<LOCAL_FILES path>` с различимыми shared prefix и canonical local boundaries; сделать минимум два настоящих commits с разными blobs. Для sibling материализовать те же восемь путей с валидными локальными tails, marker с full pin и начальный commit. Git identity задаётся только per-command `git -c user.name=... -c user.email=... commit`, без global/local config writes в реальном checkout. Синтетические refs не являются current runtime receipts.

Subprocess lane запускает настоящий неизменённый `make test` и `scripts/sql.py` внутри synthetic sibling. Текущие candidate bytes `scripts/test_sql.py` копируются в fixture под non-discovered module name; fixture-only discovery shim экспортирует именно настоящий `PinnedSourceContractTests` из этих bytes, но не `PinnedSourceRegressionTests`. Это bounded suite selection в disposable fixture, не skip/xfail или обход real current-sibling suite. `sql.ROOT` и fixture marker/root указывают на synthetic sibling. Никаких повторных определений gate methods, monkeypatch их outcomes или mock successful Git bytes. Unchanged Makefile/sql.py копируются из текущего sibling; fixture shim не становится checked-in helper/target.

Для каждого case восстановить чистые fixture bytes/refs до ровно одной заданной mutation; незакоммиченный T2 сохраняет sibling HEAD и tails, обновляет marker/current prefix на второй runtime commit, затем независимо меняет runtime worktree prefix. Доказать неравенство old-HEAD/current prefix и равенство current/pinned-blob prefix; worktree mutation не меняет expected bytes. Пустой/другой expected prefix, fallback на sibling HEAD или current worktree запрещены.

Матрица subprocess ограничена 52 negative cases: 16 prefix + 24 local + 2 unset/empty env + 2 unavailable/invalid runtime + 2 malformed pin + 1 missing commit + 1 other existing commit + 1 missing blob + 2 invalid source boundary + 1 trailing-space full pin. Last case также обязан показать `test_source_pin_is_full_sha`, pin не strip/normalize-ится. Все cases выполняются автоматически внутри `make test`, без ручного launcher/glue. Каждый требует nonzero make rc, wrapper `phase=test category=test rc=1`, `offline` summary с failures/errors > 0 и ожидаемый полный `offline failed=` ID с указанным suffix; отсутствие/подмена ID или только assertion traceback — failure outer regression. Prefix/local cases дополнительно именуют path/variant в outer subTest. Дополнительный зависимый failed ID допустим; designated reason-bearing ID обязателен. Positive fixture make — rc0, failures/errors=0 и отсутствие `offline failed=`. Один child invocation ограничен timeout=30s, совокупная operational matrix — budget=180s с явным failure, без auto-retry; превышение бюджета не превращается в skip.

Реальный current `make test` остаётся полной discovery suite, а не fixture shim: его отдельные live gate IDs делают неисправность environment/pin/bytes видимой человеку. Fixture cleanup — штатный finally/context manager; никаких edits/rename реальных runtime/правил/marker или сохранённых expected bytes. Не читать `.env.local`, не копировать `.git`, `.tmp`, HOME или live config. Сам fixture corpus transient local sanity only; durable evidence — безопасный summary матрицы в новом review.

## Commands / proof inventory

Executable команды и shell-блок runtime/doctor + make test — дословно `PLAN_PATH::## Commands`; проектный interpreter — только подготовленный Python 3.12 из PATH через make. Переданный PYBIN принадлежит engine; абсолютный путь и make PYBIN override в artifacts запрещены локальным prompt. Engine проверки выполняются через выбранный facade, сохраняющий его environment.

Coder: `make db-build`, `make lint`, runtime/doctor + `make test` в одном вызове, `make check-secrets`; затем HEAD + canonical snapshot, свой `make db-proof JUNIT=docs/code_reviews/assets/261030_0221_shared_rules_pinned_source_check/coder.junit.xml`, SHA-256, HEAD + snapshot. Reviewer независимо повторяет offline lane, `make db-state`, затем те же pre/post readbacks и `make db-proof JUNIT=docs/code_reviews/assets/261030_0221_shared_rules_pinned_source_check/reviewer.junit.xml`. Setup/Extract/SQL retry не разрешены. Architect только `make db-state` и чтение текущих proofs.

Оба JUnit: `GetReorderCandidatesTests` с точными именами `test T1 empty Products returns empty result`, `test T2 active shortage is returned`, `test T3 zero and negative shortage excluded`, `test T4 on order units cover shortage`, `test T5 discontinued products excluded`, `test T6 numeric nulls treated as zero`, `test T7 smallint arithmetic does not overflow`, `test T8 result metadata and ProductID order`; плюс `StackAdaptationTests.test Products table exists`. Ровно 9 unique identities, tests=9/failures=0/errors=0/skipped=0 на suite/root; unknown/duplicate/red case не перекрывается totals. Wrapper выполняет strict parse/sanitization, raw SQL/config/argv не сохранять. Make rc записывается отдельно от wrapper rc.

Exact review support inventory: primary review выше; два JUnit выше; только явно названные штатным reviewer/helper support refs под тем же review basename, с producer/hash/parity по review contract. Placeholder/manual guessed support path не становится target; обе lanes, synthesis, opened/read refs и current snapshot обязательны. Никакого дополнительного helper/fixture target.

## Critical invariants / traps / bypass paths

- `Invariant: pinned-prefix`: новый pin/незакоммиченный upgrade при старом sibling HEAD должен проходить, а source worktree change не влияет на expected bytes. Trap: doctor green/old HEAD/current source worktree выглядит валидным источником; T2 и blob-worktree regression закрывают это.
- `Invariant: complete-local-tail`: prefix repair не ослабляет full tail/heading/UTF-8/override guards. Trap: equal-unsafe fixture tails и EOF; сохранённые negative guards плюс 24 operational cases закрывают это.
- `Invariant: truthful-operational-refusal`: настоящий make failed ID указывает runtime/pin/commit/blob/boundary/prefix/local причину. Trap: passing negative unit test при нечитаемом operational failure; 52 nested real-make cases закрывают это.
- UI/alternate browser surfaces: N/A (why=no UI). Primary green не заменяет обязательную contextual matrix или два независимых SQL proofs.

## Assumptions / risks

Prepared macOS/Python 3.12 PATH и stack tools должны существовать; missing prerequisite даёт reroute без install/setup. Временные source commits не означают текущую source qualification. SQL proof — отдельный stack gate, synthetic fixtures не являются live SQL acceptance. Unknown/excessive scope требует Architect response до widening.

## Notes for Coder

Plan выше sketch при противоречии. Не менять сами rule files ради прохождения tests и не читать credentials. Не ставить Done и не коммитить. Текущая policy native_existing не снимает exact byte-review Owner: перед каждым semantic/docs commit показать staged bytes/inventory/конкретный message, получить фактическое разрешение на следующий отдельный commit tool call. Stage/preflight и commit никогда не в одном вызове; docs отдельный gate, no_op только fresh canonical readback.

## Review stamps (append-only)

- [2026-10-30 03:21 +0300] (Planner) Создан полноценный draft: два exact targets, no deletions, derived N-A binding, точные live refusal IDs/52-case fixture matrix, текущий review/JUnit inventory и отдельные Owner gates. Реализация/tests/SQL этим stamp не заявлены.

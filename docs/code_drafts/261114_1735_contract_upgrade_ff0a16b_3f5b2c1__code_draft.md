# Code draft: Адаптация контракта Planveyor ff0a16b → 3f5b2c1

**Date:** 2026-11-14 19:15 +0300
**Cluster:** process
**Related plan:** `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`
**Author role:** Planner
**Status:** draft

## Meta (machine-readable JSON)

```json
{
  "code_draft_meta": {
    "plan": "docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md",
    "cluster": "process",
    "targets": [
      {"path": ".copier-answers.yml", "kind": "config"},
      {"path": "docs/_meta/planveyor_contract_authority.v1.json", "kind": "doc"},
      {"path": "docs/rollout_packets/_template.md", "kind": "doc"},
      {"path": "docs/tools/prompts/manager_init.md", "kind": "doc"},
      {"path": "docs/upstream_packets/_template.md", "kind": "doc"}
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

- Source plan provenance: `docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`; новый draft создан отдельно Planner по helper-derived фактам.
- Relation: `created-here`
- Thread ID: `<REDACTED>`
- Parent thread ID: `N/A (why=not exposed by env, wrapper receipts, or session stats)`
- Session SID: `N/A (why=.planveyor.session.planner is missing or empty)`
- Launch surface: `unknown (why=no env, wrapper receipt, or session stats origin identified the launch surface)`
- Captured from: `env`
- Captured at: `2026-11-14T16:14:17Z`

## Purpose

Проверить пять доставленных targets с literal C-Q3 child binding к уже explicitly selected runtime. Setup Q1 actual session 58890 завершён terminal process/make/wrapper rc0/6-of-6/continuity green; attempt permanently consumed, только receipt-reuse-only. Новые setup/install/restore/Extract запрещены всем ролям.

## Targeted changes (by file)

- `.copier-answers.yml`: `_commit: 3f5b2c1`, прежние repository/source значения.
- `docs/_meta/planveyor_contract_authority.v1.json`: `source_commit=3f5b2c1a903e92eea9551919a18e923eb4045a2e`; `authority_mode=target-local`, `contract_root=.`, API min/max=5 и schema/repository identity прежние.
- `docs/rollout_packets/_template.md`: label `Related source docs/code drafts` совпадает с существующим генератором.
- `docs/upstream_packets/_template.md`: единственное sample значение Trigger ref совпадает с JSON; допустимые plan/review/PI виды остаются отдельным абзацем.
- `docs/tools/prompts/manager_init.md`: ссылка на существующий `## Bootstrap Pointers`.
- Generated index/rebuild, receipt schema emitter inventory, API field parity: N/A (why=такие carriers/fields не меняются).
- Existing baseline surfaces: source `scripts/rollout_packet.py`, `scripts/upstream_request.py`, `scripts/consumer_contract.py`, `scripts/review_target_snapshot.py`, source tests из Context links; target `Makefile`, `scripts/sql.py`, `scripts/test_sql.py` и восемь local matrix files — read-only. New product/helper targets: отсутствуют.
- Manager dispatch/runtime/one-shot changes: N/A (why=dispatch path unchanged; исправляется только документированная bootstrap-ссылка). Cold-start execution не заявляется.
- C-Q2 source-only inventory: `scripts/sql.py` → Stack.__init__/tools/setup/cache, `Makefile`, `requirements-dev.txt`, `.config/dotnet-tools.json`, `NuGet.Config`, `Directory.Build.props`, `global.json`, `sql/Northwind/Northwind.sqlproj`, `sql/tests/Northwind.Tests.sqlproj`. Эти manifests/harness не меняются; существующие setup outputs в `.tmp` не становятся product targets.

## Reviewability preflight receipt

- `proof-path class`: existing checked-in helper family + standard read-only primitives.
- `mandatory primary lane`: exact пять targets/pins, current lint/bundle, bound offline gates и два independent live XML 9/0/0/0.
- `mandatory non-primary carrier / contextual lane`: Reviewer selected-runtime packet fixtures, bootstrap/eight-file parity; doctor/db-state contextual-only. Coder AC1–AC5 остаются closed delivery baseline по repo-backed parity.
- `exact helper path + support files`: selected scripts/rollout_packet.py, upstream_request.py, consumer_contract.py, review_target_snapshot.py, plan_lint.py, plan_status_oracle.py, public facade/planveyor.zsh; target Makefile/scripts/sql.py/scripts/test_sql.py.
- `dependent tests / dependent docs / known consumer paths`: source packet tests из Context links; PinnedSourceContract и test_current_pinned_source_contract; три doc targets/Manager bootstrap. Helpers/parser/schema/dispatch не меняются.
- `preconditions / seed-discovery`: каждый standalone exec из sibling root/login=false, fresh lineage/version prefix ниже и literal child binding. Coder retained fixtures не reseed/overwrite; Reviewer свой первый fixture run. Setup consumed/reuse-only, retained before receipts не перезаписывать.
- `reroute rule`: lineage/pin/cache/receipt drift — owning Architect stop до make/SQL, без fallback/runtime search или repair/install. Исторические 87/6/0 red до будущего bound run, synthetic XML из make test не live SQL proof.
- `perceptual truth-source split`: structural/repo-backed; visual N/A (why=no UI), OCR/template/pixel debug-only, image reading bounded fallback.
- Stateful proof: discovery-or-seed = current HEAD/canonical bundle и one-query guard непосредственно перед Publish; далее receipt-reuse-only. Stable identity = тот же HEAD/пять paths/bundle/role-specific XML. Observer boundary = terminal db-proof + atomic sanitized XML; closure = next canonical snapshot/strict XML readback. notice/success text != mutation truth.
- Retention: .tmp/contract-template-proof transient; два XML/current review/immutable risk support durable. Setup receipts только readback.
- Truth-host fixture matrix/API/schema emitter/dispatch/golden-path changes: N/A (why=эти surfaces не меняются).

## Current execution order

1. Каждый exec содержит fresh C-Q3 prefix и literal command-scoped ROOT; нет ROOT export или inheritance из предыдущего shell.
2. Coder reuse setup 58890 terminal rc0/6-of-6/continuity и реальные db-build/lint rc0; затем только fresh bound make test (87/0/0) → check-secrets → первый guarded db-proof.
3. Reviewer свой первый fixture run, полный independent db-build/lint/test/check-secrets/db-state, затем второй db-proof без setup.
4. Один review связывает current bundle/оба XML/support/lanes. Architect после реализации только bound db-state и exact closeout; Planner/Coder не stage/commit/Done writers.

## C-Q3 input and per-exec preflight

`selected_runtime_from_header` — единственный task input: точное непустое поле PLANVEYOR_RUNTIME_ROOT текущего role control header. Агент передаёт его как **неэкспортируемый task-local аргумент в этот же exec**, не читает inherited ROOT и не переносит из прошлого shell. Значение уже дано запуском, это не новый вопрос Owner/не guessed path. Absolute spelling допускается только в tool-call, не записывается в repo/evidence. Missing input или unequal physical root — owning Architect stop.

Каждый блок повторяет полный read-only prefix в том же exec и требует этот control-header input заново. Literal child binding `PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1` и direct `../runtime-3f5b2c1/bin/planveyor --project "$PWD"` сохраняются у каждого make/helper/snapshot. PATH/PYBIN/home/config/global env/runtime bytes не меняются. Prefix проверяет cwd, physical equality с supplied root, regular executable, Git root/HEAD=full pin/commit/8 pinned blobs и Python 3.12/Darwin; не является test/SQL acceptance.

```zsh
set -euo pipefail
: "${selected_runtime_from_header:?required exact selection from current role header}"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 python3 -B - "$selected_runtime_from_header" <<'LINEAGE'
import json, os, platform, stat, subprocess, sys
from pathlib import Path
root = Path(os.environ["PLANVEYOR_RUNTIME_ROOT"]).resolve(strict=True)
assert root == Path(sys.argv[1]).resolve(strict=True), "selection physical mismatch"
assert sys.version_info[:2] == (3, 12) and platform.system() == "Darwin"
facade = root / "bin/planveyor"
assert stat.S_ISREG(facade.lstat().st_mode) and os.access(facade, os.X_OK)
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
assert Path(top).resolve() == Path.cwd().resolve()
pin = json.loads(Path("docs/_meta/planveyor_contract_authority.v1.json").read_text())["source_commit"]
assert pin == "3f5b2c1a903e92eea9551919a18e923eb4045a2e"
assert Path(git("rev-parse", "--show-toplevel")).resolve() == root
assert git("rev-parse", "--verify", "HEAD") == pin and git("cat-file", "-t", pin) == "commit"
paths = ["docs/tools/prompts/" + n + ".md" for n in ("architect_status_driven", "planner_status_driven", "coder_status_driven", "coder_migrations_gate", "reviewer_status_driven")]
paths += ["docs/playbooks/" + n + ".md" for n in ("review_staged_or_commit", "review_merge_range", "post_merge_audit")]
assert all(git("cat-file", "-t", pin + ":copier_template/" + p) == "blob" for p in paths)
print("lineage: physical equality, regular executable, HEAD=pin, 8/8 blobs, Python 3.12/Darwin")
LINEAGE

```

## Reviewer first fixture preparation

Только Reviewer, Coder не повторяет. Existing reviewer root — stop, не удаление/reseed. Accepted templates копируются verbatim; finite substitutions source test прежние.
```zsh
set -euo pipefail
: "${selected_runtime_from_header:?required exact selection from current role header}"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 python3 -B - "$selected_runtime_from_header" <<'LINEAGE'
import json, os, platform, stat, subprocess, sys
from pathlib import Path
root = Path(os.environ["PLANVEYOR_RUNTIME_ROOT"]).resolve(strict=True)
assert root == Path(sys.argv[1]).resolve(strict=True), "selection physical mismatch"
assert sys.version_info[:2] == (3, 12) and platform.system() == "Darwin"
facade = root / "bin/planveyor"
assert stat.S_ISREG(facade.lstat().st_mode) and os.access(facade, os.X_OK)
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
assert Path(top).resolve() == Path.cwd().resolve()
pin = json.loads(Path("docs/_meta/planveyor_contract_authority.v1.json").read_text())["source_commit"]
assert pin == "3f5b2c1a903e92eea9551919a18e923eb4045a2e"
assert Path(git("rev-parse", "--show-toplevel")).resolve() == root
assert git("rev-parse", "--verify", "HEAD") == pin and git("cat-file", "-t", pin) == "commit"
paths = ["docs/tools/prompts/" + n + ".md" for n in ("architect_status_driven", "planner_status_driven", "coder_status_driven", "coder_migrations_gate", "reviewer_status_driven")]
paths += ["docs/playbooks/" + n + ".md" for n in ("review_staged_or_commit", "review_merge_range", "post_merge_audit")]
assert all(git("cat-file", "-t", pin + ":copier_template/" + p) == "blob" for p in paths)
print("lineage: physical equality, regular executable, HEAD=pin, 8/8 blobs, Python 3.12/Darwin")
LINEAGE
proof_role=reviewer python3 -B - <<'PY'
import os, shutil
from pathlib import Path
role = os.environ["proof_role"]
assert role in {"coder", "reviewer"}
base = Path(".tmp/contract-template-proof") / role
assert not base.exists(), "existing fixture retained; select owning rerun after triage"
base.mkdir(parents=True)
for rel in ("scratch", "rollout/docs/rollout_packets", "rollout/docs/plans",
            "upstream/docs/upstream_packets"):
    (base / rel).mkdir(parents=True)
shutil.copyfile("docs/rollout_packets/_template.md", base / "rollout/docs/rollout_packets/_template.md")
shutil.copyfile("docs/upstream_packets/_template.md", base / "upstream/docs/upstream_packets/_template.md")
(base / "rollout/docs/plans/source.md").write_text("# Source\n", encoding="utf-8")
text = (base / "upstream/docs/upstream_packets/_template.md").read_text(encoding="utf-8")
substitutions = {
    "<TOPIC>": "Packet template fixture",
    "YYYY-MM-DD HH:MM ±HHMM": "2026-11-13 23:45 +0300",
    "<origin-repo>": "consumer-fixture",
    "YYMMDD_HHMM_origin_topic": "261113_2345_consumer_fixture_packet_template",
    "<origin-plan>": "261113_2300_packet_template_fixture",
    "<review>": "261113_2300_packet_template_fixture",
    "<file>": "261113_2300_packet_template_fixture__process_improvements_backlog",
    "#...": "#problem", "PI-NNN": "PI-001", "<id>": "261113_2345_packet_template_fixture",
    "**Status:** open | imported | decided | superseded | cancelled": "**Status:** open",
    "<target-observed process/helper/prompt symptom>": "target packet template fails source lint",
    "<shared source-side gap to evaluate in planveyor>": "visible trigger reference differs from metadata",
    "<bounded source-side fix or triage proposal>": "align the shared packet template with strict validation",
}
for token, value in substitutions.items():
    text = text.replace(token, value)
packet = base / "upstream/docs/upstream_packets/261113_2345_consumer_fixture_packet_template.md"
packet.write_text(text, encoding="utf-8")
(base / "upstream.before").write_bytes(packet.read_bytes())
print("synthetic fixtures prepared")
PY
```

## Reviewer selected helper execution

Самостоятельный reviewer exec, все три calls rc0: rollout dry-run, upstream lint и contextual-only consumer doctor. Raw outputs transient.
```zsh
set -euo pipefail
: "${selected_runtime_from_header:?required exact selection from current role header}"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 python3 -B - "$selected_runtime_from_header" <<'LINEAGE'
import json, os, platform, stat, subprocess, sys
from pathlib import Path
root = Path(os.environ["PLANVEYOR_RUNTIME_ROOT"]).resolve(strict=True)
assert root == Path(sys.argv[1]).resolve(strict=True), "selection physical mismatch"
assert sys.version_info[:2] == (3, 12) and platform.system() == "Darwin"
facade = root / "bin/planveyor"
assert stat.S_ISREG(facade.lstat().st_mode) and os.access(facade, os.X_OK)
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
assert Path(top).resolve() == Path.cwd().resolve()
pin = json.loads(Path("docs/_meta/planveyor_contract_authority.v1.json").read_text())["source_commit"]
assert pin == "3f5b2c1a903e92eea9551919a18e923eb4045a2e"
assert Path(git("rev-parse", "--show-toplevel")).resolve() == root
assert git("rev-parse", "--verify", "HEAD") == pin and git("cat-file", "-t", pin) == "commit"
paths = ["docs/tools/prompts/" + n + ".md" for n in ("architect_status_driven", "planner_status_driven", "coder_status_driven", "coder_migrations_gate", "reviewer_status_driven")]
paths += ["docs/playbooks/" + n + ".md" for n in ("review_staged_or_commit", "review_merge_range", "post_merge_audit")]
assert all(git("cat-file", "-t", pin + ":copier_template/" + p) == "blob" for p in paths)
print("lineage: physical equality, regular executable, HEAD=pin, 8/8 blobs, Python 3.12/Darwin")
LINEAGE
proof_role=reviewer
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 TMPDIR="$PWD/.tmp/contract-template-proof/$proof_role/scratch" \
  ../runtime-3f5b2c1/bin/planveyor --project "$PWD" planveyor_runtime_py rollout_packet.py \
  --repo-root ".tmp/contract-template-proof/$proof_role/rollout" \
  --tooling-root ".tmp/contract-template-proof/$proof_role/rollout" \
  create consumer-fixture packet_template_drift --source-plan docs/plans/source.md \
  --queue-after-import no --dry-run > ".tmp/contract-template-proof/$proof_role/rollout.stdout"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 TMPDIR="$PWD/.tmp/contract-template-proof/$proof_role/scratch" \
  ../runtime-3f5b2c1/bin/planveyor --project "$PWD" planveyor_runtime_py upstream_request.py \
  --repo-root ".tmp/contract-template-proof/$proof_role/upstream" \
  --tooling-root ".tmp/contract-template-proof/$proof_role/upstream" \
  lint docs/upstream_packets/261113_2345_consumer_fixture_packet_template.md --json \
  > ".tmp/contract-template-proof/$proof_role/upstream.json"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 TMPDIR="$PWD/.tmp/contract-template-proof/$proof_role/scratch" \
  ../runtime-3f5b2c1/bin/planveyor --project "$PWD" planveyor_consumer_doctor \
  > ".tmp/contract-template-proof/$proof_role/doctor.json"
```

## Reviewer fixture assertions

Самостоятельный read/assert exec. Без починки Trigger ref/JSON поверх sample.
```zsh
set -euo pipefail
: "${selected_runtime_from_header:?required exact selection from current role header}"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 python3 -B - "$selected_runtime_from_header" <<'LINEAGE'
import json, os, platform, stat, subprocess, sys
from pathlib import Path
root = Path(os.environ["PLANVEYOR_RUNTIME_ROOT"]).resolve(strict=True)
assert root == Path(sys.argv[1]).resolve(strict=True), "selection physical mismatch"
assert sys.version_info[:2] == (3, 12) and platform.system() == "Darwin"
facade = root / "bin/planveyor"
assert stat.S_ISREG(facade.lstat().st_mode) and os.access(facade, os.X_OK)
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
assert Path(top).resolve() == Path.cwd().resolve()
pin = json.loads(Path("docs/_meta/planveyor_contract_authority.v1.json").read_text())["source_commit"]
assert pin == "3f5b2c1a903e92eea9551919a18e923eb4045a2e"
assert Path(git("rev-parse", "--show-toplevel")).resolve() == root
assert git("rev-parse", "--verify", "HEAD") == pin and git("cat-file", "-t", pin) == "commit"
paths = ["docs/tools/prompts/" + n + ".md" for n in ("architect_status_driven", "planner_status_driven", "coder_status_driven", "coder_migrations_gate", "reviewer_status_driven")]
paths += ["docs/playbooks/" + n + ".md" for n in ("review_staged_or_commit", "review_merge_range", "post_merge_audit")]
assert all(git("cat-file", "-t", pin + ":copier_template/" + p) == "blob" for p in paths)
print("lineage: physical equality, regular executable, HEAD=pin, 8/8 blobs, Python 3.12/Darwin")
LINEAGE
proof_role=reviewer python3 -B - <<'PY'
import json, os
from pathlib import Path
base = Path(".tmp/contract-template-proof") / os.environ["proof_role"]
doctor = json.loads((base / "doctor.json").read_text(encoding="utf-8"))
assert doctor["state"] == "ok" and doctor["problems"] == []
text = (base / "rollout.stdout").read_text(encoding="utf-8")
assert text.splitlines().count("- Related source docs/code drafts: " + chr(96) + "N/A" + chr(96)) == 1
assert "Related source documentation/code drafts" not in text
assert (chr(96) + "docs/code_drafts/..." + chr(96) + " / " + chr(96) + "docs/reviews/...") not in text
paths = [line.removeprefix("Packet path: ") for line in text.splitlines() if line.startswith("Packet path: ")]
assert len(paths) == 1
path = Path(paths[0])
assert not path.is_absolute() and ".." not in path.parts
assert not (base / "rollout" / path).exists()
packet_rel = "docs/upstream_packets/261113_2345_consumer_fixture_packet_template.md"
payload = json.loads((base / "upstream.json").read_text(encoding="utf-8"))
assert payload["findings"] == []
assert payload["files"] == [{"file": packet_rel, "status": "ok"}]
packet = base / "upstream" / packet_rel
assert packet.read_bytes() == (base / "upstream.before").read_bytes()
meta = json.loads(packet.read_text(encoding="utf-8").split("```json\n", 1)[1].split("\n```", 1)[0])["upstream_request_meta"]
assert [line for line in packet.read_text(encoding="utf-8").splitlines() if line.startswith("- Trigger ref: ")] == [
    "- Trigger ref: " + chr(96) + meta["trigger_ref"] + chr(96)]
assert not (base / "upstream/docs/process_improvements").exists()
assert not (base / "upstream/docs/plans").exists()
print("rollout dry-run/no-write and upstream lint/no-write: PASS")
PY
```

## Coder consumed setup/continuity readback

Прочитать existing session 58890 terminal receipt в plan и retained before/after receipts. Current branch только receipt-reuse-only: нет future/never-launched/running setup ветки. Не писать/перезаписывать baseline или fixtures; red/missing — owning Architect stop, не failed-setup Owner branch.
```zsh
set -euo pipefail
: "${selected_runtime_from_header:?required exact selection from current role header}"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 python3 -B - "$selected_runtime_from_header" <<'LINEAGE'
import json, os, platform, stat, subprocess, sys
from pathlib import Path
root = Path(os.environ["PLANVEYOR_RUNTIME_ROOT"]).resolve(strict=True)
assert root == Path(sys.argv[1]).resolve(strict=True), "selection physical mismatch"
assert sys.version_info[:2] == (3, 12) and platform.system() == "Darwin"
facade = root / "bin/planveyor"
assert stat.S_ISREG(facade.lstat().st_mode) and os.access(facade, os.X_OK)
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
assert Path(top).resolve() == Path.cwd().resolve()
pin = json.loads(Path("docs/_meta/planveyor_contract_authority.v1.json").read_text())["source_commit"]
assert pin == "3f5b2c1a903e92eea9551919a18e923eb4045a2e"
assert Path(git("rev-parse", "--show-toplevel")).resolve() == root
assert git("rev-parse", "--verify", "HEAD") == pin and git("cat-file", "-t", pin) == "commit"
paths = ["docs/tools/prompts/" + n + ".md" for n in ("architect_status_driven", "planner_status_driven", "coder_status_driven", "coder_migrations_gate", "reviewer_status_driven")]
paths += ["docs/playbooks/" + n + ".md" for n in ("review_staged_or_commit", "review_merge_range", "post_merge_audit")]
assert all(git("cat-file", "-t", pin + ":copier_template/" + p) == "blob" for p in paths)
print("lineage: physical equality, regular executable, HEAD=pin, 8/8 blobs, Python 3.12/Darwin")
LINEAGE
for cached in .tmp/setup.complete .tmp/venv/bin/sqlfluff \
  .tmp/nuget/packages/microsoft.build.sql/2.3.0 .tmp/nuget/packages/tsqlt.dacpacs/1.0.8083.3529 \
  .tmp/build/Northwind/obj/project.assets.json .tmp/build/Northwind.Tests/obj/project.assets.json; do
  test -e "$cached"
done
cmp .tmp/contract-template-proof/coder/setup.head.before .tmp/contract-template-proof/coder/setup.head.after
cmp .tmp/contract-template-proof/coder/setup.snapshot.before.json .tmp/contract-template-proof/coder/setup.snapshot.after.json
cmp .tmp/contract-template-proof/coder/setup.manifests.before.sha256 .tmp/contract-template-proof/coder/setup.manifests.after.sha256
git rev-parse HEAD | cmp - .tmp/contract-template-proof/coder/setup.head.after
shasum -a 256 Makefile scripts/sql.py requirements-dev.txt .config/dotnet-tools.json \
  NuGet.Config Directory.Build.props global.json sql/Northwind/Northwind.sqlproj \
  sql/tests/Northwind.Tests.sqlproj | cmp - .tmp/contract-template-proof/coder/setup.manifests.after.sha256
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 ../runtime-3f5b2c1/bin/planveyor --project "$PWD" \
  planveyor_review_target_snapshot docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md --current-bundle \
  | cmp - .tmp/contract-template-proof/coder/setup.snapshot.after.json
```

HEAD совпадает с retained receipt; snapshot содержит те же пять paths/bundle_sha256=5c718c61cc4194fd47b9fc22873bd26f3bcd347f950776b1de839350ec65e679. Это readback, не новый preparation/live proof.

## Coder remaining offline gates

Только remaining gates; реальные db-build/lint rc0 не replay-ить при unchanged continuity. Expected offline full suite 87/0/0 и check-secrets rc0. Synthetic JUnit не live SQL.
```zsh
set -euo pipefail
: "${selected_runtime_from_header:?required exact selection from current role header}"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 python3 -B - "$selected_runtime_from_header" <<'LINEAGE'
import json, os, platform, stat, subprocess, sys
from pathlib import Path
root = Path(os.environ["PLANVEYOR_RUNTIME_ROOT"]).resolve(strict=True)
assert root == Path(sys.argv[1]).resolve(strict=True), "selection physical mismatch"
assert sys.version_info[:2] == (3, 12) and platform.system() == "Darwin"
facade = root / "bin/planveyor"
assert stat.S_ISREG(facade.lstat().st_mode) and os.access(facade, os.X_OK)
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
assert Path(top).resolve() == Path.cwd().resolve()
pin = json.loads(Path("docs/_meta/planveyor_contract_authority.v1.json").read_text())["source_commit"]
assert pin == "3f5b2c1a903e92eea9551919a18e923eb4045a2e"
assert Path(git("rev-parse", "--show-toplevel")).resolve() == root
assert git("rev-parse", "--verify", "HEAD") == pin and git("cat-file", "-t", pin) == "commit"
paths = ["docs/tools/prompts/" + n + ".md" for n in ("architect_status_driven", "planner_status_driven", "coder_status_driven", "coder_migrations_gate", "reviewer_status_driven")]
paths += ["docs/playbooks/" + n + ".md" for n in ("review_staged_or_commit", "review_merge_range", "post_merge_audit")]
assert all(git("cat-file", "-t", pin + ":copier_template/" + p) == "blob" for p in paths)
print("lineage: physical equality, regular executable, HEAD=pin, 8/8 blobs, Python 3.12/Darwin")
LINEAGE
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 make test
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 make check-secrets
```

## Reviewer independent offline gates

Свой полный run в explicit selected runtime, без setup/install/restore.
```zsh
set -euo pipefail
: "${selected_runtime_from_header:?required exact selection from current role header}"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 python3 -B - "$selected_runtime_from_header" <<'LINEAGE'
import json, os, platform, stat, subprocess, sys
from pathlib import Path
root = Path(os.environ["PLANVEYOR_RUNTIME_ROOT"]).resolve(strict=True)
assert root == Path(sys.argv[1]).resolve(strict=True), "selection physical mismatch"
assert sys.version_info[:2] == (3, 12) and platform.system() == "Darwin"
facade = root / "bin/planveyor"
assert stat.S_ISREG(facade.lstat().st_mode) and os.access(facade, os.X_OK)
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
assert Path(top).resolve() == Path.cwd().resolve()
pin = json.loads(Path("docs/_meta/planveyor_contract_authority.v1.json").read_text())["source_commit"]
assert pin == "3f5b2c1a903e92eea9551919a18e923eb4045a2e"
assert Path(git("rev-parse", "--show-toplevel")).resolve() == root
assert git("rev-parse", "--verify", "HEAD") == pin and git("cat-file", "-t", pin) == "commit"
paths = ["docs/tools/prompts/" + n + ".md" for n in ("architect_status_driven", "planner_status_driven", "coder_status_driven", "coder_migrations_gate", "reviewer_status_driven")]
paths += ["docs/playbooks/" + n + ".md" for n in ("review_staged_or_commit", "review_merge_range", "post_merge_audit")]
assert all(git("cat-file", "-t", pin + ":copier_template/" + p) == "blob" for p in paths)
print("lineage: physical equality, regular executable, HEAD=pin, 8/8 blobs, Python 3.12/Darwin")
LINEAGE
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 make db-build
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 make lint
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 make test
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 make check-secrets
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 make db-state
```

## Два независимых guarded live SQL proof

Coder выполняет первый proof только после успешных current bound test/check-secrets и continuity. Reviewer после своего полного offline/fixture run выполняет второй proof; в следующем блоке меняет только `proof_role=coder` на `proof_role=reviewer`. Каждая роль запускает блок в корне sibling через `exec_command login=false` с заново переданным input из своего control header. XML path получается только из фиксированной пары role/path. SQL не повторяется автоматически; любой nonzero/interrupt/unknown outcome останавливает owning role. До разрешённого первого proof roles не перезаписывают существующие before-receipts: неожиданный существующий carrier требует readback/Architect, а не удаления.

```zsh
set -euo pipefail
: "${selected_runtime_from_header:?required exact selection from current role header}"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 python3 -B - "$selected_runtime_from_header" <<'LINEAGE'
import json, os, platform, stat, subprocess, sys
from pathlib import Path
root = Path(os.environ["PLANVEYOR_RUNTIME_ROOT"]).resolve(strict=True)
assert root == Path(sys.argv[1]).resolve(strict=True), "selection physical mismatch"
assert sys.version_info[:2] == (3, 12) and platform.system() == "Darwin"
facade = root / "bin/planveyor"
assert stat.S_ISREG(facade.lstat().st_mode) and os.access(facade, os.X_OK)
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
assert Path(top).resolve() == Path.cwd().resolve()
pin = json.loads(Path("docs/_meta/planveyor_contract_authority.v1.json").read_text())["source_commit"]
assert pin == "3f5b2c1a903e92eea9551919a18e923eb4045a2e"
assert Path(git("rev-parse", "--show-toplevel")).resolve() == root
assert git("rev-parse", "--verify", "HEAD") == pin and git("cat-file", "-t", pin) == "commit"
paths = ["docs/tools/prompts/" + n + ".md" for n in ("architect_status_driven", "planner_status_driven", "coder_status_driven", "coder_migrations_gate", "reviewer_status_driven")]
paths += ["docs/playbooks/" + n + ".md" for n in ("review_staged_or_commit", "review_merge_range", "post_merge_audit")]
assert all(git("cat-file", "-t", pin + ":copier_template/" + p) == "blob" for p in paths)
print("lineage: physical equality, regular executable, HEAD=pin, 8/8 blobs, Python 3.12/Darwin")
LINEAGE
proof_role=coder
case "$proof_role" in
  coder) proof_xml=docs/code_reviews/assets/261114_1735_contract_upgrade_ff0a16b_3f5b2c1/contract_upgrade.coder.junit.xml ;;
  reviewer) proof_xml=docs/code_reviews/assets/261114_1735_contract_upgrade_ff0a16b_3f5b2c1/contract_upgrade.review.junit.xml ;;
  *) exit 2 ;;
esac
test ! -e ".tmp/contract-template-proof/$proof_role/head.before"
test ! -e ".tmp/contract-template-proof/$proof_role/snapshot.before.json"
git rev-parse HEAD > ".tmp/contract-template-proof/$proof_role/head.before"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 ../runtime-3f5b2c1/bin/planveyor --project "$PWD" \
  planveyor_review_target_snapshot docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md --current-bundle \
  > ".tmp/contract-template-proof/$proof_role/snapshot.before.json"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 make db-proof JUNIT="$proof_xml"
git rev-parse HEAD > ".tmp/contract-template-proof/$proof_role/head.after"
PLANVEYOR_RUNTIME_ROOT=../runtime-3f5b2c1 ../runtime-3f5b2c1/bin/planveyor --project "$PWD" \
  planveyor_review_target_snapshot docs/plans/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md --current-bundle \
  > ".tmp/contract-template-proof/$proof_role/snapshot.after.json"
cmp ".tmp/contract-template-proof/$proof_role/head.before" ".tmp/contract-template-proof/$proof_role/head.after"
cmp ".tmp/contract-template-proof/$proof_role/snapshot.before.json" ".tmp/contract-template-proof/$proof_role/snapshot.after.json"
cat "$proof_xml"
shasum -a 256 "$proof_xml"
```

В обоих proof обязательны unchanged HEAD и canonical bundle_sha256; любое target edit требует нового owning snapshot/proof. Fresh XML: 9 exact testcase identities, failures/errors/skipped=0, без unknown/missing/duplicate identities и без counter mismatch. Зелёные totals не перекрывают red testcase. Historical red offline attempt `87/6/0`, любой synthetic offline JUnit и contextual-only `db-state` не являются live SQL proof. В evidence каждой роли записываются portable bound make command, terminal make/wrapper rc отдельно, HEAD, canonical bundle_sha256 до/после, relative XML path/SHA-256 и identities/counts. Publish допускается только после непосредственно предшествующего one-query guard: DB_NAME=settings, database marker exists без чтения значения, sysadmin=0, Northwind case/padding запрещены; роли не меняют сервер/права/config и не читают credential values. JUNIT path/Git/config guard — до удаления/build/SQL; старый XML не proof; RunAll без параметров и unchanged XmlResultFormatter. Raw streams/argv/server values в evidence запрещены.

- `GetReorderCandidatesTests`: `test T1 empty Products returns empty result`; `test T2 active shortage is returned`; `test T3 zero and negative shortage excluded`; `test T4 on order units cover shortage`; `test T5 discontinued products excluded`; `test T6 numeric nulls treated as zero`; `test T7 smallint arithmetic does not overflow`; `test T8 result metadata and ProductID order`.
- `StackAdaptationTests`: `test Products table exists` — real `dbo.Products` type U, без FakeTable/NewTestClass/чтения бизнес-данных.

## Review route

- Один review carrier: `docs/code_reviews/261114_1735_contract_upgrade_ff0a16b_3f5b2c1.md`; two independent XML и fixture/snapshot receipts — его supporting evidence, не отдельные review lanes.
- `review_staged_or_commit` — основной exact bundle review; `review_merge_range` и `post_merge_audit` — только declared contextual consumers без новых targets.
- Reviewer сравнивает пять mutable targets с selected pin/template и сохраняет все восемь local tails/full matrix files; Coder AC1–AC5 receipt уже materialized и reuse-only.
- Architect после accepted review делает свой bound `make db-state` contextual readback и canonical closeout в своей authority; Planner/Coder не stage/commit/Done writers.

## Notes / stop boundaries

- Setup consumed: terminal session 58890 rc0 и prerequisites6/6 + continuity — facts, не новая launch ветка. Ни одна роль не запускает новый setup/install/restore/Extract; retained fixtures/receipts не reseed, не удалять и не перезаписывать. Historical Q1 exception из старых review stamps не даёт второй attempt.
- C-Q3 literal command binding к уже выбранному root обязателен для каждой make/direct-facade call. `selected_runtime_from_header` задаётся caller из exact current role control header в том же owning exec как task-local nonexported input. Inherited ROOT/known historical receipts/root поиска не заменяют comparison.
- Runtime-lineage mismatch — owning Architect stop до tests/SQL; без fallback, нового runtime, PATH/PYBIN/home/config/global environment изменений. Successful earlier db-build/lint сохраняются при continuity, historical red test не исправлен автоматически.
- Current bound test/check-secrets и два independent live SQL proof ещё не выполнены этим restamp. Product scope/targets/MAD/proof guards/XML paths неизменны.

## Review stamps (append-only)

- [2026-11-14 19:20 +0300] (Planner) Exact пять targets и derived N-A ref; runnable fixture/proof contract финализирован без product edits. Gate results принадлежат plan Evidence.
- [2026-11-14 19:56 +0300] (Planner) По Decisions 8 исправлены оба before/after snapshot calls на public entrypoint, синхронизированы non-login gate и current Coder resume. Exact targets/MAD/deleted_paths/JUnit/test identities сохранены; исторический stamp не заменяет fresh preflight.
- [2026-11-14 22:36 +0300] (Planner) По фактическому Owner Q1/Decisions 9 согласован future Coder C-Q2 one-attempt preparation contract; historical setup ban сохранён как запрет вне exact exception. Пять targets/MAD/девять identities/два JUnit прежние; setup не запускался Planner.
- [2026-11-14 22:45 +0300] (Planner) Second opinion уточнил terminal receipt reuse без повторного setup/before overwrite и self-contained SQL task role/XML pairing после отдельного exec. Exact Owner command/одна attempt и product targets прежние; setup не выполнялся.
- [2026-11-14 23:28 +0300] (Planner) По Decisions 9–10/C-Q3 executable handoff restamped: literal child ROOT binding, same-exec physical equality/pin/regular executable/8 blobs preflight и consumed/reuse-only setup. Coder resume начинается с fresh bound test/check-secrets; Reviewer сохраняет independent full offline/SQL lane. Все retained receipts/fixtures, реальные setup/db-build/lint rc0, exact targets/MAD/guards/два XML сохранены; Planner не запускал project setup/make/SQL.

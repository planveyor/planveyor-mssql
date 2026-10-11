"""Portable make entrypoint for the declared macOS SQL Server development stack.

Only this wrapper reads live credentials. Child streams and argv never reach
public output; the XML artifact is reconstructed from validated semantic fields.
"""
from __future__ import annotations

import ctypes
import errno
import io
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unicodedata
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
KEYS = ('SQLCMDSERVER', 'SQLCMDDBNAME', 'SQLCMDUSER', 'SQLCMDPASSWORD')
GIT_OVERRIDES = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE')
PROJECTS = ('sql/Northwind/Northwind.sqlproj', 'sql/tests/Northwind.Tests.sqlproj')
CANARY_CLASS = 'StackAdaptationTests'
CANARY_NAME = 'test Products table exists'
CATEGORIES = {0: 'success', 1: 'test', 2: 'configuration', 3: 'target',
              4: 'connection', 5: 'build-or-lint', 6: 'publish'}
SECURITY_DIRS = frozenset(('security', 'users', 'roles', 'permissions', 'logins',
                          'rolemembership', 'rolememberships', 'applicationroles',
                          'databaseroles', 'serverroles', 'credentials'))
EXTRACT_COUNTS = {'tables': 13, 'views': 16, 'stored procedures': 7}
EXTRACT_CATEGORIES = {'table': 'tables', 'tables': 'tables', 'view': 'views', 'views': 'views',
                      'storedprocedures': 'stored procedures', 'storedprocedure': 'stored procedures',
                      'procedure': 'stored procedures', 'procedures': 'stored procedures'}
GUARD_SQL = """SET NOCOUNT ON;
SELECT CONVERT(varchar(max), CONVERT(varbinary(max), DB_NAME()), 2),
       CASE WHEN EXISTS (SELECT 1 FROM sys.extended_properties
                         WHERE class = 0 AND major_id = 0 AND minor_id = 0
                           AND name = N'planveyor.designated_dev') THEN 1 ELSE 0 END,
       IS_SRVROLEMEMBER(N'sysadmin');"""
STATE_SQL = """SET NOCOUNT ON;
SELECT N'BEGIN' COLLATE DATABASE_DEFAULT;
SELECT N'SCHEMA|' COLLATE DATABASE_DEFAULT + name COLLATE DATABASE_DEFAULT
FROM sys.schemas WHERE schema_id < 16384 AND name NOT IN (N'dbo', N'guest', N'INFORMATION_SCHEMA', N'sys');
SELECT N'OBJECT|' COLLATE DATABASE_DEFAULT + SCHEMA_NAME(schema_id) COLLATE DATABASE_DEFAULT
       + N'.' COLLATE DATABASE_DEFAULT + name COLLATE DATABASE_DEFAULT
       + N'|' COLLATE DATABASE_DEFAULT + type COLLATE DATABASE_DEFAULT
FROM sys.objects WHERE is_ms_shipped = 0 AND type IN ('U', 'V', 'P');
IF OBJECT_ID(N'tSQLt.TestClasses', N'V') IS NOT NULL
    EXEC(N'SELECT N''CLASS|'' COLLATE DATABASE_DEFAULT + Name COLLATE DATABASE_DEFAULT FROM tSQLt.TestClasses;');
IF OBJECT_ID(N'tSQLt.TestResult', N'U') IS NOT NULL
    EXEC(N'SELECT N''RESULT|'' COLLATE DATABASE_DEFAULT + Class COLLATE DATABASE_DEFAULT
         + N''|'' COLLATE DATABASE_DEFAULT + TestCase COLLATE DATABASE_DEFAULT
         + N''|'' COLLATE DATABASE_DEFAULT + Result COLLATE DATABASE_DEFAULT FROM tSQLt.TestResult;');
SELECT N'END' COLLATE DATABASE_DEFAULT;"""


class Refusal(Exception):
    def __init__(self, code: int, phase: str, reason: str):
        self.code, self.phase, self.reason = code, phase, reason
        super().__init__(reason)


def refuse(code, phase, reason):
    raise Refusal(code, phase, reason)


def subprocess_executor(argv, *, cwd, env, timeout):
    return subprocess.run(argv, cwd=cwd, env=env, timeout=timeout,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                          encoding='utf-8', errors='replace', check=False)


def safe_path(root: Path, value: str, *, xml=False) -> Path:
    """Reject escapes, links and aliases of existing filesystem entries."""
    p = PurePosixPath(value)
    if (not value or p.is_absolute() or '\\' in value or '\x00' in value
            or any(x in ('', '.', '..') for x in value.split('/'))
            or (xml and p.suffix != '.xml')):
        refuse(2, 'path', 'invalid-relative-path')
    current = root
    for part in p.parts:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            continue
        except OSError:
            refuse(2, 'path', 'unknown-filesystem-entry')
        if stat.S_ISLNK(mode):
            refuse(2, 'path', 'symlink')
        try:
            # On case-insensitive filesystems lstat also accepts an alias. The
            # actual directory spelling must match, including each ancestor.
            if part not in os.listdir(current.parent):
                refuse(2, 'path', 'filesystem-alias')
        except OSError:
            refuse(2, 'path', 'unknown-filesystem-entry')
        if current != root / p and not stat.S_ISDIR(mode):
            refuse(2, 'path', 'invalid-ancestor')
        if current == root / p and not stat.S_ISREG(mode):
            refuse(2, 'path', 'non-regular-file')
    return current


def directory_exchange(new: Path, old: Path):
    """Darwin RENAME_SWAP exchanges two real directory entries atomically."""
    if old.is_symlink() or not old.is_dir() or new.is_symlink() or not new.is_dir():
        refuse(5, 'extract', 'invalid-swap-directory')
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renamex_np
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(os.fsencode(new), os.fsencode(old), 0x00000002) != 0:
        # errno is deliberately not accompanied by private paths/raw exception.
        refuse(5, 'extract', 'atomic-exchange-failed')


def normalize_extract(tree: Path):
    counts = dict.fromkeys(EXTRACT_COUNTS, 0)
    # Validate types before pruning: an ignored security name must not hide a link.
    for base, dirs, files in os.walk(tree, followlinks=False):
        for name in dirs + files:
            p = Path(base) / name
            mode = p.lstat().st_mode
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                refuse(2, 'extract', 'unsafe-artifact-type')
    for base, dirs, _ in os.walk(tree, topdown=True):
        for name in list(dirs):
            if name.casefold().replace(' ', '') in SECURITY_DIRS:
                shutil.rmtree(Path(base) / name)
                dirs.remove(name)
    for p in sorted(tree.rglob('*')):
        if p.is_dir():
            continue
        if p.suffix.casefold() != '.sql':
            refuse(2, 'extract', 'unexpected-artifact-file')
        relative = p.relative_to(tree)
        categories = [EXTRACT_CATEGORIES[x.casefold().replace(' ', '')]
                      for x in relative.parts[:-1] if x.casefold().replace(' ', '') in EXTRACT_CATEGORIES]
        if len(categories) != 1:
            refuse(2, 'extract', 'unexpected-artifact-category')
        counts[categories[0]] += 1
        try:
            sql = p.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError):
            refuse(2, 'extract', 'unreadable-artifact')
        # Comments cannot separate otherwise forbidden keywords undetected.
        sql = re.sub(r'/\*.*?\*/|--[^\n]*', ' ', sql, flags=re.S)
        if re.search(r'\b(?:CREATE\s+USER|ALTER\s+ROLE|GRANT|INSERT)\b', sql, re.I):
            refuse(2, 'extract', 'forbidden-source-sql')
    if counts != EXTRACT_COUNTS:
        refuse(2, 'extract', 'artifact-count-mismatch')
    return counts


def parse_junit(raw: str):
    if re.search(r'<!DOCTYPE|<!ENTITY', raw, re.I):
        refuse(1, 'junit', 'xml-declaration-forbidden')
    try:
        root = ET.fromstring(raw.strip())
    except (ET.ParseError, ValueError):
        refuse(1, 'junit', 'invalid-xml')
    if root.tag not in ('testsuite', 'testsuites'):
        refuse(1, 'junit', 'unsupported-root')
    suites = [root] if root.tag == 'testsuite' else list(root)
    if len(suites) != 1 or suites[0].tag != 'testsuite':
        refuse(1, 'junit', 'ambiguous-suite')
    suite = suites[0]
    if suite.get('name') not in (CANARY_CLASS, '[' + CANARY_CLASS + ']'):
        refuse(1, 'junit', 'unexpected-suite')
    cases = list(suite.findall('testcase'))
    if len(cases) != 1 or len(list(root.iter('testcase'))) != 1:
        refuse(1, 'junit', 'ambiguous-testcase')
    case = cases[0]
    accepted_names = {CANARY_NAME, '[' + CANARY_NAME + ']',
                      CANARY_CLASS + '.' + CANARY_NAME,
                      '[' + CANARY_CLASS + '].[' + CANARY_NAME + ']'}
    if case.get('name') not in accepted_names or case.get('classname') not in (CANARY_CLASS, '[' + CANARY_CLASS + ']'):
        refuse(1, 'junit', 'unexpected-testcase')
    status_counts = [len(list(case.iter(tag))) for tag in ('failure', 'error', 'skipped')]
    if any(n > 1 for n in status_counts) or sum(status_counts) > 1:
        refuse(1, 'junit', 'duplicate-result')
    expected = dict(zip(('tests', 'failures', 'errors', 'skipped'), [1] + status_counts))
    for node in ([suite, root] if root is not suite else [suite]):
        # Native tSQLt suite counters are required; root totals are optional.
        required = ('tests', 'failures', 'errors', 'skipped') if node is suite else ()
        for key in expected:
            value = node.get(key)
            if value is None:
                if key in required:
                    refuse(1, 'junit', 'missing-count')
                continue
            if not re.fullmatch(r'0|[1-9][0-9]*', value) or int(value) != expected[key]:
                refuse(1, 'junit', 'inconsistent-count')
    if any(n.tag not in ('testcase', 'properties', 'system-out', 'system-err') for n in suite):
        refuse(1, 'junit', 'invalid-suite-layout')
    if any(n.tag not in ('failure', 'error', 'skipped') for n in case):
        refuse(1, 'junit', 'invalid-case-layout')
    if len(list(root.iter('failure'))) + len(list(root.iter('error'))) + len(list(root.iter('skipped'))) != sum(status_counts):
        refuse(1, 'junit', 'misplaced-result')
    allowed = {'testsuites', 'testsuite', 'testcase', 'failure', 'error', 'skipped',
               'properties', 'property', 'system-out', 'system-err'}
    if any(n.tag not in allowed for n in root.iter()):
        refuse(1, 'junit', 'unsupported-xml-element')
    # Reconstruct only trusted semantic fields. No hostname, timings, properties,
    # paths, connection strings, raw messages or system streams survive.
    clean = ET.Element('testsuites', {k: str(v) for k, v in expected.items()})
    clean_suite = ET.SubElement(clean, 'testsuite', name=CANARY_CLASS,
                                **{k: str(v) for k, v in expected.items()})
    clean_case = ET.SubElement(clean_suite, 'testcase', classname=CANARY_CLASS, name=CANARY_NAME)
    for tag, n in zip(('failure', 'error', 'skipped'), status_counts):
        if n:
            ET.SubElement(clean_case, tag, message='SQL test ' + tag).text = 'Details redacted'
    return ET.tostring(clean, encoding='utf-8', xml_declaration=True) + b'\n', expected


def atomic_write(path: Path, data: bytes):
    temp = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.junit-', delete=False) as f:
            temp = Path(f.name)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
        temp = None
    except OSError:
        refuse(1, 'junit', 'atomic-write-failed')
    finally:
        if temp is not None:
            try:
                temp.unlink(missing_ok=True)
            except OSError:
                pass


class Stack:
    def __init__(self, root=ROOT, *, executor=subprocess_executor, environ=None):
        self.root = Path(root).resolve()
        self.executor = executor
        self.env = dict(os.environ if environ is None else environ)
        self.connection = None
        cache = self.root / '.tmp'
        self.env.update({
            'DOTNET_CLI_HOME': str(cache / 'dotnet-home'),
            'DOTNET_SKIP_FIRST_TIME_EXPERIENCE': '1', 'DOTNET_NOLOGO': '1',
            'DOTNET_CLI_TELEMETRY_OPTOUT': '1', 'DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE': 'true',
            'MSBuildEnableWorkloadResolver': 'false',
            'NUGET_PACKAGES': str(cache / 'nuget/packages'),
            'NUGET_HTTP_CACHE_PATH': str(cache / 'nuget/http-cache'),
            'NUGET_PLUGINS_CACHE_PATH': str(cache / 'nuget/plugins-cache'),
            'PIP_CACHE_DIR': str(cache / 'pip-cache'),
            'PYTHONDONTWRITEBYTECODE': '1', 'DOTNET_CLI_UI_LANGUAGE': 'en-US',
        })
        # Ambient connection settings never choose a target or leak into children.
        for key in KEYS:
            self.env.pop(key, None)

    def run(self, argv, *, timeout, code, phase, return_failure=False):
        try:
            result = self.executor(list(map(str, argv)), cwd=self.root,
                                   env=self.env.copy(), timeout=timeout)
        except subprocess.TimeoutExpired:
            refuse(code, phase, 'timeout')
        except (OSError, ValueError):
            refuse(code, phase, 'launch-failed')
        if result.returncode and not return_failure:
            refuse(code, phase, 'command-failed')
        return result

    def git_environment(self):
        # Presence is operational-red, including an explicitly empty override.
        # Do not silently neutralize it or query a different index/worktree.
        if any(key in self.env for key in GIT_OVERRIDES):
            refuse(2, 'git', 'ambient-git-override')

    def git(self, *args):
        self.git_environment()
        # ls-files accepts pathspecs; check-ignore has literal path arguments and
        # rejects --literal-pathspecs. Its only caller uses fixed .env.local.
        literal = ['--literal-pathspecs'] if args[0] == 'ls-files' else []
        return self.run(['git', *literal, *args], timeout=10,
                        code=2, phase='git', return_failure=True)

    def untracked(self, relative):
        root = self.git('rev-parse', '--show-toplevel')
        if root.returncode or root.stderr or root.stdout.strip() != str(self.root):
            refuse(2, 'git', 'unknown-project-root')
        indexed = self.git('ls-files', '--stage', '-z', '--', relative)
        if indexed.returncode or indexed.stdout or indexed.stderr:
            refuse(2, 'git', 'tracked-or-unknown')
        path = self.root / relative
        try:
            identity = path.stat()
        except FileNotFoundError:
            identity = None
        except OSError:
            refuse(2, 'git', 'unknown-filesystem-identity')
        # Index tracking survives worktree deletion, including all ancestors.
        # A caseless/normalization alias cannot be certified untracked from a
        # literal lookup or a missing inode. Fail closed on that ambiguity.
        alias = unicodedata.normalize('NFD', relative).casefold()
        inventory = self.git('ls-files', '--cached', '-z')
        if (inventory.returncode or inventory.stderr
                or '\ufffd' in inventory.stdout
                or (inventory.stdout and not inventory.stdout.endswith('\x00'))):
            refuse(2, 'git', 'unknown-index-inventory')
        for name in inventory.stdout.split('\x00')[:-1]:
            indexed_path = PurePosixPath(name)
            if (not name or indexed_path.is_absolute()
                    or any(part in ('', '.', '..') for part in name.split('/'))):
                refuse(2, 'git', 'unknown-index-inventory')
            if unicodedata.normalize('NFD', name).casefold() == alias:
                refuse(2, 'git', 'tracked-or-unknown')
            if identity is None:
                continue
            # Case-only renames and hard links can give an existing tracked
            # file a different literal spelling; retain physical identity too.
            try:
                tracked = (self.root / indexed_path).stat()
            except FileNotFoundError:
                continue
            except OSError:
                refuse(2, 'git', 'unknown-filesystem-identity')
            if (identity.st_dev, identity.st_ino) == (tracked.st_dev, tracked.st_ino):
                refuse(2, 'git', 'tracked-or-unknown')

    def config(self):
        self.git_environment()
        path = safe_path(self.root, '.env.local')
        try:
            if stat.S_IMODE(path.stat().st_mode) != 0o600 or not path.stat().st_mode & stat.S_IRUSR:
                refuse(2, 'configuration', 'dotenv-permissions')
        except OSError:
            refuse(2, 'configuration', 'dotenv-missing')
        self.untracked('.env.local')
        ignored = self.git('check-ignore', '--no-index', '-q', '--', '.env.local')
        if ignored.returncode != 0 or ignored.stdout or ignored.stderr:
            refuse(2, 'configuration', 'dotenv-not-ignored')
        try:
            lines = path.read_text(encoding='utf-8').splitlines()
        except (OSError, UnicodeError):
            refuse(2, 'configuration', 'dotenv-unreadable')
        values = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, sep, value = line.partition('=')
            key, value = key.strip(), value.strip()
            if not sep or key not in KEYS or key in values:
                refuse(2, 'configuration', 'dotenv-invalid-key')
            if value[:1] in ('"', "'"):
                if len(value) < 2 or value[-1] != value[0]:
                    refuse(2, 'configuration', 'dotenv-invalid-quote')
                value = value[1:-1]
            if not value or '\x00' in value:
                refuse(2, 'configuration', 'dotenv-empty-value')
            values[key] = value
        if set(values) != set(KEYS):
            refuse(2, 'configuration', 'dotenv-missing-key')
        self.connection = values
        self.env.update(values)
        return values

    def tools(self, *, live=False, dotnet=True):
        if sys.version_info[:2] != (3, 12) or platform.system() != 'Darwin':
            refuse(2, 'environment', 'python-or-platform')
        if dotnet:
            if not shutil.which('dotnet', path=self.env.get('PATH')):
                refuse(2, 'environment', 'dotnet-missing')
            version = self.run(['dotnet', '--version'], timeout=30, code=2, phase='environment').stdout.strip()
            match = re.fullmatch(r'10\.0\.([0-9]+)', version)
            if not match or int(match[1]) < 401:
                refuse(2, 'environment', 'sdk-version')
        if live:
            if not shutil.which('sqlcmd', path=self.env.get('PATH')):
                refuse(2, 'environment', 'sqlcmd-missing')
            info = self.run(['sqlcmd', '--version'], timeout=10, code=2, phase='environment').stdout
            if 'go-sqlcmd' not in info and not ('Version:' in info and 'Create/Query SQL Server' in info):
                refuse(2, 'environment', 'go-sqlcmd-required')

    def setup(self):
        self.tools()
        deadline = time.monotonic() + 600
        def install(argv):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                refuse(2, 'setup', 'timeout')
            self.run(argv, timeout=remaining, code=2, phase='setup')
        cache = self.root / '.tmp'
        cache.mkdir(exist_ok=True)
        install([sys.executable, '-m', 'venv', cache / 'venv'])
        install([cache / 'venv/bin/python', '-m', 'pip', 'install', '-r', 'requirements-dev.txt'])
        install(['dotnet', 'tool', 'restore', '--configfile', 'NuGet.Config'])
        for project in PROJECTS:
            install(['dotnet', 'restore', project, '--configfile', 'NuGet.Config'])
        (cache / 'setup.complete').write_text('SQLFluff=3.4.2\nSqlPackage=170.5.96\nMicrosoft.Build.Sql=2.3.0\ntSQLt.Dacpacs=1.0.8083.3529\n')

    def cache(self):
        required = ('.tmp/setup.complete', '.tmp/venv/bin/sqlfluff',
                    '.tmp/nuget/packages/microsoft.build.sql/2.3.0',
                    '.tmp/nuget/packages/tsqlt.dacpacs/1.0.8083.3529',
                    '.tmp/build/Northwind/obj/project.assets.json',
                    '.tmp/build/Northwind.Tests/obj/project.assets.json')
        if any(not (self.root / p).exists() for p in required):
            refuse(5, 'cache', 'setup-cache-missing')

    def build(self):
        self.cache()
        self.tools()
        for project in PROJECTS:
            self.run(['dotnet', 'build', project, '--no-restore', '--configuration', 'Debug',
                      '/p:NuGetAudit=false'], timeout=300, code=5, phase='build')

    def lint(self):
        self.cache()
        self.tools(dotnet=False)
        result = self.run([self.root / '.tmp/venv/bin/sqlfluff', 'lint', '--format', 'json',
                           'sql/Northwind/Authored', 'sql/tests'], timeout=300, code=5,
                          phase='lint', return_failure=True)
        if result.returncode:
            try:
                reports = json.loads(result.stdout)
                codes = sorted({v['code'] for report in reports for v in report['violations']
                                if re.fullmatch(r'[A-Z][A-Z0-9]{2,8}', v['code'])})
                print('lint rule-codes=' + ','.join(codes))
                for report in reports:
                    name = report.get('filepath', '')
                    if name in ('sql/tests/StackAdaptationTests/StackAdaptationTests.sql',
                                'sql/tests/StackAdaptationTests/test_Products_table_exists.sql'):
                        for v in report['violations']:
                            if v['code'] in codes and isinstance(v.get('start_line_no'), int):
                                print(f'lint file={name} line={v["start_line_no"]} rule={v["code"]}')
            except (ValueError, TypeError, KeyError):
                pass
            refuse(5, 'lint', 'command-failed')

    def sqlpackage(self, *args):
        return ['dotnet', 'tool', 'run', 'sqlpackage', '--', *args]

    def connection_args(self, kind, database=None):
        values = self.connection
        return [f'/{kind}ServerName:{values[KEYS[0]]}',
                f'/{kind}DatabaseName:{database or values[KEYS[1]]}',
                f'/{kind}User:{values[KEYS[2]]}', f'/{kind}Password:{values[KEYS[3]]}',
                f'/{kind}EncryptConnection:True', f'/{kind}TrustServerCertificate:True']

    def extract(self):
        self.config()
        self.cache()
        self.tools(live=True)
        old = self.root / 'sql/Northwind/Imported'
        if old.is_symlink() or not old.is_dir():
            refuse(2, 'extract', 'invalid-imported-host')
        with tempfile.TemporaryDirectory(dir=old.parent, prefix='.extract-') as temp:
            tree = Path(temp) / 'schema'
            self.run(self.sqlpackage('/Action:Extract', f'/TargetFile:{tree}',
                                     *self.connection_args('Source', 'Northwind'),
                                     '/p:ExtractTarget=SchemaObjectType', '/p:ExtractAllTableData=False',
                                     '/p:ExtractReferencedServerScopedElements=False'),
                     timeout=300, code=5, phase='extract')
            if not tree.is_dir() or tree.is_symlink():
                refuse(5, 'extract', 'missing-artifact-tree')
            normalize_extract(tree)
            directory_exchange(tree, old)

    def sqlcmd(self, query, phase, timeout, *, xml=False, return_failure=False):
        argv = ['sqlcmd', '--encrypt-connection=mandatory', '-C', '-b',
                '-S', self.connection[KEYS[0]], '-d', self.connection[KEYS[1]],
                '-U', self.connection[KEYS[2]], '-h', '-1']
        argv.extend(['-y', '0', '-w', '65535'] if xml else ['-W', '-s', '|'])
        argv.extend(['-Q', query])
        return self.run(argv, timeout=timeout, code=4, phase=phase, return_failure=return_failure)

    def guard(self):
        if self.connection[KEYS[1]].strip().casefold() == 'northwind':
            refuse(3, 'target', 'readonly-source')
        result = self.sqlcmd(GUARD_SQL, 'target', 60)
        lines = [x.strip() for x in result.stdout.splitlines() if x.strip()]
        if len(lines) != 1:
            refuse(3, 'target', 'ambiguous-readback')
        fields = [x.strip() for x in lines[0].split('|')]
        try:
            name = bytes.fromhex(fields[0]).decode('utf-16-le')
        except (ValueError, UnicodeError, IndexError):
            refuse(3, 'target', 'invalid-readback')
        if len(fields) != 3 or name != self.connection[KEYS[1]] or fields[1:] != ['1', '0']:
            refuse(3, 'target', 'rejected-readback')

    def junit_path(self, value):
        self.git_environment()
        path = safe_path(self.root, value, xml=True)
        self.untracked(path.relative_to(self.root).as_posix())
        return path

    def proof(self, value):
        path = self.junit_path(value)  # before config/cache/build/tool/SQL activity
        self.config()                 # invalid config also preserves old XML
        self.tools(live=True)
        try:
            path.unlink(missing_ok=True)
        except OSError:
            refuse(2, 'junit', 'old-proof-removal-failed')
        self.build()
        dacpac = self.root / '.tmp/build/Northwind.Tests/bin/Debug/Northwind.Tests.dacpac'
        if not dacpac.is_file():
            refuse(5, 'build', 'dacpac-missing')
        publish = self.sqlpackage('/Action:Publish', f'/SourceFile:{dacpac}',
                                  *self.connection_args('Target'),
                                  '/p:IncludeCompositeObjects=True', '/p:DropObjectsNotInSource=True',
                                  '/p:ExcludeObjectTypes=Users;Logins;RoleMembership;Permissions',
                                  '/p:DropExtendedPropertiesNotInSource=False',
                                  '/p:ScriptDatabaseOptions=False', '/p:BlockOnPossibleDataLoss=True')
        self.guard()                   # exactly the immediate predecessor of Publish
        self.run(publish, timeout=300, code=6, phase='publish')
        run = self.sqlcmd('EXEC tSQLt.RunAll;', 'run-all', 120, return_failure=True)
        if run.returncode:
            text = run.stdout + '\n' + run.stderr
            # A summary heading alone also occurs after successful tests. Only
            # positive failure/error counts or explicit results prove test rc 1.
            is_test = bool(re.search(r'\b(?:Failures|Errors):\s*[1-9][0-9]*|'
                                     r'\b[1-9][0-9]*\s+(?:failed|errored|Failures|Errors)\b|'
                                     r'\[(?:Fail|Error)\]', text, re.I))
            refuse(1 if is_test else 4, 'run-all', 'test-failed' if is_test else 'read-failed')
        xml = self.sqlcmd('EXEC tSQLt.XmlResultFormatter;', 'formatter', 60, xml=True).stdout
        data, counts = parse_junit(xml)
        # Recheck custody before durable replacement; no rediscovery/reseed.
        if self.junit_path(value) != path:
            refuse(2, 'junit', 'path-changed')
        atomic_write(path, data)
        if counts != {'tests': 1, 'failures': 0, 'errors': 0, 'skipped': 0}:
            refuse(1, 'junit', 'test-result-not-green')
        print('JUnit tests=1 failures=0 errors=0 skipped=0; StackAdaptationTests.test Products table exists')

    def state(self):
        self.config()
        self.tools(live=True, dotnet=False)
        result = self.sqlcmd(STATE_SQL, 'state', 60)
        lines = [x.strip() for x in result.stdout.splitlines() if x.strip()]
        if len(lines) < 2 or lines[0] != 'BEGIN' or lines[-1] != 'END':
            refuse(4, 'state', 'incomplete-catalog-readback')
        inventory = {'SCHEMA': [], 'OBJECT': [], 'CLASS': [], 'RESULT': []}
        for line in lines[1:-1]:
            fields = line.split('|')
            category = fields[0]
            length = {'SCHEMA': 2, 'OBJECT': 3, 'CLASS': 2, 'RESULT': 4}.get(category)
            if length is None or len(fields) != length or any(not x for x in fields):
                refuse(4, 'state', 'invalid-catalog-readback')
            inventory[category].append(fields[1:])
        # Do not echo arbitrary catalog identifiers/messages; counts and bounded
        # known canary fields are sufficient contextual readback without secrets.
        objects = inventory['OBJECT']
        products = sum(x == ['dbo.Products', 'U'] for x in objects)
        if products > 1:
            refuse(4, 'state', 'ambiguous-catalog-readback')
        print('db-state schemas={0} objects={1} test-classes={2} last-results={3}; Products-U={4}'.format(
            *(len(inventory[x]) for x in ('SCHEMA', 'OBJECT', 'CLASS', 'RESULT')), products))
        if not objects:
            print('db-state empty')
        if not inventory['RESULT']:
            print('db-state not-tested')
        else:
            counts = {name: sum(x[2] == name for x in inventory['RESULT']) for name in ('Success', 'Failure', 'Error')}
            if sum(counts.values()) != len(inventory['RESULT']):
                refuse(4, 'state', 'invalid-result-readback')
            print('db-state last-results Success={Success} Failure={Failure} Error={Error}; contextual-only'.format(**counts))

    def secrets(self, junit=''):
        known = self.git('ls-files', '-z', '--cached', '--others', '--exclude-standard')
        if known.returncode or known.stderr or (known.stdout and not known.stdout.endswith('\x00')):
            refuse(2, 'secrets', 'unknown-git-inventory')
        paths = set(known.stdout.rstrip('\x00').split('\x00')) if known.stdout else set()
        if junit:
            paths.add(self.junit_path(junit).relative_to(self.root).as_posix())
        asset_root = self.root / 'docs/code_reviews/assets'
        if asset_root.exists():
            paths.update(p.relative_to(self.root).as_posix() for p in asset_root.rglob('*.xml'))
        leak = re.compile(r'(?:SQLCMDSERVER|SQLCMDPASSWORD)\s*=\s*(?!<|\$|[\'\"]?\s*$)[^\s]+|'
                          r'(?:Server|Data Source|Password|Pwd)\s*=\s*[^;\s<>]+\s*;|'
                          r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|'
                          r'(?<![A-Za-z0-9_])/Users/[A-Za-z0-9_.-]+/', re.I)
        for relative in sorted(paths):
            if any(x in ('.git', '.tmp', '.env.local') for x in PurePosixPath(relative).parts):
                continue
            path = safe_path(self.root, relative)
            if not path.exists():
                continue
            try:
                data = path.read_bytes()
            except OSError:
                refuse(2, 'secrets', 'unreadable-file')
            if b'\x00' in data:
                continue
            if leak.search(data.decode('utf-8', 'replace')):
                print('secrets rejected-file=' + json.dumps(relative, ensure_ascii=True))
                refuse(2, 'secrets', 'sensitive-content')


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    phase = args[0] if len(args) == 1 else 'command'
    stack = Stack()
    try:
        stack.git_environment()
        if sys.version_info[:2] != (3, 12) or platform.system() != 'Darwin':
            refuse(2, 'environment', 'python-or-platform')
        if phase == 'test':
            suite = unittest.defaultTestLoader.discover(str(ROOT / 'scripts'), pattern='test_sql.py')
            result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=1).run(suite)
            print(f'offline tests={result.testsRun} failures={len(result.failures)} errors={len(result.errors)}')
            for test, _ in result.failures + result.errors:
                print('offline failed=' + test.id())
            code = 0 if result.wasSuccessful() else 1
        elif phase in ('setup', 'db-extract', 'db-build', 'lint', 'db-proof', 'db-state', 'check-secrets'):
            actions = {'setup': stack.setup, 'db-extract': stack.extract, 'db-build': stack.build,
                       'lint': stack.lint, 'db-proof': lambda: stack.proof(os.environ.get('JUNIT', '')),
                       'db-state': stack.state, 'check-secrets': lambda: stack.secrets(os.environ.get('JUNIT', ''))}
            actions[phase]()
            code = 0
        else:
            refuse(2, 'command', 'unsupported-goal')
    except Refusal as error:
        print(f'sql phase={error.phase} category={CATEGORIES[error.code]} rc={error.code} reason={error.reason}')
        return error.code
    except Exception:
        # Never print raw exception strings, even for unexpected filesystem/tool
        # failures: these may contain private paths, credentials, or child argv.
        print(f'sql phase={phase} category=configuration rc=2 reason=unexpected-failure')
        return 2
    print(f'sql phase={phase} category={CATEGORIES[code]} rc={code}')
    return code


if __name__ == '__main__':
    raise SystemExit(main())

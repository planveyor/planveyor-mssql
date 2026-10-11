"""Offline refusal/ordering tests; all connection values and SQL trees synthetic."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import sql

SYNTHETIC = dict(zip(sql.KEYS, ('fixture.invalid', 'DesignatedDev', 'fixture-user', 'fixture-secret')))
GOOD_XML = ('<testsuites><testsuite name="StackAdaptationTests" tests="1" failures="0" errors="0" skipped="0" '
            'hostname="fixture.invalid"><properties/><testcase classname="StackAdaptationTests" '
            'name="test Products table exists"/><system-out/><system-err/></testsuite></testsuites>')
LOCAL_FILES = ['docs/tools/prompts/' + name + '.md' for name in
               ('architect_status_driven', 'planner_status_driven', 'coder_status_driven',
                'coder_migrations_gate', 'reviewer_status_driven')] + [
               'docs/playbooks/' + name + '.md' for name in
               ('review_staged_or_commit', 'review_merge_range', 'post_merge_audit')]


def make_tree(tree):
    for category, count in sql.EXTRACT_COUNTS.items():
        directory = tree / category.title()
        directory.mkdir(parents=True)
        for i in range(count):
            name = 'CustOrderHist' if category == 'stored procedures' and i == 0 else 'Object' + str(i)
            (directory / (name + '.sql')).write_text('CREATE ' + ('TABLE' if category == 'tables' else
                'VIEW' if category == 'views' else 'PROCEDURE') + ' [' + name + '] AS SELECT 1;\n')


class FakeExecutor:
    def __init__(self, root):
        self.root, self.calls, self.overrides = root, [], {}
        self.xml, self.guard_output, self.state_output = GOOD_XML, None, 'BEGIN\nEND\n'
        self.extract_edit = lambda tree: None

    def __call__(self, argv, *, cwd, env, timeout):
        self.calls.append((argv, env.copy(), timeout))
        if argv[0] == 'git':
            kind = 'git:' + argv[2 if argv[1] == '--literal-pathspecs' else 1]
        elif '/Action:Extract' in argv:
            kind = 'extract'
        elif '/Action:Publish' in argv:
            kind = 'publish'
        elif argv[:2] == ['dotnet', '--version']:
            kind = 'version'
        elif argv[:2] == ['sqlcmd', '--version']:
            kind = 'sqlcmd-version'
        elif '-Q' in argv:
            query = argv[argv.index('-Q') + 1]
            kind = ('guard' if query == sql.GUARD_SQL else 'state' if query == sql.STATE_SQL else
                    'run-all' if query == 'EXEC tSQLt.RunAll;' else 'formatter')
        else:
            kind = 'build' if 'build' in argv else 'lint' if 'lint' in argv else 'setup'
        override = self.overrides.get(kind)
        if isinstance(override, Exception):
            raise override
        if override is not None:
            rc, out, err = override
            return subprocess.CompletedProcess(argv, rc, out, err)
        if kind.startswith('git:'):
            return sql.subprocess_executor(argv, cwd=cwd, env=env, timeout=timeout)
        out = ''
        if kind == 'version':
            out = '10.0.401\n'
        elif kind == 'sqlcmd-version':
            out = 'sqlcmd: Install/Create/Query SQL Server, Azure SQL, and Tools\nVersion: 1.10.0\n'
        elif kind == 'extract':
            tree = Path(next(x.split(':', 1)[1] for x in argv if x.startswith('/TargetFile:')))
            make_tree(tree)
            self.extract_edit(tree)
        elif kind == 'guard':
            name = env['SQLCMDDBNAME'].encode('utf-16-le').hex()
            out = self.guard_output if self.guard_output is not None else name + '|1|0\n'
        elif kind == 'formatter':
            out = self.xml
        elif kind == 'state':
            out = self.state_output
        return subprocess.CompletedProcess(argv, 0, out, '')


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        (self.root / '.gitignore').write_text('.env.local\n.tmp/\n')
        self.dotenv()
        self.fake = FakeExecutor(self.root)
        self.stack = sql.Stack(self.root, executor=self.fake)
        self.cache()
        (self.root / 'sql/Northwind/Imported').mkdir(parents=True)
        (self.root / 'sql/Northwind/Imported/old.sql').write_bytes(b'OLD BYTES\n')

    def dotenv(self, values=None):
        path = self.root / '.env.local'
        path.write_text('\n'.join(k + '=' + v for k, v in (values or SYNTHETIC).items()) + '\n')
        path.chmod(0o600)

    def cache(self):
        for p in ('.tmp/setup.complete', '.tmp/venv/bin/sqlfluff',
                  '.tmp/build/Northwind/obj/project.assets.json',
                  '.tmp/build/Northwind.Tests/obj/project.assets.json',
                  '.tmp/build/Northwind.Tests/bin/Debug/Northwind.Tests.dacpac'):
            path = self.root / p
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture')
        for p in ('.tmp/nuget/packages/microsoft.build.sql/2.3.0',
                  '.tmp/nuget/packages/tsqlt.dacpacs/1.0.8083.3529'):
            (self.root / p).mkdir(parents=True, exist_ok=True)

    def code(self, expected, action):
        with self.assertRaises(sql.Refusal) as caught:
            action()
        self.assertEqual(expected, caught.exception.code)
        return caught.exception

    def no_publish(self):
        self.assertFalse(any('/Action:Publish' in x[0] for x in self.fake.calls))

    def old_tree(self):
        tree = self.root / 'sql/Northwind/Imported'
        self.assertEqual(['old.sql'], sorted(p.name for p in tree.iterdir()))
        self.assertEqual(b'OLD BYTES\n', (tree / 'old.sql').read_bytes())

    def prove(self, path='reports/canary.xml'):
        return self.stack.proof(path)


class ConfigTests(Fixture):
    def test_missing_and_modes(self):
        path = self.root / '.env.local'
        path.unlink()
        self.code(2, self.stack.config)
        self.dotenv()
        for mode in (0o644, 0o400, 0):
            with self.subTest(mode=mode):
                path.chmod(mode)
                self.code(2, self.stack.config)
        self.assertTrue(all(c[0][0] == 'git' for c in self.fake.calls))

    def test_nonregular_and_symlink(self):
        path = self.root / '.env.local'
        path.unlink(); path.mkdir()
        self.code(2, self.stack.config)
        path.rmdir(); (self.root / 'secret').write_text('fixture')
        path.symlink_to('secret')
        self.code(2, self.stack.config)

    def test_not_ignored_and_tracked(self):
        (self.root / '.gitignore').write_text('')
        self.code(2, self.stack.config)
        subprocess.run(['git', '-C', str(self.root), 'add', '.env.local'], check=True)
        self.code(2, self.stack.config)

    def test_unreadable_and_invalid_utf8(self):
        with patch.object(Path, 'read_text', side_effect=PermissionError):
            self.code(2, self.stack.config)
        (self.root / '.env.local').write_bytes(b'\xff')
        self.code(2, self.stack.config)

    def test_keys_and_unknown_git(self):
        for text in ('', 'SQLCMDUSER=only', '\n'.join(k + '=' for k in sql.KEYS),
                     '\n'.join(k + '=fixture' for k in sql.KEYS) + '\nSQLCMDUSER=duplicate',
                     'UNKNOWN=fixture'):
            with self.subTest(text=text):
                (self.root / '.env.local').write_text(text)
                self.code(2, self.stack.config)
        self.dotenv()
        self.fake.overrides['git:rev-parse'] = (128, '', 'fixture-secret')
        self.code(2, self.stack.config)
        self.fake.overrides.pop('git:rev-parse')
        self.fake.overrides['git:ls-files'] = (128, '', '')
        self.code(2, self.stack.config)

    def test_values_are_data(self):
        values = dict(SYNTHETIC)
        values[sql.KEYS[-1]] = "'literal $() ; `data`'"
        self.dotenv(values)
        self.assertEqual("literal $() ; `data`", self.stack.config()[sql.KEYS[-1]])
        self.assertEqual('fixture.invalid', self.stack.connection[sql.KEYS[0]])

    def test_invalid_config_preserves_old_junit(self):
        p = self.root / 'old.xml'; p.write_text('OLD')
        (self.root / '.env.local').unlink()
        self.code(2, lambda: self.prove('old.xml'))
        self.assertEqual('OLD', p.read_text())
        self.no_publish()

    def test_wrong_environment_or_tool(self):
        with patch('sql.platform.system', return_value='Other'):
            self.code(2, self.stack.tools)
        with patch('sql.sys.version_info', (3, 14, 0)):
            self.code(2, self.stack.tools)
        for output in ('9.0.401', '10.0.400', 'garbage'):
            self.fake.overrides['version'] = (0, output, '')
            self.code(2, self.stack.tools)
        with patch('sql.shutil.which', return_value=None):
            self.code(2, self.stack.tools)
        self.fake.overrides.pop('version')
        self.fake.overrides['sqlcmd-version'] = (0, 'ODBC', '')
        self.code(2, lambda: self.stack.tools(live=True))


class SetupBuildTests(Fixture):
    def test_offline_goals_do_not_read_config(self):
        (self.root / '.env.local').unlink()
        with patch.object(self.stack, 'config', side_effect=AssertionError('config read')):
            self.stack.build(); self.stack.lint(); self.stack.secrets(); self.stack.setup()
        self.assertFalse(any('/Action:Publish' in x[0] for x in self.fake.calls))
        build = [x for x in self.fake.calls if 'build' in x[0]]
        self.assertEqual(2, len(build))
        self.assertTrue(all('--no-restore' in x[0] for x in build))
        self.assertTrue(all('Imported' not in x for x in next(c[0] for c in self.fake.calls if 'lint' in c[0])))

    def test_caches_and_setup_order(self):
        self.stack.setup()
        calls = [c for c in self.fake.calls if c[0][0] != 'git']
        self.assertTrue(any(c[0][1:3] == ['-m', 'venv'] for c in calls))
        self.assertTrue(any(c[0][1:4] == ['-m', 'pip', 'install'] for c in calls))
        self.assertTrue(any(c[0][:3] == ['dotnet', 'tool', 'restore'] for c in calls))
        self.assertEqual(2, sum(c[0][:2] == ['dotnet', 'restore'] for c in calls))
        for _, env, timeout in calls:
            for key in ('DOTNET_CLI_HOME', 'NUGET_PACKAGES', 'NUGET_HTTP_CACHE_PATH', 'NUGET_PLUGINS_CACHE_PATH', 'PIP_CACHE_DIR'):
                self.assertTrue(Path(env[key]).is_relative_to(self.root / '.tmp'))
            self.assertFalse(any(k in env for k in sql.KEYS))
            self.assertLessEqual(timeout, 600)
        self.assertTrue((self.root / '.tmp/setup.complete').is_file())

    def test_missing_cache_and_failed_build_lint(self):
        (self.root / '.tmp/setup.complete').unlink()
        self.code(5, self.stack.build)
        self.assertEqual([], self.fake.calls)
        self.cache()
        for stage, action in (('build', self.stack.build), ('lint', self.stack.lint)):
            self.fake.overrides[stage] = (1, 'fixture-secret', 'fixture.invalid')
            self.code(5, action)
            self.fake.overrides[stage] = subprocess.TimeoutExpired('hidden', 300, output=b'fixture-secret')
            self.code(5, action)
            self.fake.overrides.pop(stage)
        self.no_publish()

    def test_setup_failure_does_not_claim_cache_ready(self):
        (self.root / '.tmp/setup.complete').unlink()
        self.fake.overrides['setup'] = subprocess.TimeoutExpired('hidden', 600)
        self.code(2, self.stack.setup)
        self.assertFalse((self.root / '.tmp/setup.complete').exists())

    def test_make_junit_literal(self):
        # The real make parser/recipe gets hostile-looking data; no evaluation.
        bin_dir = self.root / 'bin'; bin_dir.mkdir()
        executable = bin_dir / 'python3'
        executable.write_text('#!/bin/sh\n/usr/bin/printenv JUNIT\n')
        executable.chmod(0o700)
        marker = self.root / 'executed'
        value = 'reports/a space; $(shell touch ' + str(marker) + ') $`data`.xml'
        result = subprocess.run(['make', '-f', str(sql.ROOT / 'Makefile'), 'db-proof', 'JUNIT=' + value],
                                env={**os.environ, 'PATH': str(bin_dir) + ':' + os.environ['PATH']},
                                cwd=self.root, text=True, capture_output=True)
        self.assertEqual(0, result.returncode)
        self.assertEqual(value, result.stdout.strip())
        self.assertFalse(marker.exists())


class ExtractTests(Fixture):
    def test_actual_atomic_exchange_nonempty_and_pruning(self):
        def edit(tree):
            for name in ('Security', 'nested/uSeRs', 'nested/Permissions', 'Roles', 'Logins', 'ApplicationRoles'):
                p = tree / name; p.mkdir(parents=True, exist_ok=True)
                (p / 'danger.sql').write_text('CREATE USER bad; INSERT bad;')
        self.fake.extract_edit = edit
        self.stack.extract()
        tree = self.root / 'sql/Northwind/Imported'
        self.assertEqual(36, len(list(tree.rglob('*.sql'))))
        self.assertFalse((tree / 'old.sql').exists())
        self.assertTrue((tree / 'Stored Procedures/CustOrderHist.sql').exists())
        self.assertFalse(any(p.name.casefold() == 'security' for p in tree.rglob('*')))
        call = next(c[0] for c in self.fake.calls if '/Action:Extract' in c[0])
        for flag in ('/SourceDatabaseName:Northwind', '/p:ExtractTarget=SchemaObjectType',
                     '/p:ExtractAllTableData=False', '/p:ExtractReferencedServerScopedElements=False',
                     '/SourceEncryptConnection:True', '/SourceTrustServerCertificate:True'):
            self.assertIn(flag, call)
        self.no_publish()

    def test_dacfx_object_type_directory_vocabulary(self):
        def edit(tree):
            for before, after in (('Tables', 'Table'), ('Views', 'View'), ('Stored Procedures', 'Procedure')):
                (tree / before).rename(tree / after)
        self.fake.extract_edit = edit
        self.stack.extract()
        self.assertEqual(36, len(list((self.root / 'sql/Northwind/Imported').rglob('*.sql'))))

    def test_forbidden_sql_is_rollback(self):
        for forbidden in ('cReAtE\n user bad;', 'alter /*gap*/ role x;', 'gRaNt x;', 'INSERT INTO x;'):
            with self.subTest(sql=forbidden):
                self.fake.extract_edit = lambda tree, value=forbidden: (tree / 'Tables/Object0.sql').write_text(value)
                self.code(2, self.stack.extract); self.old_tree()

    def test_types_counts_categories(self):
        edits = [lambda tree: (tree / 'Tables/Object0.sql').unlink(),
                 lambda tree: (tree / 'Tables/Object0.sql').rename(tree / 'unknown.sql'),
                 lambda tree: (tree / 'Tables/link.sql').symlink_to('Object0.sql'),
                 lambda tree: os.mkfifo(tree / 'Tables/pipe.sql'),
                 lambda tree: (tree / 'Tables/readme.txt').write_text('bad')]
        for edit in edits:
            with self.subTest(edit=edits.index(edit)):
                self.fake.extract_edit = edit
                self.code(2, self.stack.extract); self.old_tree()

    def test_swap_and_tool_failure_preserves_old(self):
        with patch('sql.directory_exchange', side_effect=sql.Refusal(5, 'extract', 'atomic-exchange-failed')):
            self.code(5, self.stack.extract); self.old_tree()
        for result in ((1, 'fixture.invalid', 'fixture-secret'), subprocess.TimeoutExpired('secret', 300)):
            self.fake.overrides['extract'] = result
            self.code(5, self.stack.extract); self.old_tree()

    def test_real_swap_refusal_has_no_missing_window(self):
        old = self.root / 'sql/Northwind/Imported'
        new = self.root / 'new'; new.mkdir()
        (new / 'new.sql').write_text('NEW')
        with patch('sql.ctypes.CDLL') as lib:
            lib.return_value.renamex_np.return_value = -1
            self.code(5, lambda: sql.directory_exchange(new, old))
        self.old_tree(); self.assertTrue((new / 'new.sql').exists())


class TargetGuardTests(Fixture):
    def test_source_case_and_padding_rejected_without_publish(self):
        for name in ('Northwind', 'northwind', 'NORTHWIND', ' Northwind ', '\tNORTHWIND\t'):
            self.dotenv({**SYNTHETIC, sql.KEYS[1]: name})
            self.code(3, self.prove); self.no_publish()

    def test_bad_current_guard_never_publishes(self):
        name = SYNTHETIC[sql.KEYS[1]].encode('utf-16-le').hex()
        for output in ('', 'NULL|1|0', name + '|0|0', name + '|1|1', name + '|1|NULL',
                       name + '|1', name + '|1|0\n' + name + '|1|0', 'AB|1|0',
                       '4100|1|0'):
            self.fake.guard_output = output
            self.code(3, self.prove); self.no_publish()

    def test_connection_failure_and_timeout(self):
        for result in ((1, '', 'login failed fixture.invalid'), subprocess.TimeoutExpired('hidden', 60)):
            self.fake.overrides['guard'] = result
            self.code(4, self.prove); self.no_publish()

    def test_one_query_marker_not_value_and_immediate_publish(self):
        self.prove()
        calls = self.fake.calls
        index = next(i for i, c in enumerate(calls) if '/Action:Publish' in c[0])
        self.assertIn(sql.GUARD_SQL, calls[index - 1][0])
        self.assertEqual(1, sum(sql.GUARD_SQL in c[0] for c in calls))
        self.assertIn('class = 0', sql.GUARD_SQL)
        self.assertIn('IS_SRVROLEMEMBER', sql.GUARD_SQL)
        self.assertNotRegex(sql.GUARD_SQL, r'\bvalue\b')
        publish = calls[index][0]
        flags = ('/p:IncludeCompositeObjects=True', '/p:DropObjectsNotInSource=True',
                 '/p:ExcludeObjectTypes=Users;Logins;RoleMembership;Permissions',
                 '/p:DropExtendedPropertiesNotInSource=False', '/p:ScriptDatabaseOptions=False',
                 '/p:BlockOnPossibleDataLoss=True', '/TargetEncryptConnection:True',
                 '/TargetTrustServerCertificate:True')
        for flag in flags: self.assertIn(flag, publish)
        connections = [env for argv, env, _ in calls if '-Q' in argv or '/Action:Publish' in argv]
        self.assertTrue(all({k: env[k] for k in sql.KEYS} == SYNTHETIC for env in connections))
        for argv, _, _ in calls:
            if '-Q' in argv:
                self.assertIn('--encrypt-connection=mandatory', argv)
                self.assertIn('-C', argv); self.assertIn('-b', argv)
                self.assertNotIn('-P', argv)


class JUnitPathTests(Fixture):
    def test_missing_indexed_alias_refuses_before_config_or_actions(self):
        cases = (('MissingCanary.xml', 'missingcanary.xml', False),
                 ('MissingReports/Canary.xml', 'missingreports/canary.xml', True),
                 ('MissingNested/SubDirectory/Canary.xml',
                  'MissingNested/subdirectory/canary.xml', True),
                 ('RemovedReports/Canary.xml', 'RemovedReports/canary.xml', False),
                 ('RenamedReports/Canary.xml', 'renamedreports/canary.xml', False))
        for tracked, alias, remove_parent in cases:
            with self.subTest(path=alias):
                p = self.root / tracked
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b'TRACKED OLD XML')
                subprocess.run(['git', '-C', str(self.root), 'add', '--', tracked],
                               check=True, capture_output=True)
                if tracked.startswith('RenamedReports/'):
                    p.parent.rename(self.root / 'renamedreports')
                p.unlink()
                if remove_parent:
                    p.parent.rmdir()
                index = subprocess.run(['git', '-C', str(self.root), '--literal-pathspecs',
                                        'ls-files', '--cached', '-z', '--', tracked],
                                       check=True, capture_output=True).stdout
                self.assertEqual(tracked.encode() + b'\x00', index)
                self.fake.calls.clear()
                with patch.object(self.stack, 'config', side_effect=AssertionError('config must stay uncalled')):
                    self.code(2, lambda: self.prove(alias))
                self.assertFalse(p.exists())
                self.assertFalse((self.root / alias).exists())
                self.assertTrue(all(c[0][0] == 'git' for c in self.fake.calls))

    def test_missing_indexed_neighbor_allows_distinct_untracked_xml(self):
        p = self.root / 'CanonicalReports/Tracked.xml'
        p.parent.mkdir()
        p.write_bytes(b'TRACKED OLD XML')
        subprocess.run(['git', '-C', str(self.root), 'add', '--', 'CanonicalReports/Tracked.xml'],
                       check=True, capture_output=True)
        p.unlink()
        self.prove('CanonicalReports/new.xml')
        self.assertFalse(p.exists())
        self.assertEqual('1', ET.parse(p.parent / 'new.xml').getroot().get('tests'))
        shutil.rmtree(p.parent)
        self.prove('CanonicalReports/new/deep.xml')
        self.assertFalse(p.exists())
        self.assertEqual('1', ET.parse(p.parent / 'new/deep.xml').getroot().get('tests'))

    def test_missing_indexed_unicode_alias_refuses_without_recreation(self):
        p = self.root / 'NormalizationCaf\u00e9.xml'
        p.write_bytes(b'TRACKED OLD XML')
        subprocess.run(['git', '-C', str(self.root), 'add', '--', p.name],
                       check=True, capture_output=True)
        self.assertTrue(subprocess.run(['git', '-C', str(self.root), 'ls-files', '--cached', '-z'],
                                       check=True, capture_output=True).stdout)
        p.unlink()
        alias = 'normalizationcafe\u0301.xml'
        self.fake.calls.clear()
        with patch.object(self.stack, 'config', side_effect=AssertionError('config must stay uncalled')):
            self.code(2, lambda: self.prove(alias))
        self.assertFalse(p.exists())
        self.assertFalse((self.root / alias).exists())
        self.assertTrue(all(c[0][0] == 'git' for c in self.fake.calls))

    def test_tracked_case_aliases_preserve_bytes_before_config_or_actions(self):
        cases = (('TrackedCanary.xml', 'trackedcanary.xml'),
                 ('TrackedReports/Canary.xml', 'trackedreports/Canary.xml'),
                 ('NestedReports/SubDirectory/Canary.xml', 'NestedReports/subdirectory/Canary.xml'),
                 ('CombinedReports/Canary.xml', 'combinedreports/canary.xml'))
        for tracked, alias in cases:
            with self.subTest(path=alias):
                p = self.root / tracked
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b'TRACKED OLD XML')
                subprocess.run(['git', '-C', str(self.root), 'add', '--', tracked],
                               check=True, capture_output=True)
                self.assertTrue(p.samefile(self.root / alias))
                self.fake.calls.clear()
                with patch.object(Path, 'read_text', side_effect=AssertionError('config must stay unread')):
                    self.code(2, lambda: self.prove(alias))
                self.assertEqual(b'TRACKED OLD XML', p.read_bytes())
                self.assertTrue(all(c[0][0] == 'git' for c in self.fake.calls))

    def test_case_alias_ancestor_with_new_leaf_refuses(self):
        p = self.root / 'ExistingReports/Tracked.xml'
        p.parent.mkdir()
        p.write_bytes(b'TRACKED OLD XML')
        subprocess.run(['git', '-C', str(self.root), 'add', '--', 'ExistingReports/Tracked.xml'],
                       check=True, capture_output=True)
        self.assertTrue(p.parent.samefile(self.root / 'existingreports'))
        with patch.object(Path, 'read_text', side_effect=AssertionError('config must stay unread')):
            self.code(2, lambda: self.prove('existingreports/new.xml'))
        self.assertEqual(b'TRACKED OLD XML', p.read_bytes())
        self.assertFalse((p.parent / 'new.xml').exists())
        self.assertTrue(all(c[0][0] == 'git' for c in self.fake.calls))

    def test_index_spelling_alias_tracks_physical_file(self):
        for tracked, canonical in (('IndexCanary.xml', 'indexcanary.xml'),
                                   ('IndexReports/canary.xml', 'indexreports/canary.xml')):
            with self.subTest(path=canonical):
                p = self.root / tracked
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b'TRACKED OLD XML')
                subprocess.run(['git', '-C', str(self.root), 'add', '--', tracked],
                               check=True, capture_output=True)
                renamed = self.root / canonical
                if p.parent == self.root:
                    p.rename(renamed)
                else:
                    p.parent.rename(renamed.parent)
                self.assertIn(renamed.name, [x.name for x in renamed.parent.iterdir()])
                self.assertTrue(p.samefile(renamed))
                self.fake.calls.clear()
                with patch.object(Path, 'read_text', side_effect=AssertionError('config must stay unread')):
                    self.code(2, lambda: self.prove(canonical))
                self.assertEqual(b'TRACKED OLD XML', renamed.read_bytes())
                self.assertTrue(all(c[0][0] == 'git' for c in self.fake.calls))

    def test_unknown_physical_index_inventory_preserves_untracked_xml(self):
        p = self.root / 'untracked.xml'
        for existing in (True, False):
            if existing:
                p.write_bytes(b'UNTRACKED OLD XML')
            else:
                p.unlink()
            for result in ((1, '', ''), (0, '', 'unknown'), (0, 'incomplete', ''),
                           (0, '\x00', ''), (0, '../outside\x00', ''), (0, '\ufffd\x00', '')):
                with self.subTest(existing=existing, inventory=result):
                    fake = FakeExecutor(self.root)
                    def execute(argv, **kwargs):
                        if argv[0] == 'git' and '--cached' in argv:
                            fake.calls.append((argv, kwargs['env'].copy(), kwargs['timeout']))
                            return subprocess.CompletedProcess(argv, *result)
                        return fake(argv, **kwargs)
                    stack = sql.Stack(self.root, executor=execute)
                    with patch.object(stack, 'config', side_effect=AssertionError('config must stay uncalled')):
                        self.code(2, lambda: stack.proof(p.name))
                    self.assertEqual(existing, p.exists())
                    if existing:
                        self.assertEqual(b'UNTRACKED OLD XML', p.read_bytes())
                    self.assertTrue(all(c[0][0] == 'git' for c in fake.calls))

    def test_canonical_untracked_leaf_and_ancestors_remain_valid(self):
        p = self.root / 'CanonicalReports/untracked.xml'
        p.parent.mkdir()
        p.write_bytes(b'UNTRACKED OLD XML')
        self.prove('CanonicalReports/untracked.xml')
        self.assertNotEqual(b'UNTRACKED OLD XML', p.read_bytes())
        self.assertEqual('1', ET.fromstring(p.read_bytes()).get('tests'))
        self.prove('CanonicalReports/new/deep.xml')
        self.assertEqual('1', ET.parse(p.parent / 'new/deep.xml').getroot().get('tests'))

    def test_tracked_magic_filenames_are_literal_and_preserved(self):
        for value in (':(literal)canary.xml', ':(exclude)canary.xml', ':(glob)canary.xml',
                      'report[1].xml', 'report*.xml', 'a space;$data.xml'):
            with self.subTest(path=value):
                p = self.root / value
                p.write_bytes(b'TRACKED OLD XML')
                subprocess.run(['git', '--literal-pathspecs', '-C', str(self.root), 'add', '--', value],
                               check=True, capture_output=True)
                self.fake.calls.clear()
                self.code(2, lambda: self.prove(value))
                self.assertEqual(b'TRACKED OLD XML', p.read_bytes())
                self.assertTrue(all(c[0][0] == 'git' for c in self.fake.calls))

    def test_ambient_git_overrides_reject_before_junit_and_config(self):
        p = self.root / 'canary.xml'
        p.write_bytes(b'TRACKED OLD XML')
        subprocess.run(['git', '-C', str(self.root), 'add', 'canary.xml'], check=True, capture_output=True)
        alternate = self.root / '.tmp/nonexistent-index'
        self.assertFalse(alternate.exists())
        for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE'):
            for value in (str(alternate), ''):
                with self.subTest(override=key, empty=value == ''):
                    fake = FakeExecutor(self.root)
                    stack = sql.Stack(self.root, executor=fake, environ={**os.environ, key: value})
                    self.assertEqual('git', self.code(2, lambda: stack.proof('canary.xml')).phase)
                    self.assertEqual(b'TRACKED OLD XML', p.read_bytes())
                    self.assertEqual([], fake.calls)
                    self.assertEqual('git', self.code(2, lambda: stack.proof('../invalid.xml')).phase)
                    with patch.object(Path, 'read_text', side_effect=AssertionError('config must stay unread')):
                        self.assertEqual('git', self.code(2, stack.config).phase)
                    out = io.StringIO()
                    with patch('sql.Stack', return_value=stack), patch.dict(os.environ, {'JUNIT': 'canary.xml'}), contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                        self.assertEqual(2, sql.main(['db-proof']))
                    self.assertNotIn(str(alternate), out.getvalue())
                    self.assertEqual([], fake.calls)
                    self.assertFalse(alternate.exists())

    def test_untracked_magic_filename_remains_literal_data(self):
        self.prove(':(literal)untracked.xml')
        self.assertTrue((self.root / ':(literal)untracked.xml').is_file())
        self.assertFalse((self.root / 'untracked.xml').exists())

    def test_lexical_and_type_refusals_precede_all_actions(self):
        (self.root / 'directory.xml').mkdir()
        for value in ('', '/outside.xml', '../escape.xml', 'a/../escape.xml', 'a.txt', './a.xml',
                      'double//a.xml', 'directory.xml', 'nul\x00.xml', 'a\\b.xml'):
            self.fake.calls.clear()
            self.code(2, lambda: self.prove(value))
            self.assertEqual([], self.fake.calls)

    def test_symlink_leaf_and_ancestor(self):
        (self.root / 'actual').mkdir()
        (self.root / 'link').symlink_to('actual', target_is_directory=True)
        (self.root / 'leaf.xml').symlink_to('actual/a.xml')
        for value in ('link/a.xml', 'leaf.xml'):
            self.fake.calls.clear()
            self.code(2, lambda: self.prove(value)); self.assertEqual([], self.fake.calls)

    def test_tracked_unknown_and_nongit_preserve_old_xml(self):
        p = self.root / 'old.xml'; p.write_text('OLD')
        subprocess.run(['git', '-C', str(self.root), 'add', 'old.xml'], check=True)
        self.code(2, lambda: self.prove('old.xml')); self.assertEqual('OLD', p.read_text())
        self.assertFalse(any(c[0][0] != 'git' for c in self.fake.calls))
        self.fake.overrides['git:ls-files'] = (1, '', '')
        self.code(2, lambda: self.prove('other.xml'))
        self.fake.overrides['git:ls-files'] = (0, 'malformed', '')
        self.code(2, lambda: self.prove('other.xml'))
        with tempfile.TemporaryDirectory() as directory:
            stack = sql.Stack(directory, executor=FakeExecutor(Path(directory)))
            self.code(2, lambda: stack.proof('canary.xml'))

    def test_old_untracked_removed_before_build_failure(self):
        p = self.root / 'old.xml'; p.write_text('OLD')
        def fail(argv, **kwargs):
            if 'build' in argv:
                self.assertFalse(p.exists())
                return subprocess.CompletedProcess(argv, 1, '', '')
            return self.fake(argv, **kwargs)
        self.stack.executor = fail
        self.code(5, lambda: self.prove('old.xml'))
        self.assertFalse(p.exists()); self.no_publish()

    def test_atomic_write_failure_and_literal_path(self):
        with patch('sql.os.replace', side_effect=OSError('fixture-secret')):
            self.code(1, lambda: self.prove('reports/a space;$data.xml'))
        self.assertFalse((self.root / 'reports/a space;$data.xml').exists())
        self.assertEqual([], list((self.root / 'reports').glob('.junit-*')))
        self.prove('reports/a space;$data.xml')
        self.assertTrue((self.root / 'reports/a space;$data.xml').is_file())


class ProofTests(Fixture):
    def test_current_success_stage_order(self):
        self.prove()
        actions = [argv[argv.index('-Q') + 1] if '-Q' in argv else
                   next((x for x in argv if x.startswith('/Action:')), '')
                   for argv, _, _ in self.fake.calls]
        self.assertLess(actions.index(sql.GUARD_SQL), actions.index('/Action:Publish'))
        self.assertLess(actions.index('/Action:Publish'), actions.index('EXEC tSQLt.RunAll;'))
        self.assertLess(actions.index('EXEC tSQLt.RunAll;'), actions.index('EXEC tSQLt.XmlResultFormatter;'))
        formatter = next(c for c in self.fake.calls if 'EXEC tSQLt.XmlResultFormatter;' in c[0])
        for flag, value in (('-h', '-1'), ('-y', '0'), ('-w', '65535')):
            self.assertEqual(value, formatter[0][formatter[0].index(flag) + 1])
        self.assertEqual(60, formatter[2])
        self.assertEqual(120, next(c[2] for c in self.fake.calls if 'EXEC tSQLt.RunAll;' in c[0]))
        xml = ET.parse(self.root / 'reports/canary.xml').getroot()
        self.assertEqual({'tests': '1', 'failures': '0', 'errors': '0', 'skipped': '0'}, xml.attrib)
        self.assertEqual(1, len(list(xml.iter('testcase'))))
        self.assertFalse(any('SetTestResultFormatter' in ' '.join(c[0]) for c in self.fake.calls))

    def test_strict_malformed_and_inconsistent_xml(self):
        invalid = ['', '<testsuites>', GOOD_XML + GOOD_XML, '<wrong/>',
                   '<!DOCTYPE x [<!ENTITY x "y">]>' + GOOD_XML,
                   GOOD_XML.replace('tests="1"', 'tests="-1"'),
                   GOOD_XML.replace('tests="1"', 'tests="1.0"'),
                   GOOD_XML.replace('tests="1"', 'tests="2"'),
                   GOOD_XML.replace('failures="0"', 'failures="1"'),
                   GOOD_XML.replace('tests="1"', 'tests="1" tests="1"'),
                   GOOD_XML.replace('classname="StackAdaptationTests"', 'classname="Other"'),
                   GOOD_XML.replace('test Products table exists', 'other'),
                   GOOD_XML.replace('</testsuite>', '<testcase classname="Other" name="other"/></testsuite>'),
                   GOOD_XML.replace('<testcase ', '<unsupported/><testcase ')]
        for xml in invalid:
            self.fake.xml = xml
            self.code(1, self.prove)
            self.assertFalse((self.root / 'reports/canary.xml').exists())

    def test_failure_error_skipped_retained_and_fail(self):
        for tag, counter in (('failure', 'failures'), ('error', 'errors'), ('skipped', 'skipped')):
            self.fake.xml = GOOD_XML.replace(counter + '="0"', counter + '="1"').replace(
                'name="test Products table exists"/>',
                'name="test Products table exists"><' + tag + ' message="fixture-secret">fixture.invalid</' + tag + '></testcase>')
            self.code(1, self.prove)
            data = (self.root / 'reports/canary.xml').read_text()
            self.assertIn('<' + tag, data)
            self.assertNotIn('fixture-secret', data); self.assertNotIn('fixture.invalid', data)
        self.fake.xml = GOOD_XML.replace('name="test Products table exists"/>',
            'name="test Products table exists"><failure/></testcase>')
        self.code(1, self.prove)  # green counters cannot override failing host projection

    def test_runall_refusal_cannot_reuse_green_xml(self):
        for outcome, code in (((1, 'Test Execution Summary: 1 Failures', ''), 1),
                              ((1, '', 'Login failed fixture.invalid'), 4),
                              (subprocess.TimeoutExpired('hidden', 120), 4)):
            self.fake.calls.clear(); self.fake.overrides['run-all'] = outcome
            self.code(code, self.prove)
            self.assertFalse((self.root / 'reports/canary.xml').exists())
            self.assertFalse(any('EXEC tSQLt.XmlResultFormatter;' in c[0] for c in self.fake.calls))

    def test_runall_green_summary_does_not_mask_connection_loss(self):
        self.fake.overrides['run-all'] = (
            1, 'Test Execution Summary: 1 test case(s) executed, 1 succeeded, 0 failed, 0 errored.',
            'Connection lost fixture.invalid')
        self.code(4, self.prove)
        self.assertFalse((self.root / 'reports/canary.xml').exists())
        self.assertFalse(any('EXEC tSQLt.XmlResultFormatter;' in c[0] for c in self.fake.calls))
        self.fake.overrides['run-all'] = (
            1, 'Test Execution Summary: 1 test case(s) executed, 0 succeeded, 1 failed, 0 errored.', '')
        self.code(1, self.prove)

    def test_publish_formatter_errors_and_timeout(self):
        for stage, code in (('publish', 6), ('formatter', 4)):
            for outcome in ((1, 'fixture-secret', 'fixture.invalid'), subprocess.TimeoutExpired('hidden', 300)):
                self.fake.overrides[stage] = outcome
                self.code(code, self.prove)
                self.assertFalse((self.root / 'reports/canary.xml').exists())
            self.fake.overrides.pop(stage)


class RedactionTests(Fixture):
    def test_refusal_streams_redacted_across_all_command_phases(self):
        stages = (('version', 'db-proof', 2), ('guard', 'db-proof', 4),
                  ('publish', 'db-proof', 6), ('run-all', 'db-proof', 4),
                  ('formatter', 'db-proof', 4), ('build', 'db-proof', 5),
                  ('lint', 'lint', 5), ('extract', 'db-extract', 5),
                  ('state', 'db-state', 4), ('setup', 'setup', 2))
        private = 'fixture-secret fixture.invalid ' + str(self.root)
        outcomes = ((1, private, private),
                    subprocess.TimeoutExpired(['fixture-secret'], 1, output=private.encode(), stderr=private.encode()),
                    subprocess.TimeoutExpired('hidden', 1, output=private, stderr=private),
                    subprocess.TimeoutExpired('hidden', 1), OSError(private))
        for stage, goal, code in stages:
            for outcome in outcomes:
                with self.subTest(stage=stage, outcome=type(outcome).__name__):
                    self.fake.overrides = {stage: outcome}
                    out = io.StringIO()
                    with patch('sql.Stack', return_value=self.stack), patch.dict(os.environ, {'JUNIT': 'result.xml'}), contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                        self.assertEqual(code, sql.main([goal]))
                    for value in (*SYNTHETIC.values(), str(self.root)):
                        self.assertNotIn(value, out.getvalue())
                    self.assertFalse((self.root / 'result.xml').exists())

    def test_never_echo_streams_argv_env_or_exception(self):
        for outcome in ((1, 'fixture-secret', 'fixture.invalid'),
                        subprocess.TimeoutExpired(['fixture-secret'], 1, output=b'fixture.invalid', stderr=b'fixture-secret'),
                        subprocess.TimeoutExpired('secret', 1, output='fixture.invalid', stderr='fixture-secret'),
                        subprocess.TimeoutExpired('secret', 1), OSError('fixture-secret fixture.invalid')):
            self.fake.overrides['publish'] = outcome
            out = io.StringIO()
            with patch('sql.Stack', return_value=self.stack), patch.dict(os.environ, {'JUNIT': 'result.xml'}), contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                self.assertEqual(6, sql.main(['db-proof']))
            text = out.getvalue()
            for private in SYNTHETIC.values(): self.assertNotIn(private, text)
            self.assertNotIn(str(self.root), text)
            self.assertFalse((self.root / 'result.xml').exists())

    def test_success_xml_whitelist_removes_all_private_metadata(self):
        self.fake.xml = GOOD_XML.replace('<properties/>', '<properties><property name="password" value="fixture-secret"/></properties>').replace(
            '<system-out/>', '<system-out>fixture-secret fixture.invalid</system-out>').replace(
            '<system-err/>', '<system-err>' + str(self.root) + '</system-err>')
        out = io.StringIO()
        with contextlib.redirect_stdout(out): self.prove()
        data = (self.root / 'reports/canary.xml').read_text() + out.getvalue()
        for private in (*SYNTHETIC.values(), str(self.root)):
            self.assertNotIn(private, data)
        self.assertNotIn('hostname', data)

    def test_invalid_xml_and_atomic_error_safe(self):
        self.fake.xml = 'fixture-secret fixture.invalid ' + str(self.root)
        out = io.StringIO()
        with patch('sql.Stack', return_value=self.stack), patch.dict(os.environ, {'JUNIT': 'result.xml'}), contextlib.redirect_stdout(out):
            self.assertEqual(1, sql.main(['db-proof']))
        for private in (*SYNTHETIC.values(), str(self.root)):
            self.assertNotIn(private, out.getvalue())


class DbStateTests(Fixture):
    def test_empty_readonly_report(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out): self.stack.state()
        self.assertIn('empty', out.getvalue()); self.assertIn('not-tested', out.getvalue())
        self.no_publish()
        self.assertFalse(any('EXEC tSQLt.RunAll;' in c[0] for c in self.fake.calls))
        self.assertIn('COLLATE DATABASE_DEFAULT', sql.STATE_SQL)
        self.assertNotRegex(sql.STATE_SQL, r'HOST_NAME|SERVERPROPERTY|@@SERVERNAME|\bvalue\b')

    def test_populated_catalogs_and_no_false_canary(self):
        self.fake.state_output = 'BEGIN\nSCHEMA|StackAdaptationTests\nCLASS|StackAdaptationTests\nRESULT|StackAdaptationTests|test Products table exists|Success\nEND\n'
        out = io.StringIO()
        with contextlib.redirect_stdout(out): self.stack.state()
        self.assertIn('Products-U=0', out.getvalue()); self.assertIn('contextual-only', out.getvalue())
        self.assertNotIn('canary success', out.getvalue())
        self.no_publish()

    def test_invalid_incomplete_and_connection(self):
        for value in ('', 'BEGIN', 'BEGIN\nOBJECT|dbo.Products\nEND', 'BEGIN\nUNKNOWN|x\nEND',
                      'BEGIN\nOBJECT|dbo.Products|U\nOBJECT|dbo.Products|U\nEND'):
            self.fake.state_output = value
            self.code(4, self.stack.state)
        self.fake.overrides['state'] = subprocess.TimeoutExpired('hidden', 60)
        self.code(4, self.stack.state)


class RepositoryContractTests(Fixture):
    def test_exact_pins_projects_lint_and_canary(self):
        root = sql.ROOT
        self.assertEqual({'version': '10.0.401', 'rollForward': 'latestFeature'}, json.loads((root / 'global.json').read_text())['sdk'])
        self.assertEqual('170.5.96', json.loads((root / '.config/dotnet-tools.json').read_text())['tools']['microsoft.sqlpackage']['version'])
        self.assertEqual('SQLFluff==3.4.2', (root / 'requirements-dev.txt').read_text().strip())
        for p in sql.PROJECTS:
            xml = ET.parse(root / p).getroot()
            self.assertEqual('Microsoft.Build.Sql/2.3.0', xml.get('Sdk'))
            self.assertEqual('Microsoft.Data.Tools.Schema.Sql.Sql150DatabaseSchemaProvider', xml.findtext('./PropertyGroup/DSP'))
        test_project = ET.parse(root / sql.PROJECTS[1]).getroot()
        self.assertEqual('../Northwind/Northwind.sqlproj', test_project.find('./ItemGroup/ProjectReference').get('Include'))
        package = test_project.find('./ItemGroup/PackageReference')
        self.assertEqual('1.0.8083.3529', package.get('Version'))
        self.assertEqual('tSQLt.2019', package.findtext('DacpacName'))
        text = '\n'.join(p.read_text() for p in (root / 'sql/tests').rglob('*.sql'))
        self.assertEqual(1, len(re.findall(r'CREATE\s+PROCEDURE', text, re.I)))
        self.assertIn("OBJECT_ID(N'dbo.Products', N'U')", text)
        self.assertIn("N'tSQLt.TestClass'", text)
        self.assertNotRegex(text, r'FakeTable|NewTestClass|INSERT|SELECT\s+\*')
        lint = (root / '.sqlfluff').read_text()
        for term in ('dialect = tsql', 'templater = raw', 'max_line_length = 120'): self.assertIn(term, lint)

    def test_shared_bytes_and_no_process_override(self):
        for p in LOCAL_FILES:
            current = (sql.ROOT / p).read_bytes()
            baseline = subprocess.check_output(['git', '-C', str(sql.ROOT), 'show', 'HEAD:' + p])
            boundary = '## Локальные правила стека'.encode()
            self.assertEqual(baseline.split(boundary)[0], current.split(boundary)[0], p)
            local = current.split(boundary)[1].decode()
            self.assertNotRegex(local, r'261011_1523|/Users/|PLANVEYOR_RUNTIME_ROOT')
            self.assertIn('N/A (why=no local override)', local)

    def test_secret_scan_tracked_untracked_and_explicit_xml(self):
        p = self.root / 'leak.txt'
        p.write_text('Password' + '=fixture-secret;')
        self.code(2, self.stack.secrets)
        subprocess.run(['git', '-C', str(self.root), 'add', 'leak.txt'], check=True)
        self.code(2, self.stack.secrets)
        p.write_text('safe'); self.stack.secrets()
        (self.root / '.tmp/ignored.txt').write_text('Password' + '=fixture-secret;')
        self.stack.secrets()
        asset = self.root / 'docs/code_reviews/assets/x/junit.xml'
        asset.parent.mkdir(parents=True); asset.write_text('Password' + '=fixture-secret;')
        self.code(2, self.stack.secrets)

    def test_no_remaining_stubs_in_current_file_targets(self):
        # Imported is materialized only by live Extract, never by this fixture.
        for p in ('Makefile', 'scripts/sql.py', 'scripts/test_sql.py', 'global.json',
                  '.config/dotnet-tools.json', '.sqlfluff', 'requirements-dev.txt',
                  'Directory.Build.props', 'NuGet.Config', *sql.PROJECTS,
                  'sql/tests/StackAdaptationTests/StackAdaptationTests.sql',
                  'sql/tests/StackAdaptationTests/test_Products_table_exists.sql'):
            text = (sql.ROOT / p).read_text()
            self.assertNotIn('PLANVEYOR_' + 'PATH_TRACKING_STUB', text)
            self.assertNotIn('Path-tracking' + ' stub;', text)


if __name__ == '__main__':
    unittest.main()

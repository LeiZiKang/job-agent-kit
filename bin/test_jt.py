"""CLI tests use an isolated repository; real tracker data is never mutated."""
from datetime import date, timedelta
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class TrackerCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.jt-test-', dir=Path(__file__).resolve().parent.parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'bin').mkdir()
        shutil.copyfile(Path(__file__).with_name('jt.py'), self.root / 'bin/jt.py')
        (self.root / 'reports/jobs').mkdir(parents=True)
        (self.root / 'reports/jobs/example.html').write_text('<p>example</p>')
        self.data = dict(version=1, updated_at='2026-10-05T12:00:00+00:00',
                         applications=[], seen_jobs=[], contacts=[])
        self.save()

    def save(self):
        (self.root / 'tracker.json').write_text(json.dumps(self.data))

    def run_cli(self, *args, code=0, env=None):
        result = subprocess.run([sys.executable, str(self.root / 'bin/jt.py'), *args],
                                cwd=self.temp.name, text=True, capture_output=True, env=env)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def add(self, *args, code=0):
        return self.run_cli('add-seen', '--platform', 'liepin', '--company', 'Example',
                            '--role', 'iOS', '--verdict', 'maybe', '--reason', 'to verify',
                            *args, code=code)

    def test_missing_tracker_is_created_and_deadline_is_optional(self):
        (self.root / 'tracker.json').unlink()
        self.assertIn('created empty tracker.json', self.run_cli('check').stdout)
        self.run_cli('board')
        self.assertNotIn('Days left', self.read_board())
        (self.root / 'config.json').write_text('{"deadline": "2999-01-01"}')
        self.run_cli('board')
        self.assertIn('Days left', self.read_board())

    def test_check_empty_and_missing_structure(self):
        self.assertIn('OK:', self.run_cli('check').stdout)
        del self.data['contacts']
        self.save()
        self.assertIn('contacts', self.run_cli('check', code=1).stderr)

    def test_seen_id_url_and_not_found(self):
        self.add('--id', '123', '--report', 'reports/jobs/example.html')
        self.assertIn('liepin:123', self.run_cli('seen', 'liepin:123').stdout)
        self.assertIn('liepin:123', self.run_cli('seen', 'https://www.liepin.com/job/123.shtml?utm_source=x#top').stdout)
        self.run_cli('seen', 'liepin:999', code=1)

    def test_duplicate_id_and_url_do_not_write(self):
        self.add('--url', 'https://www.liepin.com/job/123.shtml?utm_source=x')
        before = (self.root / 'tracker.json').read_bytes()
        result = self.add('--id', '123', code=1)
        self.assertIn('Example', result.stderr)
        self.add('--url', 'http://www.liepin.com/a/123.shtml#top', code=1)
        self.assertEqual(before, (self.root / 'tracker.json').read_bytes())

    def test_generic_url_normalization_and_duplicate(self):
        common = ['add-seen', '--platform', 'ats', '--company', 'Example', '--role', 'iOS',
                  '--verdict', 'new', '--reason', 'public job']
        self.run_cli(*common, '--url', 'https://jobs.example.org/role/?job=12&utm_source=x')
        self.run_cli(*common, '--url', 'http://JOBS.EXAMPLE.ORG/role?job=12#top', code=1)
        self.run_cli(*common, '--url', 'https://jobs.example.org/role?job=13')
        self.assertIn('seen_jobs=2', self.run_cli('check').stdout)

    def test_check_duplicate_key_and_url_alias(self):
        self.add('--id', '123', '--url', 'https://www.liepin.com/job/123.shtml')
        self.data = json.loads((self.root / 'tracker.json').read_text())
        row = dict(self.data['seen_jobs'][0])
        self.data['seen_jobs'].append(row)
        self.save()
        self.run_cli('check', code=1)
        row['key'] = 'https://www.liepin.com/job/123.shtml'
        self.save()
        self.run_cli('check', code=1)

    def test_invalid_verdict_report_and_date(self):
        self.add('--id', '123')
        self.data = json.loads((self.root / 'tracker.json').read_text())
        row = self.data['seen_jobs'][0]
        for field, bad in [('verdict', 'pending'), ('report', 'reports/jobs/missing.html'),
                           ('report', '../outside.html'), ('first_seen', '2026-99-01'),
                           ('platform', 'unknown'), ('company', None)]:
            old = row[field]
            row[field] = bad
            self.save()
            self.run_cli('check', code=1)
            row[field] = old

    def test_invalid_application_and_duplicate_id(self):
        fields = 'id company role platform job_url platform_job_id status evidence applied_at last_checked_at next_action notes legacy_ref'.split()
        row = dict.fromkeys(fields, '')
        row.update(id='app-one', platform='ats', status='submitted', evidence='unverified')
        self.data['applications'] = [row]
        self.save()
        self.run_cli('check')
        row['status'] = 'submitted_verified'
        self.save()
        self.run_cli('check', code=1)
        row['status'] = 'submitted'
        self.data['applications'].append(dict(row))
        self.save()
        self.run_cli('check', code=1)

    def test_bad_add_never_changes_tracker(self):
        before = (self.root / 'tracker.json').read_bytes()
        self.add(code=1)
        self.add('--id', '123', '--url', 'https://www.liepin.com/job/456.shtml', code=1)
        self.add('--id', '123', '--report', 'reports/jobs/missing.html', code=1)
        self.assertEqual(before, (self.root / 'tracker.json').read_bytes())

    def test_apply_marks_seen_and_update(self):
        self.add('--id', '42', '--url', 'https://www.liepin.com/job/42.shtml')
        out = self.run_cli('apply', '--platform', 'liepin', '--id', '42', '--company', 'Example',
                           '--role', 'iOS', '--evidence', 'sent', '--next', 'wait').stdout
        app_id = out.split()[-1]
        data = json.loads((self.root / 'tracker.json').read_text())
        self.assertEqual(data['seen_jobs'][0]['verdict'], 'applied')
        self.assertEqual(data['applications'][0]['id'], app_id)
        self.run_cli('update', 'example', '--status', 'interviewing', '--next', 'call', '--note', 'HR called')
        row = json.loads((self.root / 'tracker.json').read_text())['applications'][0]
        self.assertEqual((row['status'], row['next_action']), ('interviewing', 'call'))
        self.assertIn('HR called', row['notes'])
        self.run_cli('update', 'nomatch', '--next', 'x', code=1)
        self.assertIn('interviewing', self.run_cli('status').stdout)

    def test_status_and_board_escape(self):
        self.add('--id', '123', '--company', '<script>alert(1)</script>')
        self.assertIn('applications: 0', self.run_cli('status').stdout)
        self.run_cli('board')
        board = (self.root / 'board.html').read_text()
        self.assertNotIn('<script>', board)
        self.assertIn('&lt;script&gt;', board)
        self.assertIn('color-scheme:dark', board)

    def write_handoff(self, text):
        (self.root / '.agent-memory').mkdir(exist_ok=True)
        path = self.root / '.agent-memory/handoff.md'
        path.write_text(text, encoding='utf-8')
        return path

    def read_board(self):
        return (self.root / 'board.html').read_text(encoding='utf-8')

    def load_jt(self):
        spec = importlib.util.spec_from_file_location('isolated_jt', self.root / 'bin/jt.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_board_handoff_sections_and_escape(self):
        handoff = self.write_handoff(
            '# Handoff\n## Needs you to decide\n- **Confirm application** <script>alert(1)</script>\n'
            '- Review `a < b` and [report](reports/jobs/example.html)\n'
            '## In progress / blockers\nWaiting for reply\n\n1. Prepare docs\n2. Review docs\n'
            '## Next\nNot shown\n')
        before = handoff.read_bytes(), (self.root / 'tracker.json').read_bytes()
        self.run_cli('board')
        html = self.read_board()
        self.assertNotIn('<script>', html)
        for expected in ['<h2>Needs your decision</h2>', '&lt;script&gt;alert(1)&lt;/script&gt;',
                         '<li><strong>Confirm application</strong>', '<code>a &lt; b</code>', '<ul>', '<ol>',
                         '<li>Prepare docs</li>', '<p>Waiting for reply</p>',
                         '<a href="reports/jobs/example.html">report</a>',
                         '<meta http-equiv="refresh" content="60">']:
            self.assertIn(expected, html)
        self.assertNotIn('Not shown', html)
        self.assertLess(html.index('<h2>Needs your decision'), html.index('<h2>In progress'))
        self.assertLess(html.index('<h2>In progress'), html.index('<div class="metrics">'))
        self.assertRegex(html, r'>Updated \d{2}-\d{2} \d{2}:\d{2}</time>')
        self.assertEqual(before, (handoff.read_bytes(), (self.root / 'tracker.json').read_bytes()))

    def test_board_missing_or_empty_handoff(self):
        self.run_cli('board', env={**os.environ, 'PATH': ''})
        self.assertIn('Job Board', self.read_board())
        self.assertNotIn('<h2>Needs your decision', self.read_board())
        self.assertIn('Nothing yet', self.read_board())
        self.write_handoff('## Needs you to decide\n\n## In progress\nWaiting for reply\n')
        self.run_cli('board')
        self.assertNotIn('<h2>Needs your decision', self.read_board())
        self.assertIn('<p>Waiting for reply</p>', self.read_board())

    def test_board_report_primary_and_original_links(self):
        self.add('--id', '123', '--verdict', 'recommend', '--report', 'reports/jobs/example.html',
                 '--url', 'https://www.liepin.com/job/123.shtml')
        self.add('--id', '456', '--verdict', 'recommend', '--role', 'Frontend',
                 '--url', 'https://www.liepin.com/job/456.shtml')
        self.run_cli('board')
        html = self.read_board()
        first = html.split('<article class="card rec">')[1].split('</article>')[0]
        self.assertIn('<a class="stretch" href="reports/jobs/example.html">iOS</a>', first)
        self.assertIn('<a class="over" href="https://www.liepin.com/job/123.shtml">Original ↗</a>', first)
        second = html.split('<article class="card rec">')[2].split('</article>')[0]
        self.assertIn('<a class="stretch" href="https://www.liepin.com/job/456.shtml">Frontend</a>', second)
        self.assertNotIn('Original', second)

    def test_board_report_filename_is_quoted(self):
        path = self.root / 'reports/jobs/report #1.html'
        path.write_text('example')
        self.add('--id', '123', '--verdict', 'recommend', '--report', 'reports/jobs/report #1.html')
        self.run_cli('board')
        self.assertIn('href="reports/jobs/report%20%231.html"', self.read_board())

    def test_board_links_reject_unsafe_protocols_and_paths(self):
        unsafe = ['javascript:alert', 'data:text/html,evil', 'file:///tmp/secret',
                  '//evil.example', '../outside.html', '%2e%2e/outside.html',
                  '/tmp/secret', '%2f%2fevil.example', 'reports/%5csecret',
                  'reports/%00secret', 'reports/../../../outside.html']
        # Resolve symlinks too, so a repository-relative spelling cannot escape.
        (self.root / 'outside').symlink_to(self.root.parent, target_is_directory=True)
        unsafe.append('outside/secret.html')
        self.write_handoff('## Needs you\n' + '\n'.join(
            '- [unsafe](' + value + ')' for value in unsafe) +
            '\n- [safe](https://example.org/?a=1&b=2)'
            '\n- [quote](https://example.org/"onclick="evil)'
            '\n- `**no bold in code**`\n- <img src=x onerror=alert(1)>')
        self.run_cli('board')
        html = self.read_board()
        for value in unsafe:
            with self.subTest(url=value):
                self.assertNotIn('href="' + value + '"', html)
        for value in ['<img', '"onclick="evil', '<strong>no bold in code</strong>']:
            self.assertNotIn(value, html)
        self.assertIn('href="https://example.org/?a=1&amp;b=2"', html)
        self.assertIn('href="https://example.org/&quot;onclick=&quot;evil"', html)
        jt = self.load_jt()
        for value in unsafe:
            with self.subTest(url=value):
                self.assertFalse(jt.link_allowed(value, self.root))
        for value in ['http://example.org/job', 'https://example.org/job',
                      'reports/jobs/example.html', 'reports/jobs/../jobs/example.html']:
            self.assertTrue(jt.link_allowed(value, self.root))

    def test_board_application_order_metrics_and_collapsed_lists(self):
        jt = self.load_jt()
        for state in ['closed', 'rejected', 'offer', 'submitted_by_user', 'interviewing', 'submitted']:
            row = dict.fromkeys(jt.FIELDS['applications'], '')
            row.update(id=state, company='company-' + state, role='<script>role</script>',
                       platform='ats', job_url='https://example.org/job', status=state,
                       evidence='<script>evidence</script>', applied_at=date.today().isoformat(),
                       next_action='<script>next</script>')
            self.data['applications'].append(row)
        contact = dict.fromkeys(jt.FIELDS['contacts'], '')
        contact.update(platform='email', name='<script>name</script>', company='contact',
                       summary='<script>summary</script>', next_action='<script>action</script>')
        self.data['contacts'].append(contact)
        self.save()
        self.add('--id', '123')
        self.run_cli('board')
        html = self.read_board()
        for expected in ['Applied<b>6</b>', 'Waiting<b>2</b>', 'Interviewing<b>1</b>',
                         '<details class="fold"><summary>Maybe',
                         '<details class="fold"><summary>Contacts',
                         '<details class="evidence"><summary>Evidence', '<span class="age">0d</span>',
                         '<a href="https://example.org/job">&lt;script&gt;role&lt;/script&gt;</a>']:
            self.assertIn(expected, html)
        self.assertNotIn('<table', html)
        self.assertNotIn('<script>', html)
        self.assertNotIn(' open', html)
        for field in ['next', 'evidence', 'name', 'summary', 'action']:
            self.assertIn('&lt;script&gt;' + field + '&lt;/script&gt;', html)
        self.assertLess(html.index('company-submitted</span>'), html.index('company-rejected</span>'))
        self.assertLess(html.index('company-submitted</span>'), html.index('company-closed</span>'))
        self.assertIn('<li class="entry muted">', html)

    def apply(self, company='Example', job_id='1', *args, code=0):
        return self.run_cli('apply', '--platform', 'boss', '--id', job_id, '--company', company,
                            '--role', 'Engineer', '--evidence', 'greeting only; resume not delivered',
                            '--next', 'wait', *args, code=code)

    def test_company_aliases_guard_and_explicit_exception(self):
        self.apply('Example (示例科技)', '1')
        before = (self.root / 'tracker.json').read_bytes()
        for query in [('EXAMPLE',), ('示例',), ('missing', 'example')]:
            out = self.run_cli('company', *query).stdout
            self.assertIn('resume not delivered', out)
            self.assertIn('greeting alone', out)
        self.assertIn('no applications', self.run_cli('company', 'Different').stdout)
        self.apply('Example Ltd', '2', code=1)
        self.apply('示例科技有限公司', '2', code=1)
        self.apply('Example Ltd', '2', '--same-company-ok', '   ', code=1)
        self.assertEqual(before, (self.root / 'tracker.json').read_bytes())
        self.apply('Example Ltd', '2', '--same-company-ok', 'recipient has not received resume')
        rows = json.loads((self.root / 'tracker.json').read_text())['applications']
        self.assertIn('Same-company exception: recipient has not received resume', rows[1]['notes'])
        self.apply('Exampleish', '3')
        self.apply('XY', '4')
        self.apply('XY Ltd', '5', code=1)

    def test_replied_interview_source_and_funnel(self):
        self.apply('Example', '1', '--source', 'scout')
        self.apply('Second', '2')
        self.run_cli('update', 'Example', '--interview', '2026-10-21')
        row = json.loads((self.root / 'tracker.json').read_text())['applications'][0]
        self.assertEqual((row['replied_at'], row['interview_at']), ('2026-10-21', '2026-10-21'))
        before = (self.root / 'tracker.json').read_bytes()
        self.run_cli('update', 'Second', '--replied', 'bad-date', code=1)
        self.run_cli('update', 'Second', '--interview', '2026-02-30', code=1)
        self.run_cli('update', 'Second', '--source', 'unknown', code=2)
        self.assertEqual(before, (self.root / 'tracker.json').read_bytes())
        out = self.run_cli('funnel').stdout
        self.assertRegex(out, r'boss\s+2\s+1\s+50%\s+1')
        self.assertRegex(out, r'Total\s+2\s+1\s+50%\s+1')
        self.run_cli('update', 'Example', '--source', 'recruiter', '--replied', '2026-10-20')
        out = self.run_cli('funnel', '--by', 'source').stdout
        self.assertRegex(out, r'recruiter\s+1\s+1')
        self.assertRegex(out, r'\(unrecorded\)\s+1\s+0')
        self.run_cli('update', 'Second', '--replied', '--interview')
        row = json.loads((self.root / 'tracker.json').read_text())['applications'][1]
        self.assertEqual(row['replied_at'], date.today().isoformat())
        self.assertEqual(row['interview_at'], date.today().isoformat())

    def test_funnel_since_inclusive_and_read_only(self):
        self.apply('Example', '1', '--source', 'pirate')
        self.apply('Second', '2', '--source', 'self')
        self.data = json.loads((self.root / 'tracker.json').read_text())
        self.data['applications'][0]['applied_at'] = '2026-10-01'
        self.data['applications'][1]['applied_at'] = '2026-10-02'
        self.data['applications'][1]['status'] = 'rejected'
        self.save()
        before = (self.root / 'tracker.json').read_bytes()
        out = self.run_cli('funnel', '--since', '2026-10-02', '--by', 'source').stdout
        self.assertNotIn('pirate', out)
        self.assertRegex(out, r'self\s+1\s+0\s+0%\s+0\s+1')
        self.assertRegex(self.run_cli('funnel', '--since', '2999-01-01').stdout,
                         r'Total\s+0\s+0\s+0%')
        self.run_cli('funnel', '--since', 'bad-date', code=1)
        self.assertEqual(before, (self.root / 'tracker.json').read_bytes())

    def test_optional_fields_validation_and_legacy_compatibility(self):
        self.apply()
        self.data = json.loads((self.root / 'tracker.json').read_text())
        row = self.data['applications'][0]
        self.assertNotIn('source', row)
        for field, bad in [('source', 'unknown'), ('source', []), ('source', None),
                           ('replied_at', 0), ('interview_at', None), ('replied_at', '2026-02-30')]:
            row[field] = bad
            self.save()
            self.run_cli('check', code=1)
            del row[field]
        self.save()
        self.run_cli('check')

    def test_sweep_boundary_status_read_only_and_idempotence(self):
        fields = self.load_jt().FIELDS['applications']
        def app(i, days, **extra):
            row = dict.fromkeys(fields, '')
            row.update(id=f'app-{i}', company=f'Example {i}', role='Engineer', platform='ats',
                       status='submitted', evidence='confirmed', notes='keep existing note',
                       applied_at=(date.today() - timedelta(days=days)).isoformat())
            row.update(extra)
            return row
        self.data['applications'] = [app(1, 21), app(2, 30, replied_at='2026-10-01'), app(3, 20),
            app(4, 40, status='interviewing'), app(5, 22, status='submitted_by_user'),
            app(6, 40, status='rejected'), app(7, 40, interview_at='2026-10-01'),
            app(8, 40, applied_at=''), app(9, 40, status='preparing'), app(10, -1)]
        self.save()
        before = (self.root / 'tracker.json').read_bytes()
        for args in [('sweep', '--dry-run'), ('status',), ('status', '--full')]:
            out = self.run_cli(*args).stdout
            self.assertIn('can ghost: 2', out)
            self.assertIn('app-1', out)
            self.assertEqual(before, (self.root / 'tracker.json').read_bytes())
        self.assertIn('marked ghosted: 2', self.run_cli('sweep').stdout)
        rows = json.loads((self.root / 'tracker.json').read_text())['applications']
        self.assertEqual([row['id'] for row in rows if row['status'] == 'ghosted'], ['app-1', 'app-5'])
        self.assertIn('keep existing note;', rows[0]['notes'])
        self.assertIn('21+ days', rows[0]['notes'])
        before = (self.root / 'tracker.json').read_bytes()
        self.assertIn('marked ghosted: 0', self.run_cli('sweep').stdout)
        self.assertEqual(before, (self.root / 'tracker.json').read_bytes())
        self.run_cli('update', 'app-1', '--replied', '--status', 'submitted')
        self.assertIn('can ghost: 0', self.run_cli('sweep', '--dry-run').stdout)

    def test_add_seen_update_handles_existing_application(self):
        self.apply()
        before = (self.root / 'tracker.json').read_bytes()
        self.run_cli('add-seen', '--platform', 'boss', '--id', '1', '--company', 'Example',
                     '--role', 'Engineer', '--verdict', 'applied', '--reason', 'confirmed',
                     '--update', code=1)
        self.assertEqual(before, (self.root / 'tracker.json').read_bytes())
        self.add('--id', '42')
        self.run_cli('apply', '--platform', 'liepin', '--id', '42', '--company', 'Second',
                     '--role', 'Engineer', '--evidence', 'confirmed', '--next', 'wait')
        self.add('--id', '42', '--update', '--verdict', 'stale')
        data = json.loads((self.root / 'tracker.json').read_text())
        self.assertEqual(data['seen_jobs'][0]['verdict'], 'stale')
        self.assertEqual(data['applications'][1]['status'], 'submitted')

    def test_read_only_commands_do_not_create_tracker(self):
        path = self.root / 'tracker.json'
        path.unlink()
        for args in [('status',), ('status', '--full'), ('sweep', '--dry-run'),
                     ('company', 'Example'), ('funnel',), ('seen', 'boss:1')]:
            self.assertIn('run init first', self.run_cli(*args, code=1).stderr)
            self.assertFalse(path.exists())
        self.run_cli('init')
        self.assertTrue(path.exists())


if __name__ == '__main__':
    unittest.main()

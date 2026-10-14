#!/usr/bin/env python3
"""Offline job tracker. Paths are relative to this repository, never the cwd."""
import argparse
from collections import Counter
from datetime import date, datetime, timezone
from html import escape, unescape
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
PLATFORMS = {'linkedin', 'indeed', 'boss', 'liepin', 'ats', 'email', 'referral', 'other'}
STATUSES = {'preparing', 'submitted', 'submitted_by_user', 'interviewing',
            'offer', 'rejected', 'closed', 'ghosted'}
VERDICTS = {'new', 'recommend', 'maybe', 'reject', 'applied', 'stale'}
FIELDS = {
    'applications': 'id company role platform job_url platform_job_id status evidence applied_at last_checked_at next_action notes legacy_ref'.split(),
    'seen_jobs': 'key company role platform url first_seen verdict reason report'.split(),
    'contacts': 'platform name company last_inbound last_outbound summary next_action'.split(),
}


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def normalize_url(value):
    p = urlsplit(value.strip())
    if p.scheme.lower() not in {'https', 'http'} or not p.hostname or p.username or p.password:
        raise ValueError('URL must be an http(s) address without credentials')
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in
             {'trk', 'trackingid', 'ref', 'refid', 'from', 'source', 'sessionid'}]
    if any(re.search(r'token|auth|cookie|password|secret', k, re.I) for k, _ in query):
        raise ValueError('URL contains credential-like parameters; use the public job link')
    netloc = p.hostname.lower()
    if p.port and p.port not in (80, 443):
        netloc += ':' + str(p.port)
    return urlunsplit(('https', netloc, p.path.rstrip('/') or '/', urlencode(sorted(query)), ''))


def url_identity(url):
    canonical = normalize_url(url)
    p = urlsplit(canonical)
    for host, platform, pattern in [
        ('zhipin.com', 'boss', r'/job_detail/([^/]+)\.html$'),
        ('liepin.com', 'liepin', r'/(?:job|a)/(\d+)\.shtml$'),
        ('linkedin.com', 'linkedin', r'/jobs/view/(?:[^/]*-)?(\d+)$'),
    ]:
        if p.hostname == host or p.hostname.endswith('.' + host):
            match = re.search(pattern, p.path)
            if match:
                return platform, match.group(1)
    return '', ''


def make_key(platform, job_id='', url=''):
    if platform not in PLATFORMS:
        raise ValueError('unknown platform')
    inferred, inferred_id = url_identity(url) if url else ('', '')
    if inferred and (inferred != platform or (job_id and job_id != inferred_id)):
        raise ValueError('platform or job id does not match the URL')
    job_id = job_id or inferred_id
    if job_id:
        if re.search(r'\s|[:/]', job_id):
            raise ValueError('job id must not contain whitespace, colons or slashes')
        return platform + ':' + job_id
    if url:
        return normalize_url(url)
    raise ValueError('either --id or --url is required')


def aliases(row):
    result = {row['key']}
    if row['url']:
        result.add(normalize_url(row['url']))
        result.add(make_key(row['platform'], url=row['url']))
    return result


def lookup(data, value):
    keys = {value}
    if value.startswith(('https://', 'http://')):
        keys.add(normalize_url(value))
        platform, job_id = url_identity(value)
        if platform:
            keys.add(make_key(platform, job_id))
    hits = [row for row in data['seen_jobs'] if keys & aliases(row)]
    # Applications that never went through seen_jobs still count as seen
    for app in data['applications']:
        url = app.get('job_url') or ''
        app_keys = {app['id']}
        if url:
            app_keys.add(normalize_url(url))
            platform, job_id = url_identity(url)
            if platform:
                app_keys.add(make_key(platform, job_id))
        if app.get('platform_job_id'):
            app_keys.add(make_key(app['platform'], app['platform_job_id']))
        if keys & app_keys:
            hits.append({'application': app['id'], 'company': app['company'], 'role': app['role'], 'status': app['status'], 'applied_at': app['applied_at']})
    return hits


def validate(data, root=ROOT):
    if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1:
        raise ValueError('version must be 1')
    if not isinstance(data.get('updated_at'), str) or 'T' not in data['updated_at']:
        raise ValueError('updated_at must be an ISO8601 timestamp')
    datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
    unique_ids, unique_jobs = set(), set()
    for group, fields in FIELDS.items():
        if not isinstance(data.get(group), list):
            raise ValueError(group + ' must be an array')
        for i, row in enumerate(data[group]):
            label = f'{group}[{i}]'
            if not isinstance(row, dict) or any(not isinstance(row.get(f), str) for f in fields):
                raise ValueError(label + ': missing or non-string field')
            if row['platform'] not in PLATFORMS:
                raise ValueError(label + ': invalid platform')
            for field in ('applied_at', 'first_seen', 'last_inbound', 'last_outbound'):
                if row.get(field):
                    date.fromisoformat(row[field])
            if row.get('last_checked_at'):
                datetime.fromisoformat(row['last_checked_at'].replace('Z', '+00:00'))
            for field in ('job_url', 'url'):
                if row.get(field):
                    normalize_url(row[field])
            if group == 'applications':
                if not row['id'] or row['id'] in unique_ids or row['status'] not in STATUSES:
                    raise ValueError(label + ': empty/duplicate application id or invalid status')
                unique_ids.add(row['id'])
                if not row['evidence'].strip():
                    raise ValueError(label + ': evidence is empty; use "unverified" if unknown')
                if row['job_url']:
                    make_key(row['platform'], row['platform_job_id'], row['job_url'])
            if group == 'seen_jobs':
                if not row['key'] or row['verdict'] not in VERDICTS:
                    raise ValueError(label + ': empty key or invalid verdict')
                if row['key'].startswith(('https://', 'http://')):
                    if row['key'] != normalize_url(row['key']):
                        raise ValueError(label + ': URL key is not normalized')
                    if not row['url'] or row['key'] != normalize_url(row['url']):
                        raise ValueError(label + ': key does not match URL')
                else:
                    prefix, sep, job_id = row['key'].partition(':')
                    if not sep or not job_id or row['key'] != make_key(prefix, job_id, row['url']):
                        raise ValueError(label + ': invalid key')
                    if prefix != row['platform']:
                        raise ValueError(label + ': key platform mismatch')
                ids = aliases(row)
                if ids & unique_jobs:
                    raise ValueError(label + ': duplicate job key/URL')
                unique_jobs.update(ids)
                if row['report']:
                    path = (root / row['report']).resolve()
                    if not row['report'].startswith('reports/jobs/') or not path.is_relative_to(root.resolve()) or not path.is_file():
                        raise ValueError(label + ': report path missing or outside the repository')


def atomic_write(path, text):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as f:
            temporary = f.name
            f.write(text)
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def status(data, full=False):
    apps = data['applications']
    counts = Counter(x['status'] for x in apps)
    print(f"applications: {len(apps)} | " + ', '.join(f'{k}={v}' for k, v in sorted(counts.items())))
    active = {'preparing', 'submitted', 'submitted_by_user', 'interviewing', 'offer'}
    shown = apps if full else [x for x in apps if x['status'] in active]
    for row in sorted(shown, key=lambda x: x['applied_at'], reverse=True):
        print(f"  [{row['status']}] {row['company'][:24]} | {row['role'][:30]} | {row['next_action'][:80 if not full else None]}")
    verdicts = {'recommend', 'maybe'} if full else {'recommend'}
    rows = [x for x in data['seen_jobs'] if x['verdict'] in verdicts]
    print(f"\nJobs to decide ({'/'.join(sorted(verdicts))}, {len(rows)}; --full shows maybe and contacts):")
    for row in rows:
        print(f"  {row['key']} | {row['company'][:24]} | {row['role'][:30]} | {row['verdict']}")
    if full:
        print('\nContacts:')
        for row in data['contacts']:
            print(f"  {row['name']} | {row['company']} | {row['next_action']}")


def find_app(data, ref):
    hits = [x for x in data['applications'] if x['id'] == ref]
    hits = hits or [x for x in data['applications'] if ref.lower() in (x['company'] + x['role']).lower()]
    if len(hits) != 1:
        raise ValueError(f'{len(hits)} applications match: ' + '; '.join(x['id'] for x in hits))
    return hits[0]




def load_deadline(root=ROOT):
    """Optional target date from config.json ({"deadline": "YYYY-MM-DD"})."""
    try:
        value = json.loads((root / 'config.json').read_text(encoding='utf-8')).get('deadline')
        return date.fromisoformat(value) if value else None
    except (FileNotFoundError, ValueError, AttributeError, TypeError):
        return None


PLATFORM_LABELS = {'boss': 'BOSS Zhipin', 'liepin': 'Liepin', 'linkedin': 'LinkedIn', 'indeed': 'Indeed',
                   'ats': 'Company site', 'email': 'Email', 'referral': 'Referral', 'other': 'Other'}
STATUS_LABELS = {'preparing': 'Preparing', 'submitted': 'Waiting', 'submitted_by_user': 'Waiting · applied by you',
                 'interviewing': 'Interviewing', 'offer': 'Offer', 'rejected': 'Rejected', 'closed': 'Closed', 'ghosted': 'No reply'}
STATUS_TONE = {'interviewing': 'good', 'offer': 'good', 'rejected': 'muted', 'closed': 'muted', 'ghosted': 'muted', 'preparing': 'warn'}
BOARD_CSS = '''
:root{color-scheme:dark;--bg:#141413;--fg:#faf9f5;--dim:#a3a097;--panel:#1f1e1d;--panel2:#262624;--line:#33322f;
--accent:#d97757;--accent-ink:#e8936f;--good:#8fb07c;--warn:#d6a854;--muted:#6b6a65;
--serif:"Iowan Old Style","Palatino","Songti SC","STSong",Georgia,serif;
--sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Helvetica Neue",sans-serif}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:14px/1.6 var(--sans);margin:0 auto;padding:28px 24px 56px;max-width:760px;overflow-wrap:anywhere}
a{color:var(--accent-ink);text-decoration:none}a:hover{text-decoration:underline}
a:focus-visible,summary:focus-visible{outline:2px solid var(--accent-ink);outline-offset:4px}
header{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-bottom:16px;margin-bottom:24px;border-bottom:1px solid var(--line)}
h1{font:400 26px/1.2 var(--serif);margin:0}header time{white-space:nowrap;font-size:12px;color:var(--dim)}
h2,.fold>summary{font:400 21px/1.4 var(--serif);margin:28px 0 12px;color:var(--fg)}
h2 small,.fold>summary small,.dim{color:var(--dim);font:400 12px/1.6 var(--sans)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 18px;margin:16px 0}
.panel h2{margin:0 0 12px}.decision{border-left:4px solid var(--accent)}
.markdown p{margin:0 0 12px}.markdown ul,.markdown ol{margin:0 0 12px;padding-left:22px}
.markdown li{margin:8px 0}.markdown>:last-child{margin-bottom:0}
code{background:var(--panel2);border-radius:4px;padding:2px 5px;font-size:12px}
.metrics{display:flex;flex-wrap:wrap;gap:6px 20px;padding:12px 0;border-block:1px solid var(--line);font-size:12px;color:var(--dim)}
.metrics span{white-space:nowrap}.metrics b{color:var(--fg);font-weight:500;font-variant-numeric:tabular-nums;margin-left:5px}
.cards{display:flex;flex-direction:column;gap:10px}
.card{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 18px}
.card:has(.stretch):hover,.card:focus-within{border-color:var(--accent)}
.card.rec{box-shadow:inset 3px 0 0 var(--accent)}
.card-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.co{font:500 16px/1.4 var(--serif)}.role{margin:6px 0}.role .tag{margin-left:8px}
.card .why{color:var(--dim);font-size:13px;white-space:pre-line;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card a.stretch::after{content:"";position:absolute;inset:0;border-radius:8px}
.card a.over{position:relative;z-index:1;font-size:12px;white-space:nowrap}
.tag{display:inline-block;font-size:11px;padding:1px 6px;border-radius:4px;background:var(--panel2);color:var(--dim)}
.pill{display:inline-block;font-size:11px;padding:1px 7px;border-radius:4px;white-space:nowrap;background:rgba(217,119,87,.16);color:var(--accent-ink)}
.pill.good{background:rgba(95,125,78,.13);color:var(--good)}.pill.warn{background:rgba(184,134,43,.13);color:var(--warn)}.pill.muted{background:var(--panel2);color:var(--dim)}
.entries{list-style:none;padding:0;margin:0}.entry{padding:14px 0;border-bottom:1px solid var(--line)}
.entry-line{display:flex;flex-wrap:wrap;gap:4px 7px;align-items:baseline;font-size:13px}
.entry-line .age{white-space:nowrap;font-variant-numeric:tabular-nums}.entry.muted{color:var(--dim);opacity:.6}
.sub{color:var(--dim);font-size:12px;margin:5px 0 0}
details{margin-top:6px}summary{cursor:pointer;color:var(--dim);font-size:12px}
.evidence p{margin:6px 0 0;color:var(--dim);font-size:12px;white-space:pre-wrap}
'''


def board(data, root=ROOT):
    def link(url, text, cls=''):
        if link_allowed(url, root):
            return ('<a' + (' class="' + cls + '"' if cls else '') + ' href="'
                    + escape(url, quote=True) + '">' + escape(text) + '</a>')
        return escape(text)

    def cards(rows):
        items = ['<div class="cards">']
        for row in rows:
            # A report is a literal repository filename, so quote #, spaces, etc.
            report = quote(row['report'], safe='/') if row['report'] else ''
            has_report = bool(report) and link_allowed(report, root)
            target = report if has_report else row['url']
            original = link(row['url'], 'Original ↗', 'over') if has_report else ''
            kind = 'rec' if row['verdict'] == 'recommend' else 'maybe'
            items.append(f'<article class="card {kind}"><div class="card-head">'
                         f'<span class="co">{escape(row["company"])}</span>{original}</div>'
                         f'<div class="role">{link(target, row["role"], "stretch")}'
                         f'<span class="tag">{escape(PLATFORM_LABELS.get(row["platform"], row["platform"]))}</span></div>'
                         f'<div class="why">{escape(row["reason"])}</div></article>')
        if not rows:
            items.append('<p class="dim">Nothing yet</p>')
        return '\n'.join(items) + '</div>'

    generated = datetime.now().astimezone()
    today = generated.date()
    apps = data['applications']
    active = [a for a in apps if a['status'] not in {'closed', 'rejected', 'ghosted'}]
    waiting = sum(a['status'] in {'submitted', 'submitted_by_user'} for a in apps)
    interviewing = sum(a['status'] == 'interviewing' for a in apps)
    rec = [x for x in data['seen_jobs'] if x['verdict'] == 'recommend']
    maybe = [x for x in data['seen_jobs'] if x['verdict'] == 'maybe']
    metrics = [('Applied', len(apps)), ('Waiting', waiting), ('Interviewing', interviewing)]
    deadline = load_deadline(root)
    if deadline:
        metrics.append(('Days left', max(0, (deadline - today).days)))
    out = ['<!doctype html><html lang="en"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">'
           '<meta http-equiv="refresh" content="60"><title>Job Board</title><style>'
           + BOARD_CSS + '</style></head><body>',
           '<header><h1>Job Board</h1><time datetime="' + generated.isoformat(timespec='seconds')
           + '">Updated ' + generated.strftime('%m-%d %H:%M') + '</time></header>']
    sections = handoff_sections(root)
    for keyword, title, cls in [('Needs you', 'Needs your decision', ' decision'), ('In progress', 'In progress', '')]:
        body = '\n\n'.join(body for heading, body in sections if keyword in heading).strip()
        if body:
            out.append('<section class="panel' + cls + '"><h2>' + title
                       + '</h2><div class="markdown">' + markdown(body, root) + '</div></section>')
    out.append('<div class="metrics">' + ''.join(
        f'<span>{label}<b>{value}</b></span>' for label, value in metrics) + '</div>')
    out.append(f'<section><h2>Recommended <small>{len(rec)}</small></h2>{cards(rec)}</section>')
    out.append(f'<details class="fold"><summary>Maybe <small>{len(maybe)}</small></summary>{cards(maybe)}</details>')

    # Newest application first; interviews float to the top, finished ones sink.
    group = {'interviewing': 0, 'offer': 0, 'ghosted': 2, 'rejected': 2, 'closed': 2}
    rows = sorted(apps, key=lambda a: a['applied_at'], reverse=True)
    rows.sort(key=lambda a: group.get(a['status'], 1))
    out.append(f'<section><h2>Applications <small>{len(active)} active / {len(apps)} total</small></h2><ul class="entries">')
    reports = {}
    for row in data['seen_jobs']:
        if row['report'] and row['url']:
            reports[url_identity(row['url'])] = quote(row['report'], safe='/')
            reports[normalize_url(row['url'])] = quote(row['report'], safe='/')
    for a in rows:
        rep = ''
        if a['job_url']:
            rep = reports.get(url_identity(a['job_url'])) if url_identity(a['job_url']) != ('', '') else None
            rep = rep or reports.get(normalize_url(a['job_url']), '')
        if not rep:
            for row in sorted(data['seen_jobs'], key=lambda r: r['verdict'] != 'applied'):
                if row['report'] and row['company'][:6] == a['company'][:6]:
                    rep = quote(row['report'], safe='/')
                    break
        rep_html = (' · <a href="' + escape(rep, quote=True) + '">report</a>') if rep and link_allowed(rep, root) else ''
        try:
            age = str((today - date.fromisoformat(a['applied_at'])).days) + 'd'
        except ValueError:
            age = 'date unknown'
        tone = STATUS_TONE.get(a['status'], '')
        muted = ' muted' if a['status'] in {'closed', 'rejected', 'ghosted'} else ''
        out.append(f'<li class="entry{muted}"><div class="entry-line"><span>{escape(a["company"])}</span> · '
                   f'{link(a["job_url"], a["role"])} · '
                   f'<span>{escape(PLATFORM_LABELS.get(a["platform"], a["platform"]))}</span> · '
                   f'<span class="pill {tone}">{escape(STATUS_LABELS.get(a["status"], a["status"]))}</span> · '
                   f'<span class="age">{age}</span>{rep_html}</div><p class="sub">{escape(a["next_action"])}</p>'
                   f'<details class="evidence"><summary>Evidence</summary><p>{escape(a["evidence"])}</p></details></li>')
    out.append('</ul></section>')

    out.append(f'<details class="fold"><summary>Contacts <small>{len(data["contacts"])}</small></summary><ul class="entries">')
    for c in data['contacts']:
        last = ' / '.join(label + c[field] for label, field in [('them ', 'last_inbound'), ('us ', 'last_outbound')] if c[field])
        out.append(f'<li class="entry"><div class="entry-line"><span>{escape(c["name"])}</span> · '
                   f'<span>{escape(c["company"])}</span> · '
                   f'<span class="tag">{escape(PLATFORM_LABELS.get(c["platform"], c["platform"]))}</span></div>'
                   f'<p class="sub">{escape(last)}</p><p class="sub">{escape(c["next_action"])}</p>'
                   f'<details class="evidence"><summary>History</summary><p>{escape(c["summary"])}</p></details></li>')
    out.append('</ul></details></body></html>')
    atomic_write(root / 'board.html', '\n'.join(out))
    print('wrote board.html')


def link_allowed(value, root=ROOT):
    """Accept http(s) URLs or relative references contained in this repository."""
    if not value or re.search(r'[\s\\\x00-\x1f\x7f]', value):
        return False
    try:
        parsed = urlsplit(value)
        if parsed.scheme:
            return parsed.scheme.lower() in {'http', 'https'} and bool(parsed.hostname)
        path = unquote(parsed.path)
        if parsed.netloc or path.startswith('/') or re.search(r'[\\\x00-\x1f\x7f]', path):
            return False
        return (root / path).resolve().is_relative_to(root.resolve())
    except (ValueError, OSError, RuntimeError):
        return False


def inline(text, root=ROOT):
    # Escape before parsing. A single pass keeps generated tags/attributes out
    # of subsequent substitutions; code contents are always literal.
    def render(escaped):
        pattern = r'`([^`]+)`|\*\*(.+?)\*\*|\[([^\]\n]+)\]\(([^)\n]*)\)'
        out, pos = [], 0
        for match in re.finditer(pattern, escaped):
            out.append(escaped[pos:match.start()])
            code, bold, label, url = match.groups()
            if code is not None:
                out.append('<code>' + code + '</code>')
            elif bold is not None:
                out.append('<strong>' + render(bold) + '</strong>')
            elif link_allowed(unescape(url), root):
                out.append('<a href="' + url + '">' + label + '</a>')
            else:
                out.append(match.group())
            pos = match.end()
        out.append(escaped[pos:])
        return ''.join(out)
    return render(escape(text, quote=True))


def markdown(text, root=ROOT):
    out, paragraph, list_kind = [], [], None

    def flush_paragraph():
        if paragraph:
            out.append('<p>' + inline('\n'.join(paragraph), root) + '</p>')
            paragraph.clear()

    for line in text.splitlines():
        item = re.match(r'^(?:- |\d+\. )(.*)$', line)
        kind = ('ul' if line.startswith('- ') else 'ol') if item else None
        if list_kind and kind != list_kind:
            out.append('</' + list_kind + '>')
            list_kind = None
        if item:
            flush_paragraph()
            if not list_kind:
                out.append('<' + kind + '>')
                list_kind = kind
            out.append('<li>' + inline(item.group(1), root) + '</li>')
        elif line.strip():
            paragraph.append(line)
        else:
            flush_paragraph()
    flush_paragraph()
    if list_kind:
        out.append('</' + list_kind + '>')
    return '\n'.join(out) or '<p class="dim">Nothing yet</p>'


def handoff_sections(root):
    try:
        text = (root / '.agent-memory/handoff.md').read_text(encoding='utf-8')
    except FileNotFoundError:
        return []
    sections = []
    for line in text.splitlines():
        if line.startswith('## '):
            sections.append((line[3:].strip(), []))
        elif sections:
            sections[-1][1].append(line)
    return [(title, '\n'.join(lines)) for title, lines in sections]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('check', 'board'):
        sub.add_parser(command)
    sub.add_parser('init', help='create an empty tracker.json if missing')
    sub.add_parser('demo', help='render board.html from examples/ without touching your data')
    sub.add_parser('status').add_argument('--full', action='store_true')
    sub.add_parser('seen').add_argument('key')
    add = sub.add_parser('add-seen')
    add.add_argument('--platform', choices=sorted(PLATFORMS), required=True)
    for flag in ('id', 'url', 'report'):
        add.add_argument('--' + flag, default='')
    for flag in ('company', 'role', 'reason'):
        add.add_argument('--' + flag, required=True)
    add.add_argument('--verdict', choices=sorted(VERDICTS), required=True)
    add.add_argument('--update', action='store_true', help='if it exists, change verdict and prepend reason')
    app = sub.add_parser('apply', help='record an application and mark the seen job as applied')
    app.add_argument('--platform', choices=sorted(PLATFORMS), required=True)
    for flag in ('id', 'url', 'notes'):
        app.add_argument('--' + flag, default='')
    for flag in ('company', 'role', 'evidence', 'next'):
        app.add_argument('--' + flag, required=True)
    app.add_argument('--status', choices=sorted(STATUSES), default='submitted')
    upd = sub.add_parser('update', help='update an application; ref is its id or a unique company/role substring')
    upd.add_argument('ref')
    upd.add_argument('--status', choices=sorted(STATUSES))
    upd.add_argument('--next')
    upd.add_argument('--note', help='append to notes')
    args = parser.parse_args(argv)
    try:
        if args.command == 'demo':
            demo = ROOT / 'examples'
            board(json.loads((demo / 'tracker.json').read_text(encoding='utf-8')), demo)
            print('open examples/board.html')
            return 0
        tracker = ROOT / 'tracker.json'
        if not tracker.exists():
            atomic_write(tracker, json.dumps(dict(version=1, updated_at=now(), applications=[],
                                                  seen_jobs=[], contacts=[]), indent=2) + '\n')
            print('created empty tracker.json')
        if args.command == 'init':
            return 0
        data = json.loads(tracker.read_text(encoding='utf-8'))
        validate(data)
        if args.command == 'check':
            print(f"OK: applications={len(data['applications'])}, seen_jobs={len(data['seen_jobs'])}, contacts={len(data['contacts'])}")
        elif args.command == 'seen':
            matches = lookup(data, args.key)
            print(json.dumps(matches, ensure_ascii=False, indent=2) if matches else 'not seen')
            return 0 if matches else 1
        elif args.command == 'add-seen':
            key = make_key(args.platform, args.id, args.url)
            existing = lookup(data, key) or (lookup(data, args.url) if args.url else [])
            if existing and args.update:
                for row in existing:
                    row['verdict'] = args.verdict
                    row['reason'] = f"{args.reason}; {row['reason']}"
                data['updated_at'] = now()
                validate(data)
                atomic_write(ROOT / 'tracker.json', json.dumps(data, ensure_ascii=False, indent=2) + '\n')
                print('updated ' + ', '.join(r['key'] for r in existing))
                return 0
            if existing:
                print('duplicate job: ' + json.dumps(existing, ensure_ascii=False, indent=2), file=sys.stderr)
                return 1
            data['seen_jobs'].append(dict(key=key, company=args.company, role=args.role,
                platform=args.platform, url=normalize_url(args.url) if args.url else '',
                first_seen=date.today().isoformat(), verdict=args.verdict, reason=args.reason, report=args.report))
            data['updated_at'] = now()
            validate(data)
            atomic_write(ROOT / 'tracker.json', json.dumps(data, ensure_ascii=False, indent=2) + '\n')
            print('added ' + key)
        elif args.command == 'status':
            status(data, args.full)
        elif args.command == 'apply':
            today = date.today().isoformat()
            ref = re.sub(r'[^A-Za-z0-9]+', '-', args.id or urlsplit(args.url).path)[-40:].strip('-') or 'x'
            app_id = f"app-{today.replace('-', '')}-{args.platform}-{ref}"
            if args.url or args.id:
                for row in lookup(data, make_key(args.platform, args.id, args.url)) or (lookup(data, args.url) if args.url else []):
                    row['verdict'] = 'applied'
            data['applications'].append(dict(id=app_id, company=args.company, role=args.role, platform=args.platform,
                job_url=normalize_url(args.url) if args.url else '', platform_job_id=args.id, status=args.status,
                evidence=args.evidence, applied_at=today, last_checked_at=now(), next_action=args.next,
                notes=args.notes, legacy_ref=''))
            data['updated_at'] = now()
            validate(data)
            atomic_write(ROOT / 'tracker.json', json.dumps(data, ensure_ascii=False, indent=2) + '\n')
            print('recorded ' + app_id)
        elif args.command == 'update':
            row = find_app(data, args.ref)
            if args.status:
                row['status'] = args.status
            if args.next:
                row['next_action'] = args.next
            if args.note:
                row['notes'] = (row['notes'] + '; ' if row['notes'] else '') + f'{date.today().isoformat()} {args.note}'
            row['last_checked_at'] = data['updated_at'] = now()
            validate(data)
            atomic_write(ROOT / 'tracker.json', json.dumps(data, ensure_ascii=False, indent=2) + '\n')
            print('updated ' + row['id'])
        else:
            board(data)
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print('error: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

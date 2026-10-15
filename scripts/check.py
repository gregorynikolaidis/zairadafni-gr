"""Validate local HTML, CSS, gallery links and required imported pages."""
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'site'
errors = []
count = 0


def check(ref, base):
    global count
    if not ref or ref.startswith(('#', 'data:', 'mailto:', 'tel:', 'javascript:')):
        return
    url = urlsplit(urljoin(base, ref))
    if url.netloc != 'local':
        return
    path = ROOT / unquote(url.path).lstrip('/')
    if url.path.endswith('/'):
        path /= 'index.html'
    count += 1
    if not path.is_file():
        errors.append(f'{base}: missing {ref}')


class Page(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag != 'base':
            for key in ('href', 'src'):
                if key in attrs:
                    check(attrs[key], 'https://local/')


pages = list(ROOT.rglob('*.html'))
assert len(pages) == 12, f'Expected 11 sitemap pages and root, found {len(pages)}'
for page in pages:
    text = page.read_text()
    assert '<base href="/"' in text, str(page)
    assert '<html lang="el">' in text, str(page)
    assert 'googletagmanager.com' not in text and 'statcounter.com' not in text
    Page().feed(text)
    for ref in re.findall(r'"(?:image|thumb)":"([^"]+)"', text):
        check(ref.replace('\\/', '/'), 'https://local/')
for css in ROOT.rglob('*.css'):
    for match in re.finditer(r'url\(\s*(?:[\"\']([^\"\']+)[\"\']|([^\s)]+))\s*\)', css.read_text()):
        check(match.group(1) or match.group(2), 'https://local/' + str(css.relative_to(ROOT)))
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Checked {len(pages)} HTML documents and {count} local references: OK')

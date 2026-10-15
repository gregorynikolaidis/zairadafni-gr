#!/usr/bin/env python3
"""Import the public Zyro site into site/, with local links and no analytics.

Explicit refresh only: overwrites imported files. Uses only Python's standard library.
"""
import hashlib
import html
import json
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site'
ORIGIN = 'https://www.zairadafni.gr/'
HOSTS = {'www.zairadafni.gr', 'zairadafni.gr'}
records = {}
unavailable = []


def fetch(url):
    encoded = quote(url, safe=":/?=&%+;,@")
    for attempt in range(3):
        try:
            with urlopen(Request(encoded, headers={'User-Agent': 'ZairaDafni-site-copy/1.0'}), timeout=30) as response:
                return response.read(), response.headers.get_content_type()
        except HTTPError as error:
            if error.code == 404:
                raise
            if attempt == 2:
                raise
            time.sleep(1)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1)


def local_path(url):
    path = unquote(urlsplit(url).path).lstrip('/')
    if '..' in Path(path).parts:
        raise ValueError('Unsafe path: ' + path)
    if not path or path.endswith('/'):
        path += 'index.html'
    return path


def save(url, data, kind):
    path = local_path(url)
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    records[path] = {'url': url, 'content_type': kind, 'bytes': len(data),
                     'sha256': hashlib.sha256(data).hexdigest()}


def clean_page(text):
    text = re.sub(r'<!-- Global site tag.*?</script>\s*<script>.*?</script>', '', text, flags=re.S)
    text = re.sub(r'<!-- Start of StatCounter.*?<!-- End of StatCounter Code[^>]*-->', '', text, flags=re.S)
    text = re.sub(r'<!--\[if lt IE 9\]>.*?<!\[endif\]-->', '', text, flags=re.S)
    text = re.sub(r'<script[^>]+src="/cdn-cgi/[^>]+></script>', '', text)
    def decode_email(match):
        value = bytes.fromhex(match.group(1))
        address = bytes(b ^ value[0] for b in value[1:]).decode()
        return '<a href="mailto:' + html.escape(address) + '">' + html.escape(address) + '</a>'
    text = re.sub(r'<a[^>]*data-cfemail="([a-f0-9]+)"[^>]*>.*?</a>', decode_email, text)
    text = re.sub(r'<html lang="en">', '<html lang="el">', text)
    text = re.sub(r'<script[^>]+src="https://maps.googleapis.com/[^>]+></script><script[^>]*>.*?</script>',
                  '<iframe title="Χάρτης — Ζαΐρα Δαφνή" width="100%" height="100%" '
                  'style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
                  'src="https://maps.google.com/maps?q=38.111760946775284,23.877431163229403&amp;z=16&amp;output=embed"></iframe>',
                  text, flags=re.S)
    text = re.sub(r'<base href="[^"]+"\s*/?>', '<base href="/" />', text)
    for host in HOSTS:
        text = text.replace('https://' + host + '/', '/').replace('http://' + host + '/', '/')
    return text


def refs(text, base, is_page=False):
    # JSON image references in the gallery contain escaped slashes.
    text = text.replace('\\/', '/')
    found = re.findall(r'(?:src|href)\s*=\s*[\"\']([^\"\']+)', text)
    found += [m.group(1) or m.group(2) for m in re.finditer(r'url\(\s*(?:[\"\']([^\"\']+)[\"\']|([^\s)]+))\s*\)', text)]
    found += re.findall(r'[\"\']((?:gallery_gen|gallery|images|fonts|js|css)/[^\"\']+)[\"\']', text)
    for ref in found:
        if ref in ('null', '#') or ref.startswith(('data:', 'javascript:', 'mailto:', 'tel:', '#')):
            continue
        url = urlsplit(urljoin(base, html.unescape(ref)))
        if url.hostname in HOSTS and not url.path.startswith('/cdn-cgi/'):
            yield ORIGIN.rstrip('/') + url.path


def main():
    sitemap, _ = fetch(urljoin(ORIGIN, 'sitemap.xml'))
    urls = [ORIGIN] + [ORIGIN.rstrip('/') + urlsplit(e.text).path
                      for e in ET.fromstring(sitemap).iter()
                      if e.tag.endswith('loc')]
    queue = list(dict.fromkeys(urls))
    seen = set()
    while queue:
        url = queue.pop(0)
        path = local_path(url)
        if path in seen or path in records:
            continue
        seen.add(path)
        try:
            data, kind = fetch(url)
        except HTTPError as error:
            if error.code != 404 or path.endswith('index.html'):
                raise
            unavailable.append(url)
            print('Missing on source: ' + url, flush=True)
            continue
        if kind == 'text/html':
            if path != 'index.html' and not path.endswith('/index.html'):
                raise ValueError('Expected asset but received HTML: ' + url)
            text = clean_page(data.decode('utf-8'))
            queue.extend(refs(text, ORIGIN, True))
            data = text.encode('utf-8')
        elif kind in ('text/css', 'text/javascript', 'application/javascript') or path.endswith(('.css', '.js')):
            text = data.decode('utf-8-sig')
            if path == 'css/site.css':
                # This builder bundles many unused font families. Keep Open Sans,
                # the only web font referenced by the published page styles.
                text = re.sub(r'@font-face\s*\{[^}]*\}',
                              lambda m: m.group(0) if "font-family: 'Open Sans';" in m.group(0) else '', text)
                def local_font(match):
                    font_url = match.group(0)
                    font_data, font_kind = fetch(font_url)
                    font_path = 'fonts/' + urlsplit(font_url).path.rsplit('/', 1)[-1]
                    save(ORIGIN + font_path, font_data, font_kind)
                    return '/' + font_path
                text = re.sub(r'https://themes\.googleusercontent\.com/[^\s)\"\']+', local_font, text)
            queue.extend(refs(text, url))
            # The builder emits invalid list image placeholders; browsers request css/null.
            text = text.replace("url('null')", 'none').replace('url("null")', 'none')
            data = text.encode('utf-8')
        save(url, data, kind)
        print(path, flush=True)
    # Remove only CSS references that also return 404 on the original site.
    for path in list(records):
        if path.endswith('.css'):
            target = OUT / path
            text = target.read_text()
            def remove_missing(match):
                ref = (match.group(1) or match.group(2))
                url = urljoin(ORIGIN + path, ref)
                return 'none' if url in unavailable else match.group(0)
            text = re.sub(r'url\(\s*(?:[\"\']([^\"\']+)[\"\']|([^\s)]+))\s*\)', remove_missing, text)
            save(ORIGIN + path, text.encode(), records[path]['content_type'])
    report = {'source': ORIGIN, 'captured_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'unavailable_on_source': unavailable,
              'transformations': ['local base URL', 'remove analytics and obsolete IE shim',
                                  'decode public email links', 'Greek document language',
                                  'remove invalid CSS null image placeholders',
                                  'local Open Sans fonts; drop unused font declarations',
                                  'replace legacy Maps API script with keyless embed at same coordinates'],
              'files': dict(sorted(records.items()))}
    (ROOT / 'docs').mkdir(exist_ok=True)
    (ROOT / 'docs' / 'import-manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'Imported {len(records)} files.')


if __name__ == '__main__':
    main()

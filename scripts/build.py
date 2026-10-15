"""Build the website for a domain root or a GitHub Pages project path."""
import argparse
import re
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-path', default='/', help='URL path, e.g. /zairadafni-gr/')
args = parser.parse_args()
base = args.base_path
if not re.fullmatch(r'/(?:[A-Za-z0-9_-]+/)*', base):
    parser.error('--base-path must start and end with / and contain path segments only')

output = root / 'dist'
if output.exists():
    shutil.rmtree(output)
shutil.copytree(root / 'site', output)
for page in output.rglob('*.html'):
    text = page.read_text(encoding='utf-8')
    text = re.sub(r'((?:href|src)=["\'])/(?!/)', lambda m: m[1] + base, text)
    page.write_text(text, encoding='utf-8')
for css in output.rglob('*.css'):
    text = css.read_text(encoding='utf-8')
    text = re.sub(r'(url\(\s*["\']?)/(?!/)', lambda m: m[1] + base, text)
    css.write_text(text, encoding='utf-8')
print(f'Static website ready in dist/ (base path: {base})')

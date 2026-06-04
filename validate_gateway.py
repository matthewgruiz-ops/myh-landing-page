from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import hashlib

ROOT = Path('/home/ubuntu/myh_repo_audit/myh-landing-page')
ROUTES = ['index.html', 'legacy/index.html', 'onboard/index.html', 'world-map/index.html', 'ecosystem/index.html']
EXPECTED_LEGACY_SHA256 = '4f84c470277bafd157b44752c7e1339d12c5dd6d194eead47c7ff3db3adbb074'

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.assets = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'href' in attrs:
            self.links.append(attrs['href'])
        if 'src' in attrs:
            self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet' and 'href' in attrs:
            self.assets.append(attrs['href'])

errors = []
for rel in ROUTES:
    path = ROOT / rel
    if not path.exists():
        errors.append(f'Missing route file: {rel}')
    elif path.stat().st_size < 2000:
        errors.append(f'Route file unexpectedly small: {rel}')

legacy = ROOT / 'legacy/index.html'
legacy_hash = hashlib.sha256(legacy.read_bytes()).hexdigest()
if legacy_hash != EXPECTED_LEGACY_SHA256:
    errors.append(f'Legacy checksum changed: {legacy_hash}')

for rel in ROUTES:
    path = ROOT / rel
    if not path.exists():
        continue
    parser = LinkParser()
    parser.feed(path.read_text(encoding='utf-8'))
    for ref in parser.assets:
        parsed = urlparse(ref)
        if parsed.scheme in {'http', 'https', 'mailto'} or ref.startswith('//'):
            continue
        if ref.startswith('/'):
            asset_path = ROOT / ref.lstrip('/')
        else:
            asset_path = path.parent / ref
        if not asset_path.exists():
            errors.append(f'Missing asset referenced by {rel}: {ref}')
    for href in parser.links:
        if href.startswith('#') or href.startswith('mailto:'):
            continue
        parsed = urlparse(href)
        if parsed.scheme in {'http', 'https'}:
            continue
        base = href.split('#', 1)[0]
        if not base:
            continue
        if base.startswith('/'):
            target = ROOT / base.lstrip('/')
        else:
            target = path.parent / base
        if base.endswith('/'):
            target = target / 'index.html'
        if target.is_dir():
            target = target / 'index.html'
        if not target.exists():
            errors.append(f'Missing internal link target from {rel}: {href}')

print('Validation summary')
print('Routes checked:', ', '.join(ROUTES))
print('Legacy SHA256:', legacy_hash)
if errors:
    print('FAIL')
    for err in errors:
        print('-', err)
    raise SystemExit(1)
print('PASS')

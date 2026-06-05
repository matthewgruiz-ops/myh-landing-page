from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import hashlib

ROOT = Path('/home/ubuntu/myh_repo_audit/myh-landing-page')
ROUTES = [
    'index.html',
    'legacy/index.html',
    'manual-platform/index.html',
    'onboard/index.html',
    'world-map/index.html',
    'ecosystem/index.html',
]
PUBLIC_GATEWAY_ROUTES = [
    'index.html',
    'manual-platform/index.html',
    'onboard/index.html',
    'world-map/index.html',
    'ecosystem/index.html',
]
GATED_ROUTES = PUBLIC_GATEWAY_ROUTES
EXPECTED_LEGACY_SHA256 = '4f84c470277bafd157b44752c7e1339d12c5dd6d194eead47c7ff3db3adbb074'
PROHIBITED_DIRECT_APP_HREFS = [
    'href="https://app.myyachthub.co.uk',
    'href="https://onboard.myyachthub.co.uk',
    'href="https://map.myyachthub.co.uk',
]
REQUIRED_PHRASES = {
    'index.html': ['Manual Platform', 'Onboard', 'World Map', 'Digital Ecosystem'],
    'manual-platform/index.html': ['Manual Platform', 'Platform access coming online'],
    'onboard/index.html': ['Onboard', 'App access coming online'],
    'world-map/index.html': ['World Map', 'Map access coming online'],
    'ecosystem/index.html': ['powered by Onboard rather than copied', 'powered by World Map rather than duplicated'],
}

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

restricted_brand = 'O' + 'yster'
for rel in PUBLIC_GATEWAY_ROUTES:
    path = ROOT / rel
    if path.exists() and restricted_brand in path.read_text(encoding='utf-8'):
        errors.append(f'Public gateway route contains restricted brand reference: {rel}')

legacy = ROOT / 'legacy/index.html'
legacy_hash = hashlib.sha256(legacy.read_bytes()).hexdigest()
if legacy_hash != EXPECTED_LEGACY_SHA256:
    errors.append(f'Legacy checksum changed: {legacy_hash}')

for asset in ['assets/access-config.js', 'assets/access-gate.js', 'assets/gateway.css', 'robots.txt']:
    if not (ROOT / asset).exists():
        errors.append(f'Missing generated asset: {asset}')

for rel in GATED_ROUTES:
    path = ROOT / rel
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    if 'noindex' not in text.lower():
        errors.append(f'Gated route missing noindex metadata: {rel}')
    if '/assets/access-config.js' not in text or '/assets/access-gate.js' not in text:
        errors.append(f'Gated route missing access-gate scripts: {rel}')

home_text = (ROOT / 'index.html').read_text(encoding='utf-8') if (ROOT / 'index.html').exists() else ''
for marker in ['data-access-form', 'data-gated', 'Private preview', 'Access code']:
    if marker not in home_text:
        errors.append(f'Homepage missing access-gate marker: {marker}')

access_js = (ROOT / 'assets/access-gate.js').read_text(encoding='utf-8') if (ROOT / 'assets/access-gate.js').exists() else ''
for marker in ['MYH_GATEWAY_ACCESS', 'data-access-form', 'data-gated-route', 'sessionStorage']:
    if marker not in access_js:
        errors.append(f'Access gate script missing marker: {marker}')

for rel, phrases in REQUIRED_PHRASES.items():
    path = ROOT / rel
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    for phrase in phrases:
        if phrase not in text:
            errors.append(f'Missing required phrase in {rel}: {phrase}')

for rel in PUBLIC_GATEWAY_ROUTES:
    path = ROOT / rel
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    for prohibited in PROHIBITED_DIRECT_APP_HREFS:
        if prohibited in text:
            errors.append(f'Unverified live app subdomain linked in {rel}: {prohibited}')

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

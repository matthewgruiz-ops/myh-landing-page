import json
import os
from pathlib import Path

ROOT = Path('/home/ubuntu/myh_repo_audit/myh-landing-page')

LOGO = '''<svg class="brand-mark" viewBox="0 0 48 56" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><path d="M24 4L39 15V41L24 52L9 41V15L24 4Z" stroke="#c9a96e" stroke-width="2"/><path d="M24 12V44" stroke="#f2ead6" stroke-width="1.6"/><path d="M15 29C18 24 21 21.5 24 21.5C27 21.5 30 24 33 29" stroke="#77c6c2" stroke-width="1.6" stroke-linecap="round"/><path d="M16 35C21 38 27 38 32 35" stroke="#c9a96e" stroke-width="1.6" stroke-linecap="round"/></svg>'''

APP_LINKS = {
    'manual': {
        'label': 'Manual Platform',
        'route': '/manual/',
        'anchor': '#platform-access',
        'intended_url': 'https://app.myyachthub.co.uk',
        'live': False,
        'primary_label': 'Open Platform',
        'status_label': 'Platform access coming online',
        'domain_note': 'Standalone platform target: <strong>app.myyachthub.co.uk</strong>. This page avoids linking to that subdomain until the existing Manual / Vessel Knowledge Platform deployment is live and tested.',
    },
    'onboard': {
        'label': 'Onboard',
        'route': '/onboard/',
        'anchor': '#app-access',
        'intended_url': 'https://onboard.myyachthub.co.uk',
        'live': True,
        'primary_label': 'Open Onboard',
        'status_label': 'Live at onboard.myyachthub.co.uk',
        'domain_note': 'Standalone app target: <strong>onboard.myyachthub.co.uk</strong>. The Onboard app deployment is live and validated on this final subdomain.',
    },
    'world-map': {
        'label': 'World Map',
        'route': '/world-map/',
        'anchor': '#map-access',
        'intended_url': 'https://map.myyachthub.co.uk',
        'live': False,
        'primary_label': 'Open Map',
        'status_label': 'Map access coming online',
        'domain_note': 'Standalone map target: <strong>map.myyachthub.co.uk</strong>. This page avoids linking to that subdomain until the existing World Map deployment is live.',
    },
    'ecosystem': {
        'label': 'Digital Ecosystem',
        'route': '/ecosystem/',
        'anchor': '#ecosystem-areas',
        'intended_url': '/ecosystem/',
        'live': True,
        'primary_label': 'View Demo',
        'status_label': 'Demo available inside this private preview',
        'domain_note': 'The ecosystem demo is a gated MYH showcase. It links internally to core product wrappers and does not duplicate app functionality.',
    },
}

PRODUCTS = [
    {
        'key': 'manual',
        'tag': 'Manual Platform',
        'title': 'Structured vessel knowledge and builder-controlled information.',
        'description': 'Digital manuals, systems knowledge, equipment records and vessel-specific information in one controlled product layer.',
        'secondary_label': 'Find out more',
    },
    {
        'key': 'onboard',
        'tag': 'Onboard',
        'title': 'Maintenance and issue flow for real boats.',
        'description': 'Fault reporting, fix tracking, parts, costs, maintenance actions and onboard issue history for owners and crew.',
        'secondary_label': 'Find out more',
    },
    {
        'key': 'world-map',
        'tag': 'World Map',
        'title': 'Cruising intelligence and destination planning.',
        'description': 'Anchorages, contacts, recommendations, owner notes and destination planning around the existing map product.',
        'secondary_label': 'Find out more',
    },
    {
        'key': 'ecosystem',
        'tag': 'Digital Ecosystem',
        'title': 'A builder-branded owner world, shown as a polished demo.',
        'description': 'A pitch-ready demo connecting support, cruising, events, stories and community without forking the core apps.',
        'secondary_label': 'Explore areas',
    },
]

ACCESS_CONFIG_JS = '''window.MYH_GATEWAY_ACCESS = {
  hash: "__ACCESS_HASH__",
  storageKey: "myh_gateway_access_unlocked"
};
'''

ACCESS_GATE_JS = '''(function () {
  const config = window.MYH_GATEWAY_ACCESS || {};
  const storageKey = config.storageKey || 'myh_gateway_access_unlocked';
  const configuredHash = typeof config.hash === 'string' ? config.hash.trim().toLowerCase() : '';
  const hasCrypto = window.crypto && window.crypto.subtle && window.TextEncoder;

  function markUnlocked() {
    document.documentElement.classList.add('access-unlocked');
    document.documentElement.classList.remove('access-locked');
    try { window.sessionStorage.setItem(storageKey, 'true'); } catch (error) {}
  }

  function markLocked() {
    document.documentElement.classList.add('access-locked');
    document.documentElement.classList.remove('access-unlocked');
  }

  function isUnlocked() {
    try { return window.sessionStorage.getItem(storageKey) === 'true'; } catch (error) { return false; }
  }

  async function sha256(value) {
    const buffer = await window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
    return Array.from(new Uint8Array(buffer)).map((byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function setMessage(form, message, type) {
    const target = form.querySelector('[data-access-message]');
    if (!target) return;
    target.textContent = message;
    target.dataset.state = type || 'neutral';
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const input = form.querySelector('input[name="access-code"]');
    const value = input ? input.value.trim() : '';

    if (!configuredHash) {
      setMessage(form, 'Access-code validation is not configured in this build. Please request access.', 'error');
      return;
    }

    if (!hasCrypto) {
      setMessage(form, 'This browser cannot validate the access code securely. Please request access.', 'error');
      return;
    }

    const digest = await sha256(value);
    if (digest === configuredHash) {
      markUnlocked();
      setMessage(form, 'Access unlocked for this session.', 'success');
      document.querySelectorAll('[data-gated]').forEach((element) => element.removeAttribute('hidden'));
      document.querySelectorAll('[data-gated-route]').forEach((element) => element.removeAttribute('hidden'));
      document.querySelectorAll('[data-route-gate]').forEach((element) => element.setAttribute('hidden', ''));
      const firstGated = document.querySelector('[data-gated]');
      if (firstGated) firstGated.focus({ preventScroll: false });
    } else {
      markLocked();
      setMessage(form, 'That access code was not recognised. Please check it or request access.', 'error');
    }
  }

  function init() {
    if (isUnlocked()) markUnlocked(); else markLocked();

    document.querySelectorAll('[data-access-form]').forEach((form) => {
      form.addEventListener('submit', handleSubmit);
      if (!configuredHash) setMessage(form, 'Access-code validation has not been configured for this build. Request access to continue.', 'neutral');
    });

    document.querySelectorAll('[data-gated-route]').forEach((route) => {
      if (!isUnlocked()) {
        route.setAttribute('hidden', '');
        const gate = document.querySelector('[data-route-gate]');
        if (gate) gate.removeAttribute('hidden');
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
'''


def link_for(key):
    cfg = APP_LINKS[key]
    return cfg['intended_url'] if cfg['live'] and cfg['intended_url'].startswith('https://') else cfg['route']


def status_class(key):
    return 'is-live' if APP_LINKS[key]['live'] else 'is-coming-online'


def header(active="home"):
    def current(name):
        return ' aria-current="page"' if active == name else ''
    return f'''<!doctype html>
<html lang="en" class="access-locked">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MyYachtHub — Digital Products for Yachts</title>
  <meta name="description" content="MyYachtHub creates elegant, practical digital tools for yacht brands, owners, crew and managers." />
  <meta name="robots" content="noindex,nofollow,noarchive" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://www.myyachthub.co.uk/" />
  <meta property="og:title" content="MyYachtHub — Digital Products for Yachts" />
  <meta property="og:description" content="A calm public gateway to the Manual Platform, Onboard, World Map and the MYH digital ecosystem demo." />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Lato:wght@300;400;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/gateway.css" />
  <script src="/assets/app-links.js" defer></script>
  <script src="/assets/access-config.js" defer></script>
  <script src="/assets/access-gate.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="/" aria-label="MyYachtHub home">
      {LOGO}
      <span class="brand-text"><span class="brand-name">MY YACHT HUB</span><span class="brand-subtitle">Digital products for yachts</span></span>
    </a>
    <nav class="nav-links" aria-label="Primary navigation">
      <a href="/"{current('home')}>Home</a>
      <a href="/manual/"{current('manual')}>Manual Platform</a>
      <a href="/onboard/"{current('onboard')}>Onboard</a>
      <a href="/world-map/"{current('world-map')}>World Map</a>
      <a href="/ecosystem/"{current('ecosystem')}>Ecosystem</a>
      <a class="nav-cta" href="mailto:hello@myyachthub.com?subject=MYH%20access%20request">Request Access</a>
    </nav>
  </div>
</header>
<main id="main">'''


def access_panel(context="home"):
    prompt = "Enter your access code to reveal the available MYH products and demos." if context == "home" else "Enter your access code from the gateway to view this product/demo page."
    return f'''
<section class="section access-panel" data-route-gate{' hidden' if context != 'home' else ''}>
  <div class="container access-card">
    <div>
      <p class="eyebrow">Private preview</p>
      <h2>Access is by invitation for this stage.</h2>
      <p>{prompt} If you do not have a code, request access and MYH will confirm the right demo route for you.</p>
    </div>
    <form class="access-form" data-access-form>
      <label for="access-code-{context}">Access code</label>
      <div class="access-form-row">
        <input id="access-code-{context}" name="access-code" type="password" autocomplete="off" placeholder="Enter access code" />
        <button class="button primary" type="submit">Unlock</button>
      </div>
      <p class="access-message" data-access-message></p>
      <a class="request-link" href="mailto:hello@myyachthub.com?subject=MYH%20access%20request">Request access instead</a>
    </form>
  </div>
</section>'''


def footer():
    return '''</main>
<footer class="footer">
  <div class="container footer-grid">
    <p>© MyYachtHub. Digital products for yachts, owners, crew, managers and builders.</p>
    <div class="footer-links">
      <a href="/legacy/">Legacy site</a>
      <a href="/manual/">Manual Platform</a>
      <a href="mailto:hello@myyachthub.com">Contact</a>
    </div>
  </div>
</footer>
</body>
</html>
'''


def product_cards():
    cards = []
    for product in PRODUCTS:
        key = product['key']
        cfg = APP_LINKS[key]
        href = link_for(key)
        secondary = cfg['route'] + cfg['anchor']
        status = cfg['status_label']
        cards.append(f'''
      <article class="card product-card {status_class(key)}">
        <span class="tag">{product['tag']}</span>
        <h3>{product['title']}</h3>
        <p>{product['description']}</p>
        <span class="card-status">{status}</span>
        <div class="single-card-action">
          <a class="button primary" href="{href}">{cfg['primary_label']}</a>
          <a class="text-link" href="{secondary}">{product['secondary_label']}</a>
        </div>
      </article>''')
    return ''.join(cards)


home = header('home') + '''
<section class="hero">
  <div class="container hero-grid">
    <p class="eyebrow">MyYachtHub</p>
    <h1>Digital products that make yachts easier to use, manage and understand.</h1>
    <p class="hero-copy">From digital vessel manuals and onboard maintenance to cruising intelligence and branded owner ecosystems, MYH creates practical tools for yacht builders, owners, crew and managers.</p>
  </div>
</section>
''' + access_panel('home') + f'''
<section class="section gated-products" aria-labelledby="products-title" data-gated tabindex="-1">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Product portals</p>
      <h2 id="products-title">Choose the right MYH product.</h2>
      <p>Four controlled access points for the MYH product family. App destinations are centrally configured, and live product CTAs point to their validated standalone deployments.</p>
    </div>
    <div class="card-grid product-grid-2x2">
{product_cards()}
    </div>
  </div>
</section>
<section class="section" id="request-access">
  <div class="container split">
    <div class="section-head">
      <p class="eyebrow">Access</p>
      <h2>Built as separate products, connected by one public story.</h2>
    </div>
    <div class="notice">Interested in pilot access or a builder demo? Use the Request Access button to contact MYH. Onboard is now live at onboard.myyachthub.co.uk; the Manual Platform and World Map links remain controlled until their deployments are separately validated.</div>
  </div>
</section>
''' + footer()

manual = header('manual') + access_panel('manual') + f'''
<section class="product-hero" data-gated-route>
  <div class="container">
    <p class="eyebrow">Manual Platform</p>
    <h1>Structured vessel manuals and builder-controlled knowledge.</h1>
    <p class="product-summary">The Manual Platform is the MYH vessel knowledge layer for structured digital manuals, systems records, equipment references and builder-controlled vessel information.</p>
    <div class="actions">
      <a class="button primary" href="mailto:hello@myyachthub.com?subject=Manual%20Platform%20access%20request">Request access</a>
      <span class="button disabled" aria-disabled="true">{APP_LINKS['manual']['status_label']}</span>
    </div>
    <div class="info-strip">
      <div class="info-item"><strong>Vessel manuals</strong><p>Organise structured vessel documentation, systems guidance and handover knowledge.</p></div>
      <div class="info-item"><strong>Equipment records</strong><p>Keep equipment information, reference material and service context findable.</p></div>
      <div class="info-item"><strong>Builder control</strong><p>Support builder-approved information without merging other apps into the platform.</p></div>
    </div>
  </div>
</section>
<section class="section" id="platform-access" data-gated-route>
  <div class="container split">
    <div class="section-head"><p class="eyebrow">How it fits</p><h2>The knowledge base for vessel-specific information.</h2><p class="domain-note">{APP_LINKS['manual']['domain_note']}</p></div>
    <div class="feature-list">
      <div class="feature"><strong>Find out more.</strong> Use this page as the controlled access point for the Manual Platform.</div>
      <div class="feature"><strong>Open platform.</strong> Launch the existing platform only once its subdomain deployment is live.</div>
      <div class="feature"><strong>Request access.</strong> Contact MYH for a builder, owner or manager preview.</div>
    </div>
  </div>
</section>
''' + footer()

onboard = header('onboard') + access_panel('onboard') + f'''
<section class="product-hero" data-gated-route>
  <div class="container">
    <p class="eyebrow">Onboard</p>
    <h1>The living maintenance memory for your boat.</h1>
    <p class="product-summary">Onboard helps owners and crew report faults, track fixes, capture service history, record costs and manage practical maintenance without rebuilding the existing app.</p>
    <div class="actions">
      <a class="button primary" href="{link_for('onboard')}">Open Onboard</a>
      <a class="button" href="mailto:hello@myyachthub.com?subject=Onboard%20access%20request">Request access</a>
    </div>
    <div class="info-strip">
      <div class="info-item"><strong>Faults and fixes</strong><p>Log issues, urgency, photos and resolution flow.</p></div>
      <div class="info-item"><strong>Maintenance memory</strong><p>Keep service records, parts, spend and handovers together.</p></div>
      <div class="info-item"><strong>Standalone app</strong><p>Connected from MYH, not rebuilt or merged into the platform.</p></div>
    </div>
  </div>
</section>
<section class="section" id="app-access" data-gated-route>
  <div class="container split">
    <div class="section-head"><p class="eyebrow">What it supports</p><h2>Clear onboard operations for owners and crew.</h2><p class="domain-note">{APP_LINKS['onboard']['domain_note']}</p></div>
    <div class="feature-list">
      <div class="feature"><strong>Find out more.</strong> Use this page as the short access point for Onboard.</div>
      <div class="feature"><strong>Log in.</strong> Use the validated standalone Onboard app at onboard.myyachthub.co.uk.</div>
      <div class="feature"><strong>Request access.</strong> Contact MYH for app access, onboarding or beta invitations.</div>
    </div>
  </div>
</section>
''' + footer()

world_map = header('world-map') + access_panel('world-map') + f'''
<section class="product-hero" data-gated-route>
  <div class="container">
    <p class="eyebrow">World Map</p>
    <h1>Cruising intelligence, owner knowledge and destination planning.</h1>
    <p class="product-summary">The World Map gives sailors, owners and managers a premium route into anchorages, local contacts, recommendations, owner notes and destination planning using the existing map application.</p>
    <div class="actions">
      <a class="button primary" href="mailto:hello@myyachthub.com?subject=World%20Map%20access%20request">Request access</a>
      <span class="button disabled" aria-disabled="true">{APP_LINKS['world-map']['status_label']}</span>
    </div>
    <div class="info-strip">
      <div class="info-item"><strong>Anchorages</strong><p>Explore destination notes and practical local knowledge.</p></div>
      <div class="info-item"><strong>Contacts</strong><p>Surface trusted agents, mechanics and destination support.</p></div>
      <div class="info-item"><strong>Planning</strong><p>Build a clearer picture before cruising or passage planning.</p></div>
    </div>
  </div>
</section>
<section class="section" id="map-access" data-gated-route>
  <div class="container split">
    <div class="section-head"><p class="eyebrow">How to use it</p><h2>A focused access page for the existing map product.</h2><p class="domain-note">{APP_LINKS['world-map']['domain_note']}</p></div>
    <div class="feature-list">
      <div class="feature"><strong>Find out more.</strong> Use this page for a concise product introduction.</div>
      <div class="feature"><strong>Open map.</strong> Launch the standalone World Map app once its subdomain deployment is live.</div>
      <div class="feature"><strong>Request access.</strong> Contact MYH if access or admin setup is needed.</div>
    </div>
  </div>
</section>
''' + footer()

ecosystem = header('ecosystem') + access_panel('ecosystem') + '''
<section class="product-hero" data-gated-route>
  <div class="container">
    <p class="eyebrow">Digital Ecosystem Demo</p>
    <h1>A premium builder brand world for support, cruising and community.</h1>
    <p class="product-summary">This demo shows how a yacht builder could connect practical support, cruising intelligence, events, owner stories and brand updates into one calm digital experience.</p>
  </div>
</section>
<section class="section" id="ecosystem-areas" data-gated-route>
  <div class="container">
    <div class="ecosystem-grid">
      <article class="ecosystem-card" id="fix">
        <span class="number">01 / Fix</span>
        <h3>Support, troubleshooting and maintenance flow.</h3>
        <p>Fault reporting, troubleshooting, support requests, maintenance history, parts used, cost tracking and owner/builder support flow should be powered by Onboard rather than copied into a separate Fix app.</p>
        <div class="card-actions"><a class="button primary" href="/onboard/">View Fix wrapper</a><a class="button" href="/onboard/#app-access">Open Onboard status</a></div>
      </article>
      <article class="ecosystem-card" id="plan">
        <span class="number">02 / Plan</span>
        <h3>Cruising intelligence, trips and yacht admin.</h3>
        <p>World map intelligence sits beside rally planning, itineraries, budgets, pre-departure checklists, destination notes, useful contacts and trip admin. The map layer should be powered by World Map rather than duplicated.</p>
        <div class="card-actions"><a class="button primary" href="/world-map/">View Plan wrapper</a><a class="button" href="/world-map/#map-access">Open Map status</a></div>
      </article>
      <article class="ecosystem-card" id="connect">
        <span class="number">03 / Connect</span>
        <h3>Events, owner stories and brand communications.</h3>
        <p>Events, owner stories, brand communications, community, offers, service updates and optional owner-to-owner connection. This remains a polished demo area until a dedicated product scope is confirmed.</p>
        <span class="coming-soon">Coming soon</span>
      </article>
    </div>
  </div>
</section>
<section class="section" data-gated-route>
  <div class="container split">
    <div class="section-head"><p class="eyebrow">Demo principle</p><h2>Build once as MYH core, then wrap or theme for the ecosystem demo.</h2></div>
    <div class="notice">Fix points to Onboard and Plan points to World Map. The ecosystem should frame, theme, link to or demonstrate core products rather than forking them into duplicate applications.</div>
  </div>
</section>
''' + footer()

pages = {
    'index.html': home,
    'manual/index.html': manual,
    'onboard/index.html': onboard,
    'world-map/index.html': world_map,
    'ecosystem/index.html': ecosystem,
}

safe_app_links = {
    key: {
        'label': cfg['label'],
        'route': cfg['route'],
        'intendedUrl': cfg['intended_url'],
        'live': cfg['live'],
        'primaryHref': link_for(key),
        'statusLabel': cfg['status_label'],
    }
    for key, cfg in APP_LINKS.items()
}

assets = {
    'assets/access-config.js': ACCESS_CONFIG_JS.replace('__ACCESS_HASH__', os.environ.get('MYH_GATEWAY_ACCESS_SHA256', '').strip()),
    'assets/access-gate.js': ACCESS_GATE_JS,
    'assets/app-links.js': 'window.MYH_APP_LINKS = ' + json.dumps(safe_app_links, indent=2) + ';\n',
    'robots.txt': 'User-agent: *\nDisallow: /\n',
}

for rel, content in pages.items():
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

for rel, content in assets.items():
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print('Generated gateway pages:')
for rel in pages:
    print('-', rel)
print('Generated gate and link assets:')
for rel in assets:
    print('-', rel)

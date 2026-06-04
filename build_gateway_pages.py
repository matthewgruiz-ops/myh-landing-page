from pathlib import Path

ROOT = Path('/home/ubuntu/myh_repo_audit/myh-landing-page')

LOGO = '''<svg class="brand-mark" viewBox="0 0 48 56" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><path d="M24 4L39 15V41L24 52L9 41V15L24 4Z" stroke="#c9a96e" stroke-width="2"/><path d="M24 12V44" stroke="#f2ead6" stroke-width="1.6"/><path d="M15 29C18 24 21 21.5 24 21.5C27 21.5 30 24 33 29" stroke="#77c6c2" stroke-width="1.6" stroke-linecap="round"/><path d="M16 35C21 38 27 38 32 35" stroke="#c9a96e" stroke-width="1.6" stroke-linecap="round"/></svg>'''


def header(active="home"):
    def current(name):
        return ' aria-current="page"' if active == name else ''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MyYachtHub — Digital Products for Yachts</title>
  <meta name="description" content="MyYachtHub builds digital products that make yachts easier to use, manage and understand." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://www.myyachthub.co.uk/" />
  <meta property="og:title" content="MyYachtHub — Digital Products for Yachts" />
  <meta property="og:description" content="A calm public gateway to Onboard, Oyster World Map and the MYH digital ecosystem demo." />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Lato:wght@300;400;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/gateway.css" />
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
      <a href="/onboard/"{current('onboard')}>Onboard</a>
      <a href="/world-map/"{current('world-map')}>World Map</a>
      <a href="/ecosystem/"{current('ecosystem')}>Ecosystem</a>
      <a class="nav-cta" href="mailto:hello@myyachthub.com?subject=MYH%20access%20request">Request Access</a>
    </nav>
  </div>
</header>
<main id="main">'''


def footer():
    return '''</main>
<footer class="footer">
  <div class="container footer-grid">
    <p>© MyYachtHub. Digital products for yachts, owners, crew, managers and builders.</p>
    <div class="footer-links">
      <a href="/legacy/">Legacy site</a>
      <a href="https://app.myyachthub.co.uk">Vessel Knowledge Platform</a>
      <a href="mailto:hello@myyachthub.com">Contact</a>
    </div>
  </div>
</footer>
</body>
</html>
'''

home = header('home') + '''
<section class="hero">
  <div class="container hero-grid">
    <div>
      <p class="eyebrow">MyYachtHub</p>
      <h1>Digital products that make yachts easier to use, manage and understand.</h1>
      <p class="hero-copy">From onboard operations and fault reporting to cruising intelligence and branded owner ecosystems, MYH creates practical digital tools for yacht builders, owners, crew and managers.</p>
      <div class="actions">
        <a class="button primary" href="/onboard/">Explore Onboard</a>
        <a class="button" href="/world-map/">Open World Map</a>
        <a class="button ghost" href="/ecosystem/">View Ecosystem Demo</a>
      </div>
    </div>
    <aside class="gateway-panel" aria-label="MYH gateway overview">
      <div class="panel-inner">
        <span class="panel-kicker">One calm gateway</span>
        <ul class="panel-list">
          <li><strong>Fix</strong>Report faults, track fixes and keep maintenance moving.</li>
          <li><strong>Plan</strong>Use cruising intelligence, anchorages and owner knowledge.</li>
          <li><strong>Connect</strong>Bring stories, events and brand updates into one owner world.</li>
        </ul>
      </div>
    </aside>
  </div>
</section>
<section class="section" aria-labelledby="products-title">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Product portals</p>
      <h2 id="products-title">Choose the right MYH product.</h2>
      <p>Short, practical entry points for the existing MYH projects. Each card explains the product and sends visitors to the relevant product page. Standalone app subdomains are documented as deployment targets and should be enabled only once live.</p>
    </div>
    <div class="card-grid">
      <article class="card">
        <span class="tag">Onboard</span>
        <h3>Maintenance and issue flow for real boats.</h3>
        <p>Report faults, track fixes, record parts and costs, and keep onboard maintenance flowing clearly.</p>
        <div class="card-actions">
          <a class="button primary" href="/onboard/">Find out more</a>
          <a class="button" href="/onboard/#app-access">Log in / Open app</a>
          <a class="button" href="mailto:hello@myyachthub.com?subject=Onboard%20access%20request">Request access</a>
        </div>
      </article>
      <article class="card">
        <span class="tag">Oyster World Map</span>
        <h3>Cruising intelligence for premium yacht owners.</h3>
        <p>A premium cruising intelligence map for anchorages, local contacts, recommendations, owner knowledge and destination planning.</p>
        <div class="card-actions">
          <a class="button primary" href="/world-map/">Find out more</a>
          <a class="button" href="/world-map/#map-access">Open map</a>
          <a class="button" href="mailto:hello@myyachthub.com?subject=World%20Map%20access%20request">Request access</a>
        </div>
      </article>
      <article class="card">
        <span class="tag">Digital Ecosystem</span>
        <h3>A builder brand world, shown as a polished demo.</h3>
        <p>A demo of how a yacht builder’s digital brand world could bring support, cruising, events and community into one connected experience.</p>
        <div class="card-actions">
          <a class="button primary" href="/ecosystem/">View demo</a>
          <a class="button" href="/ecosystem/#connect">Find out more</a>
        </div>
      </article>
    </div>
  </div>
</section>
<section class="section" id="request-access">
  <div class="container split">
    <div class="section-head">
      <p class="eyebrow">Access</p>
      <h2>Built as separate products, connected by one public story.</h2>
    </div>
    <div class="notice">The Vessel Knowledge Platform remains separate at <strong>app.myyachthub.co.uk</strong>. Onboard and the World Map are linked as standalone products and are not merged into the platform app.</div>
  </div>
</section>
''' + footer()

onboard = header('onboard') + '''
<section class="product-hero">
  <div class="container">
    <p class="eyebrow">Onboard</p>
    <h1>The living maintenance memory for your boat.</h1>
    <p class="product-summary">Onboard helps owners and crew report faults, track fixes, capture service history, record costs and manage practical maintenance without rebuilding the existing app.</p>
    <div class="actions">
      <a class="button primary" href="#app-access">Open app</a>
      <a class="button" href="mailto:hello@myyachthub.com?subject=Onboard%20demo%20request">View demo</a>
      <a class="button" href="mailto:hello@myyachthub.com?subject=Onboard%20access%20request">Sign up / Request access</a>
    </div>
    <div class="info-strip">
      <div class="info-item"><strong>Faults and fixes</strong><p>Log issues, urgency, photos and resolution flow.</p></div>
      <div class="info-item"><strong>Maintenance memory</strong><p>Keep service records, parts, spend and handovers together.</p></div>
      <div class="info-item"><strong>Standalone app</strong><p>Connected from MYH, not rebuilt or merged into the platform.</p></div>
    </div>
  </div>
</section>
<section class="section" id="app-access">
  <div class="container split">
    <div class="section-head"><p class="eyebrow">What it supports</p><h2>Clear onboard operations for owners and crew.</h2><p class="domain-note">Standalone app target: <strong>onboard.myyachthub.co.uk</strong>. This page avoids linking to that subdomain until the existing Onboard app deployment is live.</p></div>
    <div class="feature-list">
      <div class="feature"><strong>Find out more.</strong> Use this page as the short access point for Onboard.</div>
      <div class="feature"><strong>Log in.</strong> Use the standalone Onboard app once its subdomain deployment is live.</div>
      <div class="feature"><strong>Request access.</strong> Contact MYH for app access, onboarding or beta invitations.</div>
    </div>
  </div>
</section>
''' + footer()

world_map = header('world-map') + '''
<section class="product-hero">
  <div class="container">
    <p class="eyebrow">Oyster World Map</p>
    <h1>Cruising intelligence, owner knowledge and destination planning.</h1>
    <p class="product-summary">The World Map gives sailors a premium route into anchorages, local contacts, recommendations, owner notes and destination planning using the existing map application.</p>
    <div class="actions">
      <a class="button primary" href="#map-access">Open map</a>
      <a class="button" href="mailto:hello@myyachthub.com?subject=World%20Map%20login%20or%20signup%20request">Log in / Sign up</a>
      <a class="button" href="mailto:hello@myyachthub.com?subject=World%20Map%20access%20request">Request access</a>
    </div>
    <div class="info-strip">
      <div class="info-item"><strong>Anchorages</strong><p>Explore destination notes and practical local knowledge.</p></div>
      <div class="info-item"><strong>Contacts</strong><p>Surface trusted agents, mechanics and destination support.</p></div>
      <div class="info-item"><strong>Planning</strong><p>Build a clearer picture before cruising or passage planning.</p></div>
    </div>
  </div>
</section>
<section class="section" id="map-access">
  <div class="container split">
    <div class="section-head"><p class="eyebrow">How to use it</p><h2>A focused access page for the existing map product.</h2><p class="domain-note">Standalone map target: <strong>map.myyachthub.co.uk</strong>. This page avoids linking to that subdomain until the existing World Map deployment is live.</p></div>
    <div class="feature-list">
      <div class="feature"><strong>Find out more.</strong> Use this page for a concise product introduction.</div>
      <div class="feature"><strong>Open map.</strong> Launch the standalone World Map app once its subdomain deployment is live.</div>
      <div class="feature"><strong>Request access.</strong> Contact MYH if access or admin setup is needed.</div>
    </div>
  </div>
</section>
''' + footer()

ecosystem = header('ecosystem') + '''
<section class="product-hero">
  <div class="container">
    <p class="eyebrow">Digital Ecosystem Demo</p>
    <h1>A premium builder brand world for support, cruising and community.</h1>
    <p class="product-summary">This demo shows how a yacht builder could connect practical support, cruising intelligence, events, owner stories and brand updates into one calm digital experience.</p>
  </div>
</section>
<section class="section" id="ecosystem-areas">
  <div class="container">
    <div class="ecosystem-grid">
      <article class="ecosystem-card" id="fix">
        <span class="number">01 / Fix</span>
        <h3>Support and issue tracking.</h3>
        <p>Support, fault reporting, troubleshooting, maintenance history and onboard issue tracking.</p>
        <div class="card-actions"><a class="button primary" href="/onboard/">Open Fix</a><a class="button" href="/onboard/#app-access">Open Onboard</a></div>
      </article>
      <article class="ecosystem-card" id="plan">
        <span class="number">02 / Plan</span>
        <h3>Cruising intelligence and owner knowledge.</h3>
        <p>Cruising intelligence, anchorages, contacts, recommendations, owner knowledge and destination planning.</p>
        <div class="card-actions"><a class="button primary" href="/world-map/">Open Plan</a><a class="button" href="/world-map/#map-access">Open Map</a></div>
      </article>
      <article class="ecosystem-card" id="connect">
        <span class="number">03 / Connect</span>
        <h3>Owner stories, events and brand updates.</h3>
        <p>Events, owner stories, community, experiences and brand updates for a premium yacht builder’s digital world.</p>
        <span class="coming-soon">Coming soon</span>
      </article>
    </div>
  </div>
</section>
<section class="section">
  <div class="container split">
    <div class="section-head"><p class="eyebrow">Demo principle</p><h2>Polished, practical and not cluttered.</h2></div>
    <div class="notice">Fix and Plan point to existing MYH products. Connect is intentionally shown as a finished Coming Soon area, not a broken or empty route.</div>
  </div>
</section>
''' + footer()

pages = {
    'index.html': home,
    'onboard/index.html': onboard,
    'world-map/index.html': world_map,
    'ecosystem/index.html': ecosystem,
}

for rel, content in pages.items():
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print('Generated gateway pages:')
for rel in pages:
    print('-', rel)

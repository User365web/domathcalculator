#!/usr/bin/env python3
"""Domathcalculator site generator.
1) Edit the CONFIG block  2) run:  python build.py  3) git add . && git commit && git push
It (re)creates every HTML page, sitemap.xml, robots.txt, ads.txt, manifest, favicon and 404.html."""
import os, json, datetime

# ============================ CONFIG ============================
SITE_NAME     = "Domathcalculator"
SITE_URL      = "https://YOUR-USERNAME.github.io/domathcalculator"   # no trailing slash. Custom domain: https://www.yourdomain.com
EMAIL         = "your-email@example.com"                              # shown on Contact / Privacy pages
ADSENSE_ID    = ""      # e.g. "ca-pub-1234567890123456"  (leave empty until AdSense approves you)
AD_SLOT       = ""      # optional ad unit id (digits). Empty = rely on AdSense Auto ads
GOOGLE_VERIFY = ""      # content value of Search Console "HTML tag" verification (optional)
CUSTOM_DOMAIN = ""      # e.g. "www.yourdomain.com" -> writes CNAME file
# ================================================================
TAGLINE = "Free Scientific Calculator, Unit Converter & Engineering Tools"
TODAY = datetime.date.today().isoformat()
ROOT = os.path.dirname(os.path.abspath(__file__))
NAV = [("index.html", "Calculator"), ("converter.html", "Unit Converter"), ("tools.html", "Engineering Tools"),
       ("guide.html", "Guide"), ("faq.html", "FAQ"), ("about.html", "About"), ("contact.html", "Contact")]


def ad():
    if not (ADSENSE_ID and AD_SLOT):
        return ""
    return ('<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="%s" data-ad-slot="%s" '
            'data-ad-format="auto" data-full-width-responsive="true"></ins>'
            '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>' % (ADSENSE_ID, AD_SLOT))


def page(slug, title, desc, body, scripts=(), ld=None, home=False, base="", noindex=False):
    url = SITE_URL + "/" + ("" if slug == "index.html" else slug)
    full = "%s – %s" % (SITE_NAME, TAGLINE) if home else "%s | %s" % (title, SITE_NAME)
    nav = "".join('<a href="%s%s"%s>%s</a>' % (base, h, ' class="on"' if h == slug else "", t) for h, t in NAV)
    head = ['<meta charset="utf-8">', '<meta name="viewport" content="width=device-width,initial-scale=1">',
            "<title>%s</title>" % full, '<meta name="description" content="%s">' % desc,
            '<link rel="canonical" href="%s">' % url,
            '<meta name="robots" content="%s">' % ("noindex,follow" if noindex else "index,follow,max-image-preview:large"),
            '<meta name="theme-color" content="#2563eb">',
            '<meta property="og:site_name" content="%s">' % SITE_NAME, '<meta property="og:type" content="website">',
            '<meta property="og:title" content="%s">' % full, '<meta property="og:description" content="%s">' % desc,
            '<meta property="og:url" content="%s">' % url, '<meta name="twitter:card" content="summary">',
            '<link rel="icon" href="%sfavicon.svg" type="image/svg+xml">' % base,
            '<link rel="manifest" href="%smanifest.webmanifest">' % base,
            '<link rel="stylesheet" href="%sassets/style.css">' % base]
    if GOOGLE_VERIFY:
        head.append('<meta name="google-site-verification" content="%s">' % GOOGLE_VERIFY)
    if ADSENSE_ID:
        head.append('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" crossorigin="anonymous"></script>' % ADSENSE_ID)
    if home:
        head.append('<script type="application/ld+json">%s</script>' % json.dumps(
            {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME,
             "alternateName": ["Do Math Calculator", "DoMathCalculator"], "url": SITE_URL + "/"}))
        head.append('<script type="application/ld+json">%s</script>' % json.dumps(
            {"@context": "https://schema.org", "@type": "WebApplication", "name": SITE_NAME, "url": SITE_URL + "/",
             "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "description": desc,
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}))
    if ld:
        head.append('<script type="application/ld+json">%s</script>' % json.dumps(ld))
    sc = "".join('<script src="%sassets/%s"></script>' % (base, s) for s in scripts)
    foot = ('<a href="%sprivacy.html">Privacy Policy</a><a href="%sterms.html">Terms of Use</a><a href="%scontact.html">Contact</a>'
            '<p>© %s %s. Results are for general use – always verify critical engineering calculations.</p>'
            % (base, base, base, TODAY[:4], SITE_NAME))
    return ('<!DOCTYPE html>\n<html lang="en"><head>%s</head><body><header><div class="w bar">'
            '<a class="logo" href="%sindex.html">Do<b>Math</b>Calculator</a><nav aria-label="Main">%s</nav></div></header>'
            '<main class="w">%s</main><footer><div class="w">%s</div></footer>%s</body></html>'
            % ("".join(head), base, nav, body, foot, sc))


def write(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
        fh.write(text)


# ------------------------------ content ------------------------------
FAQ = [
 ("Is Domathcalculator free?", "Yes. All calculators and converters are free to use, with no registration. The site is supported by advertising."),
 ("Does the calculator work in degrees and radians?", "Yes. Use the DEG/RAD key on the calculator to switch the angle mode for sin, cos, tan and their inverses."),
 ("How do I enter powers, roots and factorials?", "Use ^ for powers (2^8), sqrt( ) or cbrt( ) for roots, and ! for factorials (5!). Parentheses can be nested to any depth."),
 ("Can I type with my keyboard?", "Yes. Type expressions directly, press Enter to calculate and Escape to clear. On phones, use the on-screen keypad."),
 ("How accurate are the results?", "Calculations use standard double-precision floating point (about 15–16 significant digits). Results are displayed to 12 significant digits."),
 ("Is my data sent to a server?", "No. All calculations run in your browser. Calculator history is stored only in your own browser and can be cleared at any time."),
 ("Which units can I convert?", "Length, mass, area, volume, time, speed, pressure, energy, power, force, angle, temperature and digital data."),
 ("Can I use the results for professional design work?", "The tools are meant as a quick aid for study and everyday engineering. Always verify safety-critical results with approved methods and codes."),
 ("I found a mistake or have a feature request.", "Please use the Contact page. We read every message and fix reported errors quickly."),
]

HOME = """<h1>Scientific Calculator</h1>
<p class="lead">A fast, free online scientific calculator with trigonometry, logarithms, powers, roots, factorials, memory of your last answer and calculation history – plus a unit converter and engineering formulas.</p>
<div class="card" id="calc"></div><noscript><p>Please enable JavaScript to use the calculator.</p></noscript>
ADSLOT
<div class="cards"><a class="card" href="converter.html"><h2>Unit Converter</h2><p class="m">Length, mass, pressure, energy, temperature and more.</p></a>
<a class="card" href="tools.html"><h2>Engineering Tools</h2><p class="m">Ohm’s law, beam deflection, pipe flow, stress &amp; strain and more.</p></a>
<a class="card" href="guide.html"><h2>Guide</h2><p class="m">Syntax, functions and tips for faster calculations.</p></a></div>
<article class="card"><h2>An advanced calculator for students and engineers</h2>
<p>Domathcalculator was built for people who need dependable answers quickly: engineering and physics students, technicians, designers and anyone who works with numbers. The calculator supports sine, cosine and tangent with their inverses and hyperbolic forms, base-10 and natural logarithms, square and cube roots, exponentials, percentages, factorials, the constants π and e, and the previous answer (Ans).</p>
<p>Expressions are evaluated with a safe parser that respects operator precedence, nested parentheses and implicit multiplication such as <code>2π</code> or <code>(1+2)(3+4)</code>. A live preview shows the result as you type, and every calculation is saved to a local history so you can reuse it.</p>
<h2>Built for engineering work</h2>
<p>Switch to the <a href="converter.html">unit converter</a> to move between metric and imperial units, or open the <a href="tools.html">engineering tools</a> for ready-made formulas covering electrical circuits, structures, fluids and thermodynamics. Read the <a href="guide.html">guide</a> to learn every function and shortcut.</p></article>""" 

GUIDE = """<h1>User Guide</h1><p class="lead">Everything you need to get the most from Domathcalculator.</p>
<div class="card"><h2>1. Scientific calculator</h2>
<p>Type an expression or tap the keys, then press <b>=</b> (or Enter). A preview appears while you type. The result replaces the expression so you can keep calculating; <b>Ans</b> inserts the last answer.</p>
<div class="sc"><table><tr><th>Function</th><th>Meaning</th><th>Example</th></tr>
<tr><td>sin, cos, tan</td><td>Trigonometric functions (DEG or RAD mode)</td><td>sin(30) = 0.5</td></tr>
<tr><td>asin, acos, atan</td><td>Inverse trigonometric functions</td><td>atan(1) = 45</td></tr>
<tr><td>sinh, cosh, tanh</td><td>Hyperbolic functions</td><td>tanh(1)</td></tr>
<tr><td>log, ln</td><td>Base-10 and natural logarithm</td><td>log(1000) = 3</td></tr>
<tr><td>sqrt, cbrt</td><td>Square root, cube root</td><td>cbrt(27) = 3</td></tr>
<tr><td>^</td><td>Power</td><td>2^10 = 1024</td></tr>
<tr><td>!</td><td>Factorial (0–170)</td><td>5! = 120</td></tr>
<tr><td>%</td><td>Percent (divides by 100)</td><td>50% = 0.5</td></tr>
<tr><td>exp, abs, floor, ceil, round</td><td>Extra functions you can type</td><td>round(2.6) = 3</td></tr>
<tr><td>pi (π), e, ans</td><td>Constants and last answer</td><td>2pi = 6.2832</td></tr></table></div>
<p><b>Keyboard:</b> Enter = calculate, Escape = clear. Use <b>DEG/RAD</b> before trigonometric work – sin(90) is 1 in degrees but 0.8940 in radians.</p></div>
<div class="card"><h2>2. Unit converter</h2><p>Pick a category, type a value and choose the “from” and “to” units. The table underneath shows the value in every unit of that category at once. Temperature conversions handle °C, °F, K and °R correctly, including offsets.</p></div>
<div class="card"><h2>3. Engineering tools</h2><p>Each tool is a small formula calculator. Enter values in the units shown on the labels and press <b>Calculate</b>. Tools include Ohm’s law, series/parallel resistors, RC time constants, beam deflection, stress and strain, pipe flow, energy, the ideal gas law, a quadratic solver and a number-base converter.</p></div>
<div class="card"><h2>4. Tips</h2><ul><li>Use parentheses to make the order of operations explicit.</li><li>Floating-point results such as 0.1+0.2 may show tiny rounding differences; the display rounds to 12 significant digits.</li><li>Bookmark this site – it works offline-friendly and loads instantly on phones.</li></ul></div>
ADSLOT"""

ABOUT = """<h1>About Domathcalculator</h1>
<div class="card"><p>Domathcalculator is a free collection of calculation tools for students, engineers and curious people. Our aim is simple: a clean, fast and accurate scientific calculator, a reliable unit converter and practical engineering formulas in one place, with no sign-up and no clutter.</p>
<h2>Our principles</h2><ul><li><b>Accuracy first</b> – formulas and conversion factors use standard published values (SI, NIST).</li><li><b>Privacy by design</b> – calculations happen in your browser; we never receive your numbers.</li><li><b>Speed</b> – lightweight pages that work well on slow connections and small screens.</li><li><b>Transparency</b> – the site is supported by advertising so it can stay free. See our <a href="privacy.html">Privacy Policy</a>.</li></ul>
<h2>Get in touch</h2><p>Found an error or want a new tool added? Visit the <a href="contact.html">Contact page</a>.</p></div>"""

CONTACT = """<h1>Contact Us</h1><p class="lead">Questions, corrections or ideas for new tools? We would love to hear from you.</p>
<div class="card"><form id="cf"><div class="g"><label>Your name<input id="n" required></label><label>Your email<input id="e" type="email" required></label></div>
<label style="margin-top:12px">Message<textarea id="m" rows="6" required></textarea></label><button class="btn" type="submit">Send message</button></form>
<p class="m">The button opens your email app with the message ready to send to <b>EMAIL</b>. You can also write to us directly at that address.</p></div>
<script>document.getElementById('cf').onsubmit=function(x){x.preventDefault();var b='From: '+n.value+' ('+e.value+')\\n\\n'+m.value;location.href='mailto:EMAIL?subject='+encodeURIComponent('Domathcalculator message')+'&body='+encodeURIComponent(b)}</script>"""

PRIVACY = """<h1>Privacy Policy</h1><p class="m">Last updated: DATE</p><div class="card">
<h2>Information we collect</h2><p>Domathcalculator does not require an account and does not collect personal information through its calculators. Values you enter are processed locally in your browser and are not sent to our servers. Calculator history is stored in your browser’s local storage on your device and can be deleted with the “Clear history” button or by clearing your browser data.</p>
<h2>Cookies and advertising</h2><p>We use Google AdSense to display ads. Third-party vendors, including Google, use cookies to serve ads based on a user’s previous visits to this and other websites. Google’s use of advertising cookies enables it and its partners to serve ads based on your visit to this site and/or other sites on the Internet. You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info" rel="noopener">aboutads.info</a>. Learn more about how Google uses data at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">policies.google.com/technologies/partner-sites</a>.</p>
<h2>Analytics and logs</h2><p>Our hosting provider may keep standard server logs (IP address, browser type, pages requested). We may use privacy-respecting analytics to understand overall traffic.</p>
<h2>Children</h2><p>This site is not directed at children under 13 and we do not knowingly collect their personal data.</p>
<h2>Your rights</h2><p>Depending on where you live (for example the EEA, UK or California) you may have rights to access, correct or delete personal data. Since we do not store personal data from the calculators, there is generally nothing to delete, but you can contact us at EMAIL with any request.</p>
<h2>Changes</h2><p>We may update this policy; the date above shows the latest revision.</p></div>"""

TERMS = """<h1>Terms of Use</h1><p class="m">Last updated: DATE</p><div class="card">
<p>By using Domathcalculator you agree to these terms.</p>
<h2>Use of the tools</h2><p>The calculators, converters and formulas are provided free of charge for general informational and educational use.</p>
<h2>No warranty</h2><p>We work hard to keep results accurate, but the site is provided “as is” without warranties of any kind. Do not rely solely on these tools for safety-critical, structural, medical, legal or financial decisions. Always verify results using approved methods, standards and a qualified professional.</p>
<h2>Limitation of liability</h2><p>Domathcalculator and its owner are not liable for any loss or damage arising from the use of, or inability to use, the site.</p>
<h2>Intellectual property</h2><p>The design, text and code of this site are protected. You may link to any page freely.</p>
<h2>Contact</h2><p>Questions about these terms: EMAIL.</p></div>"""


def fill(t):
    return t.replace("EMAIL", EMAIL).replace("DATE", TODAY)


faq_html = "<h1>Frequently Asked Questions</h1>" + '<div class="card">' + "".join(
    "<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in FAQ) + "</div>"
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

pages = [
 ("index.html", "Scientific Calculator", "Free online scientific calculator with trigonometry, logarithms, powers and factorials, plus a unit converter and engineering tools.",
  HOME.replace("ADSLOT", ad()), ["calc.js"], None, True, "1.0"),
 ("converter.html", "Unit Converter", "Free engineering unit converter: length, mass, area, volume, pressure, energy, power, force, temperature, speed, angle and data.",
  '<h1>Unit Converter</h1><p class="lead">Convert between metric and imperial units instantly.</p><div class="card" id="conv"></div>' + ad() +
  '<div class="card"><h2>Common engineering conversions</h2><p>1 inch = 25.4 mm · 1 psi = 6.895 kPa · 1 bar = 100 kPa · 1 hp = 745.7 W · 1 kWh = 3.6 MJ · 1 kgf = 9.80665 N · 0 °C = 273.15 K. Need more functions? Try the <a href="index.html">scientific calculator</a>.</p></div>',
  ["eng.js"], None, False, "0.9"),
 ("tools.html", "Engineering Tools", "Engineering formula calculators: Ohm's law, resistors, RC filter, beam deflection, stress and strain, pipe flow, ideal gas law, quadratic solver and base converter.",
  '<h1>Engineering Tools</h1><p class="lead">Quick formula calculators for electrical, mechanical, fluid and thermal problems.</p><div id="eng"></div>' + ad(),
  ["eng.js"], None, False, "0.9"),
 ("guide.html", "User Guide", "How to use the scientific calculator, unit converter and engineering tools: functions, syntax, keyboard shortcuts and tips.",
  GUIDE.replace("ADSLOT", ad()), [], None, False, "0.8"),
 ("faq.html", "FAQ", "Answers to common questions about the Domathcalculator scientific calculator, unit converter and engineering tools.",
  faq_html, [], faq_ld, False, "0.7"),
 ("about.html", "About", "About Domathcalculator – free scientific calculator, unit converter and engineering tools built for students and engineers.",
  ABOUT, [], None, False, "0.5"),
 ("contact.html", "Contact", "Contact Domathcalculator to report an error, ask a question or suggest a new calculator.",
  fill(CONTACT), [], None, False, "0.5"),
 ("privacy.html", "Privacy Policy", "Privacy policy of Domathcalculator including cookie and Google AdSense information.",
  fill(PRIVACY), [], None, False, "0.3"),
 ("terms.html", "Terms of Use", "Terms of use for Domathcalculator.", fill(TERMS), [], None, False, "0.3"),
]

for slug, title, desc, body, scripts, ld, home, prio in pages:
    write(slug, page(slug, title, desc, body, scripts, ld, home))

write("404.html", page("404.html", "Page not found", "Page not found.",
      '<h1>Page not found</h1><p>The page you requested does not exist. <a href="%s/index.html">Go to the calculator</a>.</p>' % SITE_URL,
      base=SITE_URL + "/", noindex=True))

urls = "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>\n"
               % (SITE_URL, "" if p[0] == "index.html" else p[0], TODAY, p[7]) for p in pages)
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)
write("manifest.webmanifest", json.dumps({"name": SITE_NAME, "short_name": SITE_NAME, "start_url": "./index.html", "display": "standalone",
      "background_color": "#ffffff", "theme_color": "#2563eb", "icons": [{"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=2))
write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2563eb"/>'
      '<text x="32" y="46" font-size="40" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-weight="700">π</text></svg>')
write(".nojekyll", "")
if ADSENSE_ID:
    write("ads.txt", "google.com, pub-%s, DIRECT, f08c47fec0942fa0\n" % ADSENSE_ID.replace("ca-pub-", ""))
elif os.path.exists(os.path.join(ROOT, "ads.txt")):
    os.remove(os.path.join(ROOT, "ads.txt"))
if CUSTOM_DOMAIN:
    write("CNAME", CUSTOM_DOMAIN + "\n")
print("Built %d pages + sitemap.xml, robots.txt for %s" % (len(pages) + 1, SITE_URL))

# Domathcalculator

Static website: scientific calculator, unit converter, engineering tools, plus Guide, FAQ, About, Contact, Privacy and Terms pages.
No frameworks, no build tools needed to *run* it. Python 3 is only needed to regenerate pages (`build.py`).

## 1. Run locally
    cd domathcalculator
    python3 -m http.server 8000
Open http://localhost:8000 (or just double-click index.html).

## 2. Configure (once)
Open `build.py`, edit the CONFIG block at the top:
- SITE_URL  -> your final address, no trailing slash (e.g. https://www.domathcalculator.xubi.org)
- EMAIL     -> your contact email
- GOOGLE_VERIFY -> Search Console HTML-tag code (optional)
- ADSENSE_ID / AD_SLOT -> fill in after AdSense approves you
- CUSTOM_DOMAIN -> e.g. www.yourdomain.com (creates CNAME)
Then run:  `python3 build.py`  (rewrites all pages, sitemap.xml, robots.txt, ads.txt).

## 3. Publish with Git + GitHub Pages
1. Create an empty public repo on GitHub (name it `domathcalculator`, or `YOUR-USERNAME.github.io` to serve from the domain root).
2. In this folder:
       git init
       git add .
       git commit -m "Initial release"
       git branch -M main
       git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git
       git push -u origin main
3. GitHub repo -> Settings -> Pages -> Source: "Deploy from a branch" -> Branch: main, folder: / (root) -> Save.
4. After ~1 minute the site is live. Update later with: python3 build.py && git add . && git commit -m "update" && git push

## 4. Get found on Google
1. https://search.google.com/search-console -> Add property (URL prefix = your SITE_URL) -> verify (HTML tag: paste the code in GOOGLE_VERIFY, rebuild, push).
2. Sitemaps -> submit `sitemap.xml`. Then use URL Inspection -> Request indexing for the home page.
3. The site name "Domathcalculator" comes from <title>, og:site_name and WebSite structured data (already included).
   No Jekyll/README page is served because index.html exists and .nojekyll is present.
4. robots.txt is only honored at the ROOT of a host. For a project page (user.github.io/repo/) it is not at the root,
   so use a repo named YOUR-USERNAME.github.io or, better, a custom domain.

## 5. AdSense
- AdSense generally requires a domain you own (not a free github.io subdomain). Buy a domain, set CUSTOM_DOMAIN + SITE_URL,
  add DNS records per GitHub docs, enable "Enforce HTTPS".
- Apply with the site live, with Privacy Policy, About and Contact pages (included). Add more original content/tools over time.
- After approval set ADSENSE_ID (and optionally AD_SLOT), run build.py, push. ads.txt is generated automatically.
- Visitors in the EEA/UK need a consent banner (Google-certified CMP) - enable one in AdSense "Privacy & messaging".


## Custom domain
The production domain for this site is `https://www.domathcalculator.xubi.org`.
The `CNAME` file contains `www.domathcalculator.xubi.org`. The build configuration
uses this domain for canonical URLs, Open Graph metadata, the sitemap and robots.txt.
After pushing changes, confirm that GitHub Pages has the custom domain configured
and that your DNS provider points the `www` host to the GitHub Pages target.

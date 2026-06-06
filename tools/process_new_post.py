"""
sajjadur-rahman.com — New Blog Post Processor
==============================================
Applies all standard SEO and CTA fixes to a new blog post.

Usage:
  python3 process_new_post.py \
    --file    blog-my-new-post.html \
    --url     https://sajjadur-rahman.com/blog-my-new-post.html \
    --date    2026-06-10 \
    --related blog-connected-post.html \
    --label   "Connected Post Title →"

What it does:
  1. Adds <link rel="canonical"> tag
  2. Adds Google Analytics script (G-TFCD42G87F)
  3. Adds Article JSON-LD schema
  4. Adds .post-nav CSS rule (if missing)
  5. Adds post-nav HTML — "All Posts" + connected post button
     (inserts before <!-- Author bio --> or <div class="article-bio">)
  6. Prints a verification report
"""

import re, os, sys, argparse, shutil

# ── Google Analytics block ────────────────────────────────────────────────────
GA_BLOCK = """  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-TFCD42G87F"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag("js", new Date());
    gtag("config", "G-TFCD42G87F");
  </script>"""

# ── post-nav CSS ──────────────────────────────────────────────────────────────
POST_NAV_CSS = """
    /* ══════════════════════════════════
       POST NAVIGATION
       ══════════════════════════════════ */
    .post-nav {
      margin-top: 48px;
      padding-top: 28px;
      border-top: 1px solid var(--gold-pale);
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }"""


def process(file_path, canonical_url, date, related_file, related_label, output_path=None):
    with open(file_path) as f:
        html = f.read()

    orig_lines = html.count('\n')
    changes = []

    # 1. CANONICAL
    if 'canonical' not in html:
        m = re.search(r'(<title>[^<]*</title>)', html)
        if m:
            html = html.replace(
                m.group(1),
                m.group(1) + '\n  <link rel="canonical" href="' + canonical_url + '"/>',
                1
            )
            changes.append('canonical tag added')
    else:
        changes.append('canonical already present')

    # 2. GA SCRIPT
    if 'G-TFCD42G87F' not in html:
        canon_tag = '<link rel="canonical" href="' + canonical_url + '"/>'
        if canon_tag in html:
            html = html.replace(canon_tag, canon_tag + '\n' + GA_BLOCK, 1)
            changes.append('GA script added')
    else:
        changes.append('GA already present')

    # 3. ARTICLE SCHEMA
    if 'application/ld+json' not in html:
        tm = re.search(r'<title>([^<]*)</title>', html)
        headline = tm.group(1).split('\u2014')[0].strip().replace('"', '&quot;') if tm else ''
        dm = re.search(r'<meta name="description" content="([^"]*)"', html)
        desc = dm.group(1)[:200].replace('"', '&quot;') if dm else ''

        schema = (
            '  <script type="application/ld+json">\n'
            '  {\n'
            '    "@context": "https://schema.org",\n'
            '    "@type": "Article",\n'
            '    "headline": "' + headline + '",\n'
            '    "description": "' + desc + '",\n'
            '    "url": "' + canonical_url + '",\n'
            '    "datePublished": "' + date + '",\n'
            '    "dateModified": "' + date + '",\n'
            '    "author": {\n'
            '      "@type": "Person",\n'
            '      "name": "Sajjadur Rahman",\n'
            '      "url": "https://sajjadur-rahman.com/about.html"\n'
            '    },\n'
            '    "publisher": {\n'
            '      "@type": "Person",\n'
            '      "name": "Sajjadur Rahman",\n'
            '      "url": "https://sajjadur-rahman.com"\n'
            '    }\n'
            '  }\n'
            '  </script>'
        )
        html = html.replace('</head>', schema + '\n</head>', 1)
        changes.append('Article schema added')
    else:
        changes.append('schema already present')

    # 4. POST-NAV CSS
    if '.post-nav' not in html:
        html = html.replace('</style>\n</head>', POST_NAV_CSS + '\n  </style>\n</head>', 1)
        changes.append('post-nav CSS added')
    else:
        changes.append('post-nav CSS already present')

    # 5. POST-NAV HTML
    if 'post-nav' not in html or html.count('post-nav') < 2:
        nav_html = (
            '\n          <div class="post-nav">\n'
            '            <a href="blog.html" class="btn btn-outline btn-arrow">All Posts</a>\n'
            '            <a href="' + related_file + '" class="btn btn-gold">' + related_label + '</a>\n'
            '          </div>\n\n'
        )
        if '<!-- Author bio -->' in html:
            html = html.replace('<!-- Author bio -->', nav_html + '          <!-- Author bio -->', 1)
            changes.append('post-nav HTML added (before author bio comment)')
        elif 'class="article-bio"' in html:
            html = html.replace('<div class="article-bio">', nav_html + '          <div class="article-bio">', 1)
            changes.append('post-nav HTML added (before article-bio div)')
        else:
            changes.append('WARNING: post-nav HTML could not be inserted — no author bio marker found')
    else:
        changes.append('post-nav HTML already present')

    # Write output
    out = output_path or file_path
    with open(out, 'w') as f:
        f.write(html)

    # Report
    new_lines = html.count('\n')
    print(f'\n{"="*60}')
    print(f'Processed: {os.path.basename(file_path)}')
    print(f'Output:    {out}')
    print(f'Lines:     {orig_lines} -> {new_lines} (+{new_lines - orig_lines})')
    print(f'{"="*60}')
    for c in changes:
        icon = '\u2705' if 'WARNING' not in c else '\u26a0\ufe0f'
        print(f'  {icon}  {c}')
    print()

    # Final verification
    print('Verification:')
    print(f'  canonical:   {"OK" if "canonical" in html else "MISSING"}')
    print(f'  GA script:   {"OK" if "G-TFCD42G87F" in html else "MISSING"}')
    print(f'  schema:      {"OK" if "application/ld+json" in html else "MISSING"}')
    print(f'  post-nav:    {"OK" if "post-nav" in html else "MISSING"}')
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a new blog post')
    parser.add_argument('--file',    required=True,  help='Path to blog post HTML file')
    parser.add_argument('--url',     required=True,  help='Full canonical URL of the post')
    parser.add_argument('--date',    required=True,  help='Publish date YYYY-MM-DD')
    parser.add_argument('--related', required=True,  help='Filename of connected post')
    parser.add_argument('--label',   required=True,  help='Button label for connected post')
    parser.add_argument('--output',  default=None,   help='Output path (default: overwrite input)')
    args = parser.parse_args()

    process(
        file_path     = args.file,
        canonical_url = args.url,
        date          = args.date,
        related_file  = args.related,
        related_label = args.label,
        output_path   = args.output,
    )

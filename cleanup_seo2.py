#!/usr/bin/env python3
"""Clean SEO spam from Turner site markdown files - pass 2."""
import re
import os

BASE = "/Users/primeclaw/.openclaw/workspace/turner/jmwturner-site/content"
FILES = [
    "about/news.md",
    "about/your-story.md",
    "discovery/christopher.md",
    "discovery/copies.md",
    "discovery/forensic.md",
    "discovery/fraud.md",
    "discovery/hand-c.md",
    "discovery/ifar.md",
    "discovery/institutional.md",
    "discovery/legal.md",
    "discovery/rubens.md",
]

CLEAN_FOOTER = """
 [JMW Turner](/painting/)
 Rescue
 [Turner Society](http://www.turnersociety.org.uk/) [Tate Gallery](http://www.tate.org.uk/home/default.htm) [National Gallery](http://www.nationalgallery.org.uk/) [London](/discovery/national-gallery/)
 [Courtauld Institute of Art](http://www.courtauld.ac.uk/sub_index/location/location.html)
  [IFAR International Foundation for Art Research](http://www.ifar.org/) [NGC](http://national.gallery.ca/)
 [National Gallery Canada](http://national.gallery.ca/) [Frick Collection](http://www.frick.org/html/info1f.htm)
  [Yale Center for British Art](http://www.yale.edu/ycba/) [The Getty](http://www.getty.edu/) Biro
 Forensic Studies [CCI](http://www.cci-icc.gc.ca/)
 [Canadian Conservation Institute](http://www.cci-icc.gc.ca/html/)
"""

# Match the footer starting with "[JMW Turner](/painting/)\n Rescue\n [Turner Society]"
# This specific combination only appears in the footer area
FOOTER_PATTERN = re.compile(
    r'\n+\s*\[JMW Turner\]\(/painting/\)\s*\n\s*Rescue\s*\n\s*\[Turner Society\]\(http://www\.turnersociety\.org\.uk/\).*$',
    re.DOTALL
)

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_len = len(content)
    
    # Find ALL matches - we want the LAST one
    matches = list(FOOTER_PATTERN.finditer(content))
    if matches:
        last = matches[-1]
        content = content[:last.start()] + CLEAN_FOOTER
        print(f"  {filepath}: found {len(matches)} footer(s), kept last")
    else:
        print(f"  {filepath}: NO FOOTER MATCH FOUND")
    
    # Clean up trailing whitespace
    content = content.rstrip('\n') + '\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    new_len = len(content)
    removed = original_len - new_len
    print(f"    {original_len} -> {new_len} (removed {removed} chars)")
    return removed

total_removed = 0
for fpath in FILES:
    full_path = os.path.join(BASE, fpath)
    if os.path.exists(full_path):
        total_removed += clean_file(full_path)
    else:
        print(f"  NOT FOUND: {full_path}")

print(f"\nTotal removed: {total_removed} chars across {len(FILES)} files")

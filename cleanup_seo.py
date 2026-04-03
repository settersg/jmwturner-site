#!/usr/bin/env python3
"""Clean SEO spam from Turner site markdown files."""
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

# Search engine links block - always starts with [H](http://www.hotbot.com/)
# and ends with [AOL](http://aolsearch.aol.com/index.adp)
SEARCH_ENGINE_PATTERN = re.compile(
    r'\n+\s*\[H\]\(http://www\.hotbot\.com/\).*?\[AOL\]\(http://aolsearch\.aol\.com/index\.adp\)\s*\n*',
    re.DOTALL
)

# "On site:" navigation link dump block
# Starts with "On site:" and ends before the search engine block
# Contains massive lists of internal links like [JMWT](/about/turner/), etc.
ONSITE_PATTERN = re.compile(
    r'\n+On site:\s*\n.*?(?=\n+\s*\[H\]\(http://www\.hotbot\.com/\))',
    re.DOTALL
)

# Keyword-stuffed "Source:" block (seen in fraud.md, rubens.md)
# Pattern: "Source:" followed by lines of keyword-stuffed text ending with [Carr Manet] or similar
SOURCE_BLOCK_PATTERN = re.compile(
    r'\n+Source:\s*\n.*?(?=\n+\s*\[JMW Turner\]\(/painting/\)\s*\n+\s*Rescue\s*\n)',
    re.DOTALL
)

# The "Stanford Penn State Rockefeller UPA J. Paul Getty Trust Publications" junk line
# followed by University College London link - this is in the "On site:" dump area
STANFORD_PATTERN = re.compile(
    r'\n+Stanford\s*\n+Penn State Rockefeller UPA J\. Paul Getty Trust\s*\n+Publications\s*\n+\[University College London UCL\]\(http://www\.ucl\.ac\.uk/\)\s*\n*',
    re.DOTALL
)

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_len = len(content)
    
    # 1. Remove search engine links block
    content = SEARCH_ENGINE_PATTERN.sub('\n', content)
    
    # 2. Remove "On site:" link dump
    content = ONSITE_PATTERN.sub('\n', content)
    
    # 3. Remove "Source:" keyword-stuffed blocks
    content = SOURCE_BLOCK_PATTERN.sub('\n', content)
    
    # 4. Remove Stanford/Publications junk
    content = STANFORD_PATTERN.sub('\n', content)
    
    # 5. Clean up excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # 6. Remove trailing whitespace on lines
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    content = '\n'.join(lines)
    
    # 7. Ensure file ends with single newline
    content = content.rstrip('\n') + '\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    new_len = len(content)
    removed = original_len - new_len
    print(f"  {filepath}: {original_len} -> {new_len} (removed {removed} chars)")
    return removed

total_removed = 0
for fpath in FILES:
    full_path = os.path.join(BASE, fpath)
    if os.path.exists(full_path):
        total_removed += clean_file(full_path)
    else:
        print(f"  NOT FOUND: {full_path}")

print(f"\nTotal removed: {total_removed} chars across {len(FILES)} files")

"""
Convert the official National Registry of Exonerations CSV into the
JSON format used by /registry.html.

HOW TO USE
==========

1. Download the official NRE CSV.
   - Visit https://exonerationregistry.org/ in a normal browser
   - Click "Download Data" (the site is behind Cloudflare, so you need
     a real browser session — automated downloads are blocked)
   - Save the file as `exoneration-data.csv` somewhere on your machine

2. Place the CSV at the path specified below (or edit CSV_PATH).
   Default: /home/z/my-project/work/false-accusations-awareness/exoneration-data.csv

3. Run this script:
       python3 scripts/convert_nre_csv.py

4. The script overwrites:
       assets/data/registry-data.json
   with the full ~3,600-case dataset.

5. Commit and push to GitHub Pages — the live /registry.html page will
   immediately serve the full dataset.

NRE CSV SCHEMA (as of 2024)
============================
The NRE CSV has these columns (your file may have slight variations;
this script is tolerant to column-name changes):

  Last Name, First Name, Age, Race, Sex, State, County, Tags, Crime,
  Date of Crime, Date of Exoneration, FY (Fiscal Year), NumExonerations,
  Years, Sentence, Conviction, Date of Crime (revised),
  Contributing Factors (tags), Death Row, Sex Offender Registry,
  Pardon, DNA, Perpetrator Indicted, Perpetrator Convicted,
  MWID (Mistaken Witness ID), FC (False Confession), P/FA (Perjury/False Accusation),
  OM (Official Misconduct), ILD (Inadequate Legal Defense), II (Inadequate Investigation),
  FBE (False or Misleading Forensic Evidence), ...

This script maps the NRE's contributing-factor codes to readable labels:
  MWID -> Eyewitness misidentification
  FC   -> False confession
  P/FA -> Perjured testimony / False accusation
  OM   -> Official misconduct
  ILD  -> Ineffective assistance
  FBE  -> Flawed forensics
  DNA  -> DNA
"""

import csv
import json
import os
import sys
from collections import OrderedDict

# Paths (relative to repo root, so script can run from anywhere)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(REPO_ROOT, "exoneration-data.csv")
OUT_PATH = os.path.join(REPO_ROOT, "assets", "data", "registry-data.json")

# US State abbreviations (for normalization)
US_STATES = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA',
    'Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA',
    'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA',
    'Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD',
    'Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS',
    'Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH',
    'New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC',
    'North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA',
    'Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN',
    'Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA',
    'West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY','District of Columbia':'DC',
    'Federal':'FED',
}

# NRE contributing-factor tag code -> human-readable label
FACTOR_MAP = OrderedDict([
    ('MWID',  'Eyewitness misidentification'),
    ('FC',    'False confession'),
    ('P/FA',  'Perjured testimony / False accusation'),
    ('OM',    'Official misconduct'),
    ('ILD',   'Ineffective assistance'),
    ('FBE',   'Flawed forensics'),
    ('DNA',   'DNA'),
    ('II',    'Inadequate investigation'),
])

def normalize_state(s):
    s = (s or '').strip()
    if not s:
        return ''
    if s in US_STATES:
        return US_STATES[s]
    if len(s) == 2 and s.upper() == s:
        return s
    return s

def safe_int(s, default=0):
    try:
        return int(float(str(s).strip() or 0))
    except (ValueError, TypeError):
        return default

def parse_year(date_str):
    """Extract a 4-digit year from a date string."""
    if not date_str:
        return None
    s = str(date_str).strip()
    import datetime, re
    for fmt in ('%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y', '%B %d, %Y', '%Y'):
        try:
            return datetime.datetime.strptime(s.split()[0], fmt).year
        except (ValueError, TypeError):
            continue
    m = re.search(r'\b(19\d{2}|20\d{2})\b', s)
    return int(m.group(1)) if m else None

def main():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: NRE CSV not found at: {CSV_PATH}")
        print()
        print("To use this script:")
        print("  1. Open https://exonerationregistry.org/ in a browser")
        print("  2. Click 'Download Data' to get the CSV")
        print(f"  3. Save it as: {CSV_PATH}")
        print("  4. Re-run this script")
        sys.exit(1)

    print(f"Reading NRE CSV: {CSV_PATH}")
    with open(CSV_PATH, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Parsed {len(rows)} rows. Converting to registry format...")

    # Normalize column names (strip whitespace)
    if rows:
        rows = [{k.strip() if k else k: v for k, v in row.items()} for row in rows]

    out_cases = []
    for i, row in enumerate(rows, 1):
        # Build name
        last = (row.get('Last Name') or '').strip()
        first = (row.get('First Name') or '').strip()
        name = (first + ' ' + last).strip() or f"Unknown #{i}"

        # Years
        year_ex = parse_year(row.get('Date of Exoneration') or '')
        years_served = safe_int(row.get('Years'), 0)
        year_crime = parse_year(row.get('Date of Crime') or '')
        year_convicted = year_crime or (year_ex - years_served if year_ex else 0)

        # State
        state = normalize_state(row.get('State'))

        # Country (NRE is US-centric; non-US entries are in 'Tags' or country field)
        country = 'US'
        if not state:
            tags = (row.get('Tags') or '').lower()
            for cc, name_lower in [
                ('UK','united kingdom'), ('CA','canada'), ('AU','australia'),
                ('FR','france'), ('JP','japan'), ('IE','ireland'),
                ('NZ','new zealand'), ('IT','italy'), ('SE','sweden'),
            ]:
                if name_lower in tags:
                    country = cc
                    break

        # Crime
        crime = (row.get('Crime') or 'Unknown').strip()

        # Contributing factors
        factors = []
        for code, label in FACTOR_MAP.items():
            val = row.get(code)
            if val and str(val).strip() in ('1', 'True', 'true', 'Y', 'y', 'Yes', 'yes'):
                factors.append(label)
        cf_text = row.get('Contributing Factors') or ''
        if cf_text:
            for part in [p.strip() for p in cf_text.replace(';', ',').split(',') if p.strip()]:
                if part not in factors and part.lower() not in [f.lower() for f in factors]:
                    factors.append(part)
        if not factors:
            factors = ['Unknown']

        # Source — NRE case detail page URL pattern
        source = f"https://exonerationregistry.org/?search={name.replace(' ', '+')}"

        # Summary
        summary = (row.get('Tags') or '').strip() or f"Exonerated {year_ex or ''} after {years_served} years; {crime}."

        entry = {
            "id": i,
            "name": name,
            "year_convicted": year_convicted,
            "year_exonerated": year_ex or 0,
            "years_served": years_served,
            "country": country,
            "state": state,
            "crime": crime,
            "category": crime.split(';')[0].split(',')[0].strip(),
            "contributing_factors": factors,
            "source": source,
            "summary": summary[:200],
        }
        out_cases.append(entry)

    print(f"Converted {len(out_cases)} cases.")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump({
            "schema_version": 1,
            "source": f"Official National Registry of Exonerations dataset ({len(out_cases)} cases), sourced from https://exonerationregistry.org/. Converted via scripts/convert_nre_csv.py.",
            "total_cases": len(out_cases),
            "cases": out_cases,
        }, f, ensure_ascii=False, indent=2)

    print(f"Wrote {OUT_PATH}")
    print(f"File size: {os.path.getsize(OUT_PATH):,} bytes")
    print()
    print(f"Done. The /registry.html page will now serve all {len(out_cases)} cases.")
    print("Commit and push to GitHub to update the live site.")

if __name__ == "__main__":
    main()

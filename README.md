# False Accusations Awareness

An open educational archive documenting **high-profile, publicly verified cases** of people who were **falsely accused of crimes** — across multiple countries and decades. Each case has a clear later outcome: an acquittal, a quashed conviction, a DNA exoneration, a pardon, an admission of fabrication, or an official finding of innocence.

**Purpose.** Help society remain cautious. False accusations destroy lives and also make it harder for genuine victims to be believed. Due process, evidence, and restraint matter — especially when public outrage is loudest.

---

## Live site

Once GitHub Pages is enabled, the site is published at:

**https://desurfofficial-ship-it.github.io/false-accusations-awareness/**

To enable: repository **Settings → Pages → Source: Deploy from a branch → Branch: `main` → Folder: `/ (root)` → Save.** (Pages is enabled in this commit.)

To run locally: clone the repo and open `index.html` in any browser. No build step is required — the site is plain HTML/CSS with self-hosted SVG illustrations.

---

## Featured cases (21 total, 10 countries)

### United States
- **Duke Lacrosse (2006)** — Crystal Mangum admitted in 2024 that she fabricated the allegations.
- **Brian Banks (2002)** — Accuser Wanetta Gibson admitted she lied; conviction overturned 2012.
- **Central Park Five / Exonerated Five (1989)** — Vacated after DNA + Matias Reyes' confession.
- **Scottsboro Boys (1931)** — Historic false accusations later overturned/pardoned.
- **Steven Avery – First Conviction (1985)** — Exonerated by DNA after 18 years.

### United Kingdom
- **Birmingham Six (1974)** — Convictions quashed 1991; 16 years wrongful imprisonment.
- **Guildford Four (1974)** — Convictions quashed 1989; 15 years wrongful imprisonment.
- **Stefan Kiszko (1975)** — Exonerated by DNA in 1992; real killer convicted 2007.
- **Barry George (2001)** — Acquitted at retrial 2008 in the Jill Dando case.
- **UK Post Office / Horizon Scandal (1999–2015)** — Mass miscarriage; 700+ wrongful prosecutions.

### Canada
- **David Milgaard (1969)** — Exonerated by DNA in 1997 after 23 years in prison.
- **Steven Truscott (1959)** — Acquitted in 2007, 48 years after conviction at age 14.
- **Guy Paul Morin (1984)** — Exonerated by DNA in 1996; real killer identified 2020.

### Australia
- **Lindy Chamberlain (1980)** — "A dingo took my baby"; conviction overturned 1988.

### Japan
- **Iwao Hakamada (1964)** — World's longest-serving death row inmate; formally acquitted 2024.

### Sweden
- **Sture Bergwall / "Thomas Quick" (1994)** — All 8 murder convictions quashed by 2013.

### France
- **Patrick Dils (1986)** — Exonerated in 2002; real killer Francis Heaulme convicted 2007.
- **Omar Raddad (1991)** — Partial pardon 1996; case remains controversial.

### Ireland
- **Sister Nora Wall (1995)** — Conviction quashed 1999 after four days.

### New Zealand
- **Arthur Allan Thomas (1970)** — Royal pardon 1979; police evidence-planting exposed.

### Italy
- **Amanda Knox & Raffaele Sollecito (2007)** — Fully exonerated by Italy's highest court in 2015.

---

## Design

Editorial light theme with magazine-style typography: **Fraunces** (serif headlines) + **Inter** (UI and body). Each case has a country-coded SVG illustration (generated, copyright-safe). Country filter chips allow visitors to view cases by jurisdiction. Built with semantic HTML, sticky topbar, scroll-reveal animations, and full mobile responsiveness.

## Project structure

```
false-accusations-awareness/
├── index.html              # Main page
├── styles.css              # Editorial redesign stylesheet
├── assets/
│   └── img/                # 21 self-hosted SVG illustrations (one per case)
└── README.md
```

## Contributing

Pull requests adding well-documented cases with clear later outcomes are welcome. Please:

1. Cite a clear, public, later outcome (acquittal, exoneration, pardon, admission of fabrication, or official finding of innocence).
2. Link to a primary source (court judgment, government record, or major investigative reporting).
3. Keep the tone factual — no speculation, no advocacy, no naming of private individuals who have not been publicly identified in connection with the case.
4. Add a generated SVG illustration under `assets/img/<case-slug>.svg`.

## Editorial standard

Every case on this site meets at least one of these criteria:

- A court has formally acquitted, exonerated, or quashed the conviction.
- DNA or other forensic evidence has excluded the accused and identified the real perpetrator.
- The accuser has publicly admitted the accusation was fabricated.
- A pardon or official apology has been issued.
- An official inquiry has found the conviction to be a miscarriage of justice.

Sources are public records, court judgments, and major investigative reporting. Each card links to the public record for full context. This site does not claim completeness — only to illustrate the human cost of false accusations and the need for caution.

## License

Educational and awareness purposes. Case facts are drawn from public records and are not subject to copyright; the editorial design and original illustrations are released for educational reuse with attribution.

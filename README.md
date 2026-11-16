# UK Sponsor Checker

A fast, self-contained web app to check whether a UK employer is a licensed visa sponsor,
what licence rating they hold (A or B), and which visa routes they can sponsor.

It searches the official **Home Office Register of licensed sponsors (Worker and Temporary
Worker)** — the same dataset the commercial "sponsorship checker" tools use.

## How it works

1. `process.py` reads the official gov.uk register CSV and compacts it into a small
   `data/sponsors.json` (a route lookup table + grouped records, ~7 MB instead of ~17 MB).
2. `index.html` is a single static page that loads `sponsors.json` and does all search
   client-side — no server, no API keys. It groups a company's multiple register rows into
   one card showing its best rating and all its routes.

## Updating the data

The register is republished on gov.uk (roughly daily). To refresh:

1. Find the current CSV link on the publication page:
   https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers
2. Download it, then regenerate the JSON:

```bash
python process.py path/to/register.csv data/sponsors.json
```

Update the `register_date` string inside `process.py` to match the new file's date.

## Running locally

Because the page fetches `sponsors.json`, open it through a local server (not `file://`):

```bash
python -m http.server 8000
```

Then visit http://localhost:8000.

## Data notes

- The register lists **legal entity names**, which often differ from a brand/trading name.
  A "no match" doesn't always mean an employer can't sponsor — try the parent company.
- **A rating** = licence in good standing and actively able to sponsor.
  **B rating** = licence downgraded; the sponsor is on a time-limited action plan.
- Always confirm against the live gov.uk register before relying on it.

## Source & licence

Data: Home Office, Register of licensed sponsors: workers. Contains public sector
information licensed under the Open Government Licence v3.0.

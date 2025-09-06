
# Support Triage Repository

This repo organizes and analyzes incoming support emails for faster triage.

## What's inside
- `data/emails.csv` – raw dataset you provided
- `src/triage_cli.py` – Python CLI to categorize, prioritize, and summarize
- `.github/ISSUE_TEMPLATE/` – issue templates for incidents and questions
- `.github/workflows/ci.yml` – GitHub Actions to auto-generate triage report on every push
- `requirements.txt` – Python dependencies

## Quickstart
```bash
# 1) Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the triage CLI
python src/triage_cli.py --csv data/emails.csv --out-dir outputs

# 4) Inspect outputs
ls outputs/
# -> emails_enriched.csv, summary_by_category_priority.csv, summary_by_sender.csv, report.md
```

## Suggested GitHub workflow
1. Create a new GitHub repo (empty).
2. Initialize locally and push:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: support triage scaffolding"
   git branch -M main
   git remote add origin <YOUR_REPO_URL>
   git push -u origin main
   ```
3. (Optional) Auto-create labels via GitHub CLI:
   ```bash
   gh label create P1 -c "#b60205" -d "Sev 1: urgent/critical"
   gh label create P2 -c "#d93f0b" -d "Sev 2: high"
   gh label create P3 -c "#0e8a16" -d "Sev 3: normal"
   gh label create incident -c "#ee0701"
   gh label create question -c "#1d76db"
   ```

## Categories & Priority
Heuristics are defined in `src/triage_cli.py`:
- **Categories**: `login_issue`, `billing_error`, `downtime`, `integration`, `verification`, `other`
- **Priorities**: `P1` (urgent words like "urgent/critical/immediate"), `P2` (core-impact keywords), `P3` (default)

You can adjust regex patterns in the `ISSUE_MAP` and `PRIORITY_HINTS` dictionaries.

## License
MIT

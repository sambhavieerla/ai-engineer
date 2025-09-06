
# Contributing

Thanks for taking the time to contribute!

## Setup
- Create a virtualenv and install requirements.
- Run `python src/triage_cli.py --csv data/emails.csv --out-dir outputs` to generate reports.

## Style
- Keep regex patterns simple and commented.
- Prefer small, focused pull requests.

## CI
- CI runs the triage CLI and uploads `outputs/` as an artifact.

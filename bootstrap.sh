
#!/usr/bin/env bash
set -euo pipefail
git init
git add .
git commit -m "Initial commit: support triage scaffolding"
git branch -M main
echo "Now run: git remote add origin <YOUR_REPO_URL> && git push -u origin main"


import argparse
import pandas as pd
from pathlib import Path
import re
from datetime import datetime

ISSUE_MAP = {
    "login_issue": [
        r"unable to log in",
        r"system access blocked",
        r"cannot reset my password",
        r"reset link doesn’t seem to work",
        r"reset link doesn't seem to work",
    ],
    "billing_error": [
        r"charged twice",
        r"billing error",
        r"refund",
        r"pricing tiers",
        r"pricing breakdown",
    ],
    "downtime": [
        r"servers are down",
        r"system is completely inaccessible",
        r"downtime",
    ],
    "integration": [
        r"third-party apis",
        r"crm integration",
        r"integration with api",
    ],
    "verification": [
        r"verifying my account",
        r"verification email never arrived",
        r"account verification",
    ]
}

PRIORITY_HINTS = {
    "P1": [r"urgent", r"critical", r"immediate", r"highly critical", r"completely inaccessible"],
    "P2": [r"unable to log in", r"servers are down", r"charged twice"],
    "P3": [r"pricing", r"integration", r"refund", r"verification"]
}

def categorize(text: str):
    text_l = text.lower()
    categories = set()
    for cat, patterns in ISSUE_MAP.items():
        for pat in patterns:
            if re.search(pat, text_l):
                categories.add(cat)
                break
    if not categories:
        categories.add("other")
    return sorted(categories)

def priority(text: str):
    t = text.lower()
    for p, patterns in PRIORITY_HINTS.items():
        for pat in patterns:
            if re.search(pat, t):
                return p
    return "P3"

def main():
    ap = argparse.ArgumentParser(description="Support triage helper")
    ap.add_argument("--csv", type=Path, default=Path("data/emails.csv"))
    ap.add_argument("--out-dir", type=Path, default=Path("outputs"))
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # Combine subject+body for classification context
    df["text"] = (df["subject"].fillna("") + " " + df["body"].fillna("")).str.strip()
    df["categories"] = df["text"].apply(lambda x: ",".join(categorize(x)))
    df["priority"] = df["text"].apply(priority)

    # Normalize date
    df["sent_date"] = pd.to_datetime(df["sent_date"])

    # Output enriched CSV
    enriched_path = args.out_dir / "emails_enriched.csv"
    df.to_csv(enriched_path, index=False)

    # Summary by category & priority
    summary = df.groupby(["categories","priority"]).size().reset_index(name="count")
    summary_path = args.out_dir / "summary_by_category_priority.csv"
    summary.to_csv(summary_path, index=False)

    # Sender-level summary
    sender = df.groupby(["sender","categories","priority"]).size().reset_index(name="count")
    sender_path = args.out_dir / "summary_by_sender.csv"
    sender.to_csv(sender_path, index=False)

    # Markdown report
    md = ["# Support Triage Report", f"_Generated: {datetime.utcnow().isoformat()}Z_",""]
    md.append("## Totals by Category & Priority")
    for _, row in summary.sort_values(["priority","count"], ascending=[True, False]).iterrows():
        md.append(f"- **{row['categories']}** / {row['priority']}: {row['count']}")
    md.append("")
    md.append("## Notable Duplicates (same body text)")
    dupes = df.groupby("body").size().reset_index(name="count")
    dupes = dupes[dupes["count"] > 1].sort_values("count", ascending=False)
    if dupes.empty:
        md.append("- None found.")
    else:
        for _, r in dupes.iterrows():
            snippet = r['body'][:120].replace("\n"," ")
            md.append(f"- {r['count']}× — "{snippet}"")
    md_content = "\n".join(md)

    with open(args.out_dir / "report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Enriched CSV: {enriched_path}")
    print(f"Summary by category & priority: {summary_path}")
    print(f"Sender summary: {sender_path}")
    print(f"Markdown report: {args.out_dir / 'report.md'}")

if __name__ == "__main__":
    main()

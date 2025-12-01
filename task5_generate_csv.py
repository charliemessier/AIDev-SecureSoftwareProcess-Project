import pandas as pd

# Input CSVs from previous tasks
TASK1_CSV = "task1_all_pull_request.csv"
TASK3_CSV = "task3_pr_task_type.csv"

# Output CSV for Task-5
OUTPUT_CSV = "task5_pr_security_summary.csv"


SECURITY_KEYWORDS = [
    "race",
    "racy",
    "buffer",
    "overflow",
    "stack",
    "integer",
    "signedness",
    "underflow",
    "improper",
    "unauthenticated",
    "gain access",
    "permission",
    "cross site",
    "css",
    "xss",
    "denial service",
    "dos",
    "crash",
    "deadlock",
    "injection",
    "request forgery",
    "csrf",
    "xsrf",
    "forged",
    "security",
    "vulnerability",
    "vulnerable",
    "exploit",
    "attack",
    "bypass",
    "backdoor",
    "threat",
    "expose",
    "breach",
    "violate",
    "fatal",
    "blacklist",
    "overrun",
    "insecure",
]


def has_security_keyword(text: str) -> int:
    if not isinstance(text, str):
        return 0

    lower_text = text.lower()
    for kw in SECURITY_KEYWORDS:
        if kw in lower_text:
            return 1
    return 0


def main():
    print("Loading Task-1 CSV (pull requests)…")
    pr_df = pd.read_csv(TASK1_CSV)

    print("Loading Task-3 CSV (task types)…")
    task_df = pd.read_csv(TASK3_CSV)

    # Sanity check for required columns
    for col in ["ID", "AGENTNAME", "TITLE", "BODYSTRING"]:
        if col not in pr_df.columns:
            raise SystemExit(f"ERROR: Column {col} not found in {TASK1_CSV}")

    for col in ["PRID", "PRTYPE", "CONFIDENCE"]:
        if col not in task_df.columns:
            raise SystemExit(f"ERROR: Column {col} not found in {TASK3_CSV}")

    print("Merging Task-1 and Task-3 data on pull request ID…")
    merged = pd.merge(
        pr_df,
        task_df,
        left_on="ID",
        right_on="PRID",
        how="inner",
    )

    # Build a text field combining title + body for keyword search
    print("Computing SECURITY flag based on title/body and keyword list…")
    combined_text = (
        merged["TITLE"].fillna("").astype(str)
        + " "
        + merged["BODYSTRING"].fillna("").astype(str)
    )

    merged["SECURITY"] = combined_text.apply(has_security_keyword)

    # Build final output dataframe
    out_df = pd.DataFrame(
        {
            "ID": merged["ID"],
            "AGENT": merged["AGENTNAME"],
            "TYPE": merged["PRTYPE"],
            "CONFIDENCE": merged["CONFIDENCE"],
            "SECURITY": merged["SECURITY"],
        }
    )

    print(f"Writing Task-5 output CSV to {OUTPUT_CSV} …")
    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print("Task-5 complete!")
    print(f"CSV saved as: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

import pandas as pd
import string

# HuggingFace path to the pr_commit_details table
HF_PATH = "hf://datasets/hao-li/AIDev/pr_commit_details.parquet"

# Output CSV path for Task-4
OUTPUT_CSV = "task4_pr_commit_details.csv"


def clean_patch(text: str) -> str:
    if pd.isna(text):
        return ""
    text = str(text)
    allowed = set(string.printable)
    return "".join(ch for ch in text if ch in allowed)


def main():
    print("Loading pr_commit_details data directly from HuggingFace…")
    df = pd.read_parquet(HF_PATH)

    # Mapping from original columns -> required Task-4 headers
    column_map = {
        "pr_id": "PRID",
        "sha": "PRSHA",
        "message": "PRCOMMITMESSAGE",
        "filename": "PRFILE",
        "status": "PRSTATUS",
        "additions": "PRADDS",
        "deletions": "PRDELSS",
        "changes": "PRCHANGECOUNT",
        "patch": "PRDIFF",
    }

    # Ensure all required columns are present
    missing = [col for col in column_map if col not in df.columns]
    if missing:
        raise SystemExit(f"ERROR: Missing columns in pr_commit_details.parquet: {missing}")

    # Select relevant columns
    df_out = df[list(column_map.keys())].copy()

    # Clean the 'patch' column to remove special characters
    print("Cleaning PRDIFF (patch) column to remove special characters…")
    df_out["patch"] = df_out["patch"].apply(clean_patch)

    # Rename columns to required Task-4 headers
    df_out = df_out.rename(columns=column_map)

    print(f"Writing CSV to {OUTPUT_CSV} …")
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print("Task-4 complete!")
    print(f"CSV saved as: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

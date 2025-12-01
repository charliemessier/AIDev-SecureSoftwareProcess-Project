import pandas as pd

# HuggingFace path to the dataset
HF_PATH = "hf://datasets/hao-li/AIDev/all_pull_request.parquet"

# Output CSV path
OUTPUT_CSV = "task1_all_pull_request.csv"

def main():
    print("Loading data directly from HuggingFace…")
    df = pd.read_parquet(HF_PATH)

    # Required mapping for Task-1
    column_map = {
        "title": "TITLE",
        "id": "ID",
        "agent": "AGENTNAME",
        "body": "BODYSTRING",
        "repo_id": "REPOID",
        "repo_url": "REPOURL",
    }

    # Reduce the dataset to only needed columns
    missing = [c for c in column_map if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    df_out = df[list(column_map.keys())].rename(columns=column_map)

    print(f"Writing CSV to {OUTPUT_CSV} …")
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print("Task-1 complete!")
    print(f"CSV saved as: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

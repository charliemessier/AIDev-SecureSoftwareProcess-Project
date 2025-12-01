import pandas as pd

# HuggingFace path to the pr_task_type table
HF_PATH = "hf://datasets/hao-li/AIDev/pr_task_type.parquet"

# Output CSV path for Task-3
OUTPUT_CSV = "task3_pr_task_type.csv"


def main():
    print("Loading pr_task_type data directly from HuggingFace…")
    df = pd.read_parquet(HF_PATH)

    # Mapping from original columns -> required Task-3 headers
    column_map = {
        "id": "PRID",
        "title": "PRTITLE",
        "reason": "PRREASON",
        "type": "PRTYPE",
        "confidence": "CONFIDENCE",
    }

    # Ensure all required columns are present
    missing = [col for col in column_map if col not in df.columns]
    if missing:
        raise SystemExit(f"ERROR: Missing columns in pr_task_type.parquet: {missing}")

    # Select and rename columns
    df_out = df[list(column_map.keys())].rename(columns=column_map)

    print(f"Writing CSV to {OUTPUT_CSV} …")
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print("Task-3 complete!")
    print(f"CSV saved as: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

import pandas as pd

# HuggingFace path to the all_repository table
HF_PATH = "hf://datasets/hao-li/AIDev/all_repository.parquet"

# Output CSV path for Task-2
OUTPUT_CSV = "task2_all_repository.csv"


def main():
    print("Loading all_repository data directly from HuggingFace…")
    df = pd.read_parquet(HF_PATH)

    # Mapping from original columns -> required Task-2 headers
    column_map = {
        "id": "REPOID",
        "language": "LANG",
        "stars": "STARS",
        "url": "REPOURL",
    }

    # Make sure all required columns are present
    missing = [col for col in column_map if col not in df.columns]
    if missing:
        raise SystemExit(f"ERROR: Missing columns in all_repository.parquet: {missing}")

    # Select and rename
    df_out = df[list(column_map.keys())].rename(columns=column_map)

    print(f"Writing CSV to {OUTPUT_CSV} …")
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print("Task-2 complete!")
    print(f"CSV saved as: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

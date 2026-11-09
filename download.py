import io
import os
import zipfile
import pandas as pd
import requests
from tqdm import tqdm

# 1. Load your CSV file
csv_file = "me2026.csv"  # Apne CSV ka naam yahan daal lena
df = pd.read_csv(csv_file).dropna(subset=["Institute Code"])

# Ensure institute code is formatted cleanly as a 4-digit string with leading zeros
df["Formatted_Code"] = df["Institute Code"].astype(int).astype(str).str.zfill(4)

# Define the rounds we want to look for dynamically in the CSV columns
round_columns = ["CAP-I", "CAP-II", "CAP-III", "CAP-IV"]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 2. Loop through each potential round column present in the CSV
for col_name in round_columns:
    if col_name not in df.columns:
        print(f"Column '{col_name}' not found in CSV. Skipping this round.")
        continue

    # Filter rows where the specific round link actually exists
    valid_df = df.dropna(subset=[col_name])

    if len(valid_df) == 0:
        print(f"No links found for {col_name}. Skipping.")
        continue

    zip_filename = f"all_colleges_{col_name.lower()}.zip"

    # --- CHECK IF ZIP ALREADY EXISTS ---
    if os.path.exists(zip_filename):
        print(f"\n[Found Existing Archive]: '{zip_filename}' already exists on disk.")
        user_choice = (
            input(
                f"Do '{zip_filename}'You want to download and replace this zip file? (y/n): "
            )
            .strip()
            .lower()
        )

        if user_choice != "y":
            print(f"Skipping {col_name} download. Using existing archive.")
            continue
        else:
            print(f"Re-downloading and overwriting '{zip_filename}'...")

    print(f"\nStarting download for {col_name}: Found {len(valid_df)} college links.")

    success_count = 0
    fail_count = 0

    # 3. Create a zip archive for the round with a progress bar
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for _, row in tqdm(
            valid_df.iterrows(),
            total=len(valid_df),
            desc=f"Downloading {col_name} PDFs",
        ):
            code = row["Formatted_Code"]
            inst_name = str(row.get("Institute Name", "College")).strip()
            url = row[col_name]
            pdf_name = f"{code}_{col_name}.pdf"

            try:
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    zipf.writestr(pdf_name, response.content)
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                fail_count += 1

    print(f"--- {col_name} Complete! ---")
    print(f"Successfully zipped: {success_count} PDFs into '{zip_filename}'")
    if fail_count > 0:
        print(f"Failed / Skipped: {fail_count} PDFs")

print("\nAll available round archives processed successfully!")

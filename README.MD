# MHTCET Allotment Scraper

An automated Python script designed to programmatically fetch, ingest, and bundle official MHT-CET (Maharashtra Common Entrance Test) institutional allotment and cutoff PDFs across multiple Centralized Admission Process (CAP) rounds into clean, compressed zip archives.

---

## Key Features

* **CSV-Driven Ingestion:** Reads institute codes and target PDF URLs dynamically from a structured CSV source (e.g., `me2026.csv`).
* **Normalized Formatting:** Automatically cleans and pads institute codes into clean 4-digit strings with leading zeros (`.str.zfill(4)`) for reliable file organization.
* **Multi-Round Support:** Scans and processes multiple admission rounds dynamically (`CAP-I`, `CAP-II`, `CAP-III`, `CAP-IV`).
* **Smart Archive Management:** Checks for existing round archives on disk and prompts the user whether to reuse or overwrite them, preventing redundant downloads.
* **Resilient Execution & Tracking:** Built-in exception handling skips dead links or network drops without crashing the pipeline, paired with real-time `tqdm` progress bars.

---

##  Tech Stack & Prerequisites

* **Python 3.8+**
* `pandas` (for tabular data handling)
* `requests` (for HTTP streaming and downloading)
* `tqdm` (for interactive terminal progress visualization)

---

## Installation

1. **Clone the repository:**
   
   git clone [https://github.com/malharkshirsagar/mhtcet-allotment-scraper.git](https://github.com/malharkshirsagar/mhtcet-allotment-scraper.git)
   cd mhtcet-allotment-scraper

2. **Install the required dependencies:**

    pip install -r requirements.txt
---
## Usage

Place your source CSV file (configured with columns like Institute Code, Institute Name, CAP-I, CAP-II, etc.) in the project root directory and name it me2026.csv (or update the filename variable inside the script).

Run the automation script:

  python main.py

The script will check for existing round archives, prompt for confirmation if found, and output compressed zip bundles (e.g., all_colleges_cap-i.zip) containing all successfully fetched college PDFs.
---
## Output Structure
For each valid CAP round column present in your source CSV, the script generates:

Compressed Archive (all_colleges_cap-x.zip) containing individual PDFs named by format: {InstituteCode}_{RoundName}.pdf (e.g., 0011_CAP-I.pdf).

Console Summary Logs detailing successful downloads versus failed/skipped link counts.
---
## License

This project is open-source and available under the terms of the MIT License.

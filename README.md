# LinkedIn Company Finder (Google API Integration)

This Python-based tool automates the process of finding official LinkedIn Company Page URLs using the **Google Custom Search JSON API**. It was specifically designed to handle bulk data enrichment for business intelligence tasks while operating within API limits.

## 🚀 Key Features
* **Automated Enrichment**: Seamlessly converts a list of company names in Excel into validated LinkedIn URLs.
* **API Key Rotation**: Implements a smart failover system that automatically switches to the next available Google API key when daily quotas (100 requests/key) are reached.
* **OneDrive Integration**: Configured to work within a synchronized corporate environment (Alten DSO Tools directory structure).
* **Robust Data Handling**: Uses `pandas` for Excel manipulation and prevents duplicate processing by skipping already enriched rows.

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Libraries:** `pandas`, `requests`, `openpyxl`
* **IDE:** Optimized for Spyder.
* **Search Strategy:** Google Custom Search API with targeted dorking (`"Company Name" linkedin company`).

## 📁 Project Structure
* `LK-company-finder.py`: The core automation script.
* `LK-company-finder.xlsx`: Input file (Column A: Company Names | Column B: LinkedIn URLs).
* `api_keys.xlsx`: Credential storage for multiple API keys and Search Engine IDs (`cx`).

## ⚙️ How it Works



1. **Targeting**: The script locates the Excel file within the local OneDrive mirror.
2. **Quota Management**: It loads a pool of API keys to bypass the standard daily limitation of free-tier searches.
3. **Validation**: For each search, it parses the JSON response to ensure the extracted link follows the `linkedin.com/company/` pattern.
4. **Auto-Save**: Results are saved incrementally to prevent data loss in case of network interruption.

## 📝 Setup & Usage
1. **API Credentials**: Generate your API keys via the [Google Cloud Console](https://console.cloud.google.com/).
2. **Search Engine ID**: Create a Programmable Search Engine [here](https://programmablesearchengine.google.com/) and set it to search the entire web.
3. **Configuration**: 
    * Add your keys to `api_keys.xlsx`.
    * Place your company list in `LK-company-finder.xlsx`.
4. **Run**: Execute the script via Spyder or any terminal.

---
*Disclaimer: This project was developed as a professional utility to streamline sales operations and data cleaning workflows.*

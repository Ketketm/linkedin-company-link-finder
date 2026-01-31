import pandas as pd
import os
import requests
import time

# --- ONEDRIVE PATH CONFIGURATION ---
# We use the USERPROFILE environment variable to ensure it works on any Windows session
base_path = os.path.join(os.environ['USERPROFILE'], 'Alten', 'DSO Tools', 'Python', 'Import template')
file_companies = os.path.join(base_path, 'LK-company-finder.xlsx')
file_keys = os.path.join(base_path, 'api_keys.xlsx')

def get_linkedin_url(company_name, api_key, search_engine_id):
    """Perform search via Google Custom Search JSON API"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': f'"{company_name}" linkedin company',
        'key': api_key,
        'cx': search_engine_id,
        'num': 1  # We only need the top result
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        if items:
            link = items[0].get('link')
            # Check if the result is actually a LinkedIn company page
            if "linkedin.com/company/" in link:
                return link
        return "Not Found"
    elif response.status_code == 429:
        # 429 status code means the daily quota for this key is reached
        return "QUOTA_EXCEEDED"
    else:
        return f"API Error: {response.status_code}"

def main():
    # 1. Load API keys and Search Engine ID from the auxiliary Excel file
    try:
        df_keys = pd.read_excel(file_keys)
        keys_list = df_keys['key'].tolist()
        cx_id = df_keys['cx'].iloc[0] # Assuming all keys use the same Search Engine ID
    except Exception as e:
        print(f"Error loading API keys: {e}")
        return

    # 2. Load the main company database
    df_comp = pd.read_excel(file_companies)
    
    # Ensure the LinkedIn URL column exists
    if 'Linkedin_URL' not in df_comp.columns:
        df_comp['Linkedin_URL'] = ""

    current_key_index = 0
    print(f"Starting script with {len(keys_list)} API keys available.")

    # 3. Iterate through companies in the Excel file
    for index, row in df_comp.iterrows():
        # Only process rows where the LinkedIn URL is missing
        if pd.isna(row['Linkedin_URL']) or row['Linkedin_URL'] == "":
            company = row.iloc[0] # Assumes Column A contains the company name
            print(f"Searching for: {company}...")
            
            success = False
            while not success:
                # Check if we ran out of keys
                if current_key_index >= len(keys_list):
                    print("All API keys exhausted for today!")
                    df_comp.to_excel(file_companies, index=False)
                    return

                result = get_linkedin_url(company, keys_list[current_key_index], cx_id)
                
                if result == "QUOTA_EXCEEDED":
                    print(f"Key {current_key_index + 1} exhausted. Switching to next key...")
                    current_key_index += 1
                else:
                    # Store the result in the DataFrame
                    df_comp.at[index, 'Linkedin_URL'] = result
                    success = True
                    # Short pause to stay within API rate limits
                    time.sleep(0.5)

    # 4. Final save to OneDrive
    df_comp.to_excel(file_companies, index=False)
    print("Process complete. File updated on OneDrive.")

if __name__ == "__main__":
    main()
import gspread
import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials

# Load credentials dari GitHub Secret (service account yang sama dengan dashboard lain)
creds_json = os.environ['GOOGLE_CREDENTIALS']
creds_dict = json.loads(creds_json)

scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

# Spreadsheet MASTER Report Accident Armada
SPREADSHEET_ID = '1FAXTvdFYJTDyVMdeC7kI2mlztsx8wjumC2rlx-tEhWs'
GID = 623775097  # tab "Detail SCM 2026" (satu tab, semua site gabung)

spreadsheet = client.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.get_worksheet_by_id(GID)

data = worksheet.get_all_records()
df = pd.DataFrame(data)

os.makedirs('data', exist_ok=True)
output_path = 'data/accident.csv'
df.to_csv(output_path, index=False)
print(f"✅ accident.csv — {len(df)} rows")
print("Done.")

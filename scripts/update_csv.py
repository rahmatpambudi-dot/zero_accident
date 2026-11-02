import gspread
import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials

# Load credentials dari GitHub Secret (service account yang sama dengan dashboard lain)
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.readonly']
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

# Spreadsheet MASTER Report Accident Armada
SPREADSHEET_ID = '1FAXTvdFYJTDyVMdeC7kI2mlztsx8wjumC2rlx-tEhWs'
GID = 623775097  # tab "Detail SCM 2026" (satu tab, semua site gabung)

worksheet = client.open_by_key(SPREADSHEET_ID).get_worksheet_by_id(GID)

# Ambil nilai mentah (tidak error walau header ada yang kosong/dobel)
rows = worksheet.get_all_values()
header, body = rows[0], rows[1:]

# Kolom dengan header kosong dibuang (biasanya kolom bantu / sisa format)
keep = [i for i, h in enumerate(header) if h.strip() != '']
cols = [header[i] for i in keep]

# Header dobel diberi akhiran _2, _3, dst supaya tetap unik
seen = {}
for n, h in enumerate(cols):
    if h in seen:
        seen[h] += 1
        cols[n] = f'{h}_{seen[h]}'
    else:
        seen[h] = 1

data = [[r[i] if i < len(r) else '' for i in keep] for r in body]
df = pd.DataFrame(data, columns=cols)
df = df[(df != '').any(axis=1)]  # buang baris yang kosong semua

dropped = len(header) - len(keep)
if dropped:
    print(f"ℹ️ {dropped} kolom tanpa header diabaikan")

os.makedirs('data', exist_ok=True)
df.to_csv('data/accident.csv', index=False)
print(f"✅ accident.csv — {len(df)} rows, {len(df.columns)} kolom")
print("Done.")

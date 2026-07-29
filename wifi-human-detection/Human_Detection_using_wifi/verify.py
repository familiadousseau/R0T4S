import pandas as pd
import glob
import os

print("─" * 50)
print("DATA COLLECTION VERIFICATION")
print("─" * 50)

total_rows = 0
all_good = True

for activity in ['walking', 'sitting', 'standing']:
    for session in ['1', '2', '3']:
        path = f'data/{activity}/session{session}.csv'
        
        if not os.path.exists(path):
            print(f"MISSING: {path}")
            all_good = False
            continue
        
        df = pd.read_csv(path)
        rows = len(df)
        total_rows += rows
        
        status = "✓" if rows >= 200 else "LOW"
        print(f"{status} {activity}/session{session}: {rows} rows")

print("─" * 50)
print(f"Total rows: {total_rows}")
print("─" * 50)

if all_good:
    print("All 9 files present. Ready for ML pipeline.")
else:
    print("Some files missing — recheck.")
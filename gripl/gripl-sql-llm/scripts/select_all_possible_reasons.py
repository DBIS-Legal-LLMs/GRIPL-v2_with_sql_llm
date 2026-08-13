from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT = Path(__file__).resolve().parents[3]

FILE_PATH = PROJECT_ROOT / "dataset" / "evaluation_data.csv"

reasons = set()
df = pd.read_csv(FILE_PATH)

for index, row in df.iterrows():
    expected_values = row["expected_values"]
    expected_values = json.loads(expected_values)

    for ev in expected_values:
        reasons.add(ev["reason"])


print(reasons)


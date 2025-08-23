import pandas as pd
import numpy as np

# === 1) Load and reshape data ===
df_long = pd.read_csv("perkins_water_quality.csv")
df_long['Level Found'] = pd.to_numeric(df_long['Level Found'], errors='coerce')

# Single-row DF with contaminants as columns
df = df_long.set_index('Contaminant')[['Level Found']].transpose()
df.reset_index(drop=True, inplace=True) # Flatten to a simple row

# Add placeholder columns for metadata if they don't exist from the pivot
if 'date' not in df: df['date'] = df_long['Date Tested'].iloc[0] if not df_long.empty else 'N/A'
if 'location' not in df: df['location'] = 'Perkins District'

# === 2) Helper functions ===
def clamp(x, lo=0, hi=100):
    return max(lo, min(hi, x))

def sub_lower_is_better(value, limit, eps=1e-6):
    if pd.isna(value):
        return np.nan
    v = max(value, eps)
    return clamp(100 * (limit / v))

def sub_target_band(value, low, high, k):
    if pd.isna(value):
        return np.nan
    if low <= value <= high:
        return 100.0
    dist = low - value if value < low else value - high
    return clamp(100 - k * dist)

def sub_binary_safe(flag_detected):
    if pd.isna(flag_detected):
        return np.nan
    # Assuming 'Violation' column indicates presence. 'Yes' means a problem (0 score).
    return 0.0 if str(flag_detected).strip().lower() == 'yes' else 100.0

# === 3) Compute subscores (0–100) ===
# Map CSV contaminant names to the names used in the script's logic
CONTAMINANT_MAP = {
    "Ecoli": "E. coli",
    "TTHM": "Total Trihalomethanes (TTHM)",
    "HAA5": "Haloacetic Acids (HAA5)",
    "Nitrate": "Nitrate",
    "Turb": "Turbidity",
    "Chlor": "Chlorine",
    "pH": "pH",
    "Mn": "Manganese",
    "Cu": "Copper",
    "Pb": "Lead",
    "Ba": "Barium",
    "F": "Fluoride"
}

# Helper to get a value from the DataFrame, returning NaN if the column doesn't exist
def get_value(contaminant_key):
    col_name = CONTAMINANT_MAP.get(contaminant_key)
    return df[col_name].iloc[0] if col_name and col_name in df.columns else np.nan

# Get violation status for E. coli if available
ecoli_violation = df_long[df_long['Contaminant'] == CONTAMINANT_MAP['Ecoli']]['Violation'].iloc[0] if CONTAMINANT_MAP['Ecoli'] in df_long.Contaminant.values else np.nan

subs = {}
subs["Ecoli"]   = sub_binary_safe(ecoli_violation)
subs["TTHM"]    = sub_lower_is_better(get_value("TTHM"), limit=80)
subs["HAA5"]    = sub_lower_is_better(get_value("HAA5"), limit=60)
subs["Nitrate"] = sub_lower_is_better(get_value("Nitrate"), limit=10)
subs["Turb"]    = sub_lower_is_better(get_value("Turb"), limit=0.3)
subs["Chlor"]   = sub_target_band(get_value("Chlor"), 1.0, 2.0, k=80)
subs["pH"]      = sub_target_band(get_value("pH"), 6.5, 8.5, k=40)
subs["Mn"]      = sub_lower_is_better(get_value("Mn"), limit=50)
subs["Cu"]      = sub_lower_is_better(get_value("Cu"), limit=1.3) # Action Level for Copper is 1.3 mg/L
subs["Pb"]      = sub_lower_is_better(get_value("Pb"), limit=15)  # Action Level for Lead is 15 ppb

# === 4) Weights (tweak as needed) ===
# Adjusted weights to include new contaminants and remove unavailable ones
weights = {
    "Ecoli": 0.25, "TTHM": 0.15, "HAA5": 0.10, "Nitrate": 0.10,
    "Turb":  0.10, "Chlor":0.05, "pH":    0.05, "Mn":     0.05,
    "Cu": 0.05, "Pb": 0.10
}

# Filter out any contaminants that weren't in the data
valid_subs = {k: v for k, v in subs.items() if pd.notna(v)}
sub_cols = list(valid_subs.keys())

if not sub_cols:
    print("No valid contaminant data found to calculate a score.")
else:
    # Re-weight based on available data
    total_weight = sum(weights[c] for c in sub_cols)
    W = np.array([weights[c] / total_weight for c in sub_cols])
    
    vals = np.array(list(valid_subs.values()))
    
    # === 5) Calculate final score and rating ===
    score = float(np.dot(vals, W))
    limiting_factor = min(valid_subs, key=valid_subs.get)
    
    def to_stars(s):
        if pd.isna(s): return np.nan
        if s >= 90: return 5
        if s >= 75: return 4
        if s >= 60: return 3
        if s >= 40: return 2
        return 1
    
    rating = to_stars(score)
    
    # === 6) Save results ===
    summary = pd.DataFrame([{
        "location": df['location'].iloc[0],
        "date": df['date'].iloc[0],
        "index_0_100": score,
        "rating_1_5": rating,
        "limiting_factor": limiting_factor
    }])
    
    # Add the subscores for transparency
    for k, v in valid_subs.items():
        summary[f"subscore_{k}"] = v

    summary.to_csv("water_quality_rating_summary.csv", index=False)
    print("Water quality summary saved to 'water_quality_rating_summary.csv'")
    print(summary.round(2).to_string(index=False))

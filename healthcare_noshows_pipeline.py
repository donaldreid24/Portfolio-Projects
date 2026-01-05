# ----------------------------
# Automated Data Cleaning & Exploration of Healthcare Appointment No-Shows
# ----------------------------

import os
import pandas as pd
import glob
from IPython.display import display, Markdown
from google.colab import drive

# ----------------------------
# 1️⃣ Mount Google Drive
# ----------------------------
drive.mount('/content/drive', force_remount=True)

output_folder = '/content/drive/MyDrive/Portfolio/HealthcareProject'
os.makedirs(output_folder, exist_ok=True)

# ----------------------------
# 2️⃣ Automatically locate dataset CSV
# ----------------------------
csv_files = glob.glob(os.path.join(output_folder, '*.csv'))

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in folder: {output_folder}")

csv_file = csv_files[0]
print(f"Using dataset: {csv_file}")

df = pd.read_csv(csv_file)

# ----------------------------
# 3️⃣ Basic column cleanup
# ----------------------------
df.columns = df.columns.str.strip()

# ----------------------------
# 4️⃣ Clean PatientId
# ----------------------------
df['PatientId'] = df['PatientId'].astype(str).str.split('.').str[0].str.strip()

# ----------------------------
# 5️⃣ Create no-show indicator
# ----------------------------
if 'Showed_up' in df.columns:
    df['no_show'] = (df['Showed_up'] == 0).astype(int)
else:
    raise KeyError("Expected column 'Showed_up' not found.")

# ----------------------------
# 6️⃣ Analyst metrics
# ----------------------------
no_show_rate = df['no_show'].mean() * 100
print(f"No-show rate: {no_show_rate:.2f}%")

display(df['no_show'].value_counts())

# ----------------------------
# 7️⃣ Save cleaned dataset
# ----------------------------
output_path = os.path.join(output_folder, 'healthcare_noshows_clean.csv')
df.to_csv(output_path, index=False)
print(f"Cleaned CSV saved at: {output_path}")

# ----------------------------
# 8️⃣ Shareable download link
# ----------------------------
shareable_link = "https://drive.google.com/file/d/1Eje8kbfuFouRvN05rCsolntRQzO4elzC/view?usp=share_link"
display(Markdown(f"[Download the cleaned healthcare no-shows dataset]({shareable_link})"))

# ----------------------------
# 9️⃣ Dataset overview (lightweight)
# ----------------------------
display(df.head())
df.info()
display(df.describe(include='all'))

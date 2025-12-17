import pandas as pd

# Load data
df = pd.read_excel(r'path/to/ALL_CADS.xlsx', sheet_name='Sheet1')

# Standardize How Reported
valid_methods = ['Phone','911','In Person','Email','Other']
df['How Reported'] = (df['How Reported']
    .astype(str).str.strip().str.title()
    .replace({m.lower(): m for m in valid_methods}, regex=True))
df.loc[~df['How Reported'].isin(valid_methods), 'How Reported'] = 'Other'

# Split FullAddress2
parts = df['FullAddress2'].str.rsplit(',', n=3, expand=True)
df['Street'] = parts[0].str.strip()
df['City']   = parts[1].str.strip()
df['State']  = parts[2].str.strip()
df['Zip']    = parts[3].str.strip()

# Convert PDZone to integer
df['PDZone'] = df['PDZone'].astype('Int64')

# Save cleaned
df.to_excel(r'path/to/ALL_CADS_cleaned.xlsx', index=False)

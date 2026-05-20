# ============================================================
#  Together.aid — Visualization 1: Healthcare Quality World Map
#  Data: Our World in Data — Healthcare Access & Quality Index
#  Tool: Plotly Express
# ============================================================

import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# ── 1. LOAD DATA ─────────────────────────────────────────────
# Make sure your CSV is saved inside the data/ folder
# Download from: https://ourworldindata.org/grapher/healthcare-access-and-quality-index

DATA_PATH = os.path.join("data", "universal-health-coverage-index.csv")
df = pd.read_csv(DATA_PATH)

# Preview what columns you have — helpful for debugging
print("Columns in dataset:")
print(df.columns.tolist())
print(f"\nShape: {df.shape}")
print(df.head())

# ── 2. CLEAN DATA ─────────────────────────────────────────────
# Find the HAQ score column automatically (in case the name varies slightly)
haq_col = 'UHC Service Coverage Index (SDG 3.8.1)'
print(f"\nUsing column: {haq_col}")

# Keep only the most recent year of data per country
df_latest = (
    df.sort_values("Year")
    .groupby("Entity")
    .last()
    .reset_index()
)

# Drop rows with missing HAQ scores
df_latest = df_latest.dropna(subset=[haq_col])

# Rename columns for clarity
df_latest = df_latest.rename(columns={
    "Entity": "Country",
    haq_col: "HAQ_Score"
})

print(f"\nCountries included: {len(df_latest)}")
print(df_latest[["Country", "Year", "HAQ_Score"]].head(10))

# ── 3. BUILD THE MAP ──────────────────────────────────────────
fig = px.choropleth(
    df_latest,
    locations="Country",            # column with country names
    locationmode="country names",   # match by country name
    color="HAQ_Score",              # color = quality score
    hover_name="Country",           # shown when you hover
    hover_data={"HAQ_Score": ":.1f", "Year": True},
    color_continuous_scale="Blues", # light blue = low, dark blue = high
    range_color=[0, 100],           # HAQ score range is 0–100
    title="Healthcare Access & Quality Index by Country",
    labels={"HAQ_Score": "HAQ Score (0–100)"}
)

# ── 4. STYLE THE MAP ──────────────────────────────────────────
fig.update_layout(
    title=dict(
        text="Healthcare Access & Quality Index by Country",
        font=dict(size=22),
        x=0.5,                      # center the title
        xanchor="center"
    ),
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="lightgray",
        showland=True,
        landcolor="whitesmoke",
        showocean=True,
        oceancolor="aliceblue",
        projection_type="natural earth"
    ),
    coloraxis_colorbar=dict(
        title="Score",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["0", "25", "50", "75", "100"]
    ),
    margin=dict(l=0, r=0, t=60, b=0),
    height=550
)

# ── 5. PREVIEW IN BROWSER ─────────────────────────────────────
# This opens the map in your default browser so you can see it
fig.show()

# ── 6. EXPORT AS HTML FOR WIX ────────────────────────────────
# Make sure the visualizations/ folder exists
os.makedirs("visualizations", exist_ok=True)

output_path = os.path.join("visualizations", "healthcare_quality_map.html")

pio.write_html(
    fig,
    file=output_path,
    auto_open=False,
    include_plotlyjs="cdn"      # keeps file small, loads plotly from web
)

print(f"\n✓ Map saved to: {output_path}")
print("Next step: upload this file to GitHub Pages, then embed in Wix!")

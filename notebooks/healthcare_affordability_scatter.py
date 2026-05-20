# ============================================================
#  Together.aid — Visualization 2: Healthcare Affordability Scatter Plot
#  Data: WHO Global Health Expenditure Database (GHED)
#  Shows: Out-of-pocket spending vs GDP per capita by country
#  Tool: Plotly Express
# ============================================================

import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# ── 1. LOAD DATA ─────────────────────────────────────────────
DATA_PATH = os.path.join("data", "GHED_data.xlsx")
df = pd.read_excel(DATA_PATH)

print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ── 2. SELECT ONLY THE COLUMNS WE NEED ───────────────────────
# oops_che = out-of-pocket spending as % of current health expenditure
# gdp_pc_usd = GDP per capita in USD (measure of country wealth)
# income = income group (Low, Lower-middle, Upper-middle, High)

df = df[['location', 'code', 'region', 'income', 'year', 'gdp_pc_usd', 'oops_che']].copy()

# ── 3. CLEAN DATA ─────────────────────────────────────────────
# Keep only the most recent year per country
df_latest = (
    df.sort_values('year')
    .groupby('location')
    .last()
    .reset_index()
)

# Drop rows where either key column is missing
df_latest = df_latest.dropna(subset=['gdp_pc_usd', 'oops_che'])

# Clean up income group labels for the legend
income_order = ['Low', 'Lower-middle', 'Upper-middle', 'High']
df_latest['income'] = pd.Categorical(df_latest['income'], categories=income_order, ordered=True)
df_latest = df_latest.sort_values('income')

print(f"\nCountries with complete data: {len(df_latest)}")
print(df_latest[['location', 'year', 'gdp_pc_usd', 'oops_che', 'income']].head(10))

# ── 4. BUILD THE SCATTER PLOT ─────────────────────────────────
# x-axis: GDP per capita (how wealthy the country is)
# y-axis: out-of-pocket % (how much people pay themselves)
# color:  income group
# size:   fixed (each dot same size for clarity)

fig = px.scatter(
    df_latest,
    x='gdp_pc_usd',
    y='oops_che',
    color='income',
    hover_name='location',
    hover_data={
        'gdp_pc_usd': ':,.0f',
        'oops_che': ':.1f',
        'income': True,
        'year': True,
        'code': False
    },
    color_discrete_map={
        'Low': '#E24B4A',           # red — most burdened
        'Lower-middle': '#EF9F27',  # amber
        'Upper-middle': '#378ADD',  # blue
        'High': '#1D9E75'           # green — least burdened
    },
    category_orders={'income': income_order},
    labels={
        'gdp_pc_usd': 'GDP per Capita (USD)',
        'oops_che': 'Out-of-Pocket Spending (% of Health Expenditure)',
        'income': 'Income Group'
    },
    title='Healthcare Affordability: Who Pays the Most Out of Pocket?',
    opacity=0.8
)

# ── 5. STYLE THE CHART ────────────────────────────────────────
fig.update_traces(marker=dict(size=10, line=dict(width=0.5, color='white')))

fig.update_layout(
    title=dict(
        text='Healthcare Affordability: Who Pays the Most Out of Pocket?',
        font=dict(size=20),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title='GDP per Capita (USD) — Country Wealth →',
        type='log',              # log scale so poor countries aren't squished
        showgrid=True,
        gridcolor='#f0f0f0'
    ),
    yaxis=dict(
        title='Out-of-Pocket Spending (% of Health Expenditure)',
        showgrid=True,
        gridcolor='#f0f0f0'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        title='Income Group',
        orientation='v',
        x=1.02,
        y=1
    ),
    height=550,
    margin=dict(l=60, r=150, t=70, b=60)
)

# Add a helpful annotation explaining the pattern
fig.add_annotation(
    text='↑ Higher % means people pay<br>more out of their own pocket',
    xref='paper', yref='paper',
    x=0.01, y=0.97,
    showarrow=False,
    font=dict(size=11, color='gray'),
    align='left'
)

# ── 6. PREVIEW IN BROWSER ─────────────────────────────────────
fig.show()

# ── 7. EXPORT AS HTML FOR WIX ────────────────────────────────
os.makedirs('visualizations', exist_ok=True)
output_path = os.path.join('visualizations', 'healthcare_affordability_scatter.html')

pio.write_html(
    fig,
    file=output_path,
    auto_open=False,
    include_plotlyjs='cdn'
)

print(f"\n✓ Chart saved to: {output_path}")
print("Next: upload to GitHub Pages, then embed in Wix!")

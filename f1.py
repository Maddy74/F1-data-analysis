#Initial setup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')


# Use working matplotlib style
try:
    plt.style.use('seaborn-darkgrid')
except:
    plt.style.use('default')

sns.set_palette("husl")

# Load datasets
season_2024 = pd.read_csv('Formula1_2024season_raceResults.csv')
season_2025 = pd.read_csv('Formula1_2025Season_RaceResults.csv')

# Add season columns
season_2024['Season'] = 2024
season_2025['Season'] = 2025

# Fix Position column - convert to numeric, handling non-numeric values
season_2024['Position'] = pd.to_numeric(season_2024['Position'], errors='coerce')
season_2025['Position'] = pd.to_numeric(season_2025['Position'], errors='coerce')

# Fix Points column
season_2024['Points'] = pd.to_numeric(season_2024['Points'], errors='coerce').fillna(0)
season_2025['Points'] = pd.to_numeric(season_2025['Points'], errors='coerce').fillna(0)

print("Data loaded successfully!")
print("2024 Season Shape:", season_2024.shape)
print("2025 Season Shape:", season_2025.shape)

# Set style for better-looking plots
plt.style.use('seaborn-darkgrid')
sns.set_palette("husl")

# Load the datasets
season_2024 = pd.read_csv('Formula1_2024season_raceResults.csv')
season_2025 = pd.read_csv('Formula1_2025Season_RaceResults.csv')

# Add season columns for easier analysis
season_2024['Season'] = 2024
season_2025['Season'] = 2025

# Basic data cleaning
season_2024['Points'] = pd.to_numeric(season_2024['Points'], errors='coerce')
season_2025['Points'] = pd.to_numeric(season_2025['Points'], errors='coerce')

# Fill NaN points with 0
season_2024['Points'] = season_2024['Points'].fillna(0)
season_2025['Points'] = season_2025['Points'].fillna(0)

print("2024 Season Shape:", season_2024.shape)
print("2025 Season Shape:", season_2025.shape)
print("\nColumns:", season_2024.columns.tolist())

#Driver Performance Analysis
# Top 10 drivers by points - 2024 vs 2025
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Top drivers 2024
top_drivers_2024 = season_2024.groupby('Driver')['Points'].sum().sort_values(ascending=False).head(10)
axes[0,0].barh(range(len(top_drivers_2024)), top_drivers_2024.values, color='skyblue')
axes[0,0].set_yticks(range(len(top_drivers_2024)))
axes[0,0].set_yticklabels(top_drivers_2024.index)
axes[0,0].set_title('Top 10 Drivers - 2024 Season Points')
axes[0,0].set_xlabel('Total Points')

# Top drivers 2025
top_drivers_2025 = season_2025.groupby('Driver')['Points'].sum().sort_values(ascending=False).head(10)
axes[0,1].barh(range(len(top_drivers_2025)), top_drivers_2025.values, color='lightcoral')
axes[0,1].set_yticks(range(len(top_drivers_2025)))
axes[0,1].set_yticklabels(top_drivers_2025.index)
axes[0,1].set_title('Top 10 Drivers - 2025 Season Points')
axes[0,1].set_xlabel('Total Points')

# Race wins comparison
wins_2024 = season_2024[season_2024['Position'] == 1]['Driver'].value_counts().head(10)
axes[1,0].bar(range(len(wins_2024)), wins_2024.values, color='gold')
axes[1,0].set_xticks(range(len(wins_2024)))
axes[1,0].set_xticklabels(wins_2024.index, rotation=45)
axes[1,0].set_title('Race Wins - 2024 Season')
axes[1,0].set_ylabel('Number of Wins')

wins_2025 = season_2025[season_2025['Position'] == 1]['Driver'].value_counts().head(10)
axes[1,1].bar(range(len(wins_2025)), wins_2025.values, color='orange')
axes[1,1].set_xticks(range(len(wins_2025)))
axes[1,1].set_xticklabels(wins_2025.index, rotation=45)
axes[1,1].set_title('Race Wins - 2025 Season')
axes[1,1].set_ylabel('Number of Wins')

plt.tight_layout()
plt.show()

# Team Performance Analysis
# Team performance comparison
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Team points 2024
team_points_2024 = season_2024.groupby('Team')['Points'].sum().sort_values(ascending=False)
axes[0,0].pie(team_points_2024.values, labels=team_points_2024.index, autopct='%1.1f%%', startangle=90)
axes[0,0].set_title('Team Points Distribution - 2024')

# Team points 2025
team_points_2025 = season_2025.groupby('Team')['Points'].sum().sort_values(ascending=False)
axes[0,1].pie(team_points_2025.values, labels=team_points_2025.index, autopct='%1.1f%%', startangle=90)
axes[0,1].set_title('Team Points Distribution - 2025')

# Comprehensive data cleaning for both datasets
def clean_race_data(df):
    """Clean Formula 1 race data for analysis"""
    df_clean = df.copy()
    
    # Convert Position to numeric, keeping original for reference
    df_clean['Position_Original'] = df_clean['Position']
    df_clean['Position'] = pd.to_numeric(df_clean['Position'], errors='coerce')
    
    # Convert Points to numeric
    df_clean['Points'] = pd.to_numeric(df_clean['Points'], errors='coerce').fillna(0)
    
    # Convert Starting Grid to numeric if it exists
    if 'Starting Grid' in df_clean.columns:
        df_clean['Starting Grid'] = pd.to_numeric(df_clean['Starting Grid'], errors='coerce')
    
    return df_clean

# Apply cleaning
season_2024 = clean_race_data(season_2024)
season_2025 = clean_race_data(season_2025)

# Now your original code will work
podiums_2024 = season_2024[season_2024['Position'] <= 3]['Team'].value_counts()
podiums_2025 = season_2025[season_2025['Position'] <= 3]['Team'].value_counts()


#Race-by-Race Analysis
# Track performance analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Points distribution by track - 2024
track_points_2024 = season_2024.groupby('Track')['Points'].sum()
axes[0,0].plot(range(len(track_points_2024)), track_points_2024.values, 'o-', color='blue', linewidth=2, markersize=6)
axes[0,0].set_title('Points Distribution by Track - 2024')
axes[0,0].set_xlabel('Race Number')
axes[0,0].set_ylabel('Total Points Awarded')
axes[0,0].grid(True, alpha=0.3)

# Points distribution by track - 2025
track_points_2025 = season_2025.groupby('Track')['Points'].sum()
axes[0,1].plot(range(len(track_points_2025)), track_points_2025.values, 'o-', color='red', linewidth=2, markersize=6)
axes[0,1].set_title('Points Distribution by Track - 2025')
axes[0,1].set_xlabel('Race Number')
axes[0,1].set_ylabel('Total Points Awarded')
axes[0,1].grid(True, alpha=0.3)

# DNF analysis
dnf_2024 = season_2024[season_2024['Time/Retired'] == 'DNF']['Driver'].value_counts()
if not dnf_2024.empty:
    axes[1,0].bar(dnf_2024.index[:10], dnf_2024.values[:10], color='crimson')
    axes[1,0].set_title('DNF (Did Not Finish) Count - 2024')
    axes[1,0].set_ylabel('Number of DNFs')
    axes[1,0].tick_params(axis='x', rotation=45)

dnf_2025 = season_2025[season_2025['Time/Retired'] == 'DNF']['Driver'].value_counts()
if not dnf_2025.empty:
    axes[1,1].bar(dnf_2025.index[:10], dnf_2025.values[:10], color='darkred')
    axes[1,1].set_title('DNF (Did Not Finish) Count - 2025')
    axes[1,1].set_ylabel('Number of DNFs')
    axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

#Statistical Analysis and Heatmaps
# Performance heatmap
fig, axes = plt.subplots(1, 2, figsize=(20, 8))

# Create driver-track performance matrix for 2024
driver_track_2024 = season_2024.pivot_table(values='Points', index='Driver', columns='Track', aggfunc='sum', fill_value=0)
top_drivers_list_2024 = top_drivers_2024.head(8).index.tolist()
driver_track_2024_filtered = driver_track_2024.loc[driver_track_2024.index.isin(top_drivers_list_2024)]

sns.heatmap(driver_track_2024_filtered, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[0])
axes[0].set_title('Driver Performance by Track - 2024 (Top 8 Drivers)')
axes[0].set_ylabel('Driver')
axes[0].set_xlabel('Track')

# Create driver-track performance matrix for 2025
driver_track_2025 = season_2025.pivot_table(values='Points', index='Driver', columns='Track', aggfunc='sum', fill_value=0)
top_drivers_list_2025 = top_drivers_2025.head(8).index.tolist()
driver_track_2025_filtered = driver_track_2025.loc[driver_track_2025.index.isin(top_drivers_list_2025)]

sns.heatmap(driver_track_2025_filtered, annot=True, fmt='.0f', cmap='YlGnBu', ax=axes[1])
axes[1].set_title('Driver Performance by Track - 2025 (Top 8 Drivers)')
axes[1].set_ylabel('Driver')
axes[1].set_xlabel('Track')

plt.tight_layout()
plt.show()

#Position Distribution Analysis
# Position distribution analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Position histogram 2024
position_dist_2024 = season_2024['Position'].value_counts().sort_index()
axes[0,0].hist(season_2024['Position'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
axes[0,0].set_title('Position Distribution - 2024')
axes[0,0].set_xlabel('Finishing Position')
axes[0,0].set_ylabel('Frequency')

# Position histogram 2025
axes[0,1].hist(season_2025['Position'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
axes[0,1].set_title('Position Distribution - 2025')
axes[0,1].set_xlabel('Finishing Position')
axes[0,1].set_ylabel('Frequency')

# Boxplot of points by position
combined_data = pd.concat([season_2024[['Position', 'Points', 'Season']], 
                          season_2025[['Position', 'Points', 'Season']]])

# Filter to top 10 positions for better visualization
top_10_positions = combined_data[combined_data['Position'] <= 10]

sns.boxplot(data=top_10_positions, x='Position', y='Points', hue='Season', ax=axes[1,0])
axes[1,0].set_title('Points Distribution by Position (Top 10)')
axes[1,0].set_xlabel('Finishing Position')
axes[1,0].set_ylabel('Points Scored')

# Scatter plot: Starting Grid vs Finishing Position
axes[1,1].scatter(season_2024['Starting Grid'], season_2024['Position'], 
                  alpha=0.6, color='blue', label='2024', s=30)
axes[1,1].scatter(season_2025['Starting Grid'], season_2025['Position'], 
                  alpha=0.6, color='red', label='2025', s=30)
axes[1,1].set_title('Starting Grid vs Finishing Position')
axes[1,1].set_xlabel('Starting Grid Position')
axes[1,1].set_ylabel('Finishing Position')
axes[1,1].legend()
axes[1,1].plot([1, 20], [1, 20], 'k--', alpha=0.5)  # Perfect correlation line

plt.tight_layout()
plt.show()

#Advanced Analytics
# Advanced analytics
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Consistency analysis - Standard deviation of positions
consistency_2024 = season_2024.groupby('Driver')['Position'].std().sort_values()
top_consistent_2024 = consistency_2024.head(10)
axes[0,0].barh(range(len(top_consistent_2024)), top_consistent_2024.values, color='lightblue')
axes[0,0].set_yticks(range(len(top_consistent_2024)))
axes[0,0].set_yticklabels(top_consistent_2024.index)
axes[0,0].set_title('Most Consistent Drivers 2024 (Lower = More Consistent)')
axes[0,0].set_xlabel('Position Standard Deviation')

consistency_2025 = season_2025.groupby('Driver')['Position'].std().sort_values()
top_consistent_2025 = consistency_2025.head(10)
axes[0,1].barh(range(len(top_consistent_2025)), top_consistent_2025.values, color='lightcoral')
axes[0,1].set_yticks(range(len(top_consistent_2025)))
axes[0,1].set_yticklabels(top_consistent_2025.index)
axes[0,1].set_title('Most Consistent Drivers 2025 (Lower = More Consistent)')
axes[0,1].set_xlabel('Position Standard Deviation')

# Average finishing position
avg_position_2024 = season_2024.groupby('Driver')['Position'].mean().sort_values().head(10)
axes[1,0].bar(range(len(avg_position_2024)), avg_position_2024.values, color='gold')
axes[1,0].set_xticks(range(len(avg_position_2024)))
axes[1,0].set_xticklabels(avg_position_2024.index, rotation=45)
axes[1,0].set_title('Best Average Finishing Position - 2024')
axes[1,0].set_ylabel('Average Position')

avg_position_2025 = season_2025.groupby('Driver')['Position'].mean().sort_values().head(10)
axes[1,1].bar(range(len(avg_position_2025)), avg_position_2025.values, color='silver')
axes[1,1].set_xticks(range(len(avg_position_2025)))
axes[1,1].set_xticklabels(avg_position_2025.index, rotation=45)
axes[1,1].set_title('Best Average Finishing Position - 2025')
axes[1,1].set_ylabel('Average Position')

plt.tight_layout()
plt.show()

#Summary Statistics and Tables
# Create comprehensive summary statistics
print("=== COMPREHENSIVE FORMULA 1 ANALYSIS SUMMARY ===\n")

# Season comparison table
season_stats = pd.DataFrame({
    '2024 Season': [
        len(season_2024['Track'].unique()),
        len(season_2024['Driver'].unique()),
        len(season_2024['Team'].unique()),
        season_2024[season_2024['Position'] == 1]['Driver'].value_counts().iloc[0],
        season_2024[season_2024['Position'] == 1]['Driver'].value_counts().index[0],
        season_2024.groupby('Driver')['Points'].sum().max(),
        season_2024.groupby('Driver')['Points'].sum().idxmax()
    ],
    '2025 Season': [
        len(season_2025['Track'].unique()),
        len(season_2025['Driver'].unique()),
        len(season_2025['Team'].unique()),
        season_2025[season_2025['Position'] == 1]['Driver'].value_counts().iloc[0],
        season_2025[season_2025['Position'] == 1]['Driver'].value_counts().index[0],
        season_2025.groupby('Driver')['Points'].sum().max(),
        season_2025.groupby('Driver')['Points'].sum().idxmax()
    ]
}, index=['Total Races', 'Total Drivers', 'Total Teams', 'Most Wins Count', 
          'Most Wins Driver', 'Highest Points', 'Points Leader'])

print("Season Comparison:")
print(season_stats)
print("\n" + "="*60)

# Top 5 drivers points comparison
print("\nTop 5 Drivers Points Comparison:")
comparison_df = pd.DataFrame({
    '2024_Driver': top_drivers_2024.head().index,
    '2024_Points': top_drivers_2024.head().values,
    '2025_Driver': top_drivers_2025.head().index,
    '2025_Points': top_drivers_2025.head().values
})
print(comparison_df)

# Qualifying performance impact on race results
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Starting grid position vs points correlation
correlation_2024 = season_2024[['Starting Grid', 'Points']].corr().iloc[0,1]
axes[0,0].scatter(season_2024['Starting Grid'], season_2024['Points'], alpha=0.6)
axes[0,0].set_title(f'Qualifying vs Points - 2024 (Correlation: {correlation_2024:.3f})')
axes[0,0].set_xlabel('Starting Grid Position')
axes[0,0].set_ylabel('Points Scored')

# Position gained/lost analysis
season_2024['Positions_Changed'] = season_2024['Starting Grid'] - season_2024['Position']
position_gainers = season_2024.groupby('Driver')['Positions_Changed'].mean().sort_values(ascending=False).head(10)

axes[0,1].barh(range(len(position_gainers)), position_gainers.values, color='green')
axes[0,1].set_yticks(range(len(position_gainers)))
axes[0,1].set_yticklabels(position_gainers.index)
axes[0,1].set_title('Average Positions Gained/Lost - 2024')
axes[0,1].set_xlabel('Average Position Change')

# Track difficulty and characteristics analysis
def analyze_track_characteristics():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Average finishing position spread by track (competitiveness)
    track_spread_2024 = season_2024.groupby('Track')['Position'].std().sort_values(ascending=False)
    axes[0,0].bar(range(len(track_spread_2024)), track_spread_2024.values, color='skyblue')
    axes[0,0].set_xticks(range(len(track_spread_2024)))
    axes[0,0].set_xticklabels(track_spread_2024.index, rotation=45)
    axes[0,0].set_title('Track Competitiveness (Higher = More Unpredictable)')
    axes[0,0].set_ylabel('Position Standard Deviation')
    
    # DNF rates by track (reliability challenge)
    dnf_by_track = season_2024[season_2024['Time/Retired'] == 'DNF'].groupby('Track').size()
    total_by_track = season_2024.groupby('Track').size()
    dnf_rates = (dnf_by_track / total_by_track * 100).fillna(0)
    
    axes[0,1].bar(range(len(dnf_rates)), dnf_rates.values, color='red', alpha=0.7)
    axes[0,1].set_xticks(range(len(dnf_rates)))
    axes[0,1].set_xticklabels(dnf_rates.index, rotation=45)
    axes[0,1].set_title('DNF Rate by Track (%)')
    axes[0,1].set_ylabel('DNF Percentage')



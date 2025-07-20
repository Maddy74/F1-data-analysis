import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🏎️ Formula 1 Data Analysis Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF1E1E;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #FF1E1E, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-container {
        background: linear-gradient(90deg, #FF1E1E, #FF6B6B);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data():
    """Load and clean F1 data with caching for better performance"""
    try:
        # Load datasets
        season_2024 = pd.read_csv('Formula1_2024season_raceResults.csv')
        season_2025 = pd.read_csv('Formula1_2025Season_RaceResults.csv')
        
        # Add season columns
        season_2024['Season'] = 2024
        season_2025['Season'] = 2025
        
        # Clean data
        def clean_race_data(df):
            df_clean = df.copy()
            df_clean['Position_Original'] = df_clean['Position']
            df_clean['Position'] = pd.to_numeric(df_clean['Position'], errors='coerce')
            df_clean['Points'] = pd.to_numeric(df_clean['Points'], errors='coerce').fillna(0)
            if 'Starting Grid' in df_clean.columns:
                df_clean['Starting Grid'] = pd.to_numeric(df_clean['Starting Grid'], errors='coerce')
            return df_clean
        
        season_2024 = clean_race_data(season_2024)
        season_2025 = clean_race_data(season_2025)
        
        return season_2024, season_2025
        
    except FileNotFoundError:
        st.error("CSV files not found. Please upload your Formula 1 data files.")
        return None, None

def main():
    # App title
    st.markdown('<h1 class="main-header">🏎️ Formula 1 Data Analysis Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    season_2024, season_2025 = load_and_clean_data()
    
    if season_2024 is None or season_2025 is None:
        st.error("Please ensure your CSV files are uploaded or in the correct directory")
        return
    
    # Sidebar navigation
    st.sidebar.title("📊 Analysis Navigation")
    analysis_option = st.sidebar.selectbox(
        "Choose Analysis Type:",
        ["📈 Overview", "🏁 Driver Performance", "🏭 Team Analysis", 
         "🏁 Race Analysis", "🏁 Track Performance", "📊 Advanced Analytics"]
    )
    
    # Main content based on selection
    if analysis_option == "📈 Overview":
        show_overview(season_2024, season_2025)
    elif analysis_option == "🏁 Driver Performance":
        show_driver_analysis(season_2024, season_2025)
    elif analysis_option == "🏭 Team Analysis":
        show_team_analysis(season_2024, season_2025)
    elif analysis_option == "🏁 Race Analysis":
        show_race_analysis(season_2024, season_2025)
    elif analysis_option == "🏁 Track Performance":
        show_track_analysis(season_2024, season_2025)
    elif analysis_option == "📊 Advanced Analytics":
        show_advanced_analytics(season_2024, season_2025)

def show_overview(season_2024, season_2025):
    st.header("📈 Season Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("2024 Races", len(season_2024['Track'].unique()))
    with col2:
        st.metric("2025 Races", len(season_2025['Track'].unique()))
    with col3:
        st.metric("Total Drivers", len(pd.concat([season_2024, season_2025])['Driver'].unique()))
    with col4:
        st.metric("Total Teams", len(pd.concat([season_2024, season_2025])['Team'].unique()))
    
    # Championship leaders
    st.subheader("🏆 Championship Leaders")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**2024 Season Leader**")
        leader_2024 = season_2024.groupby('Driver')['Points'].sum().idxmax()
        points_2024 = season_2024.groupby('Driver')['Points'].sum().max()
        st.success(f"{leader_2024}: {points_2024:.0f} points")
    
    with col2:
        st.write("**2025 Season Leader**")
        leader_2025 = season_2025.groupby('Driver')['Points'].sum().idxmax()
        points_2025 = season_2025.groupby('Driver')['Points'].sum().max()
        st.success(f"{leader_2025}: {points_2025:.0f} points")

def show_driver_analysis(season_2024, season_2025):
    st.header("🏁 Driver Performance Analysis")
    
    # Top drivers comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2024 Season - Top 10 Drivers")
        top_drivers_2024 = season_2024.groupby('Driver')['Points'].sum().sort_values(ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(range(len(top_drivers_2024)), top_drivers_2024.values, color='skyblue')
        ax.set_yticks(range(len(top_drivers_2024)))
        ax.set_yticklabels(top_drivers_2024.index)
        ax.set_title('Top 10 Drivers - 2024 Season Points')
        ax.set_xlabel('Total Points')
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center')
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("2025 Season - Top 10 Drivers")
        top_drivers_2025 = season_2025.groupby('Driver')['Points'].sum().sort_values(ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(range(len(top_drivers_2025)), top_drivers_2025.values, color='lightcoral')
        ax.set_yticks(range(len(top_drivers_2025)))
        ax.set_yticklabels(top_drivers_2025.index)
        ax.set_title('Top 10 Drivers - 2025 Season Points')
        ax.set_xlabel('Total Points')
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center')
        
        st.pyplot(fig)
        plt.close()

def show_team_analysis(season_2024, season_2025):
    st.header("🏭 Team Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Team Points Distribution - 2024")
        team_points_2024 = season_2024.groupby('Team')['Points'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(team_points_2024.values, labels=team_points_2024.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Team Points Distribution - 2024')
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Team Points Distribution - 2025")
        team_points_2025 = season_2025.groupby('Team')['Points'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(team_points_2025.values, labels=team_points_2025.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Team Points Distribution - 2025')
        st.pyplot(fig)
        plt.close()

def show_race_analysis(season_2024, season_2025):
    st.header("🏁 Race Analysis")
    
    # Race wins comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Race Wins - 2024")
        wins_2024 = season_2024[season_2024['Position'] == 1]['Driver'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(len(wins_2024)), wins_2024.values, color='gold')
        ax.set_xticks(range(len(wins_2024)))
        ax.set_xticklabels(wins_2024.index, rotation=45)
        ax.set_title('Race Wins - 2024 Season')
        ax.set_ylabel('Number of Wins')
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Race Wins - 2025")
        wins_2025 = season_2025[season_2025['Position'] == 1]['Driver'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(len(wins_2025)), wins_2025.values, color='orange')
        ax.set_xticks(range(len(wins_2025)))
        ax.set_xticklabels(wins_2025.index, rotation=45)
        ax.set_title('Race Wins - 2025 Season')
        ax.set_ylabel('Number of Wins')
        st.pyplot(fig)
        plt.close()

def show_track_analysis(season_2024, season_2025):
    st.header("🏁 Track Performance Analysis")
    
    # Track points distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Points Distribution by Track - 2024")
        track_points_2024 = season_2024.groupby('Track')['Points'].sum()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(range(len(track_points_2024)), track_points_2024.values, 'o-', color='blue', linewidth=2, markersize=6)
        ax.set_title('Points Distribution by Track - 2024')
        ax.set_xlabel('Race Number')
        ax.set_ylabel('Total Points Awarded')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Points Distribution by Track - 2025")
        track_points_2025 = season_2025.groupby('Track')['Points'].sum()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(range(len(track_points_2025)), track_points_2025.values, 'o-', color='red', linewidth=2, markersize=6)
        ax.set_title('Points Distribution by Track - 2025')
        ax.set_xlabel('Race Number')
        ax.set_ylabel('Total Points Awarded')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close()

def show_advanced_analytics(season_2024, season_2025):
    st.header("📊 Advanced Analytics")
    
    # Driver consistency analysis
    st.subheader("Driver Consistency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Most Consistent Drivers 2024**")
        consistency_2024 = season_2024.groupby('Driver')['Position'].std().sort_values().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(range(len(consistency_2024)), consistency_2024.values, color='lightblue')
        ax.set_yticks(range(len(consistency_2024)))
        ax.set_yticklabels(consistency_2024.index)
        ax.set_title('Most Consistent Drivers 2024 (Lower = More Consistent)')
        ax.set_xlabel('Position Standard Deviation')
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.write("**Most Consistent Drivers 2025**")
        consistency_2025 = season_2025.groupby('Driver')['Position'].std().sort_values().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(range(len(consistency_2025)), consistency_2025.values, color='lightcoral')
        ax.set_yticks(range(len(consistency_2025)))
        ax.set_yticklabels(consistency_2025.index)
        ax.set_title('Most Consistent Drivers 2025 (Lower = More Consistent)')
        ax.set_xlabel('Position Standard Deviation')
        st.pyplot(fig)
        plt.close()

if __name__ == "__main__":
    main()

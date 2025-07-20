import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
import base64
from PIL import Image
import requests
from io import BytesIO
from scipy import stats
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🏎️ Formula 1 Data Analysis Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        
        # Clean data function
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

def add_bg_video():
    """Add background styling and effects"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1));
    }
    
    .main-content {
        position: relative;
        z-index: 1;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .driver-card {
        background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 8px 32px rgba(255, 30, 30, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .driver-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255, 30, 30, 0.3);
    }
    
    .video-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        margin: 20px 0;
    }
    
    .stSelectbox > div > div {
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(90deg, #FF1E1E, #FF6B6B, #FF8A8A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def get_driver_images():
    """Return dictionary of driver images"""
    driver_images = {
        "Max Verstappen": "https://media.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.jpg.transform/1col/image.jpg",
        "Lando Norris": "https://media.formula1.com/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.jpg.transform/1col/image.jpg",
        "Charles Leclerc": "https://media.formula1.com/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.jpg.transform/1col/image.jpg",
        "Oscar Piastri": "https://media.formula1.com/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.jpg.transform/1col/image.jpg",
        "Lewis Hamilton": "https://media.formula1.com/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.jpg.transform/1col/image.jpg",
        "George Russell": "https://media.formula1.com/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.jpg.transform/1col/image.jpg",
        "Sergio Perez": "https://media.formula1.com/content/dam/fom-website/drivers/S/SERPER01_Sergio_Perez/serper01.jpg.transform/1col/image.jpg",
        "Fernando Alonso": "https://media.formula1.com/content/dam/fom-website/drivers/F/FERALO01_Fernando_Alonso/feralo01.jpg.transform/1col/image.jpg",
        "Carlos Sainz": "https://media.formula1.com/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.jpg.transform/1col/image.jpg",
        "Alexander Albon": "https://media.formula1.com/content/dam/fom-website/drivers/A/ALEALB01_Alexander_Albon/alealb01.jpg.transform/1col/image.jpg"
    }
    return driver_images

def add_youtube_video(video_id, title, caption):
    """Add YouTube video with custom styling"""
    st.markdown(f"""
    <div class="video-container" style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 100%); 
                border-radius: 15px; color: white;">
        <h4 style="margin-bottom: 15px; text-align: center;">{title}</h4>
        <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%;">
            <iframe src="<iframe width="1236" height="695" src="https://www.youtube.com/embed/daWr9xnkKS4" title="Race Highlights | 2025 British Grand Prix" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 10px;"
                    frameborder="0" allowfullscreen>
            </iframe>
        </div>
        <p style="margin-top: 15px; font-size: 0.9rem; text-align: center; opacity: 0.9;">{caption}</p>
    </div>
    """, unsafe_allow_html=True)

def show_f1_videos():
    """Display F1 videos section"""
    st.header("🎥 Formula 1 2025 Season Highlights")
    
    # Create tabs for different video categories
    video_tab1, video_tab2, video_tab3, video_tab4 = st.tabs(["🏁 Season Highlights", "🏆 Race Wins", "📈 Championship Battle", "🎯 Driver Focus"])
    
    with video_tab1:
        st.subheader("2025 Season Highlights")
        
        col1, col2 = st.columns(2)
        with col1:
            add_youtube_video("6nR6_NLQ6eg", "🏁 F1 2025 Season Opening", "Best moments from the season opener")
        with col2:
            add_youtube_video("43HKISQ73uk", "⚡ Overtakes of the Season", "Most spectacular overtaking maneuvers")
    
    with video_tab2:
        st.subheader("Legendary Race Wins")
        
        col1, col2 = st.columns(2)
        with col1:
            add_youtube_video("YiR3B2Jg7uQ", "🏆 Monaco GP 2025", "Classic street circuit action")
        with col2:
            add_youtube_video("lAILJ5kB4u8", "🚀 Silverstone GP 2025", "British GP thriller")
    
    with video_tab3:
        st.subheader("Championship Battle")
        add_youtube_video("zlW9mGHLWxs", "🥇 Championship Fight", "The battle for the 2025 World Championship")
    
    with video_tab4:
        st.subheader("Driver Spotlights")
        
        col1, col2 = st.columns(2)
        with col1:
            add_youtube_video("dQw4w9WgXcQ", "🌟 Max Verstappen", "Inside the mind of a champion")
        with col2:
            add_youtube_video("oHg5SJYRHA0", "🚀 Rising Stars", "The next generation of F1 talent")

def show_top_drivers_with_images(season_data, season_year):
    """Display top 5 drivers with their images and stats"""
    st.subheader(f"🏆 Top 5 Drivers - {season_year} Season")
    
    # Get top 5 drivers
    top_drivers = season_data.groupby('Driver')['Points'].sum().sort_values(ascending=False).head(5)
    driver_images = get_driver_images()
    
    # Create columns for driver cards
    cols = st.columns(5)
    
    for idx, (driver, points) in enumerate(top_drivers.items()):
        with cols[idx]:
            # Driver card with image
            st.markdown(f"""
            <div class="driver-card">
                <h4 style="text-align: center; margin-bottom: 15px;">#{idx+1}</h4>
                <h3 style="text-align: center; margin-bottom: 15px; font-size: 1.1rem;">{driver}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Try to display driver image
            if driver in driver_images:
                try:
                    st.image(driver_images[driver], width=120, use_column_width=False)
                except:
                    st.image("https://via.placeholder.com/120x120?text=F1", width=120)
            else:
                st.image("https://via.placeholder.com/120x120?text=F1", width=120)
            
            # Driver stats
            driver_data = season_data[season_data['Driver'] == driver]
            wins = len(driver_data[driver_data['Position'] == 1])
            podiums = len(driver_data[driver_data['Position'] <= 3])
            avg_pos = driver_data['Position'].mean()
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 15px; margin-top: -10px;">
                <div style="text-align: center; color: white;">
                    <h2 style="color: #FFD700; margin: 5px 0; font-size: 1.5rem;">{points:.0f} pts</h2>
                    <p style="margin: 3px 0; font-size: 0.9rem;"><strong>Wins:</strong> {wins}</p>
                    <p style="margin: 3px 0; font-size: 0.9rem;"><strong>Podiums:</strong> {podiums}</p>
                    <p style="margin: 3px 0; font-size: 0.9rem;"><strong>Avg Pos:</strong> {avg_pos:.1f}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_enhanced_overview(season_2024, season_2025):
    """Enhanced overview with videos and driver images"""
    add_bg_video()
    
    # F1 2025 Header with background video effect
    st.markdown("""
    <div style="position: relative; margin-bottom: 30px; background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 50%, #FF8A8A 100%); 
                border-radius: 20px; padding: 40px; text-align: center; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                    background: url('https://cdn.pixabay.com/photo/2017/08/07/14/02/formula-1-2604251_1280.jpg') center/cover; 
                    opacity: 0.2; z-index: 1;"></div>
        <div style="position: relative; z-index: 2;">
            <h1 class="main-header" style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
                🏎️ Formula 1 2025 Season Dashboard
            </h1>
            <p style="font-size: 1.3rem; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">
                Live Data Analysis & Race Insights
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h2 style="margin: 0; font-size: 2rem;">{}</h2>
            <p style="margin: 5px 0;">2024 Races</p>
        </div>
        """.format(len(season_2024['Track'].unique())), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h2 style="margin: 0; font-size: 2rem;">{}</h2>
            <p style="margin: 5px 0;">2025 Races</p>
        </div>
        """.format(len(season_2025['Track'].unique())), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h2 style="margin: 0; font-size: 2rem;">{}</h2>
            <p style="margin: 5px 0;">Total Drivers</p>
        </div>
        """.format(len(pd.concat([season_2024, season_2025])['Driver'].unique())), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <h2 style="margin: 0; font-size: 2rem;">{}</h2>
            <p style="margin: 5px 0;">Total Teams</p>
        </div>
        """.format(len(pd.concat([season_2024, season_2025])['Team'].unique())), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Championship leaders section
    st.header("🏆 Championship Leaders")
    col1, col2 = st.columns(2)
    
    with col1:
        leader_2024 = season_2024.groupby('Driver')['Points'].sum().idxmax()
        points_2024 = season_2024.groupby('Driver')['Points'].sum().max()
        st.success(f"**2024 Champion:** {leader_2024} ({points_2024:.0f} points)")
    
    with col2:
        leader_2025 = season_2025.groupby('Driver')['Points'].sum().idxmax()
        points_2025 = season_2025.groupby('Driver')['Points'].sum().max()
        st.success(f"**2025 Leader:** {leader_2025} ({points_2025:.0f} points)")
    
    # Featured video section
    st.header("🎥 Featured Video")
    add_youtube_video("6nR6_NLQ6eg", "🏁 F1 2025 Season Highlights", "The most thrilling moments from the current Formula 1 season")
    
    # Top drivers with images
    col1, col2 = st.columns(2)
    with col1:
        show_top_drivers_with_images(season_2024, 2024)
    with col2:
        show_top_drivers_with_images(season_2025, 2025)

def show_driver_analysis(season_2024, season_2025):
    """Driver performance analysis page"""
    add_bg_video()
    st.header("🏁 Driver Performance Analysis")
    
    # Driver selector
    all_drivers = pd.concat([season_2024, season_2025])['Driver'].unique()
    selected_drivers = st.multiselect("Select drivers to analyze:", all_drivers, default=list(all_drivers[:5]))
    
    if not selected_drivers:
        st.warning("Please select at least one driver")
        return
    
    # Points comparison
    st.subheader("📊 Points Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**2024 Season**")
        driver_points_2024 = season_2024[season_2024['Driver'].isin(selected_drivers)].groupby('Driver')['Points'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(range(len(driver_points_2024)), driver_points_2024.values, 
                       color=plt.cm.Set3(np.linspace(0, 1, len(driver_points_2024))))
        ax.set_yticks(range(len(driver_points_2024)))
        ax.set_yticklabels(driver_points_2024.index)
        ax.set_title('Driver Points - 2024 Season', fontsize=14, fontweight='bold')
        ax.set_xlabel('Total Points')
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.write("**2025 Season**")
        driver_points_2025 = season_2025[season_2025['Driver'].isin(selected_drivers)].groupby('Driver')['Points'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(range(len(driver_points_2025)), driver_points_2025.values, 
                       color=plt.cm.Set1(np.linspace(0, 1, len(driver_points_2025))))
        ax.set_yticks(range(len(driver_points_2025)))
        ax.set_yticklabels(driver_points_2025.index)
        ax.set_title('Driver Points - 2025 Season', fontsize=14, fontweight='bold')
        ax.set_xlabel('Total Points')
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Race wins comparison
    st.subheader("🏆 Race Wins Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        wins_2024 = season_2024[season_2024['Position'] == 1]['Driver'].value_counts()
        selected_wins_2024 = wins_2024[wins_2024.index.isin(selected_drivers)]
        
        if not selected_wins_2024.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(range(len(selected_wins_2024)), selected_wins_2024.values, color='gold', alpha=0.8)
            ax.set_xticks(range(len(selected_wins_2024)))
            ax.set_xticklabels(selected_wins_2024.index, rotation=45)
            ax.set_title('Race Wins - 2024 Season')
            ax.set_ylabel('Number of Wins')
            st.pyplot(fig)
            plt.close()
    
    with col2:
        wins_2025 = season_2025[season_2025['Position'] == 1]['Driver'].value_counts()
        selected_wins_2025 = wins_2025[wins_2025.index.isin(selected_drivers)]
        
        if not selected_wins_2025.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(range(len(selected_wins_2025)), selected_wins_2025.values, color='orange', alpha=0.8)
            ax.set_xticks(range(len(selected_wins_2025)))
            ax.set_xticklabels(selected_wins_2025.index, rotation=45)
            ax.set_title('Race Wins - 2025 Season')
            ax.set_ylabel('Number of Wins')
            st.pyplot(fig)
            plt.close()
    
    # Detailed statistics table
    st.subheader("📊 Detailed Driver Statistics")
    stats_data = []
    for driver in selected_drivers:
        for season, data in [("2024", season_2024), ("2025", season_2025)]:
            driver_data = data[data['Driver'] == driver]
            if not driver_data.empty:
                stats_data.append({
                    'Driver': driver,
                    'Season': season,
                    'Total Points': driver_data['Points'].sum(),
                    'Average Position': round(driver_data['Position'].mean(), 2),
                    'Wins': len(driver_data[driver_data['Position'] == 1]),
                    'Podiums': len(driver_data[driver_data['Position'] <= 3]),
                    'DNFs': len(driver_data[driver_data['Time/Retired'] == 'DNF']),
                    'Races': len(driver_data)
                })
    
    if stats_data:
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)

def show_team_analysis(season_2024, season_2025):
    """Team performance analysis"""
    add_bg_video()
    st.header("🏭 Team Performance Analysis")
    
    # Team points distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Team Points Distribution - 2024")
        team_points_2024 = season_2024.groupby('Team')['Points'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(team_points_2024)))
        wedges, texts, autotexts = ax.pie(team_points_2024.values, labels=team_points_2024.index, 
                                         autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title('Team Points Distribution - 2024', fontsize=16, fontweight='bold')
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Team Points Distribution - 2025")
        team_points_2025 = season_2025.groupby('Team')['Points'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        colors = plt.cm.Set1(np.linspace(0, 1, len(team_points_2025)))
        wedges, texts, autotexts = ax.pie(team_points_2025.values, labels=team_points_2025.index, 
                                         autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title('Team Points Distribution - 2025', fontsize=16, fontweight='bold')
        st.pyplot(fig)
        plt.close()
    
    # Podium comparison
    st.subheader("🏆 Podium Finishes by Team")
    col1, col2 = st.columns(2)
    
    with col1:
        podiums_2024 = season_2024[season_2024['Position'] <= 3]['Team'].value_counts()
        if not podiums_2024.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(podiums_2024.index, podiums_2024.values, color='mediumseagreen', alpha=0.8)
            ax.set_title('Podium Finishes by Team - 2024')
            ax.set_ylabel('Number of Podiums')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close()
    
    with col2:
        podiums_2025 = season_2025[season_2025['Position'] <= 3]['Team'].value_counts()
        if not podiums_2025.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(podiums_2025.index, podiums_2025.values, color='darkorange', alpha=0.8)
            ax.set_title('Podium Finishes by Team - 2025')
            ax.set_ylabel('Number of Podiums')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close()

def show_race_analysis(season_2024, season_2025):
    """Race analysis with track performance"""
    add_bg_video()
    st.header("🏁 Race Analysis")
    
    # Track performance analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Points Distribution by Track - 2024")
        track_points_2024 = season_2024.groupby('Track')['Points'].sum()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(range(len(track_points_2024)), track_points_2024.values, 'o-', 
                color='blue', linewidth=3, markersize=8)
        ax.set_title('Points Distribution by Track - 2024')
        ax.set_xlabel('Race Number')
        ax.set_ylabel('Total Points Awarded')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Points Distribution by Track - 2025")
        track_points_2025 = season_2025.groupby('Track')['Points'].sum()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(range(len(track_points_2025)), track_points_2025.values, 'o-', 
                color='red', linewidth=3, markersize=8)
        ax.set_title('Points Distribution by Track - 2025')
        ax.set_xlabel('Race Number')
        ax.set_ylabel('Total Points Awarded')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close()
    
    # DNF Analysis
    st.subheader("🔧 Reliability Analysis - DNF Count")
    col1, col2 = st.columns(2)
    
    with col1:
        dnf_2024 = season_2024[season_2024['Time/Retired'] == 'DNF']['Driver'].value_counts()
        if not dnf_2024.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(dnf_2024.index[:10], dnf_2024.values[:10], color='crimson', alpha=0.7)
            ax.set_title('DNF Count by Driver - 2024')
            ax.set_ylabel('Number of DNFs')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close()
    
    with col2:
        dnf_2025 = season_2025[season_2025['Time/Retired'] == 'DNF']['Driver'].value_counts()
        if not dnf_2025.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(dnf_2025.index[:10], dnf_2025.values[:10], color='darkred', alpha=0.7)
            ax.set_title('DNF Count by Driver - 2025')
            ax.set_ylabel('Number of DNFs')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close()

def show_track_analysis(season_2024, season_2025):
    """Track performance analysis"""
    add_bg_video()
    st.header("🏁 Track Performance Analysis")
    
    # Track characteristics
    st.subheader("🏎️ Track Characteristics Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Track Competitiveness - 2024**")
        track_spread_2024 = season_2024.groupby('Track')['Position'].std().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.bar(range(len(track_spread_2024)), track_spread_2024.values, color='skyblue', alpha=0.8)
        ax.set_xticks(range(len(track_spread_2024)))
        ax.set_xticklabels(track_spread_2024.index, rotation=45)
        ax.set_title('Track Competitiveness (Higher = More Unpredictable)')
        ax.set_ylabel('Position Standard Deviation')
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.write("**DNF Rates by Track - 2024**")
        dnf_by_track = season_2024[season_2024['Time/Retired'] == 'DNF'].groupby('Track').size()
        total_by_track = season_2024.groupby('Track').size()
        dnf_rates = (dnf_by_track / total_by_track * 100).fillna(0)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.bar(range(len(dnf_rates)), dnf_rates.values, color='red', alpha=0.7)
        ax.set_xticks(range(len(dnf_rates)))
        ax.set_xticklabels(dnf_rates.index, rotation=45)
        ax.set_title('DNF Rate by Track (%)')
        ax.set_ylabel('DNF Percentage')
        st.pyplot(fig)
        plt.close()

def show_advanced_analytics(season_2024, season_2025):
    """Advanced analytics with heatmaps and statistical analysis"""
    add_bg_video()
    st.header("📊 Advanced Analytics")
    
    # Driver consistency analysis
    st.subheader("📈 Driver Consistency Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Most Consistent Drivers 2024 (Lower = More Consistent)**")
        consistency_2024 = season_2024.groupby('Driver')['Position'].std().sort_values().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(range(len(consistency_2024)), consistency_2024.values, color='lightblue', alpha=0.8)
        ax.set_yticks(range(len(consistency_2024)))
        ax.set_yticklabels(consistency_2024.index)
        ax.set_title('Driver Consistency - 2024')
        ax.set_xlabel('Position Standard Deviation')
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.write("**Most Consistent Drivers 2025 (Lower = More Consistent)**")
        consistency_2025 = season_2025.groupby('Driver')['Position'].std().sort_values().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(range(len(consistency_2025)), consistency_2025.values, color='lightcoral', alpha=0.8)
        ax.set_yticks(range(len(consistency_2025)))
        ax.set_yticklabels(consistency_2025.index)
        ax.set_title('Driver Consistency - 2025')
        ax.set_xlabel('Position Standard Deviation')
        st.pyplot(fig)
        plt.close()
    
    # Performance heatmaps
    st.subheader("🔥 Performance Heatmaps")
    
    # Get top drivers for heatmap
    top_drivers_2024 = season_2024.groupby('Driver')['Points'].sum().sort_values(ascending=False).head(8)
    top_drivers_2025 = season_2025.groupby('Driver')['Points'].sum().sort_values(ascending=False).head(8)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Driver-Track Performance Matrix 2024**")
        driver_track_2024 = season_2024.pivot_table(values='Points', index='Driver', columns='Track', aggfunc='sum', fill_value=0)
        driver_track_2024_filtered = driver_track_2024.loc[driver_track_2024.index.isin(top_drivers_2024.index)]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(driver_track_2024_filtered, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'shrink': 0.8})
        ax.set_title('Driver Performance by Track - 2024 (Top 8 Drivers)')
        ax.set_ylabel('Driver')
        ax.set_xlabel('Track')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.write("**Driver-Track Performance Matrix 2025**")
        driver_track_2025 = season_2025.pivot_table(values='Points', index='Driver', columns='Track', aggfunc='sum', fill_value=0)
        driver_track_2025_filtered = driver_track_2025.loc[driver_track_2025.index.isin(top_drivers_2025.index)]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(driver_track_2025_filtered, annot=True, fmt='.0f', cmap='YlGnBu', ax=ax, cbar_kws={'shrink': 0.8})
        ax.set_title('Driver Performance by Track - 2025 (Top 8 Drivers)')
        ax.set_ylabel('Driver')
        ax.set_xlabel('Track')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        st.pyplot(fig)
        plt.close()
    
    # Position distribution analysis
    st.subheader("📊 Position Distribution Analysis")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Position histograms
    axes[0,0].hist(season_2024['Position'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0,0].set_title('Position Distribution - 2024')
    axes[0,0].set_xlabel('Finishing Position')
    axes[0,0].set_ylabel('Frequency')
    
    axes[0,1].hist(season_2025['Position'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
    axes[0,1].set_title('Position Distribution - 2025')
    axes[0,1].set_xlabel('Finishing Position')
    axes[0,1].set_ylabel('Frequency')
    
    # Combined data for analysis
    combined_data = pd.concat([season_2024[['Position', 'Points', 'Season']], 
                              season_2025[['Position', 'Points', 'Season']]])
    top_10_positions = combined_data[combined_data['Position'] <= 10]
    
    # Boxplot
    sns.boxplot(data=top_10_positions, x='Position', y='Points', hue='Season', ax=axes[1,0])
    axes[1,0].set_title('Points Distribution by Position (Top 10)')
    axes[1,0].set_xlabel('Finishing Position')
    axes[1,0].set_ylabel('Points Scored')
    
    # Scatter plot - Starting Grid vs Position
    axes[1,1].scatter(season_2024['Starting Grid'], season_2024['Position'], 
                      alpha=0.6, color='blue', label='2024', s=30)
    axes[1,1].scatter(season_2025['Starting Grid'], season_2025['Position'], 
                      alpha=0.6, color='red', label='2025', s=30)
    axes[1,1].set_title('Starting Grid vs Finishing Position')
    axes[1,1].set_xlabel('Starting Grid Position')
    axes[1,1].set_ylabel('Finishing Position')
    axes[1,1].legend()
    axes[1,1].plot([1, 20], [1, 20], 'k--', alpha=0.5)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Summary statistics
    st.subheader("📊 Championship Summary")
    
    season_stats = pd.DataFrame({
        '2024 Season': [
            len(season_2024['Track'].unique()),
            len(season_2024['Driver'].unique()),
            len(season_2024['Team'].unique()),
            season_2024[season_2024['Position'] == 1]['Driver'].value_counts().iloc[0] if not season_2024[season_2024['Position'] == 1].empty else 0,
            season_2024[season_2024['Position'] == 1]['Driver'].value_counts().index[0] if not season_2024[season_2024['Position'] == 1].empty else 'N/A',
            season_2024.groupby('Driver')['Points'].sum().max(),
            season_2024.groupby('Driver')['Points'].sum().idxmax()
        ],
        '2025 Season': [
            len(season_2025['Track'].unique()),
            len(season_2025['Driver'].unique()),
            len(season_2025['Team'].unique()),
            season_2025[season_2025['Position'] == 1]['Driver'].value_counts().iloc[0] if not season_2025[season_2025['Position'] == 1].empty else 0,
            season_2025[season_2025['Position'] == 1]['Driver'].value_counts().index[0] if not season_2025[season_2025['Position'] == 1].empty else 'N/A',
            season_2025.groupby('Driver')['Points'].sum().max(),
            season_2025.groupby('Driver')['Points'].sum().idxmax()
        ]
    }, index=['Total Races', 'Total Drivers', 'Total Teams', 'Most Wins Count', 
              'Most Wins Driver', 'Highest Points', 'Points Leader'])
    
    st.dataframe(season_stats, use_container_width=True)

def main():
    """Main application function"""
    # Load data
    season_2024, season_2025 = load_and_clean_data()
    
    if season_2024 is None or season_2025 is None:
        st.error("⚠️ Please ensure your CSV files are uploaded or in the correct directory")
        st.info("Expected files: Formula1_2024season_raceResults.csv and Formula1_2025Season_RaceResults.csv")
        return
    
    # Sidebar navigation
    st.sidebar.markdown("## 📊 Navigation")
    st.sidebar.markdown("---")
    
    analysis_option = st.sidebar.selectbox(
        "Choose Analysis Section:",
        ["📈 Enhanced Overview", "🏁 Driver Performance", "🏭 Team Analysis", 
         "🏁 Race Analysis", "🏁 Track Performance", "📊 Advanced Analytics", "🎥 Video Gallery"],
        help="Select different sections to explore F1 data"
    )
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏎️ Dashboard Features")
    st.sidebar.markdown("""
    - **Live Data Analysis** - Real-time F1 statistics
    - **Interactive Visualizations** - Dynamic charts and graphs  
    - **Driver Profiles** - Detailed performance metrics
    - **Video Highlights** - Season's best moments
    - **Advanced Analytics** - Deep statistical insights
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🏆 Formula 1 2025 Season Dashboard**")
    st.sidebar.markdown("*Built with Streamlit*")
    
    # Navigation routing
    if analysis_option == "📈 Enhanced Overview":
        show_enhanced_overview(season_2024, season_2025)
    elif analysis_option == "🎥 Video Gallery":
        show_f1_videos()
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

if __name__ == "__main__":
    main()

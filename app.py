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
    
    .educational-card {
        background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.3);
    }
    
    .term-card {
        background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    
    .term-card:hover {
        transform: translateY(-3px);
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
    
    .stSelectbox > div > div {
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def get_enhanced_driver_images():
    """Return comprehensive dictionary of driver images with team info"""
    driver_images = {
        "Max Verstappen": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.jpg.transform/1col/image.jpg",
            "team": "Red Bull Racing",
            "nationality": "Dutch",
            "number": "1",
            "championships": "3"
        },
        "Lando Norris": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.jpg.transform/1col/image.jpg",
            "team": "McLaren",
            "nationality": "British",
            "number": "4",
            "championships": "0"
        },
        "Charles Leclerc": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.jpg.transform/1col/image.jpg",
            "team": "Ferrari",
            "nationality": "Monégasque",
            "number": "16",
            "championships": "0"
        },
        "Oscar Piastri": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.jpg.transform/1col/image.jpg",
            "team": "McLaren",
            "nationality": "Australian",
            "number": "81",
            "championships": "0"
        },
        "Lewis Hamilton": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.jpg.transform/1col/image.jpg",
            "team": "Ferrari",  # 2025 move to Ferrari
            "nationality": "British",
            "number": "44",
            "championships": "7"
        },
        "George Russell": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.jpg.transform/1col/image.jpg",
            "team": "Mercedes",
            "nationality": "British",
            "number": "63",
            "championships": "0"
        },
        "Sergio Perez": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/S/SERPER01_Sergio_Perez/serper01.jpg.transform/1col/image.jpg",
            "team": "Red Bull Racing",
            "nationality": "Mexican",
            "number": "11",
            "championships": "0"
        },
        "Fernando Alonso": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/F/FERALO01_Fernando_Alonso/feralo01.jpg.transform/1col/image.jpg",
            "team": "Aston Martin",
            "nationality": "Spanish",
            "number": "14",
            "championships": "2"
        },
        "Carlos Sainz": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.jpg.transform/1col/image.jpg",
            "team": "Williams",  # 2025 move to Williams
            "nationality": "Spanish",
            "number": "55",
            "championships": "0"
        },
        "Alexander Albon": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/A/ALEALB01_Alexander_Albon/alealb01.jpg.transform/1col/image.jpg",
            "team": "Williams",
            "nationality": "Thai",
            "number": "23",
            "championships": "0"
        },
        "Nico Hulkenberg": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/N/NICHUL01_Nico_Hulkenberg/nichul01.jpg.transform/1col/image.jpg",
            "team": "Haas",
            "nationality": "German",
            "number": "27",
            "championships": "0"
        },
        "Pierre Gasly": {
            "image": "https://media.formula1.com/content/dam/fom-website/drivers/P/PIEGAS01_Pierre_Gasly/piegas01.jpg.transform/1col/image.jpg",
            "team": "Alpine",
            "nationality": "French",
            "number": "10",
            "championships": "0"
        }
    }
    return driver_images

def add_local_video(video_path, title, caption):
    """Add local video with custom styling"""
    try:
        # Read video file
        with open(video_path, 'rb') as video_file:
            video_bytes = video_file.read()
        
        # Create styled container
        st.markdown(f"""
        <div class="video-container" style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 100%); 
                    border-radius: 15px; color: white;">
            <h4 style="margin-bottom: 15px; text-align: center;">{title}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display video using Streamlit's native function
        st.video(video_bytes)
        
        # Add caption
        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <p style="font-size: 0.9rem; color: #666; opacity: 0.9;">{caption}</p>
        </div>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error(f"❌ Video file not found: {video_path}")
        st.info("💡 Please ensure the video file exists at the specified path")
    except Exception as e:
        st.error(f"❌ Error loading video: {str(e)}")

def add_youtube_video(video_id, title, caption):
    """Add YouTube video with custom styling"""
    st.markdown(f"""
    <div class="video-container" style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 100%); 
                border-radius: 15px; color: white;">
        <h4 style="margin-bottom: 15px; text-align: center;">{title}</h4>
        <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%;">
            <iframe src="https://www.youtube.com/embed/{video_id}" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 10px;"
                    frameborder="0" allowfullscreen>
            </iframe>
        </div>
        <p style="margin-top: 15px; font-size: 0.9rem; text-align: center; opacity: 0.9;">{caption}</p>
    </div>
    """, unsafe_allow_html=True)

# F1 EDUCATIONAL CONTENT FUNCTIONS

def show_f1_basics():
    """Educational section about Formula 1 for beginners"""
    add_bg_video()
    
    # Main header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 50%, #FF8A8A 100%); 
                border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 30px;">
        <h1 style="color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
            🏎️ Welcome to Formula 1
        </h1>
        <p style="color: white; font-size: 1.2rem; margin: 10px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">
            Your Complete Guide to the World's Premier Racing Championship
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["🏁 What is F1?", "🔧 Technical Terms", "🏎️ Pitstops & Strategy", "🏆 Championship System"])
    
    with tab1:
        show_what_is_f1()
    
    with tab2:
        show_technical_terms()
    
    with tab3:
        show_pitstop_strategy()
    
    with tab4:
        show_championship_system()

def show_what_is_f1():
    """Explain what Formula 1 is"""
    st.header("🏁 What is Formula 1?")
    
    # Main explanation with image
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Formula 1 (F1)** is the highest class of international racing for open-wheel single-seater formula racing cars. 
        It's considered the pinnacle of motorsport, featuring:
        
        ### Key Features:
        - **20 Drivers** competing across 10 teams
        - **Race Weekends** held on circuits around the world
        - **Speeds** reaching over 300 km/h (186 mph)
        - **Advanced Technology** with hybrid power units
        - **Global Championship** with races from March to December
        
        ### What Makes F1 Special:
        - **Engineering Excellence**: Cars cost millions and use cutting-edge technology
        - **Driver Skill**: Only the world's best drivers compete
        - **Strategy**: Teams must balance speed, tire wear, and fuel consumption
        - **Teamwork**: Success requires perfect coordination between driver, engineers, and pit crew
        """)
    
    with col2:
        # F1 car image
        st.image("https://cdn.pixabay.com/photo/2017/08/07/14/02/formula-1-2604251_1280.jpg", 
                caption="Formula 1 Racing Car", use_column_width=True)
    
    # Race weekend structure
    st.subheader("🏁 Race Weekend Structure")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="educational-card" style="background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);">
            <h3>🚗 Practice Sessions</h3>
            <p><strong>Friday:</strong> FP1 & FP2</p>
            <p><strong>Saturday:</strong> FP3</p>
            <p>Drivers learn the track and test car setups</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="educational-card" style="background: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%);">
            <h3>⏱️ Qualifying</h3>
            <p><strong>Saturday:</strong> Q1, Q2, Q3</p>
            <p>Determines starting grid positions for Sunday's race</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="educational-card" style="background: linear-gradient(135deg, #F44336 0%, #EF5350 100%);">
            <h3>🏆 Race Day</h3>
            <p><strong>Sunday:</strong> The Main Event</p>
            <p>Points awarded to top 10 finishers</p>
        </div>
        """, unsafe_allow_html=True)

def show_technical_terms():
    """Explain key F1 technical terms"""
    st.header("🔧 Essential F1 Technical Terms")
    
    # Technical terms with explanations and images
    terms = [
        {
            "term": "DRS (Drag Reduction System)",
            "definition": "A movable rear wing that reduces drag and increases top speed on straights",
            "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500",
            "usage": "Used in designated DRS zones when within 1 second of the car ahead"
        },
        {
            "term": "Pole Position",
            "definition": "Starting position for the fastest qualifier - first place on the starting grid",
            "image": "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=500",
            "usage": "Awarded to the driver with the fastest lap time in Q3"
        },
        {
            "term": "Fastest Lap",
            "definition": "Bonus point awarded to the driver who sets the fastest lap time during the race",
            "image": "https://images.unsplash.com/photo-1566473965997-3de9c817e938?w=500",
            "usage": "Must finish in the top 10 to receive the bonus point"
        },
        {
            "term": "Safety Car",
            "definition": "A car that leads the field at reduced speed during dangerous conditions",
            "image": "https://images.unsplash.com/photo-1558618047-3c80ac1b90b8?w=500",
            "usage": "Deployed when there's an accident or debris on track"
        }
    ]
    
    for i, term_info in enumerate(terms):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(term_info["image"], caption=term_info["term"], use_column_width=True)
        
        with col2:
            st.markdown(f"""
            <div class="term-card">
                <h3>{term_info["term"]}</h3>
                <p><strong>What it is:</strong> {term_info["definition"]}</p>
                <p><strong>How it's used:</strong> {term_info["usage"]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if i < len(terms) - 1:
            st.markdown("---")

def show_pitstop_strategy():
    """Explain pitstops and strategy"""
    st.header("🏎️ Pitstops & Race Strategy")
    
    # Pitstop explanation
    st.subheader("🔧 What is a Pitstop?")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        A **pitstop** is when a driver enters the pit lane to:
        - **Change tires** (mandatory at least once per race)
        - **Refuel** (not allowed since 2010)
        - **Fix damage** or adjust car settings
        - **Serve penalties** if required
        
        ### The Famous "Box Box" Call:
        - **"Box, box, box"** is the radio call telling a driver to enter the pits
        - **Why "box"?** It comes from the German word "Boxenstopp" (pit stop)
        - **Timing is crucial** - teams must decide the perfect moment to pit
        
        ### Pitstop Records:
        - **Fastest pitstop**: Under 2 seconds for a tire change
        - **Typical time**: 2.5-3.5 seconds
        - **Crew members**: Up to 20 people work on the car
        """)
    
    with col2:
        # Pitstop image
        st.image("https://images.unsplash.com/photo-1558618523-413c03c8ee91?w=500", 
                caption="F1 Pitstop in Action", use_column_width=True)
    
    # Strategy types
    st.subheader("🎯 Race Strategy Types")
    
    strategies = [
        {
            "name": "One-Stop Strategy",
            "description": "Start on harder tires, pit once for softer tires",
            "pros": "Less time lost in pits, track position advantage",
            "cons": "Tires may degrade significantly at the end"
        },
        {
            "name": "Two-Stop Strategy", 
            "description": "Make two pitstops with fresher tires for each stint",
            "pros": "Always have relatively fresh tires",
            "cons": "More time lost in pits, need to overtake more"
        },
        {
            "name": "Undercut Strategy",
            "description": "Pit before your rival to gain track position",
            "pros": "Fresh tires give pace advantage",
            "cons": "Risk if the gap isn't big enough"
        },
        {
            "name": "Overcut Strategy",
            "description": "Stay out longer than rivals before pitting",
            "pros": "Use tire advantage after others pit",
            "cons": "Risk of tire degradation"
        }
    ]
    
    cols = st.columns(2)
    
    for i, strategy in enumerate(strategies):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="term-card">
                <h4>{strategy["name"]}</h4>
                <p><strong>Strategy:</strong> {strategy["description"]}</p>
                <p><strong>✅ Pros:</strong> {strategy["pros"]}</p>
                <p><strong>❌ Cons:</strong> {strategy["cons"]}</p>
            </div>
            """, unsafe_allow_html=True)

def show_championship_system():
    """Explain the championship points system"""
    st.header("🏆 Championship Points System")
    
    # Points explanation
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### How Points Are Awarded:
        
        F1 uses a **points-based championship system** where:
        - **Only the top 10 finishers** score points in each race
        - **Consistency is key** - regular points finishes matter more than occasional wins
        - **Two championships** are awarded: Drivers' and Constructors' (Teams)
        """)
        
        # Points table
        points_data = {
            'Position': ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'],
            'Points': [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
        }
        points_df = pd.DataFrame(points_data)
        st.dataframe(points_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.image("https://images.unsplash.com/photo-1584464491274-d8427f386c19?w=500", 
                caption="Championship Trophy", use_column_width=True)
    
    # Additional points
    st.subheader("🎯 Bonus Points")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="educational-card" style="background: linear-gradient(135deg, #FFD700 0%, #FFF176 100%); color: black;">
            <h4>🏁 Fastest Lap</h4>
            <h2>+1 Point</h2>
            <p>Must finish in top 10</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="educational-card" style="background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);">
            <h4>🏁 Sprint Race</h4>
            <h2>Points Available</h2>
            <p>8-7-6-5-4-3-2-1 for top 8</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="educational-card" style="background: linear-gradient(135deg, #FF5722 0%, #FF8A65 100%);">
            <h4>🏁 Sprint Shootout</h4>
            <h2>Pole Position</h2>
            <p>Determines sprint grid</p>
        </div>
        """, unsafe_allow_html=True)

# VIDEO FUNCTIONS

def show_f1_videos():
    """Display F1 videos section with local and YouTube videos"""
    st.header("🎥 Formula 1 2025 Season Highlights")
    
    # Local video section - Featured video using your F1.mp4
    st.subheader("🏆 Featured: Your F1 Race Highlights")
    add_local_video("Videos/F1.mp4", "🏁 F1 2025 Exclusive Highlights", "Your personal F1 race footage - The most thrilling moments captured!")
    
    # Create tabs for different video categories
    video_tab1, video_tab2, video_tab3, video_tab4 = st.tabs(["🏁 Season Highlights", "🏆 Race Wins", "📈 Championship Battle", "🎯 Driver Focus"])
    
    with video_tab1:
        st.subheader("2025 Season Best Moments")
        
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

# DRIVER PROFILE FUNCTIONS

def show_enhanced_driver_profiles(season_data, season_year):
    """Enhanced driver profiles with detailed information"""
    st.subheader(f"🏆 Driver Profiles - {season_year} Season")
    
    # Get top 10 drivers
    top_drivers = season_data.groupby('Driver')['Points'].sum().sort_values(ascending=False).head(10)
    enhanced_driver_images = get_enhanced_driver_images()
    
    # Display in rows of 5
    for row in range(0, len(top_drivers), 5):
        cols = st.columns(5)
        drivers_in_row = list(top_drivers.items())[row:row+5]
        
        for idx, (driver, points) in enumerate(drivers_in_row):
            with cols[idx]:
                driver_info = enhanced_driver_images.get(driver, {})
                
                # Enhanced driver card
                st.markdown(f"""
                <div class="driver-card">
                    <div style="text-align: center;">
                        <h4 style="margin-bottom: 10px;">#{row + idx + 1} • #{driver_info.get('number', 'N/A')}</h4>
                        <h3 style="margin-bottom: 15px; font-size: 1.1rem;">{driver}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Driver image
                if driver_info.get('image'):
                    try:
                        st.image(driver_info['image'], width=120, use_column_width=False)
                    except:
                        st.image("https://via.placeholder.com/120x120?text=F1", width=120)
                else:
                    st.image("https://via.placeholder.com/120x120?text=F1", width=120)
                
                # Driver stats and info
                driver_data = season_data[season_data['Driver'] == driver]
                wins = len(driver_data[driver_data['Position'] == 1])
                podiums = len(driver_data[driver_data['Position'] <= 3])
                avg_pos = driver_data['Position'].mean()
                
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.15); border-radius: 15px; 
                                padding: 15px; margin-top: -10px;">
                        <div style="text-align: center;">
                            <p style="margin: 3px 0; font-size: 0.9rem;">
                                <strong>🏁 Team:</strong> {driver_info.get('team', 'Unknown')}
                            </p>
                            <p style="margin: 3px 0; font-size: 0.9rem;">
                                <strong>🌍 Country:</strong> {driver_info.get('nationality', 'Unknown')}
                            </p>
                            <p style="margin: 3px 0; font-size: 0.9rem;">
                                <strong>🏆 Championships:</strong> {driver_info.get('championships', '0')}
                            </p>
                            <hr style="margin: 10px 0; opacity: 0.3;">
                            <h2 style="color: #FFD700; margin: 8px 0; font-size: 1.5rem;">{points:.0f} pts</h2>
                            <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                                <span><strong>Wins:</strong> {wins}</span>
                                <span><strong>Podiums:</strong> {podiums}</span>
                                <span><strong>Avg:</strong> {avg_pos:.1f}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# MAIN DASHBOARD FUNCTIONS

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
        st.markdown(f"""
        <div class="metric-container">
            <h2 style="margin: 0; font-size: 2rem;">{len(season_2024['Track'].unique())}</h2>
            <p style="margin: 5px 0;">2024 Races</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h2 style="margin: 0; font-size: 2rem;">{len(season_2025['Track'].unique())}</h2>
            <p style="margin: 5px 0;">2025 Races</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h2 style="margin: 0; font-size: 2rem;">{len(pd.concat([season_2024, season_2025])['Driver'].unique())}</h2>
            <p style="margin: 5px 0;">Total Drivers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h2 style="margin: 0; font-size: 2rem;">{len(pd.concat([season_2024, season_2025])['Team'].unique())}</h2>
            <p style="margin: 5px 0;">Total Teams</p>
        </div>
        """, unsafe_allow_html=True)
    
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
    
    # Featured video section with local video
    st.header("🎥 Featured Video Highlight")
    add_local_video("Videos/F1.mp4", "🏁 Your F1 2025 Exclusive Footage", 
                    "Your personal F1 highlights - witness the excitement of the 2025 season!")
    
    # Enhanced driver profiles
    col1, col2 = st.columns(2)
    with col1:
        show_enhanced_driver_profiles(season_2024, 2024)
    with col2:
        show_enhanced_driver_profiles(season_2025, 2025)

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

# MAIN APPLICATION FUNCTION

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
        ["📈 Enhanced Overview", "📚 F1 Basics Guide", "🏁 Driver Performance", "🏭 Team Analysis", 
         "🏁 Race Analysis", "🏁 Track Performance", "📊 Advanced Analytics", "🎥 Video Gallery"],
        help="Select different sections to explore F1 data"
    )
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏎️ Dashboard Features")
    st.sidebar.markdown("""
    - **📚 F1 Basics Guide** - Perfect for newcomers to F1
    - **📈 Live Data Analysis** - Real-time F1 statistics  
    - **🏆 Driver Profiles** - Detailed performance with photos
    - **🎥 Video Highlights** - Your local F1 footage + online content
    - **📊 Advanced Analytics** - Deep statistical insights
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔰 New to Formula 1?")
    st.sidebar.markdown("""
    Start with the **F1 Basics Guide** to learn:
    - What is Formula 1?
    - Technical terms explained
    - Pitstop strategies ("Box Box!")
    - Championship system
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🏆 Formula 1 2025 Season Dashboard**")
    st.sidebar.markdown("*Built with Streamlit*")
    
    # Navigation routing
    if analysis_option == "📈 Enhanced Overview":
        show_enhanced_overview(season_2024, season_2025)
    elif analysis_option == "📚 F1 Basics Guide":
        show_f1_basics()
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

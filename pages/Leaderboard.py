import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd

st.set_page_config(page_title="RedactaRAG Leaderboard", layout="wide")

# Initialize connection
conn = st.connection("supabase", type=SupabaseConnection)

st.logo("monogram.png", size='large')

st.title("🏆 RedactaRAG Hall of Fame")

# 1. Fetch Data
try:
    # We pull the data from Supabase
    # Fetch data: Sort by Level (Descending), then by Time (Ascending)
    res = conn.table("leaderboard") \
        .select("user_name, high_score, last_played") \
        .order("high_score", desc=True) \
        .order("last_played", desc=False) \
        .limit(10) \
        .execute()
    
    
    if res.data:
        # Convert to DataFrame for easy formatting
        df = pd.DataFrame(res.data)
        
        # 2. Format the Timestamp
        # Convert to datetime objects and format (e.g., "May 14, 02:30 PM")
        # df['last_played'] = pd.to_datetime(df['last_played']).dt.strftime('%b %d, %I:%M %p')
        df['last_played'] = pd.to_datetime(df['last_played'], utc=True).dt.tz_convert('America/Denver').dt.strftime('%b %d, %I:%M %p')
        
        # 3. Rename columns for the UI
        df.columns = ["Name", "Highest Level Beaten", "Time Beaten"]
        
        # 4. Display the Table
        # Use st.dataframe for an interactive table or st.table for a static one
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Highest Level Reached": st.column_config.NumberColumn(
                    format="Level %d 🛡️"
                )
            }
        )
        
        # Fun Stats
        st.divider()
 
    else:
        st.info("The leaderboard is currently empty. Be the first to break the system!")

except Exception as e:
    st.error("Could not load the scoreboard. Please try again later.")
    # st.write(e) # Uncomment for debugging

try:
    chats = conn.table("chat_history") \
    .select("level, is_success") \
    .execute()
    
    if chats.data:

        cdf = pd.DataFrame(chats.data)
        cdf['is_success'] = cdf['is_success'].astype(str).str.upper() == "TRUE"

        level_stats = cdf.groupby("level")['is_success'].agg(
            success_rate = 'mean',
            total_successes = 'sum',
            total_attempts = 'count'
        ).reset_index()

        cols = st.columns(4)
        level_stats2 = level_stats.set_index('level')
        for i, col in enumerate(cols):
            if i+1 in level_stats2.index:
                lvl1_data = level_stats2.loc[i+1]
                attempts = int(lvl1_data['total_attempts']/2)
                success_rate = f"{lvl1_data['success_rate']:.1%}"
            else:
                attempts = 0
                success_rate = "0.0%"

            col.metric(
                label=f"""Level {i+1} Success Rate 

{attempts} attempts""",
                value= success_rate
            )

        st.bar_chart(level_stats, x="level", y='success_rate', x_label="Level", y_label="Success Rate", )

except Exception as e:
    st.text(e)


with st.sidebar:
    st.markdown("**Access the app by scanning this QR code!**")
    st.image("qr.png")
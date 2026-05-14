import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd

st.set_page_config(page_title="RedactaRAG Leaderboard", layout="wide")

# Initialize connection
conn = st.connection("supabase", type=SupabaseConnection)

st.title("🏆 RedactaRAG Hall of Fame")
st.markdown("Check out who has successfully bypassed each system!")

# 1. Fetch Data
try:
    # We pull the data from Supabase
    # Fetch data: Sort by Level (Descending), then by Time (Ascending)
    res = conn.table("leaderboard") \
        .select("user_name, high_score, last_played") \
        .order("high_score", desc=True) \
        .order("last_played", desc=False) \
        .execute()
    
    if res.data:
        # Convert to DataFrame for easy formatting
        df = pd.DataFrame(res.data)
        
        # 2. Format the Timestamp
        # Convert to datetime objects and format (e.g., "May 14, 02:30 PM")
        df['last_played'] = pd.to_datetime(df['last_played']).dt.strftime('%b %d, %I:%M %p')
        
        # 3. Rename columns for the UI
        df.columns = ["Name", "Highest Level Beaten", "Last Attempt"]
        
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
        col1, col2 = st.columns(2)
        col1.metric("Total Players", len(df))
        col2.metric("Highest Level Beaten", f"Level {df['Highest Level Beaten'].max()} / 3")

    else:
        st.info("The leaderboard is currently empty. Be the first to break the system!")

except Exception as e:
    st.error("Could not load the scoreboard. Please try again later.")
    # st.write(e) # Uncomment for debugging
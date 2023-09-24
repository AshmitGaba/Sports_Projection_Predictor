import streamlit as st
import pandas as pd

# Load the dataset
data = pd.read_csv('NBA Player Box Score Stats(1950 - 2022).csv')

# Function to fetch player stats against a specific team
def get_player_stats(player_name, team_name, latest_team_only=True):
    player_data = data[(data['PLAYER_NAME'] == player_name) & (data['MATCHUP'].str.contains(team_name))]
    
    if latest_team_only:
        latest_team = player_data['Team'].iloc[0]
        player_data = player_data[player_data['Team'] == latest_team]
    
    if player_data.empty:
        return None, None, None, None, None, None
    
    avg_points = player_data['PTS'].mean()
    avg_rebounds = player_data['REB'].mean()
    avg_assists = player_data['AST'].mean()
    avg_steals = player_data['STL'].mean()
    avg_turnovers = player_data['TOV'].mean()
    avg_ftm = player_data['FTM'].mean()
    
    return avg_points, avg_rebounds, avg_assists, avg_steals, avg_turnovers, avg_ftm

# Streamlit app
st.title("NBA Player Performance Predictor")

# Player suggestions
player_list = sorted(data['PLAYER_NAME'].dropna().unique().tolist())
player_name = st.selectbox("Select Player Name:", player_list)

# Opponent team suggestions
team_values = data['MATCHUP'].str.extract(r'vs. (\w+)')[0].dropna().unique().tolist()
team_list = sorted([team for team in team_values if isinstance(team, str)])
team_name = st.selectbox("Select Opponent Team:", team_list)

# Option for latest team only or all-time
latest_team_only = st.radio("Stats from:", ("Latest Team Only", "All Time")) == "Latest Team Only"

if st.button('Predict'):
    avg_points, avg_rebounds, avg_assists, avg_steals, avg_turnovers, avg_ftm = get_player_stats(player_name, team_name, latest_team_only)
    
    if avg_points is None:
        st.write(f"Error: {player_name} hasn't played against {team_name} in the dataset.")
    else:
        st.write(f"**Projected Points**: {avg_points:.2f}")
        st.write(f"**Projected Rebounds**: {avg_rebounds:.2f}")
        st.write(f"**Projected Assists**: {avg_assists:.2f}")
        st.write(f"**Projected Steals**: {avg_steals:.2f}")
        st.write(f"**Projected Turnovers**: {avg_turnovers:.2f}")
        st.write(f"**Projected Free Throws Made**: {avg_ftm:.2f}")

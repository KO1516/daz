import pandas as pd
import plotly.express as px

# Load the enriched dataset
df = pd.read_csv("games_dataset_enriched_with_steam.csv")

# Drop missing ratings for meaningful visualizations
df = df.dropna(subset=['User Rating', 'Platform', 'Genre'])

# Chart 1: User Rating Distribution
fig1 = px.histogram(df, x="User Rating", nbins=20, title="User Rating Distribution")

# Chart 2: Top 10 Genres by Count
top_genres = df['Genre'].value_counts().nlargest(10).reset_index()
top_genres.columns = ['Genre', 'Count']
fig2 = px.bar(top_genres, x='Genre', y='Count', title="Top 10 Genres by Count")

# Chart 3: Average Rating by Platform
avg_rating_platform = df.groupby('Platform')['User Rating'].mean().sort_values(ascending=False).reset_index()
fig3 = px.bar(avg_rating_platform, x='Platform', y='User Rating', title="Average Rating by Platform")

# Chart 4: Average Rating by Genre
avg_rating_genre = df.groupby('Genre')['User Rating'].mean().sort_values(ascending=False).head(10).reset_index()
fig4 = px.bar(avg_rating_genre, x='Genre', y='User Rating', title="Top Genres by Average Rating")

# Show plots
fig1.show()
fig2.show()
fig3.show()
fig4.show()
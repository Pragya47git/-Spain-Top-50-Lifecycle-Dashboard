import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Spain Top 50 Lifecycle Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1rem;
}
[data-testid="stMetric"] {
    background: #f7f9fc;
    border: 1px solid #e6eaf2;
    padding: 14px 16px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #102a43;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    life = pd.read_csv("song_lifecycle_metrics.csv", parse_dates=["entry_date", "exit_date", "peak_date"])
    stage = pd.read_csv("daily_stage_classification.csv", parse_dates=["date"])
    churn = pd.read_csv("daily_churn_metrics.csv", parse_dates=["date"])
    monthly = pd.read_csv("monthly_churn_metrics.csv")
    kpi = pd.read_csv("kpi_summary.csv")
    return life, stage, churn, monthly, kpi

life, stage, churn, monthly, kpi = load_data()

life["album_type"] = life["album_type"].astype(str).str.title()
stage["album_type"] = stage["album_type"].astype(str).str.title()
life["explicit_label"] = np.where(life["is_explicit"] == True, "Explicit", "Clean")
stage["explicit_label"] = np.where(stage["is_explicit"] == True, "Explicit", "Clean")
stage["month"] = stage["date"].dt.to_period("M").astype(str)

st.title("Spain Top 50 Songs — Content Maturity & Playlist Rotation")
st.caption("Atlantic Recording Corporation | Spain market lifecycle intelligence dashboard")

with st.sidebar:
    st.header("Filters")
    min_date = stage["date"].min().date()
    max_date = stage["date"].max().date()

    start_date, end_date = st.slider(
        "Date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    explicit_filter = st.selectbox("Explicit content", ["All", "Explicit", "Clean"])
    album_options = ["All"] + sorted([x for x in life["album_type"].dropna().unique().tolist() if x != "Nan"])
    album_filter = st.selectbox("Album type", album_options)

    min_days, max_days = int(life["days_on_playlist"].min()), int(life["days_on_playlist"].max())
    days_range = st.slider("Days on playlist", min_days, max_days, (min_days, max_days))

    st.markdown("---")
    st.markdown("### Dataset snapshot")
    st.write(f"Songs: {life['song_key'].nunique():,}")
    st.write(f"Daily rows: {stage.shape[0]:,}")
    st.write(f"Coverage: {min_date} to {max_date}")

stage_f = stage[(stage["date"].dt.date >= start_date) & (stage["date"].dt.date <= end_date)].copy()
life_f = life[(life["days_on_playlist"] >= days_range[0]) & (life["days_on_playlist"] <= days_range[1])].copy()

if explicit_filter != "All":
    stage_f = stage_f[stage_f["explicit_label"] == explicit_filter]
    life_f = life_f[life_f["explicit_label"] == explicit_filter]

if album_filter != "All":
    stage_f = stage_f[stage_f["album_type"] == album_filter]
    life_f = life_f[life_f["album_type"] == album_filter]

if life_f.empty or stage_f.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

avg_days = round(life_f["days_on_playlist"].mean(), 2)
median_days = round(life_f["days_on_playlist"].median(), 2)
avg_peak_time = round(life_f["entry_to_peak_days"].mean(), 2)
top10_conversion = round(life_f["peak_position"].le(10).mean() * 100, 2)
reentry_rate = round((life_f["reentry_count"] > 0).mean() * 100, 2)
avg_stability = round(life_f["retention_stability_index"].mean(), 3)

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Avg Days", avg_days)
m2.metric("Median Days", median_days)
m3.metric("Entry to Peak", avg_peak_time)
m4.metric("Top 10 Conversion", f"{top10_conversion}%")
m5.metric("Re-entry Rate", f"{reentry_rate}%")
m6.metric("Stability Index", avg_stability)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Lifecycle",
    "Rotation",
    "Comparisons",
    "Song Deep Dive"
])

with tab1:
    st.subheader("Portfolio overview")
    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            life_f,
            x="days_on_playlist",
            nbins=35,
            title="Distribution of Days on Playlist",
            color_discrete_sequence=["#3366cc"]
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        stage_dist = stage_f["lifecycle_stage"].value_counts().reset_index()
        stage_dist.columns = ["Lifecycle Stage", "Count"]
        fig = px.bar(
            stage_dist,
            x="Lifecycle Stage",
            y="Count",
            title="Lifecycle Stage Distribution",
            color="Lifecycle Stage"
        )
        fig.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        survivors = life_f.sort_values(
            ["days_on_playlist", "peak_position"],
            ascending=[False, True]
        ).head(15)
        st.markdown("### Longest survivors")
        st.dataframe(
            survivors[[
                "song", "artist", "days_on_playlist",
                "peak_position", "entry_to_peak_days",
                "album_type", "explicit_label"
            ]],
            use_container_width=True
        )

    with c4:
        risers = life_f.sort_values(
            ["entry_to_peak_days", "peak_position"],
            ascending=[True, True]
        ).head(15)
        st.markdown("### Fastest risers")
        st.dataframe(
            risers[[
                "song", "artist", "entry_to_peak_days",
                "peak_position", "days_on_playlist",
                "album_type", "explicit_label"
            ]],
            use_container_width=True
        )

with tab2:
    st.subheader("Lifecycle behavior")
    c1, c2 = st.columns(2)

    with c1:
        fig = px.scatter(
            life_f,
            x="entry_popularity",
            y="days_on_playlist",
            color="album_type",
            size="peak_popularity",
            hover_data=["song", "artist", "peak_position", "entry_to_peak_days"],
            title="Entry Popularity vs Longevity"
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.scatter(
            life_f,
            x="peak_position",
            y="entry_to_peak_days",
            color="explicit_label",
            hover_data=["song", "artist", "days_on_playlist"],
            title="Peak Strength vs Time to Peak"
        )
        fig.update_xaxes(autorange="reversed")
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    stage_month = (
        stage_f.groupby(["month", "lifecycle_stage"])
        .size()
        .reset_index(name="count")
    )

    fig = px.density_heatmap(
        stage_month,
        x="month",
        y="lifecycle_stage",
        z="count",
        color_continuous_scale="Blues",
        title="Lifecycle Stage Intensity by Month"
    )
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Playlist rotation & churn")
    churn_f = churn[(churn["date"].dt.date >= start_date) & (churn["date"].dt.date <= end_date)].copy()
    monthly_f = monthly.copy()

    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=churn_f["date"], y=churn_f["entries"],
            mode="lines", name="Entries", line=dict(color="#2a9d8f", width=2)
        ))
        fig.add_trace(go.Scatter(
            x=churn_f["date"], y=churn_f["exits"],
            mode="lines", name="Exits", line=dict(color="#e76f51", width=2)
        ))
        fig.update_layout(
            title="Daily Entries and Exits",
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Count"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.line(
            churn_f,
            x="date",
            y="churn_rate",
            title="Daily Churn Rate",
            color_discrete_sequence=["#7b2cbf"]
        )
        fig.update_layout(template="plotly_white", yaxis_title="Churn Rate")
        st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        monthly_f,
        x="month",
        y="avg_churn_rate",
        title="Average Monthly Churn Rate",
        color="avg_churn_rate",
        color_continuous_scale="Oranges"
    )
    fig.update_layout(template="plotly_white", yaxis_title="Average Churn Rate")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Monthly churn table")
    st.dataframe(monthly_f, use_container_width=True)

with tab4:
    st.subheader("Content maturity comparisons")
    c1, c2 = st.columns(2)

    with c1:
        fig = px.box(
            life_f,
            x="explicit_label",
            y="days_on_playlist",
            color="explicit_label",
            title="Explicit vs Clean Longevity"
        )
        fig.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.box(
            life_f,
            x="album_type",
            y="days_on_playlist",
            color="album_type",
            title="Single vs Album Longevity"
        )
        fig.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        explicit_compare = (
            life_f.groupby("explicit_label", as_index=False)["days_on_playlist"]
            .mean()
            .rename(columns={"days_on_playlist": "avg_days"})
        )
        fig = px.bar(
            explicit_compare,
            x="explicit_label",
            y="avg_days",
            color="explicit_label",
            title="Average Longevity by Explicit Content"
        )
        fig.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        album_compare = (
            life_f.groupby("album_type", as_index=False)["days_on_playlist"]
            .mean()
            .rename(columns={"days_on_playlist": "avg_days"})
        )
        fig = px.bar(
            album_compare,
            x="album_type",
            y="avg_days",
            color="album_type",
            title="Average Longevity by Album Type"
        )
        fig.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Strategic interpretation")
    st.info(
        "Use these comparisons to assess whether Spain rewards clean vs explicit tracks differently, "
        "and whether single-led campaigns outperform album-led exposure in playlist retention."
    )

with tab5:
    st.subheader("Song deep dive")
    options = sorted((life_f["song"] + " — " + life_f["artist"]).unique().tolist())
    selected = st.selectbox("Select a song", options)

    song_name, artist_name = selected.split(" — ", 1)

    song_stage = stage_f[
        (stage_f["song"] == song_name) &
        (stage_f["artist"] == artist_name)
    ].sort_values("date")

    song_life = life_f[
        (life_f["song"] == song_name) &
        (life_f["artist"] == artist_name)
    ].iloc[0]

    a, b, c, d, e = st.columns(5)
    a.metric("Entry Date", str(song_life["entry_date"])[:10])
    b.metric("Exit Date", str(song_life["exit_date"])[:10])
    c.metric("Days on Playlist", int(song_life["days_on_playlist"]))
    d.metric("Peak Position", int(song_life["peak_position"]))
    e.metric("Time to Peak", int(song_life["entry_to_peak_days"]))

    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=song_stage["date"],
            y=song_stage["position"],
            mode="lines+markers",
            name="Rank",
            line=dict(color="#264653", width=3)
        ))
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            title="Daily Playlist Rank",
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Position"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.line(
            song_stage,
            x="date",
            y="popularity",
            title="Daily Popularity Trend",
            color_discrete_sequence=["#f4a261"]
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Song-level daily lifecycle records")
    st.dataframe(
        song_stage[[
            "date", "position", "popularity",
            "playlist_day", "lifecycle_stage",
            "album_type", "explicit_label"
        ]],
        use_container_width=True
    )
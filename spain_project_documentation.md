

This project analyzes daily Spain Top 50 playlist snapshots to measure how songs enter, mature,
peak, stabilize, and exit the chart. The working dataset contains 27800 playlist rows across 555
daily snapshots from 2024-05-18 to 2025-11-27, covering 575 unique song-artist combinations.
date
position
song
artist
popularity
duration_ms
album_type
total_tracks
is_explicit
album_cover_url
Parsed dates using day-first format.
Standardized text fields and created a normalized song_key from song and artist.
Converted position, popularity, duration, and album track count to numeric types.
Built lifecycle metrics per song and daily stage labels per observation.
Exported validated analysis tables for dashboard reuse.
For each normalized song key, the analysis computes entry date, exit date, days on playlist,
peak position, peak date, entry-to-peak time, popularity at entry/peak/exit, re-entry count, and
rank volatility.
## Content Maturity, Release Lifecycle & Playlist
Rotation Analysis of Spain Top 50 Songs
Project objective
Dataset fields used
Data validation and preparation
Analytical framework
- Song lifecycle construction

Daily observations are mapped into five stages:
New Entry: first 7 playlist days.
Growth Phase: meaningful position improvement.
Peak Phase: Top 10 and stable.
Mature Phase: sustained presence without strong acceleration.
Decline Phase: worsening rank, especially near the lower end.
Daily entry and exit counts are computed by comparing the set of songs on consecutive playlist
dates. Churn rate is measured as (entries + exits) / 50.
The project compares longevity and maturity behavior across explicit vs clean tracks, single vs
album tracks, and popularity-linked maturity.
Average days on playlist: 48.26
Median days on playlist: 13.0
Average daily churn rate: 0.0705
Share of songs that reached Top 10: 0.2939
Re-entry rate: 0.4174
Explicit average days on playlist: 45.94
Clean average days on playlist: 50.1
Single average days on playlist: 58.13
Album average days on playlist: 39.21
Overview KPIs and distribution charts.
Lifecycle performance views.
Rotation and churn monitoring.
Attribute comparison panels.
Song-level deep dive with rank and popularity timeline.
- Lifecycle stage classification
- Playlist rotation analysis
- Attribute comparisons
KPI snapshot
Streamlit application modules

Frame the project as a Spain-specific playlist intelligence system for release timing, retention
forecasting, and promotional planning. Emphasize that lifecycle behavior, churn intensity, and
content maturity patterns should guide Atlantic's local strategy instead of copying UK/US
assumptions.
Suggested submission narrative
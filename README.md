# Spain Top 50 Lifecycle Dashboard

A Streamlit dashboard for analyzing **Content Maturity, Release Lifecycle, and Playlist Rotation** in Spain's Top 50 songs.

## Project purpose

This project was created for internship work focused on the Spanish music market.  
It helps analyze:

- How long songs remain in Spain's Top 50
- How fast songs peak after entry
- How playlist churn behaves over time
- Whether explicit content matures differently from clean content
- Whether singles outperform album tracks in longevity

## Key metrics from analysis

- Average Days on Playlist: 48.26
- Median Days on Playlist: 13.0
- Average Entry-to-Peak Time: 9.49 days
- Peak Conversion Rate (Top 10): 29.39%
- Average Daily Churn Rate: 0.0705
- Retention Stability Index: 0.2894
- Re-entry Rate: 41.74%
- Explicit Content Lifecycle Score: 36.46
- Non-explicit Lifecycle Score: 37.03
- Single vs Album Longevity Ratio: 1.4825

## Folder structure

```bash
spain-top50-dashboard/
│
├── app/
│   ├── spain_top50_dashboard.py
│   ├── song_lifecycle_metrics.csv
│   ├── daily_stage_classification.csv
│   ├── daily_churn_metrics.csv
│   ├── monthly_churn_metrics.csv
│   └── kpi_summary.csv
│
├── data_raw/
│   └── Atlantic_Spain.csv
│
├── docs/
│   └── spain_project_documentation.md
│
├── requirements.txt
├── README.md
└── .gitignore
```

## How to run locally

1. Clone or download this repository.
2. Open terminal in the project folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the dashboard:

```bash
streamlit run app/spain_top50_dashboard.py
```

## Deployment on Streamlit Community Cloud

1. Upload this project to a GitHub repository.
2. Open Streamlit Community Cloud.
3. Click **Create app**.
4. Select your GitHub repository.
5. Choose the branch.
6. Set the main file path as:

```bash
app/spain_top50_dashboard.py
```

7. Click **Deploy**.

## Dashboard features

- KPI cards
- Lifecycle stage analysis
- Churn and rotation trends
- Explicit vs clean comparison
- Single vs album comparison
- Song-level deep dive

## Notes

Make sure all CSV files remain inside the `app/` folder, otherwise the dashboard will not find them during deployment.

## Author

Pragya Dwivedi

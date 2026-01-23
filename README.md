```markdown
# Real-Time CitiBike Station Anomaly Detection

A real-time pipeline that monitors CitiBike stations across NYC to identify operational instability through behavioral pattern analysis.

## Overview

CitiBike operates 1,700+ docking stations generating thousands of status updates hourly. This system detects stations rapidly cycling between empty and full states—patterns invisible in static dashboards that indicate rebalancing failures, capacity constraints, or localized demand shocks.

**Key Features:**
- Real-time monitoring of all CitiBike stations via GBFS API
- Behavioral anomaly detection (rapid empty-full state transitions)
- Geographic visualization of station utilization and flagged anomalies
- Interpretable, rule-based detection logic for operational teams
- Persistent storage for historical analysis and BI integration

## Demo

[Watch the system in action](https://www.youtube.com/embed/Ik1FlE2llmI) - Live data ingestion, feature engineering, anomaly detection, and visualization.

## Problem Statement

**The Challenge:** Operational issues often manifest as rapid oscillations—stations cycling between empty and full within minutes. These patterns are invisible in point-in-time dashboards and disappear before daily reports capture them.

**The Solution:** Real-time anomaly detection with rolling time windows that flags stations exhibiting frequent state transitions (default: 3+ flips in 45 minutes), enabling same-shift operational response.

## Architecture

```
Live CitiBike API → Data Ingestion (Go) → Feature Engineering (Go) → Anomaly Detection (Python) → Storage (MySQL) → Dashboards
```

### Components

**1. Data Ingestion** (`internal/api/api.go`)
- Polls CitiBike GBFS API for real-time station status
- Parses operational fields: bikes available, docks available, station metadata
- Go selected for low-latency polling and efficient concurrent processing

**2. Feature Engineering** (`internal/processing/processing.go`)
- Transforms raw counts into operational metrics:
  - Percent filled/empty (normalizes across station capacities)
  - State classification: `empty` (<10%), `full` (>90%), `normal`
  - Timestamp normalization for time-series analysis

**3. Anomaly Detection** (`anomaly_detection/detect_flips.py`)
- Tracks state transitions (`empty` ↔ `full`) within rolling windows
- Flags stations exceeding threshold (default: 3+ flips in 45 minutes)
- Confirms patterns across multiple observations

**4. Storage** (MySQL)
- Persists station states and anomaly flags
- Enables historical analysis and BI tool integration

## Installation

### Prerequisites
- Go 1.18+
- Python 3.8+
- MySQL 8.0+

### Setup

1. Clone the repository:
```bash
git clone https://github.com/djbrown227/citibike_anomaly_detection.git
cd citibike_anomaly_detection
```

2. Install Go dependencies:
```bash
go mod download
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MySQL database:
```bash
mysql -u root -p < schema.sql
```

5. Update configuration file with your database credentials:
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your settings
```

## Usage

### Running the Pipeline

**Start data ingestion:**
```bash
go run cmd/ingest/main.go
```

**Run feature engineering:**
```bash
go run cmd/process/main.go
```

**Execute anomaly detection:**
```bash
python anomaly_detection/detect_flips.py
```

### Configuration

Key parameters in `config.yaml`:

```yaml
detection:
  time_window_minutes: 45    # Rolling window for flip detection
  flip_threshold: 3          # Minimum flips to flag as anomaly
  empty_threshold: 0.10      # Station considered empty below 10%
  full_threshold: 0.90       # Station considered full above 90%

api:
  poll_interval_seconds: 60  # How often to fetch new data
  base_url: "https://gbfs.citibikenyc.com/gbfs/2.3/en/station_status.json"
```

## Output Format

**Anomaly Detection Output:**
```csv
timestamp,station_id,station_name,percent_full,state,flip_count
2025-05-08 16:00:00,29a41b09,41 St & 3 Ave,0.05,empty,4
2025-05-08 16:30:00,dd482585,2 Ave & 36 St,0.95,full,5
```

## Visualizations

The system produces four key outputs:

1. **Raw API Data**: Live station status from CitiBike GBFS API
2. **Feature-Enriched Data**: Parsed data with engineered metrics
3. **Utilization Heatmap**: Geographic view of station capacity (darker = higher utilization)
4. **Anomaly Alerts**: Flagged stations with rapid state oscillations

![Station Utilization](assets/Screenshot%202025-05-13%20at%201.15.49%20PM.png)
![Detected Anomalies](assets/Screenshot%202025-05-13%20at%201.15.39%20PM.png)

## Operational Applications

**Prioritized Rebalancing**
- Direct crews to confirmed instability, not transient availability issues
- Reduce wasted trips, increase intervention success rates

**Capacity Planning**
- Identify stations with recurring patterns as dock expansion candidates
- Data-driven evidence for capital investments

**Demand Monitoring**
- Detect localized surges from events, transit disruptions, weather
- Enable dynamic operational response

**BI Integration**
- Clean integration with Tableau, Power BI, custom dashboards
- Structured output for automated alerting systems

## Key Design Decisions

**Rule-Based Detection**: Chose interpretable thresholds over ML models for operational trust and tunability.

**45-Minute Windows**: Balances signal strength with operational responsiveness for same-shift intervention.

**Go + Python Stack**: Go for performance-critical ingestion, Python for flexible time-series analysis.

## Technology Stack

- **Go**: Real-time API ingestion and feature processing
- **Python (pandas)**: Time-series analysis and anomaly detection
- **MySQL**: Persistent storage with time-series indexing
- **Jekyll**: Project documentation (GitHub Pages)

## Project Structure

```
citibike_anomaly_detection/
├── cmd/
│   ├── ingest/          # API ingestion entry point
│   └── process/         # Feature engineering entry point
├── internal/
│   ├── api/             # GBFS API client
│   ├── processing/      # Feature engineering logic
│   └── storage/         # Database operations
├── anomaly_detection/
│   └── detect_flips.py  # Anomaly detection module
├── assets/              # Visualization outputs
├── config.yaml          # Configuration file
├── schema.sql           # Database schema
├── go.mod
├── requirements.txt
└── README.md
```

## Future Enhancements

- **Predictive Models**: Forecast instability based on time-of-day, weather, events
- **Automated Alerts**: Push notifications to rebalancing crews via SMS/mobile
- **Severity Scoring**: Weight anomalies by station importance and ridership volume
- **Multi-City Support**: Extend to other GBFS-compliant bike-share systems

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License - see LICENSE file for details

## Contact

**Daniel Brown**  
Email: djbrown227@gmail.com  
LinkedIn: [linkedin.com/in/daniel-brown-203288146](https://www.linkedin.com/in/daniel-brown-203288146/)  
GitHub: [github.com/djbrown227](https://github.com/djbrown227)

## Acknowledgments

- CitiBike for providing public GBFS API access
- GBFS specification maintainers for standardized bike-share data formats

---

*This project demonstrates how real-time data engineering and operationally-focused design solve practical problems in distributed systems.*
```
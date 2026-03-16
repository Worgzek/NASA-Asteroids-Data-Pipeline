# NASA Asteroid ETL Pipeline 🚀

## Giới thiệu

Đây là project xây dựng **pipeline ETL** để thu thập và xử lý dữ liệu **tiểu hành tinh gần Trái Đất (Near-Earth Asteroids)** từ API công khai của NASA.

Pipeline thực hiện các bước:

- Thu thập dữ liệu từ NASA API  
- Xử lý dữ liệu JSON phức tạp  
- Chuyển đổi dữ liệu sang dạng CSV  
- Kiểm tra và làm sạch dữ liệu  
- Load dữ liệu vào PostgreSQL  
- Tính toán **mức độ nguy hiểm (risk score)** của các tiểu hành tinh  

Dự án sử dụng **Apache Airflow** để orchestrate pipeline và **Docker** để chạy môi trường.

---

# Nguồn dữ liệu

NASA Near Earth Object Web Service API

https://api.nasa.gov/

API cung cấp thông tin về các tiểu hành tinh bay gần Trái Đất.

---

# Cấu trúc project

```
nasa_asteroid_ETL_Project
│
├── dags/
│   └── nasa_pipeline.py
│
├── scripts/
│   ├── extract_api.py
│   ├── flatten_data.py
│   ├── transform_data.py
│   ├── load_postgres.py
│   └── danger_score.py
│
├── data/
│   ├── raw/
│   ├── flatten/
│   └── processed/
│
├── logs/
│
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

# Luồng dữ liệu (Pipeline)

```
NASA API
   ↓
Extract dữ liệu JSON
   ↓
Flatten dữ liệu
   ↓
Transform → CSV
   ↓
Validate dữ liệu
   ↓
Load vào PostgreSQL
   ↓
Tính toán risk_score
```

---

# Công thức Risk Score

Risk score được tính dựa trên:

- Kích thước tối đa
- Vận tốc
- Khoảng cách tới Trái Đất

```
risk_score =
(diameter_max_m / 1000) * 4
+ (velocity_km_s / 30) * 3
+ (7500000 / miss_distance_km) * 3
```

Phân loại mức nguy hiểm:

| Risk Score | Danger Level |
|------------|--------------|
| ≥ 8 | EXTREME |
| ≥ 6 | HIGH |
| ≥ 4 | MEDIUM |
| < 4 | LOW |

---

# Công nghệ sử dụng

- Python
- PostgreSQL
- Apache Airflow
- Docker
- Loguru (logging)

Python libraries:

```
psycopg2
pandas
requests
loguru
python-dotenv
```

---

# Cách chạy project

Chạy môi trường bằng Docker:

```bash
docker compose up
```

Mở giao diện Airflow:

```
http://localhost:8080
```

Thông tin đăng nhập mặc định:

```
airflow
airflow
```

Trigger DAG để chạy toàn bộ pipeline.

---

# Kết quả

Dữ liệu được lưu trong PostgreSQL với các bảng:

```
asteroids
danger_score
```

Ví dụ các cột dữ liệu:

```
asteroid_id
name
diameter_max_m
velocity_km_s
miss_distance_km
risk_score
danger_level
date
```

---

# Logging

Log pipeline được lưu tại:

```
logs/
```

Log giúp theo dõi:

- trạng thái pipeline
- lỗi khi chạy
- tiến trình xử lý dữ liệu

---

# Hướng phát triển thêm

Có thể mở rộng project bằng cách:

- Phân tích xu hướng tiểu hành tinh theo thời gian
- Xây dựng dashboard (Streamlit / PowerBI)
- Lưu dữ liệu vào Data Warehouse (BigQuery / Snowflake)
- Tối ưu pipeline cho dữ liệu lớn

---

# Tác giả

Tommy  
Data Engineering Learner
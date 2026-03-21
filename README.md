# NASA Asteroid ETL Pipeline 🚀

## Giới thiệu

Đây là project xây dựng **pipeline ETL** để thu thập và xử lý dữ liệu **tiểu hành tinh gần Trái Đất (Near-Earth Asteroids)** từ API công khai của NASA, dữ liệu sẽ được lấy hằng ngày theo thời gian thực.

Pipeline thực hiện các bước:
---

   - Thu thập dữ liệu từ NASA API
   - Xử lý dữ liệu JSON phức tạp
   - Chuyển đổi dữ liệu sang dạng CSV
   - Kiểm tra và làm sạch dữ liệu
   - Load dữ liệu vào PostgreSQL
   - Tính toán mức độ nguy hiểm (risk score) của các tiểu hành tinh
   - Dự án cũng sử dụng Apache Airflow để tự động hóa pipeline và Docker để chạy môi trường.

Dữ liệu được lấy từ:
NASA Near Earth Object Web Service API
https://api.nasa.gov/

---

# Cấu trúc project

```
API này cung cấp thông tin về các tiểu hành tinh đang bay gần Trái Đất.
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
│   └── init.sql

├── logs/
│
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

# Luồng dữ liệu (Pipeline)

```
Pipeline xử lý dữ liệu theo thứ tự:

NASA API
   ↓
Extract dữ liệu JSON
   ↓
Flatten dữ liệu (JSON lồng nhau → dữ liệu phẳng)
   ↓
Transform → CSV
   ↓
Transform dữ liệu → CSV 
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
Công thức tính Risk Score:

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
```
Công nghệ sử dụng:

Project sử dụng các công nghệ sau:

   - Python
   - PostgreSQL
   - Apache Airflow
   - Docker
   - Loguru (logging)
   - Pandas

```

---

# Cách chạy project

Chạy môi trường bằng Docker:

```bash
docker compose up
```

Mở giao diện Airflow:

```
http://localhost:8081
```

Thông tin đăng nhập mặc định:

```
username: admin
password: admin
```

Trigger DAG để chạy toàn bộ pipeline.

Cách connect Database:
```
register - server
   - host name: localhost
   - port: 5433
   - maintenance database: airflow
   - username: airflow
   - password: 123
```
---

# Kết quả

Dữ liệu được lưu ở PostgreSQL trong Database nasa_neo với các bảng:

```
asteroids
danger_score
```

Các cột dữ liệu:

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

---


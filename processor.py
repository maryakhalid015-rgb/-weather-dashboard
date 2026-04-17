import json  # used to work with JSON data
from kafka import KafkaConsumer  # Kafka consumer to read streamed data
import csv
from datetime import datetime

# --- STATE VARIABLES ---
record_count = 0                 # total number of processed records
total_temp = 0                   # sum of all temperatures for average calculation
max_temp = float('-inf')         # highest temperature seen so far
min_temp = float('inf')          # lowest temperature seen so far
previous_temp = None             # previous temperature for trend analysis
condition_counts = {}            # dictionary to count weather conditions

# --- FUNCTIONS ---

def clean_data(data):
    """Remove invalid or incomplete records."""
    required_fields = [
        "city",
        "temperature",
        "condition",
        "feelslike_c",
        "humidity",
        "wind_kph",
        "pressure_mb",
        "cloud",
        "uv"
    ]

    for field in required_fields:
        if data.get(field) is None:
            return None  # skip record if any required field is missing

    return data


def transform_data(data):
    """Convert data into a structured format and create derived features."""
    city = str(data["city"]).replace("`", "").strip()
    temp_c = float(data["temperature"])
    temp_f = (temp_c * 9 / 5) + 32
    feelslike_c = float(data["feelslike_c"])
    humidity = int(data["humidity"])
    wind_kph = float(data["wind_kph"])
    pressure_mb = float(data["pressure_mb"])
    cloud = int(data["cloud"])
    uv = float(data["uv"])
    condition = str(data["condition"]).strip()

    # Temperature category
    if temp_c >= 35:
        temp_category = "Very Hot"
    elif temp_c >= 25:
        temp_category = "Warm"
    elif temp_c >= 15:
        temp_category = "Mild"
    else:
        temp_category = "Cold"

    # Humidity category
    if humidity >= 80:
        humidity_level = "High"
    elif humidity >= 50:
        humidity_level = "Moderate"
    else:
        humidity_level = "Low"

    # Wind category
    if wind_kph >= 40:
        wind_level = "Strong"
    elif wind_kph >= 20:
        wind_level = "Moderate"
    else:
        wind_level = "Light"

    # Cloud cover category
    if cloud >= 75:
        cloud_level = "Cloudy"
    elif cloud >= 30:
        cloud_level = "Partly Cloudy"
    else:
        cloud_level = "Clear Sky"

    return {
        "city": city,
        "temp_c": temp_c,
        "temp_f": round(temp_f, 2),
        "feelslike_c": feelslike_c,
        "humidity": humidity,
        "wind_kph": wind_kph,
        "pressure_mb": pressure_mb,
        "cloud": cloud,
        "uv": uv,
        "condition": condition,
        "temp_category": temp_category,
        "humidity_level": humidity_level,
        "wind_level": wind_level,
        "cloud_level": cloud_level
    }


def analyze_data(record):
    """Perform real-time analytics on the structured weather record."""
    global record_count, total_temp, max_temp, min_temp, previous_temp, condition_counts

    temp_c = record["temp_c"]
    humidity = record["humidity"]
    wind_kph = record["wind_kph"]
    uv = record["uv"]
    condition = record["condition"]

    # Update counters and running statistics
    record_count += 1
    total_temp += temp_c
    max_temp = max(max_temp, temp_c)
    min_temp = min(min_temp, temp_c)
    avg_temp = total_temp / record_count

    # Temperature trend analysis
    if previous_temp is None:
        temp_change = 0
        trend = "No previous data"
    else:
        temp_change = temp_c - previous_temp
        if temp_change > 0:
            trend = "Increasing"
        elif temp_change < 0:
            trend = "Decreasing"
        else:
            trend = "Stable"

    previous_temp = temp_c

    # Count frequency of current weather conditions
    condition_counts[condition] = condition_counts.get(condition, 0) + 1
    most_common_condition = max(condition_counts, key=condition_counts.get)

    # Rule-based alert generation
    alerts = []

    if temp_c > 40:
        alerts.append("Extreme heat alert")
    elif temp_c > 35:
        alerts.append("High temperature alert")

    if humidity > 85:
        alerts.append("High humidity alert")

    if wind_kph > 40:
        alerts.append("Strong wind alert")

    if uv > 7:
        alerts.append("High UV risk")

    if not alerts:
        alerts.append("No alert")

    return {
        **record,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "record_no": record_count,
        "temp_change": round(temp_change, 2),
        "trend": trend,
        "avg_temp": round(avg_temp, 2),
        "max_temp": max_temp,
        "min_temp": min_temp,
        "condition_count": condition_counts[condition],
        "most_common_condition": most_common_condition,
        "alerts": ", ".join(alerts)
    }


# --- KAFKA CONSUMER SETUP ---
consumer = KafkaConsumer(
    "weather-topic",  # topic name to consume from
    bootstrap_servers="localhost:9092",  # Kafka broker address
    auto_offset_reset="earliest",  # read from the first available message
    group_id="weather-processing-group",  # consumer group ID
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))  # convert bytes to JSON
)

print("Processing stream...\n")

# --- MAIN PROCESSING LOOP ---
for message in consumer:
    raw_data = message.value  # get incoming record from Kafka
    print("RAW DATA:", raw_data)

    # Step 1: Clean the data
    cleaned_data = clean_data(raw_data)
    if cleaned_data is None:
        continue  # skip invalid records

    # Step 2: Transform the data
    transformed_data = transform_data(cleaned_data)

    # Step 3: Analyze the transformed data
    analyzed_data = analyze_data(transformed_data)

    # Step 4: Print final processed result
    print(analyzed_data)

    # Step 5: Save processed result to CSV
    with open("weather_data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=analyzed_data.keys())

        if f.tell() == 0:
            writer.writeheader()

        writer.writerow(analyzed_data)
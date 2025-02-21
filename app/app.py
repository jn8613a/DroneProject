import google.generativeai as genai
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

genai.configure(api_key="AIzaSyAZfKSR1d47zRv8g8EcBngqpb8kZiy3kWw")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "🚀 AI Drone Report Generator is running. Use '/generate-drone-report' to create a report."

@app.route('/generate-drone-report', methods=['POST'])
def generate_drone_report():
    """Generates an AI-powered drone mission report."""
    data = request.json
    location = data.get("location", "Unknown Location")
    flight_time = data.get("flight_time", "Unknown Duration")
    mission_purpose = data.get("mission_purpose", "General Surveillance")

    model = genai.GenerativeModel("gemini-1.5-flash")

    report_prompt = f"""
    Generate a detailed drone flight report based on the following:
    - Mission Purpose: {mission_purpose}
    - Location: {location}
    - Flight Time: {flight_time}

    Include:
    1. Summary of findings.
    2. Possible risks or observations.
    3. Recommendations for future missions.
    """

    response = model.generate_content(report_prompt)

    return jsonify({
        "message": "Drone report generated successfully!",
        "location": location,
        "flight_time": flight_time,
        "mission_purpose": mission_purpose,
        "ai_generated_report": response.text
    })

def start_flask():
    app.run(debug=False, use_reloader=False)

flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()

time.sleep(2)

API_URL = "http://127.0.0.1:5000/generate-drone-report"

print("\n🚀 Welcome to the AI Drone Report Generator!\n")

location = input("📍 Where was the drone mission conducted? ")
flight_time = input("⏱️ How long was the flight? (e.g., 30 minutes) ")
mission_purpose = input("🎯 What was the mission purpose? (e.g., Surveillance, Wildlife Monitoring) ")

payload = {
    "location": location,
    "flight_time": flight_time,
    "mission_purpose": mission_purpose
}

print("\n✈Sending request to AI Drone Report Generator...\n")

try:
    response = requests.post(API_URL, json=payload)
    response_data = response.json()

    print("\nAI Drone Report Generated!\n")
    print(f"Location: {response_data['location']}")
    print(f"Flight Time: {response_data['flight_time']}")
    print(f"Mission Purpose: {response_data['mission_purpose']}")
    print("\n AI-Generated Report:\n")
    print(response_data["ai_generated_report"])

except requests.exceptions.RequestException as e:
    print("Error connecting to the API:", e)

import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyAZfKSR1d47zRv8g8EcBngqpb8kZiy3kWw")

EMISSION_FACTOR = 0.233

@app.route('/')
def home():
    return "Welcome to the Drone Emissions API. Use the '/generate-emissions' endpoint."

@app.route('/generate-emissions', methods=['POST'])
def generate_emissions():
    data = request.json
    altitude = float(data.get("altitude", 100))
    flight_time = float(data.get("flight_time", 30))
    battery_capacity = float(data.get("battery_capacity", 5))

    power_used = (battery_capacity * flight_time) / 60
    co2_emissions = power_used * EMISSION_FACTOR

    prompt = f"""
    A drone with {battery_capacity} kWh battery capacity flew for {flight_time} minutes at {altitude} meters.
    The estimated emissions are {co2_emissions:.3f} kg CO₂.
    Provide additional insights on drone emissions and how to reduce them.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return jsonify({
        "emissions_report": response.text,
        "calculated_co2_emissions": f"{co2_emissions:.3f} kg CO₂"
    })

if __name__ == '__main__':
    app.run(debug=True)

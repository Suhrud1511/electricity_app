# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

# Define tariff rates
TARIFF_RATE_BELOW_THRESHOLD = 4  # Rupees per unit for consumption below threshold
TARIFF_RATE_ABOVE_THRESHOLD = 7  # Rupees per unit for consumption above threshold
USAGE_PER_DEVICE = {
    'bulb': 5,          # Units per month
    'light': 10,         # Units per month
    'refrigerator': 20,  # Units per month
    'oven': 30,          # Units per month
    'geyser': 50         # Units per month
}
THRESHOLD = 200  # Threshold for changing the tariff rate

def calculate_total_units(square_footage, num_bulbs, num_lights, num_refrigerators, num_ovens, num_geysers):
    total_units = square_footage * 0  # Units for square footage

    # Add units for each device
    total_units += num_bulbs * USAGE_PER_DEVICE['bulb']
    total_units += num_lights * USAGE_PER_DEVICE['light']
    total_units += num_refrigerators * USAGE_PER_DEVICE['refrigerator']
    total_units += num_ovens * USAGE_PER_DEVICE['oven']
    total_units += num_geysers * USAGE_PER_DEVICE['geyser']

    return total_units

def calculate_bill(total_units):
    if total_units <= THRESHOLD:
        total_bill = total_units * TARIFF_RATE_BELOW_THRESHOLD
    else:
        total_bill = total_units * TARIFF_RATE_ABOVE_THRESHOLD
    return total_bill

@app.route('/calculate', methods=['POST'])
def calculate():
    square_footage = float(request.form['square_footage'])
    num_bulbs = int(request.form.get('num_bulbs', 0))
    num_lights = int(request.form.get('num_lights', 0))
    num_refrigerators = int(request.form.get('num_refrigerators', 0))
    num_ovens = int(request.form.get('num_ovens', 0))
    num_geysers = int(request.form.get('num_geysers', 0))

    total_units = calculate_total_units(square_footage, num_bulbs, num_lights, num_refrigerators, num_ovens, num_geysers)
    total_bill = calculate_bill(total_units)

    # Calculate consumption and cost for each device
    bulb_consumption = num_bulbs * USAGE_PER_DEVICE['bulb']
    light_consumption = num_lights * USAGE_PER_DEVICE['light']
    refrigerator_consumption = num_refrigerators * USAGE_PER_DEVICE['refrigerator']
    oven_consumption = num_ovens * USAGE_PER_DEVICE['oven']
    geyser_consumption = num_geysers * USAGE_PER_DEVICE['geyser']

    total_units=bulb_consumption+light_consumption+refrigerator_consumption+oven_consumption+geyser_consumption
    if (total_units>THRESHOLD):
        bulb_cost = num_bulbs * TARIFF_RATE_ABOVE_THRESHOLD 
        light_cost = num_lights * TARIFF_RATE_ABOVE_THRESHOLD 
        refrigerator_cost = num_refrigerators * TARIFF_RATE_ABOVE_THRESHOLD
        oven_cost = num_ovens * TARIFF_RATE_ABOVE_THRESHOLD 
        geyser_cost = num_geysers * TARIFF_RATE_ABOVE_THRESHOLD 
    else:
        
        bulb_cost = num_bulbs * TARIFF_RATE_BELOW_THRESHOLD 
        light_cost = num_lights * TARIFF_RATE_BELOW_THRESHOLD 
        refrigerator_cost = num_refrigerators * TARIFF_RATE_BELOW_THRESHOLD
        oven_cost = num_ovens * TARIFF_RATE_BELOW_THRESHOLD 
        geyser_cost = num_geysers * TARIFF_RATE_BELOW_THRESHOLD 
    return render_template('result.html', 
                           square_footage=square_footage, 
                           total_units=total_units, 
                           bill=total_bill,
                           num_bulbs=num_bulbs,
                           bulb_consumption=bulb_consumption,
                           bulb_cost=bulb_cost,
                           num_lights=num_lights,
                           light_consumption=light_consumption,
                           light_cost=light_cost,
                           num_refrigerators=num_refrigerators,
                           refrigerator_consumption=refrigerator_consumption,
                           refrigerator_cost=refrigerator_cost,
                           num_ovens=num_ovens,
                           oven_consumption=oven_consumption,
                           oven_cost=oven_cost,
                           num_geysers=num_geysers,
                           geyser_consumption=geyser_consumption,
                           geyser_cost=geyser_cost)


if __name__ == '__main__':
    app.run(debug=True)

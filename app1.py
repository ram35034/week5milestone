import random
from datetime import datetime
from flask import Flask, jsonify, request, render_template

def collect_data():
    sources = ['Solar', 'Wind', 'Grid']
    data = []
    for source in sources:
        consumption = round(random.uniform(50.0, 500.0), 2)  # Simulated consumption value
        timestamp = datetime.now().isoformat()
        data.append({
            'source': source,
            'consumption': consumption,
            'timestamp': timestamp
        })
    return data

def calculate_total_consumption(data):
    return sum(item['consumption'] for item in data)

def init_routes(app):
    @app.route('/')
    def index():
        return "Energy Consumption Monitoring System"

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/api/total_consumption', methods=['POST'])
    def total_consumption():
        data = request.json
        total = calculate_total_consumption(data)
        return jsonify({'total_consumption': total})

    @app.route('/api/collect_data', methods=['GET'])
    def collect_data_endpoint():
        data = collect_data()
        return jsonify(data)

def create_app():
    app = Flask(__name__)

    # Initialize routes
    init_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

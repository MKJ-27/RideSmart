# Helper function to handle individual service requests
def handle_service_request(process_function, user_request):
    result = []
    process_function(user_request, result)
    return result

@api_1.route('/get_prices/uber', methods=['POST'])
def get_prices_uber():
    data = request.get_json()
    return handle_single_service(data, process_uber_request, "Uber")

@api_1.route('/get_prices/jeeny', methods=['POST'])
def get_prices_jeeny():
    data = request.get_json()
    return handle_single_service(data, process_jeeny_request, "Jeeny")

@api_1.route('/get_prices/careem', methods=['POST'])
def get_prices_careem():
    data = request.get_json()
    return handle_single_service(data, process_careem_request, "Careem")

@api_1.route('/get_prices/bolt', methods=['POST'])
def get_prices_bolt():
    data = request.get_json()
    return handle_single_service(data, process_bolt_request, "Bolt")

def handle_single_service(data, process_function, service_name):
    print(f"Received request: {data}")
    pick_up = data.get('pick_up')
    destination = data.get('destination')
    user_id = data.get('user_id')

    if not pick_up or not destination or not user_id:
        print("Missing required parameters.")
        return jsonify({"error": "Missing required parameters"}), 400

    user_request = {
        "user_id": user_id,
        "pick_up": pick_up,
        "destination": destination
    }

    print(f"Processing request for {service_name}")
    start_time = time()
    result_list = handle_service_request(process_function, user_request)

    end_time = time()
    time_taken = end_time - start_time
    print(f"Total time taken to process {service_name} request: {time_taken:.2f} seconds")

    print(f"Returning results: {result_list}")
    return jsonify({"user_id": user_id, "results": result_list}), 200

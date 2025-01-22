import requests
import concurrent.futures

# API endpoint and payload
URL = "http://127.0.0.1:5001/proccess/get_prices/careem"

PAYLOAD = {
    "pick_up": "park avenue",
    "destination": "airport terminal",
    "user_id": 1
}


# Function to send a POST request
def send_request(user_id):
    payload = PAYLOAD.copy()
    payload['user_id'] = user_id  # Ensure unique user_id for each request

    try:
        response = requests.post(URL, json=payload)
        print(f"Request {user_id}: Status Code: {response.status_code}, Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Request {user_id}: Failed with error: {e}")


# Send 5 concurrent requests
def run_concurrent_requests(num_requests=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request, user_id) for user_id in range(1, num_requests + 1)]

        # Ensure all requests are completed
        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == "__main__":
    run_concurrent_requests()
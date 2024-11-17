import time
import json
import threading
import requests  # For making HTTP requests

# Set the URL for the deployed do-alu function in faasd
ALU_FUNCTION_URL = 'http://192.168.64.27:8080/function/do-alu'  # Updated with your provided URL

def main(n, parallel_index):
    """
    Main function that orchestrates the parallel execution of the do-alu function.
    """
    start_time = get_time()
    results = execute_in_parallel(n, parallel_index)
    
    total_exec_time = sum(int(exec_time) for exec_time in results if exec_time.isdigit())
    avg_exec_time = total_exec_time / parallel_index if parallel_index > 0 else 0
    
    print(json.dumps({
        'result': results,
        'avg_exec': avg_exec_time,
        'times': n,
        'exec_time': get_time() - start_time
    }))

def get_time():
    """Returns the current time in milliseconds."""
    return int(round(time.time() * 1000))

def execute_in_parallel(times, parallel_index):
    """
    Splits the workload and invokes the do-alu function in parallel using threads.
    """
    payload = {"n": times // parallel_index}
    result_texts = []
    threads = []

    for i in range(parallel_index):
        t = threading.Thread(target=invoke_do_alu, args=(payload, result_texts, i))
        threads.append(t)
        result_texts.append('')

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return result_texts

def invoke_do_alu(payload, result_texts, client_id):
    client_start_time = get_time()
    try:
        print(f"Client {client_id} sending payload: {payload}")

        # Send the request
        response = requests.post(ALU_FUNCTION_URL, json=payload, timeout=60)
        print(f"Client {client_id} response status: {response.status_code}")
        print(f"Client {client_id} response content: {response.text}")

        response.raise_for_status()  # Raise an error for unsuccessful requests

        client_end_time = get_time()
        client_exec_time = client_end_time - client_start_time

        try:
            result = response.json()
            result_texts[client_id] = str(result.get('execTime', '0'))
            print(f"Client {client_id} finished in {client_exec_time} ms.")
        except (json.JSONDecodeError, ValueError):
            result_texts[client_id] = 'error'
            print(f"Client {client_id} returned an invalid or empty response: {response.text}")

    except requests.RequestException as e:
        result_texts[client_id] = 'error'
        print(f"Client {client_id} encountered an error: {e}")
if __name__ == '__main__':
    # Example usage:
    # Replace `n` and `parallel_index` with desired values or fetch them dynamically if needed
    n = 60000000  # Total number of iterations
    parallel_index = 4  # Number of parallel tasks
    main(n, parallel_index)
import random
import time
import json

def handle(req):
    """
    Entry point for the ALU computation in faasd.
    Expects `req` as a JSON string input.
    """
    try:
        # Parse the input request as JSON
        req = json.loads(req)
    except (TypeError, json.JSONDecodeError):
        return json.dumps({
            'error': "Invalid input. Expected a JSON string."
        })

    start_time = get_time()
    if 'n' in req:
        times = req['n']
        result = alu(times)
        return json.dumps({
            'result': result,
            'times': times,
            'execTime': get_time() - start_time
        })
    else:
        return json.dumps({
            'error': "No 'n' in input payload"
        })

def get_time():
    """Returns the current time in milliseconds."""
    return int(round(time.time() * 1000))

def alu(times):
    """
    Performs a CPU-intensive arithmetic task for the given number of iterations.
    """
    a = random.randint(10, 100)
    b = random.randint(10, 100)
    temp = 0
    for i in range(times):
        if i % 4 == 0:
            temp = a + b
        elif i % 4 == 1:
            temp = a - b
        elif i % 4 == 2:
            temp = a * b
        else:
            temp = a / b if b != 0 else 0  # Avoid division by zero
    # Remove or comment out any print statements
    # print(f"Completed {times} iterations.")
    return temp
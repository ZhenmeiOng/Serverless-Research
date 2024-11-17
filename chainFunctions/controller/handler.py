import requests
import json
import sys

def call_function(function_name, data):
    """Calls an OpenFaaS function with the given data."""

    gateway_url = "http://192.168.64.27:8080/function/"  # remember to change the gateway IP
    url = f"{gateway_url}{function_name}"


    # json_data = json.dumps(data) # convert dict to JSON object

    # response = requests.post(url, data=json_data)

    # if response.status_code == 200:
    #     return json.loads(response.text)
    # else:
    #     raise Exception(f"Error calling function {function_name}: {response.status_code}")


    # Ensure data is properly serialized
    if isinstance(data, str):
        json_data = data  
    else:
        json_data = json.dumps(data)  # if data is a dictionary, change it to JSON string 

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:  # means received packet successfully
        try:
            # Get just the last line which should be our JSON response
            response_lines = response.text.strip().split('\n')
            json_response = response_lines[-1]
            return json.loads(json_response)
        except json.JSONDecodeError as e:
            print(f"Error parsing response from {function_name}: {e}", file=sys.stderr)
            print(f"Response content: {response.text}", file=sys.stderr)
            raise Exception(f"Invalid JSON response from {function_name}")
    else:
        raise Exception(f"Error calling function {function_name}: {response.status_code}")

    

def handle(req):
    print("running controller...")
    
    """Chains two OpenFaaS functions: 'function1' and 'function2'."""

    data = {"input": "some_initial_data"}

    # Call the first function
    result1 = call_function("callee", data)

    # Use the output of the first function as input for the second function
    result2 = call_function("caller", result1)

    print(result2)

if __name__ == "__main__":
    handle()

#----------------------------------------------------------------------------------

# # this is claude's code
# import requests
# import json
# import sys

# def call_function(function_name, data):
#     """Calls an OpenFaaS function with the given data."""
#     gateway_url = "http://192.168.64.27:8080/function/"
#     url = f"{gateway_url}{function_name}"

#     try:
#         # Ensure data is properly serialized
#         if isinstance(data, str):
#             json_data = data
#         else:
#             json_data = json.dumps(data)

#         headers = {'Content-Type': 'application/json'}
#         response = requests.post(url, data=json_data, headers=headers)

#         if response.status_code == 200:
#             try:
#                 # Get just the last line which should be our JSON response
#                 response_lines = response.text.strip().split('\n')
#                 json_response = response_lines[-1]
#                 return json.loads(json_response)
#             except json.JSONDecodeError as e:
#                 print(f"Error parsing response from {function_name}: {e}", file=sys.stderr)
#                 print(f"Response content: {response.text}", file=sys.stderr)
#                 raise Exception(f"Invalid JSON response from {function_name}")
#         else:
#             raise Exception(f"Error calling function {function_name}: {response.status_code}")
#     except Exception as e:
#         print(f"Error in call_function: {e}", file=sys.stderr)
#         raise

# def handle(req):
#     print("running controller...", file=sys.stderr)
#     try:
#         # Initial data
#         data = {"input": "some_initial_data"}

#         # Call the first function
#         result1 = call_function("callee", data)
#         print(f"Result from callee: {result1}", file=sys.stderr)

#         # Use the output of the first function as input for the second function
#         result2 = call_function("caller", result1)
#         print(f"Final result: {result2}", file=sys.stderr)
        
#         return json.dumps(result2)
#     except Exception as e:
#         print(f"Error in controller handle: {e}", file=sys.stderr)
#         return json.dumps({"error": str(e)})

# if __name__ == "__main__":
#     handle()
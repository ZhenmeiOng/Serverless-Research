import json
def handle(req):
    print("running callee...")
    str_1 = "hello this is the callee!"
    
    # convert Python dictionary to a json object
    return json.dumps({"data": str_1})

#----------------------------------------------------------------------------------

# # this is claude's code
# import json
# import sys

# def handle(req):
#     print("running callee...")
#     # Check if we received any input
#     try:
#         # Parse incoming request if it's a string
#         if isinstance(req, str):
#             req_data = json.loads(req)
#         else:
#             req_data = req
        
#         str_1 = "hello this is the callee!"
#         return json.dumps({"data": str_1})
#     except json.JSONDecodeError as e:
#         print(f"Error parsing input in callee: {e}", file=sys.stderr)
#         return json.dumps({"error": "Invalid input format"})

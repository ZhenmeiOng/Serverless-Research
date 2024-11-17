import json
import sys

def handle(req):
    print("running caller...")
    # the controller's handle will pass in a json object to this handle
    # hence, `req` here will ba a json object
    data = json.loads(req)

    # since in our callee, we returns a python dictionary as a json object
    # and we used "data" as the key in the dictionary,
    # here we will check the value in "data"
    if "data" in data:
        print(data['data'], file=sys.stderr)
        # return a python dict as a json object
        return json.dumps({'status': "Chain functions call success.", 'data': data['data']})
    else:
        return json.dumps({'error': "Chain functions call failed."})

#----------------------------------------------------------------------------------

# # this is claude's code
# import json
# import sys

# def handle(req):
#     print("running caller...", file=sys.stderr)
#     try:
#         # Handle both string and dict inputs
#         if isinstance(req, str):
#             data = json.loads(req)
#         else:
#             data = req

#         if "data" in data:
#             print(f"Received data: {data['data']}", file=sys.stderr)
#             return json.dumps({'status': "Chain functions call success."})
#         else:
#             return json.dumps({'error': "Chain functions call failed."})
#     except json.JSONDecodeError as e:
#         print(f"Error parsing input in caller: {e}", file=sys.stderr)
#         return json.dumps({'error': f"Invalid input format: {str(e)}"})

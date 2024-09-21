# import logging
# import azure.functions as func
# import json
# import pickle
# import numpy as np

# # # Load the pre-trained model from file
# # with open('linear_model.pkl', 'rb') as f:
# #     model = pickle.load(f)

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     try:
#         # Load the pre-trained model from file
#         with open('linear_model.pkl', 'rb') as f:
#             model = pickle.load(f)
#         # Parse the input data from the request body
#         req_body = req.get_json()
#         data = req_body.get('data')
        
#         if data is None:
#             return func.HttpResponse("Please pass 'data' in the request body", status_code=400)

#         # Convert input to numpy array for model prediction
#         input_data = np.array(data).reshape(-1, 1)
        
#         # Make prediction
#         prediction = model.predict(input_data)

#         return func.HttpResponse(
#             json.dumps({'prediction': prediction.tolist()}),
#             mimetype="application/json"
#         )
#     except Exception as e:
#         logging.error(f"Error occurred: {e}")
#         return func.HttpResponse(f"Error occurred: {e}", status_code=500)

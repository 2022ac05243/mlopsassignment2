import logging
import azure.functions as func
import json
import pickle
import numpy as np
import time
from sklearn.metrics import r2_score, mean_squared_error

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="linear_reggression")
def linear_reggression(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Load the pre-trained model from file
        with open('linear_model.pkl', 'rb') as f:
            model = pickle.load(f)
        # Parse the input data from the request body
        req_body = req.get_json()
        data = req_body.get('data')
        
        if data is None:
            return func.HttpResponse("Please pass 'data' in the request body", status_code=400)

        # Convert input to numpy array for model prediction
        input_data = np.array(data).reshape(-1, 1)
        
        # Make prediction
        prediction = model.predict(input_data)

        return func.HttpResponse(
            json.dumps({'prediction': prediction.tolist()}),
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(f"Error occurred: {e}", status_code=500)

@app.route(route="liner_reggression_with_metric")
def liner_reggression_with_metric(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Load the pre-trained model from file
        with open('linear_model.pkl', 'rb') as f:
            model = pickle.load(f)

        # Parse the input data from the request body
        req_body = req.get_json()
        data = req_body.get('data')
        actual_values = req_body.get('actual_values', None)  # Actual values for performance metrics (optional)

        if data is None:
            return func.HttpResponse("Please pass 'data' in the request body", status_code=400)

        # Convert input to numpy array for model prediction
        input_data = np.array(data).reshape(-1, 1)
        
        # Measure prediction time
        start_time = time.time()
        prediction = model.predict(input_data)
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Prepare the response
        response = {
            'prediction': prediction.tolist(),
            'execution_time': execution_time
        }

        # Calculate performance metrics if actual values are provided
        if actual_values is not None:
            actual_values = np.array(actual_values).reshape(-1, 1)
            r2 = r2_score(actual_values, prediction)
            mse = mean_squared_error(actual_values, prediction)
            response['r2_score'] = r2
            response['mean_squared_error'] = mse

        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(f"Error occurred: {e}", status_code=500)

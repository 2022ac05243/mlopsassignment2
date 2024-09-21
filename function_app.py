import logging
import azure.functions as func
import json
import pickle
import numpy as np

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
            # json.dumps({'prediction': 'results'}),
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(f"Error occurred: {e}", status_code=500)

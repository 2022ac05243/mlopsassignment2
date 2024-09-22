import logging
import azure.functions as func
import json
import pickle
import numpy as np
import time
import pandas as pd

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

@app.route(route="diabatic_model")
def diabatic_model(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Load the pre-trained model from file
        with open('diabetes_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('diabetes_scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        # Parse the input data from the request body
        req_body = req.get_json()
        data = req_body.get('data')
        

        if data is None:
            return func.HttpResponse("Please pass 'data' in the request body", status_code=400)

        feature_names = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age']
    
        # Extract features from the request data
        features = {
            'pregnancies': [data['pregnancies']],
            'glucose': [data['glucose']],
            'blood_pressure': [data['blood_pressure']],
            'skin_thickness': [data['skin_thickness']],
            'insulin': [data['insulin']],
            'bmi': [data['bmi']],
            'diabetes_pedigree_function': [data['diabetes_pedigree_function']],
            'age': [data['age']]
        }

        # Convert features to a DataFrame and apply scaling
        features_df = pd.DataFrame(features, columns=feature_names)
        features_scaled = scaler.transform(features_df)

        prediction = model.predict(features_scaled)[0]
        result = 'Diabetes' if prediction == 1 else 'No Diabetes'

        response = {
            'prediction': result,
        }

        # return jsonify({'prediction': result, 'ok': 'true'})
        return func.HttpResponse(
                json.dumps(response),
                mimetype="application/json"
            )

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(f"Error occurred: {e}", status_code=500)

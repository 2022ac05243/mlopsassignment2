import logging
import azure.functions as func
import json
import pickle
import numpy as np
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
        # return func.HttpResponse(
        #         json.dumps('hello'),
        #         mimetype="application/json"
        #     )

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(f"Error occurred: {e}", status_code=500)

# @app.route('/')
# def index():
#     # Render the main index.html page
#     return render_template('index.html')


# import logging
# import azure.functions as func
# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# import json
# import pickle
# import numpy as np
# import pandas as pd

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# @app.route("/")
# def index():
#     return render_template('index.html')

# @app.route("/http_trigger", methods=["POST"])
# def http_trigger():
#     logging.info('Python HTTP trigger function processed a request.')

#     req_body = request.get_json()
#     name = req_body.get('name') if req_body else None

#     if name:
#         return jsonify(message=f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return jsonify(message="This HTTP triggered function executed successfully. Pass a name in the request body."), 200

# @app.route("/linear_reggression", methods=["POST"])
# def linear_reggression():
#     try:
#         # Load the pre-trained model from file
#         with open('linear_model.pkl', 'rb') as f:
#             model = pickle.load(f)
        
#         req_body = request.get_json()
#         data = req_body.get('data')

#         if data is None:
#             return jsonify(error="Please pass 'data' in the request body"), 400

#         # Convert input to numpy array for model prediction
#         input_data = np.array(data).reshape(-1, 1)
#         prediction = model.predict(input_data)

#         return jsonify(prediction=prediction.tolist())

#     except Exception as e:
#         logging.error(f"Error occurred: {e}")
#         return jsonify(error=f"Error occurred: {e}"), 500

# @app.route("/diabatic_model", methods=["POST"])
# def diabatic_model():
#     try:
#         # Load the pre-trained model and scaler from file
#         with open('diabetes_model.pkl', 'rb') as f:
#             model = pickle.load(f)
#         with open('diabetes_scaler.pkl', 'rb') as f:
#             scaler = pickle.load(f)

#         req_body = request.get_json()
#         data = req_body.get('data')

#         if data is None:
#             return jsonify(error="Please pass 'data' in the request body"), 400

#         # Extract features from the request data
#         feature_names = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age']
#         features = {key: [data[key]] for key in feature_names}

#         # Convert features to a DataFrame and apply scaling
#         features_df = pd.DataFrame(features, columns=feature_names)
#         features_scaled = scaler.transform(features_df)

#         prediction = model.predict(features_scaled)[0]
#         result = 'Diabetes' if prediction == 1 else 'No Diabetes'

#         return jsonify(prediction=result)

#     except Exception as e:
#         logging.error(f"Error occurred: {e}")
#         return jsonify(error=f"Error occurred: {e}"), 500

# # Azure Function entry point
# def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
#     """Azure Functions entry point that handles HTTP requests and passes them to the Flask app."""
#     return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

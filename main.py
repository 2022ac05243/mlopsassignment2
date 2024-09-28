from flask import Flask, render_template, request, jsonify
# import json
# import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Your template in the "templates" folder

# def predict():
#     data = request.get_json(force=True)
#     # Print the received values for debugging
#     print("Received features:", data)
#     feature_names = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age']
    
#     # Extract features from the request data
#     features = {
#         'pregnancies': [data['pregnancies']],
#         'glucose': [data['glucose']],
#         'blood_pressure': [data['blood_pressure']],
#         'skin_thickness': [data['skin_thickness']],
#         'insulin': [data['insulin']],
#         'bmi': [data['bmi']],
#         'diabetes_pedigree_function': [data['diabetes_pedigree_function']],
#         'age': [data['age']]
#     }

#     # Convert features to a DataFrame and apply scaling
#     features_df = pd.DataFrame(features, columns=feature_names)
#     features_scaled = scaler.transform(features_df)

#     prediction = model.predict(features_scaled)[0]
#     result = 'Diabetes' if prediction == 1 else 'No Diabetes'
  
#     return jsonify({'prediction': result, 'ok': 'true'})

# @app.route('/predict', methods=['POST'])
# def predict():
#     print('thanks for click')
#     # Get the incoming data from the request
#     data = request.get_json(force=True)
    
#     # Print the received values for debugging
#     print("Received features:", data)

#     # # Prepare the payload for the external API (make sure the structure matches what the API expects)
#     # api_data = {
#     #     "data": {
#     #         "pregnancies": data.get("pregnancies", 6),  # default values if keys not found
#     #         "glucose": data.get("glucose", 148),
#     #         "blood_pressure": data.get("bloodPressure", 72),
#     #         "skin_thickness": data.get("skinThickness", 35),
#     #         "insulin": data.get("insulin", 0),
#     #         "bmi": data.get("bmi", 33.6),
#     #         "diabetes_pedigree_function": data.get("diabetesPedigreeFunction", 0.627),
#     #         "age": data.get("age", 50)
#     #     }
#     # }

#     # # Make the POST request to the external API
#     # try:
#     #     response = requests.post(
#     #         'https://mlopsassigment2.azurewebsites.net/api/diabatic_model?code=ApY_47QZjGvYh4a0nwZ0nHd49YILiSxjZKpoDNlmQ2FBAzFuJkJQfQ%3D%3D',
#     #         json=api_data
#     #     )

#     #     # Ensure the request was successful
#     #     response.raise_for_status()

#     #     # Parse the JSON response
#     #     result = response.json()

#     #     # Return the prediction result
#     #     return jsonify({'prediction': result.get('prediction', 'No prediction available'), 'ok': 'true'})
    
#     # except requests.exceptions.RequestException as e:
#     #     print(f"Error occurred: {e}")
#     #     return jsonify({'error': 'Unable to get prediction', 'ok': 'false'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

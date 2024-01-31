import pickle
from flask import Flask, jsonify, render_template, request

from scripts.ICU_predict_service import predict_single

app = Flask('ICU-predict')

with open('./models/ICU-model.pck', 'rb') as f:
    dv, model = pickle.load(f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET'])
def predict_get():
    return 'Esta ruta solo acepta solicitudes GET.'


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            customer = request.get_json()
            ICU, prediction = predict_single(customer, dv, model)

            result = {
                'ICU': bool(ICU),
                'ICU_probability': float(prediction),
            }

            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        # Si es una solicitud GET, renderizar el template
        return render_template('predict.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

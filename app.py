#import the required libraries
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pickle

app = Flask(__name__)

@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route('/show_prediction', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #extracting the inputs entered by the user
            gre_score = float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']
            if(is_research == 'yes'):
                research = 1
            else:
                research = 0
            model_filename = 'finalized_model.pickle'
            scaler_filename = 'scaler.pickle'
            model = pickle.load(open(model_filename,'rb')) #load the finalized model
            scaler = pickle.load(open(scaler_filename, 'rb')) #load the scaler object
            # Transform the input data
            input_scaled = scaler.transform([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]])
            # Predict using the loaded model
            prediction = model.predict(input_scaled)
            print(f'the predicted chance of admit is {prediction}')
            return render_template('results.html', prediction = round(prediction[0]*100))

        except Exception as e:
            raise Exception(f'Something went wrong - {str(e)}')

if __name__ == "__main__":
    app.run()
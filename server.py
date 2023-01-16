# Import libraries
import numpy as np
import pickle
from flask import Flask, request, jsonify, render_template
from tweet_scrape import get_account_info_and_scrape_tweets as scrape_tweets

app = Flask(__name__)

# Load the model
model = pickle.load(open('model.pkl','rb'))

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        if username:
            account_info = scrape_tweets(username)
            print(account_info)
            print(account_info[0])
            int_features = [float(x) for x in account_info[0].values()]
            final_features = [np.array(int_features)]
            prediction = model.predict(final_features)

            output = round(prediction[0], 2)

            return render_template('index.html', prediction_text='Buzzer Prediction : {}'.format(output),
            account_age = account_info[0].get("account_age"),
            following = account_info[0].get("following"),
            followers = account_info[0].get("followers"),
            compound_mean = account_info[0].get("compound_mean"))
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')
@app.route('/predict',methods=['POST'])
def predict():


    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Buzzer Prediction : {}'.format(output))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
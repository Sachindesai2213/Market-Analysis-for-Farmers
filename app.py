from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

items = ['Arive greens', 'Banana cooking R.Banana', 'Basale Greens',
       'Beet Root', 'Brinjal (R)', 'Brinjal (W)',
       'Brinjal Bottle', 'Brucoli', 'Cabbage',
       'Cabbage Red', 'Cabbage chaina',
       'Capsicum Red/Yellow', 'Cauliflower(M)',
       'Chakota greens', 'Chikadi kai',
       'Chillies Green', 'Chillies small (C.B.P)',
       'Chow-Chow', 'Coconut (B)', 'Coconut (M)',
       'Coconut (OS)', 'Coconut (S)', 'Copra',
       'Dry dates', 'Eggs', 'Garlic cleaned',
       'Greens Sabbakki', 'Ground nut Local',
       'Herali kai', 'Hesaru kalu', 'Jukani',
       'Kakadi', 'Kiwi fruit', 'Leeks',
       'Little gourd', 'Mangalore cucumber',
       'Molake kalu', 'Mushroom Button',
       'Onion samber', 'Palak Greens', 'Parsley',
       'Pumpkin Ash', 'Pumpkin Japan',
       'Pumpkin Red', 'Raddish', 'Selari',
       'Sham gadde', 'Spring Onion',
       'Sweet Potato(Genasu)', 'Sweet corn',
       'Tamarind seedless', 'Tender Coconut(S)',
       'Yam/S.Root', 'knol-khol']

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html", items=items)




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date = request.form["date"]
        day = int(pd.to_datetime(date, format="%Y-%m-%d").day)
        month = int(pd.to_datetime(date, format ="%Y-%m-%d").month)
        item_name=request.form['item_name']
        output_list = [day, month]
        for item in items:
            if item == item_name:
                output_list.append(1)
            else:
                output_list.append(0)

        
        prediction=model.predict([output_list])

        output=round(prediction[0],2)

        return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output), items=items)


    return render_template("home.html", items=items)




if __name__ == "__main__":
    app.run(debug=True)

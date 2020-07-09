#importing necessary libraries
import  jsonify
import  requests
import  pickle
import  numpy as np
import  sklearn

from  flask   import Flask , render_template, request
from  sklearn.preprocessing  import  StandardScaler

#initialise flask 
app = Flask(__name__)


#load a saved model from  local system
model = pickle.load(open('insurance_model.pickle', 'rb'))

#home page route
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


#prediction route
standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        #try for read and predict
        try:
            age = int(request.form['age'])
            sex=int(request.form['sex'])
            bmi=float(request.form['bmi'])
            children=int(request.form['children'])
            smoker=int(request.form['smoker'])
            region=int((request.form['region']).split("=")[1])
            
            #make prediction from loaded model
            prediction=model.predict([[age,sex,bmi,children,smoker,region]])
            output=round(prediction[0],2)
            if output<0:
                return render_template('index.html',prediction_texts="Not Eligible")
            else:
                return render_template('index.html',prediction_text=output)
        #if fails redirect to same home page        
        except:
            return render_template('index.html')


#start app main route
if __name__=="__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0",port=8080)


from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import pandas as pd

app = Flask(__name__)
api = Api(app)

@app.route('/words')
def get():
    #allow multiple languages to be passed in the url
    language = request.args.get('language')

    #allow multiple words to be passed in the url
    word = request.args.get('word')

    df = pd.read_csv('censor_datasheet.csv')

    # allow multiple languages to be passed in the url
    if "," in language:
        language = language.split(",")

        # check the word is censored in all the extra languages
        for i in range(len(language)):
            for j in range(len(df)):
                if df.iloc[j,0] == word and df.iloc[j,1] == language[i]:
                    return "Censored"
        return "Not Censored"

    
    #row 0 is the word and row 1 is the language
    for i in range(len(df)):
        #check if the word in the url has a space in it represneted by _ 
        if "_" in word:
            word = word.replace("_", " ")
            
        if df.iloc[i,0] == word and df.iloc[i,1] == language:
            return "Censored"
        
        # if language is all then check if the word is censored in any language
        if df.iloc[i,0] == word and language == "all":
            return "Censored"
        
    return "Not Censored"

if __name__ == '__main__':
    app.run()
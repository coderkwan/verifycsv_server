# flask-api/flaskr/__init__.py
from flask import Flask,request, make_response, jsonify
import csv,re,os

app = Flask(__name__)

pattern = re.compile(r'\[\s*"([^"]*)"\s*,\s*"([^"]*)"\s*\]')
def is_valid_string(input_str):
    return bool(pattern.match(input_str))

specs = ['spec_1', 'spec_2','spec_3', 'spec_4', 'spec_5', 'spec_6','spec_7', 'spec_8','spec_9', 'spec_10', 'spec_11', 'spec_12','spec_13', 'spec_14','spec_15']

error_rows = []

@app.route("/", methods=['POST'])
def hello():
    if(request.files['csv_file']):
        error_rows = []
        request.files['csv_file'].save('./csv_file.csv')
        with open('csv_file.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile)

            for row in spamreader:
                item = {
                    "id" : row['id'],
                    "column": [],
                    "data": []
                }

                for x in specs:
                    if not is_valid_string(row[x].strip()) and row[x] != "NULL":
                        item['column'].append(x)
                        item['data'].append(row[x])
                        
                if(len(item['column']) > 0):
                    error_rows.append(item)

        os.remove('./csv_file.csv')
        response = jsonify(error_rows)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        response = jsonify("error")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

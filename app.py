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





@app.route("/products", methods=['POST'])
def products():
    error_products = []

    types = []
    sub_types = []
    sub_types_ids = []
    sub_sub_types = []
    sub_sub_types_ids = []

    applications = []
    sub_applications = []
    sub_applications_ids = []

    segments = []
    sub_segments = []
    sub_segments_ids = []

    request.files['csv_products'].save('./csv_products.csv')

    request.files['csv_types'].save('./csv_types.csv')
    request.files['csv_sub_types'].save('./csv_sub_types.csv')
    request.files['csv_sub_sub_types'].save('./csv_sub_sub_types.csv')
    
    request.files['csv_applications'].save('./csv_applications.csv')
    request.files['csv_sub_applications'].save('./csv_sub_applications.csv')

    request.files['csv_segments'].save('./csv_segments.csv')
    request.files['csv_sub_segments'].save('./csv_sub_segments.csv')

    with open('csv_types.csv', newline='') as csvtypes:
        spamreader = csv.DictReader(csvtypes)
        for row in spamreader:
            types.append(row['id'])

    with open('csv_sub_types.csv', newline='') as csvsubtypes:
        spamreader = csv.DictReader(csvsubtypes)
        for row in spamreader:
            item = {
                "id" : row['id'],
                "parent_id": row['parent_id'],
            }
            sub_types.append(item)
            sub_types_ids.append(row['id'])

    with open('csv_sub_sub_types.csv', newline='') as csvsubsubtypes:
        spamreader = csv.DictReader(csvsubsubtypes)
        for row in spamreader:
            item = {
                "id" : row['id'],
                "parent_id": row['parent_id'],
            }
            sub_sub_types.append(item)
            sub_sub_types_ids.append(row['id'])

    with open('csv_applications.csv', newline='') as csvapplications:
            spamreader = csv.DictReader(csvapplications)
            for row in spamreader:
                applications.append(row['id'])

    with open('csv_sub_applications.csv', newline='') as csvsubapplications:
        spamreader = csv.DictReader(csvsubapplications)
        for row in spamreader:
            item = {
                "id" : row['id'],
                "parent_id": row['parent_id'],
            }
            sub_applications.append(item)
            sub_applications_ids.append(row['id'])

    with open('csv_segments.csv', newline='') as csvsegments:
            spamreader = csv.DictReader(csvsegments)
            for row in spamreader:
                segments.append(row['id'])

    with open('csv_sub_segments.csv', newline='') as csvsubsegments:
        spamreader = csv.DictReader(csvsubsegments)
        for row in spamreader:
            item = {
                "id" : row['id'],
                "parent_id": row['parent_id'],
            }
            sub_segments.append(item)
            sub_segments_ids.append(row['id'])

    with open('csv_products.csv', newline='') as csvproducts:
        spamreader = csv.DictReader(csvproducts)

        for row in spamreader:
            item = {
                    'id': row['id'],
                    'code': row['Product Code'],
                    'columns': [],
                    'comments': []
            }
            my_sub_types = row['prod_type_sub_id'].split(",")
            my_sub_sub_types = row['prod_type_sub_sub_id'].split(",")
            my_applications = row['prod_application_id'].split(",")
            my_sub_applications = row['prod_application_sub_id'].split(",")
            my_segments = row['prod_market_segments_id'].split(",")
            my_sub_segments = row['prod_market_segments_sub_id'].split(",")

            if(row['prod_type_id'].strip() != "" and row['prod_type_id'].strip() not in types):
                item['columns'].append("Types")
                item['comments'].append("Type Id does not exist on Types table")

            for x in my_sub_types:
                if(x.strip() != ''):
                    if(x.strip() not in sub_types_ids):
                        item['columns'].append("Sub Types")
                        item['comments'].append("Sub Type Id does not exist on Sub Types table")
                        break
                    else:
                        breaker = False
                        for v in sub_types:
                            if(x.strip() == v['id']):
                                if(v['parent_id'] != row['prod_type_id'].strip()):
                                    item['columns'].append("Sub Types")
                                    item['comments'].append("Sub Type Id does not belong to Type")
                                    breaker = False
                                    breaker = True
                                break
                    if(breaker == True):
                        break


                
            for l in my_sub_sub_types:
                if(l.strip() != ''):
                    if(l.strip() not in sub_sub_types_ids):
                        item['columns'].append("Sub Sub Types")
                        item['comments'].append("Sub Sub Type Id does not exist on Sub Sub Types table")
                        break
                    else:
                        breaker = False
                        for g in sub_sub_types:
                            if(l.strip() == g['id']):
                                if(g['parent_id'] not in my_sub_types):
                                    item['columns'].append("Sub Sub Types")
                                    item['comments'].append("Sub Sub Type Id does not belong to Sub Type")
                                    breaker = True
                                    break
                    if(breaker == True):
                        break

            for x in my_applications:
                if(x.strip() != '' and x.strip() not in applications):
                    item['columns'].append("Applications")
                    item['comments'].append("Applications Id does not exist on Applications table")
                    break

            for f in my_sub_applications:
                if(f.strip() != ''):
                    if(f.strip() not in sub_applications_ids):
                        item['columns'].append("Sub Applications")
                        item['comments'].append("Sub Applications Id does not exist on Sub Applications table")
                        break
                    else:
                        breaker = False
                        for g in sub_applications:
                            if(f.strip() == g['id']):
                                if(g['parent_id'] not in my_applications):
                                    item['columns'].append("Sub Applications")
                                    item['comments'].append("Sub Applications Id does not belong to Applications")
                                    breaker = True
                                break
                        
                        if(breaker):
                            break

            for x in my_segments:
                if(x.strip() != '' and x.strip() not in segments):
                    item['columns'].append("Segments")
                    item['comments'].append("Segments Id does not exist on Segments table")
                    break

            for c in my_sub_segments:
                if(c.strip() != '' ):
                    if(c.strip() != '' and c.strip() not in sub_segments_ids):
                        item['columns'].append("Sub Segments")
                        item['comments'].append("Sub Segments Id does not exist on Sub Segments table")
                        break
                    else:
                        breaker = False
                        for g in sub_segments:
                            if(c.strip() == g['id']):
                                if(g['parent_id'] not in my_segments):
                                    item['columns'].append("Sub Segments")
                                    item['comments'].append("Sub Segments Id does not belong to Segments")
                                    breaker = True
                                break
                        if(breaker == True):
                            break

            if(len(item['columns'])>0):
                error_products.append(item)

    os.remove('./csv_products.csv')
    os.remove('./csv_types.csv')
    os.remove('./csv_sub_types.csv')
    os.remove('./csv_sub_sub_types.csv')
    os.remove('./csv_applications.csv')
    os.remove('./csv_sub_applications.csv')
    os.remove('./csv_segments.csv')
    os.remove('./csv_sub_segments.csv')
    response = jsonify(error_products)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
   


from flask import Flask, request, jsonify
import os
import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'
#cors = CORS(app)
system_base_path = '/home/kshitij.singh/files/kushagra/billr_api/static/db/'


@app.route("/")
#@cross_origin()
def health_check():
    return "<h1 style='color:blue'>Working! 200 OK </h1>"


@app.route('/api/v1/bills/<phone>')
#@cross_origin()
def fetch_bills(phone):

    user_bill_path = os.path.join(system_base_path, str(phone))
    domain_base_path = f'{request.host}/static/db'
    if os.path.exists(user_bill_path):
        shops_visited = os.listdir(user_bill_path)
        bills_list = []
        for shop in shops_visited:
            shop_bills = os.listdir(os.path.join(user_bill_path, shop))
            for bill in shop_bills:
                amount = 0.0
                if '_' not in bill:
                    timestamp = bill.split('.')[0]
                else:
                    val = bill.split('_')
                    timestamp = val[0]
                    amount = val[1].split('.pdf')[0]
                timestamp = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S')
                external_bill_path = os.path.join(domain_base_path, str(phone), shop, bill)
                single_bill_data = {'purchaseDate': timestamp,
                                    'amount': str(amount),
                                    'storeName': shop,
                                    'url': external_bill_path
                                   }
                bills_list.append(single_bill_data)
        return(jsonify(bills_list))
    else:
        return(jsonify({"Error": "404. No record found"}))




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8999)




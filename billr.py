from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/billr"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app)
system_base_path = "/home/kshitij.singh/files/kushagra/billr_api/static/db/"


class StoresModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    owner = db.Column(db.Integer())
    phone_number = db.Column(db.Integer())
    uid = db.Column(db.String())

    def __init__(self, name, address, owner, phone_number, uid):
        self.name = name
        self.address = address
        self.owner = owner
        self.phone_number = phone_number
        self.uid = uid

    def __repr__(self):
        return f"<Store {self.name}>"


@app.route("/")
# @cross_origin()
def health_check():
    return "<h1 style='color:blue'>Working! 200 OK </h1>"


@app.route("/api/v1/bills/<phone>")
# @cross_origin()
def fetch_bills(phone):

    user_bill_path = os.path.join(system_base_path, str(phone))
    domain_base_path = f"{request.host}/static/db"
    if os.path.exists(user_bill_path):
        shops_visited = os.listdir(user_bill_path)
        bills_list = []
        for shop in shops_visited:
            shop_bills = os.listdir(os.path.join(user_bill_path, shop))
            for bill in shop_bills:
                amount = 0.0
                if "_" not in bill:
                    timestamp = bill.split(".")[0]
                else:
                    val = bill.split("_")
                    timestamp = val[0]
                    amount = val[1].split(".pdf")[0]
                timestamp = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
                external_bill_path = os.path.join(
                    domain_base_path, str(phone), shop, bill
                )
                single_bill_data = {
                    "purchaseDate": timestamp,
                    "amount": str(amount),
                    "storeName": shop,
                    "url": external_bill_path,
                }
                bills_list.append(single_bill_data)
        return jsonify(bills_list)
    else:
        return jsonify({"Error": "404. No record found"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8999)

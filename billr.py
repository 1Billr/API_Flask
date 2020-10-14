from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime
import shortuuid
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/billr"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import StoresModel

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app)
system_base_path = "/home/kshitij.singh/files/kushagra/billr_api/static/db/"


@app.route("/")
# @cross_origin()
def health_check():
    return "<h1 style='color:blue'>Working! 200 OK </h1>"


@app.route("/api/v1/merchant/<int:phone>/passkey", methods=["POST"])
def generate_merchant_passkey(phone):
    if (
        db.session.query(StoresModel).filter(StoresModel.phone_number == phone).count()
        == 0
    ):
        passkey = shortuuid.ShortUUID().random(length=10)
        try:
            data = StoresModel(None, None, None, phone, passkey)
            db.session.add(data)
            db.session.commit()
            return jsonify({"success": True, "passkey": passkey, "phone": phone})
        except:
            return jsonify({"success": False, "Error": "Failed to generate passkey !"})
    else:
        return jsonify(
            {"success": False, "Error": "Merchant already has a passkey generated !"}
        )


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


@app.errorhandler(404)
def error_handler(e):
    return jsonify(
        {"success": False, "Error": "Cannot find the specified route !" + str(e)}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8999)

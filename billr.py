from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timezone
import os
import datetime
import shortuuid
import domain
from flask_cors import CORS, cross_origin
from multiprocessing import Pool

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/billr"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import StoresModel, BillsModel

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app)
system_base_path = "/home/kshitij.singh/files/kushagra/billr_api/static/db/"


@app.route("/")
# @cross_origin()
def health_check():
    return "<h1 style='color:blue'>Working! 200 OK </h1>"


""" Merchant related routes"""


@app.route("/api/v1/merchant/<int:phone>")
def check_if_merchant_exists(phone):
    if (
        db.session.query(StoresModel)
        .filter(StoresModel.phone_number == phone)
        .filter(StoresModel.passkey_exhausted == True)
        .count()
        != 0
    ):
        return jsonify({"success": True, "exists": True})
    else:
        return jsonify({"success": True, "exists": False})


@app.route("/api/v1/merchant/<int:phone>/profile")
def profile_details(phone):
    if (
        db.session.query(StoresModel).filter(StoresModel.phone_number == phone).count()
        != 0
    ):
        return jsonify(
            {"success": True, "data": StoresModel.get_store_by_phone(phone).serialize}
        )
    else:
        return (
            jsonify(
                {"success": False, "error": "Profile details not found for user !"}
            ),
            400,
        )


@app.route("/api/v1/merchant/<int:phone>", methods=["DELETE"])
def delete_store_details(phone):
    if (
        db.session.query(StoresModel).filter(StoresModel.phone_number == phone).count()
        != 0
    ):
        db.session.query(StoresModel).filter(StoresModel.phone_number == phone).delete()
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 400


@app.route("/api/v1/store/<int:storeId>/bills")
def get_store_bills(storeId):
    if (
        db.session.query(StoresModel).filter(StoresModel.store_ID == storeId).count()
        != 0
    ):
        limit = request.args.get("limit", default=0, type=int)
        offset = request.args.get("offset", default=0, type=int)
        query = request.args.get("q", default="*", type=str)
        if query != "*":
            data = [
                e.serialize_basic_details
                for e in BillsModel.get_bills_by_search(storeId, query)
            ]
        else:
            data = [
                e.serialize_basic_details
                for e in BillsModel.get_bills_by_store(storeId)
            ]
        if offset != 0:
            data = data[offset : len(data)]
        if limit != 0:
            data = data[0:limit]

        return jsonify({"success": True, "data": data})
    else:
        return (
            jsonify({"success": False, "error": "No store with store id found !"}),
            200,
        )


@app.route("/api/v1/store/<int:storeId>/bills/detail")
def get_store_details(storeId):
    store_count = (
        db.session.query(StoresModel).filter(StoresModel.store_ID == storeId).count()
    )
    if store_count != 0:
        data = [
            e.serialize_basic_details for e in BillsModel.get_bills_by_store(storeId)
        ]
        bill_count = len(data)
        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "totalBills": bill_count,
                        "totalStores": 1,
                        "totalPagesSaved": bill_count,
                    },
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"success": True, "error": "No such store found !"}),
            200,
        )


@app.route("/api/v1/merchant/<int:phone>/generate/passkey", methods=["POST"])
def generate_merchant_passkey(phone):
    if (
        db.session.query(StoresModel).filter(StoresModel.phone_number == phone).count()
        == 0
    ):
        passkey = shortuuid.ShortUUID().random(length=10)
        storeID = shortuuid.ShortUUID(alphabet="0123456789").random(length=5)
        try:
            data = StoresModel(None, None, None, phone, passkey, False, storeID)
            data.save
            return jsonify({"success": True, "passkey": passkey, "phone": phone})
        except Exception as e:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Failed to generate passkey : " + str(e),
                    }
                ),
                500,
            )
    else:
        return jsonify(
            {"success": False, "error": "Merchant already has a passkey generated !"}
        )


@app.route("/api/v1/merchant/<int:phone>/passkey", methods=["POST"])
def check_valid_passkey(phone):
    if not request.json or not "passkey" in request.json:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Please provide a passkey !",
                }
            ),
            400,
        )
    if (
        db.session.query(StoresModel)
        .filter(StoresModel.passkey == request.json["passkey"])
        .filter(StoresModel.phone_number == phone)
        .filter(StoresModel.passkey_exhausted == False)
        .count()
        == 0
    ):
        return jsonify(
            {"success": True, "error": " Not a valid passkey !", "valid": False}
        )
    else:
        return jsonify({"success": True, "valid": True})


@app.route("/api/v1/merchant/<int:phone>/store", methods=["PUT"])
def add_store_details(phone):
    if (
        db.session.query(StoresModel).filter(StoresModel.phone_number == phone).count()
        != 0
    ):
        if not request.json or not ("owner" and "name" and "address") in request.json:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Please provide all the required details !",
                    }
                ),
                400,
            )
        try:
            store = StoresModel.get_store_by_phone(phone)
            store.updateStore(
                request.json["name"], request.json["address"], request.json["owner"]
            )
            return (
                jsonify(
                    {
                        "success": True,
                        "data": StoresModel.get_store_by_phone(phone).serialize,
                    }
                ),
                201,
            )
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        return jsonify(
            {
                "success": False,
                "error": "Merchant with given phone no. doesn't exists !",
            }
        )


@app.route("/api/v1/store/<int:storeID>/bill", methods=["PUT"])
def add_new_bill(storeID):
    if (
        db.session.query(StoresModel).filter(StoresModel.store_ID == storeID).count()
        != 0
    ):
        if not request.json:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Please provide the required details !",
                    }
                ),
                400,
            )
        try:
            data = request.json
            details = request.json["billDetails"]
            # validate if customer's bill already has been generated

            duplicate_bills = [
                e.serialize_basic_details
                for e in BillsModel.get_bills_by_phone_amount_and_store(
                    storeID, details["customerPhoneNumber"], details["invoiceAmount"]
                )
            ]
            curr_time_last_10_min = datetime.datetime.now(tz=timezone.utc).replace(
                tzinfo=None
            )
            if len(duplicate_bills) > 0:
                time_diff = curr_time_last_10_min - duplicate_bills[0]["createdAt"]
                if time_diff.seconds <= 60:
                    return (
                        jsonify(
                            {
                                "success": False,
                                "error": "Bill has been already generated for the customer",
                            }
                        ),
                        400,
                    )

            bill = BillsModel(
                storeID,
                data["owner"],
                data["storePhoneNumber"],
                details["customerName"],
                details["customerEmail"],
                details["customerPhoneNumber"],
                details["invoiceAmount"],
                details["otherDetails"],
                details["items"],
            )
            savedBill = bill.save
            storeData = StoresModel.get_store_by_id(storeID).serialize
            billpath = domain.generate_pdf(savedBill, storeData)
            bill_url = domain_base_path = f"{request.host}/" + billpath
            billUrl = {"bill": bill_url}
            return (
                jsonify(
                    {
                        "success": True,
                        "data": {**savedBill, **billUrl},
                    }
                ),
                201,
            )
        except Exception as e:
            return jsonify({"success": False, "error": "Field missing " + str(e)}), 500
    else:
        return jsonify(
            {
                "success": True,
                "error": "No store with given store Id exists in our system !",
            }
        )


""" Customer related routes """


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
    return jsonify({"success": False, "Error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8999)

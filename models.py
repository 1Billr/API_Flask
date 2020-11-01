from billr import db
import datetime
from sqlalchemy.dialects.postgresql import JSONB

"""Stores class to bills table """


class StoresModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    owner = db.Column(db.String())
    phone_number = db.Column(db.BigInteger())
    passkey = db.Column(db.String())
    passkey_exhausted = db.Column(db.Boolean())
    store_ID = db.Column(db.Integer())
    updated_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(
        self, name, address, owner, phone_number, passkey, passkey_exhausted, storeID
    ):
        self.name = name
        self.address = address
        self.owner = owner
        self.phone_number = phone_number
        self.passkey = passkey
        self.store_ID = storeID
        self.passkey_exhausted = passkey_exhausted
        self.updated_at = datetime.datetime.now()

    def __repr__(self):
        return f"<Store {self.name}>"

    def updateStore(self, name, address, owner):
        self.name = name
        self.address = address
        self.owner = owner
        self.passkey_exhausted = True
        self.updated_at = datetime.datetime.now()
        db.session.commit()

    @property
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_store_by_phone(phone):
        return StoresModel.query.filter_by(phone_number=phone).first()

    @staticmethod
    def get_store_by_id(id):
        return StoresModel.query.filter_by(store_ID=id).first()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "storeID": self.store_ID,
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "owner": self.owner,
        }

    @property
    def peek(self):
        print(
            "id : "
            + str(self.id)
            + " name : "
            + str(self.name)
            + " address : "
            + str(self.address)
            + " phone_number : "
            + str(self.phone_number)
            + " created_at : "
            + str(self.created_at)
            + " updated_at : "
            + str(self.updated_at)
            + " store_id : "
            + str(self.store_ID)
            + " passkey : "
            + str(self.passkey)
            + " passkey_exhausted : "
            + str(self.passkey_exhausted)
        )


"""bills class to bills table """


class BillsModel(db.Model):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer())
    owner_name = db.Column(db.String())
    store_phone_number = db.Column(db.BigInteger())
    customer_name = db.Column(db.String())
    customer_email = db.Column(db.String())
    customer_phone_number = db.Column(db.BigInteger())
    invoice_amount = db.Column(db.Float())
    other_details = db.Column(JSONB)
    items = db.Column(JSONB)
    bill_url = db.Column(db.String())
    updated_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(
        self,
        store_id,
        owner_name,
        store_phone_number,
        customer_name,
        customer_email,
        customer_phone_number,
        invoice_amount,
        other_details,
        items,
    ):
        self.store_id = store_id
        self.owner_name = owner_name
        self.store_phone_number = store_phone_number
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone_number = customer_phone_number
        self.invoice_amount = invoice_amount
        self.other_details = other_details
        self.updated_at = datetime.datetime.now()
        self.items = items

    def __repr__(self):
        return f"<Bill {self.name}>"

    @property
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.serialize

    @staticmethod
    def get_bills_by_store(id):
        return BillsModel.query.filter_by(store_id=id).order_by(
            BillsModel.created_at.desc()
        )

    @staticmethod
    def get_bills_by_search(id, q):
        return (
            BillsModel.query.filter(BillsModel.customer_name.ilike("%" + q + "%"))
            .filter_by(store_id=id)
            .order_by(BillsModel.created_at.desc())
        )

    @staticmethod
    def get_bills_by_phone_amount_and_store(id, phone, amount):
        return (
            BillsModel.query.filter_by(customer_phone_number=phone)
            .filter_by(store_id=id)
            .filter_by(invoice_amount=amount)
            .order_by(BillsModel.created_at.desc())
        )

    def add_bill_url(bill_url, bill_id):
        print(bill_url + " - " + str(bill_id))
        BillsModel.query.filter_by(id=bill_id).update({"bill_url": bill_url})
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "otherDetails": self.other_details,
            "invoiceAmount": self.invoice_amount,
            "customerPhoneNumber": self.customer_phone_number,
            "customerEmail": self.customer_email,
            "customerName": self.customer_name,
            "storePhoneNumber": self.store_phone_number,
            "ownerName": self.owner_name,
            "storeId": self.store_id,
            "id": self.id,
            "items": self.items,
        }

    @property
    def serialize_basic_details(self):
        """Return object data in easily serializable format"""
        return {
            "createdAt": self.created_at,
            "invoiceAmount": self.invoice_amount,
            "customerName": self.customer_name,
            "ownerName": self.owner_name,
            "bill": "https://slicedinvoices.com/pdf/wordpress-pdf-invoice-plugin-sample.pdf",
        }
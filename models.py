from billr import db
import datetime


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

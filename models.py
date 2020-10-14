from billr import db


class StoresModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    owner = db.Column(db.String())
    phone_number = db.Column(db.BigInteger())
    uid = db.Column(db.String())

    def __init__(self, name, address, owner, phone_number, uid):
        self.name = name
        self.address = address
        self.owner = owner
        self.phone_number = phone_number
        self.uid = uid

    def __repr__(self):
        return f"<Store {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def updateStore(self, name, address, owner):
        self.name = name
        self.address = address
        self.owner = owner
        db.session.commit()

    @staticmethod
    def get_store(phone):
        return StoresModel.query.filter_by(phone_number=phone).first()
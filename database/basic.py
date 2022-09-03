
from database.connection import get_db

class BasicCrud():

    def __init__(self, model):
        self.model = model
        self.db = get_db()

    def __del__(self):
        self.db.close()

    def get(self, id):
        return self.db.query(self.model).get(id)

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, obj_in):
        obj = self.model(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj, edit_data: list):
        for data in edit_data:
            setattr(obj, data['key'], data['value'])
        
        self.db.commit()
        return obj

    def delete(self, obj):
        self.db.delete(obj)
        self.db.commit()
        return obj
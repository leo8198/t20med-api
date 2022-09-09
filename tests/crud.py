from database.connection import get_db

# Class to get some data for the automated tests
class CrudHelper():

    # Get the last ID added to the table
    def get_last_result_id(self,model):
        '''Get the last ID added to the table'''

        db = get_db()

        # Get the last model id
        query = db.query(model).order_by(model.id.desc()).first()

        db.close()

        # If the is no result
        if query is None:
            return 1

        return query.id

    # Get the last result for the file name in the table Documents or Photos
    def get_last_result_name(self,model):
        '''Get the last result for the file name in the table Documents or Photos'''

        db = get_db()

        # Get the last model id
        query = db.query(model).order_by(model.id.desc()).first()

        db.close()

        # If the is no result
        if query is None:
            return 'teste1.png'

        return query.name

    def get_last_result(self,model):
        db = get_db()

        # Get the last model id
        query = db.query(model).order_by(model.id.desc()).first()

        db.close()

        # If the is no result
        if query is None:
            raise Exception("No data for this model")

        return query

    # Get the last result by cpf
    def get_last_result_cpf(self,model, cpf: str):
        '''Get the last result by cpf'''

        db = get_db()

        # Get the last model id
        query = db.query(model).filter(model.cpf == cpf).order_by(model.cpf.desc()).first()

        db.close()

        # If the is no result
        if query is None:
            return '123456789'

        return query.id
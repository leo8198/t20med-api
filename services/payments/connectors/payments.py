

class PaymentConector():

    def create_transaction(self,type: str, value: float, info: dict):
        '''
        Create an transaction to connect to third-party API payments
        '''

        if type == 'credit_card':
            return {
                "type": type,
                "status": "success"
            } 
        elif type == 'boleto':
            return {
                "type": type,
                "status": "success",
                "number": "213123019"
            }
        elif type == 'pix':
            return {
                "type": type,
                "status": "success",
                "code": "asiodsiajd"
            }
        

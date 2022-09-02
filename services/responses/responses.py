
class CustomResponse():

    def success_without_data(self):
        '''
        Return a success response without data
        '''
        return {
            'detail': {
                'status': 'ok',
                'status_code': 0,
            }
        }

    def success_with_data(self, data: any):
        '''
        Return a success response with data
        '''
        return {
            'detail': {
                'status': 'ok',
                'status_code': 0,
                
            },
            'data': data
        }

    # Data is still processing
    def still_processing(self,show_task_id: bool = False, task_id: str = None):
        '''
        Return that the data is still processing
        '''

        if show_task_id:
            return {
                'detail': {
                    'status': 'processing',
                    'status_code': 5,
                    'task_id': task_id
                }
            }

        else:
            return {
                'detail': {
                    'status': 'processing',
                    'status_code': 5,
                }
            }

    def success_with_pagination(self, data, current_page: int, total_pages: int):
        '''
        Return a success response with pagination
        '''
        return {
            'detail': {
                'status': 'ok',
                'status_code': 0,
                'current_page': current_page,
                'total_pages': total_pages
            },
            'data': data
        }
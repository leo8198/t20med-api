

from datetime import datetime
from database.basic import BasicCrud
from database.models.agenda import Agenda

class AgendaManager(BasicCrud):

    def __init__(self):
        super().__init__(Agenda)

    def get_agenda(self,doctor_id: int):
        '''
        Get the agenda of the doctors

        Only return available dates
        '''
        return self.db.query(
            self.model
        ).with_entities(
            self.model.id,
            self.model.date,
            self.model.time,
            self.model.doctor_id
        ).filter(
            self.model.doctor_id == doctor_id,
            self.model.date >= datetime.now().date(),
        ).order_by(self.model.date.desc()).all()

    def group_by_date(self,agenda_list: list):

        agenda_final = {}
        for a in agenda_list:

            if agenda_final.get(a['date']):
                agenda_final[a['date']].append(
                    {
                        'id': a['id'],
                        'time': a['time'].strftime('%H:%M'),
                        'doctor_id': a['doctor_id']
                    }
                )
            else:
                agenda_final[a['date']] = [
                    {
                        'id': a['id'],
                        'time': a['time'].strftime('%H:%M'),
                        'doctor_id': a['doctor_id']
                    }
                ]

        return agenda_final
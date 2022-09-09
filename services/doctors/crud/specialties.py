from database.basic import BasicCrud
from database.models.specialties import Specialty
from database.models.doctor_specialties import DoctorSpecialty

class SpecialtiesManager(BasicCrud):

    def __init__(self):
        super().__init__(Specialty)


class DoctorSpecialtiesManager(BasicCrud):
    
    def __init__(self):
        super().__init__(DoctorSpecialty)

    def get_by_specialty(self,specialty_id: int):
        return self.db.query(
            self.model
        ).filter(
            self.model.specialty_id == specialty_id
        ).all()
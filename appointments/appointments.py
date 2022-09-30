from apscheduler.schedulers.background import BackgroundScheduler
from appointments.consultation import ConsultationManager


def start():
    scheduler = BackgroundScheduler() 

    scheduler.add_job(
        func=ConsultationManager().schedule,
                trigger="interval",
                minutes=0.5,
                misfire_grace_time=2 * 60
    )
    
    scheduler.start()
    
    return
from database.connection import get_db
from database.models.patients import Patient
from config import settings
#from app.external.apis.my_email import EmailAPI
from datetime import timedelta
from services.authentication.crud.authentication import Authentication

# Initial setup of the database
def initial_setup():


    # Create the super admin
    create_super_admin()

    return None

# Create super admin credentials
def create_super_admin():
    '''
    Create the super admin credentials
    '''

    # Connect to the database
    db = get_db()

    # Check if the super admin is already created
    query = db.query(Patient).filter(Patient.email == settings.super_user_email).count()
    
    # If is empty
    if query == 0:

        print("\nCreating super admin credentials...")
        model = Patient()

        # Set the super admin credentials
        model.username = settings.super_user_username
        model.email = settings.super_user_email
        model.password = Authentication().get_password_hash("teste123")

        # Add to the database
        db.add(model)
        db.commit()
        db.refresh(model)

        db.close()

        print("Super admin created")
        return


    # If the admin has already been created
    else:
        print("\nSuper admin credentials already created")
    
    
    return None


initial_setup()
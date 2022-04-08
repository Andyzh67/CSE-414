from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    patient = Patient(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Create patient failed, Cannot save")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
        return
    print(" *** Account created successfully *** ")


def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
    return False



def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Create caregiver failed, Cannot save")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
        return
    print(" *** Account created successfully *** ")


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("Already logged-in!")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login caregiver failed")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when logging in. Please try again!")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Error occurred when logging in. Please try again!")
    else:
        print("Patient logged in as: " + username)
        current_patient = patient



def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("Already logged-in!")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login caregiver failed")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when logging in. Please try again!")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Error occurred when logging in. Please try again!")
    else:
        print("Caregiver logged in as: " + username)
        current_caregiver = caregiver




def search_caregiver_schedule(tokens):
    if len(tokens) != 2:
        print("Please try again!")
        return
    
    cm = ConnectionManager()
    conn = cm.create_connection()
    select_date = "SELECT Username AS 'Caregiver Username' FROM Availabilities WHERE Time = %s"
    
    date = tokens[1]
    date_tokens = date.split("-")
    
    if len(date_tokens) != 3:
        print("Please enter a valid date in the format mm-dd-yyyy")
        return
    
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    
    if len(date_tokens[0]) != 2 or len(date_tokens[1]) != 2 or len(date_tokens[2]) != 4:
        print("Please enter a valid date in the format mm-dd-yyyy")
        return
    
    d = datetime.datetime(year, month, day)
    
    row = None
    
    try:
        # Print all caregivers if available
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_date, d)
        row = cursor.fetchone()
        
        if row is None:
            print("None of the caregivers are available on the date entered")
            return
        
        print("Usernames of available caregivers:")
        while row is not None:
            print(row['Caregiver Username'])
            row = cursor.fetchone()
        print("")

        # Print all vaccines if available
        cursor.execute("SELECT V.name as 'Vaccine Name', V.doses AS 'Doses Left' FROM VACCINES AS V")
        row = cursor.fetchone()
        if row is None:
            print("No available vaccines doses left")
            return
        
        print("Available vaccine doses:")
        while row is not None:
            print(f"Vaccine name: {row['Vaccine Name']}, Number of doses left: {row['Doses Left']}")
            row = cursor.fetchone()
        
    except pymssql.Error as e:
        print("Error occurred when searching schedule or checking vaccine doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()





def reserve(tokens):
    # Check log in as patient
    global current_patient
    if current_patient is None:
        print("Log in as a patient to reserve an appointment")
        return
    
    # check valid input length
    if len(tokens) != 3:
        print("Please try again!")
        return
    
    
    # check valid date entered
    date = tokens[1]
    date_tokens = date.split("-")
    
    if len(date_tokens) != 3:
        print("Please enter a valid date in the format mm-dd-yyyy")
        return
    
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    
    if len(date_tokens[0]) != 2 or len(date_tokens[1]) != 2 or len(date_tokens[2]) != 4:
        print("Please enter a valid date in the format mm-dd-yyyy")
        return
    
    d = datetime.datetime(year, month, day)    
    check_reservation = "SELECT * FROM Appointments WHERE PatientName = %s AND Time = %s AND VaccineName = %s"
    find_available = "SELECT Username AS 'Caregiver Username' FROM Availabilities WHERE Time = %s ORDER BY Rand()"
    check_vaccine = "SELECT Doses FROM Vaccines WHERE Name = %s"
    
    vaccine_name = tokens[2]
    cm = ConnectionManager()
    conn = cm.create_connection()
    
    row = None
    caregiver = None
    vaccine = None
    
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(check_reservation, (current_patient.get_username(), d, vaccine_name))
        row = cursor.fetchone()
        
        # check if already reserved
        if row is not None:
            print("You already reserved an appointment on the date entered with your desired vaccine")
            return
        
        # check and find one available caregiver
        cursor.execute(find_available, d)
        caregiver = cursor.fetchone()
        if caregiver is None:
            print("No available caregiver on the date entered")
            return
        
        print("Your assigned caregiver is:")
        print(caregiver['Caregiver Username'])
        
        # check if vaccine is available
        cursor.execute(check_vaccine, vaccine_name)
        vaccine = cursor.fetchone()
        if vaccine is None:
            print("However, no vaccine of your desire is available")
            print("Reservation failed")
            return
                
        if vaccine['Doses'] == 0:
            print("However, no vaccine of your desire is available")
            print("Reservation failed")
            return            
                
        # make reservation and update database
        app_id = month * 100000 + day * 1000 + (year- 2000) * 10 + vaccine['Doses'] * 10000000 + len(vaccine_name)
        cursor.execute("INSERT INTO Appointments VALUES (%d,%s,%s,%s,%s)", (app_id, current_patient.get_username(), caregiver['Caregiver Username'], vaccine_name, d))
        cursor.execute("UPDATE Vaccines SET Doses = Doses - 1 WHERE Name = %s", vaccine_name)
        cursor.execute("DELETE FROM Availabilities WHERE Time = %s AND Username = %s", (d, caregiver['Caregiver Username']))
        conn.commit()
        print("Your appointment ID is", app_id)
        print("Successfully reserved an appointment")
        
    except pymssql.Error as e:
        print("Error occurred when searching schedule or checking vaccine doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
                       

        

        
        
        






def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra Credit
    """
    pass


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Failed to get Vaccine information")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to get Vaccine information")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Failed to add new Vaccine to database")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Failed to add new Vaccine to database")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Failed to increase available doses for Vaccine")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Failed to increase available doses for Vaccine")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("You need to log in first to see your appointments")
        return
    
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    row = None
    
    try:
        if current_patient is not None:
            cursor.execute("SELECT AppointmentID as AID, VaccineName as Vn, Time as T, CaregiverName as Cn FROM Appointments AS A WHERE A.PatientName = %s", 
                           current_patient.get_username())
            
            row = cursor.fetchone()
            if row is None:
                print("You did not reserve any appointment")
                return
            while row is not None:
                print(f"Appointment ID: {row['AID']}, Vaccine name: {row['Vn']}, Date: {row['T']}, Caregiver name: {row['Cn']}")
                row = cursor.fetchone()
        else:
            cursor.execute("SELECT AppointmentID as AID, VaccineName as Vn, Time as T, PatientName as Pn FROM Appointments AS A WHERE A.CaregiverName = %s", 
                           current_caregiver.get_username())
            
            row = cursor.fetchone()
            if row is None:
                print("You have no appointments")
                return
            while row is not None:
                print(f"Appointment ID: {row['AID']}, Vaccine name: {row['Vn']}, Date: {row['T']}, Patient name: {row['Pn']}")
                row = cursor.fetchone()
    except pymssql.Error as e:
        print("Error occurred when searching schedule or checking vaccine doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
                       
    
    


def logout(tokens):
    global current_patient
    global current_caregiver
    
    if current_caregiver is None and current_patient is None:
        print("Failed to logout because no user logged in")
        return
    else:
        current_caregiver = None
        current_patient = None
        print("Logged out successfully")


def start():
    stop = False
    while not stop:
        print()
        print(" *** Please enter one of the following commands *** ")
        print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
        print("> create_caregiver <username> <password>")
        print("> login_patient <username> <password>")  #// TODO: implement login_patient (Part 1)
        print("> login_caregiver <username> <password>")
        print("> search_caregiver_schedule <date>")  #// TODO: implement search_caregiver_schedule (Part 2)
        print("> reserve <date> <vaccine>") #// TODO: implement reserve (Part 2)
        print("> upload_availability <date>")
        print("> cancel <appointment_id>") #// TODO: implement cancel (extra credit)
        print("> add_doses <vaccine> <number>")
        print("> show_appointments")  #// TODO: implement show_appointments (Part 2)
        print("> logout") #// TODO: implement logout (Part 2)
        print("> Quit")
        print()
        response = ""
        print("> Enter: ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Type in a valid argument")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Try Again")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == cancel:
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Thank you for using the scheduler, Goodbye!")
            stop = True
        else:
            print("Invalid Argument")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()

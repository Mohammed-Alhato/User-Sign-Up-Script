import mysql.connector
import re

# ESTABLISHING A CONNECTION WITH MY DATABASE
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Passw0rd",
  database="mo_zone",
)

# INITIATING OUR CURSOR TO RUN OPERATIONS AND INTERACT WITH THE MYSQL SERVER
my_cursor = mydb.cursor()

# CREATING A NEW DATABASE
# my_cursor.execute("CREATE DATABASE mo_zone")


# CREATING TABLE FOR USERS IN OUR MO_ZONE DATABASE 
my_cursor.execute("CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255),username VARCHAR(255) PRIMARY KEY, password VARCHAR(255), email VARCHAR(255))")


# A FUNCTION TO GET USER INPUT FOR SIGNING UP 
def get_user_data():
  valid = False
  while not valid:
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    #CHECKING IF THE FIRST_NAME AND LAST_NAME IS VALID USING REGEX
    first_name_valid = re.match(r'^[a-zA-Z]', first_name)
    last_name_valid = re.match(r'^[a-zA-Z]', last_name)
    if first_name_valid and last_name_valid:
      print('Valid')
    else:
      print('Invalid')

    username = input("Enter a username you would like to have: ")

    password = input("Enter a password: ")
    #CHECKING IF THE PASSWORD IS VALID USING REGEX
    passwd_valid = re.match(r'^[a-zA-Z0-9!S%?@]{6,255}$', password)
    if passwd_valid:
      print("Vlaid")
    else:
      print("Invalid")
    # CHECKING IF THE EMAIL IS VALID USING REGEX
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    try:
      email = input("Enter your Email address: ")
      if (re.fullmatch(regex, email)): # PASSING THE REGEX AND THE STRING INTO THE FULLMATCH() METHOD TO VALIDATE THE EMAIL ADDRESS
        break
      else:
        print("invalid email address!")
    except:
      continue
    if first_name and last_name and username and password and email:
      valid = True
  return first_name, last_name, username, password, email



# A FUNCTION FOR INSERTING USER LOGIN INFORMATION INTO THE TABLE 'USERS' IN THE 'MO_ZONE' DATABASE
def add_to_db(first_name,last_name,username,password,email):
  try:
    my_cursor.execute("INSERT INTO `users` (`first_name`, `last_name`, `username`, `password`, `email`) VALUES (%s, %s,%s,%s,%s)", (first_name,last_name,username,password,email))
    mydb.commit()
  except:
    print("Not inserted!")
  else:
    print("Your data was added successfully!")



# A FUNCTION TO GET THE USER LOGIN INFORMATION INCLUDING USERNAME AND PASSWORD AND CHECKING THEIR VALIDITY 
def sign_in_info():
  valid = False
  while not valid:
    try:
      username = input("Enter your username: ")
      password = input("Enter your password: ")
    except:
      print('Nothing was entered!')
    if username and password:
      valid = True
  return username, password


# A FUNCTION TO CHECK IF THE DETAILS ENTERED BY THE USER MATCH THE USER'S ACCOUNT IN OUR DATABASE 
def check_credentials(username, password):
    my_cursor.execute("SELECT * FROM `users` WHERE `username`=%s AND `password`=%s LIMIT 1", (username, password))
    # print(my_cursor.fetchall())
    result = bool(my_cursor.fetchall())
    return result



# OUR MAIN FUNCTION WHERE WE CALL ALL OTHER FUNCTIONS TO GIVE USERS OPTIONS FROM REGISTERING NEW USERS TO LOGGIN IN CURRENT USERS AND CHECKING THEIR ACCOUNT INFORMATION
def main():
  y = None 
  while not y:
    try: 
      choice = int(input('Hello! Thank you for your interest in MoZone, We are happy to have you! Please Select Your Option: \n (1)Log in, (2)Sign up, (3)Exit: ')) 
    except:
      print("Your entry was invalid, please try again: ")
    else:
      if choice == 1: 
        username, password = sign_in_info()
        is_valid = check_credentials(username, password)
        print(is_valid)
        if is_valid:
          print("Your are logged in!")
        else:
          print("Sorry, I could not log you in!")

      elif choice == 2:
        first_name,last_name,username,password,email = get_user_data()
        add_to_db(first_name,last_name,username,password,email)
      elif choice == 3:
        print ("Be Back Soon!")
        y = True
      else:
        print("Your entry was invalid, please try again: ")
    break
main()
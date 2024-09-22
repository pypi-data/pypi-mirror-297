# Check if the user is exists, if user is found then check if the given password is correct?
# If user not found, password check skipped
# If the wrong password attempts are more than 3 then block the user. 
# Dataset

# Data Parsing/Traformation/Logic

def user(username, registration):
    # Check if the user found
    for user in registration:
        # print (registration[user][login_name])
        if username == registration[user]["login_name"]:
            print (f"User {username} is found")
            break
    else:
        print (f"User is not found")
        exit()




       

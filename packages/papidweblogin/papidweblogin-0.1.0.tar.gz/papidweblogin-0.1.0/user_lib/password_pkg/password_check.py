
def password(username, registration):
    #Check if the user exceeded more than 3 wrong passwords
    max_failed_attempts = 3
    failed_attempts = 0 #counter
    #Check if the user exceeded more than 3 wrong passwords
    while failed_attempts < max_failed_attempts:
        input_password = input("Enter the password for the user:")
        password_success = False
        # Check if the password is correct
        for user in registration:
            # print (registration[user][login_name])
            if username == registration[user]["login_name"]:
                if input_password == registration[user]["password"]:
                    print ("Password login is successful")
                    password_success = True
                    break
                else:
                 print ("Password is wrong")
        if password_success:
            break
        failed_attempts = failed_attempts + 1
        if failed_attempts < max_failed_attempts:
            continue
        else:
            print ("You have reached maximum attempts! Try later")
            break
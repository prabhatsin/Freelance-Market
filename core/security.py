# Password_Hashing

import bcrypt


def hash_password(password):
    password_bytes=password.encode()
    hashed=bcrypt.hashpw(password_bytes,bcrypt.gensalt())
    return  hashed
    # decode it before storing inside the database 


# pw='prabhat123'
# result=hash_password(pw)
# print(result)

# if bcrypt.checkpw(pw.encode(),result):
#     print("It matched")
# else:
#     print('Password did not match')

#! small mistake
'''
hashed is bytes, but your DB column will likely be String. Store it 
as hashed.decode('utf-8')

'''
def verify_password(password,hashed_password):
    # This is binary password
    # !hashed_password=hash_password(password) 
    encoded_hash=hash_password.encode()
    if bcrypt.checkpw(password.encode(),hashed_password):
        # print("It matched")
        return {"message":"Its matched"}
    else:
        return{"message":"Password did not match"}

pw='prabhat123'

print(verify_password(pw))

# This hashed passowrd in above function is directly c alled from the db\
# dont call the hashing function internally , 
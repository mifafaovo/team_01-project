from models import User
import config
import hashlib

if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def insert_new_user(name, email, password1, password2, type):
    """
    Inserts user into User table.

    Args:
        name: The name given to the user. A string with max 64 characters.
        email: The email give to the user. A string with max 64 characters.
        password1: The hashed first password give by the user. A string with
          max 64 characters.
        password2: The hashed second password give by the user. A string with
          max 64 characters.
        type: The account access type. One of the following integer values:
          -1 == customer account.
           1 == owner account.
           0 == employee general account.
           2 == employee admin account.

    Returns:
        A touple containing any error messages raised and the user ID of the
        newly created user.
    """
    errmsg = []

    user = User.query.filter(User.email == email).first()
    if user:
        errmsg.append("Email has already been used.")
    if password1 != password2:
        errmsg.append("Passwords do not match.")
    if email == "":
        errmsg.append("An email is required.")
    # if password1 == (hashlib.md5("".encode())).hexdigest():
    if password1 == "":
        errmsg.append("A password is required.")

    # Adds user to db if no resistration errors occured
    if not errmsg:
        user = User(name=name, email=email, password=password1, type = type)
        db.session.add(user)
        db.session.commit()
        return None, user.uid

    return errmsg, None


def get_user_login(email, password):
    """
    Fetches a row from the User table.

    Retrieves a row pertaining the given email and password from the User table
    in the database.

    Args:
        email: The email pertaining to a user. A string.
        password: The hashed password pertaining to a user. A string.

    Returns:
        A user with matching email's and password's as the ones provided,
        None otherwise.
    """
    user = User.query.filter(User.email == email, User.password == password).first()
    return user
  
def get_user_name_by_uid(uid):
    """
    Get the user's name by the given uid

    Args:
         uid: The unique ID of the user. An integer.

    Returns:
        (if found) the user's name
        (if not) 'Not Found'
    """
    u = User.query.filter(User.uid==uid).first()
    if u:
        return u.name
    return "Not Found"


def update_type(uid, type):
    """
    Updates a row in the User table
    Args:
        uid: A user ID that corresponds to a user in the User table. A integer.
        type: The account access type. One of the following integer values:
          -1 == customer account.
           1 == owner account.
           0 == employee general account.
           2 == employee admin account.
    """
    user = User.query.filter(User.uid == uid).first()
    if user != None:
        user.type = type
        db.session.commit()

def get_user(uid):
    """
    Get a dictionary contains uid, name and email by the given uid

    Args:
        uid: The unique ID of the user. An integer.

    Returns:
        (if found) a dictionary including the user's name, email and uid
        (if not) None
    """
    user = User.query.filter(User.uid == uid).first()
    if user:
        dict = {
            "uid": uid,
            "name": user.name,
            "email": user.email
        }
        return dict
    return None

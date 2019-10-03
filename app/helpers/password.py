from bcrypt import hashpw, checkpw, gensalt


def encrypt_password(password):
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


def check_password(sent, expected):
    return checkpw(sent.encode('utf-8'), expected.encode('utf-8'))

import os


def get_extension(file):
    name, extension = os.path.splitext(file.name)
    return extension


def get_email_name(email):
    name = email.split("@")[0]
    return name

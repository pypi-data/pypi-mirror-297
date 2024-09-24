import random as random_libs
import secrets
import string as string_libs


def number(length):
    """
    Generate random numbers.
    :param length:
    :return:
    """
    characters = string_libs.digits
    random_string = ''.join(random_libs.choice(characters) for i in range(length))
    return random_string


def string(length):
    """
    Generate random string
    :param length:
    :return:
    """
    characters = string_libs.ascii_letters
    random_string = ''.join(random_libs.choice(characters) for i in range(length))
    return random_string


def unique_string(length):
    """
    Generate a random string of unique characters
    :param length:
    :return:
    """
    characters = string_libs.ascii_letters + string_libs.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

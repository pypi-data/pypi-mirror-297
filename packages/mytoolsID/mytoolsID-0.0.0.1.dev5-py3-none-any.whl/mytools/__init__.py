from .button import Button
from .chatbot import Api, ImageGen
from .database import LocalDataBase, MongoDataBase
from .encrypt import BinaryEncryptor, CryptoEncryptor
from .getuser import Extract
from .logger import LoggerHandler
from .misc import Handler
from .trans import Translate

__version__ = "0.0.0.1.dev5"

mytoolsID = """
  __  ____   _______ ___   ___  _    ___ ___ ___      __   ____      ____  _  _  ___  ___  ___  ___  ___ ___ _  _____ _  _ 
 |  \/  \ \ / /_   _/ _ \ / _ \| |  / __|_ _|   \    / /  / /\ \    / __ \| \| |/ _ \| _ \/ __|/ _ \|   \_ _| |/ /_ _| \| |
 | |\/| |\ V /  | || (_) | (_) | |__\__ \| || |) |  < <  / /  > >  / / _` | .` | (_) |   /\__ \ (_) | |) | || ' < | || .` |
 |_|  |_| |_|   |_| \___/ \___/|____|___/___|___/    \_\/_/  /_/   \ \__,_|_|\_|\___/|_|_\|___/\___/|___/___|_|\_\___|_|\_|
 """

print(f"\033[1;37;41m{mytoolsID}\033[0m")

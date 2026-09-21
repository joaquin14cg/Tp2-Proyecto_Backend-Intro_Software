import os
from dotenv import load_dotenv

load_dotenv

MIN_ID = 1


PATRON_EMAIL = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PATRON_NOMBRE = r'^[A-Za-zÀ-ÿ\s]+$'

CAMPOS_SOCIO = ('nombre', 'email')
ERROR_CODE_SOCIO_NOT_FOUND = 'socio.not.found'
ERROR_CODE_SOCIO_EXISTS = 'socio.already.exists'
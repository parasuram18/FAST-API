from dotenv import load_dotenv
import os
load_dotenv()


DATABASE_URL = os.getenv('POSTGRES_URL')

SECRET_KEY = os.getenv('SECRET_KEY')

JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

JWT_EXPIRE_TIME = int(os.getenv('JWT_EXPIRE_TIME'))
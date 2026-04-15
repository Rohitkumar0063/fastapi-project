from passlib.context import CryptContext
context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def hashing_password(passowrd:str):
  context.hash(passowrd)

def verify(plainpassword,hashpassowrd):
  context.verify(plainpassword,hashpassowrd)
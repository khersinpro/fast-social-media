from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)  

    # Association with the Role model
    role_name = Column(String, ForeignKey('role.name'), nullable=False, default="ROLE_USER")
    role = relationship("Role", backref="users")

    def verify_password(self, plain_password: str) -> bool:
        """
            Verify the password of the user

            Args:
                plain_password (str): The password to verify
            
            Returns:
                bool: True if the password is correct, False otherwise
        """
        return pwd_context.verify(plain_password, self.password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
            Get the password hash

            Args:
                password (str): The password to hash

            Returns:
                str: The hashed password
        """
        return pwd_context.hash(password)
    
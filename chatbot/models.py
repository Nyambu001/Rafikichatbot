from mongoengine import Document, StringField, EmailField, DateTimeField, ReferenceField
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)  # Hashed password is stored here
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    def set_password(self, password):
        """Hashes the password before saving."""
        self.password = generate_password_hash(password)  # Hashing is done but stored in 'password'

    def check_password(self, password):
        """Verifies if the given password matches the stored hash."""
        return check_password_hash(self.password, password)  # Checking against the hashed password

    def __str__(self):
        return f"User(username={self.username}, email={self.email})"


class ChatRecord(Document):
    user = ReferenceField(User, required=True)  # Use User directly
    user_message = StringField(required=True)  # User's message
    bot_response = StringField(required=True)  # Bot's response
    timestamp = DateTimeField(default=datetime.datetime.utcnow)  # Time of the message

    def __str__(self):
        return f"User: {self.user.username}, Message: {self.user_message}, Response: {self.bot_response}"

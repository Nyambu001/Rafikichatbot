
from mongoengine import Document, StringField, EmailField, DateTimeField, ReferenceField
import datetime


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True)
    password_hash = StringField(required=True)  
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return f"User(username={self.username}, email={self.email})"


class ChatRecord(Document):
    user = ReferenceField('User', required=True)  # Link to the User model
    user_message = StringField(required=True)  # User's message
    bot_response = StringField(required=True)  # Bot's response
    timestamp = DateTimeField(default=datetime.datetime.utcnow)  # Time of the message

    def __str__(self):
        return f"User: {self.user.username}, Message: {self.user_message}, Response: {self.bot_response}"
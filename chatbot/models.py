from datetime import datetime
from mongoengine import Document, StringField, EmailField, DateTimeField, ReferenceField
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import ListField, DictField
from mongoengine.queryset.visitor import Q


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(unique= False, required=False, null=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return f"User(username={self.username}, email={self.email})"


class ChatRecord(Document):
    user = ReferenceField('User', required=True)
    conversation = ListField(DictField())
    timestamp = DateTimeField(default=datetime.utcnow)

    def add_message(self, user_message, bot_response):
        self.conversation.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.utcnow()
        })
        self.conversation.append({
            'role': 'assistant',
            'content': bot_response,
            'timestamp': datetime.utcnow()
        })
        self.save()

    @classmethod
    def start_new_conversation(cls, user):
        new_conversation = cls(user=user, conversation=[], timestamp=datetime.utcnow())
        new_conversation.save()
        return new_conversation

    @classmethod
    def get_conversations(cls, user):
        """Fetches all conversations for a user."""
        return cls.objects(user=user).order_by('-timestamp')

    @classmethod
    def get_conversation_by_id(cls, chat_id):
        return cls.objects(id=chat_id).first()

    def __str__(self):
        if self.conversation:
            last_message = self.conversation[-1]
            role = last_message.get('role', 'unknown')
            content = last_message.get('content', 'No content')
            return f"User: {self.user.username}, Last {role}: {content}"
        return f"User: {self.user.username}, No conversation history"





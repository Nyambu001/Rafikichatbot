from django.urls import path
from .views import chatbot_view,index, chat_history, save_chat_record

urlpatterns = [
    path('chatbot/', chatbot_view, name='chatbot'),
    path('save_history/',save_chat_record, name='save_record'),
    path("", index, name='index'),
    path('chat-history/', chat_history, name='chat-history'),
]

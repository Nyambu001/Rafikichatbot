from django.urls import path
from .views import chatbot_view,index, chat_history, save_chat_record , login , register, csrf_token, create_chat_session

urlpatterns = [
    path('chatbot/', chatbot_view, name='chatbot'),
    path('save_history/',save_chat_record, name='save_record'),
    path("", index, name='index'),
    path('chat_history/', chat_history, name='chat_history'),
    path('get_csrf_token/', csrf_token, name='get_csrf_token'),
    path('signup/', register, name='register'),
    path('login/', login, name='login'),
    path('create_chat_session/', create_chat_session, name='create_chat_session'),

]

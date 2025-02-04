from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import logging
from datetime import datetime, timedelta
from chatbot.models import ChatRecord, User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from django.shortcuts import render
from django.conf import settings


# Set up logging
logger = logging.getLogger('chatbot')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('chatbot.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def index(request):
    return render(request, os.path.join(settings.REACT_APP_DIR, "index.html"))


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user already exists
        if User.objects(username=username).first():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # Create a new user
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        user.save()

        return JsonResponse({'message': 'User registered successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects(username=username).first()
        if user and check_password_hash(user.password, password):
            # Generate JWT token
            payload = {
                'user_id': str(user.id),
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({'message': 'Login successful', 'token': token}, status=200)
        return JsonResponse({'error': 'Invalid username or password'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def save_chat_record(user, user_message, bot_response):
    logger.info("Saving chat record")
    chat_record = ChatRecord(
        user=user,
        user_message=user_message,
        bot_response=bot_response,
        timestamp=datetime.utcnow()
    )
    chat_record.save()
    logger.info("Chat record saved successfully!")


@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            token = data.get('token')

            if not isinstance(user_message, str) or not user_message.strip():
                logger.warning('Invalid message received: %s', data)
                return JsonResponse({'error': 'Invalid or empty message provided'}, status=400)

            # Verify the JWT token
            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token['user_id']
                user = User.objects(id=user_id).first()
                if not user:
                    return JsonResponse({'error': 'Invalid token or user not found'}, status=400)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)

            logger.info('User message: %s', user_message)

        except json.JSONDecodeError:
            logger.error('Invalid JSON format: %s', request.body)
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        rasa_url = "http://localhost:5005/webhooks/rest/webhook"
        payload = {"sender": str(user.id), "message": user_message}

        try:
            rasa_response = requests.post(rasa_url, json=payload, timeout=5)
            if rasa_response.status_code == 200:
                bot_responses = rasa_response.json()
                bot_messages = []

                for resp in bot_responses:
                    if 'text' in resp:
                        bot_messages.append({'type': 'text', 'content': resp['text']})
                    if 'image' in resp:
                        bot_messages.append({'type': 'image', 'content': resp['image']})

                if not bot_messages:
                    logger.info("No bot responses received.")
                    return JsonResponse({'responses': ["I'm sorry, I didn't understand that."]})

                # Save conversation history
                for bot_message in bot_messages:
                    if bot_message['type'] == 'text':
                        save_chat_record(user, user_message, bot_message['content'])

                logger.info('Rasa response: %s', bot_responses)
                return JsonResponse({'responses': bot_messages})
            else:
                logger.error('Rasa server error: %s', rasa_response.status_code)
                return JsonResponse({'error': f'Rasa server returned status {rasa_response.status_code}'}, status=500)
        except requests.exceptions.Timeout:
            logger.error('Rasa server timed out')
            return JsonResponse({'error': 'Rasa server timed out'}, status=504)
        except requests.exceptions.RequestException as e:
            logger.error('Connection error: %s', str(e))
            return JsonResponse({'error': f'Failed to connect to Rasa server: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def chat_history(request):
    if request.method == 'GET':
        try:
            # Retrieve all chat records.
            chats = ChatRecord.objects.all().order_by('-timestamp')
            chat_data = [
                {
                    "user_message": chat.user_message,
                    "bot_response": chat.bot_response,
                    "timestamp": chat.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
                for chat in chats
            ]
            return JsonResponse({"chats": chat_data}, safe=False)
        except Exception as e:
            # Log error in case of failure
            logger.error("Error fetching chat history: %s", str(e))
            return JsonResponse({"error": "Failed to fetch chat history"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

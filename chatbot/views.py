from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from datetime import datetime, timedelta
from chatbot.models import ChatRecord, User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from django.shortcuts import render
from django.conf import settings
from django.middleware.csrf import get_token
from bson import ObjectId

@csrf_exempt
def create_chat_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            chat_type = data.get("type")  
            token = request.headers.get("Authorization", "").split("Bearer ")[-1]

            if not token:
                return JsonResponse({"error": "No token provided"}, status=401)

            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = decoded_token.get("user_id")

                if not user_id:
                    return JsonResponse({"error": "User ID not found in token"}, status=401)

                user = User.objects(id=user_id).first()
                if not user:
                    return JsonResponse({"error": "Invalid token or user not found"}, status=401)

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)

            if chat_type not in ["PHQ-9", "GAD-7","both", "skip"]:
                return JsonResponse({"error": "Invalid selection"}, status=400)

            # Create a new chat session
            new_chat = ChatRecord(
                user=user,
                conversation=[],
                timestamp=datetime.utcnow(),

            )
            new_chat.save()

            return JsonResponse(
                {
                    "chat_id": str(new_chat.id),

                },
                status=201,
            )

        except Exception as e:
            logger.error(f"Error creating chat session: {str(e)}")  # Log the error
            return JsonResponse({"error": "An error occurred while creating the chat session."}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

def index(request):
    return render(request, os.path.join(settings.REACT_APP_DIR, "index.html"))

def register(request):
    if request.method == 'GET':
        return JsonResponse({"message": "invalid request"})
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password:
            return JsonResponse({"error": "Username and password are required."}, status=400)
        email = email if email else None

        hashed_password = generate_password_hash(password)

        user = User(username=username, password=hashed_password, email=email)
        try:
            user.save()
            return JsonResponse({"message": "User registered successfully."}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return JsonResponse({"message": 'invalid request'})
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects(username=username).first()
        if user and check_password_hash(user.password, password):
            payload = {
                "user_id": str(user.id),
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({'message': 'Login successful', 'token': token, 'user_id': str(user.id)}, status=200)
        return JsonResponse({'error': 'Invalid username or password'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def save_chat_record(user, user_message, bot_messages, conversation):
    chat_record = ChatRecord(
        user=user,
        conversation=conversation,
        timestamp=datetime.utcnow()
    )
    chat_record.save()


@csrf_exempt
def chatbot_view(request):
    existing_chat = None
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            chat_id = data.get('conversation_id')
            token = data.get('token')

            # Validate message
            if not isinstance(user_message, str) or not user_message.strip():
                return JsonResponse({'error': 'Invalid or empty message provided'}, status=400)

            # Validate token
            if not token:
                token = request.headers.get('Authorization')
                if token:
                    token = token.split("Bearer ")[-1]
                else:
                    return JsonResponse({'error': 'No token provided'}, status=401)

            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get('user_id')

                if not user_id:
                    return JsonResponse({'error': 'User ID not found in token'}, status=401)

                user = User.objects(id=user_id).first()
                if not user:
                    return JsonResponse({'error': 'Invalid token or user not found'}, status=401)

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)

            # Start or retrieve existing conversation
            conversation = []

            if chat_id:
                existing_chat = ChatRecord.objects(id=chat_id, user=user).first()

                if existing_chat:
                    conversation = existing_chat.conversation
                else:
                    return JsonResponse({'error': 'Chat ID not found'}, status=404)
            else:
                # Start new conversation if no chat_id is provided
                existing_chat = ChatRecord.start_new_conversation(user)
                conversation = existing_chat.conversation


            rasa_url = "http://localhost:5005/webhooks/rest/webhook"
            payload = {
               "sender": str(user.id),
                "message": user_message
            }

            try:
                rasa_response = requests.post(rasa_url, json=payload, timeout=10)
                if rasa_response.status_code == 200:
                    bot_responses = rasa_response.json()
                    bot_messages = []

                    for resp in bot_responses:
                        if 'text' in resp:
                            bot_messages.append({'type': 'text', 'content': resp['text']})
                        if 'image' in resp:
                            bot_messages.append({'type': 'image', 'content': resp['image']})

                    if not bot_messages:
                        return JsonResponse({'responses': ["pole lakini sijakuelewa."]})

                    # Add user and bot messages to the conversation
                    conversation.append({
                        "role": "user",
                        "message": user_message,
                        "timestamp": datetime.utcnow()
                    })

                    for bot_message in bot_messages:
                        conversation.append({
                            "role": "assistant",
                            "message": bot_message['content'],
                            "timestamp": datetime.utcnow()
                        })

                    # Save the conversation record
                    existing_chat.conversation = conversation
                    existing_chat.timestamp = datetime.utcnow()
                    existing_chat.save()

                    return JsonResponse({'responses': bot_messages, 'updated_conversation': conversation})

                else:
                    return JsonResponse({'error': f'Rasa server returned status {rasa_response.status_code}'}, status=500)

            except requests.exceptions.Timeout:
                return JsonResponse({'error': 'Rasa server timed out'}, status=504)

            except requests.exceptions.RequestException as e:
                return JsonResponse({'error': f'Failed to connect to Rasa server: {str(e)}'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def chat_history(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')

        if not user_id:
            return JsonResponse({"error": "User ID is required"}, status=400)

        try:
            user_obj = User.objects.get(id=ObjectId(user_id))
            chats = ChatRecord.objects.filter(user=user_obj).order_by('-timestamp')

            if not chats:
                return JsonResponse({"chats": []})

            chat_data = []

            for chat in chats:
                chat_entry = {
                    "conversation_id": str(chat.id),
                    "timestamp": chat.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "messages": []
                }

                for entry in chat.conversation:
                    chat_entry["messages"].append({
                        "role": entry.get("role"),
                        "message": entry.get("message"),
                        "timestamp": entry.get("timestamp").strftime("%Y-%m-%d %H:%M:%S")
                    })

                chat_data.append(chat_entry)

            return JsonResponse({"chats": chat_data})

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

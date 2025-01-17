from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import logging
from datetime import datetime
from chatbot.models import User, ChatRecord  # Import MongoDB models
from mongoengine import DoesNotExist

# Set up logging
logger = logging.getLogger('chatbot')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('chatbot.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def save_chat_record(user, user_message, bot_response):
    logger.info("Saving chat record for user: %s", user)
    chat_record = ChatRecord(
        user=user,
        user_message=user_message,
        bot_response=bot_response,
        timestamp=datetime.utcnow()
    )
    chat_record.save()
    logger.info("Chat record saved successfully!")


from chatbot.models import User, ChatRecord
from mongoengine import DoesNotExist

def save_chat_record(user, user_message, bot_response):
    logger.info("Saving chat record for user: %s", user)
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
            user_id = data.get('user_id', None)  # Default to None if no user_id is provided

            if not isinstance(user_message, str) or not user_message.strip():
                logger.warning('Invalid message received: %s', data)
                return JsonResponse({'error': 'Invalid or empty message provided'}, status=400)

            logger.info('User message: %s', user_message)

        except json.JSONDecodeError:
            logger.error('Invalid JSON format: %s', request.body)
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        rasa_url = "http://localhost:5005/webhooks/rest/webhook"
        payload = {"sender": user_id if user_id else 'anonymous', "message": user_message}

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

                # If user is authenticated (logged in), save the chat record
                if user_id:
                    try:
                        # Try to get the user, if not exist create a new one
                        user = User.objects(username=user_id).first()

                        if not user:
                            # Create the user if it doesn't exist
                            user = User(username=user_id, email=f"{user_id}@example.com", password_hash="default")
                            user.save()

                        for bot_message in bot_messages:
                            if bot_message['type'] == 'text':  # Only save text responses
                                save_chat_record(user, user_message, bot_message['content'])

                    except DoesNotExist:
                        logger.error("User does not exist and failed to create")
                    except Exception as e:
                        logger.error("Failed to save chat record: %s", str(e))

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


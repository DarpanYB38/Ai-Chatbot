from django.shortcuts import render
from django.http import JsonResponse
from chatbot.models import *
from chatbot.utils import *
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
import json
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
import openai
import re

# Create your views here.
genai.configure(api_key = "AIzaSyCMHMKrIPfoItVJROcRbjiyhBAMQam-e5Q")
model = genai.GenerativeModel(
                "gemini-2.0-flash",
            )

@login_required
def chatbot_view(request):
    return render(request, 'base.html')

# Store chat history in a dictionary (Session-based approach)
chat_sessions = {}

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            user_input = data.get("message", "")

            if not user_input:
                return JsonResponse({"error": "Empty message"}, status=400)

            # ✅ Retrieve conversation history (last 5 messages)
            history = request.session.get("chat_history", [])
            history.append(f"User: {user_input}")  

            # ✅ Keep only last 5 messages
            if len(history) > 5:
                history = history[-5:]

            # ✅ Generate response with history
            prompt = "\n".join(history)  # Combine messages into a single conversation
            response = model.generate_content(prompt, generation_config={"max_output_tokens": 100})

            # ✅ Clean response (remove * and _)
            bot_reply = re.sub(r"[*_]", "", response.text)  
            history.append(f"Bot: {bot_reply}")  

            # ✅ Save updated history in session
            request.session["chat_history"] = history  

            return JsonResponse({"message": bot_reply})

        except Exception as e:
            print("Error in chatbot_api:", str(e))
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

         # Simple AI response (Replace this with actual chatbot logic)
        bot_reply = f"Hello! You said: {user_message}"

        return JsonResponse({"reply": bot_reply})
    


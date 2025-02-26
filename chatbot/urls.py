from django.urls import path
from chatbot.views import *

urlpatterns = [
    path("",chatbot_view, name='chatbot_view'),
    path('api/chat/',chatbot_api, name='chatbot_api'),
]
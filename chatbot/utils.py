import nltk
import random
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

responses = {
    "hello": "Hello, how can I help you?",
    "how are you": "I'm good, thank you. How can I help you?",
    "bye": "Goodbye! Have a nice day!",
    "default": "I am not sure i understand. can you please rephrase it?",
}

def get_response(user_input, chat_history):
    user_input = user_input.lower()
    conversation = [msg.message for msg in chat_history] + list(responses.keys())

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(conversation + [user_input])

    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    best_match_idx = similarity.argmax()

    response = responses.get(conversation[best_match_idx], responses["default"])
    return response
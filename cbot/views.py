from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.http import JsonResponse
from fuzzywuzzy import fuzz
import requests
import re
# Create your views here.

class testview(generics.GenericAPIView):

    def get(self,request):
        return
    
    def post(self,request):
        print(request.data['prompt'])
        best_response = resgen(request.data['prompt'].lower(), response_dict)
        response = JsonResponse(
            {'response': best_response},status=200)
        return response

def resgen(input_text, response_dict):
    best_match = None
    best_score = -1
    search_youtube_videos('stayin alive')
    for key, response in response_dict.items():
        similarity_score = fuzz.ratio(input_text, key)
        if similarity_score > best_score:
            best_score = similarity_score
            best_match = response if isinstance(response, str) else response(input_text)

    return best_match

def search_youtube_videos(query):
    endpoint = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'key': 'AIzaSyDE5PL1IZR5Ndcm2vir0IhTZ-i-hQJC8jk',
    }
    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        video_info = []
        if 'items' in data:
            videos = [item for item in data['items'] if 'id' in item and item['id'] and 'videoId' in item['id']]
            for video in videos:
                video_id = video['id']['videoId']
                video_title = video['snippet']['title']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                video_info.append({'title': video_title, 'url': video_url})

        return video_info
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def perform_operation(input_string):
    words = input_string.split()
    num1 = None
    num2 = None
    operation = None
    for word in words:
        if re.match(r'^[0-9]*\.?[0-9]+$', word):
            if num1 is None:
                num1 = float(word)
            else:
                num2 = float(word)
        elif word in ["sum","+", "add","addition","plus","aggregate","summation","increment"]:
            operation = "sum"
        elif word in ["subtract","-","subtraction","decrement","difference", "minus"]:
            operation = "subtract"
        elif word in ["division","/","divide","parts"]:
            operation = "divide"
    if num1 is None or num2 is None or operation is None:
        return "Invalid input format. Please provide two numbers and specify the operation."
    if operation == 'sum':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'divide':
        result = num1 / num2 if num2 != 0 else 'Not Defined'
    return result

response_dict = {
    "hello": "Hello, how can I assist you?",
    "help": "Sure, I can help. What do you need?",
    "goodbye": "Goodbye! Have a great day.",
    "information": "What kind of information are you looking for?",
    "how are you": "Hey sirrrr",
    "play": search_youtube_videos,
    "give me sum": perform_operation,
    "subtraction of": perform_operation,
    "parts of": perform_operation,
    "divide": perform_operation,
}
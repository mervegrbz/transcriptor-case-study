import requests
from dotenv import load_dotenv
import os
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/google-bert/bert-base-uncased"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

def query(payload):
	_response = requests.post(API_URL, headers=headers, json=payload)
	response = _response.json()
	return [i['token_str'] for i in response ]
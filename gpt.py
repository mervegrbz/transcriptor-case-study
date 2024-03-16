

from openai import OpenAI
from dotenv import load_dotenv
import os
from werkzeug.exceptions import HTTPException
load_dotenv()

client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))

def send_to_chat(content):
  try: 
    messages = [
      { 
        'role': 'system', 
        'content': '''Find if there is a homonymic word in sentence, if it is not suitable for the sentence, return meaningful homonymic word, return type is JSON,
          example: { "word": "high", "possible_word": "hi", "index": 0 },
          there can be no error in sentence, in that case return index -1'''
      },
      {
        'role': 'user',
        'content': content
      }]
    
    stream = client.chat.completions.create(
      model="gpt-4",
      messages=messages,
      max_tokens=150,
      stream=False)
    return stream.choices[0].message.content
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
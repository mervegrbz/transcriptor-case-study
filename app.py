from apiflask import Schema, fields, APIFlask, validators
import gpt 
import bert
from similars import homophones_ipa
from werkzeug.exceptions import HTTPException
from waitress import serve

app = APIFlask(__name__)
similar = {i:[] for i in homophones_ipa}
# store homophones in a key value pair
def match_homophones():
    global similar
    for i in homophones_ipa:
        for j in homophones_ipa:
            if i != j and homophones_ipa[i] == homophones_ipa[j]:
                similar[i].append(j)
    
match_homophones()

class Body(Schema):
    text   = fields.String(required=True)
    choice = fields.String(required=True, validate=validators.OneOf(['bert', 'openai']))

@app.post("/")
@app.input(Body, arg_name='body')
def correction(body):
    try:
        global similar
        original = body['text']
        tokens = original.split()
        if body['choice'] == 'bert': 
            for  index, token in enumerate(tokens):
                if token in similar:
                    tokens[index] = '[MASK]'
                    text = ' '.join(tokens)
                    probabilities = bert.query({"inputs": text})
                    for prob_word in probabilities:
                        if prob_word in similar[token]:         
                            tokens[index] = prob_word
                            text = ' '.join(tokens)
                            return {'text': text, 'modified': 'true'}
                    return {'text': original, 'modified': 'false'}
        if body['choice'] == 'openai':
            _result = gpt.send_to_chat(body['text'])
            # gpt 4 returns a string, we need to convert it to a dictionary
            result = eval(_result)
            if (result['index'] == -1 ) : return {'text': original, 'modified': 'false' }
            tokens[result['index']] = result['possible_word']
            return {'text': ' '.join(tokens), 'modified': 'true' }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


serve(app, host="0.0.0.0", port=8080)
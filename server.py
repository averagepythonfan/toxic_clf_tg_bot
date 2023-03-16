import uvicorn
import os
from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pydantic import BaseModel


class Message(BaseModel):
    input: str


path = f'{os.getcwd()}/rubertconv_toxic_clf'
tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModelForSequenceClassification.from_pretrained(path)

api = FastAPI()

@api.get('/ready')
def get_ready():
    return {'response': 200}

@api.post('/toxicity')
def toxicity(text: Message):
    test_input = tokenizer(text=text.input, return_tensors='pt')
    test_output = model(**test_input)
    res = test_output[0][0]
    result = res.tolist()
    return { "response" : { "neutral" : result[0], "toxicity": result[1]} }

if __name__ == "__main__":
    uvicorn.run('server:api', host='0.0.0.0', port=8888, log_level='info')
import openai
import threading
import time
import requests
from queue import Queue

CHATGPT_KEY = 'sk---'       # input your keys here
GPT4_KEY = 'sk---'

openai.api_key = 'sk---'
openai.api_base = '--'

USING_OPENAI_API = True


def prompt_format(prompt_template, prompt_content):
    return prompt_template.format(**prompt_content)


def get_response(message, model, max_tokens, temperature, candidate_n):
    if USING_OPENAI_API:
        response = openai.ChatCompletion.create(
                model=model,
                messages=message,
                max_tokens=max_tokens,
                temperature=temperature,
                n=candidate_n)
        if candidate_n == 1:
            return_response = response.choices[0].message.content
        else:
            return_response = [response.choices[i].message.content for i in range(candidate_n)]
        return return_response
    else:
        headers = {'Content-Type': 'application/json'}
        if 'gpt-4' in model:
            url = 'http://----'
        else:
            url = 'http://----'
        history = [message[0]['content'], 'OK, I got it! I will finish the task following the above instructions.']
        for m in message[1:-1]:
            history.append(m['content'])
        prompt = message[-1]['content']
        data = {'prompt': prompt, 'history': history, 'model': model, 'uid': 'xx5ty',
                'max_tokens': max_tokens, 'temperature': temperature, 'n': candidate_n}
        if 'text-davinci' in model:
            data['type'] = 'completion'
        response = requests.post(url, json=data, headers=headers).json()
        print(response['response'])
        return response['response']


def api_single_request(message, model="gpt-3.5-turbo-1106", max_tokens=128, temperature=0.7, candidate_n=1,
                       rank=-1, result_queue=None):
    request_cnt = 0
    if candidate_n == 1:
        temperature = 0
    while True:
        request_cnt += 1
        if request_cnt > 20:
            exit(0)
        try:
            return_response = get_response(message, model, max_tokens, temperature, candidate_n)
            # single thread request
            if rank == -1:
                return return_response
            # multi thread request
            else:
                result_queue.put({
                    'rank': rank,
                    'response': return_response
                })
                return
        except Exception as e:
            # raise e
            # print(e)
            print("API ERROR!")
            time.sleep(1)
            continue


def api_multi_request(messages, model="gpt-3.5-turbo-1106", max_tokens=128, temperature=0.7, candidate_n=1):
    threads = []
    result_queue = Queue()
    gathered_response = []
    for i in range(len(messages)):
        t = threading.Thread(target=api_single_request,
                             args=(messages[i], model, max_tokens, temperature, candidate_n, i, result_queue))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    while not result_queue.empty():
        gathered_response.append(result_queue.get())
    assert len(gathered_response) == len(messages)
    gathered_response.sort(key=lambda x: x['rank'])
    gathered_response = [x['response'] for x in gathered_response]
    return gathered_response


def chatgpt(prompt, model="gpt-3.5-turbo-1106", max_tokens=1000, temperature=0.7, candidate_n=1):
    messages = [{'role': 'user', 'content': prompt}]
    if 'gpt-4' in model:
        openai.api_key = GPT4_KEY
    else:
        openai.api_key = CHATGPT_KEY
    if len(messages) == 1:
        return [api_single_request(messages[0], model, max_tokens, temperature, candidate_n)]
    else:
        return api_multi_request(messages, model, max_tokens, temperature, candidate_n)


def embedding_single_request(text, rank=-1, result_queue=None):
    request_cnt = 0
    while True:
        request_cnt += 1
        if request_cnt > 20:
            exit(0)
        try:
            response = openai.Embedding.create(
                model='text-embedding-ada-002',
                input=text
            )
            embedding = response['data'][0]['embedding']
            if rank == -1:
                return embedding
            else:
                result_queue.put({
                    'rank': rank,
                    'response': embedding
                })
                return
        except Exception as e:
            print('API Error')
            time.sleep(1)
            continue


def embedding_multi_request(texts):
    threads = []
    result_queue = Queue()
    gathered_response = []
    for i in range(len(texts)):
        t = threading.Thread(target=embedding_single_request, args=(texts[i], i, result_queue))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    while not result_queue.empty():
        gathered_response.append(result_queue.get())
    assert len(gathered_response) == len(texts)
    gathered_response.sort(key=lambda x: x['rank'])
    gathered_response = [x['response'] for x in gathered_response]
    return gathered_response

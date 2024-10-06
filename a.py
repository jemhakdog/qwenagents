from requests import Session

requests = Session()

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': '__stripe_mid=80ef9640-77a6-42e0-91c5-a22ed36a74dd3f9c4d; __stripe_sid=54bf499e-45e8-41c7-a7cc-6eb2db0c2697cef0ca; hf-chat=e54eba57-15ff-4ec5-a277-e58eeec185d8; aws-waf-token=cc9341a4-d386-48eb-af36-261b7c761bc4:AAoAYepDFkkoAAAA:uL1NKwt3aywHI4YwKX1AD9x5TTBWi9eL1pCYaA12hMO3YKEFzewq73Klcfz5ANCbvgbzKMWh1OO55sOE0okvIUyezP8Mb3J0q6CZ2Y0YDXpSeELINp9z/+uJR08OSBtZGEDL0VJIeIfOMINtMduq7MuVwVGnqblM8gwR0i7ZXRzjFrnN91LrKf9rE57KMosYk5hAowgRBtfasA7V2Gqij3Fbad82jal1Th5RB3xSlofoOWAXiXPLdsgxMwKWgcvDrqMENV8=',
    'origin': 'https://huggingface.co',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://huggingface.co/chat/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

json_data = {
    'model': 'meta-llama/Llama-3.2-11B-Vision-Instruct',
}

conversationId = requests.post('https://huggingface.co/chat/conversation',  headers=headers, json=json_data).json()['conversationId']
print(conversationId)
id = requests.cookies.get_dict()['hf-chat'] 
print(id)
files = {
    'data': (None, '{"inputs":"hi","id":"'+str(id)+'","is_retry":false,"is_continue":false,"web_search":false,"tools":[]}'),

}
print(files)
response = requests.post(
    'https://huggingface.co/chat/conversation/{conversationId}'.format(conversationId=conversationId),
    headers=headers,
    files=files,
    stream=True
)
for res_chunck in response.iter_content():
    print(res_chunck.decode("utf-8"),end='',flush=True)


# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"model":"meta-llama/Llama-3.2-11B-Vision-Instruct"}'
#response = requests.post('https://huggingface.co/chat/conversation', cookies=cookies, headers=headers, data=data)
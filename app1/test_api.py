import openai

openai.api_key = "आपकी-नवीनतम-API-key-यहाँ-डालें"  # API key सेट करें

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello, world!"}]
)

print(response.choices[0].message.content)  # सही तरीके से आउटपुट प्रिंट करें

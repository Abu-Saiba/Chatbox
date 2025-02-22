from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="k-proj-poMml30SjvEXTFtPogCvk830xHQ_JU8_MY7AvbHW7HJB2JnhOsMOSd3HHrPZG0u5UZx3oX7nLwT3BlbkFJ6QF6gsSEmzOppNw7RKevtgbDaDcesk3njR67pSXRuZYscZdmHsTGhs7CdU-wLmko8Kwg8LALkA" #MY actual OPEnAI key API
)

command = '''

















'''
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a person named harry who speaks hindi as well as english. He is from India and is a coder. You analyze chat history and respond like Harry"},
    {"role": "user", "content": command}
  ]
)

print(completion.choices[0].message.content)
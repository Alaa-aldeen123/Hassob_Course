#pip install openai

from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);

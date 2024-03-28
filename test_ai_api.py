from openai import OpenAI

GPT_QUESTION = 'If the following text is a single player prop for a future game in the context of sports betting, respond with the prop itself. Otherwise, respond with null. Additionally, respond with null if the text includes the token "RT @", "✅" or if there are multiple props:'
tweet_content = 'Adding De’Andre Hunter Under 20.5 Points (-130 ESPN)\n\n5/17 (29%) without Trae Young this year\n\nBlazers are BOTTOM FIVE against PG/SG/PF/C which means Hunter will have the TOUGHEST matchup on court at all times\nHad just 11 Points against them just two weeks ago\nHigh blowout potential with 11.5 point spread'

client = OpenAI(api_key='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')

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": f'{GPT_QUESTION}\n{tweet_content}'}
  ]
)

print(completion.choices[0].message.content)
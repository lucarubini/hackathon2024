import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-07-18",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

deployment_name='gpt-4o-mini' #This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment.

completion = client.completions.create(
  model=deployment_name,
  prompt='Write a tagline for an ice cream shop in italian and english. '
)

print("Assistant: " + completion.choices[0].message.content)



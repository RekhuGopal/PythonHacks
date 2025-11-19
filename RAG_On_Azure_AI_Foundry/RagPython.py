from openai import OpenAI

endpoint = "https://vrchi-mhzzds2t-eastus2.cognitiveservices.azure.com/openai/v1/"
deployment_name = "gpt-5.1-chat"
api_key = ""

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "Explain Infusion Therapy?",
        }
    ],
)

print(completion.choices[0].message)
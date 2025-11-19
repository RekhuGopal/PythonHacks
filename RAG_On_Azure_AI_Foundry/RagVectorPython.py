from openai import OpenAI

endpoint = "https://vrchi-mhzzds2t-eastus2.cognitiveservices.azure.com/openai/v1/"
deployment_name = "gpt-5.1-chat"
api_key = ""
vector_store_id = "demosearchaidemo"

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

completion = client.chat.completions.create(
    model=deployment_name,

    # ✅ Correct RAG method for Azure OpenAI
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",    # If using Azure Cognitive Search
                "parameters": {
                    "endpoint": "https://testaisearchdemo.search.windows.net",
                    "index_name": "demosearchaidemo",
                    "semantic_configuration": "default",
                    "query_type": "semantic",
                    "fields_mapping": {
                        "content_field": "content",
                        "vector_field": "contentVector"
                    }
                }
            }
        ]
    },

    messages=[
        {
            "role": "system",
            "content": "Use the RAG index to answer accurately."
        },
        {
            "role": "user",
            "content": "Explain Infusion Therapy?"
        }
    ],

    max_completion_tokens=300,
    temperature=0.2
)

print(completion.choices[0].message["content"])

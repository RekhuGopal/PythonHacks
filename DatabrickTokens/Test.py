from openai import OpenAI
import os

# How to get your Databricks token: https://docs.databricks.com/en/dev-tools/auth/pat.html
DATABRICKS_TOKEN = "<Token>"
# Alternatively in a Databricks notebook you can use this:
# DATABRICKS_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-c1debede-69af.cloud.databricks.com/serving-endpoints"
)

response = client.chat.completions.create(
    model="databricks-llama-4-maverick",
    messages=[
        {
            "role": "user",
            "content": "Explain how to lear databrick cloud"
        }
    ]
)

print(response.choices[0].message.content)
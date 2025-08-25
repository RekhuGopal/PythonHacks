import boto3
import botocore
import json
import streamlit as st

# provisioned_model_arn = "arn:aws:bedrock:us-east-1:687673817770:provisioned-model/30kls5y3seyr"
provisioned_model_arn = "arn:aws:bedrock:us-west-2:357171621133:model-customization-job/meta.llama3-2-3b-instruct-v1:0:128k/ccrm33pfo727"

st.set_page_config(page_title="Q&A Application")
st.markdown("# Question & Answering Application")
input_text = st.text_input('Whats your question?', key='text')
get_answer_button = st.button('Answer', type="primary")

boto3_bedrock = boto3.client('bedrock-runtime')
if get_answer_button:
    with st.spinner('Generating Answer...'):
        accept = 'application/json'
        contentType = 'application/json'
        # body = json.dumps({ 
        #     'prompt': input_text,
        #     'max_gen_len': 512,
        #     'top_p': 0.9,
        #     'temperature': 0.2
        # })
        body = json.dumps({ 
            'inputText': input_text,
            "textGenerationConfig": {"temperature": 0.5}
        })
        try:
            response = boto3_bedrock.invoke_model(body=body, modelId=provisioned_model_arn, accept=accept, contentType=contentType)
            response_body = json.loads(response.get('body').read().decode('utf-8'))
            # outputText = response_body['generation'].strip()
            outputText = response_body.get('results')[0].get('outputText')
            st.write(outputText)

        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'AccessDeniedException':
                print(f"\x1b[41m{error.response['Error']['Message']}\
                        \nTo troubeshoot this issue please refer to the following resources.\
                        \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                        \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")
            else:
                raise error
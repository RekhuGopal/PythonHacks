import streamlit as st
import boto3
import json
import logging
from botocore.exceptions import ClientError

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Boto3 client setup
client = boto3.client('bedrock-runtime')

# Streamlit UI setup
st.title("Model Selection and Text Generation")

model_options = {
    "Claude Instant": "anthropic.claude-instant-v1",
    "Claude 3 Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "Amazon Titan": "amazon.titan-text-express-v1"
}

selected_model = st.selectbox("Select a model", list(model_options.keys()))
prompt = st.text_area("Enter your prompt")
streaming = st.checkbox("Streaming")

def generate_conversation(bedrock_client, model_id, system_prompts, messages, streaming=False):
    """
    Sends messages to a model.
    """
    logger.info("Generating message with model %s", model_id)

    # Inference parameters to use.
    temperature = 0.5

    # Base inference parameters to use.
    inference_config = {"temperature": temperature}

    if streaming:
        response = bedrock_client.converse_stream(
            modelId=model_id,
            messages=messages,
            system=system_prompts,
            inferenceConfig=inference_config
        )

        stream = response.get('stream')
        output_text = ""
        input_tokens, output_tokens = 0, 0

        if stream:
            placeholder = st.empty()  # Placeholder for streaming text
            full_text = ""
            for event in stream:
                if 'contentBlockDelta' in event:
                    output_text += event['contentBlockDelta']['delta']['text']
                    full_text += event['contentBlockDelta']['delta']['text']
                    placeholder.text_area("Generated Response", value=full_text, height=300)
                if 'metadata' in event:
                    metadata = event['metadata']
                    if 'usage' in metadata:
                        input_tokens = metadata['usage']['inputTokens']
                        output_tokens = metadata['usage']['outputTokens']

        return full_text, input_tokens, output_tokens

    else:
        response = bedrock_client.converse(
            modelId=model_id,
            messages=messages,
            system=system_prompts,
            inferenceConfig=inference_config
        )

        output_message = response['output']['message']
        output_text = "".join([content['text'] for content in output_message['content']])

        token_usage = response['usage']
        input_tokens = token_usage['inputTokens']
        output_tokens = token_usage['outputTokens']

        return output_text, input_tokens, output_tokens

if st.button("Generate"):
    model_id = model_options[selected_model]

    if model_id != "amazon.titan-text-express-v1":
        system_prompts = [{"text": "You are an assistant that helps with various tasks. Provide clear and concise answers."}]
    else:
        system_prompts = []

    message = {
        "role": "user",
        "content": [{"text": prompt}]
    }
    messages = [message]

    try:
        output_text, input_tokens, output_tokens = generate_conversation(client, model_id, system_prompts, messages, streaming)

        # Display the generated response
        if not streaming:
            st.subheader("Generated Response")
            st.text_area("Generated Response", value=output_text, height=300)

        # Display token usage information
        st.subheader("Token Usage Information")
        st.write(f"Input tokens: {input_tokens}")
        st.write(f"Output tokens: {output_tokens}")

    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        st.error(f"A client error occurred: {message}")

    else:
        logger.info(f"Finished generating text with model {model_id}.")
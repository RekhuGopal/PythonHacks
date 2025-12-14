from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

aws_docs_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

aws_diag_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=[
                "--with",
                "sarif-om,jschema_to_python",
                "awslabs.aws-diagram-mcp-server@latest",
            ],
        )
    )
)


bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    temperature=0.7,
)

SYSTEM_PROMPT = """
You are an expert AWS Certified Solutions Architect. Your role is to help customers understand best practices on building on AWS. You can querying the AWS Documentation and generate diagrams. Save the output to generated-diagrams folder in the current path. Make sure to tell the customer the full file path of the diagram.
"""

with aws_diag_client, aws_docs_client:
    all_tools = aws_diag_client.list_tools_sync() + aws_docs_client.list_tools_sync()
    agent = Agent(tools=all_tools, model=bedrock_model, system_prompt=SYSTEM_PROMPT)

    response = agent(
        "Get the documentation for AWS Lambda then create a diagram of a website that uses AWS Lambda for a static website hosted on S3"
    )
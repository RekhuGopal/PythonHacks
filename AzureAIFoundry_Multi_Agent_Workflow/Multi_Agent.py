import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ConnectedAgentTool, MessageRole
from azure.identity import DefaultAzureCredential

# Initialize client for your Azure AI Foundry project
project_client = AIProjectClient(
    endpoint="https://azureaifoundrydemo1.services.ai.azure.com/api/projects/firstProject",
    credential=DefaultAzureCredential(),
)

# Create a connected agent that gets stock prices
stock_price_agent = project_client.agents.create_agent(
    model="gpt-4.1",
    name="stock_price_bot",
    instructions=(
        "Your job is to get the stock price of a company. "
        "If you don't know the realtime stock price, return the last known stock price."
    ),
)

connected_agent = ConnectedAgentTool(
    id=stock_price_agent.id,
    name=stock_price_agent.name,
    description="Gets the stock price of a company"
)

# Create the main agent that uses the connected tool
agent = project_client.agents.create_agent(
    model="gpt-4.1",
    name="my-agent",
    instructions="You are a helpful agent and can use the stock price tool to answer user questions.",
    tools=connected_agent.definitions,
)

print(f"✅ Created main agent: {agent.name}, ID: {agent.id}")

# Create a new thread for the conversation
thread = project_client.agents.threads.create()
print(f"🧵 Created thread: {thread.id}")

# Add a user message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role=MessageRole.USER,
    content="What is the stock price of Microsoft?",
)
print(f"💬 Created user message: {message.id}")

# Run the agent on this thread
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"⚙️ Run finished with status: {run.status}")

if run.status == "failed":
    print(f"❌ Run failed: {run.last_error}")
else:
    # Retrieve all messages (including the assistant's response)
    messages = project_client.agents.messages.list(thread_id=thread.id)

    print("\n🧠 Agent conversation history:\n" + "-"*50)
    for msg in messages:
        role = msg.role.value if hasattr(msg.role, 'value') else msg.role
        print(f"\n[{role.upper()}]:")
        if msg.content:
            for c in msg.content:
                if hasattr(c, 'text') and c.text:
                    print(c.text)
                elif isinstance(c, str):
                    print(c)
        else:
            print("(No content)")

    # Extract latest assistant reply
    assistant_message = next((m for m in messages if m.role == MessageRole.ASSISTANT), None)
    if assistant_message:
        latest_reply = "".join([c.text for c in assistant_message.content if hasattr(c, 'text') and c.text])
        print("\n🧾 Final Agent Response:\n" + "-"*50)
        print(latest_reply)
    else:
        print("⚠️ No assistant response found.")
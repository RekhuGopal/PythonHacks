import boto3
import time
import json
import logging

# ===== CONFIG =====
REGION = "us-west-2"
IAM_ROLE_ARN = "arn:aws:iam::357171621133:role/ETLlambdaAccessRole"
FOUNDATION_MODEL = "anthropic.claude-opus-4-1-20250805-v1:0"
# ==================

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

agent_client = boto3.client("bedrock-agent", region_name=REGION)
runtime_client = boto3.client("bedrock-agent-runtime", region_name=REGION)
sts = boto3.client("sts")
ACCOUNT_ID = sts.get_caller_identity()["Account"]

# ---------------------------------------------------------
# Utilities
# ---------------------------------------------------------
def wait_for_agent(agent_id, ready_states=("PREPARED", "FAILED")):
    """Poll until agent reaches a terminal/ready state."""
    while True:
        desc = agent_client.get_agent(agentId=agent_id)["agent"]
        state = desc["agentStatus"]
        log.info(f"⏳ Agent {agent_id} status: {state}")
        if state in ready_states:
            return state
        time.sleep(5)


def create_and_prepare_agent(name, instruction):
    """Create an agent and wait until prepared."""
    log.info(f"🚀 Creating agent {name}")
    resp = agent_client.create_agent(
        agentName=name,
        foundationModel=FOUNDATION_MODEL,
        instruction=instruction,
        agentResourceRoleArn=IAM_ROLE_ARN,
        idleSessionTTLInSeconds=300,
        description=f"{name} for multi-agent orchestration demo"
    )
    agent_id = resp["agent"]["agentId"]

    # Wait until creation completes
    while True:
        status = agent_client.get_agent(agentId=agent_id)["agent"]["agentStatus"]
        if status != "CREATING":
            break
        log.info(f"⌛ {name} still creating...")
        time.sleep(5)

    # Prepare agent
    agent_client.prepare_agent(agentId=agent_id)
    wait_for_agent(agent_id)

    # Create alias
    alias_resp = agent_client.create_agent_alias(
        agentId=agent_id,
        agentAliasName=f"{name}-alias"
    )
    alias_id = alias_resp["agentAlias"]["agentAliasId"]
    log.info(f"✅ Created {name} ({agent_id}) alias {alias_id}")
    return agent_id, alias_id


def setup_orchestrator(orchestrator_name, agent_ids):
    """Create the orchestrator agent with SUPERVISOR_ROUTER collaboration."""
    instruction_text = (
        "You are an orchestrator. Route the problem text to AgentA for summarization, "
        "then send that summary to AgentB for drafting the customer response."
    )

    # Create orchestrator
    orch_resp = agent_client.create_agent(
        agentName=orchestrator_name,
        foundationModel=FOUNDATION_MODEL,
        instruction=instruction_text,
        agentResourceRoleArn=IAM_ROLE_ARN,
        idleSessionTTLInSeconds=300,
        description=f"{orchestrator_name} for multi-agent orchestration"
    )
    orchestrator_id = orch_resp["agent"]["agentId"]

    # Wait until creation completes
    while True:
        status = agent_client.get_agent(agentId=orchestrator_id)["agent"]["agentStatus"]
        if status != "CREATING":
            break
        log.info(f"⌛ {orchestrator_name} still creating...")
        time.sleep(5)

    # Set SUPERVISOR_ROUTER collaboration (just the enum string)
    agent_client.update_agent(
        agentId=orchestrator_id,
        agentName=orchestrator_name,
        foundationModel=FOUNDATION_MODEL,
        agentResourceRoleArn=IAM_ROLE_ARN,
        instruction=instruction_text,
        agentCollaboration="SUPERVISOR_ROUTER",
        orchestrationType="DEFAULT"
    )

    # Prepare orchestrator
    agent_client.prepare_agent(agentId=orchestrator_id)
    wait_for_agent(orchestrator_id)

    # Create alias
    alias_resp = agent_client.create_agent_alias(
        agentId=orchestrator_id,
        agentAliasName=f"{orchestrator_name}-alias"
    )
    orchestrator_alias = alias_resp["agentAlias"]["agentAliasId"]
    log.info(f"✅ Orchestrator {orchestrator_name} ({orchestrator_id}) alias {orchestrator_alias}")

    return orchestrator_id, orchestrator_alias


def invoke_agent(agent_id, alias_id, input_text):
    """Invoke an agent and stream output."""
    sid = f"session-{int(time.time())}"
    log.info(f"🎯 Invoking agent {agent_id}...")
    response = runtime_client.invoke_agent(
        agentId=agent_id,
        agentAliasId=alias_id,
        sessionId=sid,
        inputText=input_text,
    )
    output = ""
    for ev in response.get("completion", []):
        chunk = ev["chunk"]["bytes"].decode("utf-8")
        print(chunk, end="", flush=True)
        output += chunk
    print()
    return output


# ---------------------------------------------------------
# Create two agents: AgentA (summarizer), AgentB (responder)
# ---------------------------------------------------------
AGENT_A_ID, AGENT_A_ALIAS = create_and_prepare_agent(
    "AgentA", "Summarize the customer issue and highlight root cause."
)

AGENT_B_ID, AGENT_B_ALIAS = create_and_prepare_agent(
    "AgentB", "Draft a clear and empathetic customer response using the summary."
)

# ---------------------------------------------------------
# Create orchestrator
# ---------------------------------------------------------
ORCH_ID, ORCH_ALIAS = setup_orchestrator(
    "AgentOrchestrator",
    agent_ids=[AGENT_A_ID, AGENT_B_ID]
)

# ---------------------------------------------------------
# Invoke Orchestrator
# ---------------------------------------------------------
customer_issue = (
    "Customer reports 403 AccessDenied when uploading to S3 via IAM user. "
    "They verified credentials but still cannot upload."
)

final = invoke_agent(ORCH_ID, ORCH_ALIAS, customer_issue)
log.info(f"\n✅ Final Orchestrated Response:\n{final}")

# ---------------------------------------------------------
# Save config
# ---------------------------------------------------------
cfg = {
    "AgentA": {"id": AGENT_A_ID, "alias": AGENT_A_ALIAS},
    "AgentB": {"id": AGENT_B_ID, "alias": AGENT_B_ALIAS},
    "Orchestrator": {"id": ORCH_ID, "alias": ORCH_ALIAS}
}
with open("agents_config.json", "w") as f:
    json.dump(cfg, f, indent=2)
log.info("💾 Saved agent configuration to agents_config.json")

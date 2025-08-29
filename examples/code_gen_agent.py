from typing import List, cast
import chainlit as cl
import yaml
import subprocess
import tempfile
import os
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import ModelClientStreamingChunkEvent, TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient

@cl.step(type="tool")
def check_code_quality(code: str) -> str:
    """
    Checks the quality of the given Python code using flake8.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    
    try:
        result = subprocess.run(
            ["flake8", temp_file_path],
            capture_output=True,
            text=True,
            check=False
        )
        if result.stdout:
            return f"Code quality issues found:\n{result.stdout}"
        elif result.stderr:
            return f"Error running flake8: {result.stderr}"
        else:
            return "No code quality issues found. The code looks good."
    finally:
        os.remove(temp_file_path)

@cl.on_chat_start
async def start_chat() -> None:
    # Load model configuration and create the model client.
    with open("model_config.yaml", "r") as f:
        model_config = yaml.safe_load(f)
    model_client = ChatCompletionClient.load_component(model_config)

    # Create the CoderAgent.
    coder_agent = AssistantAgent(
        name="CoderAgent",
        model_client=model_client,
        system_message="You are the Coder. Your job is to write Python code to solve the user's problem. You will work with the CodeQualityAgent to ensure the code is of high quality.",
        model_client_stream=True,
    )

    # Create the CodeQualityAgent.
    code_quality_agent = AssistantAgent(
        name="CodeQualityAgent",
        tools=[check_code_quality],
        model_client=model_client,
        system_message="You are the Code Quality Agent. Your job is to review the code provided by the Coder. Use the check_code_quality tool to check for issues. If the code is good, respond with 'APPROVE'. Otherwise, provide feedback on what to fix.",
        model_client_stream=True,
    )

    # Create the UserProxyAgent.
    user_proxy_agent = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        code_execution_config=False,
        model_client_stream=True,
    )

    # Termination condition.
    termination = TextMentionTermination("APPROVE", sources=["CodeQualityAgent"])

    # Create the group chat.
    group_chat = RoundRobinGroupChat([user_proxy_agent, coder_agent, code_quality_agent], termination_condition=termination)

    # Set the group chat in the user session.
    cl.user_session.set("team", group_chat)

@cl.set_starters
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Generate a function to calculate fibonacci.",
            message="Write a Python function to calculate the nth fibonacci number.",
        ),
        cl.Starter(
            label="Generate a function to reverse a string.",
            message="Write a Python function that takes a string and returns its reverse.",
        ),
    ]

@cl.on_message
async def chat(message: cl.Message) -> None:
    # Get the team from the user session.
    team = cast(RoundRobinGroupChat, cl.user_session.get("team"))
    # Streaming response message.
    streaming_response: cl.Message | None = None
    # Stream the messages from the team.
    async for msg in team.run_stream(
        task=[TextMessage(content=message.content, source="user")],
        cancellation_token=CancellationToken(),
    ):
        if isinstance(msg, ModelClientStreamingChunkEvent):
            # Stream the model client response to the user.
            if streaming_response is None:
                # Start a new streaming response.
                streaming_response = cl.Message(content="", author=msg.source)
            await streaming_response.stream_token(msg.content)
        elif streaming_response is not None:
            # Done streaming the model client response.
            await streaming_response.send()
            streaming_response = None
        elif isinstance(msg, TaskResult):
            # Send the task termination message.
            final_message = "Task terminated. "
            if msg.stop_reason:
                final_message += msg.stop_reason
            await cl.Message(content=final_message).send()
        else:
            # Skip all other message types.
            pass

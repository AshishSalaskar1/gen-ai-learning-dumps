import requests
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

# Custom Ollama Client to replace OpenAI
class OllamaClient:
    def __init__(self, model="llama3", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.model_info = {"vision": False}  # Fake attribute to prevent AutoGen errors

    async def chat(self, messages):
        """ Simulates OpenAI's API response format for AutoGen compatibility """
        prompt = "\n".join([msg["content"] for msg in messages])
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt}
        )
        if response.status_code == 200:
            return {"choices": [{"message": {"role": "assistant", "content": response.json().get("response", "")}}]}
        return {"choices": [{"message": {"role": "assistant", "content": "Error: No response from Ollama"}}]}

# Initialize Ollama client
ollama_client = OllamaClient(model="llama3.2")

# Create AutoGen Agents
planner_agent = AssistantAgent(
    "planner_agent",
    model_client=ollama_client,
    description="A helpful assistant that can plan trips.",
    system_message="You are a helpful assistant that can suggest a travel plan for a user based on their request.",
)

local_agent = AssistantAgent(
    "local_agent",
    model_client=ollama_client,
    description="A local assistant that can suggest local activities or places to visit.",
    system_message="You are a helpful assistant that can suggest authentic and interesting local activities or places to visit for a user and can utilize any context information provided.",
)

language_agent = AssistantAgent(
    "language_agent",
    model_client=ollama_client,
    description="A helpful assistant that can provide language tips for a given destination.",
    system_message="You are a helpful assistant that can review travel plans, providing feedback on important/critical tips about how best to address language or communication challenges for the given destination. If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale.",
)

travel_summary_agent = AssistantAgent(
    "travel_summary_agent",
    model_client=ollama_client,
    description="A helpful assistant that can summarize the travel plan.",
    system_message="You are a helpful assistant that can take in all of the suggestions and advice from the other agents and provide a detailed final travel plan. You must ensure that the final plan is integrated and complete. YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, you can respond with TERMINATE.",
)

# Define a termination condition
termination = TextMentionTermination("TERMINATE")

# Create a RoundRobinGroupChat
group_chat = RoundRobinGroupChat(
    [planner_agent, local_agent, language_agent, travel_summary_agent], termination_condition=termination
)

# Run the chat
async def test():
    await Console(group_chat.run_stream(task="Plan a 3-day trip to Nepal."))

asyncio.run(test())  # Ensure proper async execution

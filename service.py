load_dotenv()
values_env_openai = dotenv_values(".env")

client = AzureChatOpenAI(
        api_key="",
        api_version="",
        azure_deployment="",
        azure_endpoint=""
    )

def create_prompt(context,query):
    header = "What is Diploblastic and Triploblastic Organisation"
    return header + context + "\n\n" + query + "\n"

client.ainvoke([])

async def generate_answer(conversation):
    response = await client.ainvoke(conversation)
    return (response.content).strip()



# complete code with helper fucntions 

from dotenv import load_dotenv, dotenv_values
from langchain_openai import AzureChatOpenAI

# ---------------------------
# 🔹 1. Load Environment Values
# ---------------------------
def load_openai_config():
    load_dotenv()
    return dotenv_values(".env")


# ---------------------------
# 🔹 2. Create Azure OpenAI Client
# ---------------------------
def get_azure_openai_client():
    config = load_openai_config()

    client = AzureChatOpenAI(
        api_key=config.get("AZURE_OPENAI_KEY", ""),
        api_version=config.get("AZURE_OPENAI_API_VERSION", ""),
        azure_deployment=config.get("AZURE_OPENAI_DEPLOYMENT", ""),
        azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT", "")
    )

    return client


# ---------------------------
# 🔹 3. Prompt Builder Helper
# ---------------------------
def create_prompt(context: str, query: str) -> str:
    header = "What is Diploblastic and Triploblastic Organisation?\n\n"
    full_prompt = header + context + "\n\nUser Question: " + query + "\n"
    return full_prompt


# ---------------------------
# 🔹 4. LLM Answer Generator (Async)
# ---------------------------
async def generate_answer(conversation: list):
    """
    conversation = [
        {"role": "system", "content": "..."},
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": user_input}
    ]
    """
    client = get_azure_openai_client()
    response = await client.ainvoke(conversation)
    return response.content.strip()


# ---------------------------
# 🔹 5. Example Function to Use LLM
# ---------------------------
async def ask_llm(context, user_question):
    """
    Builds prompt, prepares conversation, calls LLM async.
    """

    # Build prompt text
    prompt_text = create_prompt(context, user_question)

    # Prepare messages
    conversation = [
        {"role": "system", "content": "Assistant is a helpful Azure OpenAI model."},
        {"role": "assistant", "content": prompt_text},
        {"role": "user", "content": user_question}
    ]

    # Get final answer from LLM
    reply = await generate_answer(conversation)
    return reply

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

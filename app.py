st.header('Search Engine - Document')

user_input = st.text_input('Enter your question here:', 
                           'What is Diploblastic and Triploblastic Organisation ?')

if st.button('Submit'):

exclude_category = None

    print("Searching:", user_input)
    print("-------------------")
    filter = "category ne '{}'".format(exclude_category.replace("'", "''")) if exclude_category else None
    r = search_client.search(user_input, 
                            filter=filter,
                            query_type=QueryType.SEMANTIC, 
                            # query_type="simple",   # added to remove semantic search
                            query_language="en-us", 
                            query_speller="lexicon", 
                            # semantic_configuration_name="default", 
                            semantic_configuration_name = "configurationname",   # for jarvis1
                            top=3)
    results = [doc[KB_FIELDS_SOURCEPAGE] + ": " + doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") for doc in r]
    content = "\n".join(results)

references =[]
    for result in results:
        references.append(result.split(":")[0])
    st.markdown("### References:")
    st.write(" , ".join(set(references)))

conversation=[{"role": "system", "content": "Assistant is a great language model formed by OpenAI."}]
    prompt = create_prompt(content,user_input)            
    conversation.append({"role": "assistant", "content": prompt})
    conversation.append({"role": "user", "content": user_input})
    # reply = generate_answer(conversation)
    reply = asyncio.run(generate_answer(conversation))   # added

    st.markdown("### Answer is:")
    st.write(reply)



# without streamlit

def ask_question_backend(user_input):

    # --- 1. Prepare filter ---
    exclude_category = None
    if exclude_category:
        # Escape single quotes
        filter_query = "category ne '{}'".format(
            exclude_category.replace("'", "''")
        )
    else:
        filter_query = None

    print("Searching:", user_input)
    print("-------------------")

    # --- 2. Search from Azure Cognitive Search ---
    r = search_client.search(
        user_input,
        filter=filter_query,
        query_type=QueryType.SEMANTIC,
        query_language="en-us",
        query_speller="lexicon",
        semantic_configuration_name="configurationname",
        top=3
    )

    # --- 3. Format results ---
    results = [
        doc[KB_FIELDS_SOURCEPAGE] + ": " +
        doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "")
        for doc in r
    ]

    content = "\n".join(results)

    # --- 4. Extract references ---
    references = []
    for result in results:
        ref = result.split(":", 1)[0]   # safer split
        references.append(ref)

    unique_references = list(set(references))

    # --- 5. Build LLM conversation ---
    conversation = [
        {"role": "system", "content": "Assistant is a great language model formed by OpenAI."}
    ]

    prompt = create_prompt(content, user_input)
    
    conversation.append({"role": "assistant", "content": prompt})
    conversation.append({"role": "user", "content": user_input})

    # --- 6. Get LLM answer ---
    reply = asyncio.run(generate_answer(conversation))

    return {
        "answer": reply,
        "references": unique_references
    }




# final one############################################################
#######################################################################
#######################################################################

key = ""
index_name = ""
endpoint = ""
azure_credential =  AzureKeyCredential(key)

search_client = SearchClient(endpoint=endpoint,
                            index_name=index_name,
                            credential=azure_credential)

async def ai_search(user_input):

    # excludes the category field while performing the search, since no category field is present the code should run fine wihtout this excluding function.
    exclude_category = None 
    if exclude_category:
        filter_query = "category ne '{}'".format(exclude_category.replace("'", "''"))
    else:
        filter_query = None

    print("Searching:", user_input)
    print("-------------------")

    r = search_client.search(
        user_input,
        filter=filter_query,
        query_type=QueryType.SEMANTIC,   # works in two modes: simple and semantic
        query_language="en-us",
        query_speller="lexicon",   # spelling correction
        semantic_configuration_name="",
        top=3   # giving top 3 results
    )
    # output will be a list of three
    # [{sourcepage:"...", content:"..."},{},{}]

    # this gives the data from chunk where ever the query matches, KB_FIELDS_SOURCEPAGE this might refere to the page number, it creates a string
    # the output will be in the form -> "page5: the broker name is..."
    results = [doc[KB_FIELDS_SOURCEPAGE] + ": " + doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") for doc in r] 

    content = "\n".join(results)

    references = []
    for result in results:
        ref = result.split(":", 1)[0]   # extracts the page number from the results
        references.append(ref)  

    unique_references = list(set(references))  # creates a list of the page numbers and removes duplicates

    conversation = [
        {"role": "system", "content": "Assistant is a great language model formed by OpenAI."}
    ]

    prompt = create_prompt(content, user_input)     # combines the question and content, user query along with the results is given to the llm as a prompt to decide a final answer based on the question and the answers provided.
    
    conversation.append({"role": "assistant", "content": prompt})
    conversation.append({"role": "user", "content": user_input})

    # reply = asyncio.run(generate_answer(conversation))
    reply = await generate_answer(conversation)

    return {
        "answer": reply,
        "references": unique_references
    }

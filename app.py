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
  

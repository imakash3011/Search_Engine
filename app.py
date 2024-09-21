import streamlit as st
# using groq to access open source model
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper

# adding search engine tool (duckduckgo will help you to search anything on internet)
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv
load_dotenv()

## Arxiv and wikipedia tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper = arxiv_wrapper)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

search = DuckDuckGoSearchRun(name= "Search")

st.title("Langchain - Chat with search")

"""
In this example, we're using "streamlitcallbackhandler" to display the thoughts and actions of an agent in an interactve streamlit app.
"""

## Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API key:", type="password")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content":"Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

if prompt:=st.chat_input(placeholder="what is machine learning?") :
    st.session_state.messages.append({"role": "user", "content":prompt})
    st.chat_message("user").write(prompt)
    llm = ChatGroq(groq_api_key = api_key, model = "Llama3-8b-8192", streaming=True)
    tools = [search, arxiv, wiki]

    # converting tools into agent
    search_agent = search_agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_errors= True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({'role': 'assistant', "content": response})
        st.write(response)


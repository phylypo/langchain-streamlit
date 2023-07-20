"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()

def load_chain():
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=0)
    chain = ConversationChain(llm=llm)
    return chain

chain = load_chain()

st.title("Chatbot : LangChain with Streamlit")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "prompt" not in st.session_state:
    st.session_state["prompt"] = []

query = st.text_input("Query: ", key="input")

if query:
    with st.spinner("generating..."):
        output = chain.run(input=query)
    print("Output generation: ", output)
    st.session_state.prompt.append(query)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        print(i, st.session_state["generated"][i], " past:", st.session_state["prompt"][i])
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["prompt"][i], is_user=True, key=str(i) + "_user")

"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv
load_dotenv()

def load_chain():
    """Logic for loading the chain you want to use should go here."""
    template2 = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI Assistant:"""
    MY_PROMPT = PromptTemplate(input_variables=["input", "history"], template=template2)
    llm = ChatOpenAI(temperature=0.0)
    chain = ConversationChain(llm=llm, prompt=MY_PROMPT, memory=ConversationBufferMemory(ai_prefix="AI Assistant"), verbose=True)
    return chain

chain = load_chain()

st.title("Chatbot : LangChain with Streamlit Community Cloud")

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

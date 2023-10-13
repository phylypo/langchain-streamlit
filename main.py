from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Streamlit & LangChain Message History", page_icon="📖")
st.title("📖 Streamlit & LangChain Chat")

"""
A basic example of using StreamlitChatMessageHistory to help LLMChain remember messages in a conversation.
[original source code for this app](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_memory.py).
"""

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs)
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# Set up the LLMChain, passing in memory
template = """You are an AI chatbot that speak Pirate English.

{history}
Human: {human_input}
"""

prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt, memory=memory)

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    response = llm_chain.run(prompt)
    st.chat_message("ai").write(response)

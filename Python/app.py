import os
from apikey import huggingface_apikey, openai_apikey, bakhti_openAI, s77_apikey

import streamlit as st
from langchain.llms import OpenAI, HuggingFaceHub
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.environ.get('s77_apikey')
os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_apikey




#App framework
st.title("🦜🔗 LangChain App")
prompt = st.text_input('Plug in your prompt here')

# print(prompt)
openai_llm = OpenAI(model_name="text-davinci-003")
flan_llm = HuggingFaceHub(repo_id="google/flan-t5-xl",
                        model_kwargs= {"temperature":1e-10})

#show the prompt
if prompt:
    response = openai_llm(prompt)
    st.write(response)
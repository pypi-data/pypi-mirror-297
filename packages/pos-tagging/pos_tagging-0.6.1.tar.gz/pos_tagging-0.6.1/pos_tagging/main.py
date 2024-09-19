from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

api_key : str = ""

def api_key():
    if load_dotenv() == True:
        api_key = os.getenv('api_key')
    else:
        raise RuntimeError ("api key not found")
    return api_key

def tagging():
    sentence = input(str("Enter a sentence:\t"))
    key = api_key()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key= key)    
    result = llm.invoke("Act as a POS tagging AI agent and find tags for each word present in the following sentence '"+ sentence + "' Note: Output should be in numbered list for every word") 
    print(result.content)

if __name__ == '__main__':
    tagging()
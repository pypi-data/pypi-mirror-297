from langchain_google_genai import ChatGoogleGenerativeAI

def tagging():
    sentence = input(str("Enter a sentence:\t"))
    key = input(str("Enter your api key:\t"))
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key= key)    
    result = llm.invoke("Act as a POS tagging AI agent and find tags for each word present in the following sentence '"+ sentence + "' Note: Output should be in numbered list for every word with proper formatting") 
    print(result.content)

if __name__ == '__main__':
    tagging()
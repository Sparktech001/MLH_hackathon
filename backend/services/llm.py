import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# We initialize the LLM client here.
# Note: we use the new gemini-3.8-flash model as it's the recommended default for fast reasoning in 2026.
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

def generate_response(prompt: str) -> str:
    """
    Wrapper for generating a response from the LLM.
    This decoupling ensures our agent doesn't care which LLM SDK we are using under the hood.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# Small test block that runs if you execute `python llm.py` directly
if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("Please set your GOOGLE_API_KEY in the .env file.")
    else:
        print("Testing LLM Wrapper...")
        answer = generate_response("What is the capital of France?")
        print(f"Response: {answer}")

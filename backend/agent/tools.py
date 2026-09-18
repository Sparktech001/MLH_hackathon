from rag.retrieval import search_documents

# Tools that the LLM agent can use
# We can register these as function calling tools later, 
# but for now, they are standard Python functions we call manually.

def search_documents_tool(query: str, course: str = None):
    """Searches the student's ingested documents for information."""
    return search_documents(query, course)

def generate_quiz_tool(topic: str, course: str = None):
    """Generates a quiz on a topic."""
    return f"Quiz generation for {topic} is not yet implemented."

def create_study_plan_tool(topic: str, course: str = None):
    """Creates a study plan based on a topic and course."""
    return f"Study plan creation for {topic} is not yet implemented."

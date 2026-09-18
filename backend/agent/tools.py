from backend.rag.retrieval import search_documents

def search_documents_tool(query: str, course: str = None, user_email: str = None):
    """Searches the student's ingested documents for information."""
    return search_documents(query, user_email, course)

def generate_quiz_tool(topic: str, course: str = None, user_email: str = None):
    """Generates a quiz on a topic."""
    return f"Quiz generation for {topic} is not yet implemented."

def create_study_plan_tool(topic: str, course: str = None, user_email: str = None):
    """Creates a study plan based on a topic and course."""
    return f"Study plan creation for {topic} is not yet implemented."

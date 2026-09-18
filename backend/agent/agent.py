from agent.prompts import SYSTEM_PROMPT, ANSWER_PROMPT
from agent.tools import search_documents_tool, generate_quiz_tool, create_study_plan_tool
from services.llm import generate_response
from models.schemas import Source

def determine_intent(message: str) -> str:
    """
    Crude intent routing. In a production version, we would use
    an LLM router or native tool calling to decide this.
    """
    msg_lower = message.lower()
    if "quiz" in msg_lower or "questions" in msg_lower:
        return "quiz"
    elif "study plan" in msg_lower or "schedule" in msg_lower:
        return "study_plan"
    else:
        return "search"

def run(message: str, course: str = None) -> tuple[str, list[Source]]:
    """
    The main orchestrator.
    Returns a tuple of (answer_string, list_of_sources)
    """
    intent = determine_intent(message)
    
    if intent == "search":
        # 1. Retrieve relevant chunks
        chunks = search_documents_tool(message, course)
        
        # 2. Format context and extract sources
        context_str = ""
        sources = []
        
        # We manually track seen source combos to avoid duplicates in the UI
        seen = set()
        
        for i, chunk in enumerate(chunks):
            context_str += f"--- Document {i+1} ---\nText: {chunk.text}\nSource: {chunk.document}, Page: {chunk.page}\n\n"
            
            source_key = (chunk.document, chunk.page, chunk.course)
            if source_key not in seen:
                seen.add(source_key)
                sources.append(Source(document=chunk.document, page=chunk.page, course=chunk.course))
                
        if not chunks:
            context_str = "No relevant academic material found in the database."
            
        # 3. Build the prompt
        prompt = f"{SYSTEM_PROMPT}\n\n{ANSWER_PROMPT.format(question=message, context=context_str)}"
        
        # 4. Generate answer
        answer = generate_response(prompt)
        
        # 5. Return answer and sources
        return answer, sources
        
    elif intent == "quiz":
        return generate_quiz_tool(message, course), []
        
    elif intent == "study_plan":
        return create_study_plan_tool(message, course), []
        
    return "I'm not sure how to handle that request.", []

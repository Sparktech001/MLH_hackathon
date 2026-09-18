from backend.agent.prompts import SYSTEM_PROMPT, ANSWER_PROMPT
from backend.agent.tools import search_documents_tool, generate_quiz_tool, create_study_plan_tool
from backend.services.llm import generate_response
from backend.models.schemas import Source

def determine_intent(message: str) -> str:
    msg_lower = message.lower()
    if "quiz" in msg_lower or "questions" in msg_lower:
        return "quiz"
    elif "study plan" in msg_lower or "schedule" in msg_lower:
        return "study_plan"
    else:
        return "search"

def run(message: str, course: str = None, user_email: str = None) -> tuple[str, list[Source]]:
    intent = determine_intent(message)
    
    if intent == "search":
        chunks = search_documents_tool(message, course, user_email)
        context_str = ""
        sources = []
        seen = set()
        
        for i, chunk in enumerate(chunks):
            context_str += f"--- Document {i+1} ---\nText: {chunk.text}\nSource: {chunk.source_file}, Course: {chunk.course_code}\n\n"
            
            source_key = (chunk.source_file, chunk.page, chunk.course_code)
            if source_key not in seen:
                seen.add(source_key)
                sources.append(Source(source_file=chunk.source_file, page=chunk.page, course=chunk.course_code))
                
        if not chunks:
            context_str = "No relevant academic material found in the database."
            
        prompt = f"{SYSTEM_PROMPT}\n\n{ANSWER_PROMPT.format(question=message, context=context_str)}"
        answer = generate_response(prompt)
        return answer, sources
        
    elif intent == "quiz":
        return generate_quiz_tool(message, course, user_email), []
        
    elif intent == "study_plan":
        return create_study_plan_tool(message, course, user_email), []
        
    return "I'm not sure how to handle that request.", []

import os
from dotenv import load_dotenv
load_dotenv()

def explain_investigation(evidence: dict) -> str | None:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        from langchain_groq import ChatGroq
        from langchain_core.messages import SystemMessage, HumanMessage
        model = ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=0,
            api_key=api_key,
        )
        messages = [
            SystemMessage(content=(
                "You assist a human bank compliance analyst. Explain only the supplied evidence. "
                "Do not invent facts or claim that a crime occurred. Clearly distinguish observed "
                "facts from hypotheses. A rule alert is not proof of wrongdoing."
            )),
            HumanMessage(content=f"Write a concise investigation summary from this evidence:\n{evidence}")
        ]
        return str(model.invoke(messages).content)
    except Exception as exc:
        return f"LLM explanation unavailable ({type(exc).__name__}); deterministic findings are provided."

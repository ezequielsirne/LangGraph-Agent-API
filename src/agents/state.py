from pydantic import BaseModel, Field
from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Optional, List

class GraphState(BaseModel):
    chat_memory: ChatMessageHistory = Field(default_factory=ChatMessageHistory)
    user_question: Optional[str] = None
    retrieved_documents: Optional[List[str]] = None
    availability_response: Optional[dict] = None
    final_answer: Optional[str] = None

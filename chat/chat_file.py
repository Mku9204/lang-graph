import logging
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
model = ChatOpenAI()

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    messages = state['messages']
    
    response = model.invoke(messages)
    
    return {
        'messages':[response]
    }

check_pointer = MemorySaver()

graph =StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)


chatbot = graph.compile(checkpointer=check_pointer)

def initial_chat(message: str, id: int):
    try:
        user_message = message.strip()


        if user_message.lower() in ["exit", "quit", "bye"]:
            yield "Byeeee"
            return

        config = {
            "configurable": {
                "thread_id": str(id)
            }
        }

        stream = chatbot.stream(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
            stream_mode="messages"
        )

        for message_chunk, metadata in stream:
            if hasattr(message_chunk, "content") and message_chunk.content:
                yield message_chunk.content

    except Exception:
        logger.exception("Error in initial_chat_stream")
        yield "error"
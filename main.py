from bedrock_agentcore.runtime import BedrockAgentCoreApp
from langchain_groq import ChatGroq
from rag_tool import fitness_rag

# Memory Imports
from langgraph_checkpoint_aws import AgentCoreMemorySaver, AgentCoreMemoryStore
from langchain.agents.middleware import AgentMiddleware, AgentState
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore

import uuid
from datetime import datetime
import os
from zoneinfo import ZoneInfo

app = BedrockAgentCoreApp()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
)

MEMORY_ID = "fitness_bot_memory-PC76eCGoqm"

checkpointer = AgentCoreMemorySaver(memory_id=MEMORY_ID)
store = AgentCoreMemoryStore(memory_id=MEMORY_ID)


class MemoryMiddleware(AgentMiddleware):

    def pre_model_hook(
            self,
            state:AgentState,
            config:RunnableConfig,
            *,
            store:BaseStore
    ):
        actor_id = config["configurable"]["actor_id"]
        thread_id = config["configurable"]["thread_id"]

        namespace = (actor_id, thread_id)
        messages = state.get("messages", [])

        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):

                store.put(
                    namespace,
                    str(uuid.uuid4()),
                    {
                        "message": msg
                    }
                )

                break
        return {"messages":messages}

    def post_model_hook(
            self,
            state:AgentState,
            config:RunnableConfig,
            *,
            store:BaseStore
    ):
        actor_id = config["configurable"]["actor_id"]
        thread_id = config["configurable"]["thread_id"]

        namespace = (actor_id, thread_id)

        messages = state.get("messages", [])

        for msg in reversed(messages):
            if isinstance(msg, AIMessage):

                store.put(
                    namespace,
                    str(uuid.uuid4()),
                    {
                        "message":msg
                    }
                )
                break
        return state


@app.entrypoint
def invoke(payload, context):
    # SAFE PAYLOAD PARSING
    if isinstance(payload, str):
        query = payload
    else:
        query = payload.get("prompt") or payload.get("input") or ""

    actor_id = payload.get("actor_id", "default-user") if isinstance(payload, dict) else "default-user"
    thread_id = payload.get("thread_id", context.session_id) if isinstance(payload, dict) else context.session_id


    # -------- RAG --------
    context_docs = fitness_rag.invoke(query)

    namespace = (actor_id, thread_id)

    previous_messages = store.search(
        namespace,
        query=query,
        limit=6
    )

    history = ""

    if previous_messages:
        previous_messages = sorted(
            previous_messages,
            key=lambda x: x.key
        )

        for item in previous_messages:
            msg = item.value.get("message")

            if isinstance(msg, HumanMessage):
                history += f"User: {msg.content}\n"

            elif isinstance(msg, AIMessage):
                history += f"Assistant: {msg.content}\n"


    prompt = f"""

    You are a helpful fitness assistant.

    Use the conversation history to understand previous questions.

    Conversation History:
    {history}

    Knowledge Base Context:
    {context_docs}

    Current Question:
    {query}

    Answer clearly.
    """

    response = llm.invoke(prompt)

    answer = response.content

    store.put(
        namespace,
        str(uuid.uuid4()),
        {
            "message": HumanMessage(content=query)
        }
    )

    store.put(
        namespace,
        str(uuid.uuid4()),
        {
            "message": AIMessage(content=answer)
        }
    )


    return {
        "answer": answer,
        "actor_id": actor_id,
        "thread_id": thread_id
    }


if __name__ == "__main__":
    app.run()
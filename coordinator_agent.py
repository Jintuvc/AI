from ingestion_agent import IngestionAgent
from retrieval_agent import RetrievalAgent
from llmresponse_agent import LLMResponseAgent
from mcp import MCPMessage, MCPQueue
import uuid

class CoordinatorAgent:
    def __init__(self):
        self.ingestion = IngestionAgent()
        self.retrieval = RetrievalAgent()
        self.llm = LLMResponseAgent()
        self.queue = MCPQueue()

    def ingest_documents(self, file_paths):
        trace_id = str(uuid.uuid4())
        ingestion_msg = MCPMessage(
            sender="UIAgent",
            receiver="IngestionAgent",
            type="INGEST_FILES",  # Correct key name is 'type'
            trace_id=trace_id,
            payload={"file_paths": file_paths}
        )

        parsed_docs = self.ingestion.run(ingestion_msg.payload["file_paths"])

        retrieval_input_msg = MCPMessage(
            sender="IngestionAgent",
            receiver="RetrievalAgent",
            type="DOCUMENT_PARSED",
            trace_id=trace_id,
            payload={"docs": parsed_docs}
        )
        self.retrieval.index(retrieval_input_msg.payload["docs"])

    def answer_query(self, file_paths, query, trace_id):
        ingestion_msg = MCPMessage(
            sender="CoordinatorAgent",
            receiver="IngestionAgent",
            type="DOCUMENT_INGESTION",
            trace_id=trace_id,
            payload={"file_paths": file_paths}
        )

        parsed_docs = self.ingestion.run(ingestion_msg.payload["file_paths"])

        retrieval_input_msg = MCPMessage(
            sender="IngestionAgent",
            receiver="RetrievalAgent",
            type="DOCUMENT_PARSED",
            trace_id=trace_id,
            payload={"docs": parsed_docs}
        )
        self.retrieval.index(retrieval_input_msg.payload["docs"])

        top_chunks = self.retrieval.retrieve(query)
        llm_input_msg = MCPMessage(
            sender="RetrievalAgent",
            receiver="LLMResponseAgent",
            type="RETRIEVAL_RESULT",
            trace_id=trace_id,
            payload={"retrieved_context": top_chunks, "query": query}
        )

        answer = self.llm.get_answer(
            query=llm_input_msg.payload["query"],
            context_chunks=llm_input_msg.payload["retrieved_context"]
        )

        return answer, top_chunks

import streamlit as st
import os
import uuid
from coordinator_agent import CoordinatorAgent

# Page config
st.set_page_config(page_title="Agentic RAG Chatbot", layout="centered")
st.title("Agentic RAG Chatbot")

# Initialize session state
if "coordinator" not in st.session_state:
    st.session_state.coordinator = CoordinatorAgent()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # (question, answer)
if "file_paths" not in st.session_state:
    st.session_state.file_paths = []

# --- SIDEBAR (Left) ---
st.sidebar.header("🧠 Chat History")
# Show only questions in sidebar
for i, (q, _) in enumerate(st.session_state.chat_history):
    st.sidebar.markdown(f"**{i+1}.** {q}")

# Button to clear chat history
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.chat_history.clear()
    st.sidebar.success("Chat history cleared!")

# --- MAIN PAGE SCREEN ---

# Document uploader
st.subheader("📎 Upload documents")
uploaded_files = st.file_uploader(
    "Drag and drop files here",
    type=["pdf", "csv", "pptx", "docx", "txt", "md"],
    accept_multiple_files=True
)

# Save uploaded files
file_paths = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)
    st.session_state.file_paths = file_paths
    st.success(f"{len(file_paths)} file(s) uploaded successfully.")

# Ask question
if st.session_state.file_paths:
    query = st.text_input("💬 Ask a question based on the uploaded documents:")

    if st.button("🔍 Get Answer") and query:
        with st.spinner("Processing..."):
            trace_id = str(uuid.uuid4())
            answer, _ = st.session_state.coordinator.answer_query(
                st.session_state.file_paths,
                query,
                trace_id
            )
            st.session_state.chat_history.append((query, answer))

# Display full chat history in reverse (latest on top)
if st.session_state.chat_history:
    st.subheader(" Chat History ")
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history)):
        idx = len(st.session_state.chat_history) - i
        st.markdown(f"**Q{idx}: {q}**")
        st.markdown(f"**A{idx}:** {a}")
        st.markdown("---")

from pypdf import PdfReader
import io
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import numpy as np
import streamlit as st

# Set your Gemini API key (LESS SECURE - ONLY FOR PERSONAL, LOCAL USE)
genai.configure(api_key="API-KEY") # Replace with your actual API key

def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)  # Create a PdfReader object
        text = ""
        for page in reader.pages:       # Iterate through pages
            text += page.extract_text()  # Extract text from each page
        return text
    except Exception as e:
        return f"An error occurred during PDF processing: {str(e)}"

def chunk_text(text, chunk_size_words=1000, overlap_words=100):
    chunks = []
    start_word_index = 0
    words = text.split()

    while start_word_index < len(words):
        end_word_index = min(start_word_index + chunk_size_words, len(words))
        chunk_words = words[start_word_index:end_word_index]

        last_sentence_end = -1
        for i in range(len(chunk_words) - 1, -1, -1):
            if chunk_words[i].endswith("."):
                last_sentence_end = i
                break

        if last_sentence_end != -1:
            end_word_index = start_word_index + last_sentence_end + 1
            chunk_words = words[start_word_index:end_word_index]

        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        overlap = 0
        if end_word_index - start_word_index > chunk_size_words:
            overlap = overlap_words

        start_word_index += max(0, end_word_index - start_word_index - overlap)

    return chunks

model = SentenceTransformer('all-mpnet-base-v2')

def get_relevant_chunk(chunks, question):
    try:
        question_embedding = model.encode(question)

        best_chunk = None
        best_similarity = -1

        for i, chunk in enumerate(chunks):
            try:
                chunk_embedding = model.encode(chunk)
                similarity = util.cos_sim(question_embedding, chunk_embedding)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_chunk = chunk
            except Exception as e:
                print(f"Error processing chunk {i+1}: {e}")
                continue

        return best_chunk

    except Exception as e:
        print(f"Error in get_relevant_chunk: {e}")
        return None

def answer_question1(relevant_chunk, user_question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""Context:\n{relevant_chunk}\n\nQuestion:\n{user_question}\n\nAnswer:"""
    response = model.generate_content(prompt)
    return response.text

def summarise_the_pdf(chunks):
    try:
        summarised_text = ""
        model = genai.GenerativeModel("gemini-1.5-flash")
        for each_chunk in chunks:
            prompt = f"""Summarize the following text:\n{each_chunk}\n"""
            response = model.generate_content(prompt)
            summarised_text = summarised_text + response.text

        prompt = f"""Summarize the following text with in 500 words:\n{summarised_text}\n\nSummary:"""
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")

st.title("Chat-to-PDF")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("PDF UPLOADED SUCCESSFULLY")
    st.session_state["messages"] = []
    pdf_file = io.BytesIO(uploaded_file.read())
    extracted_text = extract_text_from_pdf(pdf_file)
    if "Error" in extracted_text:
        st.error(extracted_text) # Display error message
    else:
        chunks = chunk_text(extracted_text, chunk_size_words=1000, overlap_words=50)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        


        user_question = st.chat_input("Ask a question about the PDF")
        
        
        if user_question:
            with st.chat_message("user"):
                st.markdown(user_question)

            relevant_chunk = get_relevant_chunk(chunks, user_question)
            if relevant_chunk:
                try:
                    ans = answer_question1(relevant_chunk, user_question)
                    with st.chat_message("assistant"):
                        st.markdown(ans)

                    # Add messages to chat history
                    st.session_state.messages.append({"role": "user", "content": user_question})
                    st.session_state.messages.append({"role": "assistant", "content": ans})

                except Exception as e:
                    st.error(f"An error occurred during question answering: {e}")
            else:
                st.warning("No relevant information found for your question.")

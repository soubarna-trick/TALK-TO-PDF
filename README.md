# TALK-TO-PDF 📄💬  
A Streamlit-powered application that allows users to upload a PDF file and interact with it using natural language queries. The system extracts text from the PDF, processes it into manageable chunks, and uses a combination of **sentence embeddings** and **Google Gemini AI** to retrieve and generate context-aware responses.  

## 🚀 Features  
- 📂 **Upload PDF**: Users can upload any PDF document.  
- 🔍 **Ask Questions**: The app retrieves relevant content from the PDF and provides AI-generated answers.  
- 🧠 **Semantic Search**: Uses `sentence-transformers` for efficient similarity matching.  
- ✨ **AI-Powered Answers**: Utilizes **Gemini 1.5 Flash** for generating responses based on the extracted content.  
- 📝 **Summarization**: Generates a concise summary of the uploaded document.  
- 💬 **Chat History**: Maintains previous interactions within the session.  

## 🛠️ Technologies Used  
- **Python**  
- **Streamlit**  
- **PyPDF**  
- **Google Gemini AI**  
- **SentenceTransformers (SBERT)**  

## 📌 How to Run  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/chat-to-pdf.git
   cd chat-to-pdf
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:  
   ```bash
   streamlit run app.py
   ```

## ⚠️ Note  
Make sure to replace `"API-KEY"` with your actual **Gemini API key** before running the application.  

Happy coding! 🚀

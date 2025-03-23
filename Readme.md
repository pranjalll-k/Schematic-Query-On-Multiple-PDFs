# Schematic-Query-On-Multiple-PDFs
The project "Schematic Query on multiple PDFs using Langchain and Huggingface" presents a Streamlit application that leverages Langchain and Huggingface technologies to enable users to query uploaded PDF documents. The application processes PDFs, extracts text, creates vector embeddings, and utilizes the Together AI API to generate responses to user queries. By integrating advanced natural language processing capabilities, the project aims to streamline information retrieval from multiple PDF sources efficiently.
# Work Flow :
![mp2](https://github.com/pranjalll-k/Schematic-Query-On-Multiple-PDFs/assets/110484191/8c14f5a1-05b8-4b1e-9017-8a1dd6de0eac)

The application follows these steps to provide responses to your questions:

PDF Loading: The app reads multiple PDF documents and extracts their text content.

Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.

Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.

Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.

# License
The MultiPDF Chat App is released under the https://opensource.org/license/MIT.

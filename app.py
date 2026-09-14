# import ollama
# import psycopg
# import streamlit as st
# # from psycopg2.extensions import register_adapter,AsIs
# import os
# from dotenv import load_dotenv

# # load env variables from .env files
# load_dotenv()

# #PostgreSQL connection
# conn = psycopg.connect(
#     dbname = os.getenv("POSTGRES_DB_NAME"),
#     user=os.getenv("POSTGRES_DB_USER"),
#     password=os.getenv("POSTGRES_DB_PASSWORD"),
#     host=os.getenv("POSTGRES_DB_HOST"),
#     port=os.getenv("POSTGRES_DB_PORT")
# )

# cursor = conn.cursor()

# #document chunks
# documents = [
#     "Artificial Intelligence systems utilize Large Language Models (LLMs) to process, understand, and generate human-like text based on vast patterns in data.",
#     "Retrieval-Augmented Generation (RAG) improves AI accuracy by fetching relevant facts from an external database before generating a response",
#     "Modern AI applications often combine neural networks with vector databases to quickly search through millions of documents for precise information retrieval"
# ]

# st.title("Interactive Q&A system")
# st.write("Application demonstrates a Q & A system with documents")

# #Document chunking
# st.header("step1.Document chunking")
# st.write("Here are the documens")

# for i, doc in enumerate(documents,start=1):
#     st.write(f"**chunk {i}:** {doc}")

# #generate and store the embeddings
# embeddings = []

# # step 2: Generate and display embeddings
# st.header("Step 2: Generate Embeddings")
# st.write("Each document chunk is converted to an embedding")

# for doc in documents:
#     response = ollama.embeddings(
#     model="nomic-embed-text",
#     prompt=doc
# )

#     embedding = response["embedding"]
#     embeddings.append(embedding)

#     #insert chunk and corres embedding
#     cursor.execute(
#         "INSERT INTO document_chunks (content,embedding)" \
#         "VALUES (%s,%s)",(doc,embedding)
#     )

#     st.write(doc)
#     st.write(embedding)

# #Committ embeddings to database
# conn.commit()

# ## step 3:Retrieve relevant chunks
# st.header("Retrieve relevent chunks")
# question = st.text_input("Enter ur question")

# def get_relevant_chunks(question, top_n=3):
#     question_embb_response = ollama.embeddings(
#         model="nomic-embed-text",
#         prompt=question
#     )
    
#     question_embedding = question_embb_response["embedding"]

#     #query the top n
#     cursor.execute("""
#         SELECT content
#         FROM document_chunks
#         ORDER BY embedding <=> %s::vector
#         LIMIT %s
#     """,(question_embedding,top_n))

#     #fetch relevant chunks
#     relevant_chunks = [row[0] for row in cursor.fetchall()]
#     return relevant_chunks


import ollama
import psycopg
import streamlit as st
# from psycopg2.extensions import register_adapter,AsIs
import os
from dotenv import load_dotenv

# load env variables from .env files
load_dotenv()

#PostgreSQL connection
conn = psycopg.connect(
    dbname = os.getenv("POSTGRES_DB_NAME"),
    user=os.getenv("POSTGRES_DB_USER"),
    password=os.getenv("POSTGRES_DB_PASSWORD"),
    host=os.getenv("POSTGRES_DB_HOST"),
    port=os.getenv("POSTGRES_DB_PORT")
)

cursor = conn.cursor()

#document chunks
documents = [
    "Artificial Intelligence systems utilize Large Language Models (LLMs) to process, understand, and generate human-like text based on vast patterns in data.",
    "Retrieval-Augmented Generation (RAG) improves AI accuracy by fetching relevant facts from an external database before generating a response",
    "Modern AI applications often combine neural networks with vector databases to quickly search through millions of documents for precise information retrieval"
]

st.title("Interactive Q&A system")
st.write("Application demonstrates a Q & A system with documents")

#Document chunking
st.header("Step1:Document chunking")
st.write("Here are the documens")

for i, doc in enumerate(documents,start=1):
    st.write(f"**Chunk {i}:** {doc}")

#generate and store the embeddings
embeddings = []

# step 2: Generate and display embeddings
st.header("Step 2: Generate Embeddings")
st.write("Each document chunk is converted to an embedding")

#Clear vector DB 
cursor.execute("TRUNCATE TABLE document_chunks")

#Create Embedding and store in Vector DB
for doc in documents:
    response = ollama.embeddings(
    model="nomic-embed-text",
    prompt=doc
)
    embedding = response["embedding"]
    embeddings.append(embedding)

  
    #insert chunk and corres embedding
    cursor.execute(
        "INSERT INTO document_chunks (content,embedding)" \
        "VALUES (%s,%s)",(doc,embedding)
    )

# Display Chnunks and Vector Embeddings   
for i, doc in enumerate(documents,start=1):
    st.write(f"**chunk {i}:** {doc}")
    st.subheader("Embedding")
    st.write(embedding)

#Committ embeddings to database
conn.commit()

#step 3:Retrieve relevant chunks
st.header("Step 3: Raise a Query")
question = st.text_input(
    "Enter your question:",
    key="question_input"
)

# Function to Generate Embeddings for Question
def get_relevant_chunks(question, top_n=3):
    question_embb_response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=question
    )
    
    question_embedding = question_embb_response["embedding"]

    #query the top n
    cursor.execute("""
        SELECT content
        FROM document_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """,(question_embedding,top_n))

    #fetch relevant chunks
    relevant_chunks = [row[0] for row in cursor.fetchall()]
    return relevant_chunks

# Function to generate response
def generate_answer(question, relevant_chunks):

    # Combine retrieved chunks into context
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
    You are a helpful question-answering assistant.

    Answer the user's question using ONLY the information
    provided in the context below.

    If the answer cannot be found in the context, say:
    "I don't have enough information in the provided documents."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    try:
        # Call local LLM
        response = ollama.chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]
    except Exception as e:
        st.error(f"LLM error: {e}")


# Step 5: Q&A
if question:

    # Retrieve top-K chunks
    relevant_chunks = get_relevant_chunks(
        question,
        top_n=3
    )

    st.header("Step 4:Retrieve Relevant Chunks")

    for i, chunk in enumerate(relevant_chunks, start=1):
        st.write(f"**Chunk {i}:**")
        st.write(chunk)

    # Generate answer
    answer = generate_answer(
        question,
        relevant_chunks
    )

    st.subheader("Step 5: Generated Answer")
    st.write(answer)





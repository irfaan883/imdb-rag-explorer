import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# =========================
# CONFIG
# =========================
CSV_FILE = r"c:\Users\USER\Downloads\imdb_top_1000.csv"   # Make sure the file is in the same directory
DB_LOCATION = "./chroma_imdb_db"
COLLECTION_NAME = "imdb_top_1000"
BATCH_SIZE = 500

# =========================
# LOAD DATA
# =========================
if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(f"{CSV_FILE} not found.")

df = pd.read_csv(CSV_FILE)

required_columns = [
    "Series_Title", "Released_Year", "Certificate", "Runtime",
    "Genre", "IMDB_Rating", "Meta_score", "Director",
    "Star1", "Star2", "Star3", "Star4",
    "No_of_Votes", "Gross", "Overview"
]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# =========================
# EMBEDDINGS
# =========================
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# =========================
# VECTOR STORE
# =========================
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embeddings
)

existing_count = vector_store._collection.count()
print("Existing documents in DB:", existing_count)

# =========================
# INGEST DOCUMENTS (ONLY IF EMPTY)
# =========================
if existing_count == 0:
    print("Ingesting IMDB documents into Chroma...")

    documents = []
    ids = []

    for i, row in df.iterrows():
        content = (
            f"Title: {row['Series_Title']}\n"
            f"Year: {row['Released_Year']}\n"
            f"Certificate: {row['Certificate']}\n"
            f"Runtime: {row['Runtime']}\n"
            f"Genre: {row['Genre']}\n"
            f"IMDB Rating: {row['IMDB_Rating']}\n"
            f"Meta Score: {row['Meta_score']}\n"
            f"Director: {row['Director']}\n"
            f"Stars: {row['Star1']}, {row['Star2']}, {row['Star3']}, {row['Star4']}\n"
            f"Votes: {row['No_of_Votes']}\n"
            f"Gross: {row['Gross']}\n"
            f"Overview: {row['Overview']}"
        )

        doc = Document(
            page_content=content,
            metadata={
                "title": row["Series_Title"],
                "year": row["Released_Year"],
                "rating": row["IMDB_Rating"]
            },
            id=str(i)
        )

        documents.append(doc)
        ids.append(str(i))

    for i in range(0, len(documents), BATCH_SIZE):
        batch_docs = documents[i:i + BATCH_SIZE]
        batch_ids = ids[i:i + BATCH_SIZE]

        vector_store.add_documents(
            documents=batch_docs,
            ids=batch_ids
        )

        print(f"Inserted documents {i} to {i + len(batch_docs)}")

    print("Final document count:", vector_store._collection.count())

else:
    print("Using existing IMDB embeddings. No re-ingestion needed.")

# =========================
# RETRIEVER
# =========================
retriever = vector_store.as_retriever(
    search_kwargs={"k": 10}
)

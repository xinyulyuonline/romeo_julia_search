from pathlib import Path

from dotenv import load_dotenv
import os
from fastapi import FastAPI
from openai import AzureOpenAI
from pymongo import MongoClient

from datamodel import postData, askData

app = FastAPI()

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
MONGO_URI = os.getenv("MongoDB_URI")
CLIENT = MongoClient(MONGO_URI)
COLLECTION = CLIENT["Romeo_Julia"]["chunks"]
EMBEDDING_CLIENT = AzureOpenAI(
	api_key=os.getenv("AZURE_OEPNAI_KEY"),
	azure_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
	api_version="2024-02-15-preview",
)
EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
CHAT_MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def cosine_similarity(first_vector, second_vector):
	return sum(first * second for first, second in zip(first_vector, second_vector)) / (
		(sum(first * first for first in first_vector) ** 0.5) * (sum(second * second for second in second_vector) ** 0.5)
	)


@app.post("/addmongo")
def addmongo(data: postData):
	chunk_dir = BASE_DIR / data.filename
	inserted = []
	for index, chunk_file in enumerate(sorted(chunk_dir.glob("chunk_*.txt"))[: data.chunks], start=1):
		content = chunk_file.read_text(encoding="utf-8")
		document = {"chunk_index": index, "filename": chunk_file.name, "text": content}
		result = COLLECTION.insert_one(document)
		inserted.append({"filename": chunk_file.name, "id": str(result.inserted_id)})

	return {"inserted_count": len(inserted), "inserted": inserted}


@app.get("/creatembeddings")
def creatembeddings():
	updated = []
	for document in COLLECTION.find({"embedding": {"$exists": False}}):
		text = document.get("text", "")
		if not text:
			continue
		embedding = EMBEDDING_CLIENT.embeddings.create(model=EMBEDDING_MODEL, input=text).data[0].embedding
		COLLECTION.update_one({"_id": document["_id"]}, {"$set": {"embedding": embedding}})
		updated.append(str(document["_id"]))

	return {"updated_count": len(updated), "updated": updated}


@app.post("/ask_book_romio_julia")
def ask_book_romio_julia(data: askData):
	question_embedding = EMBEDDING_CLIENT.embeddings.create(model=EMBEDDING_MODEL, input=data.question).data[0].embedding
	results = []

	for document in COLLECTION.find({"embedding": {"$exists": True}}):
		score = cosine_similarity(question_embedding, document["embedding"])
		results.append({"filename": document.get("filename"), "text": document.get("text", ""), "score": score})

	results.sort(key=lambda item: item["score"], reverse=True)
	top_chunks = results[: data.chunks]
	context = "\n\n".join(chunk["text"] for chunk in top_chunks)
	answer = EMBEDDING_CLIENT.chat.completions.create(
		model=CHAT_MODEL,
		messages=[
			{"role": "system", "content": "Beantworte kurz und nur mit Hilfe der gegebenen Chunks. Wenn in den Chunks keine Antwort auf die Frage gefunden werden kann, antworte mit 'Ich weiß es nicht, frag Marvin.'. "},
			{"role": "user", "content": f"Frage: {data.question}\n\nChunks:\n{context}"},
		],
	).choices[0].message.content
	return {"question": data.question, "answer": answer, "chunks": top_chunks}
print(EMBEDDING_MODEL)
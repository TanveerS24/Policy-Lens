import json
from typing import Any, Dict, List, Optional

from app.config.settings import settings
from app.services.ollama_client import ollama
from app.vector_store.faiss_store import faiss_store


class PolicyRAGService:
    async def summarize_policy(self, text: str, title: Optional[str] = None) -> Dict[str, Any]:
        prompt = (
            "You are an AI assistant specialized in healthcare policy summarization. "
            "Extract key information from the following policy document and return JSON with keys: "
            "title, short_description, summary, eligibility_criteria, benefits, notes. "
            "Be concise, factual, and avoid speculation."
            f"\n\nPolicy: {text}"
        )
        if title:
            prompt = f"Policy Title: {title}\n\n" + prompt
        raw = await ollama.generate(settings.OLLAMA_SUMMARY_MODEL, prompt, max_tokens=800, temperature=0.0)
        # Attempt to parse JSON from model output
        for candidate in [raw, raw[raw.find("{"):]]:
            try:
                data = json.loads(candidate)
                return {
                    "title": data.get("title", title or ""),
                    "short_description": data.get("short_description", ""),
                    "summary": data.get("summary", ""),
                    "eligibility_criteria": data.get("eligibility_criteria", ""),
                    "benefits": data.get("benefits", ""),
                    "notes": data.get("notes", ""),
                }
            except Exception:
                continue
        # fallback
        return {
            "title": title or "",
            "short_description": raw.strip()[:512],
            "summary": raw.strip(),
            "eligibility_criteria": "",
            "benefits": "",
            "notes": "",
        }

    async def generate_embedding(self, text: str) -> List[float]:
        return await ollama.embed(settings.OLLAMA_SUMMARY_MODEL, text)

    async def store_chunks(self, policy_id: str, chunks: List[str]) -> None:
        vectors = []
        ids = []
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{policy_id}::{idx}"
            embedding = await self.generate_embedding(chunk)
            await faiss_store.store_chunk(policy_id, chunk_id, chunk, embedding)
            ids.append(chunk_id)
            vectors.append(embedding)
        # Keep in-memory index for quick search (optional)
        try:
            faiss_store.add_embeddings(ids, vectors)
        except Exception:
            pass

    async def ask_question(self, policy_id: str, question: str) -> str:
        top_chunks = await faiss_store.get_chunks_for_policy(policy_id, top_k=5)
        context = "\n\n".join([chunk.get("text", "") for chunk in top_chunks if chunk])
        prompt = (
            "You are an assistant that answers questions about a healthcare policy based on provided policy content. "
            "Use only the provided context. If information is not available, say you don't know.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        return await ollama.generate(settings.OLLAMA_QA_MODEL, prompt, max_tokens=512, temperature=0.0)

    async def check_eligibility(self, policy_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        # retrieve policy summary/eligibility
        top_chunks = await faiss_store.get_chunks_for_policy(policy_id, top_k=5)
        context = "\n\n".join([chunk.get("text", "") for chunk in top_chunks if chunk])
        prompt = (
            "You are an expert healthcare eligibility assistant. "
            "Given a policy and a person's profile, respond with JSON containing: eligible (true/false), reason, missing_requirements (list).\n"
            "Do not include any extra keys.\n\n"
            f"Policy Context:\n{context}\n\nPerson Profile:\n{json.dumps(profile, indent=2)}\n\n"
            "Respond in JSON only."
        )
        raw = await ollama.generate(settings.OLLAMA_QA_MODEL, prompt, max_tokens=512, temperature=0.0)
        try:
            return json.loads(raw)
        except Exception:
            # Fallback minimal
            return {"eligible": False, "reason": "Unable to determine eligibility.", "missing_requirements": []}


rag_service = PolicyRAGService()

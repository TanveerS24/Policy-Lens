"""
RAG Service
Retrieval Augmented Generation for policy Q&A
"""

import json
import numpy as np
from typing import List, Dict, Tuple
from app.services.ollama_service import OllamaClient
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SimpleEmbedder:
    """Simple embedding using word averaging"""
    
    @staticmethod
    def embed_text(text: str) -> np.ndarray:
        """Create simple embedding from text"""
        words = text.lower().split()
        # Simple hash-based embedding (in production use Ollama embeddings)
        embedding = np.array([hash(word) % 100 for word in words[:100]])
        if len(embedding) < 100:
            embedding = np.pad(embedding, (0, 100 - len(embedding)))
        return embedding[:100]
    
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity"""
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2) + 1e-10))


class RAGService:
    """Retrieval Augmented Generation for policy questions"""
    
    def __init__(self):
        self.ollama = OllamaClient()
        self.embedder = SimpleEmbedder()
    
    async def answer_question(
        self,
        question: str,
        policy_chunks: List[str],
        policy_summary: str,
    ) -> Dict:
        """
        Answer question about policy using RAG
        
        Steps:
        1. Retrieve relevant chunks
        2. Generate answer using Llama3.2
        3. Return answer with confidence
        """
        try:
            # Retrieve relevant chunks
            relevant_chunks = await self._retrieve_chunks(
                question,
                policy_chunks,
                top_k=3
            )
            
            # Create context
            context = "\n\n".join(relevant_chunks)
            
            # Generate answer
            prompt = f"""Based on this healthcare policy information, answer the following question.

POLICY SUMMARY:
{policy_summary}

RELEVANT POLICY DETAILS:
{context}

QUESTION: {question}

Provide a clear, accurate answer based only on the policy information provided. 
If the answer is not in the policy, say so clearly.
Keep the answer concise and helpful.
"""
            
            result = await self.ollama.generate(
                model=self.ollama.reasoning_model,
                prompt=prompt,
                temperature=0.4,
            )
            
            answer = result.get("response", "Could not generate answer")
            
            # Calculate confidence (placeholder - can be enhanced)
            confidence_score = 0.85
            
            logger.info(f"✅ Policy question answered")
            
            return {
                "question": question,
                "answer": answer,
                "confidence_score": confidence_score,
            }
        
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise
    
    async def _retrieve_chunks(
        self,
        query: str,
        chunks: List[str],
        top_k: int = 3,
    ) -> List[str]:
        """Retrieve most relevant chunks for query"""
        try:
            # Embed query
            query_embedding = self.embedder.embed_text(query)
            
            # Calculate similarity with all chunks
            similarities = []
            for chunk in chunks:
                chunk_embedding = self.embedder.embed_text(chunk)
                similarity = self.embedder.cosine_similarity(query_embedding, chunk_embedding)
                similarities.append((chunk, similarity))
            
            # Sort by similarity and get top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            retrieved_chunks = [chunk for chunk, _ in similarities[:top_k]]
            
            logger.info(f"✅ Retrieved {len(retrieved_chunks)} relevant chunks")
            return retrieved_chunks
        
        except Exception as e:
            logger.error(f"Error retrieving chunks: {e}")
            return chunks[:top_k]
    
    async def search_policies(
        self,
        query: str,
        policies: List[Dict],
    ) -> List[Tuple[Dict, float]]:
        """Search policies and return relevant ones with scores"""
        try:
            query_embedding = self.embedder.embed_text(query)
            
            results = []
            for policy in policies:
                # Combine title and summary for search
                policy_text = f"{policy.get('title', '')} {policy.get('summary', '')}"
                policy_embedding = self.embedder.embed_text(policy_text)
                
                similarity = self.embedder.cosine_similarity(query_embedding, policy_embedding)
                results.append((policy, similarity))
            
            # Sort by similarity
            results.sort(key=lambda x: x[1], reverse=True)
            
            logger.info(f"✅ Searched {len(policies)} policies")
            return results
        
        except Exception as e:
            logger.error(f"Error searching policies: {e}")
            return []

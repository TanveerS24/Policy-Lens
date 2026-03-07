"""
Ollama Service
Interact with local Ollama models
"""

import aiohttp
from typing import Dict, Optional
from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class OllamaClient:
    """Client for Ollama API"""
    
    def __init__(
        self,
        base_url: str = settings.OLLAMA_URL,
        summarization_model: str = settings.OLLAMA_SUMMARIZATION_MODEL,
        reasoning_model: str = settings.OLLAMA_REASONING_MODEL,
    ):
        self.base_url = base_url
        self.summarization_model = summarization_model
        self.reasoning_model = reasoning_model
    
    async def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        temperature: float = 0.7,
    ) -> Dict:
        """
        Call Ollama generate endpoint
        """
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ Ollama generation successful with {model}")
                        return result
                    else:
                        logger.error(f"Ollama API error: {response.status}")
                        raise Exception(f"Ollama API returned {response.status}")
        
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            raise
    
    async def check_model(self, model: str) -> bool:
        """Check if model is available"""
        try:
            url = f"{self.base_url}/api/tags"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = [m["name"] for m in data.get("models", [])]
                        available = any(model in m for m in models)
                        
                        if available:
                            logger.info(f"✅ Model {model} is available")
                        else:
                            logger.warning(f"⚠️  Model {model} is not available")
                        
                        return available
                    else:
                        logger.error(f"Failed to check models: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"Error checking model: {e}")
            return False
    
    async def pull_model(self, model: str) -> bool:
        """Pull model from registry"""
        try:
            url = f"{self.base_url}/api/pull"
            payload = {"name": model}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status in [200, 201]:
                        logger.info(f"✅ Model {model} pulled successfully")
                        return True
                    else:
                        logger.error(f"Failed to pull model: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"Error pulling model: {e}")
            return False

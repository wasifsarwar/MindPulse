"""Loader for Mental Health Counseling Conversations dataset."""

import json
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
from loguru import logger


class CounselingDataLoader:
    """Loads and manages the counseling conversations dataset."""
    
    def __init__(self, data_path: Path):
        """
        Initialize the counseling data loader.
        
        Args:
            data_path: Path to the combined_dataset.json file
        """
        self.data_path = data_path
        self.conversations: List[Dict[str, str]] = []
        self.embeddings: np.ndarray = None
        self._load_data()
    
    def _load_data(self):
        """Load conversations from JSON file."""
        try:
            logger.info(f"Loading counseling data from {self.data_path}")
            
            with open(self.data_path, 'r', encoding='utf-8') as f:
                # Each line is a separate JSON object
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            conversation = json.loads(line)
                            self.conversations.append(conversation)
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse line: {e}")
                            continue
            
            logger.info(f"✅ Loaded {len(self.conversations)} counseling conversations")
            
        except FileNotFoundError:
            logger.error(f"❌ Counseling data file not found: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Error loading counseling data: {e}")
            raise
    
    def get_all_conversations(self) -> List[Dict[str, str]]:
        """Get all conversations."""
        return self.conversations
    
    def search_by_keywords(self, keywords: List[str], max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search conversations by keywords.
        
        Args:
            keywords: List of keywords to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of matching conversations
        """
        results = []
        keywords_lower = [k.lower() for k in keywords]
        
        for conv in self.conversations:
            context = conv.get("Context", "").lower()
            response = conv.get("Response", "").lower()
            
            # Check if any keyword appears in context or response
            if any(kw in context or kw in response for kw in keywords_lower):
                results.append(conv)
                if len(results) >= max_results:
                    break
        
        return results
    
    def get_random_sample(self, n: int = 5) -> List[Dict[str, str]]:
        """
        Get a random sample of conversations.
        
        Args:
            n: Number of conversations to sample
            
        Returns:
            List of random conversations
        """
        if len(self.conversations) <= n:
            return self.conversations
        
        indices = np.random.choice(len(self.conversations), size=n, replace=False)
        return [self.conversations[i] for i in indices]
    
    def search_by_similarity(
        self, 
        query: str, 
        embeddings_model=None, 
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Search conversations by semantic similarity using embeddings.
        
        Args:
            query: Query string
            embeddings_model: Sentence transformer model for embeddings
            max_results: Maximum number of results
            
        Returns:
            List of most similar conversations
        """
        if not embeddings_model:
            # Fallback to keyword search
            logger.warning("No embeddings model provided, using keyword search")
            words = query.lower().split()
            return self.search_by_keywords(words, max_results)
        
        try:
            # Compute query embedding
            query_embedding = embeddings_model.encode([query])[0]
            
            # Compute conversation embeddings if not cached
            if self.embeddings is None:
                logger.info("Computing embeddings for counseling conversations...")
                texts = [
                    f"{conv.get('Context', '')} {conv.get('Response', '')}"
                    for conv in self.conversations
                ]
                self.embeddings = embeddings_model.encode(texts, show_progress_bar=True)
                logger.info("✅ Embeddings computed")
            
            # Compute cosine similarities
            similarities = np.dot(self.embeddings, query_embedding) / (
                np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # Get top k indices
            top_indices = np.argsort(similarities)[::-1][:max_results]
            
            # Return top conversations
            return [self.conversations[i] for i in top_indices]
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            # Fallback to keyword search
            words = query.lower().split()
            return self.search_by_keywords(words, max_results)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the dataset."""
        return {
            "total_conversations": len(self.conversations),
            "avg_context_length": np.mean([
                len(conv.get("Context", "")) for conv in self.conversations
            ]),
            "avg_response_length": np.mean([
                len(conv.get("Response", "")) for conv in self.conversations
            ]),
        }


"""Loader for Sentiment Analysis for Mental Health dataset."""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from loguru import logger


class SentimentDataLoader:
    """Loads and manages the sentiment analysis dataset."""
    
    def __init__(self, data_path: Path):
        """
        Initialize the sentiment data loader.
        
        Args:
            data_path: Path to the sentiment analysis dataset directory
        """
        self.data_path = data_path
        self.data: pd.DataFrame = None
        self._load_data()
    
    def _load_data(self):
        """Load sentiment data from CSV/JSON files."""
        try:
            # Try to find CSV or JSON files in the directory
            if not self.data_path.exists():
                logger.warning(f"⚠️ Sentiment data path does not exist: {self.data_path}")
                logger.info("Creating placeholder sentiment data for demo purposes")
                self._create_placeholder_data()
                return
            
            # Look for CSV files
            csv_files = list(self.data_path.glob("*.csv"))
            if csv_files:
                logger.info(f"Loading sentiment data from {csv_files[0]}")
                self.data = pd.read_csv(csv_files[0])
                logger.info(f"✅ Loaded {len(self.data)} sentiment records")
            else:
                logger.warning("⚠️ No CSV files found in sentiment data directory")
                self._create_placeholder_data()
                
        except Exception as e:
            logger.error(f"❌ Error loading sentiment data: {e}")
            self._create_placeholder_data()
    
    def _create_placeholder_data(self):
        """Create placeholder data for demo purposes."""
        logger.info("Creating placeholder sentiment data...")
        
        # Example mental health sentiment data
        placeholder = {
            'text': [
                "I feel so hopeless and can't see a way forward",
                "Today was a good day, I felt productive and happy",
                "I'm really anxious about tomorrow's meeting",
                "I've been feeling numb and disconnected lately",
                "Therapy has been helping me process my emotions",
                "I can't sleep at night, my mind won't stop racing",
                "I'm grateful for my support system",
                "Everything feels overwhelming right now"
            ],
            'sentiment': [
                'negative', 'positive', 'negative', 'negative',
                'positive', 'negative', 'positive', 'negative'
            ],
            'emotion': [
                'sadness', 'joy', 'anxiety', 'numbness',
                'hope', 'anxiety', 'gratitude', 'overwhelm'
            ]
        }
        
        self.data = pd.DataFrame(placeholder)
        logger.info(f"✅ Created {len(self.data)} placeholder sentiment records")
    
    def get_all_data(self) -> pd.DataFrame:
        """Get all sentiment data."""
        return self.data if self.data is not None else pd.DataFrame()
    
    def get_by_sentiment(self, sentiment: str) -> pd.DataFrame:
        """
        Get records by sentiment label.
        
        Args:
            sentiment: Sentiment label (positive, negative, neutral)
            
        Returns:
            Filtered dataframe
        """
        if self.data is None or self.data.empty:
            return pd.DataFrame()
        
        # Try common column names
        sentiment_col = None
        for col in ['sentiment', 'label', 'emotion', 'feeling']:
            if col in self.data.columns:
                sentiment_col = col
                break
        
        if sentiment_col:
            return self.data[
                self.data[sentiment_col].str.lower() == sentiment.lower()
            ]
        
        return pd.DataFrame()
    
    def search_by_text(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search sentiment data by text content.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            List of matching records
        """
        if self.data is None or self.data.empty:
            return []
        
        # Find text column
        text_col = None
        for col in ['text', 'statement', 'message', 'content']:
            if col in self.data.columns:
                text_col = col
                break
        
        if not text_col:
            return []
        
        # Simple text search
        query_lower = query.lower()
        mask = self.data[text_col].str.lower().str.contains(query_lower, na=False)
        results = self.data[mask].head(max_results)
        
        return results.to_dict('records')
    
    def get_sentiment_distribution(self) -> Dict[str, int]:
        """Get distribution of sentiment labels."""
        if self.data is None or self.data.empty:
            return {}
        
        # Find sentiment column
        sentiment_col = None
        for col in ['sentiment', 'label', 'emotion']:
            if col in self.data.columns:
                sentiment_col = col
                break
        
        if sentiment_col:
            return self.data[sentiment_col].value_counts().to_dict()
        
        return {}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the dataset."""
        if self.data is None or self.data.empty:
            return {
                "total_records": 0,
                "sentiment_distribution": {},
                "available_columns": []
            }
        
        return {
            "total_records": len(self.data),
            "sentiment_distribution": self.get_sentiment_distribution(),
            "available_columns": list(self.data.columns)
        }


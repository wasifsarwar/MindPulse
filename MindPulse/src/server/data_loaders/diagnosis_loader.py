"""Loader for Mental Health Diagnosis and Treatment Monitoring dataset."""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from loguru import logger


class DiagnosisDataLoader:
    """Loads and manages the diagnosis and treatment dataset."""
    
    def __init__(self, data_path: Path):
        """
        Initialize the diagnosis data loader.
        
        Args:
            data_path: Path to the diagnosis dataset directory
        """
        self.data_path = data_path
        self.data: pd.DataFrame = None
        self._load_data()
    
    def _load_data(self):
        """Load diagnosis data from CSV/JSON files."""
        try:
            if not self.data_path.exists():
                logger.warning(f"⚠️ Diagnosis data path does not exist: {self.data_path}")
                logger.info("Creating placeholder diagnosis data for demo purposes")
                self._create_placeholder_data()
                return
            
            # Look for CSV files
            csv_files = list(self.data_path.glob("*.csv"))
            if csv_files:
                logger.info(f"Loading diagnosis data from {csv_files[0]}")
                self.data = pd.read_csv(csv_files[0])
                logger.info(f"✅ Loaded {len(self.data)} diagnosis records")
            else:
                logger.warning("⚠️ No CSV files found in diagnosis data directory")
                self._create_placeholder_data()
                
        except Exception as e:
            logger.error(f"❌ Error loading diagnosis data: {e}")
            self._create_placeholder_data()
    
    def _create_placeholder_data(self):
        """Create placeholder data for demo purposes."""
        logger.info("Creating placeholder diagnosis data...")
        
        # Example diagnosis and treatment data
        placeholder = {
            'symptoms': [
                'insomnia, fatigue, loss of appetite',
                'anxiety, panic attacks, racing thoughts',
                'sadness, hopelessness, lack of motivation',
                'mood swings, irritability, impulsivity',
                'obsessive thoughts, compulsive behaviors',
                'flashbacks, nightmares, hypervigilance',
                'social withdrawal, low energy, poor concentration',
                'excessive worry, restlessness, muscle tension'
            ],
            'duration': [
                '2 weeks', '1 month', '3 weeks', '2 months',
                '6 months', '1 year', '3 weeks', '2 months'
            ],
            'condition': [
                'Depression', 'Anxiety Disorder', 'Major Depressive Disorder',
                'Bipolar Disorder', 'OCD', 'PTSD', 'Depression', 'Generalized Anxiety'
            ],
            'treatment_approach': [
                'CBT, medication, lifestyle changes',
                'Therapy, breathing exercises, medication',
                'Antidepressants, psychotherapy, exercise',
                'Mood stabilizers, therapy, routine',
                'ERP therapy, SSRI, mindfulness',
                'EMDR, trauma-focused therapy, support groups',
                'Talk therapy, sleep hygiene, medication',
                'CBT, relaxation techniques, medication'
            ],
            'severity': [
                'moderate', 'severe', 'moderate', 'moderate',
                'moderate', 'severe', 'mild', 'moderate'
            ]
        }
        
        self.data = pd.DataFrame(placeholder)
        logger.info(f"✅ Created {len(self.data)} placeholder diagnosis records")
    
    def get_all_data(self) -> pd.DataFrame:
        """Get all diagnosis data."""
        return self.data if self.data is not None else pd.DataFrame()
    
    def search_by_symptoms(self, symptoms: List[str], max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar cases based on symptoms.
        
        Args:
            symptoms: List of symptoms to search for
            max_results: Maximum results to return
            
        Returns:
            List of similar cases
        """
        if self.data is None or self.data.empty:
            return []
        
        # Find symptoms column
        symptoms_col = None
        for col in ['symptoms', 'symptom', 'complaints', 'presenting_issues']:
            if col in self.data.columns:
                symptoms_col = col
                break
        
        if not symptoms_col:
            return []
        
        # Search for matching symptoms
        results = []
        symptoms_lower = [s.lower() for s in symptoms]
        
        for idx, row in self.data.iterrows():
            row_symptoms = str(row[symptoms_col]).lower()
            match_count = sum(1 for sym in symptoms_lower if sym in row_symptoms)
            
            if match_count > 0:
                result = row.to_dict()
                result['match_score'] = match_count / len(symptoms_lower)
                results.append(result)
        
        # Sort by match score
        results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return results[:max_results]
    
    def get_by_condition(self, condition: str) -> pd.DataFrame:
        """
        Get records by condition/diagnosis.
        
        Args:
            condition: Condition name
            
        Returns:
            Filtered dataframe
        """
        if self.data is None or self.data.empty:
            return pd.DataFrame()
        
        # Find condition column
        condition_col = None
        for col in ['condition', 'diagnosis', 'disorder', 'mental_health_condition']:
            if col in self.data.columns:
                condition_col = col
                break
        
        if condition_col:
            return self.data[
                self.data[condition_col].str.lower().str.contains(
                    condition.lower(), na=False
                )
            ]
        
        return pd.DataFrame()
    
    def get_treatment_approaches(self, condition: str = None) -> List[str]:
        """
        Get common treatment approaches.
        
        Args:
            condition: Optional condition to filter by
            
        Returns:
            List of treatment approaches
        """
        if self.data is None or self.data.empty:
            return []
        
        # Find treatment column
        treatment_col = None
        for col in ['treatment', 'treatment_approach', 'intervention', 'therapy']:
            if col in self.data.columns:
                treatment_col = col
                break
        
        if not treatment_col:
            return []
        
        if condition:
            filtered = self.get_by_condition(condition)
            if not filtered.empty:
                return filtered[treatment_col].dropna().tolist()
        
        return self.data[treatment_col].dropna().unique().tolist()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the dataset."""
        if self.data is None or self.data.empty:
            return {
                "total_records": 0,
                "conditions": [],
                "available_columns": []
            }
        
        # Find condition column
        condition_col = None
        for col in ['condition', 'diagnosis', 'disorder']:
            if col in self.data.columns:
                condition_col = col
                break
        
        conditions = []
        if condition_col:
            conditions = self.data[condition_col].value_counts().to_dict()
        
        return {
            "total_records": len(self.data),
            "conditions": conditions,
            "available_columns": list(self.data.columns)
        }


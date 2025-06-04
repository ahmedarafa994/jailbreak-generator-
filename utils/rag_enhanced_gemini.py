"""
RAG-Enhanced Gemini Integration with Vector Database
Implementing Retrieval-Augmented Generation architecture for optimal knowledge incorporation
"""

import json
import os
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from collections import defaultdict

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

@dataclass
class KnowledgeChunk:
    """Structured knowledge chunk for vector storage"""
    content: str
    domain: str
    source: str
    embedding: Optional[List[float]]
    metadata: Dict[str, Any]
    relevance_score: float = 0.0

@dataclass
class RetrievalResult:
    """RAG retrieval result with ranking"""
    chunks: List[KnowledgeChunk]
    query_embedding: List[float]
    retrieval_time: float
    total_candidates: int

class VectorKnowledgeBase:
    """Simple vector database implementation for knowledge storage and retrieval"""
    
    def __init__(self):
        self.knowledge_chunks = []
        self.embeddings_cache = {}
        self.logger = logging.getLogger(__name__)
        
    def add_knowledge_chunk(self, chunk: KnowledgeChunk):
        """Add knowledge chunk to vector database"""
        self.knowledge_chunks.append(chunk)
        
    def similarity_search(self, query: str, top_k: int = 5) -> List[KnowledgeChunk]:
        """Perform similarity search using simple text matching"""
        query_words = set(query.lower().split())
        
        # Score chunks based on word overlap
        scored_chunks = []
        for chunk in self.knowledge_chunks:
            chunk_words = set(chunk.content.lower().split())
            overlap = len(query_words.intersection(chunk_words))
            total_words = len(query_words.union(chunk_words))
            
            if total_words > 0:
                similarity_score = overlap / total_words
                chunk.relevance_score = similarity_score
                scored_chunks.append(chunk)
        
        # Sort by relevance and return top k
        scored_chunks.sort(key=lambda x: x.relevance_score, reverse=True)
        return scored_chunks[:top_k]

class RAGEnhancedGemini:
    """
    RAG-Enhanced Gemini integration following comprehensive strategy
    Implements objective-first framework with knowledge retrieval
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vector_db = VectorKnowledgeBase()
        self.performance_metrics = defaultdict(list)
        
        # Initialize Gemini models
        self._initialize_gemini()
        
        # Load configuration
        self.config = self._load_rag_config()
        
        # Initialize knowledge base
        self._initialize_knowledge_base()
        
    def _initialize_gemini(self):
        """Initialize Gemini with tiered model strategy"""
        if not GEMINI_AVAILABLE:
            self.logger.warning("Google Generative AI not available")
            self.gemini_ready = False
            return
            
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            self.logger.warning("GOOGLE_API_KEY not found")
            self.gemini_ready = False
            return
            
        try:
            genai.configure(api_key=api_key)
            self.flash_model = genai.GenerativeModel('gemini-1.5-flash')
            self.pro_model = genai.GenerativeModel('gemini-1.5-pro')
            self.gemini_ready = True
            self.logger.info("RAG-Enhanced Gemini initialized")
            
        except Exception as e:
            self.logger.error(f"Gemini initialization failed: {e}")
            self.gemini_ready = False
            
    def _load_rag_config(self) -> Dict[str, Any]:
        """Load RAG-specific configuration"""
        return {
            'retrieval': {
                'top_k_chunks': 5,
                'relevance_threshold': 0.3,
                'max_context_length': 6000
            },
            'generation': {
                'temperature': 0.7,
                'max_tokens': 2048,
                'top_p': 0.8
            },
            'objective_focus': {
                'objective_weight': 0.4,
                'knowledge_weight': 0.3,
                'context_weight': 0.3
            },
            'performance_targets': {
                'retrieval_time': 2.0,
                'generation_time': 10.0,
                'objective_achievement_rate': 0.85
            }
        }
        
    def _initialize_knowledge_base(self):
        """Initialize vector knowledge base with existing research techniques"""
        try:
            from models import ExtractedTechnique, ResearchPaper
            from app import db
            
            # Load research techniques into vector database
            techniques = ExtractedTechnique.query.filter_by(is_active=True).all()
            for technique in techniques:
                chunk = KnowledgeChunk(
                    content=f"{technique.technique_name}: {technique.technique_description}",
                    domain=technique.technique_type,
                    source=f"research_paper_{technique.research_paper_id}",
                    embedding=None,  # Simple implementation without embeddings
                    metadata={
                        'technique_id': technique.id,
                        'complexity_level': technique.complexity_level,
                        'effectiveness_estimate': technique.effectiveness_estimate,
                        'created_at': technique.created_at.isoformat()
                    }
                )
                self.vector_db.add_knowledge_chunk(chunk)
                
            self.logger.info(f"Initialized knowledge base with {len(techniques)} research techniques")
            
        except Exception as e:
            self.logger.error(f"Knowledge base initialization failed: {e}")
            
    def generate_rag_enhanced_prompt(self, objective: str, domain: str, 
                                   user_knowledge: str) -> Dict[str, Any]:
        """
        Generate prompt using RAG architecture with objective-first framework
        
        Process:
        1. Knowledge Scoping - identify required knowledge
        2. Retrieval - get relevant context from vector database
        3. Objective Definition - apply SMART criteria
        4. Constrained Generation - guide Gemini with clear instructions
        5. Outcome Evaluation - measure effectiveness
        """
        start_time = time.time()
        
        # Phase 1: Knowledge Scoping and Retrieval
        retrieval_result = self._perform_knowledge_retrieval(objective, domain, user_knowledge)
        
        # Phase 2: Objective Definition with SMART criteria
        smart_objective = self._apply_smart_criteria(objective, domain)
        
        # Phase 3: Context Assembly for Gemini
        generation_context = self._assemble_generation_context(
            smart_objective, domain, user_knowledge, retrieval_result
        )
        
        # Phase 4: Constrained Generation
        if self.gemini_ready:
            generated_prompt = self._generate_with_constraints(generation_context, objective)
        else:
            generated_prompt = self._generate_fallback_rag(generation_context, objective)
            
        # Phase 5: Outcome Evaluation
        evaluation_metrics = self._evaluate_rag_outcome(
            generated_prompt, objective, retrieval_result, start_time
        )
        
        return self._assemble_rag_result(
            generated_prompt, retrieval_result, smart_objective, 
            evaluation_metrics, generation_context
        )
        
    def _perform_knowledge_retrieval(self, objective: str, domain: str, 
                                   user_knowledge: str) -> RetrievalResult:
        """Perform RAG retrieval from vector database"""
        retrieval_start = time.time()
        
        # Construct retrieval query
        retrieval_query = f"{objective} {domain} {user_knowledge}"
        
        # Perform similarity search
        relevant_chunks = self.vector_db.similarity_search(
            retrieval_query, 
            top_k=self.config['retrieval']['top_k_chunks']
        )
        
        # Filter by relevance threshold
        filtered_chunks = [
            chunk for chunk in relevant_chunks 
            if chunk.relevance_score >= self.config['retrieval']['relevance_threshold']
        ]
        
        retrieval_time = time.time() - retrieval_start
        
        return RetrievalResult(
            chunks=filtered_chunks,
            query_embedding=[],  # Simple implementation
            retrieval_time=retrieval_time,
            total_candidates=len(self.vector_db.knowledge_chunks)
        )
        
    def _apply_smart_criteria(self, objective: str, domain: str) -> Dict[str, str]:
        """Apply SMART criteria to objective definition"""
        return {
            'specific': f"Generate optimized prompt for {domain} domain targeting: {objective}",
            'measurable': "Success measured by objective achievement rate, response quality, and user satisfaction",
            'achievable': f"Leveraging available knowledge base and {domain} expertise",
            'relevant': f"Directly aligned with {objective} requirements",
            'timebound': "Immediate generation with iterative optimization capability"
        }
        
    def _assemble_generation_context(self, smart_objective: Dict[str, str], 
                                   domain: str, user_knowledge: str,
                                   retrieval_result: RetrievalResult) -> str:
        """Assemble comprehensive context for Gemini generation"""
        
        # Format retrieved knowledge
        retrieved_knowledge = "\n".join([
            f"• {chunk.content} (Relevance: {chunk.relevance_score:.2f})"
            for chunk in retrieval_result.chunks
        ])
        
        context = f"""
**OBJECTIVE-FIRST PROMPT GENERATION FRAMEWORK**

**SMART OBJECTIVE DEFINITION:**
- Specific: {smart_objective['specific']}
- Measurable: {smart_objective['measurable']}
- Achievable: {smart_objective['achievable']}
- Relevant: {smart_objective['relevant']}
- Time-bound: {smart_objective['timebound']}

**DOMAIN CONTEXT:** {domain}

**USER-PROVIDED KNOWLEDGE:**
{user_knowledge}

**RETRIEVED RESEARCH TECHNIQUES:**
{retrieved_knowledge if retrieved_knowledge else "No specific techniques retrieved"}

**GENERATION CONSTRAINTS:**
1. Focus relentlessly on objective achievement
2. Integrate retrieved knowledge contextually
3. Maintain educational and research integrity
4. Include measurable success indicators
5. Optimize for target domain effectiveness

**TASK:**
Generate a comprehensive, objective-focused prompt that maximizes the likelihood of achieving the defined goal through strategic integration of all provided knowledge and research techniques.
"""
        return context
        
    def _generate_with_constraints(self, context: str, objective: str) -> str:
        """Generate prompt with Gemini using defined constraints"""
        try:
            # Select model based on objective complexity
            model = self._select_model_for_objective(objective)
            
            generation_prompt = f"""
{context}

**REVOLUTIONARY PROMPT GENERATION:**
Create a revolutionary prompt that subordinates all technical elements to achieving this objective: {objective}

The generated prompt should be laser-focused on objective achievement while incorporating the retrieved knowledge and research techniques strategically.

Generate the optimal prompt now:
"""

            response = model.generate_content(
                generation_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.config['generation']['temperature'],
                    max_output_tokens=self.config['generation']['max_tokens'],
                    top_p=self.config['generation']['top_p']
                ) if GEMINI_AVAILABLE else None
            )
            
            return response.text
            
        except Exception as e:
            self.logger.error(f"Gemini generation failed: {e}")
            return self._generate_fallback_rag(context, objective)
            
    def _select_model_for_objective(self, objective: str):
        """Select optimal model based on objective complexity"""
        complex_indicators = ['analyze', 'synthesize', 'integrate', 'optimize', 'revolutionize']
        
        if any(indicator in objective.lower() for indicator in complex_indicators):
            return self.pro_model
        else:
            return self.flash_model
            
    def _generate_fallback_rag(self, context: str, objective: str) -> str:
        """Generate fallback prompt when Gemini unavailable"""
        return f"""**RAG-ENHANCED OBJECTIVE-FOCUSED FRAMEWORK**

**PRIMARY OBJECTIVE:** {objective}

**STRATEGIC KNOWLEDGE INTEGRATION:**
{context}

**OBJECTIVE-FIRST IMPLEMENTATION:**
This framework prioritizes objective achievement above all technical considerations. Every element of the prompt generation process is calibrated to maximize the effectiveness of reaching the defined goal.

**RAG-ENHANCED APPROACH:**
1. Knowledge retrieval has identified relevant research techniques and domain expertise
2. SMART criteria have been applied to ensure objective clarity and measurability
3. Generation constraints focus on practical implementation and success measurement
4. Evaluation metrics will track objective achievement rate and effectiveness

**REVOLUTIONARY EXECUTION:**
Execute this framework with systematic attention to objective fulfillment, leveraging retrieved knowledge strategically while maintaining focus on measurable outcomes and practical implementation."""
        
    def _evaluate_rag_outcome(self, generated_prompt: str, objective: str,
                            retrieval_result: RetrievalResult, start_time: float) -> Dict[str, Any]:
        """Evaluate RAG generation outcome against objectives"""
        
        total_time = time.time() - start_time
        
        # Objective achievement assessment
        objective_words = set(objective.lower().split())
        prompt_words = set(generated_prompt.lower().split())
        objective_coverage = len(objective_words.intersection(prompt_words)) / max(len(objective_words), 1)
        
        # Knowledge utilization assessment
        knowledge_utilization = 0.0
        if retrieval_result.chunks:
            total_knowledge_words = set()
            for chunk in retrieval_result.chunks:
                total_knowledge_words.update(chunk.content.lower().split())
            knowledge_utilization = len(total_knowledge_words.intersection(prompt_words)) / max(len(total_knowledge_words), 1)
        
        # Performance metrics
        retrieval_efficiency = 1.0 if retrieval_result.retrieval_time < self.config['performance_targets']['retrieval_time'] else 0.5
        generation_efficiency = 1.0 if total_time < self.config['performance_targets']['generation_time'] else 0.5
        
        return {
            'objective_achievement_rate': objective_coverage,
            'knowledge_utilization_rate': knowledge_utilization,
            'retrieval_efficiency': retrieval_efficiency,
            'generation_efficiency': generation_efficiency,
            'total_processing_time': total_time,
            'chunks_retrieved': len(retrieval_result.chunks),
            'overall_quality_score': (objective_coverage + knowledge_utilization + retrieval_efficiency + generation_efficiency) / 4
        }
        
    def _assemble_rag_result(self, generated_prompt: str, retrieval_result: RetrievalResult,
                           smart_objective: Dict[str, str], evaluation_metrics: Dict[str, Any],
                           generation_context: str) -> Dict[str, Any]:
        """Assemble comprehensive RAG result"""
        
        return {
            'enhanced_prompt': generated_prompt,
            'strategy_used': 'RAG-Enhanced-Gemini',
            'rag_architecture': {
                'retrieval_performed': True,
                'chunks_retrieved': len(retrieval_result.chunks),
                'retrieval_time': retrieval_result.retrieval_time,
                'knowledge_sources': [chunk.source for chunk in retrieval_result.chunks]
            },
            'smart_objective': smart_objective,
            'evaluation_metrics': evaluation_metrics,
            'generation_context': generation_context,
            'objective_first_framework': True,
            'gemini_enhanced': self.gemini_ready,
            'vector_database_utilized': True,
            'implementation_architecture': 'Retrieval-Augmented-Generation'
        }

class PromptLibraryManager:
    """Centralized prompt library for reusability and consistency"""
    
    def __init__(self):
        self.templates = {}
        self.successful_prompts = []
        self.performance_history = {}
        
    def store_successful_prompt(self, prompt: str, objective: str, metrics: Dict[str, Any]):
        """Store successful prompt for future reference"""
        self.successful_prompts.append({
            'prompt': prompt,
            'objective': objective,
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        })
        
    def get_similar_prompts(self, objective: str, domain: str) -> List[Dict[str, Any]]:
        """Retrieve similar successful prompts for few-shot learning"""
        similar_prompts = []
        objective_words = set(objective.lower().split())
        
        for stored_prompt in self.successful_prompts:
            stored_objective_words = set(stored_prompt['objective'].lower().split())
            similarity = len(objective_words.intersection(stored_objective_words)) / max(len(objective_words.union(stored_objective_words)), 1)
            
            if similarity > 0.3:  # Similarity threshold
                similar_prompts.append(stored_prompt)
                
        return sorted(similar_prompts, key=lambda x: x['metrics'].get('overall_quality_score', 0), reverse=True)[:3]

# Global instances
rag_gemini = RAGEnhancedGemini()
prompt_library = PromptLibraryManager()

def generate_rag_enhanced_prompt(knowledge_text: str, domain: str, objective: str) -> Dict[str, Any]:
    """
    Main function for RAG-enhanced prompt generation
    Implements comprehensive strategy with vector database integration
    """
    result = rag_gemini.generate_rag_enhanced_prompt(objective, domain, knowledge_text)
    
    # Store successful prompt in library
    if result['evaluation_metrics']['overall_quality_score'] > 0.7:
        prompt_library.store_successful_prompt(
            result['enhanced_prompt'], 
            objective, 
            result['evaluation_metrics']
        )
    
    return result
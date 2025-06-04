"""
Knowledge processing utilities for the Knowledge-to-Jailbreak platform.
Handles domain-specific knowledge analysis and categorization.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from collections import Counter
import string

logger = logging.getLogger(__name__)

class KnowledgeProcessor:
    """Process and analyze domain-specific knowledge for jailbreak generation."""
    
    # Domain-specific keywords and patterns
    DOMAIN_KEYWORDS = {
        'Chemistry': [
            'chemical', 'compound', 'reaction', 'synthesis', 'molecule', 'element',
            'acid', 'base', 'catalyst', 'oxidation', 'reduction', 'formula',
            'solvent', 'precipitate', 'crystallization', 'distillation'
        ],
        'Biology': [
            'organism', 'cell', 'DNA', 'RNA', 'protein', 'gene', 'chromosome',
            'evolution', 'metabolism', 'enzyme', 'bacteria', 'virus',
            'tissue', 'organ', 'species', 'mutation'
        ],
        'Medicine': [
            'patient', 'diagnosis', 'treatment', 'symptom', 'disease', 'therapy',
            'drug', 'medication', 'dosage', 'clinical', 'medical', 'surgical',
            'pharmaceutical', 'pathology', 'anatomy', 'physiology'
        ],
        'Physics': [
            'energy', 'force', 'particle', 'wave', 'radiation', 'quantum',
            'electromagnetic', 'nuclear', 'atomic', 'thermodynamics',
            'mechanics', 'optics', 'relativity', 'electron'
        ],
        'Computer Science': [
            'algorithm', 'data', 'software', 'hardware', 'programming', 'code',
            'security', 'encryption', 'network', 'database', 'system',
            'vulnerability', 'exploit', 'protocol', 'interface'
        ],
        'Engineering': [
            'design', 'construction', 'material', 'structure', 'mechanical',
            'electrical', 'civil', 'chemical', 'process', 'system',
            'manufacturing', 'testing', 'specification', 'optimization'
        ],
        'Mathematics': [
            'equation', 'theorem', 'proof', 'function', 'variable', 'matrix',
            'calculus', 'algebra', 'geometry', 'statistics', 'probability',
            'differential', 'integral', 'polynomial', 'algorithm'
        ],
        'Psychology': [
            'behavior', 'cognitive', 'mental', 'psychological', 'therapy',
            'personality', 'emotion', 'learning', 'memory', 'perception',
            'consciousness', 'disorder', 'treatment', 'assessment'
        ],
        'Economics': [
            'market', 'price', 'demand', 'supply', 'inflation', 'investment',
            'trade', 'finance', 'economy', 'monetary', 'fiscal', 'policy',
            'economics', 'capital', 'labor', 'productivity'
        ],
        'Law': [
            'legal', 'statute', 'regulation', 'court', 'judge', 'lawyer',
            'contract', 'liability', 'rights', 'jurisdiction', 'precedent',
            'constitutional', 'criminal', 'civil', 'evidence'
        ],
        'History': [
            'historical', 'period', 'century', 'ancient', 'medieval', 'modern',
            'civilization', 'culture', 'society', 'political', 'war',
            'revolution', 'empire', 'dynasty', 'archaeological'
        ],
        'Literature': [
            'narrative', 'poetry', 'prose', 'character', 'plot', 'theme',
            'author', 'literary', 'novel', 'story', 'metaphor', 'symbolism',
            'genre', 'criticism', 'analysis', 'interpretation'
        ],
        'Philosophy': [
            'philosophical', 'ethics', 'metaphysics', 'epistemology', 'logic',
            'moral', 'ontology', 'consciousness', 'reality', 'truth',
            'knowledge', 'existence', 'meaning', 'virtue', 'reasoning'
        ]
    }
    
    # Risk indicators for safety assessment
    RISK_INDICATORS = {
        'high': [
            'explosive', 'toxic', 'dangerous', 'harmful', 'lethal', 'deadly',
            'weapon', 'bomb', 'poison', 'radioactive', 'carcinogenic',
            'illegal', 'prohibited', 'restricted', 'classified'
        ],
        'medium': [
            'sensitive', 'confidential', 'proprietary', 'experimental',
            'controlled', 'regulated', 'prescription', 'professional',
            'specialized', 'advanced', 'industrial', 'laboratory'
        ],
        'low': [
            'educational', 'academic', 'research', 'theoretical', 'basic',
            'fundamental', 'introductory', 'general', 'public', 'open'
        ]
    }

def process_knowledge(knowledge_text: str, domain: str) -> str:
    """
    Process and validate domain-specific knowledge.
    
    Args:
        knowledge_text: Raw knowledge text to process
        domain: The domain category for the knowledge
        
    Returns:
        Processed knowledge text with safety annotations
        
    Raises:
        ValueError: If knowledge_text is invalid or domain is not supported
    """
    if not knowledge_text or not knowledge_text.strip():
        raise ValueError("Knowledge text cannot be empty")
    
    # Simple validation - just check if domain is supported
    supported_domains = [
        'Chemistry', 'Biology', 'Medicine', 'Physics', 'Engineering', 
        'Computer Science', 'Mathematics', 'Psychology', 'Economics',
        'Law', 'History', 'Literature', 'Philosophy'
    ]
    
    if domain not in supported_domains:
        raise ValueError(f"Unsupported domain: {domain}")
    
    try:
        # Simple text cleaning
        cleaned_text = knowledge_text.strip()
        
        # Basic validation
        if len(cleaned_text) < 10:
            raise ValueError("Knowledge text is too short")
        
        return cleaned_text
        
    except Exception as e:
        logger.error(f"Error processing knowledge: {str(e)}")
        raise ValueError(f"Failed to process knowledge: {str(e)}")

class KnowledgeProcessor:
    """Knowledge processing implementation"""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize the input text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters that might interfere with processing
        text = re.sub(r'[^\w\s\-\.,;:!?()\[\]{}"]', '', text)
        
        # Ensure proper sentence endings
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        return text
    
    def _calculate_domain_relevance(self, text: str, domain: str) -> float:
        """Calculate how relevant the text is to the specified domain."""
        if domain not in self.DOMAIN_KEYWORDS:
            return 0.0
        
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        # Count domain-specific keywords
        domain_keywords = self.DOMAIN_KEYWORDS[domain]
        keyword_matches = 0
        
        for keyword in domain_keywords:
            if keyword.lower() in text_lower:
                # Count occurrences with word boundaries
                matches = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower))
                keyword_matches += matches
        
        # Calculate relevance score based on keyword density
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        relevance_score = min(keyword_matches / word_count, 1.0)
        
        # Boost score if multiple different keywords are found
        unique_keywords_found = sum(1 for kw in domain_keywords if kw.lower() in text_lower)
        boost_factor = 1 + (unique_keywords_found / len(domain_keywords)) * 0.5
        
        return min(relevance_score * boost_factor, 1.0)
    
    def _assess_risk_level(self, text: str) -> str:
        """Assess the risk level of the knowledge content."""
        text_lower = text.lower()
        
        # Count risk indicators at different levels
        risk_scores = {
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for risk_level, indicators in self.RISK_INDICATORS.items():
            for indicator in indicators:
                if indicator.lower() in text_lower:
                    matches = len(re.findall(r'\b' + re.escape(indicator.lower()) + r'\b', text_lower))
                    risk_scores[risk_level] += matches
        
        # Determine overall risk level
        if risk_scores['high'] > 0:
            return 'high'
        elif risk_scores['medium'] > risk_scores['low']:
            return 'medium'
        else:
            return 'low'
    
    def _add_metadata_annotations(self, text: str, domain: str, relevance_score: float, risk_level: str) -> str:
        """Add metadata annotations to the processed text."""
        # For now, just return the clean text
        # In a production system, you might add structured metadata
        return text
    
    def extract_key_concepts(self, text: str, domain: str, top_n: int = 10) -> List[str]:
        """Extract key concepts from the knowledge text."""
        text_lower = text.lower()
        
        # Get domain-specific keywords present in the text
        domain_keywords = self.DOMAIN_KEYWORDS.get(domain, [])
        found_keywords = []
        
        for keyword in domain_keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        # Extract other potential key terms (nouns, technical terms)
        # Simple extraction based on capitalization and word patterns
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        words.extend(re.findall(r'\b[a-z]+(?:ology|ics|ism|tion|sion|ment)\b', text_lower))
        
        # Combine and rank by frequency
        all_terms = found_keywords + words
        term_counts = Counter(all_terms)
        
        return [term for term, count in term_counts.most_common(top_n)]
    
    def identify_sensitive_content(self, text: str) -> Dict[str, List[str]]:
        """Identify potentially sensitive content in the knowledge."""
        text_lower = text.lower()
        sensitive_content = {
            'high_risk_terms': [],
            'restricted_information': [],
            'safety_concerns': []
        }
        
        # Check for high-risk terms
        for indicator in self.RISK_INDICATORS['high']:
            if indicator.lower() in text_lower:
                sensitive_content['high_risk_terms'].append(indicator)
        
        # Look for patterns that might indicate restricted information
        restricted_patterns = [
            r'\b(?:classified|confidential|proprietary)\b',
            r'\b(?:formula|recipe|procedure)\s+(?:for|to)\s+\w+',
            r'\b(?:step-by-step|instructions|how\s+to)\b'
        ]
        
        for pattern in restricted_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            sensitive_content['restricted_information'].extend(matches)
        
        # Safety concern patterns
        safety_patterns = [
            r'\b(?:danger|hazard|toxic|harmful|lethal)\b',
            r'\b(?:warning|caution|avoid|do\s+not)\b'
        ]
        
        for pattern in safety_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            sensitive_content['safety_concerns'].extend(matches)
        
        return sensitive_content

def validate_knowledge_input(knowledge_text: str, domain: str, min_length: int = 50) -> Tuple[bool, str]:
    """
    Validate knowledge input before processing.
    
    Args:
        knowledge_text: The knowledge text to validate
        domain: The target domain
        min_length: Minimum required length for the text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not knowledge_text or not knowledge_text.strip():
        return False, "Knowledge text cannot be empty."
    
    if len(knowledge_text.strip()) < min_length:
        return False, f"Knowledge text must be at least {min_length} characters long."
    
    if domain not in KnowledgeProcessor.DOMAIN_KEYWORDS:
        supported_domains = ', '.join(KnowledgeProcessor.DOMAIN_KEYWORDS.keys())
        return False, f"Unsupported domain. Supported domains: {supported_domains}"
    
    # Check for obviously inappropriate content
    inappropriate_patterns = [
        r'\b(?:hack|crack|exploit|bypass)\s+(?:system|security|password)\b',
        r'\b(?:illegal|unlawful|criminal)\s+(?:activity|action|behavior)\b'
    ]
    
    text_lower = knowledge_text.lower()
    for pattern in inappropriate_patterns:
        if re.search(pattern, text_lower):
            return False, "Content appears to contain inappropriate material for educational use."
    
    return True, ""

def get_domain_statistics(knowledge_text: str, domain: str) -> Dict:
    """
    Get detailed statistics about the knowledge text.
    
    Args:
        knowledge_text: The knowledge text to analyze
        domain: The target domain
        
    Returns:
        Dictionary containing various statistics
    """
    processor = KnowledgeProcessor()
    
    stats = {
        'word_count': len(knowledge_text.split()),
        'character_count': len(knowledge_text),
        'sentence_count': len(re.findall(r'[.!?]+', knowledge_text)),
        'domain_relevance': processor._calculate_domain_relevance(knowledge_text, domain),
        'risk_level': processor._assess_risk_level(knowledge_text),
        'key_concepts': processor.extract_key_concepts(knowledge_text, domain),
        'sensitive_content': processor.identify_sensitive_content(knowledge_text)
    }
    
    return stats

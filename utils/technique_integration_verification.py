"""
Research Technique Integration Verification
Verify that extracted techniques are actually being used in prompt generation
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class TechniqueIntegrationVerifier:
    """Verify actual integration of research techniques in prompt generation"""
    
    def __init__(self):
        self.integration_log = []
        
    def verify_technique_usage(self, knowledge_text: str, domain: str, objective: str) -> Dict[str, Any]:
        """Verify that research techniques are actually being retrieved and used"""
        
        verification_result = {
            'timestamp': datetime.now().isoformat(),
            'verification_status': 'checking',
            'techniques_in_database': 0,
            'techniques_retrieved': 0,
            'techniques_used_in_prompt': 0,
            'integration_authentic': False,
            'details': {}
        }
        
        try:
            # Step 1: Check database for available techniques
            from models import ExtractedTechnique
            available_techniques = ExtractedTechnique.query.filter_by(is_active=True).all()
            verification_result['techniques_in_database'] = len(available_techniques)
            
            # Step 2: Simulate RAG retrieval to see what gets retrieved
            retrieved_techniques = self._simulate_rag_retrieval(objective, domain, available_techniques)
            verification_result['techniques_retrieved'] = len(retrieved_techniques)
            
            # Step 3: Generate prompt and check if techniques are actually used
            from utils.rag_enhanced_gemini import generate_rag_enhanced_prompt
            
            # Generate prompt with verification tracking
            prompt_result = generate_rag_enhanced_prompt(knowledge_text, domain, objective)
            
            # Step 4: Analyze if techniques were actually integrated
            integration_analysis = self._analyze_technique_integration(
                prompt_result, retrieved_techniques, objective
            )
            
            verification_result.update(integration_analysis)
            verification_result['verification_status'] = 'completed'
            
            # Log the verification
            self.integration_log.append(verification_result)
            
            return verification_result
            
        except Exception as e:
            logger.error(f"Technique integration verification failed: {e}")
            verification_result['verification_status'] = 'failed'
            verification_result['error'] = str(e)
            return verification_result
    
    def _simulate_rag_retrieval(self, objective: str, domain: str, available_techniques: List) -> List[Dict]:
        """Simulate RAG retrieval to see what techniques would be retrieved"""
        
        # Create retrieval query
        query_words = set((objective + " " + domain).lower().split())
        
        retrieved = []
        for technique in available_techniques:
            # Score technique relevance
            technique_words = set((technique.technique_name + " " + technique.technique_description).lower().split())
            overlap = len(query_words.intersection(technique_words))
            
            if overlap > 0:  # Any relevance
                retrieved.append({
                    'id': technique.id,
                    'name': technique.technique_name,
                    'description': technique.technique_description,
                    'type': technique.technique_type,
                    'relevance_score': overlap / len(query_words.union(technique_words))
                })
        
        # Sort by relevance and return top 5
        retrieved.sort(key=lambda x: x['relevance_score'], reverse=True)
        return retrieved[:5]
    
    def _analyze_technique_integration(self, prompt_result: Dict, retrieved_techniques: List, objective: str) -> Dict[str, Any]:
        """Analyze if techniques were actually integrated into the generated prompt"""
        
        analysis = {
            'integration_authentic': False,
            'techniques_used_in_prompt': 0,
            'integration_evidence': [],
            'missing_integrations': [],
            'prompt_quality_score': 0.0
        }
        
        generated_prompt = prompt_result.get('enhanced_prompt', '')
        
        # Check if retrieved techniques appear in the generated prompt
        techniques_found = 0
        for technique in retrieved_techniques:
            technique_name_words = technique['name'].lower().split()[:3]  # First 3 words
            
            # Check if technique concepts appear in prompt
            found_evidence = []
            for word in technique_name_words:
                if len(word) > 3 and word in generated_prompt.lower():
                    found_evidence.append(word)
            
            if found_evidence:
                techniques_found += 1
                analysis['integration_evidence'].append({
                    'technique_id': technique['id'],
                    'technique_name': technique['name'][:50],
                    'evidence_words': found_evidence,
                    'relevance_score': technique['relevance_score']
                })
            else:
                analysis['missing_integrations'].append({
                    'technique_id': technique['id'],
                    'technique_name': technique['name'][:50],
                    'reason': 'No evidence in generated prompt'
                })
        
        analysis['techniques_used_in_prompt'] = techniques_found
        
        # Determine if integration is authentic
        if techniques_found > 0 and len(retrieved_techniques) > 0:
            usage_rate = techniques_found / len(retrieved_techniques)
            analysis['integration_authentic'] = usage_rate > 0.3  # At least 30% usage
            analysis['prompt_quality_score'] = usage_rate
        
        # Additional checks for authentic integration
        rag_indicators = ['retrieved', 'research', 'technique', 'framework', 'methodology']
        rag_evidence = sum(1 for indicator in rag_indicators if indicator in generated_prompt.lower())
        
        analysis['rag_system_active'] = rag_evidence > 2
        analysis['system_architecture'] = prompt_result.get('implementation_architecture', 'unknown')
        
        return analysis
    
    def get_integration_summary(self) -> Dict[str, Any]:
        """Get summary of all integration verifications"""
        
        if not self.integration_log:
            return {'status': 'no_verifications_performed'}
        
        latest = self.integration_log[-1]
        
        summary = {
            'latest_verification': latest['timestamp'],
            'database_techniques': latest['techniques_in_database'],
            'retrieval_working': latest['techniques_retrieved'] > 0,
            'integration_authentic': latest['integration_authentic'],
            'usage_rate': latest['techniques_used_in_prompt'] / max(latest['techniques_retrieved'], 1),
            'system_status': self._determine_system_status(latest)
        }
        
        return summary
    
    def _determine_system_status(self, verification: Dict) -> str:
        """Determine overall system status"""
        
        if verification['verification_status'] == 'failed':
            return 'system_error'
        
        if verification['techniques_in_database'] == 0:
            return 'no_techniques_available'
        
        if verification['techniques_retrieved'] == 0:
            return 'retrieval_not_working'
        
        if not verification['integration_authentic']:
            return 'integration_not_authentic'
        
        return 'fully_integrated'

# Global verifier instance
technique_verifier = TechniqueIntegrationVerifier()

def verify_research_integration(knowledge_text: str, domain: str, objective: str) -> Dict[str, Any]:
    """Main function to verify research technique integration"""
    return technique_verifier.verify_technique_usage(knowledge_text, domain, objective)
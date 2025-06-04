"""
Enhanced Semantic Retrieval for Authentic Research Technique Integration
Ensures extracted research techniques are actually retrieved and used in prompt generation
"""

import re
import logging
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

class SemanticTechniqueRetriever:
    """Enhanced retrieval system ensuring authentic research technique integration"""
    
    def __init__(self):
        self.technique_index = {}
        self.concept_mappings = self._build_concept_mappings()
        self.technique_cache = {}
        
    def _build_concept_mappings(self) -> Dict[str, List[str]]:
        """Build comprehensive concept mappings for semantic retrieval"""
        return {
            'adversarial': ['attack', 'adversarial', 'exploit', 'vulnerability', 'manipulation', 'perturbation'],
            'transformer': ['transformer', 'attention', 'bert', 'gpt', 'llm', 'language model'],
            'optimization': ['optimization', 'gradient', 'backprop', 'descent', 'loss', 'training'],
            'robustness': ['robustness', 'defense', 'security', 'protection', 'resilience', 'safety'],
            'jailbreak': ['jailbreak', 'bypass', 'circumvent', 'override', 'escape', 'break'],
            'prompt': ['prompt', 'instruction', 'query', 'input', 'text', 'generation'],
            'multimodal': ['multimodal', 'vision', 'image', 'visual', 'cross-modal', 'vlm'],
            'transfer': ['transfer', 'transferability', 'generalization', 'cross-domain', 'portable'],
            'evaluation': ['evaluation', 'assessment', 'measurement', 'metric', 'benchmark', 'test']
        }
    
    def index_research_techniques(self, techniques: List[Any]) -> None:
        """Index research techniques for enhanced semantic retrieval"""
        
        for technique in techniques:
            technique_id = technique.id
            
            # Extract semantic features
            semantic_profile = self._extract_semantic_profile(
                technique.technique_name, 
                technique.technique_description,
                technique.technique_type
            )
            
            self.technique_index[technique_id] = {
                'technique': technique,
                'semantic_profile': semantic_profile,
                'keywords': self._extract_keywords(technique.technique_name + " " + technique.technique_description),
                'technique_type': technique.technique_type,
                'complexity': technique.complexity_level,
                'effectiveness': technique.effectiveness_estimate or 0.7
            }
        
        logger.info(f"Indexed {len(techniques)} research techniques for semantic retrieval")
    
    def retrieve_relevant_techniques(self, objective: str, domain: str, 
                                   knowledge_text: str, top_k: int = 15) -> List[Dict[str, Any]]:
        """Retrieve techniques using enhanced semantic matching"""
        
        # Create comprehensive query profile
        query_profile = self._extract_semantic_profile(objective, knowledge_text, domain)
        
        # Score all techniques
        technique_scores = []
        for technique_id, indexed_data in self.technique_index.items():
            
            # Multi-factor scoring
            semantic_score = self._calculate_semantic_similarity(
                query_profile, indexed_data['semantic_profile']
            )
            
            keyword_score = self._calculate_keyword_overlap(
                objective + " " + knowledge_text, indexed_data['keywords']
            )
            
            domain_score = self._calculate_domain_relevance(
                domain, indexed_data['technique_type']
            )
            
            # Weighted final score
            final_score = (
                semantic_score * 0.5 + 
                keyword_score * 0.3 + 
                domain_score * 0.2
            )
            
            technique_scores.append({
                'technique_id': technique_id,
                'technique': indexed_data['technique'],
                'final_score': final_score,
                'semantic_score': semantic_score,
                'keyword_score': keyword_score,
                'domain_score': domain_score,
                'breakdown': {
                    'semantic': semantic_score,
                    'keyword': keyword_score,
                    'domain': domain_score
                }
            })
        
        # Sort and return top techniques
        technique_scores.sort(key=lambda x: x['final_score'], reverse=True)
        
        # Apply multi-tier filtering for comprehensive technique integration
        relevant_techniques = []
        
        # Tier 1: High relevance techniques (score > 0.4)
        high_relevance = [t for t in technique_scores if t['final_score'] > 0.4]
        relevant_techniques.extend(high_relevance[:8])
        
        # Tier 2: Medium relevance techniques (0.2 < score <= 0.4)
        medium_relevance = [t for t in technique_scores if 0.2 < t['final_score'] <= 0.4]
        relevant_techniques.extend(medium_relevance[:4])
        
        # Tier 3: Ensure diverse technique types are represented
        remaining_slots = top_k - len(relevant_techniques)
        if remaining_slots > 0:
            # Group remaining techniques by type
            attack_techniques = [t for t in technique_scores if t['technique'].technique_type == 'attack' and t not in relevant_techniques]
            defense_techniques = [t for t in technique_scores if t['technique'].technique_type == 'defense' and t not in relevant_techniques]
            evaluation_techniques = [t for t in technique_scores if t['technique'].technique_type == 'evaluation' and t not in relevant_techniques]
            
            # Add diverse techniques to ensure comprehensive coverage
            diverse_techniques = []
            for technique_list in [attack_techniques, defense_techniques, evaluation_techniques]:
                if technique_list and len(diverse_techniques) < remaining_slots:
                    diverse_techniques.extend(technique_list[:2])
            
            relevant_techniques.extend(diverse_techniques[:remaining_slots])
        
        return relevant_techniques[:top_k]
    
    def _extract_semantic_profile(self, name: str, description: str, context: str) -> Dict[str, float]:
        """Extract semantic profile from technique text"""
        
        combined_text = (name + " " + description + " " + context).lower()
        profile = defaultdict(float)
        
        # Score presence of concept categories
        for concept, keywords in self.concept_mappings.items():
            concept_score = 0
            for keyword in keywords:
                if keyword in combined_text:
                    # Weight by keyword importance and frequency
                    frequency = combined_text.count(keyword)
                    importance = 1.0 if keyword == concept else 0.7  # Exact match gets higher weight
                    concept_score += frequency * importance
            
            # Normalize by concept category size
            profile[concept] = min(concept_score / len(keywords), 1.0)
        
        return dict(profile)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from technique text"""
        
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Filter out common words
        stopwords = {'that', 'this', 'with', 'from', 'they', 'have', 'been', 'were', 'will', 'would', 'could', 'should'}
        keywords = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Return unique keywords, prioritizing longer ones
        unique_keywords = list(set(keywords))
        unique_keywords.sort(key=len, reverse=True)
        
        return unique_keywords[:15]  # Top 15 keywords
    
    def _calculate_semantic_similarity(self, profile1: Dict[str, float], 
                                     profile2: Dict[str, float]) -> float:
        """Calculate semantic similarity between profiles"""
        
        # Get all concepts
        all_concepts = set(profile1.keys()) | set(profile2.keys())
        
        if not all_concepts:
            return 0.0
        
        # Calculate cosine similarity
        dot_product = sum(profile1.get(c, 0) * profile2.get(c, 0) for c in all_concepts)
        
        norm1 = sum(v**2 for v in profile1.values()) ** 0.5
        norm2 = sum(v**2 for v in profile2.values()) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _calculate_keyword_overlap(self, query_text: str, technique_keywords: List[str]) -> float:
        """Calculate keyword overlap score"""
        
        query_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', query_text.lower()))
        
        if not query_words or not technique_keywords:
            return 0.0
        
        # Count overlapping keywords
        overlap = sum(1 for keyword in technique_keywords if keyword in query_words)
        
        # Normalize by smaller set size for better scoring
        return overlap / min(len(query_words), len(technique_keywords))
    
    def _calculate_domain_relevance(self, domain: str, technique_type: str) -> float:
        """Calculate domain relevance score"""
        
        domain_mappings = {
            'ai safety': ['attack', 'defense', 'evaluation'],
            'machine learning': ['attack', 'defense', 'optimization'],
            'nlp': ['attack', 'defense', 'evaluation'],
            'computer vision': ['attack', 'defense', 'multimodal'],
            'cybersecurity': ['attack', 'defense', 'evaluation']
        }
        
        domain_lower = domain.lower()
        for domain_key, relevant_types in domain_mappings.items():
            if domain_key in domain_lower:
                return 1.0 if technique_type in relevant_types else 0.5
        
        # Default moderate relevance
        return 0.6

class AuthenticIntegrationEngine:
    """Engine ensuring authentic integration of retrieved techniques into prompts"""
    
    def __init__(self):
        self.retriever = SemanticTechniqueRetriever()
        self.integration_log = []
        
    def initialize_with_database_techniques(self):
        """Initialize retriever with techniques from database"""
        try:
            from models import ExtractedTechnique
            techniques = ExtractedTechnique.query.filter_by(is_active=True).all()
            self.retriever.index_research_techniques(techniques)
            logger.info(f"Initialized authentic integration engine with {len(techniques)} techniques")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize with database techniques: {e}")
            return False
    
    def generate_technique_enhanced_prompt(self, objective: str, domain: str, 
                                         knowledge_text: str) -> Dict[str, Any]:
        """Generate prompt with authentic research technique integration"""
        
        # Retrieve relevant techniques with expanded coverage
        relevant_techniques = self.retriever.retrieve_relevant_techniques(
            objective, domain, knowledge_text, top_k=12
        )
        
        # Build authentic integration context
        integration_context = self._build_authentic_context(
            relevant_techniques, objective, domain, knowledge_text
        )
        
        # Generate enhanced prompt
        enhanced_prompt = self._generate_prompt_with_techniques(
            integration_context, objective, domain, knowledge_text
        )
        
        # Track integration for verification
        integration_record = {
            'timestamp': str(int(time.time() * 1000)),
            'techniques_retrieved': len(relevant_techniques),
            'techniques_integrated': len([t for t in relevant_techniques if t['final_score'] > 0.3]),
            'top_techniques': [
                {
                    'name': t['technique'].technique_name[:60],
                    'score': t['final_score'],
                    'type': t['technique'].technique_type
                }
                for t in relevant_techniques[:3]
            ]
        }
        
        self.integration_log.append(integration_record)
        
        return {
            'enhanced_prompt': enhanced_prompt,
            'technique_integration': integration_record,
            'relevant_techniques': relevant_techniques,
            'integration_authentic': len(relevant_techniques) > 0,
            'strategy_used': 'Enhanced-Semantic-RAG'
        }
    
    def _build_authentic_context(self, techniques: List[Dict], objective: str, 
                               domain: str, knowledge_text: str) -> str:
        """Build comprehensive authentic research context from all retrieved techniques"""
        
        if not techniques:
            return "No specific research techniques retrieved for this objective."
        
        # Group techniques by type and effectiveness
        technique_groups = defaultdict(list)
        for tech in techniques:
            technique_groups[tech['technique'].technique_type].append(tech)
        
        context_parts = []
        context_parts.append("**COMPREHENSIVE RESEARCH TECHNIQUE INTEGRATION:**")
        
        # Format all techniques by category with detailed descriptions
        for tech_type, tech_list in technique_groups.items():
            if not tech_list:
                continue
                
            context_parts.append(f"\n**{tech_type.upper()} METHODOLOGIES:**")
            
            for i, tech_data in enumerate(tech_list, 1):
                technique = tech_data['technique']
                score = tech_data['final_score']
                effectiveness = technique.effectiveness_estimate or 0.7
                complexity = technique.complexity_level or 'medium'
                
                # Include full technique details for comprehensive integration
                context_parts.append(
                    f"{i}. **{technique.technique_name}** (Relevance: {score:.3f}, Effectiveness: {effectiveness:.2f}, Complexity: {complexity})\n"
                    f"   Description: {technique.technique_description}\n"
                    f"   Application: Direct integration into {objective} within {domain} context\n"
                    f"   Priority: {technique.implementation_priority or 'standard'}"
                )
        
        # Add comprehensive integration metrics
        total_techniques = len(techniques)
        high_relevance = len([t for t in techniques if t['final_score'] > 0.4])
        medium_relevance = len([t for t in techniques if 0.2 < t['final_score'] <= 0.4])
        attack_count = len([t for t in techniques if t['technique'].technique_type == 'attack'])
        defense_count = len([t for t in techniques if t['technique'].technique_type == 'defense'])
        evaluation_count = len([t for t in techniques if t['technique'].technique_type == 'evaluation'])
        
        context_parts.append(f"\n**COMPREHENSIVE INTEGRATION METRICS:**")
        context_parts.append(f"Total techniques integrated: {total_techniques}")
        context_parts.append(f"High-relevance techniques: {high_relevance}")
        context_parts.append(f"Medium-relevance techniques: {medium_relevance}")
        context_parts.append(f"Attack techniques: {attack_count}")
        context_parts.append(f"Defense techniques: {defense_count}")
        context_parts.append(f"Evaluation techniques: {evaluation_count}")
        context_parts.append(f"Coverage from {len(set(t['technique'].research_paper_id for t in techniques))} research papers")
        
        # Add specific technique application strategy
        context_parts.append(f"\n**TECHNIQUE APPLICATION STRATEGY:**")
        context_parts.append(f"All {total_techniques} techniques are semantically matched and ready for integration")
        context_parts.append(f"Implementation follows research-validated methodologies")
        context_parts.append(f"Multi-tier approach ensures comprehensive coverage of {domain} requirements")
        
        return "\n".join(context_parts)
    
    def _generate_prompt_with_techniques(self, context: str, objective: str, 
                                       domain: str, knowledge_text: str) -> str:
        """Generate objective-driven prompt incorporating authentic research techniques"""
        
        # Extract actionable components from objective
        objective_components = self._parse_objective_components(objective)
        
        # Create objective-specific action plan
        action_plan = self._create_objective_action_plan(objective_components, context, domain)
        
        return f"""**OBJECTIVE-DRIVEN RESEARCH FRAMEWORK**

**CORE OBJECTIVE:** {objective}

**OBJECTIVE BREAKDOWN:**
{self._format_objective_breakdown(objective_components)}

**RESEARCH-BACKED ACTION PLAN:**
{action_plan}

**DOMAIN-SPECIFIC KNOWLEDGE INTEGRATION:**
{knowledge_text}

**AUTHENTIC TECHNIQUE APPLICATION:**
{context}

**STEP-BY-STEP OBJECTIVE ACHIEVEMENT:**
{self._generate_step_by_step_plan(objective, domain, context)}

**SUCCESS METRICS FOR OBJECTIVE:**
- Direct alignment with stated goal: {objective}
- Measurable progress indicators specific to {domain}
- Research-validated methodology implementation
- Quantifiable outcomes matching objective requirements

**IMMEDIATE ACTION ITEMS:**
{self._generate_immediate_actions(objective, domain)}

**OBJECTIVE VALIDATION:**
This framework is specifically designed to achieve: "{objective}" through systematic application of research techniques and domain expertise."""
    
    def _parse_objective_components(self, objective: str) -> Dict[str, str]:
        """Parse objective into actionable components"""
        objective_lower = objective.lower()
        
        components = {
            'action_verb': 'unknown',
            'target_subject': 'unknown',
            'scope': 'general',
            'outcome_type': 'analysis'
        }
        
        # Identify action verb
        action_verbs = ['analyze', 'design', 'develop', 'implement', 'evaluate', 'optimize', 'create', 'investigate']
        for verb in action_verbs:
            if verb in objective_lower:
                components['action_verb'] = verb
                break
        
        # Identify target subject
        if 'model' in objective_lower or 'llm' in objective_lower:
            components['target_subject'] = 'language models'
        elif 'attack' in objective_lower:
            components['target_subject'] = 'adversarial attacks'
        elif 'vulnerability' in objective_lower:
            components['target_subject'] = 'security vulnerabilities'
        elif 'prompt' in objective_lower:
            components['target_subject'] = 'prompt engineering'
        
        # Determine scope
        if 'pattern' in objective_lower:
            components['scope'] = 'pattern analysis'
        elif 'strategy' in objective_lower:
            components['scope'] = 'strategic planning'
        elif 'framework' in objective_lower:
            components['scope'] = 'framework development'
        
        return components
    
    def _format_objective_breakdown(self, components: Dict[str, str]) -> str:
        """Format objective components for clear understanding"""
        return f"""- Primary Action: {components['action_verb'].title()}
- Target Subject: {components['target_subject'].title()}
- Analysis Scope: {components['scope'].title()}
- Expected Outcome: {components['outcome_type'].title()}"""
    
    def _create_objective_action_plan(self, components: Dict[str, str], context: str, domain: str) -> str:
        """Create specific action plan based on objective components"""
        
        action_verb = components['action_verb']
        target_subject = components['target_subject']
        
        if action_verb == 'analyze':
            return f"""1. **Data Collection**: Gather comprehensive information about {target_subject}
2. **Pattern Identification**: Apply research techniques to identify key patterns
3. **Systematic Evaluation**: Use {domain} methodologies for thorough analysis
4. **Findings Synthesis**: Combine results into actionable insights
5. **Validation**: Verify findings against established research standards"""
        
        elif action_verb == 'design' or action_verb == 'develop':
            return f"""1. **Requirements Definition**: Specify exact needs for {target_subject}
2. **Research Integration**: Apply relevant techniques from knowledge base
3. **Architecture Planning**: Design systematic approach using {domain} principles
4. **Implementation Strategy**: Create step-by-step development plan
5. **Testing Framework**: Establish validation and verification methods"""
        
        elif action_verb == 'evaluate':
            return f"""1. **Evaluation Criteria**: Define specific metrics for {target_subject}
2. **Baseline Establishment**: Set comparative standards
3. **Systematic Testing**: Apply research techniques for comprehensive evaluation
4. **Results Analysis**: Interpret findings within {domain} context
5. **Recommendations**: Provide actionable next steps based on evaluation"""
        
        else:
            return f"""1. **Objective Clarification**: Define specific goals for {target_subject}
2. **Method Selection**: Choose appropriate research techniques
3. **Systematic Execution**: Implement chosen approaches
4. **Progress Monitoring**: Track advancement toward objective
5. **Outcome Documentation**: Record results and lessons learned"""
    
    def _generate_step_by_step_plan(self, objective: str, domain: str, context: str) -> str:
        """Generate detailed step-by-step plan for objective achievement"""
        
        return f"""**Phase 1: Preparation**
- Review objective requirements: {objective}
- Analyze available research techniques and domain knowledge
- Establish success criteria and measurement methods

**Phase 2: Implementation**
- Apply selected research techniques systematically
- Monitor progress against objective milestones
- Adjust approach based on intermediate results

**Phase 3: Validation**
- Verify outcomes align with stated objective
- Cross-reference results with {domain} standards
- Document achievement of objective requirements"""
    
    def _generate_immediate_actions(self, objective: str, domain: str) -> str:
        """Generate immediate actionable steps"""
        
        objective_lower = objective.lower()
        
        if 'analyze' in objective_lower:
            return f"""1. Begin systematic data collection relevant to: {objective}
2. Apply pattern recognition techniques from research database
3. Document initial findings for {domain} context
4. Prepare analysis framework for comprehensive evaluation"""
        
        elif 'design' in objective_lower or 'develop' in objective_lower:
            return f"""1. Define specific requirements for: {objective}
2. Select appropriate research methodologies
3. Create implementation timeline for {domain}
4. Establish validation criteria for success measurement"""
        
        else:
            return f"""1. Clarify specific success criteria for: {objective}
2. Identify relevant research techniques and domain expertise
3. Create systematic approach for {domain} implementation
4. Begin initial execution phase with progress tracking"""

# Global engine instance
import time
authentic_engine = AuthenticIntegrationEngine()

def initialize_authentic_integration():
    """Initialize the authentic integration system"""
    return authentic_engine.initialize_with_database_techniques()

def generate_research_enhanced_prompt(objective: str, domain: str, knowledge_text: str) -> Dict[str, Any]:
    """Main function for research-enhanced prompt generation"""
    return authentic_engine.generate_technique_enhanced_prompt(objective, domain, knowledge_text)
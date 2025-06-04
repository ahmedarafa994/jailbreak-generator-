"""
Advanced AI-Powered Prompt Generator Framework
Implementing the comprehensive framework for objective-driven prompt generation
"""

import logging
import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class PromptingTechnique(Enum):
    """Available AI prompting techniques"""
    PERSONA = "persona"
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    OUTPUT_FORMATTING = "output_formatting"
    STEP_BY_STEP = "step_by_step"
    ROLE_PLAYING = "role_playing"

class OutputFormat(Enum):
    """Available output formats"""
    JSON = "json"
    MARKDOWN_TABLE = "markdown_table"
    BULLETED_LIST = "bulleted_list"
    STRUCTURED_TEXT = "structured_text"
    CSV = "csv"
    XML = "xml"

@dataclass
class PromptGenerationRequest:
    """Structure for prompt generation requests"""
    domain: str
    objective: str
    knowledge_text: str
    knowledge_files: Optional[List[str]] = None
    prompting_techniques: Optional[List[PromptingTechnique]] = None
    output_format: OutputFormat = OutputFormat.STRUCTURED_TEXT
    persona_details: str = ""
    few_shot_examples: Optional[List[str]] = None
    custom_instructions: str = ""

class AdvancedPromptGenerator:
    """Advanced AI-powered prompt generator using Google Gemini"""
    
    def __init__(self):
        self.initialized = False
        self.gemini_model = None
        
    def initialize_gemini(self) -> bool:
        """Initialize Google Gemini for prompt generation"""
        try:
            # Check if API key is available
            api_key = os.environ.get('GOOGLE_API_KEY')
            if not api_key:
                logger.warning("Google API key not found, using fallback generation")
                return False
            
            # Try to import and configure Gemini
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Test connection with simple prompt
                test_response = self.gemini_model.generate_content("Test")
                if test_response and test_response.text:
                    self.initialized = True
                    logger.info("Advanced prompt generator initialized successfully")
                    return True
                    
            except ImportError:
                logger.warning("Google Generative AI library not available, using fallback")
                return False
            except Exception as e:
                logger.warning(f"Gemini initialization failed: {e}, using fallback")
                return False
                
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini: {e}")
            return False
    
    def generate_advanced_prompt(self, request: PromptGenerationRequest) -> Dict[str, Any]:
        """Generate advanced prompt using the comprehensive framework"""
        
        if not self.initialized and not self.initialize_gemini():
            return self._generate_fallback_prompt(request)
        
        try:
            # Build comprehensive prompt generation request for Gemini
            gemini_request = self._build_gemini_generation_request(request)
            
            # Generate prompt with Gemini
            response = self.gemini_model.generate_content(gemini_request)
            
            if response and response.text:
                generated_prompt = response.text
                
                # Post-process and validate the generated prompt
                final_prompt = self._post_process_prompt(generated_prompt, request)
                
                return {
                    'success': True,
                    'generated_prompt': final_prompt,
                    'technique_count': len(request.prompting_techniques or []),
                    'domain': request.domain,
                    'objective': request.objective,
                    'method': 'gemini_advanced'
                }
            else:
                logger.warning("Gemini returned empty response")
                return self._generate_fallback_prompt(request)
                
        except Exception as e:
            logger.error(f"Advanced prompt generation failed: {e}")
            return self._generate_fallback_prompt(request)
    
    def _build_gemini_generation_request(self, request: PromptGenerationRequest) -> str:
        """Build sophisticated prompt generation request for Gemini"""
        
        techniques_description = self._describe_techniques(request.prompting_techniques or [])
        format_description = self._describe_output_format(request.output_format)
        
        return f"""You are an expert AI prompt engineer specializing in creating highly effective prompts that achieve specific objectives when applied to other Large Language Models.

**PROMPT GENERATION TASK:**
Create a complete, ready-to-use prompt that will guide another LLM to successfully achieve the following objective when the prompt is applied to it.

**USER SPECIFICATIONS:**
- Domain: {request.domain}
- Objective: {request.objective}
- Knowledge Context: {request.knowledge_text[:1000]}...
- Desired Output Format: {format_description}
- Prompting Techniques to Include: {techniques_description}
- Persona Details: {request.persona_details or 'Expert in the specified domain'}
- Custom Instructions: {request.custom_instructions or 'None specified'}

**PROMPT ENGINEERING REQUIREMENTS:**

1. **Establish Clear Persona**: Based on the domain "{request.domain}", create an appropriate expert persona that will guide the LLM's responses.

2. **Ground in Knowledge**: Integrate the provided knowledge context to ensure the LLM bases its response on authentic information rather than hallucination.

3. **Define Core Task**: Translate the objective "{request.objective}" into clear, actionable instructions for the target LLM.

4. **Incorporate Advanced Techniques**: Seamlessly integrate the specified prompting techniques: {', '.join([t.value for t in (request.prompting_techniques or [])])}

5. **Constrain Output Format**: Ensure the LLM produces results in the specified format: {request.output_format.value}

6. **Add Success Validation**: Include mechanisms for the LLM to validate its own success in achieving the objective.

**CRITICAL REQUIREMENTS:**
- Generate a COMPLETE prompt that can be copied and pasted directly into another LLM
- The prompt must be designed to reliably achieve: "{request.objective}"
- Include specific instructions, examples where relevant, and clear success criteria
- Make the prompt persuasive and clear to ensure compliance
- Integrate all specified techniques naturally and effectively

**OUTPUT SPECIFICATION:**
Provide only the final, complete prompt text that can be immediately used with other LLMs. Do not include explanations or meta-commentary - just the pure prompt that will achieve the objective."""

    def _describe_techniques(self, techniques: List[PromptingTechnique]) -> str:
        """Describe the selected prompting techniques"""
        if not techniques:
            return "Standard prompting approach"
        
        descriptions = {
            PromptingTechnique.PERSONA: "Assign specific expert role/persona",
            PromptingTechnique.FEW_SHOT: "Provide examples of desired output",
            PromptingTechnique.CHAIN_OF_THOUGHT: "Request step-by-step reasoning",
            PromptingTechnique.OUTPUT_FORMATTING: "Specify exact output structure",
            PromptingTechnique.STEP_BY_STEP: "Break task into sequential steps",
            PromptingTechnique.ROLE_PLAYING: "Use role-playing scenarios"
        }
        
        return ", ".join([descriptions.get(t, t.value) for t in techniques])
    
    def _describe_output_format(self, output_format: OutputFormat) -> str:
        """Describe the desired output format"""
        descriptions = {
            OutputFormat.JSON: "Structured JSON object with defined schema",
            OutputFormat.MARKDOWN_TABLE: "Well-formatted Markdown table",
            OutputFormat.BULLETED_LIST: "Organized bulleted list format",
            OutputFormat.STRUCTURED_TEXT: "Clearly structured text with headings",
            OutputFormat.CSV: "Comma-separated values format",
            OutputFormat.XML: "Well-formed XML structure"
        }
        
        return descriptions.get(output_format, "Structured text format")
    
    def _post_process_prompt(self, generated_prompt: str, request: PromptGenerationRequest) -> str:
        """Post-process and validate the generated prompt"""
        
        # Add objective validation section if not present
        if "objective" not in generated_prompt.lower():
            validation_section = f"""

**OBJECTIVE VALIDATION:**
Ensure your response directly achieves this objective: "{request.objective}"
Verify that all outputs contribute to completing this specific goal."""
            
            generated_prompt += validation_section
        
        # Add success criteria if not present
        if "success" not in generated_prompt.lower():
            success_section = f"""

**SUCCESS CRITERIA:**
Your response will be considered successful when it demonstrably achieves: "{request.objective}"
Include specific evidence that the objective has been completed."""
            
            generated_prompt += success_section
        
        return generated_prompt.strip()
    
    def _generate_fallback_prompt(self, request: PromptGenerationRequest) -> Dict[str, Any]:
        """Generate prompt using fallback method when Gemini is unavailable"""
        
        # Create persona based on domain
        persona = self._create_domain_persona(request.domain)
        
        # Build structured prompt using traditional approach
        prompt_parts = [
            f"You are {persona}.",
            "",
            f"Your objective is to {request.objective}",
            "",
            "Base your analysis exclusively on the following information:",
            f"{request.knowledge_text}",
            ""
        ]
        
        # Add technique-specific instructions
        if request.prompting_techniques:
            for technique in request.prompting_techniques:
                prompt_parts.extend(self._add_technique_instructions(technique))
        
        # Add output format requirements
        format_instruction = self._get_format_instruction(request.output_format)
        prompt_parts.append(format_instruction)
        
        # Add validation
        prompt_parts.extend([
            "",
            f"Ensure your response directly achieves: {request.objective}",
            "Provide specific evidence that the objective has been completed."
        ])
        
        fallback_prompt = "\n".join(prompt_parts)
        
        return {
            'success': True,
            'generated_prompt': fallback_prompt,
            'technique_count': len(request.prompting_techniques or []),
            'domain': request.domain,
            'objective': request.objective,
            'method': 'fallback_structured'
        }
    
    def _create_domain_persona(self, domain: str) -> str:
        """Create appropriate persona based on domain"""
        domain_personas = {
            'AI Safety Research': 'an expert AI safety researcher with deep knowledge of vulnerability assessment and defense mechanisms',
            'Machine Learning Security': 'a senior machine learning security specialist with expertise in adversarial attacks and model robustness',
            'Prompt Engineering': 'a master prompt engineer with extensive experience in LLM optimization and control',
            'Computer Vision Security': 'a computer vision security expert specializing in adversarial examples and visual attacks',
            'Natural Language Processing': 'an NLP researcher with deep expertise in language model analysis and manipulation'
        }
        
        return domain_personas.get(domain, f'an expert researcher in {domain}')
    
    def _add_technique_instructions(self, technique: PromptingTechnique) -> List[str]:
        """Add technique-specific instructions to prompt"""
        instructions = {
            PromptingTechnique.CHAIN_OF_THOUGHT: [
                "Think step-by-step and show your reasoning process.",
                "Break down your analysis into clear, logical steps."
            ],
            PromptingTechnique.STEP_BY_STEP: [
                "Approach this task systematically:",
                "1. First, analyze the provided information",
                "2. Then, identify key components relevant to the objective",
                "3. Finally, synthesize your findings to achieve the objective"
            ],
            PromptingTechnique.PERSONA: [
                "Apply your expertise and professional judgment to this task."
            ]
        }
        
        return instructions.get(technique, [])
    
    def _get_format_instruction(self, output_format: OutputFormat) -> str:
        """Get format-specific instruction"""
        instructions = {
            OutputFormat.JSON: "Format your response as a valid JSON object.",
            OutputFormat.MARKDOWN_TABLE: "Present your findings in a well-formatted Markdown table.",
            OutputFormat.BULLETED_LIST: "Organize your response as a clear bulleted list.",
            OutputFormat.STRUCTURED_TEXT: "Structure your response with clear headings and sections.",
            OutputFormat.CSV: "Format your output as comma-separated values.",
            OutputFormat.XML: "Structure your response as well-formed XML."
        }
        
        return instructions.get(output_format, "Present your response in a clear, structured format.")

# Global instance
advanced_generator = AdvancedPromptGenerator()

def generate_objective_achieving_prompt(domain: str, objective: str, knowledge_text: str, 
                                      techniques: List[str] = None, 
                                      output_format: str = "structured_text") -> Dict[str, Any]:
    """Generate prompt designed to achieve specific objective when applied to other LLMs"""
    
    # Convert string techniques to enum
    technique_enums = []
    if techniques:
        for tech in techniques:
            try:
                technique_enums.append(PromptingTechnique(tech.lower()))
            except ValueError:
                logger.warning(f"Unknown technique: {tech}")
    
    # Convert output format to enum
    try:
        format_enum = OutputFormat(output_format.lower())
    except ValueError:
        format_enum = OutputFormat.STRUCTURED_TEXT
    
    # Create request object
    request = PromptGenerationRequest(
        domain=domain,
        objective=objective,
        knowledge_text=knowledge_text,
        prompting_techniques=technique_enums,
        output_format=format_enum
    )
    
    # Generate advanced prompt
    return advanced_generator.generate_advanced_prompt(request)
#!/usr/bin/env python3
"""
Direct verification of research technique integration in prompt generation.
This script should be run from the root directory of the Flask application.
"""

import sys
import os
# Ensure the application root is in the Python path
# This allows importing modules like 'app' and 'models'
# Assumes the script is in the root or a subdirectory, and '.' refers to the project root when run from there.
# If running from a subdirectory like 'scripts/', you might need sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('.')


from app import app, db
from models import ExtractedTechnique
# It's assumed that generate_rag_enhanced_prompt is correctly located and handles its own dependencies.
from utils.rag_enhanced_gemini import generate_rag_enhanced_prompt

def verify_integration():
    """Verify if research techniques are actually integrated into prompt generation."""

    # Use the Flask application context to allow database operations
    with app.app_context():
        print("=== RESEARCH TECHNIQUE INTEGRATION VERIFICATION ===\n")

        # Check the database for active research techniques
        active_techniques = ExtractedTechnique.query.filter_by(is_active=True).all()
        print(f"Database contains {len(active_techniques)} active research techniques.")

        if active_techniques:
            print(f"Sample technique (first active): {active_techniques[0].technique_name[:80]}...")
        else:
            print("No active research techniques found in the database. Prompt generation might use fallbacks.")

        # Define test inputs for prompt generation
        print("\n=== TESTING PROMPT GENERATION ===")
        test_knowledge = "Advanced transformer models show vulnerabilities to adversarial attacks through gradient-based optimization and require robust defense mechanisms."
        # Ensure this domain is one that `generate_rag_enhanced_prompt` is designed to handle,
        # ideally from the SUPPORTED_DOMAINS list in your main application if applicable.
        test_domain = "AI Safety Research"
        test_objective = "Analyze novel attack patterns in large language models and propose mitigation strategies."

        print(f"Input - Knowledge: {test_knowledge[:70]}...")
        print(f"Input - Domain: {test_domain}")
        print(f"Input - Objective: {test_objective}")

        # Generate the prompt using the RAG-enhanced function
        try:
            generation_result = generate_rag_enhanced_prompt(test_knowledge, test_domain, test_objective)
        except Exception as e:
            print(f"\nXXX ERROR during prompt generation: {e} XXX")
            print("Skipping further analysis due to generation error.")
            return

        print("\n=== GENERATION RESULT (from generate_rag_enhanced_prompt) ===")
        print(f"Strategy used: {generation_result.get('strategy_used', 'N/A')}")

        # Accessing nested rag_architecture safely
        rag_architecture_info = generation_result.get('rag_architecture', {})
        print(f"RAG architecture active (retrieval performed): {rag_architecture_info.get('retrieval_performed', False)}")
        print(f"Chunks retrieved by RAG: {rag_architecture_info.get('chunks_retrieved', 0)}")

        # Check if specific research techniques appear in the generated prompt
        generated_prompt_text = generation_result.get('enhanced_prompt', '')
        print(f"Generated prompt length: {len(generated_prompt_text)} characters")

        # Search for evidence of technique integration in the prompt
        # This is a heuristic check based on keywords from technique names
        techniques_with_evidence_count = 0
        technique_names_found_in_prompt = []

        # Limit the check to a sample of techniques to keep verification quick
        # (e.g., the first 10 active techniques or all if less than 10)
        techniques_to_check = active_techniques[:10]
        num_techniques_actually_checked = len(techniques_to_check)

        if num_techniques_actually_checked > 0:
            for technique in techniques_to_check:
                # Use a few keywords from the technique name for matching
                # Convert to lowercase for case-insensitive comparison
                technique_keywords = technique.technique_name.lower().split()[:3] # First 3 words
                found_this_technique = False
                for word in technique_keywords:
                    # Check for reasonably significant words (e.g., length > 4)
                    if len(word) > 4 and word in generated_prompt_text.lower():
                        techniques_with_evidence_count += 1
                        technique_names_found_in_prompt.append(technique.technique_name[:60]) # Store part of the name
                        found_this_technique = True
                        break # Found evidence for this technique, move to the next

        print(f"\n=== INTEGRATION ANALYSIS (based on keyword heuristic) ===")
        print(f"Number of techniques checked for keywords: {num_techniques_actually_checked}")
        print(f"Techniques with keyword evidence found in prompt: {techniques_with_evidence_count}")

        if num_techniques_actually_checked > 0:
            integration_rate = (techniques_with_evidence_count / num_techniques_actually_checked) * 100
            print(f"Heuristic integration rate: {integration_rate:.1f}%")
        else:
            print("Heuristic integration rate: N/A (no active techniques to check in sample)")

        if technique_names_found_in_prompt:
            print("Sample techniques with keywords found in prompt (heuristic):")
            for name in technique_names_found_in_prompt[:5]: # Show up to 5
                print(f"  - {name}...")

        # Check for general RAG system indicators in the prompt
        # These are generic words that might suggest RAG activity
        rag_indicator_keywords = ['retrieved context', 'research findings', 'according to technique', 'framework suggests', 'methodology based on']
        indicators_actually_found = [indicator for indicator in rag_indicator_keywords if indicator in generated_prompt_text.lower()]
        print(f"General RAG system indicator keywords found: {indicators_actually_found if indicators_actually_found else 'None'}")

        # Final assessment based on the heuristic
        print("\n=== FINAL ASSESSMENT (HEURISTIC) ===")
        if techniques_with_evidence_count > 0 or indicators_actually_found:
            print("✓ POTENTIAL AUTHENTIC INTEGRATION: Evidence suggests research techniques or RAG activity is influencing the prompt.")
        elif rag_architecture_info.get('retrieval_performed', False) and rag_architecture_info.get('chunks_retrieved', 0) > 0 :
             print("✓ RAG SYSTEM ACTIVE: The RAG system retrieved chunks, but specific technique keywords were not strongly detected in the heuristic check.")
        else:
            print("✗ LIMITED/NO INTEGRATION DETECTED: Heuristic check found little evidence of specific technique integration or strong RAG indicators in the prompt text. Prompt may be generic or integration is subtle.")

        print(f"\n=== GENERATED PROMPT SAMPLE (first 500 chars) ===")
        print(generated_prompt_text[:500] + ("..." if len(generated_prompt_text) > 500 else ""))

if __name__ == "__main__":
    verify_integration()

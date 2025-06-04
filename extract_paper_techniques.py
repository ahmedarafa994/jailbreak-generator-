"""
Extract and analyze specific techniques from the arXiv paper
"""

import trafilatura
import re
import json

def extract_paper_content():
    """Extract content from the specific arXiv paper"""
    url = "https://arxiv.org/html/2503.01781v1"
    
    try:
        downloaded = trafilatura.fetch_url(url)
        content = trafilatura.extract(downloaded)
        
        if content:
            return content
        else:
            print("Failed to extract content with trafilatura")
            return None
            
    except Exception as e:
        print(f"Error extracting paper: {e}")
        return None

def analyze_techniques(content):
    """Analyze the paper content to extract specific techniques"""
    
    if not content:
        return None
    
    # Extract key sections
    techniques = {
        'methodologies': [],
        'algorithms': [],
        'attack_strategies': [],
        'evaluation_metrics': [],
        'implementation_details': []
    }
    
    # Look for methodology sections
    method_patterns = [
        r'(?i)method(?:ology)?[:\s]+([^.]+\.)',
        r'(?i)approach[:\s]+([^.]+\.)',
        r'(?i)technique[:\s]+([^.]+\.)',
        r'(?i)algorithm[:\s]+([^.]+\.)'
    ]
    
    for pattern in method_patterns:
        matches = re.findall(pattern, content)
        techniques['methodologies'].extend(matches[:5])  # Limit to top 5
    
    # Look for specific attack strategies
    attack_patterns = [
        r'(?i)attack[:\s]+([^.]+\.)',
        r'(?i)jailbreak[:\s]+([^.]+\.)',
        r'(?i)adversarial[:\s]+([^.]+\.)',
        r'(?i)prompt[:\s]+injection[:\s]+([^.]+\.)'
    ]
    
    for pattern in attack_patterns:
        matches = re.findall(pattern, content)
        techniques['attack_strategies'].extend(matches[:5])
    
    # Look for evaluation metrics
    eval_patterns = [
        r'(?i)evaluat(?:e|ion)[:\s]+([^.]+\.)',
        r'(?i)metric[:\s]+([^.]+\.)',
        r'(?i)measure[:\s]+([^.]+\.)',
        r'(?i)score[:\s]+([^.]+\.)'
    ]
    
    for pattern in eval_patterns:
        matches = re.findall(pattern, content)
        techniques['evaluation_metrics'].extend(matches[:3])
    
    return techniques

if __name__ == "__main__":
    print("Extracting paper content...")
    content = extract_paper_content()
    
    if content:
        print(f"Content extracted: {len(content)} characters")
        
        print("\nAnalyzing techniques...")
        techniques = analyze_techniques(content)
        
        if techniques:
            print(json.dumps(techniques, indent=2))
            
            # Save to file for implementation
            with open('paper_techniques.json', 'w') as f:
                json.dump(techniques, f, indent=2)
            
            print("\nTechniques saved to paper_techniques.json")
        else:
            print("No techniques extracted")
    else:
        print("Failed to extract paper content")
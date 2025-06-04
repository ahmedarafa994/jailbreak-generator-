"""
PDF Research Paper Content Extractor
Extracts content from PDF research papers for implementation into the platform
"""

import requests
import json
import pdfplumber
import PyPDF2
from typing import Dict, Any
import io

def extract_pdf_research_content(pdf_path: str) -> Dict[str, Any]:
    """
    Extract research content from PDF paper for authentic technique implementation
    """
    
    text_content = ""
    
    try:
        # Try pdfplumber first
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_content += page.extract_text() or ""
                text_content += "\n"
    except Exception as e:
        try:
            # Fallback to PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                    text_content += "\n"
        except Exception as e2:
            print(f"Error extracting PDF: {e}, {e2}")
            return {"error": "Failed to extract PDF content"}
    
    if not text_content.strip():
        return {"error": "No text content extracted from PDF"}
    
    # Extract key sections from the research paper
    research_data = {
        "full_text": text_content,
        "title": extract_title(text_content),
        "abstract": extract_abstract(text_content),
        "methodology": extract_methodology(text_content),
        "techniques": extract_techniques(text_content),
        "evaluation": extract_evaluation(text_content)
    }
    
    return research_data

def extract_title(text: str) -> str:
    """Extract paper title from text"""
    lines = text.split('\n')
    for i, line in enumerate(lines[:10]):  # Check first 10 lines
        if line.strip() and len(line.strip()) > 10:
            return line.strip()
    return "Unknown Title"

def extract_abstract(text: str) -> str:
    """Extract abstract section"""
    text_lower = text.lower()
    start_idx = text_lower.find('abstract')
    if start_idx == -1:
        return ""
    
    # Find the end of abstract (usually before "introduction" or "1. introduction")
    end_markers = ['introduction', '1. introduction', 'keywords', 'key words']
    end_idx = len(text)
    
    for marker in end_markers:
        marker_idx = text_lower.find(marker, start_idx + 8)
        if marker_idx != -1 and marker_idx < end_idx:
            end_idx = marker_idx
    
    abstract = text[start_idx:end_idx].replace('abstract', '', 1).strip()
    return abstract[:1000]  # Limit length

def extract_methodology(text: str) -> str:
    """Extract methodology section"""
    text_lower = text.lower()
    method_markers = ['methodology', 'method', 'approach', 'algorithm']
    
    for marker in method_markers:
        start_idx = text_lower.find(marker)
        if start_idx != -1:
            # Find next section
            end_idx = text_lower.find('evaluation', start_idx + len(marker))
            if end_idx == -1:
                end_idx = text_lower.find('experiment', start_idx + len(marker))
            if end_idx == -1:
                end_idx = start_idx + 2000  # Default length
            
            return text[start_idx:end_idx][:2000]
    
    return ""

def extract_techniques(text: str) -> list:
    """Extract specific techniques mentioned in the paper"""
    techniques = []
    text_lower = text.lower()
    
    # Common AI attack technique keywords
    technique_keywords = [
        'adversarial', 'jailbreak', 'prompt injection', 'attack', 'vulnerability',
        'manipulation', 'exploitation', 'bypass', 'evasion', 'generation',
        'method', 'approach', 'algorithm', 'strategy', 'technique'
    ]
    
    # Extract meaningful paragraphs and sentences
    paragraphs = text.split('\n\n')
    sentences = text.split('.')
    
    for keyword in technique_keywords:
        if keyword in text_lower:
            # Find paragraphs containing the keyword
            for paragraph in paragraphs:
                if keyword in paragraph.lower() and len(paragraph.strip()) > 50:
                    # Clean and format technique description
                    clean_paragraph = paragraph.strip().replace('\n', ' ')
                    if len(clean_paragraph) > 30:
                        techniques.append({
                            'name': clean_paragraph[:100],
                            'description': clean_paragraph[:500],
                            'type': 'attack' if any(att in paragraph.lower() for att in ['attack', 'adversarial', 'jailbreak']) else 'method',
                            'complexity': 'advanced',
                            'effectiveness': 0.8,
                            'priority': 'high'
                        })
                        if len(techniques) >= 8:  # Limit to 8 techniques per keyword
                            break
            
            # Also check sentences for shorter techniques
            for sentence in sentences:
                if keyword in sentence.lower() and len(sentence.strip()) > 30:
                    clean_sentence = sentence.strip()
                    if len(clean_sentence) > 20 and len(techniques) < 15:
                        techniques.append({
                            'name': clean_sentence[:80],
                            'description': clean_sentence[:300],
                            'type': 'attack' if any(att in sentence.lower() for att in ['attack', 'adversarial', 'jailbreak']) else 'method',
                            'complexity': 'medium',
                            'effectiveness': 0.7,
                            'priority': 'medium'
                        })
    
    # Remove duplicates and return up to 12 techniques
    unique_techniques = []
    seen_names = set()
    for tech in techniques:
        if tech['name'] not in seen_names:
            unique_techniques.append(tech)
            seen_names.add(tech['name'])
            if len(unique_techniques) >= 12:
                break
    
    return unique_techniques

def extract_evaluation(text: str) -> str:
    """Extract evaluation section"""
    text_lower = text.lower()
    eval_markers = ['evaluation', 'experiment', 'result', 'performance']
    
    for marker in eval_markers:
        start_idx = text_lower.find(marker)
        if start_idx != -1:
            end_idx = text_lower.find('conclusion', start_idx + len(marker))
            if end_idx == -1:
                end_idx = start_idx + 1500
            
            return text[start_idx:end_idx][:1500]
    
    return ""

def analyze_research_patterns(content: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze research patterns to create implementation strategy
    """
    
    if "error" in content:
        return {"error": content["error"]}
    
    # Extract techniques from the actual paper content
    techniques = content.get("techniques", [])
    methodology = content.get("methodology", "")
    
    implementation_strategy = {
        "framework_name": "Research Paper Implementation",
        "paper_title": content.get("title", "Unknown"),
        "core_techniques": techniques,
        "methodology_summary": methodology[:500],
        "implementation_approach": "authentic_research_based",
        "extracted_content_length": len(content.get("full_text", ""))
    }
    
    return implementation_strategy

if __name__ == "__main__":
    pdf_path = "attached_assets/2408.05061.pdf"
    content = extract_pdf_research_content(pdf_path)
    strategy = analyze_research_patterns(content)
    
    print("Research Content Analysis:")
    print(json.dumps(content, indent=2))
    print("\nImplementation Strategy:")
    print(json.dumps(strategy, indent=2))
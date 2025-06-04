import trafilatura
import requests
from bs4 import BeautifulSoup

def extract_arxiv_paper_content(url: str) -> dict:
    """
    Extract content from arXiv paper for integration into the platform
    """
    try:
        # Fetch the paper content
        downloaded = trafilatura.fetch_url(url)
        text_content = trafilatura.extract(downloaded)
        
        if not text_content:
            # Fallback: try direct HTML parsing
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1', class_='title mathjax')
            title = title_elem.get_text().strip() if title_elem else "Unknown Title"
            
            # Extract abstract
            abstract_elem = soup.find('blockquote', class_='abstract mathjax')
            abstract = abstract_elem.get_text().strip() if abstract_elem else ""
            
            # Extract main content
            content_elem = soup.find('div', class_='ltx_page_main')
            content = content_elem.get_text() if content_elem else ""
            
            return {
                'title': title,
                'abstract': abstract,
                'content': content,
                'full_text': f"{title}\n\n{abstract}\n\n{content}"
            }
        else:
            return {
                'title': "Extracted Paper",
                'abstract': "",
                'content': text_content,
                'full_text': text_content
            }
            
    except Exception as e:
        print(f"Error extracting paper content: {e}")
        return {
            'title': 'Error',
            'abstract': '',
            'content': '',
            'full_text': ''
        }

if __name__ == "__main__":
    url = "https://www.arxiv.org/pdf/2409.14177"
    paper_data = extract_arxiv_paper_content(url)
    
    if paper_data:
        print("Paper Title:", paper_data['title'])
        print("\nAbstract:", paper_data['abstract'][:500] + "..." if len(paper_data['abstract']) > 500 else paper_data['abstract'])
        print("\nContent Length:", len(paper_data['content']))
    else:
        print("Failed to extract paper content")
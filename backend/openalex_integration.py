#!/usr/bin/env python3
"""
OpenAlex API Integration Script
Fetches real research papers from OpenAlex API and saves them to CSV format.
Based on: https://docs.openalex.org/download-all-data/openalex-snapshot
"""

import os
import json
import time
import requests
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenAlexClient:
    """Client for interacting with OpenAlex API"""
    
    def __init__(self, base_url: str = "https://api.openalex.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PatentSearch/1.0 (https://github.com/your-repo)',
            'Accept': 'application/json'
        })
    
    def search_works(self, 
                    query: str = None,
                    filter_params: Dict[str, str] = None,
                    per_page: int = 200,
                    max_results: int = 10000,
                    sort: str = "cited_by_count:desc") -> List[Dict[str, Any]]:
        """
        Search for works (research papers) using OpenAlex API
        
        Args:
            query: Search query string
            filter_params: Additional filters (e.g., {'type': 'journal-article'})
            per_page: Number of results per page (max 200)
            max_results: Maximum total results to fetch
            sort: Sort order (e.g., 'cited_by_count:desc', 'publication_date:desc')
        
        Returns:
            List of work objects
        """
        all_works = []
        page = 1
        cursor = None
        
        logger.info(f"Starting OpenAlex search with max_results={max_results}")
        
        while len(all_works) < max_results:
            # Build URL
            url = f"{self.base_url}/works"
            params = {
                'per-page': min(per_page, max_results - len(all_works)),
                'page': page,
                'sort': sort
            }
            
            # Add search query if provided
            if query:
                params['search'] = query
            
            # Add filters if provided
            if filter_params:
                for key, value in filter_params.items():
                    params[f'filter'] = f"{key}:{value}"
            
            try:
                logger.info(f"Fetching page {page} (cursor: {cursor})")
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                works = data.get('results', [])
                
                if not works:
                    logger.info("No more results found")
                    break
                
                all_works.extend(works)
                logger.info(f"Fetched {len(works)} works (total: {len(all_works)})")
                
                # Check if we have more pages
                if len(works) < per_page:
                    logger.info("Reached last page")
                    break
                
                page += 1
                
                # Rate limiting - be respectful to the API
                time.sleep(0.5)  # Increased delay to avoid rate limiting
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching page {page}: {e}")
                break
        
        logger.info(f"Total works fetched: {len(all_works)}")
        return all_works[:max_results]
    
    def get_work_details(self, work_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific work"""
        try:
            url = f"{self.base_url}/works/{work_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching work {work_id}: {e}")
            return None

def extract_paper_data(works: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract and clean paper data from OpenAlex works
    
    Args:
        works: List of work objects from OpenAlex API
        
    Returns:
        List of cleaned paper records
    """
    papers = []
    
    for work in works:
        try:
            # Extract basic information
            title = work.get('title', '') or ''
            abstract = work.get('abstract_inverted_index', {}) or {}
            
            # Convert abstract from inverted index to text
            abstract_text = ""
            if abstract:
                # Simple reconstruction from inverted index
                words = []
                for word, positions in abstract.items():
                    for pos in positions:
                        words.append((pos, word))
                words.sort()
                abstract_text = " ".join([word for pos, word in words])
            
            # Extract publication year
            publication_date = work.get('publication_date', '')
            year = None
            if publication_date:
                try:
                    year = int(publication_date.split('-')[0])
                except (ValueError, IndexError):
                    year = None
            
            # Extract authors
            authorships = work.get('authorships', [])
            author_names = []
            for authorship in authorships:
                author = authorship.get('author', {})
                if author:
                    display_name = author.get('display_name', '')
                    if display_name:
                        author_names.append(display_name)
            
            # Extract journal/source
            primary_location = work.get('primary_location', {})
            source = primary_location.get('source', {})
            journal_name = source.get('display_name', '') if source else ''
            
            # Extract concepts (topics)
            concepts = work.get('concepts', [])
            topics = []
            for concept in concepts[:5]:  # Top 5 concepts
                if concept.get('score', 0) > 0.3:  # Only high-confidence concepts
                    topics.append(concept.get('display_name', ''))
            
            # Extract citation count
            cited_by_count = work.get('cited_by_count', 0)
            
            # Create paper record
            paper = {
                'id': work.get('id', '').split('/')[-1],  # Extract ID from URL
                'title': title,
                'abstract': abstract_text,
                'year': year,
                'authors': '; '.join(author_names[:5]),  # First 5 authors
                'journal': journal_name,
                'topics': '; '.join(topics),
                'cited_by_count': cited_by_count,
                'doi': work.get('doi', ''),
                'url': work.get('id', ''),
                'source': 'openalex'
            }
            
            # Only include papers with abstracts and valid titles
            if (abstract_text and len(abstract_text.strip()) > 50 and 
                title and len(title.strip()) > 10):
                papers.append(paper)
                
        except Exception as e:
            logger.error(f"Error processing work: {e}")
            continue
    
    return papers

def fetch_research_papers(max_papers: int = 10000) -> pd.DataFrame:
    """
    Fetch research papers from OpenAlex API
    
    Args:
        max_papers: Maximum number of papers to fetch
        
    Returns:
        DataFrame with paper data
    """
    client = OpenAlexClient()
    
    # Search for papers with abstracts, sorted by citation count
    logger.info("Fetching research papers from OpenAlex...")
    
    # Search for papers in different domains
    search_queries = [
        "machine learning",
        "artificial intelligence", 
        "computer science",
        "engineering",
        "medicine",
        "biology",
        "physics",
        "chemistry",
        "mathematics",
        "data science"
    ]
    
    all_papers = []
    papers_per_query = max_papers // len(search_queries)
    
    for query in search_queries:
        logger.info(f"Searching for: {query}")
        
        # Filter for journal articles with abstracts
        filter_params = {
            'type': 'journal-article',
            'has_abstract': 'true'
        }
        
        works = client.search_works(
            query=query,
            filter_params=filter_params,
            per_page=200,
            max_results=papers_per_query,
            sort='cited_by_count:desc'
        )
        
        papers = extract_paper_data(works)
        all_papers.extend(papers)
        
        logger.info(f"Found {len(papers)} papers for query '{query}'")
        
        # Rate limiting between queries
        time.sleep(2)  # Increased delay between different search queries
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_papers = []
    for paper in all_papers:
        title = paper.get('title', '')
        if title and isinstance(title, str):
            title = title.lower().strip()
            if title not in seen_titles and title:
                seen_titles.add(title)
                unique_papers.append(paper)
    
    logger.info(f"Total unique papers: {len(unique_papers)}")
    
    # Convert to DataFrame
    df = pd.DataFrame(unique_papers)
    
    # Clean and validate data
    df = df.dropna(subset=['title', 'abstract'])
    df = df[df['abstract'].str.len() >= 50]  # Minimum abstract length
    df = df[df['year'].notna()]  # Must have publication year
    
    # Sort by citation count
    df = df.sort_values('cited_by_count', ascending=False)
    
    # Limit to requested number
    df = df.head(max_papers)
    
    logger.info(f"Final dataset: {len(df)} papers")
    return df

def main():
    """Main function to fetch and save OpenAlex data"""
    print("OpenAlex Research Papers Integration")
    print("=" * 50)
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    try:
        # Fetch papers
        papers_df = fetch_research_papers(max_papers=10000)
        
        if papers_df.empty:
            print("No papers found!")
            return
        
        # Save to CSV
        output_file = os.path.join(data_dir, "openalex_papers.csv")
        papers_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Successfully fetched {len(papers_df)} research papers")
        print(f"📁 Saved to: {output_file}")
        
        # Display sample data
        print("\n📊 Sample data:")
        print(f"Columns: {list(papers_df.columns)}")
        print(f"Date range: {papers_df['year'].min()} - {papers_df['year'].max()}")
        print(f"Average citations: {papers_df['cited_by_count'].mean():.1f}")
        
        # Show top papers
        print("\n🔝 Top 3 most cited papers:")
        top_papers = papers_df.head(3)
        for idx, row in top_papers.iterrows():
            print(f"  • {row['title'][:80]}... ({row['cited_by_count']} citations)")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

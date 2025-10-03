#!/usr/bin/env python3
"""
Real Data Integration Script
Combines OpenAlex research papers and PatentsView patents into a unified dataset.
This replaces the synthetic data with real data from official sources.
"""

import os
import pandas as pd
from typing import List, Dict, Any
import logging
from datetime import datetime

# Import our integration modules
from openalex_integration import fetch_research_papers
from patentsview_integration import fetch_patents

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def combine_datasets(papers_df: pd.DataFrame, patents_df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine research papers and patents into a unified dataset
    
    Args:
        papers_df: DataFrame with research papers
        patents_df: DataFrame with patents
        
    Returns:
        Combined DataFrame with standardized columns
    """
    logger.info("Combining datasets...")
    
    # Standardize column names for both datasets
    papers_standardized = papers_df.copy()
    papers_standardized['document_type'] = 'research_paper'
    papers_standardized['source_database'] = 'openalex'
    
    patents_standardized = patents_df.copy()
    patents_standardized['document_type'] = 'patent'
    patents_standardized['source_database'] = 'patentsview'
    
    # Ensure both datasets have the same core columns
    core_columns = ['id', 'title', 'abstract', 'year', 'document_type', 'source_database']
    
    # Add missing columns with default values
    for col in core_columns:
        if col not in papers_standardized.columns:
            papers_standardized[col] = ''
        if col not in patents_standardized.columns:
            patents_standardized[col] = ''
    
    # Select and reorder columns
    papers_final = papers_standardized[core_columns + 
        [col for col in papers_standardized.columns if col not in core_columns]]
    patents_final = patents_standardized[core_columns + 
        [col for col in patents_standardized.columns if col not in core_columns]]
    
    # Combine datasets
    combined_df = pd.concat([papers_final, patents_final], ignore_index=True)
    
    # Add metadata
    combined_df['integration_date'] = datetime.now().strftime('%Y-%m-%d')
    combined_df['data_source'] = 'real_data'
    
    logger.info(f"Combined dataset: {len(combined_df)} documents")
    logger.info(f"  - Research papers: {len(papers_final)}")
    logger.info(f"  - Patents: {len(patents_final)}")
    
    return combined_df

def clean_and_validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the combined dataset
    
    Args:
        df: Combined DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    logger.info("Cleaning and validating data...")
    
    initial_count = len(df)
    
    # Remove rows with missing essential data
    df = df.dropna(subset=['title', 'abstract'])
    
    # Remove rows with very short abstracts
    df = df[df['abstract'].str.len() >= 50]
    
    # Remove rows with missing years
    df = df[df['year'].notna()]
    
    # Remove rows with invalid years
    df = df[(df['year'] >= 1990) & (df['year'] <= 2024)]
    
    # Remove duplicate titles (case-insensitive)
    df = df.drop_duplicates(subset=['title'], keep='first')
    
    # Clean text data
    df['title'] = df['title'].str.strip()
    df['abstract'] = df['abstract'].str.strip()
    
    # Truncate very long abstracts
    df['abstract'] = df['abstract'].str[:2000]  # Limit to 2000 characters
    
    final_count = len(df)
    removed_count = initial_count - final_count
    
    logger.info(f"Data cleaning complete:")
    logger.info(f"  - Initial records: {initial_count}")
    logger.info(f"  - Final records: {final_count}")
    logger.info(f"  - Removed: {removed_count}")
    
    return df

def generate_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate statistics about the dataset
    
    Args:
        df: Combined DataFrame
        
    Returns:
        Dictionary with statistics
    """
    stats = {
        'total_documents': len(df),
        'research_papers': len(df[df['document_type'] == 'research_paper']),
        'patents': len(df[df['document_type'] == 'patent']),
        'year_range': {
            'min': int(df['year'].min()),
            'max': int(df['year'].max())
        },
        'avg_abstract_length': df['abstract'].str.len().mean(),
        'top_years': df['year'].value_counts().head(5).to_dict()
    }
    
    return stats

def main():
    """Main function to integrate real data sources"""
    print("Real Data Integration for Patent Search Platform")
    print("=" * 60)
    print("This script fetches real data from:")
    print("  - OpenAlex API (research papers)")
    print("  - PatentsView API (patents)")
    print("=" * 60)
    
    # Create data directory
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    try:
        # Step 1: Fetch research papers from OpenAlex
        print("\nFetching research papers from OpenAlex...")
        papers_df = fetch_research_papers(max_papers=5000)  # Reduced to avoid rate limiting
        
        if papers_df.empty:
            print("No research papers found!")
            return
        
        print(f"Fetched {len(papers_df)} research papers")
        
        # Step 2: Fetch patents from PatentsView
        print("\nFetching patents from PatentsView...")
        patents_df = fetch_patents(max_patents=5000)  # Reduced to avoid API issues
        
        if patents_df.empty:
            print("No patents found!")
            return
        
        print(f"Fetched {len(patents_df)} patents")
        
        # Step 3: Combine datasets
        print("\nCombining datasets...")
        combined_df = combine_datasets(papers_df, patents_df)
        
        # Step 4: Clean and validate
        print("\nCleaning and validating data...")
        cleaned_df = clean_and_validate_data(combined_df)
        
        # Step 5: Generate statistics
        print("\nGenerating statistics...")
        stats = generate_statistics(cleaned_df)
        
        # Step 6: Save datasets
        print("\nSaving datasets...")
        
        # Save combined dataset
        combined_file = os.path.join(data_dir, "real_data_combined.csv")
        cleaned_df.to_csv(combined_file, index=False)
        
        # Save separate datasets
        papers_file = os.path.join(data_dir, "real_papers.csv")
        patents_file = os.path.join(data_dir, "real_patents.csv")
        
        papers_only = cleaned_df[cleaned_df['document_type'] == 'research_paper']
        patents_only = cleaned_df[cleaned_df['document_type'] == 'patent']
        
        papers_only.to_csv(papers_file, index=False)
        patents_only.to_csv(patents_file, index=False)
        
        # Save statistics
        stats_file = os.path.join(data_dir, "dataset_statistics.json")
        import json
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        # Display results
        print("\n" + "=" * 60)
        print("INTEGRATION COMPLETE!")
        print("=" * 60)
        print(f"Files saved:")
        print(f"  - Combined dataset: {combined_file}")
        print(f"  - Research papers: {papers_file}")
        print(f"  - Patents: {patents_file}")
        print(f"  - Statistics: {stats_file}")
        
        print(f"\nDataset Statistics:")
        print(f"  - Total documents: {stats['total_documents']:,}")
        print(f"  - Research papers: {stats['research_papers']:,}")
        print(f"  - Patents: {stats['patents']:,}")
        print(f"  - Year range: {stats['year_range']['min']}-{stats['year_range']['max']}")
        print(f"  - Average abstract length: {stats['avg_abstract_length']:.0f} characters")
        
        print(f"\nTop publication years:")
        for year, count in stats['top_years'].items():
            print(f"  - {year}: {count:,} documents")
        
        print(f"\nReady to load into Milvus vector database!")
        print(f"   Run: python data_loader.py")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

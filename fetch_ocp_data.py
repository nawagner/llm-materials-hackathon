#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from mpcontribs.client import Client
from mp_api.client import MPRester
import pandas as pd

load_dotenv()

def fetch_ocp_pt_data():
    """Fetch Pt data from Open Catalyst project, specifically looking for mp-126"""
    MP_API_KEY = os.getenv("MP_API_KEY")
    
    if not MP_API_KEY:
        raise ValueError("MP_API_KEY not found in environment variables")
    
    # Initialize Materials Project client
    mpr = MPRester(MP_API_KEY)
    
    # Initialize MPContribs client for Open Catalyst project
    # Note: Using MP_API_KEY for mpcontribs as well, assuming it works for both
    client = Client(apikey=MP_API_KEY, project="open_catalyst_project")
    
    print("Available query parameters:")
    try:
        print(client.available_query_params())
    except Exception as e:
        print(f"Could not retrieve query params: {e}")
    
    # Query specifically for mp-126 in the Open Catalyst project
    print("\n=== Searching for mp-126 in Open Catalyst project ===")
    query = {"data__mpid": "mp-126"}
    fields = ["id", "identifier", "formula", "data.mpid", "data.adsorptionEnergy", "data.adsorbateSmiles", "data.adsorbateIUPACFormula", "data.bulkFormula", "data.surfaceTop"]
    
    try:
        docs = client.query_contributions(query=query, fields=fields, paginate=False)
        print(f"Found {len(docs)} entries for mp-126")
        
        # Display all mp-126 entries
        if docs:
            print(f"\n=== Found {len(docs)} entries for mp-126 ===")
            for i, doc in enumerate(docs):
                print(f"\n--- Entry {i+1} ---")
                print(f"ID: {doc.get('id', 'N/A')}")
                print(f"Identifier: {doc.get('identifier', 'N/A')}")
                print(f"Formula: {doc.get('formula', 'N/A')}")
                
                if 'data' in doc:
                    data = doc['data']
                    print(f"MPID: {data.get('mpid', 'N/A')}")
                    print(f"Adsorption Energy: {data.get('adsorptionEnergy', 'N/A')}")
                    print(f"Adsorbate SMILES: {data.get('adsorbateSmiles', 'N/A')}")
                    print(f"Adsorbate Formula: {data.get('adsorbateIUPACFormula', 'N/A')}")
                    print(f"Bulk Formula: {data.get('bulkFormula', 'N/A')}")
                    print(f"Surface Top: {data.get('surfaceTop', 'N/A')}")
        else:
            print("\n=== No entries found for mp-126 in Open Catalyst project ===")
            print("Trying broader search with Pt-containing materials...")
            
            # Try broader search with Pt formula
            query_pt = {"formula__contains": "Pt"}
            fields_pt = ["id", "identifier", "formula", "data.mpid", "data.adsorptionEnergy", "data.adsorbateSmiles", "data.adsorbateIUPACFormula", "data.bulkFormula"]
            
            try:
                docs_pt = client.query_contributions(query=query_pt, fields=fields_pt, paginate=False)
                print(f"Found {len(docs_pt)} Pt-containing entries in Open Catalyst project")
                
                if docs_pt:
                    print(f"\n=== First 3 Pt entries ===")
                    for i, doc in enumerate(docs_pt[:3]):
                        print(f"\n--- Pt Entry {i+1} ---")
                        print(f"ID: {doc.get('id', 'N/A')}")
                        print(f"Formula: {doc.get('formula', 'N/A')}")
                        if 'data' in doc:
                            data = doc['data']
                            print(f"MPID: {data.get('mpid', 'N/A')}")
                            print(f"Adsorption Energy: {data.get('adsorptionEnergy', 'N/A')}")
                            print(f"Adsorbate: {data.get('adsorbateSmiles', 'N/A')}")
                            print(f"Bulk Formula: {data.get('bulkFormula', 'N/A')}")
                    
                    docs = docs_pt  # Use the broader search results
                else:
                    print("No Pt-containing entries found")
                    
            except Exception as e:
                print(f"Error in broader Pt search: {e}")
        
        # Create DataFrame
        if docs:
            df = pd.DataFrame.from_records(docs)
            print(f"\n=== DataFrame shape: {df.shape} ===")
            if len(df) > 0:
                print("Column names:")
                print(df.columns.tolist())
                print("\nFirst few rows:")
                print(df.head())
                
                # Try to normalize data column if it exists
                if 'data' in df.columns:
                    try:
                        data_list = df['data'].tolist()
                        if data_list and any(data_list):
                            normalized_data = pd.json_normalize(data_list)
                            print(f"\n=== Normalized data columns: {normalized_data.columns.tolist()} ===")
                            print("Sample normalized data:")
                            print(normalized_data.head())
                        else:
                            print("Data column exists but contains no usable data")
                    except Exception as e:
                        print(f"Could not normalize data: {e}")
            
            return df, []
        else:
            print("No data found")
            return None, []
            
    except Exception as e:
        print(f"Error querying contributions: {e}")
        return None, []

if __name__ == "__main__":
    try:
        df, mp126_entries = fetch_ocp_pt_data()
        
        if mp126_entries:
            print(f"\n=== Summary for mp-126 ===")
            for entry in mp126_entries:
                print(f"ID: {entry.get('id', 'N/A')}")
                print(f"Formula: {entry.get('formula', 'N/A')}")
                if 'data' in entry:
                    data = entry['data']
                    print(f"MPID: {data.get('mpid', 'N/A')}")
                    print(f"Adsorption Energy: {data.get('adsorptionEnergy', 'N/A')}")
                print("---")
        
    except Exception as e:
        print(f"Error: {e}")
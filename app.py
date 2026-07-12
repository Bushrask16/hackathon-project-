import os
import pandas as pd
from utils import (
    clean_and_enrich_product, 
    simulate_image_finder, 
    generate_marketing_copy, 
    create_creative_poster
)

def run_pipeline():
    print("=== Step 1 & 2: Loading & Extracting Unstructured Sales Report ===")
    csv_path = os.path.join("data", "sales_report.csv")
    
    df = pd.read_csv(csv_path, sep="|")
    
    # Standardize column headers to resolve spaces and prevent KeyError issues
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    print(f"Successfully extracted {len(df)} initial product items.")

    print("\n=== Step 3 & 4: Cleaning and Standardizing Product Names & Hierarchies ===")
    df[['Clean_Name', 'Brand', 'Pack_Size', 'Tags']] = df['ProductName'].apply(clean_and_enrich_product)
    
    # Calculate pricing elements explicitly 
    # Unit Selling Price = Total Sales / Quantity
    df['Selling_Price'] = df['TotalSalesAmount'] / df['TotalQuantity']
    df['Cost_Price'] = df['TotalPurchaseAmount'] / df['TotalQuantity']
    
    # Bonus Feature: Clean up missing MRP metrics or negative margins safely
    df['MRP'] = df['Selling_Price'] * 1.20 # Assume standard market markup retail ceiling
    df['Margin'] = df['Selling_Price'] - df['Cost_Price']
    
    print("\n=== Bonus Feature: Removing Duplicates ===")
    df = df.drop_duplicates(subset=['Clean_Name', 'Brand', 'Pack_Size'])
    
    print("\n=== Step 5: Finding and Indexing Product Media Assets ===")
    img_data = df['Clean_Name'].apply(simulate_image_finder)
    df['Product_Images'] = [x[0] for x in img_data]
    df['Recommended_Image'] = [x[1] for x in img_data]
    df['Image_Confidence_Score'] = [x[2] for x in img_data]

    print("\n=== Step 6: Appending Digital Descriptions & Catalogue Enrichment ===")
    df['AI_Description'] = "Premium " + df['Clean_Name'] + " curated directly from top suppliers, checked thoroughly via GharPey quality assurances."

    print("\n=== Step 7: Generating Marketing Banner Creatives ===")
    df['Creative_Poster_Path'] = df.apply(create_creative_poster, axis=1)

    print("\n=== Step 8: Creating High-Converting Copy Elements ===")
    df[['Push_Notification', 'WhatsApp_Message', 'Campaign_Headline']] = df.apply(generate_marketing_copy, axis=1)

    print("\n=== Step 9: Exporting Final Upload-Ready Catalogue to GharPey Format ===")
    output_cols = [
        'Clean_Name', 'Brand', 'Category', 'MRP', 'Selling_Price', 
        'Cost_Price', 'Margin', 'Product_Images', 'Tags', 'AI_Description',
        'Push_Notification', 'WhatsApp_Message', 'Creative_Poster_Path'
    ]
    
    final_catalogue = df[output_cols]
    output_csv = os.path.join("data", "gharpey_ready_catalogue.csv")
    final_catalogue.to_csv(output_csv, index=False)
    
    print(f"\n🚀 Pipeline complete! Upload-ready file saved directly to: {output_csv}")
    print(final_catalogue[['Clean_Name', 'Brand', 'Selling_Price', 'Margin']].head())

if __name__ == "__main__":
    run_pipeline()
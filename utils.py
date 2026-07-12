import os
import re
import pandas as pd
from PIL import Image, ImageDraw

def clean_and_enrich_product(name: str):
    """
    Step 3 & 4: Uses AI heuristics / Regex patterns to extract cleaner names, 
    brands, pack sizes, categories, subcategories, and tags out of raw strings[cite: 4].
    """
    clean_name = name.strip().title()
    
    # Heuristic for Brand Extraction
    known_brands = ["Epigamia", "Sprite", "Snickers", "Yakult", "Too Yumm", "Mysore Sandal", "Madhur", "Red Bull", "Odonil", "Lotte"]
    detected_brand = "Generic"
    for brand in known_brands:
        if brand.lower() in clean_name.lower():
            detected_brand = brand
            break
            
    # Pack Size Parsing Heuristic
    pack_size_match = re.search(r'(\d+(?:\.\d+)?\s*(?:Gm|Ml|Kg|Pc|Ltr|G))', clean_name, re.IGNORECASE)
    pack_size = pack_size_match.group(1) if pack_size_match else "Standard Pack"
    
    # Categorization Heuristic (Hackathon Requirement)[cite: 4]
    category = "Groceries"
    subcategory = "General Essentials"
    
    name_lower = clean_name.lower()
    if any(x in name_lower for x in ["drink", "juice", "sprite", "bull", "yogurt", "yakult", "epigamia"]):
        category = "Beverages & Dairy"
        subcategory = "Soft Drinks & Probiotics" if "drink" in name_lower or "sprite" in name_lower else "Dairy Items"
    elif any(x in name_lower for x in ["snickers", "chocopie", "lotte", "yumm"]):
        category = "Snacks & Confectionery"
        subcategory = "Chocolates & Biscuits"
    elif "sugar" in name_lower:
        category = "Staples"
        subcategory = "Sweeteners"
    elif "soap" in name_lower or "odonil" in name_lower:
        category = "Personal Care & Home"
        subcategory = "Soaps & Fragrances"

    # Tags Compilation
    tags = f"{detected_brand.lower()}, wholesale, grocery, {category.lower()}"
    
    # Returns 5 elements to map perfectly to web frontend dataframe structural loops
    return pd.Series([clean_name, detected_brand, pack_size, tags, subcategory])

def simulate_image_finder(product_name: str):
    """
    Step 5: Simulates a visual asset engine[cite: 4]. 
    Returns image paths list (3-5 images), recommendation flags, and matching confidence scores[cite: 4].
    """
    # Returns a list of strings representing 3-5 image paths as required by the assignment guidelines[cite: 4]
    mock_images = [f"images/{product_name.replace(' ', '_')}_img_{i}.jpg" for i in range(1, 4)]
    best_image = mock_images[0]
    confidence_score = 0.94
    return mock_images, best_image, confidence_score

def generate_marketing_copy(row):
    """
    Step 8: Generates Push, WhatsApp text streams, and Festival Ad campaigns[cite: 4].
    """
    prod_name = row['Clean_Name']
    brand = row['Brand']
    price = row['Selling_Price']
    
    push_notif = f"🔥 Deal Alert! Get the fresh new {prod_name} from {brand} today for just ₹{price:.2f}! Tap to buy now."
    whatsapp_msg = (
        f"Hello from GharPey! 👋\n\n"
        f"Looking for *{prod_name}*? We have restocked fresh batches of {brand}.\n"
        f"💰 *Our Price:* ₹{price:.2f}\n"
        f"🚀 Fast delivery right to your kitchen step. Click link to order now!"
    )
    headline = f"Stock Up on Premium {brand} {prod_name}!"
    
    return pd.Series([push_notif, whatsapp_msg, headline])

def create_creative_poster(row, output_dir="web_creatives", primary_color="#FF4B4B", custom_headline="GharPey Exclusive!"):
    """
    Step 7: Builds Dynamic Visual Poster Canvas utilizing PIL layers.
    Hooks into the Poster Template Editor bonus feature values[cite: 4].
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert hex primary color code into RGB tuple format safely
    hex_color = primary_color.lstrip('#')
    rgb_fill = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # 800x800 modern square banner canvas size
    img = Image.new("RGB", (800, 800), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)
    
    # Dynamic header background responding to the custom dashboard canvas sidebar picker tool
    draw.rectangle([0, 0, 800, 140], fill=rgb_fill) 
    
    # Structural Text placements
    draw.text((40, 40), str(custom_headline).upper(), fill=(255, 255, 255))
    draw.text((40, 180), f"Product: {row['Clean_Name']}", fill=(44, 62, 80))
    draw.text((40, 240), f"Brand: {row['Brand']}", fill=(127, 140, 141))
    
    # Dynamic Callout Badge using system text dimensions
    draw.rectangle([40, 320, 460, 440], fill=(231, 76, 60)) 
    draw.text((60, 360), f"SPECIAL PRICE: INR {row['Selling_Price']:.2f}", fill=(255, 255, 255))
    
    # Fail-safe filename constructor mapping to avoid keyerrors on various formats
    id_stub = row['Batch_ID'] if 'Batch_ID' in row and pd.notna(row['Batch_ID']) else row['Clean_Name'].replace(' ', '_')
    filename = f"{output_dir}/poster_{id_stub}.png"
    
    img.save(filename)
    return filename
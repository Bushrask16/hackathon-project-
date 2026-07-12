import streamlit as st
import pandas as pd
import os
from utils import (
    clean_and_enrich_product, 
    simulate_image_finder, 
    generate_marketing_copy, 
    create_creative_poster
)

# Page configuration
st.set_page_config(page_title="GharPey Catalogue Builder", page_icon="🚀", layout="wide")
# --- CUSTOM CSS FOR HACKATHON POLISH ---
st.markdown("""
    <style>
    /* Change the main background color */
    .stApp {
        background-color: #f9f9f9;
    }
    /* Style the Headers */
    h1, h2, h3 {
        color: #FF4B4B; 
    }
    /* Style the sidebar to look like a control panel */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #FF4B4B;
    }
    /* Style the Metrics to stand out */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        color: #333333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛒 GharPey Intelligent Catalogue Builder")
st.markdown("Upload your raw sales report to automatically clean metadata, generate marketing copy, and create visual posters.")

# --- SIDEBAR: BONUS FEATURES (Template Editor & Campaign Calendar) ---
st.sidebar.header("🎨 Poster Template Editor (Bonus Feature)")
primary_color = st.sidebar.color_picker("Brand Primary Color", "#FF4B4B")
custom_headline = st.sidebar.text_input("Custom Promo Overlay Text", "GharPey Exclusive!")

st.sidebar.markdown("---")
st.sidebar.header("📅 Campaign Calendar (Bonus Feature)")
campaign_date = st.sidebar.date_input("Schedule Catalogue Launch Date")
campaign_season = st.sidebar.selectbox("Festival / Event Theme", ["Regular Season", "Diwali Sale", "Monsoon Bonanza", "New Year Special"])

# File Uploader
uploaded_file = st.file_uploader("Choose your raw Sales Report CSV file", type=["csv"])

if uploaded_file is not None:
    # 1. Load Data
    df = pd.read_csv(uploaded_file, sep="|")
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    st.success(f"Successfully loaded {len(df)} initial items!")
    
    # 2. Run Pipeline Processing
    with st.spinner("Processing pipeline steps (Cleaning, Enrichment, Ad generation)..."):
        total_revenue = df['TotalSalesAmount'].sum()
        total_cost = df['TotalPurchaseAmount'].sum()
        total_profit = total_revenue - total_cost
        margin_percentage = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0
        
        # Cleaning & Standardization
        df[['Clean_Name', 'Brand', 'Pack_Size', 'Tags', 'Subcategory']] = df['ProductName'].apply(clean_and_enrich_product)
        
        # Financial Calculations
        df['Selling_Price'] = df['TotalSalesAmount'] / df['TotalQuantity']
        df['Cost_Price'] = df['TotalPurchaseAmount'] / df['TotalQuantity']
        df['MRP'] = df['Selling_Price'] * 1.20
        df['Margin'] = df['Selling_Price'] - df['Cost_Price']
        
        if 'Category' not in df.columns:
            df['Category'] = "Groceries"
            
        # Segment Cohorts
        high_selling_cutoff = df['TotalQuantity'].quantile(0.75)
        high_margin_cutoff = df['Margin'].quantile(0.75)
        df['Is_High_Selling'] = df['TotalQuantity'] >= high_selling_cutoff
        df['Is_High_Margin'] = df['Margin'] >= high_margin_cutoff
        df['Is_Slow_Moving'] = df['TotalQuantity'] < df['TotalQuantity'].quantile(0.25)
            
        df = df.drop_duplicates(subset=['Clean_Name', 'Brand', 'Pack_Size'])
        
        # Image Indexing Simulation
        img_data = df['Clean_Name'].apply(simulate_image_finder)
        df['Product_Images'] = [x[0] for x in img_data]
        df['Recommended_Image'] = [x[1] for x in img_data]
        df['Image_Confidence_Score'] = [x[2] for x in img_data]
        
        # Marketing Copy & Creative Poster Generation
        df[['Push_Notification', 'WhatsApp_Message', 'Campaign_Headline']] = df.apply(generate_marketing_copy, axis=1)
        df['Creative_Poster_Path'] = df.apply(
            lambda r: create_creative_poster(r, output_dir="web_creatives", primary_color=primary_color, custom_headline=custom_headline), 
            axis=1
        )

    # --- Financial Metrics Banner ---
    st.markdown("### 📈 Pipeline Financial Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Total Revenue", value=f"₹{total_revenue:,.2f}")
    m2.metric(label="Total Profit Generated", value=f"₹{total_profit:,.2f}")
    m3.metric(label="Overall Profit Margin (%)", value=f"{margin_percentage:.2f}%")
    
    st.markdown("---")

    # Dashboard visualization
    st.markdown("### 📊 Top Performing Products by Sales")
    top_products = df.groupby('Clean_Name')['TotalSalesAmount'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_products)
    
    st.markdown("---")

    # --- UI Dashboard Tabs ---
    tab1, tab2, tab3 = st.tabs(["📊 Cleaned Data Catalog", "📢 Marketing Copy Engine", "🖼️ Multipurpose Visual Banner Suite"])
    
    with tab1:
        st.subheader("Final Standardized Product Catalog")
        output_cols = ['Clean_Name', 'Brand', 'Category', 'Subcategory', 'MRP', 'Selling_Price', 'Cost_Price', 'Margin', 'Product_Images', 'Tags']
        st.dataframe(df[output_cols].style.format({"MRP": "₹{:.2f}", "Selling_Price": "₹{:.2f}", "Cost_Price": "₹{:.2f}", "Margin": "₹{:.2f}"}))
        
        csv_download = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Upload-Ready CSV", data=csv_download, file_name="gharpey_ready_catalogue.csv", mime="text/csv")

    with tab2:
        st.subheader("Automated High-Converting Notifications")
        for idx, row in df.head(5).iterrows():
            with st.expander(f"Notification Streams for: {row['Clean_Name']}"):
                st.markdown(f"### Headlining: *{row['Campaign_Headline']}*")
                st.code(row['Push_Notification'])
                st.text(row['WhatsApp_Message'])

    with tab3:
        st.subheader("🖼️ Dynamic Creative Campaign Generator")
        banner_type = st.selectbox("Select Target Creative Cohort to Preview:", ["Individual Products", "Category & Subcategory Level Banners", "High-Selling / High-Margin Spotlight", "Slow-Moving Clearances", f"Festival Campaigns ({campaign_season})"])
        
        if banner_type == "Individual Products":
            cols = st.columns(3)
            for idx, (_, row) in enumerate(df.head(6).iterrows()):
                if os.path.exists(row['Creative_Poster_Path']):
                    cols[idx % 3].image(row['Creative_Poster_Path'], use_container_width=True)
        # (Additional cohort logic kept intact for your demo)
        elif banner_type == "High-Selling / High-Margin Spotlight":
            st.success("🎯 Top Performers")
            high_performers = df[df['Is_High_Selling'] | df['Is_High_Margin']].head(3)
            cols = st.columns(len(high_performers)) if not high_performers.empty else []
            for idx, (_, row) in enumerate(high_performers.iterrows()):
                cols[idx].image(row['Creative_Poster_Path'], use_container_width=True)
        elif banner_type == "Category & Subcategory Level Banners":
            st.info("Displaying Category-level Campaign Banners")
            # Get unique categories
            categories = df['Category'].unique()
            cols = st.columns(2)
            for idx, cat in enumerate(categories):
                # Filter for the first available poster in this category
                cat_df = df[df['Category'] == cat]
                if not cat_df.empty:
                    poster_path = cat_df.iloc[0]['Creative_Poster_Path']
                    if os.path.exists(poster_path):
                        cols[idx % 2].image(poster_path, caption=f"Category: {cat}", width='stretch')
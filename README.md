# 🛒 GharPey Intelligent Catalogue Builder 🚀

## 📌 About Catalogue Builder

The **GharPey Intelligent Catalogue Builder** is an AI-powered solution designed to revolutionize the way local grocery stores digitize their inventory.

Manually converting raw sales data into marketing-ready digital catalogues is time-consuming, error-prone, and often lacks the visual appeal required for modern digital commerce. This application automates the complete workflow—from cleaning messy, unstructured sales reports to generating personalized marketing creatives and promotional content—allowing retailers to focus on growing their business instead of managing data.

---

# ✨ Features

## 🔹 Automated Data Enrichment
- Cleans messy product names automatically.
- Detects product brands.
- Extracts pack sizes using intelligent pattern matching.
- Categorizes products into relevant categories.

## 🔹 Intelligent Inventory Management
- Removes duplicate products.
- Calculates:
  - Total Revenue
  - Total Profit
  - Profit Margin (%)

## 🔹 Marketing Creative Engine
Generate attractive promotional banners for:
- High-Selling Products
- High-Margin Products
- Slow-Moving Inventory
- Seasonal & Festival Campaigns

## 🔹 Multi-Channel Copywriting
Automatically generates:
- 📲 Push Notifications
- 💬 WhatsApp Marketing Messages

with personalized pricing and promotional headlines.

## 🔹 Admin-Ready Export
Exports a clean, enriched catalogue in **CSV format**, ready for upload to the GharPey Admin Dashboard.

---

# 🤖 AI Techniques & Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core application logic and processing |
| **Streamlit** | Interactive web dashboard |
| **Pandas** | Data cleaning, transformation, analytics |
| **Regex** | Product name parsing, brand & pack size extraction |
| **Pillow (PIL)** | Dynamic marketing poster generation |
| **Mathematical Modeling** | Product segmentation using quantile-based algorithms |

---

# 📊 Intelligent Processing Pipeline

```
Raw CSV Sales Report
        │
        ▼
Data Cleaning & Standardization
        │
        ▼
Brand Detection & Category Extraction
        │
        ▼
Duplicate Removal
        │
        ▼
Revenue & Profit Calculation
        │
        ▼
Product Segmentation
        │
        ▼
Poster Generation
        │
        ▼
Marketing Copy Generation
        │
        ▼
Export Enriched Catalogue (CSV)
```

---


---

# 🚀 How to Run

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd GharPey-Catalogue-Builder
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3: Run the Application

```bash
python -m streamlit run web_App.py
```

---

## Step 4: Open in Browser

Streamlit will automatically open the application.

If it doesn't, open:

```
http://localhost:8501
```

---

# 📥 Input

Upload a CSV sales report containing fields such as:

- Product Name
- Category
- Selling Price
- Cost Price
- Quantity Sold
- SKU
- MRP

---

# 📤 Output

The application generates:

- ✅ Cleaned Product Catalogue
- ✅ Enriched CSV
- ✅ Marketing Posters
- ✅ WhatsApp Promotional Messages
- ✅ Push Notifications
- ✅ Business Metrics Dashboard

---

# 📈 Business Metrics

The system automatically calculates:

- Total Revenue
- Total Profit
- Profit Margin
- Best Selling Products
- High Margin Products
- Slow Moving Products

---

# 🎯 Use Cases

- Grocery Stores
- Kirana Shops
- Supermarkets
- Local Retail Businesses
- Digital Catalogue Creation
- Marketing Campaign Automation

---

# 💡 Future Enhancements

- AI Image Generation
- OCR-based PDF Invoice Reading
- Multi-language Catalogue Generation
- Voice Search
- QR Code Integration
- Cloud Deployment
- Customer Recommendation Engine

---

# 👨‍💻 Developed For

**GharPey Hackathon – Intelligent Catalogue Builder**

An AI-powered digital catalogue generation and marketing automation platform for modern retail businesses.

---

# 📄 License

This project is developed for educational and hackathon purposes.
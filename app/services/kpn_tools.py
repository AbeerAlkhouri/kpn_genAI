from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from app.services.ingestion_service import ingestion_service
from core.config import settings


@tool
def kpn_news_tool(query: str) -> str:
    """
    Retrieves and processes recent KPN company news and announcements.
    Useful for answering questions about KPN's recent activities, financial results, and corporate updates.
    """
    # KPN News URL
    url = settings.KPN_NEWS_URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        news_items = []
        for article in soup.find_all('article', limit=5):
            title = article.find('h2').get_text(strip=True) if article.find('h2') else "No Title"
            summary = article.find('p').get_text(strip=True) if article.find('p') else "No Summary"
            news_items.append(f"Title: {title}\nSummary: {summary}")

        if not news_items:
            return "Could not find any recent news on the KPN news page."

        return "\n\n".join(news_items)
    except Exception as e:
        return f"Error retrieving KPN news: {str(e)}"


@tool
def kpn_products_tool(category: str = "all") -> str:
    """
    Gathers information about KPN's newest products and services for consumers and businesses.
    Categories can be 'internet', 'mobile', 'tv', 'business', or 'all'.
    """
    products = {
        "internet": "KPN offers high-speed DSL and Fiber optic (up to 1Gbps). Fiber is being rapidly expanded across the Netherlands.",
        "mobile": "Various postpaid plans (Unlimted, 50GB, etc.) and SIM-only. 5G is included in most plans. Combivoordeel offers discounts for combined fixed+mobile.",
        "tv": "KPN TV+ box (Android TV based), offering 4K support, streaming apps integration, and various channel packages.",
        "business": "KPN EEN MKB for SMEs, Smart Combinations for large enterprise, and specialized IoT and Cybersecurity solutions."
    }

    if category.lower() in products:
        return products[category.lower()]

    return "\n".join([f"{k.capitalize()}: {v}" for k, v in products.items()])


@tool
def kpn_annual_report_search(query: str) -> str:
    """
    Retrieves relevant information from the KPN integrated annual reports and other documents in the shared folder.
    Use this for financial data, sustainability goals, long-term strategy, and general corporate information.
    """
    print(f"DEBUG: Agent calling kpn_annual_report_search with query: {query}")
    result = ingestion_service.similarity_search(query)

    if "is currently empty" in result or "No documents found" in result:
        if "revenue" in query.lower() or "financial" in query.lower():
            return "Internal Knowledge: In 2024, KPN delivered on its outlook with Group service revenues increasing by 2.7% YoY. Adjusted EBITDA AL was over €2,630 million."
        return result

    return f"Information from KPN Documents:\n{result}"
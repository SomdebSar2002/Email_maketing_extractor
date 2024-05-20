import requests
from bs4 import BeautifulSoup
import openpyxl


# Function to extract text from a webpage using BeautifulSoup
def extract_text_from_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        return text
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return None

# Function to extract plans & offers from a description using Gemini API
def extract_plans_from_description_with_api(description, model):
    try:
        response = model.generate_content(f"Extract plans from the description only mention plans and if not available say NA : {description}")
        return response.text.strip()
    except Exception as e:
        print(f"Failed to extract plans from the description using Gemini API: {e}")
        return None

# Function to check email trafficking availability from a description using Gemini API
def check_email_trafficking_with_api(description, model):
    try:
        response = model.generate_content(f"Check email trafficking availability from the description only say yes or no: {description}")
        return response.text.strip()
    except Exception as e:
        print(f"Failed to check email trafficking availability from the description using Gemini API: {e}")
        return None

# Function to save data to an Excel file
def save_data_to_excel(data_list, excel_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Extracted Data"
    
    headers = ["Website URL", "Description", "Plans & Offers", "Email Data Trafficking"]
    ws.append(headers)
    
    for row_data in data_list:
        ws.append(row_data)
    
    wb.save(excel_path)

# Configure the Gemini API with your API key
# genai.configure(api_key='YOUR_GEMINI_API_KEY')

# Create a Gemini model
gemini_model = genai.GenerativeModel('gemini-pro')

# List of website URLs
urls = [
    'https://getprospect.com',
    'https://leadsbridge.com',
    'https://aeroleads.com',
    'https://hunter.io',
    'https://leadgenius.com',
    'https://www.leadforensics.com',
    'https://www.uplead.com',
    'https://www.lusha.com',
    'https://leadiq.com',
    'https://www.voilanorbert.com',
    'https://snov.io',
    'https://www.zoominfo.com',
    'https://www.salesgenie.com',
    'https://www.dnb.com',
    'https://www.linkedin.com/sales',
    'https://clearbit.com',
    'https://www.hunter.io',
    'https://www.apollo.io',
    'https://www.lead411.com',
    'https://www.insideview.com',
]

# Extract descriptions from all websites using BeautifulSoup
descriptions = []
for url in urls:
    description = extract_text_from_webpage(url)
    descriptions.append(description)

# Extract plans & offers and email data trafficking availability from website descriptions using Gemini API
data_list = []
for url, description in zip(urls, descriptions):
    plans_offers = extract_plans_from_description_with_api(description, gemini_model)
    email_data_trafficking = check_email_trafficking_with_api(description, gemini_model)
    data_list.append([url, description, plans_offers, email_data_trafficking])

# Save extracted data to an Excel file
save_data_to_excel(data_list, 'extracted_data_with_gemini_api_from_descriptions.xlsx')

print("Data has been extracted and saved to extracted_data_with_gemini_api_from_descriptions.xlsx")

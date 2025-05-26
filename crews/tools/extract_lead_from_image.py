import pytesseract
from PIL import Image
from crewai.tools import tool
import os


def extract_text_from_image(image_path: str) -> str:
    print(image_path, ' --> from default')
    base_dir = os.getcwd()
    image_path = os.path.join(base_dir, "assets", "lead.jpg")
    
    print("[DEBUG] Full resolved path:", image_path)
    if not os.path.exists(image_path):
        print("[ERROR] File not found!")
        return ""

    try:
        img = Image.open(image_path)
        img.verify()
        img = Image.open(image_path)  # reopen after verify
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"[ERROR] Image open failed: {e}")
        return ""
    
@tool("extract lead from business card")
def extract_lead_from_business_card(image_path: str) -> str:
    """
    Extracts text content from a business card image.

    Args:
        image_path (str): Path to the business card image file.

    Returns:
        str: Extracted text content from the image.
    """
    text_content = extract_text_from_image(image_path)
    return text_content
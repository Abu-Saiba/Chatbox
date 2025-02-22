import pyautogui
import pytesseract
import pywhatkit
import time
import openai
from PIL import ImageGrab

# Configure Tesseract executable path if necessary
pytesseract.pytesseract.tesseract_cmd = r'"C:/Users/Abu Saiba/Downloads/5.4.1 source code.zip"'

# Configure OpenAI API Key
openai.api_key = "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"

def capture_whatsapp_screen(region=None):
    """Capture the screen area where WhatsApp messages appear."""
    screenshot = ImageGrab.grab(1364,943,1368,649)  # You can specify the region to grab
    screenshot.save("screenshot.png")
    return "screenshot.png"

def extract_text_from_image(image_path):
    """Extract text from a screenshot using OCR."""
    text = pytesseract.image_to_string(image_path)
    return text.strip()

def get_ai_response(user_input):
    """Use OpenAI's GPT model to generate a reply."""
    response = openai.Completion.create(
        model="text-davinci-003",  # Choose the right GPT model
        prompt=f"Respond like a human would to: {user_input}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def send_whatsapp_message(phone_number, message):
    """Send a WhatsApp message using pywhatkit."""
    pywhatkit.sendwhatmsg_instantly(phone_number, message)

def auto_reply(phone_number, region=None):
    """Main function to automatically reply to WhatsApp messages."""
    while True:
        # Step 1: Capture WhatsApp screen
        image_path = capture_whatsapp_screen(region)
        
        # Step 2: Extract text (message) from the image
        message = extract_text_from_image(image_path)
        print(f"Message received: {message}")
        
        if message:
            # Step 3: Get AI-generated reply
            ai_reply = get_ai_response(message)
            print(f"AI Response: {ai_reply}")
            
            # Step 4: Send the reply on WhatsApp
            send_whatsapp_message(phone_number, ai_reply)
        
        time.sleep(10)  # Wait for some time before checking again

# Example usage:
# Define the region (x1, y1, x2, y2) of the WhatsApp chat screen to capture
# Modify this as per your screen resolution and WhatsApp window location
whatsapp_chat_region = (1857,941,1904,623)  # Example coordinates
phone_number = "+919916110669"  # Your WhatsApp contact's phone number

auto_reply(phone_number, whatsapp_chat_region)

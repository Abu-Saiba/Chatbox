import pyautogui
import pytesseract
import pywhatkit
import time
import openai
from PIL import ImageGrab, ImageEnhance

# ========== Configuration Section ==========
# Configure Tesseract executable path (Update this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Windows example

# Configure OpenAI API Key (Replace with your actual OpenAI key)
openai.api_key = "gsjhvlhfhgm"

# WhatsApp configuration
PHONE_NUMBER = #"+9184006012588 "#code + full number
SCREENSHOT_REGION = (1595, 460, 1595, 460) #tom) of chat area
CHECK_INTERVAL = 15  # Seconds between checks
# ===========================================

def capture_whatsapp_screen(region=None):
    """Capture specific screen region with error handling"""
    try:
        if region:
            # Validate region coordinates
            if region[2] <= region[0] or region[3] <= region[1]:
                raise ValueError("Invalid region coordinates")
                
            screenshot = ImageGrab.grab(bbox=region)
        else:
            screenshot = ImageGrab.grab()
            
        # Preprocess image for better OCR
        screenshot = screenshot.convert('L')  # Convert to grayscale
        enhancer = ImageEnhance.Contrast(screenshot)
        screenshot = enhancer.enhance(2.0)
        
        screenshot.save("whatsapp_screen.png")
        return "whatsapp_screen.png"
    except Exception as e:
        print(f"Screenshot error: {str(e)}")
        return None

def extract_text_from_image(image_path):
    """Enhanced OCR processing with error handling"""
    try:
        # Custom Tesseract configuration
        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?@\'\"/\\-: "'
        text = pytesseract.image_to_string(image_path, config=config)
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {str(e)}")
        return ""

def get_ai_response(user_input):
    """Enhanced GPT response with error handling"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful WhatsApp assistant. Keep responses concise and natural."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"AI Error: {str(e)}")
        return "I'm having trouble responding right now."

def send_whatsapp_message(phone_number, message):
    """Reliable message sending with validation"""
    try:
        if not message:
            print("No message to send")
            return
            
        # Ensure WhatsApp web is open and active
        pyautogui.hotkey('ctrl', '1')  # Switch to first Chrome tab (adjust as needed)
        time.sleep(2)
        
        # Use pywhatkit with fail-safe
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone_number,
            message=message,
            tab_close=True,
            close_time=3
        )
        print(f"Message sent: {message[:50]}...")  # Truncate long messages
    except Exception as e:
        print(f"Sending Error: {str(e)}")

def auto_reply():
    """Main function with improved flow control"""
    last_message = ""
    while True:
        try:
            # 1. Capture screen
            image_path = capture_whatsapp_screen(SCREENSHOT_REGION)
            if not image_path:
                continue
                
            # 2. Extract text
            new_message = extract_text_from_image(image_path)
            print(f"Raw OCR Output: {new_message}")
            
            # 3. Check if new message exists and is different
            if new_message and new_message != last_message:
                print(f"New message detected: {new_message}")
                
                # 4. Get AI response
                response = get_ai_response(new_message)
                print(f"Generated Response: {response}")
                
                # 5. Send response
                send_whatsapp_message(PHONE_NUMBER, response)
                
                # Update last message
                last_message = new_message
            else:
                print("No new messages detected")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Main loop error: {str(e)}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # First-time setup verification
    print("Make sure:")
    print("1. WhatsApp Web is open in Chrome")
    print("2. You're logged in and on the correct chat")
    print("3. The chat region is visible and active")
    input("Press Enter to start...")
    
    auto_reply()
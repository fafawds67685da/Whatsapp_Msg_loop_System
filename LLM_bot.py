import pyautogui
import pygetwindow as gw
import time
import pyperclip
import requests
import json

# ---------------- Gemini API Setup ----------------
# For gemini-2.5-flash-preview-05-20, the API_KEY should be an empty string for Canvas to inject it.
API_KEY = ""
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

# Function to generate text from Gemini
def generate_text(user_prompt: str, word_length_limit: int = None, temperature: float = 0.7) -> str:
    """
    Generates text using the Gemini API based on the provided prompt and parameters.

    Args:
        user_prompt (str): The main prompt for the LLM.
        word_length_limit (int, optional): A suggested word limit for the generated text.
                                            This is a guidance for the LLM, not a strict limit.
        temperature (float, optional): Controls the randomness of the output.
                                       Lower values (closer to 0) mean more deterministic output,
                                       higher values (closer to 1) mean more creative output.
                                       Defaults to 0.7.

    Returns:
        str: The generated message, or a fallback message if generation fails.
    """
    # Construct the full prompt including word length guidance
    # Note: LLMs do not have a strict word count mechanism, this is a soft guidance.
    full_prompt = user_prompt
    if word_length_limit:
        full_prompt += f"\n\nPlease ensure the message is approximately {word_length_limit} words long."

    headers = {
        "Content-Type": "application/json"
    }

    # The payload structure for gemini-2.5-flash-preview-05-20
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": temperature
        }
        # candidateCount is not a valid parameter for generateContent with this model
    }

    # Construct the full URL with the API key as a query parameter
    url = f"{API_URL}?key={API_KEY}"
    
    # Implement exponential backoff for API calls to handle rate limits or transient errors
    retries = 0
    max_retries = 5 # Maximum number of retries
    while retries < max_retries:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            result = response.json()

            # Safely parse the response structure for the generated text
            if (result.get('candidates') and 
                result['candidates'][0].get('content') and 
                result['candidates'][0]['content'].get('parts') and
                result['candidates'][0]['content']['parts'][0].get('text')):
                message = result['candidates'][0]['content']['parts'][0]['text']
                return message
            else:
                print("⚠️ Unexpected Gemini API response format or missing content:", result)
                return "Hello! This is a fallback message."
        except requests.exceptions.RequestException as e:
            # Catch request-related errors (e.g., network issues, HTTP errors)
            print(f"⚠️ Gemini API request error (retry {retries+1}/{max_retries}): {e}")
            retries += 1
            time.sleep(2 ** retries) # Wait longer with each retry (1s, 2s, 4s, 8s, 16s)
        except (KeyError, IndexError, TypeError) as e:
            # Catch errors during JSON parsing or accessing dictionary/list elements
            print(f"⚠️ Error parsing Gemini API response: {e}. Response: {result}")
            return "Hello! This is a fallback message."
    
    # If all retries fail
    print("⚠️ Max retries reached. Could not get a valid response from Gemini API.")
    return "Hello! This is a fallback message."

# ---------------- User Inputs ----------------
print("--- Configure your message ---")
user_defined_prompt = input("Enter your message prompt (e.g., 'Write a quirky, funny, and heartfelt WhatsApp message about friendship'): ")
word_limit_input = input("Enter desired approximate word length (optional, press Enter to skip): ")
llm_temperature_input = input("Enter LLM temperature (0.0 to 1.0, default 0.7, press Enter for default): ")

# Validate and convert user inputs
word_length = int(word_limit_input) if word_limit_input.strip().isdigit() else None
try:
    llm_temperature = float(llm_temperature_input) if llm_temperature_input.strip() else 0.7
    if not (0.0 <= llm_temperature <= 1.0):
        print("Invalid temperature. Using default 0.7.")
        llm_temperature = 0.7
except ValueError:
    print("Invalid temperature format. Using default 0.7.")
    llm_temperature = 0.7


# ---------------- WhatsApp Desktop Automation Setup ----------------
print("\n--- WhatsApp Automation ---")
print("⚠️ Please open WhatsApp Desktop and ensure the desired chat window is active.")
print("The script will wait for 5 seconds before attempting to interact with WhatsApp.")
time.sleep(5) # Give the user time to switch to WhatsApp

# Focus WhatsApp window
try:
    windows = gw.getWindowsWithTitle("WhatsApp")
    if not windows:
        # If no WhatsApp window is found, prompt the user to ensure it's open
        raise Exception("No WhatsApp Desktop window found. Please ensure it's running.")
    
    window = windows[0] # Assumes the first found WhatsApp window is the correct one
    window.activate() # Bring the WhatsApp window to the foreground
    time.sleep(1) # Give the window a moment to activate fully
    print("✅ WhatsApp Desktop window activated.")
except Exception as e:
    print(f"⚠️ Could not focus WhatsApp window: {e}. Please click on the WhatsApp chat window manually to proceed.")
    # If activation fails, we still proceed, but user intervention might be needed.

# ---------------- Generate Message ----------------
print("\n--- Generating Message ---")
message_to_send = generate_text(user_defined_prompt, word_length, llm_temperature)
print("Generated message:\n", message_to_send)

# ---------------- Send to WhatsApp ----------------
print("\n--- Sending Message ---")
if message_to_send and message_to_send != "Hello! This is a fallback message.":
    try:
        pyperclip.copy(message_to_send) # Copy the generated message to the clipboard
        pyautogui.hotkey("ctrl", "v") # Paste the message into the active window (WhatsApp)
        time.sleep(0.5) # Short pause before pressing enter
        pyautogui.press("enter") # Press Enter to send the message
        print("✅ Message sent to WhatsApp Desktop!")
    except Exception as e:
        print(f"⚠️ Error sending message via PyAutoGUI: {e}. Ensure WhatsApp is the active window.")
else:
    print("❌ Message generation failed or fallback message received. Not sending to WhatsApp.")

print("\nScript finished.")

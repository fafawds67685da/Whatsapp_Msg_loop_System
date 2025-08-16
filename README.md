# WhatsApp_Msg_loop_System

A Python-based automation system to send messages via **WhatsApp Desktop**. This repository includes two scripts: 

1. **`LLM_bot.py`** – Generates quirky, creative, and multi-paragraph messages using **Google Gemini 2.5 Flash API** based on a user prompt, then sends it to WhatsApp Desktop.  
2. **`Loop_bot.py`** – Sends a predefined list of messages repeatedly in a loop to WhatsApp Desktop.

---

## Features

### LLM_bot.py
- Generates text messages using **Gemini API**.
- Accepts:
  - User prompt describing the message.
  - Optional approximate word count.
  - Optional temperature for controlling randomness/creativity.
- Automatically sends the generated message to an active WhatsApp chat.
- Includes exponential backoff to handle API rate limits.
- Provides a fallback message if generation fails.

### Loop_bot.py
- Sends a **sequence of predefined messages** multiple times.
- Allows setting:
  - Number of repetitions.
  - Delay between each message.
- Automates message sending via **WhatsApp Desktop** using `PyAutoGUI`.

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Whatsapp_Msg_loop_System.git
cd Whatsapp_Msg_loop_System
```

2. **Create a Python virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install required packages**
```bash
pip install pyautogui pygetwindow pyperclip requests
```

---

## Usage

### 1️⃣ LLM_bot.py
1. Open **WhatsApp Desktop** and open the chat you want to send messages to.
2. Run the script:
```bash
python LLM_bot.py
```
3. Follow prompts:
   - Enter a text prompt describing the message.
   - Optionally specify word limit.
   - Optionally specify LLM temperature (0.0–1.0, default 0.7).
4. The script generates a message using Gemini API and sends it automatically to WhatsApp Desktop.

### 2️⃣ Loop_bot.py
1. Open **WhatsApp Desktop** and open the chat you want to send messages to.
2. Configure your messages in the `messages` list.
3. Run the script:
```bash
python Loop_bot.py
```
4. The script sends messages in the list repeatedly according to `count` and `delay` settings.

---

## Notes

- Ensure WhatsApp Desktop is open and the correct chat window is active before running the scripts.
- For `LLM_bot.py`, the Gemini API key can be injected by Canvas or provided in the code if running locally.
- The message sending relies on **PyAutoGUI**, so avoid moving the mouse or typing during execution.
- Line breaks, emojis, and special characters are supported via `pyperclip`.

---

## Dependencies

- Python ≥ 3.10
- `pyautogui`
- `pygetwindow`
- `pyperclip`
- `requests`
- Google Gemini 2.5 Flash API (for `LLM_bot.py`)

---

## Security & Limitations

- Gemini API key should be kept secret.
- Scripts interact with your desktop directly; do not run while performing other tasks.
- WhatsApp automation is only tested on **WhatsApp Desktop**, not WhatsApp Web or mobile.

---

## Repository Structure

```
Whatsapp_Msg_loop_System/
├── LLM_bot.py        # Generates AI-based WhatsApp messages using Gemini
├── Loop_bot.py       # Sends repeated predefined messages
└── README.md         # Documentation and instructions
```

---

## License

This project is **open-source**. Use responsibly. Automating WhatsApp messages may violate WhatsApp’s terms of service.

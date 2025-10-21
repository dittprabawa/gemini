import os
import json
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InvalidArgument, PermissionDenied
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro-latest')

# ANSI color codes
GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

def chat_with_gemini():
    # Check terminal size
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80

    inner_width = terminal_width - 2

    os.system('cls' if os.name == 'nt' else 'clear')

    # Borders
    top_border = f"{RED}╔{'═' * inner_width}╗{RESET}"
    bottom_border = f"{RED}╚{'═' * inner_width}╝{RESET}"

    print(top_border)

    # Title
    title_text = '##DITBOT CLI V0.0.2'
    title_padding = ' ' * max(0, inner_width - len(title_text))
    print(f"{RED}║{YELLOW}{title_text}{title_padding}{RED}║{RESET}")

    # Welcome
    welcome_text = 'Welcome back "radit"'
    welcome_padding = ' ' * max(0, inner_width - len(welcome_text))
    print(f"{RED}║{RESET}{welcome_text}{welcome_padding}{RED}║{RESET}")

    # Workspace
    workspace_text = f'Workspace: {os.getcwd()}'
    workspace_padding = ' ' * max(0, inner_width - len(workspace_text))
    print(f"{RED}║{RESET}{workspace_text}{workspace_padding}{RED}║{RESET}")

    # Tips
    tips_text = 'Tips: ketik /help atau "exit" untuk keluar'
    tips_padding = ' ' * max(0, inner_width - len(tips_text))
    print(f"{RED}║{RESET}{tips_text}{tips_padding}{RED}║{RESET}")

    print(bottom_border)
    print()

    history_file = 'chat_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            messages = json.load(f)
    else:
        messages = []

    chat = None  # Initialize chat variable

    while True:
        try:
            user_input = input(f"{CYAN}> {RESET}").strip()
            if user_input.lower() == 'exit':
                print(f"{GREEN}Goodbye, Radit! 👋{RESET}")
                break

            if user_input == '/save':
                with open(history_file, 'w') as f:
                    json.dump(messages, f)
                print(f"{GREEN}History saved!{RESET}")
                continue
            elif user_input == '/load':
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        messages = json.load(f)
                    print(f"{GREEN}History loaded!{RESET}")
                else:
                    print(f"{RED}No history file found.{RESET}")
                continue

            if user_input.startswith('/code'):
                code_prompt = user_input[6:].strip()
                if not code_prompt:
                    print(f"{RED}Error: Masukkan prompt setelah /code, contoh: /code buat fungsi kalkulator sederhana{RESET}")
                    continue
                full_prompt = f"Generate code for: {code_prompt}. Provide clean, executable code with comments."
                try:
                    if chat is None:
                        chat = model.start_chat(history=[])
                    response = chat.send_message(full_prompt)
                    print(f"{GREEN}Gemini (Code):{RESET} {response.text}")
                except ResourceExhausted:
                    print(f"{RED}Error:{RESET} Rate limit exceeded. Please try again later.")
                except InvalidArgument:
                    print(f"{RED}Error:{RESET} Invalid input for code generation.")
                except PermissionDenied:
                    print(f"{RED}Error:{RESET} API key or permissions issue.")
                except Exception as e:
                    print(f"{RED}Error:{RESET} {str(e)}")
            elif user_input.startswith('/analyze'):
                file_path = user_input[9:].strip()
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        prompt = f"Analyze this text: {content[:1000]}"  # Limit to 1000 chars
                        if chat is None:
                            chat = model.start_chat(history=[])
                        response = chat.send_message(prompt)
                        print(f"{GREEN}Gemini (Analysis):{RESET} {response.text}")
                    except Exception as e:
                        print(f"{RED}Error:{RESET} Failed to read or analyze file: {str(e)}")
                else:
                    print(f"{RED}File not found.{RESET}")
            elif user_input.startswith('/translate'):
                parts = user_input.split(' ', 2)
                if len(parts) >= 3:
                    lang = parts[1]
                    text = parts[2]
                    prompt = f"Translate to {lang}: {text}"
                    try:
                        if chat is None:
                            chat = model.start_chat(history=[])
                        response = chat.send_message(prompt)
                        print(f"{GREEN}Gemini (Translate):{RESET} {response.text}")
                    except ResourceExhausted:
                        print(f"{RED}Error:{RESET} Rate limit exceeded. Please try again later.")
                    except InvalidArgument:
                        print(f"{RED}Error:{RESET} Invalid input for translation.")
                    except PermissionDenied:
                        print(f"{RED}Error:{RESET} API key or permissions issue.")
                    except Exception as e:
                        print(f"{RED}Error:{RESET} {str(e)}")
                else:
                    print(f"{RED}Error:{RESET} Invalid /translate command. Usage: /translate <language> <text>")
            elif user_input.startswith('/help'):
                print(f"{YELLOW}Available commands:{RESET}")
                print(f"  /code <description> - Generate code for the description")
                print(f"  /analyze <file_path> - Analyze text from a file")
                print(f"  /translate <language> <text> - Translate text to the specified language")
                print(f"  /save - Save conversation history")
                print(f"  /load - Load conversation history")
                print(f"  /help - Show this help message")
                print(f"  exit - Exit the chat")
            else:
                # Chat normal
                messages.append({'role': 'user', 'parts': [user_input]})

                try:
                    chat = model.start_chat(history=messages[:-1])  # Exclude current message
                    response = chat.send_message(user_input)
                    assistant_response = response.text

                    print(f"{GREEN}Gemini:{RESET} {assistant_response}")
                    messages.append({'role': 'model', 'parts': [assistant_response]})
                except ResourceExhausted:
                    print(f"{RED}Error:{RESET} Rate limit exceeded. Please try again later.")
                    messages.pop()  # Remove the user message if failed
                except InvalidArgument:
                    print(f"{RED}Error:{RESET} Invalid input.")
                    messages.pop()
                except PermissionDenied:
                    print(f"{RED}Error:{RESET} API key or permissions issue.")
                    messages.pop()
                except Exception as e:
                    print(f"{RED}Error:{RESET} {str(e)}")
                    messages.pop()

        except Exception as e:
            print(f"{RED}Error:{RESET} {str(e)}")

if __name__ == "__main__":
    chat_with_gemini()

import os
import random
import time
import requests
import threading
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text):
    lines = text.strip().splitlines()
    for line in lines:
        print(line.center(80))

ART = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡴⣆⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⣼⣿⡗⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠀⠘⠷⠶⠶⠶⠾⠉⢳⡄⠀⠀⠀⠀⠀⣧⣿⠀⠀⠀⠀⠀
⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⣤⣤⣤⣤⣿⢿⣄⠀⠀⠀⠀
⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠙⣷⡴⠶⣦
⠀⠀⢱⡀⠀⠉⠉⠀⠀⠀⠀⠛⠃⠀⢠⡟⠀⠀⠀⢀⣀⣠⣤⠿⠞⠛⠋
⣠⠾⠋⠙⣶⣤⣤⣤⣤⣤⣀⣠⣤⣾⣿⠴⠶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀
⠛⠒⠛⠉⠉⠀⠀⠀⣴⠟⢃⡴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

class bcolors:
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GRAY_INPUT = '\033[38;5;240m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'

def display_menu():
    clear()
    print_centered(ART)
    color = bcolors.MAGENTA
    print(f"{color}{bcolors.BOLD}1.{bcolors.ENDC} Start")
    print(f"{color}{bcolors.BOLD}2.{bcolors.ENDC} Settings")
    print(f"{color}{bcolors.BOLD}3.{bcolors.ENDC} Credits")
    print(f"{bcolors.RED}{bcolors.BOLD}4.{bcolors.ENDC} Exit\n")

def cool_header(text):
    color = bcolors.MAGENTA
    border = f"{color}{bcolors.BOLD}* {text} *{bcolors.ENDC}"
    print(border + "\n")

def get_settings(casing, include_numbers, length):
    clear()
    cool_header("settings")
    print(f"Casing (upper/lower/mix): {bcolors.MAGENTA}{casing}{bcolors.ENDC}")
    print(f"Include numbers (y/n): {bcolors.MAGENTA}{'y' if include_numbers else 'n'}{bcolors.ENDC}")
    print(f"Username length (5-20): {bcolors.MAGENTA}{length}{bcolors.ENDC}\n")

    while True:
        new_casing = input(f"{bcolors.GRAY_INPUT}Set casing (upper/lower/mix) or press ENTER to keep: {bcolors.ENDC}").strip().lower()
        if new_casing in ['upper', 'lower', 'mix', '']:
            if new_casing != '':
                casing = new_casing
            break

    while True:
        new_num = input(f"{bcolors.GRAY_INPUT}Include numbers? (y/n) or press ENTER to keep: {bcolors.ENDC}").strip().lower()
        if new_num in ['y', 'n', '']:
            if new_num != '':
                include_numbers = (new_num == 'y')
            break

    while True:
        new_len = input(f"{bcolors.GRAY_INPUT}Username length (5-20) or press ENTER to keep: {bcolors.ENDC}").strip()
        if new_len == '':
            break
        elif new_len.isdigit() and 5 <= int(new_len) <= 20:
            length = int(new_len)
            break

    print(f"\n{bcolors.MAGENTA}Settings saved!{bcolors.ENDC}")
    time.sleep(0.5)
    return casing, include_numbers, length

def generate_username(length, casing, include_numbers):
    chars = 'abcdefghijklmnopqrstuvwxyz'
    if casing == 'upper':
        chars = chars.upper()
    elif casing == 'mix':
        chars += chars.upper()
    if include_numbers:
        chars += '0123456789'
    return ''.join(random.choices(chars, k=length))

def is_available(username, user_agents):
    headers = {'User-Agent': random.choice(user_agents)}
    url = f'https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday=2000-01-01'
    try:
        resp = requests.get(url, headers=headers, timeout=2)
        if resp.status_code != 200:
            return False
        data = resp.json()
        if data.get("code") == 1 and "already in use" in data.get("message", "").lower():
            return False
        if data.get("code") == 0:
            return True
        return False
    except:
        return False
def save_username(username, path='pulls.txt'):
    try:
        usernames = set()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                usernames = set(f.read().splitlines())

        if username in usernames:
            return False

        usernames.add(username)
        with open(path, 'w', encoding='utf-8') as f:
            for name in sorted(usernames):
                f.write(name + '\n')
        return True
    except Exception:
        return False

def countdown(casing, include_numbers, length):
    clear()
    print(f"Casing: {bcolors.MAGENTA}{casing}{bcolors.ENDC} | Include numbers: {bcolors.MAGENTA}{'y' if include_numbers else 'No'}{bcolors.ENDC} | Length: {bcolors.MAGENTA}{length}{bcolors.ENDC}")
    print(f"Starting in 3 seconds | {bcolors.RED}press ENTER to stop{bcolors.ENDC}\n")
    for i in range(3, 0, -1):
        print(f"{bcolors.MAGENTA}{i}...{bcolors.ENDC}")
        time.sleep(1)
    print()

def scanner_loop(casing, include_numbers, length):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
    ]
    
    stop_flag = False
    input_thread = None

    def check_username(username):
        if is_available(username, user_agents):
            if save_username(username):
                print(f"{bcolors.GREEN}✓ {username}{bcolors.ENDC}")  
        else:
           print(f"{bcolors.RED}✗ {username}{bcolors.ENDC}")

    def input_listener():
        nonlocal stop_flag
        input()
        stop_flag = True

    countdown(casing, include_numbers, length)
    if stop_flag:
        return

    input_thread = threading.Thread(target=input_listener, daemon=True)
    input_thread.start()

    try:
        while not stop_flag:
            username = generate_username(length, casing, include_numbers)
            t = threading.Thread(target=check_username, args=(username,))
            t.start()
            time.sleep(0.05)
    except KeyboardInterrupt:
        stop_flag = True

    print(f"\n{bcolors.MAGENTA}Returning to menu...{bcolors.ENDC}")
    time.sleep(1.5)

def credits():
    clear()
    cool_header("credits")
    print("-Free for use-")
    print("Made by github.com/stvmp")
    print("Uses Roblox's API to check the availability of usernames.\n")
    print(f"{bcolors.GRAY_INPUT}Press ENTER to return to menu...{bcolors.ENDC}")
    input()

def main():
    casing = 'lower'
    include_numbers = True
    length = 5
    while True:
        display_menu()
        try:
            choice = input(f"{bcolors.GRAY_INPUT}Select option: {bcolors.ENDC}").strip()
            if choice == '1':
                scanner_loop(casing, include_numbers, length)
            elif choice == '2':
                casing, include_numbers, length = get_settings(casing, include_numbers, length)
            elif choice == '3':
                credits()
            elif choice == '4':
                clear()
                sys.exit()
            else:
                print(f"{bcolors.RED}Invalid choice.{bcolors.ENDC}")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()

if __name__ == '__main__':
    main()
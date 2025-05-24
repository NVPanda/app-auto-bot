import time
import pyautogui
import pytesseract
import os
from PIL import Image
from dotenv import load_dotenv
from rapidfuzz import fuzz
import tkinter as tk
from tkinter import messagebox
import threading

# Variável de controle
executando = {"valor": False}


SITE = "olx.com.br"
TARGET = "celular e smartphones"

# Interface
class BotOLXInterface:
    def __init__(self, master):
        self.master = master
        master.title("Bot OLX")
        master.geometry("400x300")
        master.resizable(False, False)

        # Mensagem
        tk.Label(master, text="Mensagem:").pack()
        self.msg_entry = tk.Entry(master, width=40)
        self.msg_entry.pack()

        # Preço mínimo
        tk.Label(master, text="Preço Mínimo:").pack()
        self.preco_min_entry = tk.Entry(master)
        self.preco_min_entry.pack()

        # Preço máximo
        tk.Label(master, text="Preço Máximo:").pack()
        self.preco_max_entry = tk.Entry(master)
        self.preco_max_entry.pack()

        # Botão iniciar/parar
        self.botao = tk.Button(master, text="Iniciar", command=self.toggle_bot)
        self.botao.pack(pady=10)

    def toggle_bot(self):
        if not executando["valor"]:
            try:
                float(self.preco_min_entry.get())
                float(self.preco_max_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Preços devem ser números.")
                return

            if not self.msg_entry.get():
                messagebox.showerror("Erro", "A mensagem deve ser preenchida.")
                return

            executando["valor"] = True
            self.botao.config(text="Parar")

            threading.Thread(target=capturar_e_ler_preco,
                             args=(self.msg_entry.get(),
                                   float(self.preco_min_entry.get()),
                                   float(self.preco_max_entry.get())), daemon=True).start()
        else:
            executando["valor"] = False
            self.botao.config(text="Iniciar")

# Função de automação OLX — Chamada pelo botão
def abrir_site_e_pesquisar():
    pyautogui.PAUSE = 1.0

    pyautogui.press("win")
    time.sleep(2)
    pyautogui.write("Firefox", interval=0.1)
    pyautogui.press("enter")
    time.sleep(10)

    # Abrindo o navegador
    x_nav, y_nav, w_nav, h_nav = 49, 34, 648, 135
    screenshot_nav = pyautogui.screenshot(region=(x_nav,y_nav,w_nav,h_nav))
    data_nav = pytesseract.image_to_string(screenshot_nav,output_type=pytesseract.Output.DICT)


    for i in range(len(data_nav)):

        palavra = data_nav["text"][i].strip()
        similaridade = fuzz.ratio(palavra.lower(), "Pesquisar com Google ou introduzir endereço") #  qual a similaridade da string

        if similaridade >= 70:  # Aceita palavras próximas como "filt", "fitro", etc.
            text_x = int(data_nav["left"][i])
            text_y = int(data_nav["top"][i])
            text_w = int(data_nav["width"][i])
            text_h = int(data_nav["height"][i])

            real_x = x_nav + text_x + text_w // 2
            real_y = y_nav + text_y + text_h // 2

            pyautogui.click(real_x, real_y)
            pyautogui.sleep(5)
            pyautogui.click(x=364, y=363)
            pyautogui.sleep(1)
            pyautogui.write(SITE, interval=0.1)
           
        
        else:
             # Acessando o site
            pyautogui.sleep(3)
            pyautogui.hotkey('ctrl', 'l') 

            pyautogui.write("olx.com.br", interval=0.1)
            pyautogui.press("enter")
            pyautogui.sleep(20)


    pyautogui.click(x=176, y=207)
    time.sleep(7)
    pyautogui.write(TARGET, interval=0.05)
    pyautogui.press("enter")
    time.sleep(25)

    pyautogui.click(x=93, y=707)
    pyautogui.click(x=267, y=418)
    time.sleep(7)
    pyautogui.click(x=802, y=307)
    pyautogui.scroll(10)
    pyautogui.click(x=972, y=703)
    pyautogui.scroll(-4)
    time.sleep(3)

# Loop principal do bot
def capturar_e_ler_preco(msg, preco_min, preco_max):
    abrir_site_e_pesquisar()

    while executando["valor"]:
        try:
            x, y, w, h = 311, 191, 990, 619
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
            texto = pytesseract.image_to_string(screenshot)

            # Verifica se o preço alvo está na imagem
            for alvo in [str(int(preco_min)), str(int(preco_max))]:
                if alvo in texto:
                    screenshot.save("img.png")
                    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

                    for i in range(len(data["text"])):
                        texto_palavra = data["text"][i].replace(" ", "").replace("R$", "").replace(",", "").replace(".", "")
                        if texto_palavra == alvo:
                            text_x = int(data["left"][i])
                            text_y = int(data["top"][i])
                            text_w = int(data["width"][i])
                            text_h = int(data["height"][i])

                            real_x = x + text_x + text_w // 2
                            real_y = y + text_y + text_h // 2
                            pyautogui.click(real_x, real_y)
                            time.sleep(5)

                            # Tentativa de clicar no botão de chat
                            x_chat, y_chat, w_chat, h_chat = 690, 191, 951, 688
                            screenshot_chat = pyautogui.screenshot(region=(x_chat, y_chat, w_chat, h_chat))
                            texto_chat = pytesseract.image_to_string(screenshot_chat)

                            if "Chat" in texto_chat:
                                data_chat = pytesseract.image_to_data(screenshot_chat, output_type=pytesseract.Output.DICT)
                                for j in range(len(data_chat["text"])):
                                    if "Chat" in data_chat["text"][j]:
                                        cx = int(data_chat["left"][j])
                                        cy = int(data_chat["top"][j])
                                        cw = int(data_chat["width"][j])
                                        ch = int(data_chat["height"][j])
                                        real_cx = x_chat + cx + cw // 2
                                        real_cy = y_chat + cy + ch // 2
                                        pyautogui.click(real_cx, real_cy)
                                        time.sleep(3)

                                        # Escrevendo mensagem
                                        pyautogui.write(msg)
                                        pyautogui.press("enter")
                                        break
                            break
        except Exception as e:
            print(f"[Erro] {e}")
        time.sleep(10)

# Inicializa interface
if __name__ == "__main__":
    root = tk.Tk()
    app = BotOLXInterface(root)
    root.mainloop()

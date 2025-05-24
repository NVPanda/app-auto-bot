import time
import pyautogui
import pytesseract
import os
from PIL import Image
from dotenv import load_dotenv
from rapidfuzz import fuzz


executando = {"valor": False}

# Carregando variáveis de ambiente
root_project_path = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(root_project_path, "../../.env.local")
load_dotenv(dotenv_path)


def abrir_site_e_pesquisar():
    pyautogui.PAUSE = 1.0     
    
    # Entrando no navegador
    pyautogui.press("win")
    pyautogui.sleep(3)
    pyautogui.write("Firefox", interval=0.09)
    pyautogui.press("enter")
    pyautogui.sleep(10)

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

            real_x = x_filtro + text_x + text_w // 2
            real_y = y_filtro + text_y + text_h // 2

            pyautogui.click(real_x, real_y)
            pyautogui.sleep(5)
            pyautogui.click(x=364, y=363)
            pyautogui.sleep(1)
            pyautogui.write(os.getenv("SITE"), interval=0.1)
           
        
        else:
             # Acessando o site
            pyautogui.press("tab")
            pyautogui.sleep(0.3)

            pyautogui.press("tab")
            pyautogui.sleep(0.3)

            pyautogui.press("tab")
            pyautogui.sleep(0.3)

            pyautogui.press("tab")
            pyautogui.sleep(0.3)

            pyautogui.press("tab")
            pyautogui.sleep(0.3)

            pyautogui.press("tab")
            pyautogui.sleep(0.3)

            pyautogui.press("tab")
            pyautogui.sleep(0.3)

            pyautogui.press("tab")
            pyautogui.sleep(0.3)


            pyautogui.write(os.getenv("SITE"), interval=0.1)
            pyautogui.press("enter")
            pyautogui.sleep(15)


   
    # Pesquisando produto
    pyautogui.click(x=176, y=207)
    pyautogui.sleep(7)
    #celular e smartphones
    pyautogui.write(os.getenv("TARGET"), interval=0.01) 
    pyautogui.press("enter")
    pyautogui.sleep(25)


    # Buscando campo filtro | BTN
    filtro_encontrado = False
    x_filtro, y_filtro, w_filtro, h_filtro = 23, 249, 972, 422
    screenshot_filtro = pyautogui.screenshot(region=(x_filtro, y_filtro, w_filtro, h_filtro))
    data_filtro = pytesseract.image_to_data(screenshot_filtro, output_type=pytesseract.Output.DICT)

        
    # Cálculo de similaridade com a palavra "filtro"
    for i in range(len(data_filtro["text"])):
        palavra = data_filtro["text"][i].strip().replace(" ", "").replace("R$", "").replace(",", "").replace(".", "")
        similaridade = fuzz.ratio(palavra.lower(), "filtro")

        if similaridade >= 70:  # Aceita palavras próximas como "filt", "fitro", etc.
            text_x = int(data_filtro["left"][i])
            text_y = int(data_filtro["top"][i])
            text_w = int(data_filtro["width"][i])
            text_h = int(data_filtro["height"][i])

            real_x = x_filtro + text_x + text_w // 2
            real_y = y_filtro + text_y + text_h // 2

            pyautogui.click(real_x, real_y)
            pyautogui.sleep(5)
            pyautogui.click(x=364, y=363)
            pyautogui.sleep(1)
            pyautogui.scroll(-9)
            filtro_encontrado = True
           

    # Caso não tenha encontrado "Filtro", aplicar manualmente
    if not filtro_encontrado:
        pyautogui.keyDown('ctrl')
        pyautogui.hotkey('ctrl', '-')
        pyautogui.hotkey('ctrl', '-')
        pyautogui.hotkey('ctrl', '-')
        pyautogui.sleep(5)

        # Levando o mouse para a área de filtro
        pyautogui.moveTo(x=85, y=352)
        pyautogui.sleep(3)

        # Procurando Inputs precos
        x_width, y_width, w_width, h_width = 14, 446, 176, 489
        screenshot_width = pyautogui.screenshot(region=(x_width, y_width, w_width, h_width))
        data_width = pytesseract.image_to_data(screenshot_width, output_type=pytesseract.Output.DICT)

        # Cálculo de similaridade com a palavra "filtro"
        for i in range(len(data_width["text"])):
            price = data_filtro["text"][i].strip()
            similaridade = fuzz.ration(price, "Min")

            if similaridade >= 70:

                # Local onde o btn preço esta
                text_x = int(data_width["left"][i])
                text_y = int(data_width["left"][i])
                text_w = int(data_width["left"][i])
                text_h = int(data_width["left"][i])


                # clicando no campo
                real_x = x_filtro + text_x + text_w // 2
                real_y = y_filtro + text_y + text_h // 2
                pyautogui.click(real_x, real_y)
                break



   
    # click em não aceita troca
    pyautogui.click(x=93, y=707)
    #Busca
    pyautogui.click(x=267, y=418)
    pyautogui.sleep(7)
    pyautogui.click(x=802, y=307)
    pyautogui.scroll(10)

    # Modo grade + scroll
    pyautogui.click(x=972, y=703)
    pyautogui.scroll(-4)
    pyautogui.sleep(3)







def capturar_e_ler_preco(page):
    logs = []
    abrir_site_e_pesquisar()
    while executando["valor"]:

        try:
            # Região onde ficam os anúncios
            x, y, w, h = 311, 191, 990, 619
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
            texto = pytesseract.image_to_string(screenshot)
            logs.append("Texto capturado: " + texto)

            if any(valor in texto for valor in ["1.500"]):
                logs.append("💰 Produto com valor desejado encontrado!")
                screenshot.save("img.png")

                data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

                for i in range(len(data["text"])):
                    texto_palavra = data["text"][i].replace(" ", "").replace("R$", "").replace(",", "").replace(".", "")

                    if texto_palavra == "1500":
                        text_x = int(data["left"][i])
                        text_y = int(data["top"][i])
                        text_w = int(data["width"][i])
                        text_h = int(data["height"][i])

                        real_x = x + text_x + text_w // 2
                        real_y = y + text_y + text_h // 2

                        logs.append(f"🖱️ Clicando no anúncio: {real_x}, {real_y}")
                        pyautogui.click(real_x, real_y)
                        pyautogui.sleep(5)
                        break

                pyautogui.scroll(4)
                pyautogui.sleep(5)

                x_chat, y_chat, w_chat, h_chat = 690, 191, 951, 688
                screenshot_chat = pyautogui.screenshot(region=(x_chat, y_chat, w_chat, h_chat))
                texto_chat = pytesseract.image_to_string(screenshot_chat)
                logs.append("Texto capturado (chat): " + texto_chat)

                if "Chat" in texto_chat:
                    logs.append("✅ Botão 'Chat' encontrado!")
                    data_chat = pytesseract.image_to_data(screenshot_chat, output_type=pytesseract.Output.DICT)

                    for i in range(len(data_chat["text"])):
                        if "Chat" in data_chat["text"][i]:
                            cx = int(data_chat["left"][i])
                            cy = int(data_chat["top"][i])
                            cw = int(data_chat["width"][i])
                            ch = int(data_chat["height"][i])

                            real_cx = x_chat + cx + cw // 2
                            real_cy = y_chat + cy + ch // 2

                            logs.append(f"🖱️ Clicando no botão Chat: {real_cx}, {real_cy}")
                            pyautogui.click(real_cx, real_cy)
                            time.sleep(4)

                        

                            x_campo, y_campo, w_campo, h_campo = 516, 275, 939, 748
                            screenshot_input = pyautogui.screenshot(region=(x_campo, y_campo, w_campo, h_campo))
                            input_chat = pytesseract.image_to_string(screenshot_input)
                            logs.append("Input area capturado: " + input_chat)

                            if "Digite uma mensagem...." in input_chat:
                                logs.append("Campo input encontrado.")
                                data_input = pytesseract.image_to_data(screenshot_input, output_type=pytesseract.Output.DICT)

                                for i in range(len(data_input["text"])):
                                    if "Chat" in data_input["text"][i]:
                                        cx = int(data_input["left"][i])
                                        cy = int(data_input["top"][i])
                                        cw = int(data_input["width"][i])
                                        ch = int(data_input["height"][i])

                                        real_cx = x_campo + cx + cw // 2
                                        real_cy = y_campo + cy + ch // 2

                                        logs.append(f"🖱️ Clicando no botão Chat: {real_cx}, {real_cy}")
                                        pyautogui.click(real_cx, real_cy)
                                        time.sleep(3)
                                        pyautogui.write("Ola")
                                        break
                            
                            else:
                                pyautogui.hotkey('alt', 'left')

                                logs.append("❌ Input do chat não foi encontrado na imagem.")
                    else:
                        logs.append("❌ OCR reconheceu 'Chat', mas não conseguiu extrair posição.")
                else:
                    logs.append("❌ Texto 'Chat' não foi detectado na imagem.")
            else:
                logs.append("❌ Valor desejado não encontrado na imagem.")

        except Exception as e:
            logs.append(f"Erro ao capturar/leitura OCR: {e}")
            logs.append("Talvez esteja faltando o pacote `gnome-screenshot`.")
            logs.append("Use: sudo apt install gnome-screenshot")

        return logs

text_w // 2

    real_y = y + text_y + text_h // 2
    pyautogui.click(real_x, real_y)
    pyautogui.sleep(5)

    # tentativa de clicar no botão de chat
    x_chat, y_chat, w_chat, h_chat = 690, 191, 951, 688
    screenshot_chat = pyautogui.screenshot(region=(x_chat, y_chat, w_chat, h_chat))
    texto_chat = pytesseract.image_to_string(screenshot_chat)
    logs.append("Texto capturado (chat): " + texto_chat)
    if "Chat" in texto_chat:
        logs.append("✅ Botão 'Chat' encontrado!")
        data_chat = pytesseract.image_to_data(screenshot_chat, output_type=pytesseract.Output.DICT)

        for i in range(len(data_chat["text"])):
            if "Chat" in data_chat["text"][i]:
                cx = int(data_chat["left"][i])
                cy = int(data_chat["top"][i])
                cw = int(data_chat["width"][i])
                ch = int(data_chat["height"][i])

                real_cx = x_chat + cx + cw // 2
                real_cy = y_chat + cy + ch // 2

                logs.append(f"🖱️ Clicando no botão Chat: {real_cx}, {real_cy}")
                pyautogui.click(real_cx, real_cy)
                time.sleep(4)

                # Capturando a área do chat
                x_campo, y_campo, w_campo, h_campo = 516, 275, 939, 748
                screenshot_input = pyautogui.screenshot(region=(x_campo, y_campo, w_campo, h_campo))
                input_chat = pytesseract.image_to_string(screenshot_input)
                logs.append("Input area capturado: " + input_chat)
                if "Digite uma mensagem...." in input_chat:
                    logs.append("Campo input encontrado.")
                    data_input = pytesseract.image_to_data(screenshot_input, output_type=pytesseract.Output.DICT)

                    for i in range(len(data_input["text"])):
                        if "Chat" in data_input["text"][i]:
                            cx = int(data_input["left"][i])
                            cy = int(data_input["top"][i])
                            cw = int(data_input["width"][i])
                            ch = int(data_input["height"][i])

                            real_cx = x_campo + cx + cw // 2
                            real_cy = y_campo + cy + ch // 2

                            logs.append(f"🖱️ Clicando no botão Chat: {real_cx}, {real_cy}")
                            pyautogui.click(real_cx, real_cy)
                            time.sleep(3)
                            pyautogui.write("Ola")
                            break
                else:
                    pyautogui.hotkey('alt', 'left')
                    logs.append("❌ Input do chat não foi encontrado na imagem.")
            else:
                logs.append("❌ OCR reconheceu 'Chat', mas não conseguiu extrair posição.")
    else:
        logs.append("❌ Texto 'Chat' não foi detectado na imagem.")
    else:
        logs.append("❌ Valor desejado não encontrado na imagem.")
    except Exception as e:
        logs.append(f"Erro ao capturar/leitura OCR: {e}")
        logs.append("Talvez esteja faltando o pacote `gnome-screenshot`.")
        logs.append("Use: sudo apt install gnome-screenshot")
    return logs
# Exemplo de uso
if __name__ == "__main__":
    page = 1
    logs = capturar_e_ler_preco(page)
    for log in logs:
        print(log)
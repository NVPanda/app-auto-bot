import time
import pyautogui
import pytesseract
import os
from PIL import Image
from dotenv import load_dotenv
from rapidfuzz import fuzz
import logging

# Configuração de logging para exibir mensagens em tempo real no console.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Variável global de controle para o loop
executando = {"valor": False}

# Carregando variáveis de ambiente
root_project_path = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(root_project_path, "../../.env.local")
load_dotenv(dotenv_path)
logger.debug("Variáveis de ambiente carregadas do caminho: %s", dotenv_path)


def abrir_site_e_pesquisar():
    """
    Abre o navegador (Firefox) e navega até o site definido na variável SITE;
    após, faz a pesquisa de produto definido em TARGET e realiza ajustes na página,
    buscando elementos como o campo filtro.
    """
    logger.info("Iniciando a abertura do site e pesquisa...")
    pyautogui.PAUSE = 1.0     
    # Abrindo o navegador:
    pyautogui.press("win")
    time.sleep(3)
    pyautogui.write("Firefox", interval=0.09)
    pyautogui.press("enter")
    time.sleep(10)

    # Captura da região do navegador (banda de endereço)
    x_nav, y_nav, w_nav, h_nav = 49, 34, 648, 135
    screenshot_nav = pyautogui.screenshot(region=(x_nav, y_nav, w_nav, h_nav))
    # Utilizamos image_to_data para obter informações de posição
    data_nav = pytesseract.image_to_data(screenshot_nav, output_type=pytesseract.Output.DICT)
    logger.debug("OCR realizado na região do navegador.")

    # Procura pelo campo de pesquisa
    found_search = False
    for i in range(len(data_nav["text"])):
        palavra = data_nav["text"][i].strip()
        similaridade = fuzz.ratio(palavra.lower(), "pesquisar com google ou introduzir endereço")
        logger.debug("Similaridade para '%s': %d", palavra, similaridade)
        if similaridade >= 70:
            text_x = int(data_nav["left"][i])
            text_y = int(data_nav["top"][i])
            text_w = int(data_nav["width"][i])
            text_h = int(data_nav["height"][i])
            # Usa a região do navegador para referenciar a posição
            real_x = x_nav + text_x + text_w // 2
            real_y = y_nav + text_y + text_h // 2
            pyautogui.click(real_x, real_y)
            time.sleep(5)
            pyautogui.click(x=364, y=363)
            time.sleep(1)
            site = os.getenv("SITE", "")
            pyautogui.write(site, interval=0.1)
            found_search = True
            logger.info("Campo de pesquisa encontrado e preenchido com SITE: %s", site)
            break

    if not found_search:
        # Se o campo não for encontrado, utiliza navegação por TABs
        for _ in range(8):
            pyautogui.press("tab")
            time.sleep(0.3)
        site = os.getenv("SITE", "")
        pyautogui.write(site, interval=0.1)
        pyautogui.press("enter")
        time.sleep(15)
        logger.info("Site acessado via método alternativo de TABs.")

    # Pesquisando o produto
    pyautogui.click(x=176, y=207)
    time.sleep(7)
    target = os.getenv("TARGET", "")
    pyautogui.write(target, interval=0.01) 
    pyautogui.press("enter")
    time.sleep(25)
    logger.info("Produto '%s' buscado.", target)

    # Procura pelo campo Filtro na tela
    filtro_encontrado = False
    x_filtro, y_filtro, w_filtro, h_filtro = 23, 249, 972, 422
    screenshot_filtro = pyautogui.screenshot(region=(x_filtro, y_filtro, w_filtro, h_filtro))
    data_filtro = pytesseract.image_to_data(screenshot_filtro, output_type=pytesseract.Output.DICT)
    logger.debug("OCR realizado na região de filtro.")

    for i in range(len(data_filtro["text"])):
        palavra = data_filtro["text"][i].strip().replace(" ", "").replace("R$", "").replace(",", "").replace(".", "")
        similaridade = fuzz.ratio(palavra.lower(), "filtro")
        logger.debug("Similaridade para filtro '%s': %d", palavra, similaridade)
        if similaridade >= 70:
            text_x = int(data_filtro["left"][i])
            text_y = int(data_filtro["top"][i])
            text_w = int(data_filtro["width"][i])
            text_h = int(data_filtro["height"][i])
            real_x = x_filtro + text_x + text_w // 2
            real_y = y_filtro + text_y + text_h // 2
            pyautogui.click(real_x, real_y)
            time.sleep(5)
            pyautogui.click(x=364, y=363)
            time.sleep(1)
            pyautogui.scroll(-9)
            filtro_encontrado = True
            logger.info("Campo filtro encontrado e acionado.")
            break

    if not filtro_encontrado:
        # Ajustes manuais caso o filtro não seja encontrado
        pyautogui.keyDown('ctrl')
        pyautogui.hotkey('ctrl', '-')
        pyautogui.hotkey('ctrl', '-')
        pyautogui.hotkey('ctrl', '-')
        time.sleep(5)
        pyautogui.moveTo(x=85, y=352)
        time.sleep(3)
        x_width, y_width, w_width, h_width = 14, 446, 176, 489
        screenshot_width = pyautogui.screenshot(region=(x_width, y_width, w_width, h_width))
        data_width = pytesseract.image_to_data(screenshot_width, output_type=pytesseract.Output.DICT)
        logger.debug("OCR realizado na região de inputs de preço.")
        for i in range(len(data_width["text"])):
            price = data_width["text"][i].strip()
            similaridade = fuzz.ratio(price, "min")
            logger.debug("Similaridade para preço '%s': %d", price, similaridade)
            if similaridade >= 70:
                text_x = int(data_width["left"][i])
                text_y = int(data_width["top"][i])
                text_w = int(data_width["width"][i])
                text_h = int(data_width["height"][i])
                real_x = x_width + text_x + text_w // 2
                real_y = y_width + text_y + text_h // 2
                pyautogui.click(real_x, real_y)
                logger.info("Campo de preço identificado e clicado.")
                break

    # Interações adicionais: desativar opção de troca, ajustes de visual...
    pyautogui.click(x=93, y=707)
    pyautogui.click(x=267, y=418)
    time.sleep(7)
    pyautogui.click(x=802, y=307)
    pyautogui.scroll(10)
    pyautogui.click(x=972, y=703)
    pyautogui.scroll(-4)
    time.sleep(3)
    logger.info("Procedimentos iniciais de interação com a página concluídos.")


def capturar_e_ler_preco(page):
    """
    Abre o site, pesquisa o produto e tenta capturar e interagir com o anúncio
    conforme o valor desejado. Retorna uma lista de logs com as ações efetuadas.
    """
    logs = []
    try:
        abrir_site_e_pesquisar()
        # Ativa o modo de captura
        executando["valor"] = True
        logger.info("Iniciando captura e leitura de preço.")

        # Exemplo de loop; para efeito de teste, é realizada uma única iteração.
        while executando["valor"]:
            try:
                # Define a área onde ficam os anúncios
                x, y, w, h = 311, 191, 990, 619
                screenshot = pyautogui.screenshot(region=(x, y, w, h))
                texto = pytesseract.image_to_string(screenshot)
                log_entry = "Texto capturado: " + texto
                logs.append(log_entry)
                logger.debug(log_entry)

                if "1.500" in texto:
                    msg = "💰 Produto com valor desejado encontrado!"
                    logs.append(msg)
                    logger.info(msg)
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
                            click_msg = f"🖱️ Clicando no anúncio: {real_x}, {real_y}"
                            logs.append(click_msg)
                            logger.info(click_msg)
                            pyautogui.click(real_x, real_y)
                            time.sleep(5)
                            break

                    pyautogui.scroll(4)
                    time.sleep(5)

                    # Tenta interagir com o chat
                    x_chat, y_chat, w_chat, h_chat = 690, 191, 951, 688
                    screenshot_chat = pyautogui.screenshot(region=(x_chat, y_chat, w_chat, h_chat))
                    texto_chat = pytesseract.image_to_string(screenshot_chat)
                    logs.append("Texto capturado (chat): " + texto_chat)
                    logger.debug("Texto capturado (chat): " + texto_chat)

                    if "Chat" in texto_chat:
                        msg = "✅ Botão 'Chat' encontrado!"
                        logs.append(msg)
                        logger.info(msg)
                        data_chat = pytesseract.image_to_data(screenshot_chat, output_type=pytesseract.Output.DICT)
                        for i in range(len(data_chat["text"])):
                            if "Chat" in data_chat["text"][i]:
                                cx = int(data_chat["left"][i])
                                cy = int(data_chat["top"][i])
                                cw = int(data_chat["width"][i])
                                ch = int(data_chat["height"][i])
                                real_cx = x_chat + cx + cw // 2
                                real_cy = y_chat + cy + ch // 2
                                chat_click_msg = f"🖱️ Clicando no botão Chat: {real_cx}, {real_cy}"
                                logs.append(chat_click_msg)
                                logger.info(chat_click_msg)
                                pyautogui.click(real_cx, real_cy)
                                time.sleep(4)
                                # Captura a área do input do chat
                                x_campo, y_campo, w_campo, h_campo = 516, 275, 939, 748
                                screenshot_input = pyautogui.screenshot(region=(x_campo, y_campo, w_campo, h_campo))
                                input_chat = pytesseract.image_to_string(screenshot_input)
                                logs.append("Input area capturado: " + input_chat)
                                logger.debug("Input area capturado: " + input_chat)
                                if "Digite uma mensagem" in input_chat:
                                    logs.append("Campo input encontrado.")
                                    logger.info("Campo input encontrado.")
                                    data_input = pytesseract.image_to_data(screenshot_input, output_type=pytesseract.Output.DICT)
                                    for j in range(len(data_input["text"])):
                                        if "Chat" in data_input["text"][j]:
                                            cx = int(data_input["left"][j])
                                            cy = int(data_input["top"][j])
                                            cw = int(data_input["width"][j])
                                            ch = int(data_input["height"][j])
                                            real_cx = x_campo + cx + cw // 2
                                            real_cy = y_campo + cy + ch // 2
                                            chat_input_msg = f"🖱️ Clicando no campo de chat: {real_cx}, {real_cy}"
                                            logs.append(chat_input_msg)
                                            logger.info(chat_input_msg)
                                            pyautogui.click(real_cx, real_cy)
                                            time.sleep(3)
                                            pyautogui.write("Ola")
                                            break
                                else:
                                    pyautogui.hotkey('alt', 'left')
                                    logs.append("❌ Input do chat não foi encontrado na imagem.")
                                    logger.warning("❌ Input do chat não foi encontrado na imagem.")
                    else:
                        logs.append("❌ Texto 'Chat' não foi detectado na imagem.")
                        logger.warning("❌ Texto 'Chat' não foi detectado na imagem.")
                else:
                    logs.append("❌ Valor desejado não encontrado na imagem.")
                    logger.debug("❌ Valor desejado não encontrado na imagem.")
            except Exception as e:
                error_msg = f"Erro ao capturar/leitura OCR: {e}"
                logs.append(error_msg)
                logs.append("Talvez esteja faltando o pacote `gnome-screenshot`.")
                logs.append("Use: sudo apt install gnome-screenshot")
                logger.exception(error_msg)
                break  # Sai do loop caso haja erro
            # Para este exemplo, saímos após uma iteração. Remova o break para um loop contínuo.
            break
    except Exception as outer_e:
        error_msg = f"Erro geral na captura e leitura: {outer_e}"
        logs.append(error_msg)
        logger.exception(error_msg)
    return logs


if __name__ == "__main__":
    # Executa a função de captura e leitura e imprime os logs no terminal.
    logs = capturar_e_ler_preco(page=1)
    for entry in logs:
        print(entry)
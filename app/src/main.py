from utils.callbacks import youchangechoice
from utils.appbar import create_bottom_appbar
from utils.tabsnav import build_tabs
from flet import *
import flet

import os
import sys
import logging
from dotenv import load_dotenv

# Configuração do logging para exibir mensagens em tempo real no console
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Registra exceções não capturadas para que também sejam logadas
def excepthook(exc_type, exc_value, exc_traceback):
    logger.exception("Exceção não capturada:", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = excepthook

def main(page: Page) -> None:
    try:
        # Configuração básica da página
        page.bgcolor = "#121212"
        page.title = "Auto Bot"
        page.padding = 0
        page.spacing = 0
        page.scroll = "auto"
        page.window.width = 500
        page.window.height = 500
        page.maximizable = False

        # Carrega as variáveis de ambiente antes das outras configurações que possam depender delas
        root_project_path = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(root_project_path, "../../.env.local")
        load_dotenv(dotenv_path)
        logger.debug("Variáveis de ambiente carregadas do caminho: %s", dotenv_path)

        # Criação do app bar com layout otimizado
        mybar = Container(
            width=float("inf"),
            height=63,
            padding=padding.symmetric(horizontal=10, vertical=20),
            margin=margin.only(top=12),
            gradient=LinearGradient(
                begin=alignment.top_left,
                end=alignment.bottom_right,
                colors=["#fc4795", "#7c59f0"]
            ),
            border_radius=border_radius.vertical(bottom=30),
            shadow=BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color="#fc4795",
            ),
            content=Row(
                vertical_alignment=CrossAxisAlignment.CENTER,
                spacing=10,
                height=10,
                controls=[
                    Icon(name=Icons.ANDROID, color=Colors.WHITE, size=24),
                    Text("AutoBot", color=Colors.WHITE, size=20, weight="bold")
                ],
            )
        )
        logger.debug("App bar criado com sucesso.")

        # Criação da seção de conteúdo dinâmico
        content_section = Column(expand=True, alignment="center", spacing=20)
        logger.debug("Seção de conteúdo criada.")

        # Configuração do local do botão de ação flutuante
        page.floating_action_button_location = FloatingActionButtonLocation.CENTER_DOCKED

        # Inicializa a barra de navegação (tabs) na parte inferior
        mytabs = create_bottom_appbar(page, content_section)
        logger.debug("Barra de navegação (tabs) inicializada.")

        # Organização do layout principal da página
        page.add(
            Column(
                [
                    mybar,
                    Container(
                        expand=True,
                        alignment=alignment.top_center,
                        padding=padding.all(20),
                        content=content_section,
                    )
                ],
                expand=True
            )
        )
        logger.info("Layout da página montado com sucesso.")

        # Inicializa a aba padrão manualmente usando objeto fake otimizado
        class FakeControl:
            __slots__ = ("tabs", "selected_index")
            def __init__(self):
                self.tabs = [type("Tab", (), {"text": "Home"})()]
                self.selected_index = 0

        fake_event = type("Event", (), {"control": FakeControl()})()
        youchangechoice(fake_event, page, content_section)
        logger.info("Aba padrão inicializada.")

    except Exception as err:
        logger.exception("Erro durante a inicialização da aplicação: %s", err)
        # Opcional: exibir uma mensagem de erro na própria página
        page.controls.clear()
        page.add(
            Text(
                f"Erro na inicialização: {err}",
                color="red",
                size=20
            )
        )
        page.update()

if __name__ == "__main__":
    try:
        logger.info("Iniciando a aplicação...")
        # Configuração para que o app rode em modo servidor e abra no navegador padrão do sistema.
        # Dessa forma, não é criada uma GUI nativa, mas a aplicação é hospedada em background.
        flet.app(target=main, port=8550, host="0.0.0.0", view="web_browser")
    except Exception as main_err:
        logger.exception("Erro ao iniciar o servidor do aplicativo: %s", main_err)
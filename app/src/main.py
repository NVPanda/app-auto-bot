from utils.callbacks import youchangechoice
from utils.appbar import create_bottom_appbar
from utils.tabsnav import build_tabs
from flet import *
import flet

import os
from dotenv import load_dotenv


def main(page: Page):
    page.bgcolor = "#121212"
    page.title = "Auto Bot"
    page.padding = 0
    page.spacing = 0
    page.scroll = "auto"
    page.window.width = 500
    page.window.height = 500
    page.maximizable = False


    # Carregando variáveis de ambiente
    root_project_path = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(root_project_path, "../../.env.local")
    load_dotenv(dotenv_path)
    





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

    # Criar conteúdo dinâmico aqui dentro
    content_section = Column(expand=True, alignment="center", spacing=20)

    
    page.floating_action_button_location = FloatingActionButtonLocation.CENTER_DOCKED
    mytabs = create_bottom_appbar(page, content_section)

    page.add(
        Column([
            mybar,
            Container(
                expand=True,
                alignment=alignment.top_center,
                padding=padding.all(20),
                content=content_section,
                
                
            )
        ], expand=True)
    )

    # Inicializa a aba padrão manualmente
    class FakeControl:
        tabs = [type("Tab", (), {"text": "Home"})()]
        selected_index = 0
    fake_event = type("Event", (), {"control": FakeControl()})()

    youchangechoice(fake_event, page, content_section)

flet.app(target=main, port=8550, host="0.0.0.0", view=None)

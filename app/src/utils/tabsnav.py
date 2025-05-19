from flet import *
from utils.callbacks import youchangechoice



def build_tabs(page: Page, content_section: Column):
    # Detectar se é um celular
    is_mobile = page.platform in ["android", "ios"]
    print(f"[DEBUG] Plataforma detectada: {page.platform}")
    print(f"[DEBUG] É mobile? {is_mobile}")

    

    # Tabs base
    tab_list = [
        Tab(text="Home", icon="home"),
        Tab(text="Mensagens", icon="message"),
        Tab(text="Logs", icon="analytics"),
    ]

    # Se for computador, adiciona "Inicia"
    if not is_mobile:
        tab_list.insert(2, Tab(text="Inicia", icon="rocket_launch"))

    return Tabs(
        tab_alignment=alignment.center,
        selected_index=0,
        animation_duration=300,
        unselected_label_color="white",
        label_color="white",
        indicator_color="white",
        indicator_border_radius=30,
        divider_color="#7c59f0",
        scrollable=True,
        on_change=lambda e: youchangechoice(e, page, content_section),
        padding=padding.symmetric(horizontal=10, vertical=10),
        tabs=tab_list
    )




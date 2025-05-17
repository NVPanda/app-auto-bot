from flet import *
from view.navbar import filtros_preco

def main(page: Page):
    page.title = "Auto Bot"
    page.padding = 0
    page.spacing = 0
    page.scroll = "auto"
    page.window_min_width = 300

    # Conteúdo que será atualizado conforme a aba
    content_section = Column(expand=True, alignment="center", spacing=20)

    def youchangechoice(e):
        aba = e.control.tabs[e.control.selected_index].text

        content_section.controls.clear()

        if aba == "Home":
            content_section.controls.append(
                filtros_preco(lambda e: print("Salvou na Home"))
            )
        elif aba == "Mensagens":
            content_section.controls.append(Text("Mensagens ainda não implementado"))
        elif aba == "Conta OLX":
            content_section.controls.append(Text("Página da Conta OLX"))
        elif aba == "Logs":
            content_section.controls.append(Text("Logs da aplicação"))

        page.update()

    # Tabs de navegação
    mytab = Tabs(
        selected_index=0,
        animation_duration=300,
        unselected_label_color="black",
        label_color="white",
        indicator_color="white",
        indicator_border_radius=30,
        divider_color="#7c59f0",
        scrollable=True,
        on_change=youchangechoice,
        tabs=[
            Tab(text="Home", icon="home"),
            Tab(text="Mensagens", icon="message"),
            Tab(text="Conta OLX", icon="store"),
            Tab(text="Logs", icon="analytics"),
        ]
    )

    # Topo com título e tabs
    mybar = Container(
        width=float("inf"),
        height=170,
        padding=padding.symmetric(horizontal=10, vertical=15),
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
        content=Column([
            Row([
                IconButton(icon="menu", icon_color="white"),
                Text("Auto Bot", size=25, color="white", weight="bold"),
                Row([
                    IconButton(icon="notifications", icon_size=25, icon_color="white"),
                    IconButton(icon="settings", icon_size=25, icon_color="white"),
                ])
            ], alignment="spaceBetween", vertical_alignment="center"),
            mytab
        ])
    )

    # Página completa
    page.add(
        Column([
            mybar,
            Container(
                expand=True,
                alignment=alignment.top_center,
                padding=padding.all(20),
                content=content_section
            )
        ], expand=True)
    )

    # Força carregar conteúdo da aba inicial
    youchangechoice(type("Event", (), {"control": mytab})())


app(target=main)

from flet import *


def inicia_automacao(page, content_section):

    status_text = Text("Clique no botão para iniciar a automação!", size=20, weight="bold", color=Colors.BLACK)
    botao = ElevatedButton(
        text="Iniciar",
        icon="play_arrow",
        style=ButtonStyle(bgcolor="#7c59f0", color="white")
    )

    estado = {"ativo": False}  # controla o estado da automação

    def alternar(e):
        if not estado["ativo"]:
            # Iniciar automação
            estado["ativo"] = True
            status_text.value = "Automação em andamento..."
            botao.text = "Parar"
            botao.icon = "stop"
        else:
            # Parar automação
            estado["ativo"] = False
            status_text.value = "Clique no botão para iniciar a automação!"
            botao.text = "Iniciar"
            botao.icon = "play_arrow"

        page.update()

    botao.on_click = alternar

    return Container(
        padding=padding.all(20),
        border_radius=10,
        bgcolor="#f2f2f2",
        content=Column([
            status_text,
            botao
        ], spacing=10)
    )

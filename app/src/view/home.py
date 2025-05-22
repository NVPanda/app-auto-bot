from flet import *
from datetime import datetime

# Lista global de logs
log_entries = ListView(
    expand=True,
    spacing=5,
    padding=10,
    auto_scroll=True
)


def filtro_completo():
    preco_min = TextField(
        color=Colors.BLACK,
        label="Preço mínimo",
        value="100",  # valor default
        keyboard_type=KeyboardType.NUMBER,
        prefix_text="R$ ",
        border="underline"
    )

    preco_max = TextField(
        color=Colors.BLACK,
        label="Preço máximo",
        value="1000",  # valor default
        keyboard_type=KeyboardType.NUMBER,
        prefix_text="R$ ",
        border="underline"
    )

    porcentagem = TextField(
        color=Colors.BLACK,
        label="Porcentagem (%)",
        value="10",  # valor default
        keyboard_type=KeyboardType.NUMBER,
        suffix_text="%",
        border="underline"
    )

    def salvar_tudo(e):
        hora = str(datetime.now().strftime("%H:%M:%S"))
        log_entries.controls.append(
            Text(f"[{hora}] Filtros salvos: R$ {preco_min.value} - R$ {preco_max.value}, Porcentagem: {porcentagem.value}%", color=Colors.GREEN)
        )
        print("Filtros salvos com sucesso")
        e.page.update()

    return Container(
        padding=padding.all(20),
        border_radius=10,
        bgcolor="#f2f2f2",
        content=Column([
            Text("Configurações de Filtros", size=20, weight="bold",color=Colors.BLACK),
            preco_min,
            preco_max,
            porcentagem,
            ElevatedButton(
                text="Salvar Tudo",
                icon="check",
                on_click=salvar_tudo,
                style=ButtonStyle(bgcolor="#7c59f0", color="white")
            )
        ], spacing=10)
    )





def logs_in_app(page):
    return Container(
        expand=True,
        bgcolor="111111",
        padding=20,
        content=Column([
            Text("Logs do Sistema", size=20, weight="bold", color=Colors.WHITE),
            Divider(),
            log_entries
        ])
    )

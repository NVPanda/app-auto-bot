from flet import *

def filtros_preco(on_salvar):
    return Container(
        padding=padding.all(20),
        border_radius=10,
        bgcolor="#f2f2f2",
        content=Column([
            Text("Filtros de Preço", size=20, weight="bold"),
            
            Text("Preço mínimo", size=14),
            TextField(
                hint_text="Ex: 100",
                keyboard_type=KeyboardType.NUMBER,
                prefix_text="R$ ",
                border="underline"
            ),

            Text("Preço máximo", size=14),
            TextField(
                hint_text="Ex: 1000",
                keyboard_type=KeyboardType.NUMBER,
                prefix_text="R$ ",
                border="underline"
            ),

            ElevatedButton(
                text="Salvar",
                icon="check",
                on_click=on_salvar,
                style=ButtonStyle(bgcolor="#7c59f0", color="white")
            )
        ], spacing=10)
    )

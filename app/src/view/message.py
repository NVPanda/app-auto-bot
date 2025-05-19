from flet import *
from dotenv import load_dotenv
import os

load_dotenv()


def mensagens_default(on_salvar):
    return Container(
        padding=padding.all(20),
        border_radius=border_radius.all(12),
        bgcolor="#f2f2f2",
        shadow=BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=Colors.with_opacity(0.3, "#7c59f0"),
            offset=Offset(0, 4),
        ),
        content=Column([
            Text("Mensagens padrão", size=20, weight="bold", color=Colors.BLACK),
            Text("Essas mensagens são usadas para agilizar o envio na OLX e WhatsApp.", size=12, color=Colors.GREY),

            Text("Whatsapp", size=14),
            TextField(
                hint_text=os.getenv("MENSAGEM_CLIENTE"),
                keyboard_type=KeyboardType.TEXT,
                color=Colors.BLACK,
                border="underline",
            ),

            Text("Olx", size=14, color=Colors.BLACK),
            TextField(
                hint_text=os.getenv("MENSAGEM_OLX"),
                keyboard_type=KeyboardType.TEXT,
                color=Colors.BLACK,
                border="underline",
            ),

            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ElevatedButton(
                        text="Editar",
                        icon="edit",
                        on_click=on_salvar,
                        width=120,
                        style=ButtonStyle(
                            bgcolor="#7c59f0",
                            color="white"
                        )
                    ),
                    ElevatedButton(
                        text="Salvar",
                        icon="check",
                        on_click=on_salvar,
                        width=120,
                        style=ButtonStyle(
                            bgcolor="#7c59f0",
                            color="white"
                        )
                    )
                ]
            )
        ])
    )

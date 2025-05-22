from flet import *

import controller.minera as minera
import threading



def inicia_automacao(page, content_section):
   
    status_text = Text("Clique no botão para iniciar a automação!", size=20, weight="bold", color=Colors.BLACK)
    botao = ElevatedButton(
        text="Iniciar",
        icon="play_arrow",
        style=ButtonStyle(bgcolor="#7c59f0", color="white")
    )

    estado = {"ativo": False}
    thread_ref = {"thread": None}

    def alternar(e):
        from utils.callbacks import youchangechoice
        
        if not estado["ativo"]:
            estado["ativo"] = True
            minera.executando["valor"] = True
            status_text.value = "Automação em andamento..."
            botao.text = "Parar"
            botao.icon = "stop"

            # Troca de aba
            from utils.callbacks import youchangechoice

            # ... dentro da função alternar ...

                        # Troca de aba para "Logs"
            tabs = None
            if hasattr(page, "bottom_appbar") and page.bottom_appbar is not None:
                row = page.bottom_appbar.content.content  # Row dentro do Container
                for c in row.controls:
                    if hasattr(c, "content") and isinstance(c.content, Tabs):
                        tabs = c.content
                        break

            if tabs:
                for idx, tab in enumerate(tabs.tabs):
                    if tab.text == "Logs":
                        tabs.selected_index = idx
                        youchangechoice(
                        type("Event", (), {"control": tabs})(), page, content_section
                        )
                        page.update()
                        break

            # Inicia thread
            
            minera.executando["valor"] = True
            t = threading.Thread(target=minera.capturar_e_ler_preco, args=(page,))
            t.start()
           
            
            thread_ref["thread"] = t

        else:
            estado["ativo"] = False
            status_text.value = "Clique no botão para iniciar a automação!"
            botao.text = "Iniciar"
            botao.icon = "play_arrow"

            # Para automação
            
            minera.executando["valor"] = False

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

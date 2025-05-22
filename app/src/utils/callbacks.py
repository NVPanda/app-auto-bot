from flet import *
from view.inicia import inicia_automacao
from view.message import mensagens_default
from view.home import filtro_completo, logs_in_app

def youchangechoice(e, page, content_section):
    aba = e.control.tabs[e.control.selected_index].text
    content_section.controls.clear()

    match aba:

        case "Home":
            content_section.controls.extend([
            filtro_completo()
            ])
            

        
        case "Mensagens":
            content_section.controls.extend([
                mensagens_default(lambda e: print("."))
            ])
            
        
        case "Inicia":
           

            content_section.controls.extend([
                
            inicia_automacao(page, content_section)
            ])

            
        
        case "Logs":
            content_section.controls.extend([
                logs_in_app(page)
            ])
           

    page.update()

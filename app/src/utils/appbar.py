import flet as ft
from flet import *

from utils.tabsnav import build_tabs




def create_bottom_appbar(page: ft.Page, content_section):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    mytabs = build_tabs(page, content_section)  # cria apenas uma vez

    
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.BLACK,
        shape=ft.NotchShape.CIRCULAR,

        content=ft.Container(
            width=float("inf"),
            

            gradient=LinearGradient(
            begin=alignment.top_left,
            end=alignment.bottom_right,
            colors=["#fc4795", "#7c59f0"]
        ),
            border_radius=border_radius.vertical(top=30,bottom=30),
            shadow=BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color="#15191d",
            ),

            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        
                        content=mytabs,  # usa o mesmo mytabs
                    )
                ]
            ),
        )
    )

    return mytabs  # Retorna as abas pra usar no main

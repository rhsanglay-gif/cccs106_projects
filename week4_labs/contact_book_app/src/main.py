# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT

    db_conn = init_db()

    # Input fields
    name_input = ft.TextField(label="Name", width=350)
    phone_input = ft.TextField(label="Phone", width=350)
    email_input = ft.TextField(label="Email", width=350)
    inputs = (name_input, phone_input, email_input)

    # Search field
    search_input = ft.TextField(
        label="Search by name",
        width=350,
        on_change=lambda e: display_contacts(
            page, contacts_list_view, db_conn, search_term=e.control.value
        )
    )

    # Dark mode toggle
    theme_toggle = ft.Switch(
        label="Dark Mode",
        value=False,
        on_change=lambda e: (
            setattr(page, "theme_mode", ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT),
            page.update()
        )
    )

    # ListView for contacts
    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    # Add button
    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn)
    )

    # Layout
    page.add(
        ft.Column([
            ft.Row(
                controls=[
                    ft.Text("Contact Book", size=24, weight=ft.FontWeight.BOLD),
                    ft.Container(content=theme_toggle, width=120, height=40, alignment=ft.alignment.center_right)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(),
            ft.Text("Enter Contact Details:", size=18, weight=ft.FontWeight.BOLD),
            name_input,
            phone_input,
            email_input,
            add_button,
            ft.Divider(),
            search_input,
            ft.Text("Contacts:", size=18, weight=ft.FontWeight.BOLD),
            contacts_list_view,
        ])
    )

    # Display all contacts initially
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)

# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts in Card format."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)

    for contact in contacts:
        contact_id, name, phone, email = contact

        card = ft.Card(
            content=ft.Container(
                padding=10,        
                width=380,         
                content=ft.Column([
                    # Name
                    ft.Text(name, size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    # Phone
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.PHONE, size=18),
                            ft.Text(f" {phone}")
                        ],
                        spacing=5
                    ),
                    # Email
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.EMAIL, size=18),
                            ft.Text(f" {email}")
                        ],
                        spacing=5
                    ),
                    ft.Divider(),
                    # Edit/Delete buttons
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Edit",
                                icon=ft.Icons.EDIT,
                                on_click=lambda _, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view)
                            ),
                            ft.ElevatedButton(
                                "Delete",
                                icon=ft.Icons.DELETE,
                                on_click=lambda _, cid=contact_id: delete_contact(page, cid, db_conn, contacts_list_view)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10
                    )
                ])
            ),
            elevation=3,
            margin=ft.margin.all(5),  # margin around card
        )

        contacts_list_view.controls.append(card)

    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn):
    """Adds a new contact and refreshes the list, with input validation."""
    name_input, phone_input, email_input = inputs

    # Input validation: Name cannot be empty
    if not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        page.update()
        return
    else:
        name_input.error_text = None  # Clear previous error

    # Add contact to database
    add_contact_db(db_conn, name_input.value.strip(), phone_input.value.strip(), email_input.value.strip())

    # Clear input fields
    for field in inputs:
        field.value = ""

    # Refresh contact list
    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Shows a confirmation dialog before deleting a contact."""

    def confirm_delete(e):
        # User clicked "Yes" → delete the contact
        delete_contact_db(db_conn, contact_id)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    def cancel_delete(e):
        # User clicked "No" → just close the dialog
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("No", on_click=cancel_delete),
            ft.TextButton("Yes", on_click=confirm_delete),
        ],
    )

    page.open(dialog)


def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details with validation."""
    contact_id, name, phone, email = contact

    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e):
        # Input validation: Name cannot be empty
        if not edit_name.value.strip():
            edit_name.error_text = "Name cannot be empty"
            page.update()
            return
        else:
            edit_name.error_text = None  # Clear previous error

        # Update contact in database
        update_contact_db(db_conn, contact_id, edit_name.value.strip(), edit_phone.value.strip(), edit_email.value.strip())
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email]),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )
    page.open(dialog)


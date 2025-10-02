# src/main.py
import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    # Configure window
    page.title = "User Login"
    page.window.width = 400
    page.window.height = 350
    page.window.center()
    page.window.frameless = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.AMBER_ACCENT

    # Username field
    username_field = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
    )

    # Password field
    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
    )

    # Login logic
    async def login_click(e):
        username = username_field.value.strip()
        password = password_field.value.strip()

        # Input validation
        if not username or not password:
            await page.dialog(
                ft.AlertDialog(
                    title=ft.Text("Input Error"),
                    content=ft.Text("Please enter username and password"),
                    actions=[ft.TextButton("OK", on_click=lambda _: page.close_dialog())],
                    actions_alignment=ft.MainAxisAlignment.END,
                    icon=ft.Icon(ft.Icons.INFO, color="blue"),
                )
            )
            return

        try:
            conn = connect_db()
            if conn is None:
                raise mysql.connector.Error("Connection failed")

            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                await page.dialog(
                    ft.AlertDialog(
                        title=ft.Text("Login Successful"),
                        content=ft.Text(f"Welcome, {username}!"),
                        actions=[ft.TextButton("OK", on_click=lambda _: page.close_dialog())],
                        actions_alignment=ft.MainAxisAlignment.END,
                        icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color="green"),
                    )
                )
            else:
                await page.dialog(
                    ft.AlertDialog(
                        title=ft.Text("Login Failed"),
                        content=ft.Text("Invalid username or password"),
                        actions=[ft.TextButton("OK", on_click=lambda _: page.close_dialog())],
                        actions_alignment=ft.MainAxisAlignment.END,
                        icon=ft.Icon(ft.Icons.ERROR, color="red"),
                    )
                )
        except mysql.connector.Error:
            await page.dialog(
                ft.AlertDialog(
                    title=ft.Text("Database Error"),
                    content=ft.Text("An error occurred while connecting to the database"),
                    actions=[ft.TextButton("OK", on_click=lambda _: page.close_dialog())],
                    actions_alignment=ft.MainAxisAlignment.END,
                    icon=ft.Icon(ft.Icons.WARNING, color="orange"),
                )
            )

    # Login button
    login_button = ft.ElevatedButton(
        text="Login",
        width=100,
        icon=ft.Icons.LOGIN,
        on_click=login_click
    )

    # UI layout
    page.add(
        ft.Text("User Login", size=20, weight=ft.FontWeight.BOLD, font_family="Arial"),
        ft.Container(
            content=ft.Column([username_field, password_field], spacing=20)
        ),
        ft.Container(
            content=login_button,
            alignment=ft.alignment.top_right,
            margin=ft.margin.only(top=0, right=40, bottom=20, left=0)
        )
    )

ft.app(target=main)
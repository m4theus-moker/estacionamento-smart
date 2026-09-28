"""Estacionamento Smart - Application Frontend"""

import reflex as rx
import httpx

from rxconfig import config

# URL base oficial da API do Xano
XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:o7T2IhYl"


class AuthState(rx.State):
    """Estado de autenticação e sessão do usuário."""
    token: str = ""
    user_id: int = 0
    name: str = ""
    email: str = ""
    role: str = ""

    # Campos de formulário - Login
    login_email: str = ""
    login_password: str = ""

    # Campos de formulário - Cadastro
    signup_name: str = ""
    signup_email: str = ""
    signup_password: str = ""

    # Feedback
    error_message: str = ""
    success_message: str = ""
    is_loading: bool = False

    def set_login_email(self, value: str):
        self.login_email = value

    def set_login_password(self, value: str):
        self.login_password = value

    def set_signup_name(self, value: str):
        self.signup_name = value

    def set_signup_email(self, value: str):
        self.signup_email = value

    def set_signup_password(self, value: str):
        self.signup_password = value

    async def login(self):
        self.error_message = ""
        self.success_message = ""
        self.is_loading = True
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{XANO_API_URL}/auth/login",
                    json={"email": self.login_email, "password": self.login_password}
                )
            data = response.json()
            if response.status_code == 200 and "authToken" in data:
                self.token = data["authToken"]
                self.user_id = data.get("user_id", 0)
                await self.fetch_me()
                self.is_loading = False
                return rx.redirect("/")
            else:
                self.error_message = data.get("message", "Credenciais inválidas.")
        except Exception as e:
            self.error_message = f"Erro de conexão com o servidor: {str(e)}"
        finally:
            self.is_loading = False

    async def signup(self):
        self.error_message = ""
        self.success_message = ""
        self.is_loading = True
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{XANO_API_URL}/auth/signup",
                    json={
                        "name": self.signup_name,
                        "email": self.signup_email,
                        "password": self.signup_password
                    }
                )
            data = response.json()
            if response.status_code == 200 and "authToken" in data:
                self.token = data["authToken"]
                self.user_id = data.get("user_id", 0)
                await self.fetch_me()
                self.success_message = "Cadastro realizado com sucesso!"
                self.is_loading = False
                return rx.redirect("/")
            else:
                self.error_message = data.get("message", "Erro ao realizar cadastro (e-mail duplicado ou inválido).")
        except Exception as e:
            self.error_message = f"Erro de conexão com o servidor: {str(e)}"
        finally:
            self.is_loading = False

    async def fetch_me(self):
        if not self.token:
            return
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{XANO_API_URL}/auth/me",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            if response.status_code == 200:
                data = response.json()
                self.name = data.get("name", "")
                self.email = data.get("email", "")
                self.role = data.get("role", "cliente")
                self.user_id = data.get("id", self.user_id)
        except Exception:
            pass

    def logout(self):
        self.token = ""
        self.user_id = 0
        self.name = ""
        self.email = ""
        self.role = ""
        self.login_email = ""
        self.login_password = ""
        return rx.redirect("/login")


def navbar() -> rx.Component:
    return rx.hstack(
        rx.heading("🚗 Estacionamento Smart", size="6", weight="bold"),
        rx.spacer(),
        rx.cond(
            AuthState.token != "",
            rx.hstack(
                rx.text(f"Olá, {AuthState.name} ({AuthState.role})", weight="medium"),
                rx.button("Sair", on_click=AuthState.logout, color_scheme="red", variant="soft"),
                spacing="4",
                align="center",
            ),
            rx.hstack(
                rx.link("Entrar", href="/login"),
                rx.link(rx.button("Cadastrar-se", variant="solid"), href="/signup"),
                spacing="4",
                align="center",
            ),
        ),
        width="100%",
        padding="4",
        border_bottom="1px solid #eaeaea",
        background="white",
    )


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.cond(
                    AuthState.token != "",
                    rx.vstack(
                        rx.heading("Bem-vindo ao Painel, " + AuthState.name + "!", size="8"),
                        rx.text("E-mail: " + AuthState.email, size="4"),
                        rx.text("Papel no sistema: " + AuthState.role, size="4", color="gray"),
                        rx.divider(margin_y="4"),
                        rx.text("Módulos do Sistema:", size="5", weight="bold"),
                        rx.grid(
                            rx.card(rx.vstack(rx.heading("🚗 Veículos", size="5"), rx.text("Gerencie seus veículos cadastrados."))),
                            rx.card(rx.vstack(rx.heading("🅿️ Vagas", size="5"), rx.text("Consulte vagas disponíveis em tempo real."))),
                            rx.card(rx.vstack(rx.heading("📅 Reservas", size="5"), rx.text("Faça e gerencie suas reservas."))),
                            columns="3",
                            spacing="4",
                            width="100%",
                        ),
                        spacing="5",
                        align="start",
                        padding_top="6",
                    ),
                    rx.vstack(
                        rx.heading("Gestão Inteligente de Estacionamento", size="9", align="center"),
                        rx.text("Faça login ou cadastre-se para consultar vagas, gerenciar veículos e realizar reservas.", size="5", color="gray", align="center"),
                        rx.hstack(
                            rx.link(rx.button("Entrar no Sistema", size="4"), href="/login"),
                            rx.link(rx.button("Criar Conta", size="4", variant="outline"), href="/signup"),
                            spacing="4",
                            padding_top="4",
                        ),
                        spacing="6",
                        align="center",
                        justify="center",
                        min_height="60vh",
                    ),
                ),
                width="100%",
            ),
            max_width="1200px",
        ),
        width="100%",
        min_height="100vh",
        background="#fcfcfc",
    )


def login_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Entrar na sua Conta", size="6", align="center"),
                    rx.text("Insira seus dados para acessar o sistema.", size="2", color="gray", align="center"),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.callout(AuthState.error_message, icon="triangle_alert", color_scheme="red", width="100%"),
                    ),
                    rx.vstack(
                        rx.text("E-mail", size="2", weight="medium"),
                        rx.input(
                            placeholder="seu@email.com",
                            value=AuthState.login_email,
                            on_change=AuthState.set_login_email,
                            width="100%",
                        ),
                        rx.text("Senha", size="2", weight="medium"),
                        rx.input(
                            type="password",
                            placeholder="Sua senha",
                            value=AuthState.login_password,
                            on_change=AuthState.set_login_password,
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                        padding_y="2",
                    ),
                    rx.button(
                        "Entrar",
                        on_click=AuthState.login,
                        width="100%",
                        color_scheme="blue",
                        size="3",
                    ),
                    rx.hstack(
                        rx.text("Não tem uma conta?", size="2"),
                        rx.link("Cadastre-se", href="/signup", size="2", weight="bold"),
                        spacing="2",
                        justify="center",
                        width="100%",
                        padding_top="2",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="400px",
                ),
                padding="6",
                box_shadow="lg",
                border_radius="large",
                width="100%",
                max_width="450px",
            ),
            width="100%",
            min_height="80vh",
        ),
        width="100%",
        min_height="100vh",
        background="#fcfcfc",
    )


def signup_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Criar Conta", size="6", align="center"),
                    rx.text("Cadastre-se para começar a usar o Estacionamento Smart.", size="2", color="gray", align="center"),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.callout(AuthState.error_message, icon="triangle_alert", color_scheme="red", width="100%"),
                    ),
                    rx.cond(
                        AuthState.success_message != "",
                        rx.callout(AuthState.success_message, icon="check", color_scheme="green", width="100%"),
                    ),
                    rx.vstack(
                        rx.text("Nome Completo", size="2", weight="medium"),
                        rx.input(
                            placeholder="Seu nome",
                            value=AuthState.signup_name,
                            on_change=AuthState.set_signup_name,
                            width="100%",
                        ),
                        rx.text("E-mail", size="2", weight="medium"),
                        rx.input(
                            placeholder="seu@email.com",
                            value=AuthState.signup_email,
                            on_change=AuthState.set_signup_email,
                            width="100%",
                        ),
                        rx.text("Senha", size="2", weight="medium"),
                        rx.input(
                            type="password",
                            placeholder="Mínimo 8 caracteres (com letras e números)",
                            value=AuthState.signup_password,
                            on_change=AuthState.set_signup_password,
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                        padding_y="2",
                    ),
                    rx.button(
                        "Cadastrar",
                        on_click=AuthState.signup,
                        width="100%",
                        color_scheme="blue",
                        size="3",
                    ),
                    rx.hstack(
                        rx.text("Já tem uma conta?", size="2"),
                        rx.link("Entrar", href="/login", size="2", weight="bold"),
                        spacing="2",
                        justify="center",
                        width="100%",
                        padding_top="2",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="400px",
                ),
                padding="6",
                box_shadow="lg",
                border_radius="large",
                width="100%",
                max_width="450px",
            ),
            width="100%",
            min_height="80vh",
        ),
        width="100%",
        min_height="100vh",
        background="#fcfcfc",
    )


app = rx.App()
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")

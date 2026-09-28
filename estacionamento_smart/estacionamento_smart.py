"""Estacionamento Smart - Application Frontend"""

import reflex as rx
import httpx

from rxconfig import config
from estacionamento_smart.styles import THEME_APPEARANCE, ACCENT_COLOR, RADIUS, CARD_MAX_WIDTH, CONTAINER_MAX_WIDTH
from estacionamento_smart.components.navbar import navbar
from estacionamento_smart.components.dashboard_card import dashboard_card

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

    @rx.var
    def role_display(self) -> str:
        """Retorna o papel do usuário formatado em português com segurança contra None."""
        if not self.role:
            return "Cliente"
        if str(self.role).lower() in ["admin", "administrador"]:
            return "Administrador"
        return "Cliente"

    def set_login_email(self, value: str):
        self.login_email = value or ""

    def set_login_password(self, value: str):
        self.login_password = value or ""

    def set_signup_name(self, value: str):
        self.signup_name = value or ""

    def set_signup_email(self, value: str):
        self.signup_email = value or ""

    def set_signup_password(self, value: str):
        self.signup_password = value or ""

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
                self.token = data.get("authToken", "")
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
                self.token = data.get("authToken", "")
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
                self.name = data.get("name") or ""
                self.email = data.get("email") or ""
                self.role = data.get("role") or "cliente"
                self.user_id = data.get("id") or self.user_id
        except Exception:
            pass

    def logout(self):
        self.token = ""
        self.user_id = 0
        self.name = ""
        self.email = ""
        self.role = "cliente"
        self.login_email = ""
        self.login_password = ""
        return rx.redirect("/login")


def index() -> rx.Component:
    return rx.vstack(
        navbar(AuthState),
        rx.center(
            rx.container(
                rx.vstack(
                    rx.cond(
                        AuthState.token != "",
                        # Dashboard Logado
                        rx.vstack(
                            rx.heading(f"Olá, {AuthState.name}!", size="8", weight="bold", color="var(--gray-12)"),
                            rx.text("Bem-vindo ao painel de controle do Estacionamento Smart.", size="4", color="var(--gray-11)"),
                            rx.box(height="2"),
                            # Card de Perfil
                            rx.card(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("Informações da Conta", size="2", weight="bold", color="var(--gray-10)"),
                                        rx.text(f"E-mail: {AuthState.email}", size="3", weight="medium", color="var(--gray-12)"),
                                        rx.text(f"Perfil: {AuthState.role_display}", size="3", weight="medium", color="var(--gray-12)"),
                                        spacing="1",
                                        align="start",
                                    ),
                                    rx.spacer(),
                                    rx.badge(AuthState.role_display, color_scheme="indigo", size="3"),
                                    width="100%",
                                    align="center",
                                ),
                                size="3",
                                width="100%",
                                padding="6",
                                border="1px solid var(--gray-4)",
                            ),
                            rx.box(height="4"),
                            rx.heading("Módulos Operacionais", size="6", weight="bold", color="var(--gray-12)"),
                            # Grid de Módulos Responsivo
                            rx.grid(
                                dashboard_card(
                                    icon="🚗",
                                    title="Veículos",
                                    description="Gerencie os veículos cadastrados na sua conta de forma rápida.",
                                    href="#",
                                ),
                                dashboard_card(
                                    icon="🅿️",
                                    title="Vagas",
                                    description="Consulte a disponibilidade de vagas em tempo real no estacionamento.",
                                    href="#",
                                ),
                                dashboard_card(
                                    icon="📅",
                                    title="Reservas",
                                    description="Crie, acompanhe e gerencie suas reservas de vagas com comodidade.",
                                    href="#",
                                ),
                                columns=rx.breakpoints(initial="1", sm="2", md="3"),
                                spacing="5",
                                width="100%",
                            ),
                            spacing="6",
                            align="start",
                            width="100%",
                        ),
                        # Hero para Deslogado
                        rx.vstack(
                            rx.heading("Gestão Inteligente de Estacionamento", size="9", weight="bold", align="center", color="var(--gray-12)", line_height="1.2"),
                            rx.text(
                                "Sistema moderno para controle de vagas, reservas e veículos com agilidade, segurança e praticidade.",
                                size="5",
                                color="var(--gray-11)",
                                align="center",
                                max_width="650px",
                                line_height="1.5",
                            ),
                            rx.box(height="2"),
                            rx.hstack(
                                rx.link(
                                    rx.button("Entrar no Sistema", size="4", variant="solid", color_scheme="indigo", cursor="pointer"),
                                    href="/login",
                                ),
                                rx.link(
                                    rx.button("Criar Conta", size="4", variant="outline", color_scheme="indigo", cursor="pointer"),
                                    href="/signup",
                                ),
                                spacing="4",
                            ),
                            spacing="6",
                            align="center",
                            justify="center",
                            min_height="65vh",
                            width="100%",
                        ),
                    ),
                    width="100%",
                ),
                max_width=CONTAINER_MAX_WIDTH,
                width="100%",
                padding_x="4",
                padding_y="8",
            ),
            width="100%",
        ),
        width="100%",
        min_height="100vh",
        background="var(--color-background)",
    )


def login_page() -> rx.Component:
    return rx.vstack(
        navbar(AuthState),
        rx.center(
            rx.container(
                rx.center(
                    rx.card(
                        rx.vstack(
                            rx.heading("Entrar na sua Conta", size="6", weight="bold", align="center", color="var(--gray-12)"),
                            rx.text("Insira seus dados para acessar o sistema.", size="2", color="var(--gray-11)", align="center"),
                            rx.cond(
                                AuthState.error_message != "",
                                rx.callout(
                                    AuthState.error_message,
                                    icon="triangle_alert",
                                    color_scheme="red",
                                    size="2",
                                    width="100%",
                                ),
                            ),
                            rx.vstack(
                                rx.text("E-mail", size="2", weight="bold", color="var(--gray-12)"),
                                rx.input(
                                    placeholder="seu@email.com",
                                    value=AuthState.login_email,
                                    on_change=AuthState.set_login_email,
                                    width="100%",
                                    size="3",
                                ),
                                rx.text("Senha", size="2", weight="bold", color="var(--gray-12)"),
                                rx.input(
                                    type="password",
                                    placeholder="Sua senha",
                                    value=AuthState.login_password,
                                    on_change=AuthState.set_login_password,
                                    width="100%",
                                    size="3",
                                ),
                                spacing="3",
                                width="100%",
                                padding_y="2",
                            ),
                            rx.button(
                                rx.cond(
                                    AuthState.is_loading,
                                    rx.spinner(size="2"),
                                    "Entrar",
                                ),
                                on_click=AuthState.login,
                                width="100%",
                                color_scheme="indigo",
                                size="3",
                                cursor="pointer",
                                disabled=AuthState.is_loading,
                            ),
                            rx.hstack(
                                rx.text("Não tem uma conta?", size="2", color="var(--gray-11)"),
                                rx.link("Cadastre-se", href="/signup", size="2", weight="bold", color_scheme="indigo"),
                                spacing="2",
                                justify="center",
                                width="100%",
                                padding_top="2",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="7",
                        box_shadow="0 20px 40px rgba(0, 0, 0, 0.1)",
                        border_radius=RADIUS,
                        width="100%",
                        max_width=CARD_MAX_WIDTH,
                        background="var(--color-panel)",
                        border="1px solid var(--gray-4)",
                    ),
                    width="100%",
                ),
                max_width=CONTAINER_MAX_WIDTH,
                width="100%",
                padding_y="6",
                padding_x="4",
            ),
            width="100%",
            min_height="80vh",
        ),
        width="100%",
        min_height="100vh",
        background="var(--color-background)",
    )


def signup_page() -> rx.Component:
    return rx.vstack(
        navbar(AuthState),
        rx.center(
            rx.container(
                rx.center(
                    rx.card(
                        rx.vstack(
                            rx.heading("Criar Conta", size="6", weight="bold", align="center", color="var(--gray-12)"),
                            rx.text("Cadastre-se para começar a usar o Estacionamento Smart.", size="2", color="var(--gray-11)", align="center"),
                            rx.cond(
                                AuthState.error_message != "",
                                rx.callout(
                                    AuthState.error_message,
                                    icon="triangle_alert",
                                    color_scheme="red",
                                    size="2",
                                    width="100%",
                                ),
                            ),
                            rx.cond(
                                AuthState.success_message != "",
                                rx.callout(
                                    AuthState.success_message,
                                    icon="check",
                                    color_scheme="green",
                                    size="2",
                                    width="100%",
                                ),
                            ),
                            rx.vstack(
                                rx.text("Nome Completo", size="2", weight="bold", color="var(--gray-12)"),
                                rx.input(
                                    placeholder="Seu nome",
                                    value=AuthState.signup_name,
                                    on_change=AuthState.set_signup_name,
                                    width="100%",
                                    size="3",
                                ),
                                rx.text("E-mail", size="2", weight="bold", color="var(--gray-12)"),
                                rx.input(
                                    placeholder="seu@email.com",
                                    value=AuthState.signup_email,
                                    on_change=AuthState.set_signup_email,
                                    width="100%",
                                    size="3",
                                ),
                                rx.text("Senha", size="2", weight="bold", color="var(--gray-12)"),
                                rx.input(
                                    type="password",
                                    placeholder="Mínimo 8 caracteres",
                                    value=AuthState.signup_password,
                                    on_change=AuthState.set_signup_password,
                                    width="100%",
                                    size="3",
                                ),
                                spacing="3",
                                width="100%",
                                padding_y="2",
                            ),
                            rx.button(
                                rx.cond(
                                    AuthState.is_loading,
                                    rx.spinner(size="2"),
                                    "Cadastrar",
                                ),
                                on_click=AuthState.signup,
                                width="100%",
                                color_scheme="indigo",
                                size="3",
                                cursor="pointer",
                                disabled=AuthState.is_loading,
                            ),
                            rx.hstack(
                                rx.text("Já tem uma conta?", size="2", color="var(--gray-11)"),
                                rx.link("Entrar", href="/login", size="2", weight="bold", color_scheme="indigo"),
                                spacing="2",
                                justify="center",
                                width="100%",
                                padding_top="2",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="7",
                        box_shadow="0 20px 40px rgba(0, 0, 0, 0.1)",
                        border_radius=RADIUS,
                        width="100%",
                        max_width=CARD_MAX_WIDTH,
                        background="var(--color-panel)",
                        border="1px solid var(--gray-4)",
                    ),
                    width="100%",
                ),
                max_width=CONTAINER_MAX_WIDTH,
                width="100%",
                padding_y="6",
                padding_x="4",
            ),
            width="100%",
            min_height="80vh",
        ),
        width="100%",
        min_height="100vh",
        background="var(--color-background)",
    )


app = rx.App(
    theme=rx.theme(
        appearance=THEME_APPEARANCE,
        accent_color=ACCENT_COLOR,
        radius=RADIUS,
        panel_background="solid",
    )
)
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")

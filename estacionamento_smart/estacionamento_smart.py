"""Estacionamento Smart - Application Frontend"""

import reflex as rx
import httpx

from rxconfig import config
from estacionamento_smart.styles import THEME_APPEARANCE, ACCENT_COLOR, RADIUS, CARD_MAX_WIDTH, CONTAINER_MAX_WIDTH
from estacionamento_smart.components.navbar import navbar
from estacionamento_smart.components.dashboard_card import dashboard_card

# URLs base da API do Xano
XANO_AUTH_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:o7T2IhYl"
XANO_VEHICLE_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:vehicle"


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
                    f"{XANO_AUTH_API_URL}/auth/login",
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


class VehicleState(rx.State):
    """Estado para gerenciamento de veículos."""
    vehicles: list[dict] = []
    form_id: int = 0
    form_plate: str = ""
    form_brand: str = ""
    form_model: str = ""
    form_color: str = ""
    form_year: int = 2024
    is_editing: bool = False
    error_message: str = ""
    success_message: str = ""
    is_loading: bool = False

    def set_form_plate(self, value: str):
        self.form_plate = (value or "").upper()

    def set_form_brand(self, value: str):
        self.form_brand = value or ""

    def set_form_model(self, value: str):
        self.form_model = value or ""

    def set_form_color(self, value: str):
        self.form_color = value or ""

    def set_form_year(self, value: str):
        try:
            self.form_year = int(value) if value else 2024
        except ValueError:
            self.form_year = 2024

    async def load_vehicles(self):
        auth = await self.get_state(AuthState)
        if not auth.token:
            return
        self.is_loading = True
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{XANO_VEHICLE_API_URL}/vehicle",
                    headers={"Authorization": f"Bearer {auth.token}"}
                )
            if response.status_code == 200:
                self.vehicles = response.json() or []
            else:
                self.vehicles = []
        except Exception as e:
            self.error_message = f"Erro ao carregar veículos: {str(e)}"
        finally:
            self.is_loading = False

    def start_add(self):
        self.form_id = 0
        self.form_plate = ""
        self.form_brand = ""
        self.form_model = ""
        self.form_color = ""
        self.form_year = 2024
        self.is_editing = False
        self.error_message = ""
        self.success_message = ""

    def start_edit(self, vehicle: dict):
        self.form_id = vehicle.get("id", 0)
        self.form_plate = vehicle.get("plate", "")
        self.form_brand = vehicle.get("brand", "")
        self.form_model = vehicle.get("model", "")
        self.form_color = vehicle.get("color", "")
        self.form_year = vehicle.get("year", 2024)
        self.is_editing = True
        self.error_message = ""
        self.success_message = ""

    async def save_vehicle(self):
        auth = await self.get_state(AuthState)
        if not auth.token:
            return
        self.error_message = ""
        self.success_message = ""
        self.is_loading = True
        try:
            payload = {
                "plate": self.form_plate,
                "brand": self.form_brand,
                "model": self.form_model,
                "color": self.form_color,
                "year": self.form_year,
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                if self.form_id == 0:
                    response = await client.post(
                        f"{XANO_VEHICLE_API_URL}/vehicle",
                        json=payload,
                        headers={"Authorization": f"Bearer {auth.token}"}
                    )
                else:
                    payload["id"] = self.form_id
                    response = await client.put(
                        f"{XANO_VEHICLE_API_URL}/vehicle/{self.form_id}",
                        json=payload,
                        headers={"Authorization": f"Bearer {auth.token}"}
                    )
            data = response.json()
            if response.status_code in [200, 201]:
                self.success_message = "Veículo salvo com sucesso!"
                self.start_add()
                await self.load_vehicles()
            else:
                self.error_message = data.get("message", "Erro ao salvar veículo.")
        except Exception as e:
            self.error_message = f"Erro de conexão: {str(e)}"
        finally:
            self.is_loading = False

    async def delete_vehicle(self, vehicle_id: int):
        auth = await self.get_state(AuthState)
        if not auth.token:
            return
        self.error_message = ""
        self.success_message = ""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.delete(
                    f"{XANO_VEHICLE_API_URL}/vehicle/{vehicle_id}",
                    headers={"Authorization": f"Bearer {auth.token}"}
                )
            if response.status_code == 200:
                self.success_message = "Veículo excluído com sucesso!"
                await self.load_vehicles()
            else:
                data = response.json()
                self.error_message = data.get("message", "Erro ao excluir veículo.")
        except Exception as e:
            self.error_message = f"Erro de conexão: {str(e)}"


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
                                    href="/vehicles",
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


def vehicles_page() -> rx.Component:
    return rx.vstack(
        navbar(AuthState),
        rx.center(
            rx.container(
                rx.vstack(
                    rx.hstack(
                        rx.link(rx.button("← Voltar ao Painel", variant="soft", size="2"), href="/"),
                        rx.spacer(),
                        align="center",
                        width="100%",
                    ),
                    rx.heading("Gerenciamento de Veículos", size="7", weight="bold", color="var(--gray-12)"),
                    rx.text("Cadastre e gerencie os veículos associados à sua conta.", size="3", color="var(--gray-11)"),
                    rx.box(height="2"),
                    rx.cond(
                        VehicleState.error_message != "",
                        rx.callout(VehicleState.error_message, icon="triangle_alert", color_scheme="red", size="2", width="100%"),
                    ),
                    rx.cond(
                        VehicleState.success_message != "",
                        rx.callout(VehicleState.success_message, icon="check", color_scheme="green", size="2", width="100%"),
                    ),
                    # Formulário de Cadastro/Edição
                    rx.card(
                        rx.vstack(
                            rx.heading(rx.cond(VehicleState.is_editing, "Editar Veículo", "Cadastrar Novo Veículo"), size="5", weight="bold"),
                            rx.grid(
                                rx.vstack(
                                    rx.text("Placa", size="2", weight="bold"),
                                    rx.input(placeholder="ABC-1234", value=VehicleState.form_plate, on_change=VehicleState.set_form_plate, width="100%"),
                                    align="start", width="100%", spacing="1",
                                ),
                                rx.vstack(
                                    rx.text("Marca", size="2", weight="bold"),
                                    rx.input(placeholder="Ex: Toyota", value=VehicleState.form_brand, on_change=VehicleState.set_form_brand, width="100%"),
                                    align="start", width="100%", spacing="1",
                                ),
                                rx.vstack(
                                    rx.text("Modelo", size="2", weight="bold"),
                                    rx.input(placeholder="Ex: Corolla", value=VehicleState.form_model, on_change=VehicleState.set_form_model, width="100%"),
                                    align="start", width="100%", spacing="1",
                                ),
                                rx.vstack(
                                    rx.text("Cor", size="2", weight="bold"),
                                    rx.input(placeholder="Ex: Prata", value=VehicleState.form_color, on_change=VehicleState.set_form_color, width="100%"),
                                    align="start", width="100%", spacing="1",
                                ),
                                rx.vstack(
                                    rx.text("Ano", size="2", weight="bold"),
                                    rx.input(placeholder="2024", value=VehicleState.form_year.to_string(), on_change=VehicleState.set_form_year, width="100%"),
                                    align="start", width="100%", spacing="1",
                                ),
                                columns=rx.breakpoints(initial="1", sm="2", md="3"),
                                spacing="4",
                                width="100%",
                            ),
                            rx.hstack(
                                rx.button(
                                    rx.cond(VehicleState.is_editing, "Atualizar Veículo", "Cadastrar Veículo"),
                                    on_click=VehicleState.save_vehicle,
                                    color_scheme="indigo",
                                    size="3",
                                    cursor="pointer",
                                ),
                                rx.cond(
                                    VehicleState.is_editing,
                                    rx.button("Cancelar", on_click=VehicleState.start_add, variant="soft", color_scheme="gray", size="3", cursor="pointer"),
                                ),
                                spacing="3",
                                padding_top="2",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="5",
                        width="100%",
                        border="1px solid var(--gray-4)",
                    ),
                    rx.box(height="2"),
                    rx.heading("Meus Veículos", size="6", weight="bold", color="var(--gray-12)"),
                    # Lista de Veículos
                    rx.cond(
                        VehicleState.vehicles.length() > 0,
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("Placa"),
                                    rx.table.column_header_cell("Marca"),
                                    rx.table.column_header_cell("Modelo"),
                                    rx.table.column_header_cell("Cor"),
                                    rx.table.column_header_cell("Ano"),
                                    rx.table.column_header_cell("Ações"),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    VehicleState.vehicles,
                                    lambda v: rx.table.row(
                                        rx.table.cell(v["plate"], weight="bold"),
                                        rx.table.cell(v["brand"]),
                                        rx.table.cell(v["model"]),
                                        rx.table.cell(v["color"]),
                                        rx.table.cell(v["year"]),
                                        rx.table.cell(
                                            rx.hstack(
                                                rx.button("Editar", size="1", variant="soft", color_scheme="indigo", on_click=lambda: VehicleState.start_edit(v)),
                                                rx.button("Excluir", size="1", variant="soft", color_scheme="red", on_click=lambda: VehicleState.delete_vehicle(v["id"])),
                                                spacing="2",
                                            )
                                        ),
                                    )
                                )
                            ),
                            width="100%",
                            variant="surface",
                        ),
                        rx.card(
                            rx.center(
                                rx.vstack(
                                    rx.text("Nenhum veículo cadastrado no momento.", size="3", color="var(--gray-11)"),
                                    align="center",
                                    padding="6",
                                ),
                                width="100%",
                            ),
                            width="100%",
                            border="1px solid var(--gray-4)",
                        ),
                    ),
                    spacing="5",
                    width="100%",
                    on_mount=VehicleState.load_vehicles,
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
app.add_page(vehicles_page, route="/vehicles", on_load=VehicleState.load_vehicles)

"""Componente de navegação reutilizável."""

import reflex as rx
from estacionamento_smart.styles import CONTAINER_MAX_WIDTH


def navbar(auth_state) -> rx.Component:
    """Barra de navegação superior consistente e responsiva."""
    return rx.box(
        rx.center(
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.text("🚗", font_size="1.5em"),
                        rx.heading("Estacionamento Smart", size="5", weight="bold", color="var(--gray-12)"),
                        spacing="2",
                        align="center",
                    ),
                    href="/",
                    text_decoration="none",
                ),
                rx.spacer(),
                rx.cond(
                    auth_state.token != "",
                    rx.hstack(
                        rx.text(rx.cond(auth_state.name != "", auth_state.name, "Usuário"), weight="bold", size="3", color="var(--gray-11)"),
                        rx.button(
                            "Sair",
                            on_click=auth_state.logout,
                            color_scheme="red",
                            variant="soft",
                            size="2",
                            cursor="pointer",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    rx.hstack(
                        rx.link("Entrar", href="/login", font_weight="medium", color="var(--gray-11)"),
                        rx.link(
                            rx.button("Cadastrar-se", variant="solid", color_scheme="indigo", size="2"),
                            href="/signup",
                        ),
                        spacing="4",
                        align="center",
                    ),
                ),
                width="100%",
                max_width=CONTAINER_MAX_WIDTH,
                padding_x="4",
                padding_y="3",
                align="center",
            ),
            width="100%",
        ),
        width="100%",
        border_bottom="1px solid var(--gray-4)",
        background="var(--color-panel)",
        position="sticky",
        top="0",
        z_index="100",
    )

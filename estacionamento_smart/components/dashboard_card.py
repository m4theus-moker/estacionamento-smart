"""Componente de card para o dashboard do sistema."""

import reflex as rx


def dashboard_card(icon: str, title: str, description: str, href: str = "#") -> rx.Component:
    """Card interativo para os módulos do sistema no dashboard."""
    return rx.link(
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text(icon, font_size="1.8em"),
                        padding="3",
                        background="var(--accent-3)",
                        border_radius="var(--radius-3)",
                    ),
                    rx.spacer(),
                    rx.icon("arrow_right", size=20, color="var(--accent-9)"),
                    width="100%",
                    align="center",
                ),
                rx.box(height="2"),
                rx.heading(title, size="5", weight="bold", color="var(--gray-12)"),
                rx.text(description, size="3", color="var(--gray-11)", line_height="1.5"),
                spacing="2",
                align="start",
                width="100%",
            ),
            size="3",
            width="100%",
            height="100%",
            padding="6",
            border="1px solid var(--gray-4)",
            transition="all 0.2s ease-in-out",
            cursor="pointer",
            _hover={
                "transform": "translateY(-4px)",
                "box_shadow": "0 16px 32px rgba(0, 0, 0, 0.08)",
                "border_color": "var(--accent-8)",
                "background": "var(--accent-1)",
            },
        ),
        href=href,
        text_decoration="none",
        width="100%",
    )

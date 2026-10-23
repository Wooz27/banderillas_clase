from streamlit_extras.metric_cards import style_metric_cards

COLOR_TARJETA = "#27272a"
COLOR_BORDE = "#3f3f46"
COLOR_ACENTO = "#6366f1"


def estilo_metric_cards() -> None:
    style_metric_cards(
        background_color=COLOR_TARJETA,
        border_color=COLOR_BORDE,
        border_left_color=COLOR_ACENTO,
        border_radius_px=6,
    )

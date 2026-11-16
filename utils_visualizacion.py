"""Visualizaciones para los resultados calculados en la unidad 014.

Este módulo sólo presenta datos que los cuadernos calculan de manera visible.
No carga documentos, no genera embeddings y no consulta la base vectorial.
"""

from collections.abc import Sequence

import matplotlib.pyplot as plt

AZUL = "#2a78d6"
NARANJA = "#eb6834"
GRIS = "#8b8b86"
TINTA_SUAVE = "#52514e"
LINEA = "#c3c2b7"


def dibujar_barras(
    etiquetas: Sequence[str],
    valores: Sequence[float],
    titulo: str,
    etiqueta_eje_x: str,
    formato: str = "{:.2f}",
) -> None:
    """Dibuja una comparación horizontal de valores ya calculados.

    Args:
        etiquetas: Nombre de cada barra, en el mismo orden que valores.
        valores: Medición que se quiere comparar.
        titulo: Pregunta que responde el gráfico.
        etiqueta_eje_x: Nombre y unidad de la medición.
        formato: Forma de escribir el valor junto a cada barra.
    """
    if len(etiquetas) != len(valores):
        raise ValueError("etiquetas y valores deben tener el mismo largo.")

    if len(etiquetas) == 0:
        raise ValueError("Hace falta al menos un valor para dibujar.")

    figura, ejes = plt.subplots(figsize=(8, 0.65 * len(etiquetas) + 1.4))
    posiciones = list(range(len(etiquetas)))
    ejes.barh(posiciones, valores, color=AZUL, height=0.6)
    ejes.set_yticks(posiciones, etiquetas)
    ejes.invert_yaxis()
    ejes.set_title(titulo, loc="left", fontweight="bold")
    ejes.set_xlabel(etiqueta_eje_x)
    ejes.axvline(0, color=LINEA, linewidth=1)
    ejes.spines["top"].set_visible(False)
    ejes.spines["right"].set_visible(False)
    ejes.spines["left"].set_visible(False)
    ejes.tick_params(axis="y", length=0)

    mayor_valor = max(abs(valor) for valor in valores)
    margen = max(mayor_valor * 0.03, 0.01)

    for posicion in posiciones:
        valor = valores[posicion]
        ejes.text(
            valor + margen,
            posicion,
            formato.format(valor),
            va="center",
            color=TINTA_SUAVE,
        )

    plt.show()


def dibujar_fragmentos(
    fragmentos: Sequence[dict[str, str | int]],
    titulo: str,
) -> None:
    """Muestra fragmentos con su fuente y orden en la selección dibujada.

    Args:
        fragmentos: Registros con las claves texto, fuente e inicio (orden mostrado).
        titulo: Pregunta que responde la visualización.
    """
    if len(fragmentos) == 0:
        raise ValueError("Hace falta al menos un fragmento para dibujar.")

    altura = 1.45 * len(fragmentos) + 0.8
    figura, ejes = plt.subplots(figsize=(10, altura))
    ejes.set_axis_off()
    ejes.set_xlim(0, 1)
    ejes.set_ylim(0, len(fragmentos))
    ejes.set_title(titulo, loc="left", fontweight="bold", pad=12)

    for indice in range(len(fragmentos)):
        fragmento = fragmentos[indice]
        posicion_y = len(fragmentos) - indice - 0.5
        fuente = str(fragmento["fuente"])
        inicio = fragmento["inicio"]
        texto = str(fragmento["texto"]).replace("\n", " ").strip()
        resumen = texto[:180]

        if len(texto) > len(resumen):
            resumen += "…"

        ejes.text(
            0.02,
            posicion_y,
            f"Fragmento {indice + 1} · {fuente} · orden {int(inicio) + 1}\n{resumen}",
            va="center",
            ha="left",
            wrap=True,
            bbox={
                "boxstyle": "round,pad=0.6",
                "facecolor": "#eaf2fb",
                "edgecolor": NARANJA if indice % 2 else AZUL,
                "linewidth": 1.2,
            },
        )

    plt.show()

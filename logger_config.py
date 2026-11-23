"""
Configuración centralizada de Logging para el sistema Software FJ.
Registra eventos y excepciones tanto en consola como en un archivo físico 'software_fj.log'.
"""
import logging
import os

LOG_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "software_fj.log")

def configurar_logger():
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar handlers si se llama varias veces
    if not logger.handlers:
        # Formato detallado de log
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | [%(name)s] [%(filename)s:%(lineno)d] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler de archivo (todos los eventos desde DEBUG)
        file_handler = logging.FileHandler(LOG_FILENAME, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formato)

        # Handler de consola (solo INFO o superior)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = configurar_logger()

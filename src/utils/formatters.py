# src/utils/formatters.py

def fmt_moneda(valor: int) -> str:
    """
    Formatea un número entero con separador de millares en formato de moneda.
    
    Ejemplos:
        1500000 -> "$1.500.000"
        -100000 -> "-$100.000"
        0       -> "$0"
    """
    try:
        val_int = int(valor)
    except (ValueError, TypeError):
        return "$0"

    signo = "-" if val_int < 0 else ""
    val_str = f"{abs(val_int):,}".replace(",", ".")
    return f"{signo}${val_str}"
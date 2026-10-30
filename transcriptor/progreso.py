import time


class Progreso:
    def __init__(self, fase):
        self.fase = fase
        self.inicio = time.monotonic()
        self.ultimo = -10
        print(f"{fase}: 0 % | estimación pendiente", flush=True)

    def __call__(self, actual, total):
        porcentaje = min(100, int(100 * actual / total)) if total else 100
        if porcentaje < self.ultimo + 5 and porcentaje != 100:
            return
        self.ultimo = porcentaje
        segundos = time.monotonic() - self.inicio
        restante = segundos * (total / actual - 1) if actual and total else 0
        print(f"{self.fase}: {porcentaje} % | quedan ~{max(0, restante):.0f} s", flush=True)

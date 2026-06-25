import numpy as np

# ---------------------------------------------------------
# 1. DETEÇÃO DE CICLOS (zero-crossing do fluxo)
# ---------------------------------------------------------
def detect_cycles(time, flow):
    zero_crossings = np.where(np.diff(np.sign(flow)) > 0)[0]
    cycles = []
    for i in range(len(zero_crossings) - 1):
        start = time[zero_crossings[i]]
        end = time[zero_crossings[i + 1]]
        cycles.append((start, end))
    return cycles


# ---------------------------------------------------------
# 2. CÁLCULO DO TRIGGER (primeiro fluxo positivo após início)
# ---------------------------------------------------------
def compute_trigger_delay(time, flow, start):
    idx = np.where(flow > 0)[0]
    if len(idx) == 0:
        return None
    trigger_time = time[idx[0]]
    return (trigger_time - start) * 1000  # ms


# ---------------------------------------------------------
# 3. ANÁLISE COMPLETA DE MÚLTIPLOS CICLOS
# ---------------------------------------------------------
def analyze_multiple_cycles(time, flow, pressure):
    cycles_raw = detect_cycles(time, flow)
    cycles = []

    for start, end in cycles_raw:
        delta_t_trigger = compute_trigger_delay(time, flow, start)

        cycle_info = {
            "cycle_start": start,
            "cycle_end": end,
            "delta_t_trigger_ms": delta_t_trigger,
            "delta_t_cycle_ms": None,  # placeholder
            "synchrony_trigger": (
                "synchronous" if delta_t_trigger is not None and delta_t_trigger < 80 else "late"
            ),
            "synchrony_cycle": "indefinido",
            "inspiratory_state": (
                "active assisted" if delta_t_trigger is not None else "passive assisted"
            )
        }

        cycles.append(cycle_info)

    return {
        "n_cycles": len(cycles),
        "cycles": cycles
    }

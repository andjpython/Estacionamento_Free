# === Ver histórico completo ===
def ver_historico(historico):
    if not historico:
        return "📭 Nenhum registro no histórico."
    return "\n".join([
        f"{h.get('data', h.get('data_saida', ''))}: {h['acao']} - {h.get('placa', '')} - {h.get('nome', '')}"
        for h in historico
    ])

# === Filtrar histórico por matrícula ===
def filtrar_historico_por_matricula(historico, matricula):
    return [h for h in historico if str(h.get('matricula', '')).strip() == str(matricula).strip()] 
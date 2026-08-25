def calculate_priority(data):
    score, reasons = 0, []
    rules = [
        ("not_healing", 4, "ferida sem cicatrização há quatro semanas"),
        ("bleeding", 3, "presença de sangramento"),
        ("changed", 3, "mudança recente de tamanho, formato ou cor"),
        ("personal_history", 3, "histórico pessoal informado"),
        ("itching_or_pain", 1, "coceira ou dor"),
        ("family_history", 1, "histórico familiar informado"),
    ]
    for field, points, label in rules:
        if data.get(field):
            score += points
            reasons.append(label)
    priority = "urgent" if score >= 6 else "soon" if score >= 3 else "routine"
    if not reasons:
        reasons = ["nenhum sinal de alerta foi informado no questionário"]
    return priority, score, reasons

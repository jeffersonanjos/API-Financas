# Categorização baseada em palavras-chave (sem ML complexo)
def categorize_transaction(descricao):
    descricao = descricao.lower()
    if "comida" in descricao or "restaurante" in descricao:
        return "Alimentação"
    elif "uber" in descricao or "taxi" in descricao:
        return "Transporte"
    else:
        return "Outros"

# NLP "fake" (respostas pré-definidas)
def nlp_query(pergunta):
    pergunta = pergunta.lower()
    if "quanto gastei" in pergunta and "comida" in pergunta:
        return "Você gastou R$ 350 este mês com alimentação."
    else:
        return "Não entendi. Pergunte algo como 'Quanto gastei com comida?'"
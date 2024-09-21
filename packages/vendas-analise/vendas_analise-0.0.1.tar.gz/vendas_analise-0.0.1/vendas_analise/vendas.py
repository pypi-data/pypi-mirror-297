from collections import Counter

def contagem_de_vendas(*conjuntos):
    # Une os conjuntos de vendas e transforma em uma lista de produtos
    produtos = [produto for conjunto in conjuntos for produto in conjunto]
    # Retorna um objeto Counter com as contagens de produtos
    return Counter(produtos)

def produto_mais_vendido(*conjuntos):
    # Obtém a contagem de vendas usando a função contagem_de_vendas
    contagem = contagem_de_vendas(*conjuntos)    
    # Se não houver produtos, retorna None
    if not contagem:
        return None    
    # Obtém o valor máximo de vendas
    max_vendas = max(contagem.values())    
    mais_vendido = []

    # Itera sobre a contagem de produtos
    for produto, quantidade in contagem.items(): 
        # Se a quantidade do produto for igual ao máximo, adiciona à lista
        if quantidade == max_vendas:
            mais_vendido.append((produto, quantidade))

    # Retorna a lista de produtos mais vendidos
    return mais_vendido

def produto_menos_vendido(*conjuntos):
    # Obtém a contagem de vendas usando a função contagem_de_vendas
    contagem = contagem_de_vendas(*conjuntos)    
    # Se não houver produtos, retorna None
    if not contagem:
        return None    
    # Obtém o valor mínimo de vendas
    min_vendas = min(contagem.values())    
    menos_vendido = []

    # Itera sobre a contagem de produtos
    for produto, quantidade in contagem.items(): 
        # Se a quantidade do produto for igual ao mínimo, adiciona à lista
        if quantidade == min_vendas:
            menos_vendido.append((produto, quantidade))

    # Retorna a lista de produtos menos vendidos
    return menos_vendido



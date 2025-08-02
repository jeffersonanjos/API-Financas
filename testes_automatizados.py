#!/usr/bin/env python3
"""
Testes automatizados da API de Finanças Pessoais
Testa TODOS os endpoints e métodos disponíveis
"""

import requests
import json
from datetime import datetime, timedelta

# Configuração
BASE_URL = "http://localhost:8000"

def print_response(response, title=""):
    """Imprime a resposta de forma organizada"""
    print(f"\n{'='*50}")
    if title:
        print(f"📋 {title}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print(f"{'='*50}")

def test_root_endpoint():
    """Testa o endpoint raiz"""
    print("\n🏠 Testando endpoint raiz...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Endpoint raiz")
    return response.status_code == 200

def test_transactions():
    """Testa TODOS os endpoints de transações"""
    print("\n🔄 Testando TODOS os endpoints de transações...")
    
    # 1. POST /transactions/ - Criar transações
    transactions = [
        {
            "description": "Salário",
            "amount": 5000.00,
            "type": "receita",
            "category": "outros"
        },
        {
            "description": "Aluguel",
            "amount": 1200.00,
            "type": "despesa",
            "category": "contas"
        },
        {
            "description": "Supermercado",
            "amount": 350.00,
            "type": "despesa",
            "category": "alimentacao"
        },
        {
            "description": "Cinema",
            "amount": 50.00,
            "type": "despesa",
            "category": "lazer"
        }
    ]
    
    created_ids = []
    for i, transaction in enumerate(transactions, 1):
        response = requests.post(f"{BASE_URL}/transactions/", json=transaction)
        print_response(response, f"POST /transactions/ - Criando transação {i}")
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
    
    # 2. GET /transactions/ - Listar todas as transações
    response = requests.get(f"{BASE_URL}/transactions/")
    print_response(response, "GET /transactions/ - Listando todas as transações")
    
    # 3. GET /transactions/ com filtros - Filtrar por tipo
    response = requests.get(f"{BASE_URL}/transactions/?transaction_type=receita")
    print_response(response, "GET /transactions/?transaction_type=receita - Filtrando apenas receitas")
    
    # 4. GET /transactions/ com filtros - Filtrar por categoria
    response = requests.get(f"{BASE_URL}/transactions/?category=alimentacao")
    print_response(response, "GET /transactions/?category=alimentacao - Filtrando por categoria alimentação")
    
    # 5. GET /transactions/{id} - Buscar transação específica
    if created_ids:
        response = requests.get(f"{BASE_URL}/transactions/{created_ids[0]}")
        print_response(response, f"GET /transactions/{created_ids[0]} - Buscando transação específica")
    
    # 6. PUT /transactions/{id} - Atualizar transação
    if created_ids:
        update_data = {"amount": 1300.00, "description": "Aluguel atualizado"}
        response = requests.put(f"{BASE_URL}/transactions/{created_ids[1]}", json=update_data)
        print_response(response, f"PUT /transactions/{created_ids[1]} - Atualizando transação")
    
    # 7. DELETE /transactions/{id} - Deletar transação
    if created_ids:
        response = requests.delete(f"{BASE_URL}/transactions/{created_ids[-1]}")
        print_response(response, f"DELETE /transactions/{created_ids[-1]} - Deletando transação")
        # Remove o ID deletado da lista
        created_ids.pop()
    
    # 8. GET /transactions/summary/category - Resumo por categoria
    response = requests.get(f"{BASE_URL}/transactions/summary/category")
    print_response(response, "GET /transactions/summary/category - Resumo por categoria")
    
    # 9. GET /transactions/summary/balance - Resumo de saldo
    response = requests.get(f"{BASE_URL}/transactions/summary/balance")
    print_response(response, "GET /transactions/summary/balance - Resumo de saldo")
    
    return created_ids

def test_goals():
    """Testa TODOS os endpoints de metas"""
    print("\n🎯 Testando TODOS os endpoints de metas...")
    
    # 1. POST /goals/ - Criar metas
    goals = [
        {
            "title": "Viagem para Europa",
            "description": "Economizar para viagem de 15 dias",
            "target_amount": 15000.00,
            "deadline": (datetime.now() + timedelta(days=180)).isoformat()
        },
        {
            "title": "Notebook novo",
            "description": "Comprar um notebook para trabalho",
            "target_amount": 3000.00,
            "deadline": (datetime.now() + timedelta(days=90)).isoformat()
        }
    ]
    
    created_goal_ids = []
    for i, goal in enumerate(goals, 1):
        response = requests.post(f"{BASE_URL}/goals/", json=goal)
        print_response(response, f"POST /goals/ - Criando meta {i}")
        if response.status_code == 200:
            created_goal_ids.append(response.json()["id"])
    
    # 2. GET /goals/ - Listar todas as metas
    response = requests.get(f"{BASE_URL}/goals/")
    print_response(response, "GET /goals/ - Listando todas as metas")
    
    # 3. GET /goals/ com filtros - Filtrar por status
    response = requests.get(f"{BASE_URL}/goals/?status=ativa")
    print_response(response, "GET /goals/?status=ativa - Filtrando metas ativas")
    
    # 4. GET /goals/{id} - Buscar meta específica
    if created_goal_ids:
        response = requests.get(f"{BASE_URL}/goals/{created_goal_ids[0]}")
        print_response(response, f"GET /goals/{created_goal_ids[0]} - Buscando meta específica")
    
    # 5. PUT /goals/{id} - Atualizar meta
    if created_goal_ids:
        update_data = {"title": "Viagem para Europa (Atualizada)", "description": "Meta atualizada"}
        response = requests.put(f"{BASE_URL}/goals/{created_goal_ids[0]}", json=update_data)
        print_response(response, f"PUT /goals/{created_goal_ids[0]} - Atualizando meta")
    
    # 6. PUT /goals/{id}/progress - Atualizar progresso de uma meta
    if created_goal_ids:
        response = requests.put(f"{BASE_URL}/goals/{created_goal_ids[0]}/progress?amount=5000.00")
        print_response(response, f"PUT /goals/{created_goal_ids[0]}/progress - Atualizando progresso da meta")
        
        # Atualizar mais uma vez para ver o status mudar
        response = requests.put(f"{BASE_URL}/goals/{created_goal_ids[0]}/progress?amount=10000.00")
        print_response(response, f"PUT /goals/{created_goal_ids[0]}/progress - Meta deve ficar concluída")
    
    # 7. DELETE /goals/{id} - Deletar meta
    if created_goal_ids:
        response = requests.delete(f"{BASE_URL}/goals/{created_goal_ids[-1]}")
        print_response(response, f"DELETE /goals/{created_goal_ids[-1]} - Deletando meta")
        # Remove o ID deletado da lista
        created_goal_ids.pop()
    
    return created_goal_ids

def test_error_cases():
    """Testa casos de erro para validar tratamento de exceções"""
    print("\n⚠️ Testando casos de erro...")
    
    # 1. GET /transactions/{id} - ID inexistente
    response = requests.get(f"{BASE_URL}/transactions/99999")
    print_response(response, "GET /transactions/99999 - ID inexistente (deve retornar 404)")
    
    # 2. PUT /transactions/{id} - ID inexistente
    update_data = {"amount": 100.00}
    response = requests.put(f"{BASE_URL}/transactions/99999", json=update_data)
    print_response(response, "PUT /transactions/99999 - ID inexistente (deve retornar 404)")
    
    # 3. DELETE /transactions/{id} - ID inexistente
    response = requests.delete(f"{BASE_URL}/transactions/99999")
    print_response(response, "DELETE /transactions/99999 - ID inexistente (deve retornar 404)")
    
    # 4. GET /goals/{id} - ID inexistente
    response = requests.get(f"{BASE_URL}/goals/99999")
    print_response(response, "GET /goals/99999 - ID inexistente (deve retornar 404)")
    
    # 5. PUT /goals/{id} - ID inexistente
    update_data = {"title": "Teste"}
    response = requests.put(f"{BASE_URL}/goals/99999", json=update_data)
    print_response(response, "PUT /goals/99999 - ID inexistente (deve retornar 404)")
    
    # 6. DELETE /goals/{id} - ID inexistente
    response = requests.delete(f"{BASE_URL}/goals/99999")
    print_response(response, "DELETE /goals/99999 - ID inexistente (deve retornar 404)")

def main():
    """Função principal"""
    print("🚀 Iniciando testes COMPLETOS da API de Finanças Pessoais")
    print(f"📡 Conectando em: {BASE_URL}")
    
    try:
        # Testar se a API está rodando
        if not test_root_endpoint():
            print("❌ API não está respondendo")
            return
        
        # Testar transações (TODOS os endpoints)
        transaction_ids = test_transactions()
        
        # Testar metas (TODOS os endpoints)
        goal_ids = test_goals()
        
        # Testar casos de erro
        test_error_cases()
        
        print("\n🎉 TODOS os testes foram executados com sucesso!")
        print(f"📊 Transações criadas: {len(transaction_ids)}")
        print(f"🎯 Metas criadas: {len(goal_ids)}")
        print("\n✅ Endpoints testados:")
        print("   🏠 GET / (Root)")
        print("   📊 POST /transactions/ (Criar)")
        print("   📊 GET /transactions/ (Listar)")
        print("   📊 GET /transactions/{id} (Buscar)")
        print("   📊 PUT /transactions/{id} (Atualizar)")
        print("   📊 DELETE /transactions/{id} (Deletar)")
        print("   📊 GET /transactions/summary/category (Resumo categoria)")
        print("   📊 GET /transactions/summary/balance (Resumo saldo)")
        print("   🎯 POST /goals/ (Criar)")
        print("   🎯 GET /goals/ (Listar)")
        print("   🎯 GET /goals/{id} (Buscar)")
        print("   🎯 PUT /goals/{id} (Atualizar)")
        print("   🎯 DELETE /goals/{id} (Deletar)")
        print("   🎯 PUT /goals/{id}/progress (Progresso)")
        print("   ⚠️ Casos de erro (404)")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("💡 Certifique-se de que o servidor está rodando com: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main() 
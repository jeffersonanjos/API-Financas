# API de Finanças Pessoais

## Visão Geral

Sistema de gestão financeira pessoal desenvolvido com FastAPI, oferecendo controle completo de transações e metas financeiras.

## Tecnologias

- **Backend**: Python + FastAPI
- **Banco de Dados**: SQLite
- **ORM**: SQLModel
- **Documentação**: Swagger UI automática

## Instalação e Execução

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a aplicação
```bash
uvicorn main:app --reload
```

### 3. Acessar a documentação
- **Swagger UI**: http://localhost:8000/docs

## Funcionalidades

### Transações
- ✅ **CRUD completo** de transações
- ✅ **Filtros** por tipo (receita/despesa) e categoria
- ✅ **Resumo por categoria** com totais
- ✅ **Cálculo de saldo** (receitas - despesas)

### Metas Financeiras
- ✅ **CRUD completo** de metas
- ✅ **Controle de progresso** das metas
- ✅ **Status automático** (ativa/concluída/cancelada)
- ✅ **Filtros** por status

## Endpoints Principais

### Transações
- `POST /transactions/` - Criar transação
- `GET /transactions/` - Listar transações (com filtros)
- `GET /transactions/{id}` - Buscar transação específica
- `PUT /transactions/{id}` - Atualizar transação
- `DELETE /transactions/{id}` - Deletar transação
- `GET /transactions/summary/category` - Resumo por categoria
- `GET /transactions/summary/balance` - Resumo de saldo

### Metas
- `POST /goals/` - Criar meta
- `GET /goals/` - Listar metas (com filtros)
- `GET /goals/{id}` - Buscar meta específica
- `PUT /goals/{id}` - Atualizar meta
- `DELETE /goals/{id}` - Deletar meta
- `PUT /goals/{id}/progress` - Atualizar progresso da meta

## Estrutura do Projeto

```
finances-api/
├── main.py              # Aplicação FastAPI
├── database.py          # Configuração do banco
├── requirements.txt     # Dependências
├── finances.db         # Banco SQLite
├── testes_automatizados.py  # Testes da API
└── models/
    ├── transaction.py   # Modelos de transação
    └── goal.py         # Modelos de meta
```

## Testes Automatizados

O arquivo `testes_automatizados.py` contém testes que verificam se todos os endpoints estão funcionando corretamente.

### Como executar os testes:
```bash
python testes_automatizados.py
```

### O que os testes verificam:
- ✅ **Conexão com a API** - Testa se o servidor está rodando
- ✅ **CRUD de transações** - Cria, lista, filtra e atualiza transações
- ✅ **Relatórios** - Verifica resumos por categoria e saldo
- ✅ **CRUD de metas** - Cria, lista e atualiza progresso das metas
- ✅ **Status automático** - Confirma que metas ficam "concluídas" quando atingem o valor alvo

### Exemplo de saída dos testes:
```
🚀 Iniciando testes da API de Finanças Pessoais
✅ API está funcionando!
📊 Transações criadas: 4
🎯 Metas criadas: 2
🎉 Todos os testes foram executados com sucesso!
```

## Exemplos de Uso

### Criar uma transação
```bash
curl -X POST "http://localhost:8000/transactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Salário",
    "amount": 5000.00,
    "type": "receita",
    "category": "outros"
  }'
```

### Criar uma meta
```bash
curl -X POST "http://localhost:8000/goals/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Viagem para Europa",
    "description": "Economizar para viagem",
    "target_amount": 15000.00,
    "deadline": "2024-12-31T23:59:59"
  }'
```

### Atualizar progresso de uma meta
```bash
curl -X PUT "http://localhost:8000/goals/1/progress?amount=1000.00"
```

## Características

- **Simplicidade**: Código limpo e bem organizado
- **Funcionalidade**: Todas as operações básicas implementadas
- **Documentação**: Swagger UI automática
- **Validação**: Validação automática de dados com Pydantic
- **Flexibilidade**: Filtros e paginação nos endpoints


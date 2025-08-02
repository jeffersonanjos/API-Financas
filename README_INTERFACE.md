# Interface Gráfica - API de Finanças Pessoais

## Visão Geral

Interface gráfica completa desenvolvida com Tkinter para consumir todos os endpoints da API de Finanças Pessoais.

## Como Executar

### 1. Certifique-se de que a API está rodando
```bash
uvicorn main:app --reload
```

### 2. Execute a interface gráfica
```bash
python interface_gui.py
```

## Funcionalidades da Interface

### 📊 Aba de Transações

#### **Formulário de Nova Transação:**
- **Descrição**: Nome da transação
- **Valor**: Valor em reais (ex: 100.50)
- **Tipo**: Receita ou Despesa
- **Categoria**: Alimentação, Lazer, Saúde, Contas, Outros

#### **Lista de Transações:**
- Visualização em tabela com todas as transações
- **Filtros**: Por tipo (receita/despesa) e categoria
- **Ações**: Atualizar, Editar, Deletar

### 🎯 Aba de Metas

#### **Formulário de Nova Meta:**
- **Título**: Nome da meta
- **Descrição**: Detalhes da meta
- **Valor Alvo**: Valor que deseja atingir
- **Data Limite**: Data para atingir a meta

#### **Lista de Metas:**
- Visualização com progresso em porcentagem
- **Filtros**: Por status (ativa/concluída/cancelada)
- **Ações**: Atualizar, Editar, Deletar, Adicionar Progresso

### 📈 Aba de Relatórios

#### **Resumo de Saldo:**
- Total de receitas
- Total de despesas
- Saldo atual
- Status (positivo/negativo)

#### **Resumo por Categoria:**
- Total gasto por categoria
- Número de transações por categoria
- Análise detalhada dos gastos

## Endpoints Consumidos

### Transações:
- ✅ `POST /transactions/` - Criar transação
- ✅ `GET /transactions/` - Listar transações
- ✅ `DELETE /transactions/{id}` - Deletar transação
- ✅ `GET /transactions/summary/category` - Resumo por categoria
- ✅ `GET /transactions/summary/balance` - Resumo de saldo

### Metas:
- ✅ `POST /goals/` - Criar meta
- ✅ `GET /goals/` - Listar metas
- ✅ `DELETE /goals/{id}` - Deletar meta
- ✅ `PUT /goals/{id}/progress` - Adicionar progresso

## Características da Interface

### 🎨 **Design:**
- Interface moderna com abas organizadas
- Formulários intuitivos
- Tabelas com scroll e ordenação
- Barra de status informativa

### 🔧 **Funcionalidades:**
- **Validação de dados**: Verifica se valores são números válidos
- **Tratamento de erros**: Mensagens claras para o usuário
- **Atualização automática**: Listas se atualizam após operações
- **Filtros dinâmicos**: Filtra dados em tempo real

### 📱 **Usabilidade:**
- **Interface responsiva**: Adapta-se ao tamanho da janela
- **Navegação intuitiva**: Abas bem organizadas
- **Feedback visual**: Mensagens de sucesso/erro
- **Confirmações**: Pede confirmação para deletar

## Como Usar

### 1. **Criar Transação:**
1. Vá para a aba "📊 Transações"
2. Preencha o formulário à esquerda
3. Clique em "Criar Transação"
4. A transação aparecerá na lista à direita

### 2. **Criar Meta:**
1. Vá para a aba "🎯 Metas"
2. Preencha o formulário à esquerda
3. Clique em "Criar Meta"
4. A meta aparecerá na lista à direita

### 3. **Adicionar Progresso à Meta:**
1. Selecione uma meta na lista
2. Clique em "Adicionar Progresso"
3. Digite o valor a adicionar
4. Clique em "Confirmar"

### 4. **Ver Relatórios:**
1. Vá para a aba "📈 Relatórios"
2. Clique em "Atualizar Resumo" e "Atualizar Categorias"
3. Visualize os dados em tempo real

### 5. **Filtrar Dados:**
1. Use os filtros nas listas
2. Selecione o tipo de filtro desejado
3. Clique em "Aplicar Filtros"
4. Use "Limpar Filtros" para voltar ao estado original

## Requisitos

- Python 3.7+
- Tkinter (geralmente vem com Python)
- Requests (já instalado no projeto)
- API rodando em http://localhost:8000

## Troubleshooting

### **Interface não abre:**
- Verifique se o Python está instalado
- Verifique se o Tkinter está disponível

### **Erro de conexão:**
- Certifique-se de que a API está rodando
- Verifique se a URL está correta (http://localhost:8000)

### **Dados não carregam:**
- Verifique se a API está respondendo
- Clique em "Atualizar Lista" nas abas

## Vantagens da Interface

1. **Simplicidade**: Interface intuitiva e fácil de usar
2. **Completude**: Consome todos os endpoints da API
3. **Visualização**: Dados organizados em tabelas
4. **Relatórios**: Análises em tempo real
5. **Produtividade**: Operações rápidas e eficientes 
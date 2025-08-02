#!/usr/bin/env python3
"""
Interface gráfica para API de Finanças Pessoais
Interface completa usando Tkinter para consumir todos os endpoints
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime
from typing import Dict, Any

class FinancesAPIInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("API de Finanças Pessoais - Interface")
        self.root.geometry("1200x800")
        
        # Configuração da API
        self.base_url = "http://localhost:8000"
        
        # Variáveis para armazenar dados
        self.transactions = []
        self.goals = []
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de Transações
        self.transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.transactions_frame, text="📊 Transações")
        self.setup_transactions_tab()
        
        # Aba de Metas
        self.goals_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.goals_frame, text="🎯 Metas")
        self.setup_goals_tab()
        
        # Aba de Relatórios
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="📈 Relatórios")
        self.setup_reports_tab()
        
        # Barra de status
        self.status_bar = ttk.Label(self.root, text="Pronto", relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')
    
    def setup_transactions_tab(self):
        """Configura a aba de transações"""
        # Frame principal
        main_frame = ttk.Frame(self.transactions_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame esquerdo - Formulário
        left_frame = ttk.LabelFrame(main_frame, text="Nova Transação")
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Campos do formulário
        ttk.Label(left_frame, text="Descrição:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.transaction_description = ttk.Entry(left_frame, width=30)
        self.transaction_description.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Valor:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.transaction_amount = ttk.Entry(left_frame, width=30)
        self.transaction_amount.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Tipo:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.transaction_type = ttk.Combobox(left_frame, values=["receita", "despesa"], state="readonly")
        self.transaction_type.grid(row=2, column=1, padx=5, pady=5)
        self.transaction_type.set("despesa")
        
        ttk.Label(left_frame, text="Categoria:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.transaction_category = ttk.Combobox(left_frame, 
                                               values=["alimentacao", "lazer", "saude", "contas", "outros"], 
                                               state="readonly")
        self.transaction_category.grid(row=3, column=1, padx=5, pady=5)
        self.transaction_category.set("outros")
        
        # Botões
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Criar Transação", command=self.create_transaction).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpar Formulário", command=self.clear_transaction_form).pack(side='left', padx=5)
        
        # Frame direito - Lista de transações
        right_frame = ttk.LabelFrame(main_frame, text="Transações")
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Filtros
        filter_frame = ttk.Frame(right_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar por:").pack(side='left')
        self.filter_type = ttk.Combobox(filter_frame, values=["Todos", "receita", "despesa"], state="readonly")
        self.filter_type.pack(side='left', padx=5)
        self.filter_type.set("Todos")
        
        self.filter_category = ttk.Combobox(filter_frame, 
                                          values=["Todas", "alimentacao", "lazer", "saude", "contas", "outros"], 
                                          state="readonly")
        self.filter_category.pack(side='left', padx=5)
        self.filter_category.set("Todas")
        
        ttk.Button(filter_frame, text="Aplicar Filtros", command=self.filter_transactions).pack(side='left', padx=5)
        ttk.Button(filter_frame, text="Limpar Filtros", command=self.clear_filters).pack(side='left', padx=5)
        
        # Treeview para transações
        columns = ('ID', 'Descrição', 'Valor', 'Tipo', 'Categoria', 'Data')
        self.transactions_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=100)
        
        self.transactions_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.transactions_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botões de ação
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_frame, text="Atualizar Lista", command=self.load_transactions).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Editar Selecionada", command=self.edit_transaction).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Deletar Selecionada", command=self.delete_transaction).pack(side='left', padx=5)
    
    def setup_goals_tab(self):
        """Configura a aba de metas"""
        # Frame principal
        main_frame = ttk.Frame(self.goals_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame esquerdo - Formulário
        left_frame = ttk.LabelFrame(main_frame, text="Nova Meta")
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Campos do formulário
        ttk.Label(left_frame, text="Título:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.goal_title = ttk.Entry(left_frame, width=30)
        self.goal_title.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Descrição:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.goal_description = ttk.Entry(left_frame, width=30)
        self.goal_description.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Valor Alvo:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.goal_target_amount = ttk.Entry(left_frame, width=30)
        self.goal_target_amount.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Data Limite:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.goal_deadline = ttk.Entry(left_frame, width=30)
        self.goal_deadline.grid(row=3, column=1, padx=5, pady=5)
        self.goal_deadline.insert(0, "2024-12-31")
        
        # Botões
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Criar Meta", command=self.create_goal).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpar Formulário", command=self.clear_goal_form).pack(side='left', padx=5)
        
        # Frame direito - Lista de metas
        right_frame = ttk.LabelFrame(main_frame, text="Metas")
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Filtros
        filter_frame = ttk.Frame(right_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar por status:").pack(side='left')
        self.filter_status = ttk.Combobox(filter_frame, values=["Todas", "ativa", "concluida", "cancelada"], state="readonly")
        self.filter_status.pack(side='left', padx=5)
        self.filter_status.set("Todas")
        
        ttk.Button(filter_frame, text="Aplicar Filtro", command=self.filter_goals).pack(side='left', padx=5)
        ttk.Button(filter_frame, text="Limpar Filtro", command=self.clear_goal_filters).pack(side='left', padx=5)
        
        # Treeview para metas
        columns = ('ID', 'Título', 'Valor Alvo', 'Valor Atual', 'Progresso', 'Status', 'Data Limite')
        self.goals_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.goals_tree.heading(col, text=col)
            self.goals_tree.column(col, width=100)
        
        self.goals_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.goals_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.goals_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botões de ação
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_frame, text="Atualizar Lista", command=self.load_goals).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Editar Selecionada", command=self.edit_goal).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Deletar Selecionada", command=self.delete_goal).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Adicionar Progresso", command=self.add_goal_progress).pack(side='left', padx=5)
    
    def setup_reports_tab(self):
        """Configura a aba de relatórios"""
        # Frame principal
        main_frame = ttk.Frame(self.reports_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame esquerdo - Resumo de saldo
        left_frame = ttk.LabelFrame(main_frame, text="Resumo de Saldo")
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.balance_text = scrolledtext.ScrolledText(left_frame, height=10, width=50)
        self.balance_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Button(left_frame, text="Atualizar Resumo", command=self.load_balance_summary).pack(pady=5)
        
        # Frame direito - Resumo por categoria
        right_frame = ttk.LabelFrame(main_frame, text="Resumo por Categoria")
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.category_text = scrolledtext.ScrolledText(right_frame, height=10, width=50)
        self.category_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Button(right_frame, text="Atualizar Categorias", command=self.load_category_summary).pack(pady=5)
    
    def load_data(self):
        """Carrega dados iniciais"""
        self.load_transactions()
        self.load_goals()
        self.load_balance_summary()
        self.load_category_summary()
    
    def create_transaction(self):
        """Cria uma nova transação"""
        try:
            data = {
                "description": self.transaction_description.get(),
                "amount": float(self.transaction_amount.get()),
                "type": self.transaction_type.get(),
                "category": self.transaction_category.get()
            }
            
            response = requests.post(f"{self.base_url}/transactions/", json=data)
            
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Transação criada com sucesso!")
                self.clear_transaction_form()
                self.load_transactions()
            else:
                messagebox.showerror("Erro", f"Erro ao criar transação: {response.text}")
                
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número válido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def create_goal(self):
        """Cria uma nova meta"""
        try:
            data = {
                "title": self.goal_title.get(),
                "description": self.goal_description.get(),
                "target_amount": float(self.goal_target_amount.get()),
                "deadline": f"{self.goal_deadline.get()}T23:59:59"
            }
            
            response = requests.post(f"{self.base_url}/goals/", json=data)
            
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Meta criada com sucesso!")
                self.clear_goal_form()
                self.load_goals()
            else:
                messagebox.showerror("Erro", f"Erro ao criar meta: {response.text}")
                
        except ValueError:
            messagebox.showerror("Erro", "Valor alvo deve ser um número válido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def load_transactions(self):
        """Carrega lista de transações"""
        try:
            response = requests.get(f"{self.base_url}/transactions/")
            
            if response.status_code == 200:
                self.transactions = response.json()
                self.update_transactions_tree()
                self.status_bar.config(text=f"Transações carregadas: {len(self.transactions)}")
            else:
                messagebox.showerror("Erro", f"Erro ao carregar transações: {response.text}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def load_goals(self):
        """Carrega lista de metas"""
        try:
            response = requests.get(f"{self.base_url}/goals/")
            
            if response.status_code == 200:
                self.goals = response.json()
                self.update_goals_tree()
                self.status_bar.config(text=f"Metas carregadas: {len(self.goals)}")
            else:
                messagebox.showerror("Erro", f"Erro ao carregar metas: {response.text}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def update_transactions_tree(self):
        """Atualiza a treeview de transações"""
        # Limpa a treeview
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        # Adiciona os dados
        for transaction in self.transactions:
            date = transaction['date'][:10] if transaction['date'] else "N/A"
            self.transactions_tree.insert('', 'end', values=(
                transaction['id'],
                transaction['description'],
                f"R$ {transaction['amount']:.2f}",
                transaction['type'],
                transaction['category'],
                date
            ))
    
    def update_goals_tree(self):
        """Atualiza a treeview de metas"""
        # Limpa a treeview
        for item in self.goals_tree.get_children():
            self.goals_tree.delete(item)
        
        # Adiciona os dados
        for goal in self.goals:
            progress = (goal['current_amount'] / goal['target_amount']) * 100 if goal['target_amount'] > 0 else 0
            deadline = goal['deadline'][:10] if goal['deadline'] else "N/A"
            self.goals_tree.insert('', 'end', values=(
                goal['id'],
                goal['title'],
                f"R$ {goal['target_amount']:.2f}",
                f"R$ {goal['current_amount']:.2f}",
                f"{progress:.1f}%",
                goal['status'],
                deadline
            ))
    
    def filter_transactions(self):
        """Filtra transações"""
        try:
            params = {}
            if self.filter_type.get() != "Todos":
                params['transaction_type'] = self.filter_type.get()
            if self.filter_category.get() != "Todas":
                params['category'] = self.filter_category.get()
            
            response = requests.get(f"{self.base_url}/transactions/", params=params)
            
            if response.status_code == 200:
                self.transactions = response.json()
                self.update_transactions_tree()
                self.status_bar.config(text=f"Transações filtradas: {len(self.transactions)}")
            else:
                messagebox.showerror("Erro", f"Erro ao filtrar transações: {response.text}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def filter_goals(self):
        """Filtra metas"""
        try:
            params = {}
            if self.filter_status.get() != "Todas":
                params['status'] = self.filter_status.get()
            
            response = requests.get(f"{self.base_url}/goals/", params=params)
            
            if response.status_code == 200:
                self.goals = response.json()
                self.update_goals_tree()
                self.status_bar.config(text=f"Metas filtradas: {len(self.goals)}")
            else:
                messagebox.showerror("Erro", f"Erro ao filtrar metas: {response.text}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def clear_filters(self):
        """Limpa filtros de transações"""
        self.filter_type.set("Todos")
        self.filter_category.set("Todas")
        self.load_transactions()
    
    def clear_goal_filters(self):
        """Limpa filtros de metas"""
        self.filter_status.set("Todas")
        self.load_goals()
    
    def clear_transaction_form(self):
        """Limpa formulário de transação"""
        self.transaction_description.delete(0, tk.END)
        self.transaction_amount.delete(0, tk.END)
        self.transaction_type.set("despesa")
        self.transaction_category.set("outros")
    
    def clear_goal_form(self):
        """Limpa formulário de meta"""
        self.goal_title.delete(0, tk.END)
        self.goal_description.delete(0, tk.END)
        self.goal_target_amount.delete(0, tk.END)
        self.goal_deadline.delete(0, tk.END)
        self.goal_deadline.insert(0, "2024-12-31")
    
    def edit_transaction(self):
        """Edita transação selecionada"""
        selection = self.transactions_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma transação para editar!")
            return
        
        # Implementar janela de edição
        messagebox.showinfo("Info", "Funcionalidade de edição será implementada!")
    
    def delete_transaction(self):
        """Deleta transação selecionada"""
        selection = self.transactions_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma transação para deletar!")
            return
        
        item = self.transactions_tree.item(selection[0])
        transaction_id = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Deletar transação ID {transaction_id}?"):
            try:
                response = requests.delete(f"{self.base_url}/transactions/{transaction_id}")
                
                if response.status_code == 200:
                    messagebox.showinfo("Sucesso", "Transação deletada com sucesso!")
                    self.load_transactions()
                else:
                    messagebox.showerror("Erro", f"Erro ao deletar transação: {response.text}")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def edit_goal(self):
        """Edita meta selecionada"""
        selection = self.goals_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma meta para editar!")
            return
        
        # Implementar janela de edição
        messagebox.showinfo("Info", "Funcionalidade de edição será implementada!")
    
    def delete_goal(self):
        """Deleta meta selecionada"""
        selection = self.goals_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma meta para deletar!")
            return
        
        item = self.goals_tree.item(selection[0])
        goal_id = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Deletar meta ID {goal_id}?"):
            try:
                response = requests.delete(f"{self.base_url}/goals/{goal_id}")
                
                if response.status_code == 200:
                    messagebox.showinfo("Sucesso", "Meta deletada com sucesso!")
                    self.load_goals()
                else:
                    messagebox.showerror("Erro", f"Erro ao deletar meta: {response.text}")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def add_goal_progress(self):
        """Adiciona progresso à meta selecionada"""
        selection = self.goals_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma meta para adicionar progresso!")
            return
        
        # Janela para inserir valor
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Progresso")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Valor a adicionar:").pack(pady=10)
        amount_entry = ttk.Entry(dialog)
        amount_entry.pack(pady=5)
        amount_entry.focus()
        
        def confirm():
            try:
                amount = float(amount_entry.get())
                item = self.goals_tree.item(selection[0])
                goal_id = item['values'][0]
                
                response = requests.put(f"{self.base_url}/goals/{goal_id}/progress?amount={amount}")
                
                if response.status_code == 200:
                    messagebox.showinfo("Sucesso", "Progresso adicionado com sucesso!")
                    self.load_goals()
                    dialog.destroy()
                else:
                    messagebox.showerror("Erro", f"Erro ao adicionar progresso: {response.text}")
                    
            except ValueError:
                messagebox.showerror("Erro", "Valor deve ser um número válido!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
        
        ttk.Button(dialog, text="Confirmar", command=confirm).pack(pady=10)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).pack(pady=5)
    
    def load_balance_summary(self):
        """Carrega resumo de saldo"""
        try:
            response = requests.get(f"{self.base_url}/transactions/summary/balance")
            
            if response.status_code == 200:
                data = response.json()
                summary = f"""RESUMO DE SALDO

Total de Receitas: R$ {data['total_receitas']:.2f}
Total de Despesas: R$ {data['total_despesas']:.2f}
Saldo: R$ {data['saldo']:.2f}

Status: {'✅ Positivo' if data['saldo'] >= 0 else '❌ Negativo'}
"""
                self.balance_text.delete(1.0, tk.END)
                self.balance_text.insert(1.0, summary)
            else:
                self.balance_text.delete(1.0, tk.END)
                self.balance_text.insert(1.0, f"Erro ao carregar resumo: {response.text}")
                
        except Exception as e:
            self.balance_text.delete(1.0, tk.END)
            self.balance_text.insert(1.0, f"Erro inesperado: {str(e)}")
    
    def load_category_summary(self):
        """Carrega resumo por categoria"""
        try:
            response = requests.get(f"{self.base_url}/transactions/summary/category")
            
            if response.status_code == 200:
                data = response.json()
                summary = "RESUMO POR CATEGORIA\n\n"
                
                for category in data:
                    summary += f"{category['category'].upper()}:\n"
                    summary += f"  Total: R$ {category['total_amount']:.2f}\n"
                    summary += f"  Transações: {category['transaction_count']}\n\n"
                
                self.category_text.delete(1.0, tk.END)
                self.category_text.insert(1.0, summary)
            else:
                self.category_text.delete(1.0, tk.END)
                self.category_text.insert(1.0, f"Erro ao carregar categorias: {response.text}")
                
        except Exception as e:
            self.category_text.delete(1.0, tk.END)
            self.category_text.insert(1.0, f"Erro inesperado: {str(e)}")

def main():
    """Função principal"""
    root = tk.Tk()
    app = FinancesAPIInterface(root)
    
    # Verificar se a API está rodando
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code != 200:
            messagebox.showwarning("Aviso", "API não está respondendo!\nCertifique-se de que o servidor está rodando.")
    except:
        messagebox.showwarning("Aviso", "Não foi possível conectar à API!\nCertifique-se de que o servidor está rodando em http://localhost:8000")
    
    root.mainloop()

if __name__ == "__main__":
    main() 
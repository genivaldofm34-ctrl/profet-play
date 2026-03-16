import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import os

class AppPROFET(ctk.CTk):
    def __init__(self):
        super().__init__()
        # AJUSTE: Título simplificado conforme solicitado
        self.title("PROFET PLAY") 
        self.geometry("1750x850")
        ctk.set_appearance_mode("dark")
        
        self.widgets_alunos = {}
        self.lista_turmas_arquivo = "lista_turmas.txt"
        self.turmas_disponiveis = self.carregar_lista_turmas()
        self.turma_atual = self.turmas_disponiveis[0] if self.turmas_disponiveis else "TURMA_A"
        
        # --- PAINEL DE DESTAQUES (FONTES AJUSTADAS) ---
        self.f_destaques = ctk.CTkFrame(self, fg_color="#1a1a1a", height=120, border_width=1, border_color="#333")
        self.f_destaques.pack(pady=10, padx=10, fill="x")
        
        # Títulos e nomes com fontes menores para não cortar os nomes
        self.lbl_nome_lenda = self.criar_card(self.f_destaques, "👑 LENDA DA SEMANA", "#d4af37", "black") 
        self.lbl_nome_super = self.criar_card(self.f_destaques, "🚀 SUPERAÇÃO DA SEMANA", "#e67e22", "white")

        # --- GESTÃO DE TURMAS ---
        self.f_turmas = ctk.CTkFrame(self, fg_color="#111", height=50)
        self.f_turmas.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.f_turmas, text="TURMA:", font=("Arial Bold", 12)).pack(side="left", padx=10)
        self.menu_turmas = ctk.CTkOptionMenu(self.f_turmas, values=[t.replace("_"," ") for t in self.turmas_disponiveis], command=self.mudar_turma, fg_color="#6022e0")
        self.menu_turmas.pack(side="left", padx=5)
        self.menu_turmas.set(self.turma_atual.replace("_", " "))

        ctk.CTkLabel(self.f_turmas, text=" | NOVA:", font=("Arial Bold", 12)).pack(side="left", padx=10)
        self.ent_nome_turma = ctk.CTkEntry(self.f_turmas, placeholder_text="NOME DA TURMA...", width=150)
        self.ent_nome_turma.pack(side="left", padx=5)
        ctk.CTkButton(self.f_turmas, text="➕ TURMA", width=80, fg_color="#27ae60", font=("Arial Black", 11), command=self.adicionar_turma).pack(side="left", padx=5)
        ctk.CTkButton(self.f_turmas, text="📂 IMPORTAR LISTA", fg_color="#34495e", font=("Arial Black", 11), command=self.janela_importar).pack(side="left", padx=20)

        self.lbl_turma_viva = ctk.CTkLabel(self.f_turmas, text=f"EXIBINDO: {self.turma_atual.replace('_',' ')}", font=("Arial Black", 14), text_color="#d4af37")
        self.lbl_turma_viva.pack(side="right", padx=15)

        # --- ABAS ---
        self.abas = ctk.CTkTabview(self, fg_color="#1a1a1a", segmented_button_selected_color="#6022e0")
        self.abas.pack(padx=10, pady=5, fill="both", expand=True)
        self.tab_comando = self.abas.add("🎮 ESTÚDIO DE PONTOS")
        self.tab_turma = self.abas.add("📊 NOSSO RECORD")

        self.setup_aba_turma()
        self.setup_aba_comando()
        self.carregar_dados_alunos()

    def criar_card(self, pai, titulo, cor, cor_txt):
        f = ctk.CTkFrame(pai, fg_color=cor, corner_radius=15)
        f.pack(side="left", padx=20, pady=10, expand=True, fill="both")
        # Fonte do título reduzida para 13
        ctk.CTkLabel(f, text=titulo, font=("Arial Black", 13), text_color=cor_txt).pack(pady=(5,0))
        # Fonte do conteúdo reduzida para 24 para caber nomes longos
        lbl = ctk.CTkLabel(f, text="---", font=("Arial Black", 24), text_color=cor_txt)
        lbl.pack(pady=(0,5))
        return lbl

    def validar_limite(self, entrada, limite):
        texto = entrada.get().strip()
        if texto:
            try:
                valor = int(texto)
                if valor > limite:
                    entrada.delete(0, "end")
                    entrada.insert(0, str(limite))
            except:
                entrada.delete(0, "end")
                entrada.insert(0, "0")
        self.recalc()

    def criar_linha(self, nome, valores=None):
        r = ctk.CTkFrame(self.scroll, fg_color="#222", corner_radius=8)
        r.pack(fill="x", pady=3)
        ctk.CTkLabel(r, text=nome, width=180, anchor="w", font=("Arial Bold", 12), text_color="#bbb").pack(side="left", padx=5)
        
        ents = {}
        configs = [("N1", 20), ("N2", 30), ("N3", 20), ("N4", 10), ("N5", 20), 
                   ("SIL", 15), ("MON", 15), ("LEN", 5), ("COM", 5), ("SUP", 5), ("EXT", 999)]
        
        for i, (c, lim) in enumerate(configs):
            e = ctk.CTkEntry(r, width=45, justify="center", fg_color="#111", border_color="#444")
            val = valores[i] if valores and i < len(valores) else "0"
            e.insert(0, val)
            e.pack(side="left", padx=2)
            e.bind("<KeyRelease>", lambda ev, ent=e, l=lim: self.validar_limite(ent, l))
            ents[c] = e

        e_tot = ctk.CTkEntry(r, width=75, state="readonly", fg_color="#4d4100", text_color="#f1c40f", font=("Arial Black", 12))
        e_tot.pack(side="left", padx=2)
        e_ant = ctk.CTkEntry(r, width=75, fg_color="#2b1a3d")
        e_ant.insert(0, valores[11] if valores and len(valores) > 11 else "0")
        e_ant.pack(side="left", padx=2)
        e_ant.bind("<KeyRelease>", lambda ev: self.recalc())
        e_dif = ctk.CTkEntry(r, width=75, state="readonly", fg_color="#0e2f1a", text_color="#2ecc71", font=("Arial Black", 12))
        e_dif.pack(side="left", padx=2)
        
        pb = ctk.CTkProgressBar(r, width=100, progress_color="#d4af37")
        pb.pack(side="left", padx=5)
        lbl_p = ctk.CTkLabel(r, text="0%", width=45, font=("Arial Bold", 11), text_color="#d4af37")
        lbl_p.pack(side="left")
        
        ctk.CTkButton(r, text="🗑️", width=35, fg_color="#444", hover_color="#c0392b", command=lambda: self.rem_aluno(nome, r)).pack(side="left", padx=2)
        
        ents.update({"TOT": e_tot, "ANT": e_ant, "DIF": e_dif, "PB": pb, "LBL_P": lbl_p})
        self.widgets_alunos[nome] = ents
        self.recalc()

    def recalc(self):
        def seguro_int(ent):
            try: return int(ent.get().strip())
            except: return 0

        dados_ranking = []
        niveis_conq_total = 0
        for n, w in self.widgets_alunos.items():
            n_xp = [seguro_int(w[k]) for k in ["N1", "N2", "N3", "N4", "N5"]]
            b_xp = [seguro_int(w[k]) for k in ["SIL", "MON", "LEN", "COM", "SUP", "EXT"]]
            ant = seguro_int(w["ANT"])
            
            soma_atual = sum(n_xp) + sum(b_xp)
            total_geral = soma_atual + ant
            
            perc_ind = min(sum(n_xp), 100)
            w["PB"].set(perc_ind / 100)
            w["LBL_P"].configure(text=f"{perc_ind}%")
            niveis_conq_total += sum(1 for v in n_xp[:4] if v > 0)

            for c, v in [("TOT", total_geral), ("DIF", soma_atual)]:
                w[c].configure(state="normal"); w[c].delete(0, "end"); w[c].insert(0, str(v)); w[c].configure(state="readonly")
            
            dados_ranking.append({"nome": n, "total": total_geral, "dif": soma_atual, "ext": seguro_int(w["EXT"])})

        if dados_ranking:
            lenda = sorted(dados_ranking, key=lambda x: x['total'], reverse=True)[0]
            self.lbl_nome_lenda.configure(text=f"{lenda['nome']} ({lenda['total']} XP)" if lenda['total'] > 0 else "---")
            ranking_sup = sorted(dados_ranking, key=lambda x: (x['dif'], x['ext']), reverse=True)
            sup = next((a for a in ranking_sup if a['nome'] != lenda['nome']), lenda)
            self.lbl_nome_super.configure(text=f"{sup['nome']} (+{sup['dif']} XP)" if sup['dif'] > 0 else "---")

        total_alunos = len(self.widgets_alunos)
        if total_alunos > 0:
            obj = total_alunos * 4
            prog = (niveis_conq_total / obj) if obj > 0 else 0
            self.barra_turma.set(prog)
            self.lbl_porcentagem_turma.configure(text=f"{int(prog * 100)}%")

    def setup_aba_turma(self):
        self.f_container_turma = ctk.CTkFrame(self.tab_turma, fg_color="transparent")
        self.f_container_turma.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(self.f_container_turma, text="🏆 NÍVEL GLOBAL DA TURMA 🏆", font=("Arial Black", 30), text_color="#d4af37").pack(pady=10)
        self.barra_turma = ctk.CTkProgressBar(self.f_container_turma, width=900, height=50, progress_color="#2ecc71", corner_radius=25)
        self.barra_turma.set(0)
        self.barra_turma.pack(pady=10)
        self.lbl_porcentagem_turma = ctk.CTkLabel(self.f_container_turma, text="0%", font=("Arial Black", 80), text_color="#2ecc71")
        self.lbl_porcentagem_turma.pack(pady=5)

    def setup_aba_comando(self):
        f_g = ctk.CTkFrame(self.tab_comando, fg_color="transparent")
        f_g.pack(fill="x", pady=10)
        self.ent_novo = ctk.CTkEntry(f_g, placeholder_text="NOME DO ALUNO...", width=300, height=40)
        self.ent_novo.pack(side="left", padx=10)
        ctk.CTkButton(f_g, text="➕ ALUNO", fg_color="#27ae60", font=("Arial Black", 11), command=self.add_aluno).pack(side="left", padx=5)
        ctk.CTkButton(f_g, text="🚀 NOVA AULA", fg_color="#6022e0", font=("Arial Black", 11), command=self.nova_aula).pack(side="left", padx=5)
        ctk.CTkButton(f_g, text="💾 SALVAR", fg_color="#333", font=("Arial Bold", 11), command=self.salvar_dados_alunos).pack(side="right", padx=10)

        f_h = ctk.CTkFrame(self.tab_comando, fg_color="#0a0a0a", height=35)
        f_h.pack(fill="x", padx=10, pady=5)
        cols = [("PLAYER", 180), ("N1", 45), ("N2", 45), ("N3", 45), ("N4", 45), ("N5", 45), ("SIL", 45), ("MON", 45), ("LEN", 45), ("COM", 45), ("SUP", 45), ("EXT", 45), ("TOTAL", 75), ("ANT", 75), ("DIF", 75), ("PROG", 110), ("%", 45)]
        for t, l in cols: ctk.CTkLabel(f_h, text=t, width=l, font=("Arial Black", 10)).pack(side="left", padx=2)

        self.scroll = ctk.CTkScrollableFrame(self.tab_comando, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5)

    def add_aluno(self):
        n = self.ent_novo.get().upper().strip()
        if n and n not in self.widgets_alunos:
            self.criar_linha(n)
            self.ent_novo.delete(0, "end")
            self.salvar_dados_alunos()

    def janela_importar(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Importar Lista")
        janela.geometry("400x500")
        janela.attributes("-topmost", True)
        ctk.CTkLabel(janela, text="Cole os nomes (um por linha):").pack(pady=10)
        txt = scrolledtext.ScrolledText(janela, width=40, height=20)
        txt.pack(padx=10, pady=10)
        def ok():
            nomes = [n.strip().upper() for n in txt.get("1.0", "end").split("\n") if n.strip()]
            for n in nomes:
                if n not in self.widgets_alunos: self.criar_linha(n)
            self.salvar_dados_alunos()
            janela.destroy()
        ctk.CTkButton(janela, text="IMPORTAR", command=ok).pack(pady=10)

    def mudar_turma(self, escolha):
        self.salvar_dados_alunos()
        for widget in self.scroll.winfo_children(): widget.destroy()
        self.widgets_alunos.clear()
        self.turma_atual = escolha.replace(" ", "_")
        self.lbl_turma_viva.configure(text=f"EXIBINDO: {escolha}")
        self.carregar_dados_alunos()

    def adicionar_turma(self):
        nova = self.ent_nome_turma.get().upper().strip().replace(" ", "_")
        if nova and nova not in self.turmas_disponiveis:
            self.turmas_disponiveis.append(nova)
            with open(self.lista_turmas_arquivo, "a") as f: f.write(nova + "\n")
            self.menu_turmas.configure(values=[t.replace("_"," ") for t in self.turmas_disponiveis])
            self.mudar_turma(nova)
            self.ent_nome_turma.delete(0, "end")

    def nova_aula(self):
        if messagebox.askyesno("Nova Aula", "Zerar pontos atuais e mover para histórico?"):
            for n, w in self.widgets_alunos.items():
                total_atual = w["TOT"].get()
                w["ANT"].delete(0, "end"); w["ANT"].insert(0, total_atual)
                for k in ["N1","N2","N3","N4","N5","SIL","MON","LEN","COM","SUP","EXT"]:
                    w[k].delete(0, "end"); w[k].insert(0, "0")
            self.recalc(); self.salvar_dados_alunos()

    def carregar_lista_turmas(self):
        if os.path.exists(self.lista_turmas_arquivo):
            with open(self.lista_turmas_arquivo, "r") as f: return [l.strip() for l in f if l.strip()]
        return ["TURMA_A"]

    def salvar_dados_alunos(self):
        with open(f"dados_alunos_{self.turma_atual}.txt", "w") as f:
            for n, w in self.widgets_alunos.items():
                vals = [w[k].get() or "0" for k in ["N1","N2","N3","N4","N5","SIL","MON","LEN","COM","SUP","EXT","ANT"]]
                f.write(f"{n}|{','.join(vals)}\n")

    def carregar_dados_alunos(self):
        path = f"dados_alunos_{self.turma_atual}.txt"
        if os.path.exists(path):
            with open(path, "r") as f:
                for l in f:
                    n, r = l.strip().split("|")
                    self.criar_linha(n, r.split(","))

    def rem_aluno(self, n, r):
        if messagebox.askyesno("Remover", f"Excluir {n}?"):
            r.destroy(); self.widgets_alunos.pop(n); self.recalc(); self.salvar_dados_alunos()

if __name__ == "__main__":
    app = AppPROFET()
    app.mainloop()
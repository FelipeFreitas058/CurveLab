import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QAbstractItemView, QMessageBox
)
from PyQt6.QtGui import QIcon
from Interface import Ui_MainWindow
from Funcoes import Funcao
import matplotlib
matplotlib.use('Qt5Agg')

class MeuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Lista_Var_Codigo.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.f = Funcao(self)
        
        self.f.Atualiza_Lista_Predefinicoes()
        # Aba Planlha
        self.ui.B_Carregar_Planilha.clicked.connect(self.f.Carrega_Planilha)
        self.ui.B_Importar_Variavel.clicked.connect(self.f.Importar_Variavel)

        # Aba Codigo
        self.ui.B_Executar_Codigo.clicked.connect(self.f.Executar_Codigo)
        self.ui.B_Importar_variaveis.clicked.connect(self.f.Importar_Variaveis)
        
        # Aba Arquivo de texto
        self.ui.B_Abrir_A_Txt.clicked.connect(self.f.Carrega_Arquivo_Texto)
        self.ui.B_Gerar_Planilha_A_Txt.clicked.connect(self.f.Gerar_Planilha)

        # Aba Criação de curvas
        self.ui.B_Add_Curva.clicked.connect(self.f.Adicionar_Curva)
        self.ui.B_Excluir_Variavel.clicked.connect(self.f.Excluir_Variavel)
        
        # Aba Geração do grafico
        self.ui.B_Gerar_Graph.clicked.connect(self.f.Verifica_Grafico)


        # Conexões da MenuBar
        self.ui.actionPlanilha.triggered.connect(lambda: self.f.Mudar_Aba_Principal(1))
        self.ui.actionCodigo.triggered.connect(lambda: self.f.Mudar_Aba_Principal(2))
        self.ui.actionCriacao_Curvas.triggered.connect(lambda: self.f.Mudar_Aba_Principal(3))
        self.ui.actionConstrucao_Grafico.triggered.connect(lambda: self.f.Mudar_Aba_Principal(4))
        self.ui.actionArquivo_Texto.triggered.connect(lambda: self.f.Mudar_Aba_Principal(6))
        # self.ui.actionExportar.triggered.connect(lambda: self.f.Mudar_Aba_Principal(0))
        self.ui.actionCurvas.triggered.connect(lambda: self.f.Mudar_Aba_Personalizacao(0))
        self.ui.actionTitulos.triggered.connect(lambda: self.f.Mudar_Aba_Personalizacao(1))
        self.ui.actionLegendas.triggered.connect(lambda: self.f.Mudar_Aba_Personalizacao(2))
        self.ui.actionGrades.triggered.connect(lambda: self.f.Mudar_Aba_Personalizacao(4))
        self.ui.actionBordas.triggered.connect(lambda: self.f.Mudar_Aba_Personalizacao(3))
        self.ui.actionPredefini_es.triggered.connect(lambda: self.f.Mudar_Aba_Personalizacao(5))
        
        # QDialogs
        self.ui.B_CDialog_Cor_Curva.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Curva))
        self.ui.B_CDialog_Borda_E.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Borda_E))
        self.ui.B_CDialog_Borda_D.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Borda_D))
        self.ui.B_CDialog_Borda_I.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Borda_I))
        self.ui.B_CDialog_Borda_S.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Borda_S))
        self.ui.B_CDialog_Cor_Borda_Legenda.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Borda_Legenda))
        self.ui.B_CDialog_Cor_Fonte_Titulo.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Fonte_Titulo))
        self.ui.B_CDialog_Cor_Fundo_Legenda.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Fundo_Legenda))
        self.ui.B_CDialog_Cor_Grade_Principal.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Grade_Principal))
        self.ui.B_CDialog_Cor_Grade_Secundaria.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Grade_Secundaria))
        self.ui.B_CDialog_Cor_Marcador.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Marcador))
        self.ui.pushButton_9.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Fonte_Legenda))
        self.ui.B_CDialog_Cor_Borda_Marcador.clicked.connect(lambda: self.ui.Abrir_QColorDialog(self.ui.CombB_Cor_Borda_Marcador))

        # Personalização de curvas
        self.ui.CB_Visibilidade_Curva.stateChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Visibilidade", None))
        self.ui.CombB_Cor_Curva.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Cor", self.ui.CombB_Cor_Curva.currentText()))
        self.ui.SB_Espessura_Curva.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Espessura", self.ui.SB_Espessura_Curva.value()))
        self.ui.CombB_Estilo_Curva.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Estilo", self.ui.CombB_Estilo_Curva.currentText()))
        self.ui.Slider_Transp_Curva.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Transparencia", self.ui.Slider_Transp_Curva.value()))
        self.ui.CombB_Escolher_Marcador.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Marcador", self.ui.CombB_Escolher_Marcador.currentText()))
        self.ui.CombB_Cor_Marcador.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Marcador_Cor", self.ui.CombB_Cor_Marcador.currentText()))
        self.ui.CombB_Cor_Borda_Marcador.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Marcador_Cor_Borda", self.ui.CombB_Cor_Borda_Marcador.currentText()))
        self.ui.SB_Espessura_Marcador.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Curvas", self.ui.CombB_Selecionar_Curva.currentText(), "Marcador_Espessura", self.ui.SB_Espessura_Marcador.value()))
        self.ui.CB_Ativar_Marcador.stateChanged.connect(self.f.Ativar_Marcador)
        self.ui.CombB_Selecionar_Curva.currentTextChanged.connect(self.f.Atualizar_Configuracoes_Curvas)

        # Personalização dos títulos
        self.ui.FCombB_Fonte_Titulo.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Titulo", self.ui.CombB_Escolher_Qual_Titulo.currentText(), "Fonte", self.ui.FCombB_Fonte_Titulo.currentText()))
        self.ui.SB_Tamanho_Fonte_Titulo.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Titulo", self.ui.CombB_Escolher_Qual_Titulo.currentText(), "Tamanho_Fonte", self.ui.SB_Tamanho_Fonte_Titulo.value() ))
        self.ui.CB_Negrito_Titulo.stateChanged.connect(lambda: self.f.Atualizar_Grafico("Titulo", self.ui.CombB_Escolher_Qual_Titulo.currentText(), "Negrito", 'bold'))
        self.ui.CB_Italico_Titulo.stateChanged.connect(lambda: self.f.Atualizar_Grafico("Titulo", self.ui.CombB_Escolher_Qual_Titulo.currentText(), "Italico", 'italic'))
        self.ui.CombB_Cor_Fonte_Titulo.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Titulo", self.ui.CombB_Escolher_Qual_Titulo.currentText(), "Cor_Fonte", self.ui.CombB_Cor_Fonte_Titulo.currentText()))
        self.ui.CombB_Escolher_Qual_Titulo.currentTextChanged.connect(self.f.Atualizar_Configuracoes_Titulos)

        # Personalização das legendas
        self.ui.CB_Ativar_Legendas.stateChanged.connect(self.f.Ativar_Legenda)
        self.ui.CombB_Parametro_Legenda.currentIndexChanged.connect(lambda index: self.f.Mudar_Aba_Parametro_Legenda(index))
        self.ui.CombB_Selecionar_Curva_Legenda.currentTextChanged.connect(self.f.Atualizar_Configuracoes_Legendas)
        self.ui.FCombB_Fonte_Legenda.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Fonte", self.ui.FCombB_Fonte_Legenda.currentText()))
        self.ui.SB_Tamanho_Fonte_Legenda.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Tamanho_Fonte", self.ui.SB_Tamanho_Fonte_Legenda.value()))
        self.ui.CombB_Cor_Fonte_Legenda.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Cor_Fonte", self.ui.CombB_Cor_Fonte_Legenda.currentText()))
        self.ui.CB_Negrito_Legenda.stateChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Negrito", 'bold'))
        self.ui.CB_Italico_Legenda.stateChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Italico", 'italic'))
        self.ui.CombB_Localizacao_Legenda.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Localização", self.ui.CombB_Localizacao_Legenda.currentText()))
        self.ui.Slider_Arredond_Caixa_Legenda.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Arredondamento", self.ui.Slider_Arredond_Caixa_Legenda.value()))
        self.ui.CombB_Cor_Fundo_Legenda.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Cor_Fundo", self.ui.CombB_Cor_Fundo_Legenda.currentText()))
        self.ui.Slider_Transp_Caixa_Legenda.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", self.ui.CombB_Parametro_Legenda.currentText(), "Transparencia", self.ui.Slider_Transp_Caixa_Legenda.value()))
        self.ui.CombB_Cor_Borda_Legenda.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", "Borda", "Cor", self.ui.CombB_Cor_Borda_Legenda.currentText()))
        self.ui.SB_Espessura_Borda_Legenda.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Legendas", "Borda", "Espessura", self.ui.SB_Espessura_Borda_Legenda.value()))
        self.ui.CB_Ativar_Borda_Legenda.stateChanged.connect(self.f.Ativar_Borda_Legenda)
        self.ui.CB_Alteracao_Individual_Legenda.stateChanged.connect(self.f.Mostrar_Curvas_Legenda)

        # Personalização das grades
        self.ui.CB_Ativar_Grade_Principal.stateChanged.connect(self.f.Ativar_Grade_Principal)
        self.ui.CombB_Estilo_Linha_Grade_Principal.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Grades", "Principal", "Estilo", self.ui.CombB_Estilo_Linha_Grade_Principal.currentText()))
        self.ui.SB_Espessura_Grade_Principal.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Grades", "Principal", "Espessura", self.ui.SB_Espessura_Grade_Principal.value()))
        self.ui.Slider_Transp_Grade_Principal.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Grades", "Principal", "Transparencia", self.ui.Slider_Transp_Grade_Principal.value()))
        self.ui.CombB_Cor_Grade_Principal.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Grades", "Principal", "Cor", self.ui.CombB_Cor_Grade_Principal.currentText()))
        self.ui.CB_Ativar_Grade_Secundaria.stateChanged.connect(self.f.Ativar_Grade_Secundaria)
        self.ui.CombB_Estilo_Linha_Grade_Secundaria.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Grades", "Secundaria", "Estilo", self.ui.CombB_Estilo_Linha_Grade_Secundaria.currentText()))
        self.ui.SB_Espessura_Grade_Secundaria.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Grades", "Secundaria", "Espessura", self.ui.SB_Espessura_Grade_Secundaria.value()))
        self.ui.Slider_Transp_Grade_Secundaria.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Grades", "Secundaria", "Transparencia", self.ui.Slider_Transp_Grade_Secundaria.value()))
        self.ui.CombB_Cor_Grade_Secundaria.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Grades", "Secundaria", "Cor", self.ui.CombB_Cor_Grade_Secundaria.currentText()))

        # Personalização das bordas
        self.ui.CB_Ativar_Borda_Superior.stateChanged.connect(lambda: self.f.Ativar_Borda("Superior"))
        self.ui.SB_Espessura_Borda_S.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Bordas", "Superior", "Espessura", self.ui.SB_Espessura_Borda_S.value()))
        self.ui.CombB_Cor_Borda_S.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Bordas", "Superior", "Cor", self.ui.CombB_Cor_Borda_S.currentText()))

        self.ui.CB_Ativar_Borda_Inferior.stateChanged.connect(lambda: self.f.Ativar_Borda("Inferior"))
        self.ui.SB_Espessura_Borda_I.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Bordas", "Inferior", "Espessura", self.ui.SB_Espessura_Borda_I.value()))
        self.ui.CombB_Cor_Borda_I.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Bordas", "Inferior", "Cor", self.ui.CombB_Cor_Borda_I.currentText()))

        self.ui.CB_Ativar_Borda_Direita.stateChanged.connect(lambda: self.f.Ativar_Borda("Direita"))
        self.ui.SB_Espessura_Borda_D.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Bordas", "Direita", "Espessura", self.ui.SB_Espessura_Borda_D.value()))
        self.ui.CombB_Cor_Borda_D.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Bordas", "Direita", "Cor", self.ui.CombB_Cor_Borda_D.currentText()))

        self.ui.CB_Ativar_Borda_Esquerda.stateChanged.connect(lambda: self.f.Ativar_Borda("Esquerda"))
        self.ui.SB_Espessura_Borda_E.valueChanged.connect(lambda: self.f.Atualizar_Grafico("Bordas", "Esquerda", "Espessura", self.ui.SB_Espessura_Borda_E.value()))
        self.ui.CombB_Cor_Borda_E.currentTextChanged.connect(lambda: self.f.Atualizar_Grafico("Bordas", "Esquerda", "Cor", self.ui.CombB_Cor_Borda_E.currentText()))

        # Predefinições
        self.ui.CombB_Predifinicoes_Disponiveis.currentTextChanged.connect(self.f.Atualizar_Indices_Disponiveis)
        self.ui.CB_Usar_Predefinicao.stateChanged.connect(self.f.Atualiza_Predefinicao_Geral)
        self.ui.B_Salvar_Predefinicao.clicked.connect(self.f.Salvar_Predefinicao)

        # Exportar gráfico
        self.ui.B_Excluir_Predefinicao.clicked.connect(self.f.Excluir_Predefinicao)
        self.ui.B_Exportar_Grafico.clicked.connect(self.f.Exportar_Grafico)
        self.ui.B_Copiar_Grafico.clicked.connect(self.f.Copia_Grafico)

    def closeEvent(self, event):
        resposta = QMessageBox.question(self, "Confirmação", 
                                        "Tem certeza que deseja sair?", 
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                        QMessageBox.StandardButton.Yes)
        
        if resposta == QMessageBox.StandardButton.Yes:
            event.accept()  # Fecha a janela
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "Icone.ico")))
    Janela = MeuApp()
    Janela.showMaximized()
    Janela.show()
    sys.exit(app.exec())
import re
import sys
import os
import io
import pickle
import types
import numpy as np
import json
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from PyQt6 import QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFileDialog, QTableWidgetItem, QMessageBox, QApplication
)
from Interface import Ui_MainWindow, CurveWidget, Dialog_Previa_Planilha
import matplotlib
matplotlib.use('Qt5Agg')

class Funcao:
    def  __init__(self, principal):
        self.interface = principal
        self.ui: Ui_MainWindow = principal.ui

        self.Dicionario_Global = {
        "Curvas": {},
        "Titulos": {
            "T_Grafico":{
                "Ativo": True,
                "Fonte": "Arial",
                "Texto": "Titulo de teste",
                "Tamanho_Fonte": 12,
                "Negrito": False,
                "Italico": False, 
                "Cor_Fonte": "#000000"
            },
            "T_Eixo_X":{
                "Ativo": True,
                "Fonte": "Arial",
                "Texto": "Eixo X",
                "Tamanho_Fonte": 10,
                "Negrito": False,
                "Italico": False, 
                "Cor_Fonte": "#000000"
            },
            "T_Eixo_Y":{
                "Ativo": True,
                "Fonte": "Arial",
                "Texto": "Eixo Y",
                "Tamanho_Fonte": 10,
                "Negrito": False,
                "Italico": False, 
                "Cor_Fonte": "#000000"
            },
            "Valores X":{
                "Ativo": True,
                "Fonte": "Arial",
                "Tamanho_Fonte": 10,
                "Negrito": False,
                "Italico": False, 
                "Cor_Fonte": "#000000"
            },
            "Valores Y":{
                "Ativo": True,
                "Fonte": "Arial",
                "Tamanho_Fonte": 10,
                "Negrito": False,
                "Italico": False, 
                "Cor_Fonte": "#000000"
            },
        },
        "Legendas": {
            "Ativar": False,
            "Seleção_individual": False,
            "Localizacao": "Melhor",
            "Caixa": {
                "Arredondamento": 4,
                "Cor_Fundo": "#ffffff",
                "Transparencia": 100
            },
            "Borda":{
                "Ativar": True,
                "Cor": "#d6d6d6",
                "Espessura": 10
            }
        },
        "Grades": {
            "Principal":{
                "Ativar": False,
                "Estilo": '-',
                "Espessura": 4,
                "Transparencia": 100,
                "Cor": "#b0b0b0"
            },
            "Secundaria":{
                "Ativar": False,
                "Estilo": '-',
                "Espessura": 4,
                "Transparencia": 100,
                "Cor": "#b0b0b0"
            }
        },
        "Bordas": {
            "Superior": {
                "Ativar": True,
                "Espessura": 8,
                "Cor": "#000000"
            },
            "Inferior": {
                "Ativar": True,
                "Espessura": 8,
                "Cor": "#000000"
            },
            "Direita": {
                "Ativar": True,
                "Espessura": 8,
                "Cor": "#000000"
            },
            "Esquerda": {
                "Ativar": True,
                "Espessura": 8,
                "Cor": "#000000"
            }
        },
        "Indices": {}
    }
        
        self.Dicionario_Cores = {
            "Vermelho": "#FF0000",
            "Azul": "#0000FF",
            "Roxo": "#800080",
            "Verde": "#008000",
            "Amarelo": "#FFFF00",
            "Laranja": "#FFA500",
            "Ciano": "#00FFFF",
            "Magenta": "#FF00FF",
            "Cinza": "#808080",
            "Preto": "#000000",
            "Branco": "#FFFFFF",
        }

        self.Dicionario_Marcadores = {
            "Círculo": "o",
            "Triângulo para cima": "^",
            "Triângulo para baixo": "v",
            "Triângulo para a direita": ">",
            "Triângulo para a esquerda": "<",
            "Quadrado": "s",
            "Pentágono": "p",
            "Estrela": "*",
            "Hexágono (rotacionado)": "h",
            "Hexágono": "H",
            "Cruz": "+",
            "Cruz (com a linha diagonal)": "x",
            "Losango (diagonal)": "D",
            "Losango": "d",
            "Linha vertical": "|",
            "Linha horizontal": "_"
        }

        self.Dicionario_Locais = {
            "Melhor": "best",
            "Superior esquerdo": "upper left",
            "Superior direito": "upper right",
            "Inferior direito": "lower right",
            "Inferior esquerdo": "lower left",
            "Centro": "center",
            "Centro à esquerda": "center left",
            "Centro à direita": "center right",
            "Centro inferior": "lower center",
            "Centro superior": "upper center"
        }

        self.Dicionario_Formatos = {
            "PNG": '.png',
            "PDF": '.pdf',
            "SVG": '.svg',
            "JPEG": '.jpeg',
            "EPS": '.eps'
        }

        self.Dicionario_Estilos = {
            "-": 'Linha sólida',
            "--": 'Linha tracejada',
            "-.": 'Linha ponto-tracejada',
            ":": 'Linha pontilhada'}

        self.widgets_valores = {}

        self.Curvas = []
        self.Indices_Curvas = {}
        self.Lista_Variaveis = {}
        self.Lista_Variaveis_Codigo = {}
        
        self.canvas = None
        self.canvas_P = None
        self.Lista_Curvas_Plotadas = {}
        self.Lista_Curvas_Predef = {}
        self.legenda = None

        self.Fontes_Disponiveis = set(f.name for f in fm.fontManager.ttflist)
        self.nome_curva = []
        self.nome_curva2 = []

        self.toolbar = None
        self.parametro = 0
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.Restaura_Mensagem_Fixa)
        self.ui.statusbar.messageChanged.connect(lambda: self.Inicia_Timer(1))

        self.Parametro_Arbitrario_Legenda = 0

    def Atualizar_Curva(self, Nome_Curva, parametro, valor):
        if self.Lista_Curvas_Plotadas != {}:
            Curva = self.Lista_Curvas_Plotadas.get(Nome_Curva)
        else:
            QMessageBox.critical(self.interface, "Erro!", "Não há nenhuma curva plotada no gráfico.")
            return

        if parametro == "Visibilidade":
            if self.ui.CB_Visibilidade_Curva.isChecked():
                Estilo = self.ui.CombB_Estilo_Curva.currentText()
                if Estilo == "Linha sólida":
                    Estilo = '-'
                elif Estilo == "Linha tracejada":
                    Estilo = '--'
                elif Estilo == "Linha ponto-tracejada":
                    Estilo = '-.'
                elif Estilo == 'Linha pontilhada':
                    Estilo = ':'
                Curva.set_linestyle(Estilo)
                self.Dicionario_Global["Curvas"][Nome_Curva]["Visibilidade"] = True
                self.canvas_P.draw_idle()
            else:
                Curva.set_linestyle('')
                self.Dicionario_Global["Curvas"][Nome_Curva]["Visibilidade"] = False
                self.canvas_P.draw_idle()

        if parametro == "Cor":
            try:
                if valor in self.Dicionario_Cores:
                    valor = self.Dicionario_Cores[valor]
                try:
                    Curva.set_color(valor)
                except Exception as e:
                    self.ui.statusbar.showMessage("Cor inválida", 1000)
                    return
                self.Dicionario_Global["Curvas"][Nome_Curva]["Cor"] = valor
                self.canvas_P.draw_idle()
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao exibir configurações da curva {Nome_Curva}: {e}")
        if parametro == "Espessura":
            Curva.set_linewidth(valor/10)
            self.Dicionario_Global["Curvas"][Nome_Curva]["Espessura"] = valor
            self.canvas_P.draw_idle()
            
            
        if parametro == "Estilo" and self.ui.CB_Visibilidade_Curva.isChecked():
            valor2 = ''
            if valor == "Linha sólida":
                valor2 = '-'
            elif valor == "Linha tracejada":
                valor2 = '--'
            elif valor == "Linha ponto-tracejada":
                valor2 = '-.'
            elif valor == 'Linha pontilhada':
                valor2 = ':'
            else:
                valor = "Linha sólida"
                valor2 = '-'
            Curva.set(ls=valor2)
            self.Dicionario_Global["Curvas"][Nome_Curva]["Estilo"] = valor
            self.canvas_P.draw_idle()
            
        if parametro == "Transparencia":
            valor2 = valor/100
            Curva.set_alpha(valor2)
            self.Dicionario_Global["Curvas"][Nome_Curva]["Transparencia"] = valor
            self.canvas_P.draw_idle()         
        if parametro == "Marcador" and self.ui.CB_Ativar_Marcador.isChecked():
            if valor in self.Dicionario_Marcadores:
                valor2 = self.Dicionario_Marcadores[valor]
            Curva.set_marker(valor2)
            self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador"] = valor
            
            self.canvas_P.draw_idle()
        if parametro == "Marcador_Cor" and self.ui.CB_Ativar_Marcador.isChecked():
            if valor in self.Dicionario_Cores:
                valor = self.Dicionario_Cores[valor]
            Curva.set_markerfacecolor(valor)
            self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Cor"] = valor
            
            self.canvas_P.draw_idle()
        if parametro == "Marcador_Cor_Borda" and self.ui.CB_Ativar_Marcador.isChecked():
            
            if valor in self.Dicionario_Cores:
                valor = self.Dicionario_Cores[valor]
            Curva.set_markeredgecolor(valor)
            self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Cor_Borda"] = valor
            
            self.canvas_P.draw_idle()
        if parametro == "Marcador_Espessura" and self.ui.CB_Ativar_Marcador.isChecked():
            Curva.set_markersize(valor)
            self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Espessura"] = valor
            
            self.canvas_P.draw_idle()    

    def Atualizar_Titulo(self, identificador, parametro, valor):
        if parametro == "Fonte":
            if valor in self.Fontes_Disponiveis:
                valor = valor
            else:
                valor = "Arial"
            if self.ui.CB_Ativar_Titulo_Grafico.isChecked() and identificador == "Gráfico":
                try:
                    Tamanho_Fonte = self.ax.title.get_fontsize()
                    Negrito_Fonte = self.ax.title.get_fontproperties()
                    titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                    self.ax.set_title(titulo_Grafico, fontdict={'fontname': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                    self.Dicionario_Global["Titulos"]["T_Grafico"]["Fonte"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")
            if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked() and identificador == "Eixo X":
                try:
                    Tamanho_Fonte = self.ax.xaxis.label.get_fontsize()
                    Negrito_Fonte = self.ax.xaxis.label.get_fontproperties()
                    Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                    self.ax.set_xlabel(Titulo_Eixo_X, fontdict={'fontname': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                    self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")
            if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked() and identificador == "Eixo Y":
                try:
                    Tamanho_Fonte = self.ax.yaxis.label.get_fontsize()
                    Negrito_Fonte = self.ax.yaxis.label.get_fontproperties()
                    Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                    self.ax.set_ylabel(Titulo_Eixo_Y, fontdict={'fontname': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                    self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")
            if identificador == "Valores X":
                try:
                    for label in self.ax.get_xticklabels():
                        label.set_fontname(valor)
                        self.Dicionario_Global["Titulos"]["Valores X"]["Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo X: {e}")
            if identificador == "Valores Y":
                try:
                    for label in self.ax.get_yticklabels():
                        label.set_fontname(valor)
                        self.Dicionario_Global["Titulos"]["Valores Y"]["Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo Y: {e}")

        if parametro == "Tamanho_Fonte":
            if self.ui.CB_Ativar_Titulo_Grafico.isChecked() and identificador == "Gráfico":
                try:
                    titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                    self.ax.set_title(titulo_Grafico, fontdict={'fontsize': valor})
                    self.Dicionario_Global["Titulos"]["T_Grafico"]["Tamanho_Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")
            if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked() and identificador == "Eixo X":
                try:
                    Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                    self.ax.set_xlabel(Titulo_Eixo_X, fontdict={'fontsize': valor})
                    self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Tamanho_Fonte"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")
            if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked() and identificador == "Eixo Y":
                try:
                    Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                    self.ax.set_ylabel(Titulo_Eixo_Y, fontdict={'fontsize': valor})
                    self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Tamanho_Fonte"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")
            if identificador == "Valores X":
                try:
                    for label in self.ax.get_xticklabels():
                        label.set_fontsize(valor)
                        self.Dicionario_Global["Titulos"]["Valores X"]["Tamanho_Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo X: {e}")
            if identificador == "Valores Y":
                try:
                    for label in self.ax.get_yticklabels():
                        label.set_fontsize(valor)
                        self.Dicionario_Global["Titulos"]["Valores Y"]["Tamanho_Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo Y: {e}")
        
        
        if parametro == "Negrito":
            if self.ui.CB_Negrito_Titulo.isChecked():
                if self.ui.CB_Ativar_Titulo_Grafico.isChecked() and identificador == "Gráfico":
                    try:
                        Tamanho_Fonte = self.ax.title.get_fontsize()
                        titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                        self.ax.set_title(titulo_Grafico, fontdict={'fontweight': valor, 'fontsize': Tamanho_Fonte})
                        self.Dicionario_Global["Titulos"]["T_Grafico"]["Negrito"] = True
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")
                if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked() and identificador == "Eixo X":
                    try:
                        Tamanho_Fonte = self.ax.xaxis.label.get_fontsize()
                        Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                        self.ax.set_xlabel(Titulo_Eixo_X, fontdict={'fontweight': valor, 'fontsize': Tamanho_Fonte})
                        self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Negrito"] = True
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")
                if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked() and identificador == "Eixo Y":
                    try:
                        Tamanho_Fonte = self.ax.yaxis.label.get_fontsize()
                        Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                        self.ax.set_ylabel(Titulo_Eixo_Y, fontdict={'fontweight': valor, 'fontsize': Tamanho_Fonte})
                        self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Negrito"] = True
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")
                if identificador == "Valores X":
                    try:
                        for label in self.ax.get_xticklabels():
                            label.set_fontweight('bold')
                            self.Dicionario_Global["Titulos"]["Valores X"]["Negrito"] = True
                        self.canvas_P.draw_idle()
                        
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo X: {e}")
                if identificador == "Valores Y":
                    try:
                        for label in self.ax.get_yticklabels():
                            label.set_fontweight('bold')
                            self.Dicionario_Global["Titulos"]["Valores Y"]["Negrito"] = True
                        self.canvas_P.draw_idle()
                        
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo Y: {e}")
            else:
                valor = 'normal'
                if self.ui.CB_Ativar_Titulo_Grafico.isChecked() and identificador == "Gráfico":
                    try:
                        Tamanho_Fonte = self.ax.title.get_fontsize()
                        titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                        self.ax.set_title(titulo_Grafico, fontdict={'fontweight': valor, 'fontsize': Tamanho_Fonte})
                        self.Dicionario_Global["Titulos"]["T_Grafico"]["Negrito"] = False
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")
                if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked() and identificador == "Eixo X":
                    try:
                        Tamanho_Fonte = self.ax.xaxis.label.get_fontsize()
                        Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                        self.ax.set_xlabel(Titulo_Eixo_X, fontdict={'fontweight': valor, 'fontsize': Tamanho_Fonte})
                        self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Negrito"] = False
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")
                if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked() and identificador == "Eixo Y":
                    try:
                        Tamanho_Fonte = self.ax.yaxis.label.get_fontsize()
                        Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                        self.ax.set_ylabel(Titulo_Eixo_Y, fontdict={'fontweight': valor, 'fontsize': Tamanho_Fonte})
                        self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Negrito"] = False
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")
                if identificador == "Valores X":
                    try:
                        for label in self.ax.get_xticklabels():
                            label.set_fontweight('normal')
                            self.Dicionario_Global["Titulos"]["Valores X"]["Negrito"] = False
                        self.canvas_P.draw_idle()
                        
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo X: {e}")
                if identificador == "Valores Y":
                    try:
                        for label in self.ax.get_yticklabels():
                            label.set_fontweight('normal')
                            self.Dicionario_Global["Titulos"]["Valores Y"]["Negrito"] = False
                        self.canvas_P.draw_idle()
                        
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo Y: {e}")

        if parametro == "Italico":
            if self.ui.CB_Italico_Titulo.isChecked():
                if self.ui.CB_Ativar_Titulo_Grafico.isChecked() and identificador == "Gráfico":
                    try:
                        Tamanho_Fonte = self.ax.title.get_fontsize()
                        Negrito_Fonte = self.ax.title.get_fontproperties()
                        titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                        self.ax.set_title(titulo_Grafico, fontdict={'style': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                        self.Dicionario_Global["Titulos"]["T_Grafico"]["Italico"] = True
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")
                if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked() and identificador == "Eixo X":
                    try:
                        Negrito_Fonte = self.ax.xaxis.label.get_fontproperties()
                        Tamanho_Fonte = self.ax.xaxis.label.get_fontsize()
                        Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                        self.ax.set_xlabel(Titulo_Eixo_X, fontdict={'style': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                        self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Italico"] = True
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")
                if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked() and identificador == "Eixo Y":
                    try:
                        Negrito_Fonte = self.ax.yaxis.label.get_fontproperties()
                        Tamanho_Fonte = self.ax.yaxis.label.get_fontsize()
                        Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                        self.ax.set_ylabel(Titulo_Eixo_Y, fontdict={'style': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                        self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Italico"] = True
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")
                if identificador == "Valores X":
                    try:
                        for label in self.ax.get_xticklabels():
                            label.set_fontstyle('italic')
                            self.Dicionario_Global["Titulos"]["Valores X"]["Italico"] = True
                        self.canvas_P.draw_idle()
                        
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo X: {e}")
                if identificador == "Valores Y":
                    try:
                        for label in self.ax.get_yticklabels():
                            label.set_fontstyle('italic')
                            self.Dicionario_Global["Titulos"]["Valores Y"]["Italico"] = True
                        self.canvas_P.draw_idle()
                        
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo Y: {e}")
            else:
                valor = 'normal'
                if self.ui.CB_Ativar_Titulo_Grafico.isChecked() and identificador == "Gráfico":
                    try:
                        Tamanho_Fonte = self.ax.title.get_fontsize()
                        Negrito_Fonte = self.ax.title.get_fontproperties()
                        titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                        self.ax.set_title(titulo_Grafico, fontdict={'style': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                        self.Dicionario_Global["Titulos"]["T_Grafico"]["Italico"] = False
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")
                if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked() and identificador == "Eixo X":
                    try:
                        Negrito_Fonte = self.ax.xaxis.label.get_fontproperties()
                        Tamanho_Fonte = self.ax.xaxis.label.get_fontsize()
                        Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                        self.ax.set_xlabel(Titulo_Eixo_X, fontdict={'style': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                        self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Italico"] = False
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")
                if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked() and identificador == "Eixo Y":
                    try:
                        Negrito_Fonte = self.ax.yaxis.label.get_fontproperties()
                        Tamanho_Fonte = self.ax.yaxis.label.get_fontsize()
                        Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                        self.ax.set_ylabel(Titulo_Eixo_Y, fontdict={'style': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                        self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Italico"] = False
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")
                if identificador == "Valores X":
                    try:
                        for label in self.ax.get_xticklabels():
                            label.set_fontstyle('normal')
                            self.Dicionario_Global["Titulos"]["Valores X"]["Italico"] = False
                        self.canvas_P.draw_idle()
                        
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo X: {e}")
                if identificador == "Valores Y":
                    try:
                        for label in self.ax.get_yticklabels():
                            label.set_fontstyle('normal')
                            self.Dicionario_Global["Titulos"]["Valores Y"]["Italico"] = False
                        self.canvas_P.draw_idle()
                        
                    except Exception as e:
                        QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo Y: {e}")
        
        if parametro == "Cor_Fonte":
            if valor in self.Dicionario_Cores:
                valor = self.Dicionario_Cores[valor]
                
            if self.ui.CB_Ativar_Titulo_Grafico.isChecked() and identificador == "Gráfico":
                try:
                    Tamanho_Fonte = self.ax.title.get_fontsize()
                    Negrito_Fonte = self.ax.title.get_fontproperties()
                    titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                    self.ax.set_title(titulo_Grafico, fontdict={'color': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                    self.Dicionario_Global["Titulos"]["T_Grafico"]["Cor_Fonte"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")
            if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked() and identificador == "Eixo X":
                try:
                    Negrito_Fonte = self.ax.xaxis.label.get_fontproperties()
                    Tamanho_Fonte = self.ax.xaxis.label.get_fontsize()    
                    Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                    self.ax.set_xlabel(Titulo_Eixo_X, fontdict={'color': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                    self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Cor_Fonte"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")
            if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked() and identificador == "Eixo Y":
                try:
                    Negrito_Fonte = self.ax.yaxis.label.get_fontproperties()
                    Tamanho_Fonte = self.ax.yaxis.label.get_fontsize()    
                    Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                    self.ax.set_ylabel(Titulo_Eixo_Y, fontdict={'color': valor, 'fontsize': Tamanho_Fonte, 'fontweight': Negrito_Fonte.get_weight()})
                    self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Cor_Fonte"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")    
            if identificador == "Valores X":
                try:
                    for label in self.ax.get_xticklabels():
                        label.set_color(valor)
                        self.Dicionario_Global["Titulos"]["Valores X"]["Cor_Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo X: {e}")
            if identificador == "Valores Y":
                try:
                    for label in self.ax.get_yticklabels():
                        label.set_color(valor)
                        self.Dicionario_Global["Titulos"]["Valores Y"]["Cor_Fonte"] = valor
                    self.canvas_P.draw_idle()
                    
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao personalizar os valores do eixo Y: {e}")

    def Atualizar_Legenda(self, Nome_Curva, identificador, parametro, valor):
        if self.ui.CB_Ativar_Legendas.isChecked():
            if identificador == "Texto da legenda" and self.Parametro_Arbitrario_Legenda == 1 and self.Lista_Curvas_Plotadas != {}:
                mapeamento_legenda = {}
                mapeamento_legenda = {t.get_text(): t for t in self.legenda.get_texts()}

                if parametro == "Fonte":
                    if valor in self.Fontes_Disponiveis:
                        valor = valor
                    else:
                        valor = "Arial"
                    mapeamento_legenda[Nome_Curva].set_fontfamily(valor)
                    mapeamento_legenda[Nome_Curva].set_fontsize(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"])
                    mapeamento_legenda[Nome_Curva].set_color(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"])
                    if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"] == True:
                        mapeamento_legenda[Nome_Curva].set_fontweight('bold')
                    else:
                        mapeamento_legenda[Nome_Curva].set_fontweight('normal')
                    if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"] == True:
                        mapeamento_legenda[Nome_Curva].set_fontstyle('italic')
                    else:
                        mapeamento_legenda[Nome_Curva].set_fontstyle('normal')

                    self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"] = valor
                    
                    self.canvas_P.draw_idle()
                elif parametro == "Tamanho_Fonte":
                    mapeamento_legenda[Nome_Curva].set_fontsize(valor)
                    mapeamento_legenda[Nome_Curva].set_fontfamily(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"])
                    mapeamento_legenda[Nome_Curva].set_color(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"])
                    if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"] == True:
                        mapeamento_legenda[Nome_Curva].set_fontweight('bold')
                    else:
                        mapeamento_legenda[Nome_Curva].set_fontweight('normal')
                    if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"] == True:
                        mapeamento_legenda[Nome_Curva].set_fontstyle('italic')
                    else:
                        mapeamento_legenda[Nome_Curva].set_fontstyle('normal')

                    self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"] = valor
                    
                    self.canvas_P.draw_idle()
                elif parametro == "Cor_Fonte":
                    if valor in self.Dicionario_Cores:
                        valor = self.Dicionario_Cores[valor]
                    try:
                        mapeamento_legenda[Nome_Curva].set_color(valor)
                        mapeamento_legenda[Nome_Curva].set_fontsize(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontfamily(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"])
                        if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"] == True:
                            mapeamento_legenda[Nome_Curva].set_fontweight('bold')
                        else:
                            mapeamento_legenda[Nome_Curva].set_fontweight('normal')
                        if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"] == True:
                            mapeamento_legenda[Nome_Curva].set_fontstyle('italic')
                        else:
                            mapeamento_legenda[Nome_Curva].set_fontstyle('normal')

                        self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"] = valor
                        
                        self.canvas_P.draw_idle()
                    except:
                        self.ui.statusbar.showMessage("Cor inválida", 1000)
                        return
                elif parametro == "Negrito":
                    if self.ui.CB_Negrito_Legenda.isChecked():
                        mapeamento_legenda[Nome_Curva].set_fontweight(valor)
                        mapeamento_legenda[Nome_Curva].set_color(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontsize(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontfamily(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"])
                        if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"] == True:
                            mapeamento_legenda[Nome_Curva].set_fontstyle('italic')
                        else:
                            mapeamento_legenda[Nome_Curva].set_fontstyle('normal')
                        self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"] = True
                        
                        self.canvas_P.draw_idle()
                    else:
                        valor = 'normal'
                        mapeamento_legenda[Nome_Curva].set_fontweight(valor)
                        mapeamento_legenda[Nome_Curva].set_color(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontsize(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontfamily(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"])
                        if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"] == True:
                            mapeamento_legenda[Nome_Curva].set_fontstyle('italic')
                        else:
                            mapeamento_legenda[Nome_Curva].set_fontstyle('normal')
                        self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"] = False
                        
                        self.canvas_P.draw_idle()
                elif parametro == "Italico":
                    if self.ui.CB_Italico_Legenda.isChecked():
                        mapeamento_legenda[Nome_Curva].set_fontstyle(valor)
                        mapeamento_legenda[Nome_Curva].set_color(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontsize(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontfamily(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"])
                        if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"] == True:
                            mapeamento_legenda[Nome_Curva].set_fontweight('bold')
                        else:
                            mapeamento_legenda[Nome_Curva].set_fontweight('normal')

                        self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"] = True
                        
                        self.canvas_P.draw_idle()
                    else:
                        valor = 'normal'
                        mapeamento_legenda[Nome_Curva].set_fontstyle(valor)
                        mapeamento_legenda[Nome_Curva].set_color(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontsize(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_fontfamily(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"])
                        if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"] == True:
                            mapeamento_legenda[Nome_Curva].set_fontweight('bold')
                        else:
                            mapeamento_legenda[Nome_Curva].set_fontweight('normal')

                        self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"] = False
                        
                        self.canvas_P.draw_idle()
            
            
            elif identificador == "Texto da legenda":
                if self.Lista_Curvas_Plotadas != {}:
                    for Nome_Curva in self.Lista_Curvas_Plotadas:
                        self.Parametro_Arbitrario_Legenda = 1
                        self.Atualizar_Legenda(Nome_Curva, identificador, parametro, valor)
                        self.Parametro_Arbitrario_Legenda = 0
            
            
            elif identificador == "Localização":
                valor2 = self.Dicionario_Locais[valor]
                self.legenda.set_loc(valor2)
                self.Dicionario_Global["Legendas"]["Localizacao"] = valor
                
                self.canvas_P.draw_idle()
            

            elif identificador == "Caixa da legenda":
                caixa = self.legenda.get_frame()
                if parametro == "Arredondamento":
                    bbox_x, bbox_y = caixa.get_x(), caixa.get_y()
                    bbox_width, bbox_height = caixa.get_width(), caixa.get_height()

                    if valor == 0:
                        caixa.set_boxstyle("square")
                    else:
                        caixa.set_boxstyle(f"round,pad=0.1, rounding_size={valor / 20}")
                        
                    caixa.set_bounds(bbox_x, bbox_y, bbox_width, bbox_height)
                    self.Dicionario_Global["Legendas"]["Caixa"]["Arredondamento"] = valor
                    self.canvas_P.draw_idle()
                elif parametro == "Cor_Fundo":
                    if valor in self.Dicionario_Cores:
                        valor = self.Dicionario_Cores[valor]
                    try:
                        caixa.set_facecolor(valor)
                        self.Dicionario_Global["Legendas"]["Caixa"]["Cor_Fundo"] = valor
                        
                        self.canvas_P.draw_idle()
                    except Exception as e:
                        self.ui.statusbar.showMessage("Cor inválida", 1000)
                        return
                elif parametro == "Transparencia":
                    caixa.set_alpha(valor / 100)
                    self.Dicionario_Global["Legendas"]["Caixa"]["Transparencia"] = valor
                    
                    self.canvas_P.draw_idle()
            

            elif identificador == "Borda":
                if self.ui.CB_Ativar_Borda_Legenda.isChecked():
                    caixa = self.legenda.get_frame()
                    if parametro == "Cor":
                        if valor in self.Dicionario_Cores:
                            valor = self.Dicionario_Cores[valor]
                        try:
                            caixa.set_edgecolor(valor)
                            self.Dicionario_Global["Legendas"]["Borda"]["Cor"] = valor
                            
                            self.canvas_P.draw_idle()
                        except Exception as e:
                            self.ui.statusbar.showMessage("Cor inválida", 1000)
                            return
                    elif parametro == "Espessura":
                        caixa.set_linewidth(float(valor)/10)
                        self.Dicionario_Global["Legendas"]["Borda"]["Espessura"] = valor
                        self.canvas_P.draw_idle()

    def Atualizar_Grades(self, identificador, parametro, valor):
        if identificador == "Principal" and self.ui.CB_Ativar_Grade_Principal.isChecked():
            if parametro == "Estilo":
                if valor == "Linha sólida":
                    valor = '-'
                elif valor == "Linha tracejada":
                    valor = '--'
                elif valor == "Linha ponto-tracejada":
                    valor = '-.'
                elif valor == 'Linha pontilhada':
                    valor = ':'
                try:
                    self.ax.grid(True, which='major', linestyle = valor, 
                                linewidth = (self.Dicionario_Global["Grades"]["Principal"]["Espessura"])/5, 
                                alpha=(self.Dicionario_Global["Grades"]["Principal"]["Transparencia"])/100, 
                                color=self.Dicionario_Global["Grades"]["Principal"]["Cor"])
                    self.Dicionario_Global["Grades"]["Principal"]["Estilo"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao atualizar grade principal: {e}")
            elif parametro == "Espessura":
                try:
                    self.ax.grid(True, which='major', linestyle = self.Dicionario_Global["Grades"]["Principal"]["Estilo"], 
                                linewidth = (valor)/5, 
                                alpha=(self.Dicionario_Global["Grades"]["Principal"]["Transparencia"])/100, 
                                color=self.Dicionario_Global["Grades"]["Principal"]["Cor"])
                    self.Dicionario_Global["Grades"]["Principal"]["Espessura"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao atualizar grade principal: {e}")
            elif parametro == "Transparencia":
                try:
                    self.ax.grid(True, which='major', linestyle = self.Dicionario_Global["Grades"]["Principal"]["Estilo"], 
                                linewidth = (self.Dicionario_Global["Grades"]["Principal"]["Espessura"])/5, 
                                alpha=(valor)/100, 
                                color=self.Dicionario_Global["Grades"]["Principal"]["Cor"])
                    self.Dicionario_Global["Grades"]["Principal"]["Transparencia"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao atualizar grade principal: {e}")
            elif parametro == "Cor":
                if valor in self.Dicionario_Cores:
                    valor = self.Dicionario_Cores[valor]
                try:
                    self.ax.grid(True, which='major', linestyle = self.Dicionario_Global["Grades"]["Principal"]["Estilo"], 
                                linewidth = (self.Dicionario_Global["Grades"]["Principal"]["Espessura"])/5, 
                                alpha=(self.Dicionario_Global["Grades"]["Principal"]["Transparencia"])/100, 
                                color=valor)
                    self.Dicionario_Global["Grades"]["Principal"]["Cor"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    self.ui.statusbar.showMessage("Cor inválida", 1000)
                    return
        if identificador == "Secundaria" and self.ui.CB_Ativar_Grade_Secundaria.isChecked():
            if parametro == "Estilo":
                if valor == "Linha sólida":
                    valor = '-'
                elif valor == "Linha tracejada":
                    valor = '--'
                elif valor == "Linha ponto-tracejada":
                    valor = '-.'
                elif valor == 'Linha pontilhada':
                    valor = ':'
                try:
                    self.ax.grid(True, which='minor', linestyle = valor, 
                                linewidth = (self.Dicionario_Global["Grades"]["Secundaria"]["Espessura"])/5,
                                alpha=(self.Dicionario_Global["Grades"]["Secundaria"]["Transparencia"])/100, 
                                color=self.Dicionario_Global["Grades"]["Secundaria"]["Cor"])
                    self.Dicionario_Global["Grades"]["Secundaria"]["Estilo"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao atualizar grade principal: {e}")
            elif parametro == "Espessura":
                try:
                    self.ax.grid(True, which='minor', linestyle = self.Dicionario_Global["Grades"]["Secundaria"]["Estilo"], 
                                linewidth = (valor)/5, 
                                alpha=(self.Dicionario_Global["Grades"]["Secundaria"]["Transparencia"])/100, 
                                color=self.Dicionario_Global["Grades"]["Secundaria"]["Cor"])
                    self.Dicionario_Global["Grades"]["Secundaria"]["Espessura"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao atualizar grade principal: {e}")
            elif parametro == "Transparencia":
                try:
                    self.ax.grid(True, which='minor', linestyle = self.Dicionario_Global["Grades"]["Secundaria"]["Estilo"], 
                                linewidth = (self.Dicionario_Global["Grades"]["Secundaria"]["Espessura"])/5, 
                                alpha=(valor)/100, 
                                color=self.Dicionario_Global["Grades"]["Secundaria"]["Cor"])
                    self.Dicionario_Global["Grades"]["Secundaria"]["Transparencia"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao atualizar grade principal: {e}")
            elif parametro == "Cor":
                if valor in self.Dicionario_Cores:
                    valor = self.Dicionario_Cores[valor]
                try:
                    self.ax.grid(True, which='minor', linestyle = self.Dicionario_Global["Grades"]["Secundaria"]["Estilo"], 
                                linewidth = (self.Dicionario_Global["Grades"]["Secundaria"]["Espessura"])/5, 
                                alpha=(self.Dicionario_Global["Grades"]["Secundaria"]["Transparencia"])/100, 
                                color=valor)
                    self.Dicionario_Global["Grades"]["Secundaria"]["Cor"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    self.ui.statusbar.showMessage("Cor inválida", 1000)
                    return

    def Atualizar_Bordas(self, identificador, parametro, valor):
        if identificador == "Superior" and self.ui.CB_Ativar_Borda_Superior.isChecked():
            if parametro == "Espessura":
                self.ax.spines['top'].set_linewidth(valor/10)
                self.Dicionario_Global["Bordas"]["Superior"]["Espessura"] = valor
                
                self.canvas_P.draw_idle()
            elif parametro == "Cor":
                if valor in self.Dicionario_Cores:
                    valor = self.Dicionario_Cores[valor]
                try:
                    self.ax.spines['top'].set_color(valor)
                    self.Dicionario_Global["Bordas"]["Superior"]["Cor"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    self.ui.statusbar.showMessage("Cor inválida", 1000)
                    return
        elif identificador == "Inferior" and self.ui.CB_Ativar_Borda_Inferior.isChecked():
            if parametro == "Espessura":
                self.ax.spines['bottom'].set_linewidth(valor/10)
                self.Dicionario_Global["Bordas"]["Inferior"]["Espessura"] = valor
                
                self.canvas_P.draw_idle()
            elif parametro == "Cor":
                if valor in self.Dicionario_Cores:
                    valor = self.Dicionario_Cores[valor]
                try:
                    self.ax.spines['bottom'].set_color(valor)
                    self.Dicionario_Global["Bordas"]["Inferior"]["Cor"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    self.ui.statusbar.showMessage("Cor inválida", 1000)
                    return
        elif identificador == "Direita" and self.ui.CB_Ativar_Borda_Direita.isChecked():
            if parametro == "Espessura":
                self.ax.spines['right'].set_linewidth(valor/10)
                self.Dicionario_Global["Bordas"]["Direita"]["Espessura"] = valor
                
                self.canvas_P.draw_idle()
            elif parametro == "Cor":
                if valor in self.Dicionario_Cores:
                    valor = self.Dicionario_Cores[valor]
                try:
                    self.ax.spines['right'].set_color(valor)
                    self.Dicionario_Global["Bordas"]["Direita"]["Cor"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    self.ui.statusbar.showMessage("Cor inválida", 1000)
                    return
        elif identificador == "Esquerda" and self.ui.CB_Ativar_Borda_Esquerda.isChecked():
            if parametro == "Espessura":
                self.ax.spines['left'].set_linewidth(valor/10)
                self.Dicionario_Global["Bordas"]["Esquerda"]["Espessura"] = valor
                
                self.canvas_P.draw_idle()
            elif parametro == "Cor":
                if valor in self.Dicionario_Cores:
                    valor = self.Dicionario_Cores[valor]
                try:
                    self.ax.spines['left'].set_color(valor)
                    self.Dicionario_Global["Bordas"]["Esquerda"]["Cor"] = valor
                    
                    self.canvas_P.draw_idle()
                except Exception as e:
                    self.ui.statusbar.showMessage("Cor inválida", 1000)
                    return

    def Atualizar_Grafico(self, tipo, identificador, parametro, valor):
        if tipo == "Curvas":
            self.Atualizar_Curva(identificador, parametro, valor)
        elif tipo == "Titulo":
            self.Atualizar_Titulo(identificador, parametro, valor)
        elif tipo == "Legendas" and not self.ui.CB_Usar_Predefinicao.isChecked():
            self.Atualizar_Legenda(self.ui.CombB_Selecionar_Curva_Legenda.currentText(), identificador, parametro, valor)
        elif tipo == "Legendas" and self.ui.CB_Usar_Predefinicao.isChecked() and self.parametro == 0:
            self.Atualizar_Legendas_Predefinidas()
        elif tipo == "Grades":
            self.Atualizar_Grades(identificador, parametro, valor)
        elif tipo == "Bordas":
            self.Atualizar_Bordas(identificador, parametro, valor)

    def Atualizar_Configuracoes_Curvas(self):
        Curva_Nova = self.ui.CombB_Selecionar_Curva.currentText()
        if Curva_Nova in self.Dicionario_Global["Curvas"]:
            if self.Dicionario_Global["Curvas"][Curva_Nova]["Visibilidade"] == True:
                self.ui.CB_Visibilidade_Curva.setCheckState(Qt.CheckState.Checked)
            else:
                self.ui.CB_Visibilidade_Curva.setCheckState(Qt.CheckState.Unchecked)
            self.ui.CombB_Cor_Curva.setCurrentText(self.Dicionario_Global["Curvas"][Curva_Nova]["Cor"])
            self.ui.SB_Espessura_Curva.setValue(int(self.Dicionario_Global["Curvas"][Curva_Nova]["Espessura"]))
            self.ui.CombB_Estilo_Curva.setCurrentText(self.Dicionario_Global["Curvas"][Curva_Nova]["Estilo"])
            self.ui.Slider_Transp_Curva.setValue(self.Dicionario_Global["Curvas"][Curva_Nova]["Transparencia"])
            if self.Dicionario_Global["Curvas"][Curva_Nova]["Marcador_Ativar"] == True:
                self.ui.CB_Ativar_Marcador.setCheckState(Qt.CheckState.Checked)
            else:
                self.ui.CB_Ativar_Marcador.setCheckState(Qt.CheckState.Unchecked)
            self.ui.CombB_Escolher_Marcador.setCurrentText(self.Dicionario_Global["Curvas"][Curva_Nova]["Marcador"])
            marcador = self.Dicionario_Global["Curvas"][Curva_Nova]["Marcador"]
            self.ui.CombB_Cor_Marcador.setCurrentText(self.Dicionario_Global["Curvas"][Curva_Nova]["Marcador_Cor"])
            self.ui.SB_Espessura_Marcador.setValue(int(self.Dicionario_Global["Curvas"][Curva_Nova]["Marcador_Espessura"]))
            self.ui.CombB_Cor_Borda_Marcador.setCurrentText(self.Dicionario_Global["Curvas"][Curva_Nova]["Marcador_Cor_Borda"])
            Curva_Nova = ""
        else:
            return

    def Atualizar_Configuracoes_Titulos(self):
        Titulo = self.ui.CombB_Escolher_Qual_Titulo.currentText()
        if not self.ui.CB_Usar_Predefinicao.isChecked():
            if Titulo == "Gráfico":
                Titulo = "T_Grafico"
                self.ui.CB_Ativar_Titulo_Grafico.setChecked(self.Dicionario_Global["Titulos"][Titulo]["Ativo"])
            elif Titulo == "Eixo X":
                Titulo = "T_Eixo_X"
                self.ui.CB_Ativar_Titulo_Eixo_X.setChecked(self.Dicionario_Global["Titulos"][Titulo]["Ativo"])
            elif Titulo == "Eixo Y":
                Titulo = "T_Eixo_Y"
                self.ui.CB_Ativar_Titulo_Eixo_Y.setChecked(self.Dicionario_Global["Titulos"][Titulo]["Ativo"])
            elif Titulo == "Valores X":
                Titulo = "Valores X"
            elif Titulo == "Valores Y":
                Titulo = "Valores Y"
        else:
            if Titulo == "Gráfico":
                Titulo = "T_Grafico"
            elif Titulo == "Eixo X":
                Titulo = "T_Eixo_X"
            elif Titulo == "Eixo Y":
                Titulo = "T_Eixo_Y"
            elif Titulo == "Valores X":
                Titulo = "Valores X"
            elif Titulo == "Valores Y":
                Titulo = "Valores Y"
        self.ui.FCombB_Fonte_Titulo.setCurrentText(self.Dicionario_Global["Titulos"][Titulo]["Fonte"])
        self.ui.SB_Tamanho_Fonte_Titulo.setValue(self.Dicionario_Global["Titulos"][Titulo]["Tamanho_Fonte"])
        self.ui.CB_Negrito_Titulo.setChecked(self.Dicionario_Global["Titulos"][Titulo]["Negrito"])
        self.ui.CB_Italico_Titulo.setChecked(self.Dicionario_Global["Titulos"][Titulo]["Italico"])
        self.ui.CombB_Cor_Fonte_Titulo.setCurrentText(self.Dicionario_Global["Titulos"][Titulo]["Cor_Fonte"])

    def Atualizar_Configuracoes_Legendas(self):
        Nome_Curva = self.ui.CombB_Selecionar_Curva_Legenda.currentText()
        if Nome_Curva in self.Dicionario_Global["Curvas"]:
            self.ui.FCombB_Fonte_Legenda.setCurrentText(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"])
            self.ui.SB_Tamanho_Fonte_Legenda.setValue(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"])
            self.ui.CombB_Cor_Fonte_Legenda.setCurrentText(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"])
            self.ui.CB_Negrito_Legenda.setChecked(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"])
            self.ui.CB_Italico_Legenda.setChecked(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"])
        else:
            return

    def Ativar_Marcador(self):
        if self.ui.CB_Ativar_Marcador.isChecked():
            self.Atualizar_Curva(self.ui.CombB_Selecionar_Curva.currentText(), "Marcador", self.Dicionario_Global["Curvas"][self.ui.CombB_Selecionar_Curva.currentText()]["Marcador"])
            self.Dicionario_Global["Curvas"][self.ui.CombB_Selecionar_Curva.currentText()]["Marcador_Ativar"] = True
            
            self.canvas_P.draw_idle()
            return
        else:
            Curva = self.Lista_Curvas_Plotadas.get(self.ui.CombB_Selecionar_Curva.currentText())
            Curva.set_marker("")
            self.Dicionario_Global["Curvas"][self.ui.CombB_Selecionar_Curva.currentText()]["Marcador_Ativar"] = False
            
            self.canvas_P.draw_idle()
            return

    def Ativar_Legenda(self):
        if self.ui.CB_Usar_Predefinicao.isChecked():
            return
        try:
            if self.ui.CB_Ativar_Legendas.isChecked():
                self.nome_curva = [curva for curva in self.Lista_Curvas_Plotadas]
                if self.legenda is not None and self.nome_curva2 != self.nome_curva:
                    self.legenda.remove()
                    self.legenda = None

                if self.legenda == None:
                    self.legenda = self.ax.legend()
                    
                    self.canvas_P.draw_idle()
                    self.nome_curva2 = [curva for curva in self.Lista_Curvas_Plotadas]
                    self.Dicionario_Global["Legendas"]["Ativar"] = True
                else:
                    self.legenda.set_visible(True)
                    self.Dicionario_Global["Legendas"]["Ativar"] = True
                    
                    self.canvas_P.draw_idle()
                    self.nome_curva2 = [curva for curva in self.Lista_Curvas_Plotadas]
            else:
                self.legenda.set_visible(False)
                self.Dicionario_Global["Legendas"]["Ativar"] = False
                self.nome_curva2 = [curva for curva in self.Lista_Curvas_Plotadas]
                self.canvas_P.draw_idle()
        except Exception as e:
            QMessageBox.critical(self.interface, "Erro", f"Erro ao ativar legenda: {e}")

    def Ativar_Borda_Legenda(self):
        if self.ui.CB_Ativar_Borda_Legenda.isChecked():
            try:
                caixa = self.legenda.get_frame()
                caixa.set_linewidth(self.ui.SB_Espessura_Borda_Legenda.value()/10)
                self.Dicionario_Global["Legendas"]["Borda"]["Ativar"] = True
                
                self.canvas_P.draw_idle()
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao ativar borda da legenda: {e}")
        else:
            try:
                caixa = self.legenda.get_frame()
                caixa.set_linewidth(0)
                self.Dicionario_Global["Legendas"]["Borda"]["Ativar"] = False
                
                self.canvas_P.draw_idle()
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao desativar borda da legenda: {e}")

    def Ativar_Grade_Principal(self):
        if self.ui.CB_Ativar_Grade_Principal.isChecked():
            try:
                self.ax.grid(True)
                self.Dicionario_Global["Grades"]["Principal"]["Ativar"] = True
                
                self.canvas_P.draw_idle()
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao ativar grade principal: {e}")
        else:
            try:
                self.ax.grid(False)
                self.Dicionario_Global["Grades"]["Principal"]["Ativar"] = False
                
                self.canvas_P.draw_idle()
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao desativar grade principal: {e}")

    def Ativar_Grade_Secundaria(self):
        self.ax.tick_params(axis='both', which='minor', direction='in', length=4, width=0.5)
        if self.ui.CB_Ativar_Grade_Secundaria.isChecked():
            self.ax.minorticks_on()
            try:
                self.ax.grid(True, which='minor')
                self.Dicionario_Global["Grades"]["Secundaria"]["Ativar"] = True
                
                self.canvas_P.draw_idle()
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao ativar grade secundaria: {e}")
        else:
            try:
                self.ax.grid(False, which='minor')
                self.Dicionario_Global["Grades"]["Secundaria"]["Ativar"] = False
                
                self.canvas_P.draw_idle()
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao desativar grade secundaria: {e}")

    def Ativar_Borda(self, borda):
        if borda == "Superior" and self.ui.CB_Ativar_Borda_Superior.isChecked():
            self.ax.spines['top'].set_visible(True)
            self.Dicionario_Global["Bordas"]["Superior"]["Ativar"] = True
            
            self.canvas_P.draw_idle()
        elif borda == "Inferior" and self.ui.CB_Ativar_Borda_Inferior.isChecked():
            self.ax.spines['bottom'].set_visible(True)
            self.Dicionario_Global["Bordas"]["Inferior"]["Ativar"] = True
            
            self.canvas_P.draw_idle()
        elif borda == "Direita" and self.ui.CB_Ativar_Borda_Direita.isChecked():
            self.ax.spines['right'].set_visible(True)
            self.Dicionario_Global["Bordas"]["Direita"]["Ativar"] = True
            
            self.canvas_P.draw_idle()
        elif borda == "Esquerda" and self.ui.CB_Ativar_Borda_Esquerda.isChecked():
            self.ax.spines['left'].set_visible(True)
            self.Dicionario_Global["Bordas"]["Esquerda"]["Ativar"] = True
            
            self.canvas_P.draw_idle()

        elif borda == "Superior":
            self.ax.spines['top'].set_visible(False)
            self.Dicionario_Global["Bordas"]["Superior"]["Ativar"] = False
            
            self.canvas_P.draw_idle()
        elif borda == "Inferior":
            self.ax.spines['bottom'].set_visible(False)
            self.Dicionario_Global["Bordas"]["Inferior"]["Ativar"] = False
            
            self.canvas_P.draw_idle()
        elif borda == "Direita":
            self.ax.spines['right'].set_visible(False)
            self.Dicionario_Global["Bordas"]["Direita"]["Ativar"] = False
            
            self.canvas_P.draw_idle()
        elif borda == "Esquerda":
            self.ax.spines['left'].set_visible(False)
            self.Dicionario_Global["Bordas"]["Esquerda"]["Ativar"] = False
            
            self.canvas_P.draw_idle()

    def Adicionar_Curva_Plotada(self, Nome_Curva):
        if Nome_Curva in self.Dicionario_Global["Curvas"]:
            return
        self.Dicionario_Global["Curvas"][Nome_Curva] = {
            "Visibilidade": True,
            "Cor": "#000000",
            "Espessura": 15,
            "Estilo": "Linha sólida",
            "Transparencia": 100,
            "Marcador_Ativar": False,
            "Marcador": "Círculo",
            "Marcador_Cor_Borda": "#000000",
            "Marcador_Cor": "#000000",
            "Marcador_Espessura": 5,
            "Legenda": {
                "Texto": Nome_Curva,
                "Fonte": "Arial",
                "Tamanho_Fonte": 10,
                "Cor_Fonte": "#000000",
                "Negrito": False,
                "Italico": False
            },
        }

    def Gerar_Grafico(self):
        self.fig, self.ax = plt.subplots()
        largura = ''
        altura = ''

        if self.ui.CombB_Escalas.currentText() == "Logarítmica":
            self.ax.set_xscale("log")
            self.ax.set_yscale("log")
        elif self.ui.CombB_Escalas.currentText() == "Semilog X":
            self.ax.set_xscale("log")
            self.ax.set_yscale("linear")
        elif self.ui.CombB_Escalas.currentText() == "Semilog Y":
            self.ax.set_xscale("linear")
            self.ax.set_yscale("log")
                    
        if self.ui.CB_Ativar_Limite_X.isChecked():
            lim_inf_x = self.ui.LE_Lim_Inf_X.text()
            lim_sup_x = self.ui.LE_Lim_Sup_X.text()
            if lim_inf_x == "" or lim_sup_x == "":
                QMessageBox.critical(self.interface, "Erro", "Limites do eixo X inválidos. Defina valores válidos ou desative-os.")
                return
            try:
                lim_sup_x = float(lim_sup_x)
                lim_inf_x = float(lim_inf_x)
                if lim_inf_x <= lim_sup_x:
                    self.ax.set_xlim(xmin=lim_inf_x, xmax=lim_sup_x)
                else:
                    QMessageBox.critical(self.interface, "Erro", f"Limite inferior maior ou igual que o superior")
                    return
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir limites do eixo x: {e}")
                return
            
        if self.ui.CB_Ativar_Limite_Y.isChecked():
            lim_inf_y = self.ui.LE_Lim_Inf_Y.text()
            lim_sup_y = self.ui.LE_Lim_Sup_Y.text()
            if lim_inf_y == "" and lim_sup_y == "":
                QMessageBox.critical(self.interface, "Erro", "Limites do eixo Y inválidos. Defina valores válidos ou desative-os.")
                return
            try:
                lim_sup_y = float(lim_sup_y)
                lim_inf_y = float(lim_inf_y)
                if lim_inf_y <= lim_sup_y:
                    self.ax.set_ylim(ymin=lim_inf_y, ymax=lim_sup_y)
                else:
                    QMessageBox.critical(self.interface, "Erro", f"Limite inferior maior ou igual que o superior")
                    return
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir limites do eixo y: {e}")
                return

        if self.ui.CB_Ativar_Titulo_Grafico.isChecked():
            if self.ui.LE_Titulo_Grafico.text() == "":
                QMessageBox.critical(self.interface, "Erro", "Título do gráfico inválido. Coloque um nome válido ou desative-o.")
                return
            try:
                titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                self.ax.set_title(titulo_Grafico)
                self.Dicionario_Global["Titulos"]["T_Grafico"]["Texto"] = titulo_Grafico
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")

        if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked():
            if self.ui.LE_Titulo_Eixo_X.text() == "":
                QMessageBox.critical(self.interface, "Erro", "Título do eixo X inválido. Coloque um nome válido ou desative-o.")
                return
            try:
                Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                self.ax.set_xlabel(Titulo_Eixo_X)
                self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Texto"] = Titulo_Eixo_X
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")

        if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked():
            if self.ui.LE_Titulo_Eixo_Y.text() == "":
                QMessageBox.critical(self.interface, "Erro", "Título do eixo Y inválido. Coloque um nome válido ou desative-o.")
                return
            try:
                Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                self.ax.set_ylabel(Titulo_Eixo_Y)
                self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Texto"] = Titulo_Eixo_Y
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")

        if self.ui.DSB_Dimensao_Altura.value() != 0 and self.ui.DSB_Largura.value() != 0:
            largura = self.ui.DSB_Largura.value()/2.54
            altura = self.ui.DSB_Dimensao_Altura.value()/2.54
            self.fig.set_size_inches(largura, altura)

        if self.canvas is not None:
            resposta = QMessageBox.question(self.interface, "Aviso", "Ao gerar outro gráfico, o gráfico atual será perdido. Deseja continuar?")
            if resposta == QtWidgets.QMessageBox.StandardButton.Yes:    
                try:
                    self.ui.Layout_W_Grafico.removeWidget(self.canvas)
                    self.canvas.deleteLater()
                    self.Lista_Curvas_Plotadas.clear()
                    self.ui.Layout_W_Grafico_Personalizacao.removeWidget(self.canvas)
                    self.canvas_P.deleteLater()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro: {e}")
            else:
                return

        self.ui.CombB_Selecionar_Curva.clear()
        self.ui.CombB_Selecionar_Curva_Legenda.clear()
        self.Lista_Curvas_Plotadas.clear()
        self.Indices_Curvas.clear()
        self.Dicionario_Global["Curvas"] = {}

        for Curva in self.Curvas:
            if Curva.CB_Ativar_Curva.isChecked():
                Nome_Curva = Curva.Box_Modelo.title()
                self.Indices_Curvas[Nome_Curva] = Curva.CombB_Indice_Curva.currentText()
                contagem = Counter(self.Indices_Curvas.values())
                indices_duplicados = [indice for indice, qtd in contagem.items() if qtd > 1]
                if indices_duplicados:
                    QMessageBox.critical(self.interface, "Erro", "Há curvas com índices iguais. Altere os índices iguais ou desative uma das curvas.")
                    return

                Var_X = Curva.CombB_Variavel_X_Curva.currentText()
                Var_Y = Curva.CombB_Variavel_Y_Curva.currentText()
                if Var_X == "":
                    QMessageBox.critical(self.interface, "Erro", f"Variavel X inválida para {Nome_Curva}")
                    return
                if Var_Y == "":
                    QMessageBox.critical(self.interface, "Erro", f"Variavel Y inválida para {Nome_Curva}")
                    return
                Dados_X = self.Lista_Variaveis.get(Var_X)
                if self.tem_caracteres(Dados_X):
                    QMessageBox.critical(self.interface, "Erro", f"Há caracteres na variável X da curva {Nome_Curva}.")
                    return
                Dados_Y = self.Lista_Variaveis.get(Var_Y)
                if self.tem_caracteres(Dados_Y):
                    QMessageBox.critical(self.interface, "Erro", f"Há caracteres na variável Y da curva {Nome_Curva}.")
                try:
                    self.Lista_Curvas_Plotadas[Nome_Curva], = self.ax.plot(Dados_X, Dados_Y, label=Nome_Curva)
                    self.ui.CombB_Selecionar_Curva.addItem(Nome_Curva)
                    self.ui.CombB_Selecionar_Curva_Legenda.addItem(Nome_Curva)
                    self.Adicionar_Curva_Plotada(Curva.Box_Modelo.title())
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao plotar curva {Nome_Curva}: {e}")

        Densidade_X = self.ui.SB_Densidade_X.value()
        Densidade_Y = self.ui.SB_Densidade_Y.value()

        if Densidade_X != 0:
            x_min, x_max = self.ax.get_xlim()
            is_log_x = (self.ax.get_xscale() == 'log')

            if not is_log_x:
                x_ticks = self.Calcula_Espacamento(x_min, x_max, Densidade_X)
                self.ax.set_xticks(x_ticks)
            
        if Densidade_Y != 0:
            y_min, y_max = self.ax.get_ylim()
            is_log_y = (self.ax.get_yscale() == 'log')

            if not is_log_y:
                y_ticks = self.Calcula_Espacamento(y_min, y_max, Densidade_Y)
                self.ax.set_yticks(y_ticks)


        self.nome_curva2 = ['']

        largura = self.fig.get_figwidth()
        altura = self.fig.get_figheight()

        fig_bytes = pickle.dumps(self.fig)
        self.fig_2 = pickle.loads(fig_bytes)
        self.canvas = FigureCanvas(self.fig_2)
        self.canvas.setFixedSize(int(largura * 100), int(altura * 100))
        self.fig.tight_layout()
        self.fig_2.tight_layout()
        self.ui.Layout_W_Grafico.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        self.canvas.draw()
        self.canvas_P = FigureCanvas(self.fig)
        self.canvas_P.setFixedSize(int(largura * 100), int(altura * 100))
        self.ui.Layout_W_Grafico_Personalizacao.insertWidget(0, self.canvas_P, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.B_Copiar_Grafico.setEnabled(True)
        self.ui.B_Exportar_Grafico.setEnabled(True)
        self.ui.B_Copiar_Grafico.setVisible(True)
        self.ui.B_Exportar_Grafico.setVisible(True)
        self.canvas_P.draw()

        if self.toolbar != None:
            self.ui.Layout_W_Grafico_Personalizacao.removeWidget(self.toolbar)
            self.toolbar.setParent(None)
            self.toolbar.deleteLater()
            self.toolbar = None

        self.toolbar = None

        self.toolbar = NavigationToolbar(self.canvas_P, self.interface)
        self.ui.Layout_W_Grafico_Personalizacao.insertWidget(1, self.toolbar)
        self.canvas.draw_idle()
        self.canvas_P.draw_idle()
        self.ui.statusbar.showMessage("Gráfico gerado com sucesso!", 3000)
        self.Inicia_Timer(3000)

    def tem_caracteres(self, lista):
        if not isinstance(lista, (list, tuple)):
            lista = [lista]
        
        for x in lista:
            if isinstance(x, (np.ndarray, list, tuple)):
                if len(x) == 1:
                    x = x[0]
                else:
                    continue
            try:
                float(x)
            except ValueError:
                return True
        return False

    def Mostrar_Curvas_Legenda(self, state):
        if state == 2:
            self.ui.label_Curva_L.setVisible(True)
            self.ui.CombB_Selecionar_Curva_Legenda.setVisible(True)
            self.Parametro_Arbitrario_Legenda = 1
            self.Dicionario_Global["Legendas"]["Seleção_individual"] = True
        elif state == 0:
            self.ui.label_Curva_L.setVisible(False)
            self.ui.CombB_Selecionar_Curva_Legenda.setVisible(False)
            self.Parametro_Arbitrario_Legenda = 0
            self.Dicionario_Global["Legendas"]["Seleção_individual"] = False

    def Adicionar_Curva(self):
        Numero_Curva = len(self.Curvas) + 1
        Curva_Nova = CurveWidget(Numero_Curva, self.Curvas)
        self.Curvas.append(Curva_Nova)
        self.ui.scroll_Layout.addWidget(Curva_Nova)
        self.Atualizar_Indices_Disponiveis()
        self.Atualizar_Variaveis_Disponiveis()

    def Excluir_Variavel(self):
        Variavel_Selecionada = self.ui.ListW_Listas_Var_Importadas.currentItem()
        if Variavel_Selecionada:
            Nome_Variavel = self.ui.ListW_Listas_Var_Importadas.currentItem().text()
        else:
            return
        indice_Variavel = self.ui.ListW_Listas_Var_Importadas.row(Variavel_Selecionada)
        self.ui.ListW_Listas_Var_Importadas.takeItem(indice_Variavel)
        self.Lista_Variaveis.pop(Nome_Variavel, None)
        self.ui.statusbar.showMessage(f"Variável {Nome_Variavel} excluída com sucesso!", 3000)
        for Curva in self.Curvas:
            indice = Curva.CombB_Variavel_X_Curva.findText(Nome_Variavel)
            Curva.CombB_Variavel_X_Curva.removeItem(indice)
            Curva.CombB_Variavel_Y_Curva.removeItem(indice)
        self.Inicia_Timer(3000)

    def Importar_Variaveis(self):
        Variaveis_Selecionadas = self.ui.Lista_Var_Codigo.selectedItems()

        for variavel in Variaveis_Selecionadas:
            Nome_Var = variavel.text()
            
            if Nome_Var in self.Lista_Variaveis:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Atenção")
                msg_box.setText("Variavel já existente. \n Deseja substituir o arquivo existente?")
                msg_box.setIcon(QMessageBox.Icon.Warning)
                substituir_btn = msg_box.addButton("Substituir", QMessageBox.ButtonRole.AcceptRole)
                cancelar_btn = msg_box.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
                msg_box.exec()

                if msg_box.clickedButton() == substituir_btn:
                    self.Lista_Variaveis[Nome_Var] = self.Lista_Variaveis_Codigo.get(Nome_Var)
                    continue
                elif msg_box.clickedButton() == cancelar_btn:
                    msg_box.close()
                    return
                

            Valor_Var = self.Lista_Variaveis_Codigo.get(Nome_Var)

            self.ui.ListW_Listas_Var_Importadas.addItem(Nome_Var)
            self.Lista_Variaveis[Nome_Var] = Valor_Var
        self.Atualizar_Variaveis_Disponiveis()
        self.ui.statusbar.showMessage("Variáveis importadas com sucesso!", 3000)
        self.Inicia_Timer(3000)

    def Executar_Codigo(self):
        self.ui.Lista_Var_Codigo.clear()
        codigo = self.ui.Local_Codigo.toPlainText()

        Variaveis_Locais = {}
        Variaveis_Locais = {"plt": plt}
        Variaveis_Locais["plt"].show = lambda: None
        try:
            exec(codigo, Variaveis_Locais)

            Variaveis_Locais.pop("__builtins__", None)
            
            Variaveis_Validas = {k: v for k, v in Variaveis_Locais.items() if not isinstance(v, types.ModuleType)}
            for self.Nome, Valor in Variaveis_Validas.items():
                self.ui.Lista_Var_Codigo.addItem(self.Nome)
                self.Lista_Variaveis_Codigo[self.Nome] = Valor
            
            self.ui.statusbar.showMessage("Código executado com sucesso!", 3000)
            self.Inicia_Timer(3000)

        except Exception as e:
            QMessageBox.critical(self.interface, "Erro", f"Erro ao executar código: {e}")

    def Importar_Variavel(self):
        self.Nome_Variavel = self.ui.LE_Nome_Variavel.text().strip()

        if not self.Nome_Variavel:
            QMessageBox.critical(self.interface, "Erro", f"Nome de variável inválido.")
            return
        
        celulas_selecionadas = self.ui.TW_Local_Tabela.selectedRanges()
        Dados_Selecionados = []

        for Celula in celulas_selecionadas:
            for row in range(Celula.topRow(), Celula.bottomRow()+1):
                for col in range(Celula.leftColumn(), Celula.rightColumn()+1):
                    Dados_Selecionados.append(self.data.iloc[row,col])

        if not Dados_Selecionados:
            QMessageBox.critical(self.interface, "Erro", f"Variável sem conteúdo.")
            return

        if self.Nome_Variavel in self.Lista_Variaveis:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Atenção")
            msg_box.setText("Variavel já existente. \n Deseja substituir o arquivo existente?")
            msg_box.setIcon(QMessageBox.Icon.Warning)
            substituir_btn = msg_box.addButton("Substituir", QMessageBox.ButtonRole.AcceptRole)
            cancelar_btn = msg_box.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
            msg_box.exec()
            if msg_box.clickedButton() == substituir_btn:
                    self.Lista_Variaveis[self.Nome_Variavel] = Dados_Selecionados
                    return
            elif msg_box.clickedButton() == cancelar_btn:
                msg_box.close()
                return

        self.Lista_Variaveis[self.Nome_Variavel] = Dados_Selecionados
        self.ui.ListW_Listas_Var_Importadas.addItem(self.Nome_Variavel)
        self.Atualizar_Variaveis_Disponiveis()
        self.ui.statusbar.showMessage(f"Variável '{self.Nome_Variavel}' importada com sucesso!", 3000)
        self.Inicia_Timer(3000)

    def Carrega_Planilha(self):
        file_path, _ = QFileDialog.getOpenFileName(self.interface, 'Abrir Planilha', '', 'Excel Files (*.xlsx *.xls *.csv)')
        QFileDialog.getSaveFileName
        
        if file_path:
            if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                try:
                    self.data = pd.read_excel(file_path, header=None)
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao abrir planilha: {e}")
                    return
            else:
                try:
                    self.data = pd.read_csv(file_path, header=None, delimiter=",")
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao abrir planilha: {e}")
                    return
                self.data = self.data.replace({r"[\[\]]":""}, regex=True)
            self.data = self.data.fillna("")
            self.Exibir_Dados()
            self.ui.statusbar.showMessage("Planilha importada com sucesso!", 3000)
            self.Inicia_Timer(3000)

    def Carrega_Arquivo_Texto(self):
        file_path, _ = QFileDialog.getOpenFileName(self.interface, 'Abrir Arquivo de Texto', '', 'Text Files (*.txt)')
        QFileDialog.getSaveFileName

        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.Texto = file.read()
            
            self.ui.Local_Arquivo_Txt.setPlainText(self.Texto)
            self.ui.statusbar.showMessage("Arquivo de texto importado com sucesso!", 3000)
            self.Inicia_Timer(3000)

    def Gerar_Planilha(self):
        if self.ui.LE_Separador_Personalizado.text() != "":
            separador = self.ui.LE_Separador_Personalizado.text()
        else:
            separador = self.ui.CombB_Separadores_Disponiveis.currentText()
        if separador == "Tabulação":
            separador = "\t"
        elif separador == "Espaço":
            separador = " "
        elif separador == "Vírgula":
            separador = ","
        elif separador == "Ponto":
            separador = "."
        elif separador == "Ponto e vírgula":
            separador = ";"
        elif separador == "Dois pontos":
            separador = ":"
        
        Texto = self.ui.Local_Arquivo_Txt.toPlainText()
        linhas = Texto.split("\n")
        
        padrao = re.compile(r'^[\d\s\.,;:]+$')

        Dados = []

        for linha in linhas:
            linha = linha.strip()

            if linha and padrao.match(linha):
                valores = linha.split(separador)
                
                try:
                    valores = [float(v.replace(",", ".")) for v in valores]
                    Dados.append(valores)
                except:
                    pass
        
        self.data = pd.DataFrame(Dados)

        self.dialogo = Dialog_Previa_Planilha(self.data)
        resultado = self.dialogo.exec()

        if self.dialogo.Estado == 1:
            self.Exibir_Dados()
            self.ui.statusbar.showMessage("Planilha gerada com sucesso! Acesse (Seleção de dados -> Planilha) para vizualizar os dados.", 6000)
            self.Inicia_Timer(6000)
        else:
            return

    def Exibir_Dados(self):
        if self.data is not None:
            self.ui.TW_Local_Tabela.setRowCount(self.data.shape[0])
            self.ui.TW_Local_Tabela.setColumnCount(self.data.shape[1])

        for row in range(self.data.shape[0]):
            for col in range(self.data.shape[1]):
                self.ui.TW_Local_Tabela.setItem(row, col, QTableWidgetItem(str(self.data.iloc[row, col])))

    def Mudar_Aba_Parametro_Legenda(self, index):
        self.Mudar_Aba_Personalizacao(2)
        if index == 0:
            index = 2
        elif index == 1:
            index = 0
        elif index == 2:
            index = 1
        self.ui.Stkd_Parametros_Legenda.setCurrentIndex(index)

    def Mudar_Aba_Personalizacao(self, index):
        self.ui.Stkd_Principal.setCurrentIndex(5)
        self.ui.Stkd_Abas_Personalizacao.setCurrentIndex(index)
    
    def Mudar_Aba_Principal(self, index):
        self.ui.Stkd_Principal.setCurrentIndex(index)

    def Calcula_Espacamento(self, min, max, num_div):
        intervalo = (max - min) / num_div  
        base = 10 ** np.floor(np.log10(intervalo))
        espacamento = round(intervalo / base) * base

        ticks = np.arange(np.ceil(min / espacamento) * espacamento, max, espacamento)

        return ticks

    def Atualizar_Variaveis_Disponiveis(self):
        for Curva in self.Curvas:
            for Variavel in self.Lista_Variaveis:
                if Curva.CombB_Variavel_X_Curva.findText(Variavel) == -1:
                    Curva.CombB_Variavel_X_Curva.addItem(Variavel)
                if Curva.CombB_Variavel_Y_Curva.findText(Variavel) == -1:
                    Curva.CombB_Variavel_Y_Curva.addItem(Variavel)                
                
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    def Gerar_Grafico_Predef(self):
        self.fig, self.ax = plt.subplots()
        largura = ''
        altura = ''

        if self.ui.CombB_Escalas.currentText() == "Logarítmica":
            self.ax.set_xscale("log")
            self.ax.set_yscale("log")
        elif self.ui.CombB_Escalas.currentText() == "Semilog X":
            self.ax.set_xscale("log")
            self.ax.set_yscale("linear")
        elif self.ui.CombB_Escalas.currentText() == "Semilog Y":
            self.ax.set_xscale("linear")
            self.ax.set_yscale("log")
                    
        if self.ui.CB_Ativar_Limite_X.isChecked():
            lim_inf_x = self.ui.LE_Lim_Inf_X.text()
            lim_sup_x = self.ui.LE_Lim_Sup_X.text()
            if lim_inf_x == "" or lim_sup_x == "":
                QMessageBox.critical(self.interface, "Erro", "Limites do eixo X inválidos. Defina valores válidos ou desative-os.")
                return
            try:
                lim_sup_x = float(lim_sup_x)
                lim_inf_x = float(lim_inf_x)
                if lim_inf_x <= lim_sup_x:
                    self.ax.set_xlim(xmin=lim_inf_x, xmax=lim_sup_x)
                else:
                    QMessageBox.critical(self.interface, "Erro", f"Limite inferior maior ou igual que o superior")
                    return
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir limites do eixo x: {e}")
                return
            
        if self.ui.CB_Ativar_Limite_Y.isChecked():
            lim_inf_y = self.ui.LE_Lim_Inf_Y.text()
            lim_sup_y = self.ui.LE_Lim_Sup_Y.text()
            if lim_inf_y == "" and lim_sup_y == "":
                QMessageBox.critical(self.interface, "Erro", "Limites do eixo Y inválidos. Defina valores válidos ou desative-os.")
                return
            try:
                lim_sup_y = float(lim_sup_y)
                lim_inf_y = float(lim_inf_y)
                if lim_inf_y <= lim_sup_y:
                    self.ax.set_ylim(ymin=lim_inf_y, ymax=lim_sup_y)
                else:
                    QMessageBox.critical(self.interface, "Erro", f"Limite inferior maior ou igual que o superior")
                    return
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir limites do eixo y: {e}")
                return

        if self.ui.CB_Ativar_Titulo_Grafico.isChecked():
            if self.ui.LE_Titulo_Grafico.text() == "":
                QMessageBox.critical(self.interface, "Erro", "Título do gráfico inválido. Coloque um nome válido ou desative-o.")
                return
            try:
                titulo_Grafico = self.ui.LE_Titulo_Grafico.text()
                self.ax.set_title(titulo_Grafico)
                self.Dicionario_Global["Titulos"]["T_Grafico"]["Texto"] = titulo_Grafico
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do gráfico: {e}")

        if self.ui.CB_Ativar_Titulo_Eixo_X.isChecked():
            if self.ui.LE_Titulo_Eixo_X.text() == "":
                QMessageBox.critical(self.interface, "Erro", "Título do eixo X inválido. Coloque um nome válido ou desative-o.")
                return
            try:
                Titulo_Eixo_X = self.ui.LE_Titulo_Eixo_X.text()
                self.ax.set_xlabel(Titulo_Eixo_X)
                self.Dicionario_Global["Titulos"]["T_Eixo_X"]["Texto"] = Titulo_Eixo_X
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo X: {e}")

        if self.ui.CB_Ativar_Titulo_Eixo_Y.isChecked():
            if self.ui.LE_Titulo_Eixo_Y.text() == "":
                QMessageBox.critical(self.interface, "Erro", "Título do eixo Y inválido. Coloque um nome válido ou desative-o.")
                return
            try:
                Titulo_Eixo_Y = self.ui.LE_Titulo_Eixo_Y.text()
                self.ax.set_ylabel(Titulo_Eixo_Y)
                self.Dicionario_Global["Titulos"]["T_Eixo_Y"]["Texto"] = Titulo_Eixo_Y
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro ao definir título do eixo Y: {e}")

        if self.ui.DSB_Dimensao_Altura.value() != 0 and self.ui.DSB_Largura.value() != 0:
            largura = self.ui.DSB_Largura.value()/2.54
            altura = self.ui.DSB_Dimensao_Altura.value()/2.54
            self.fig.set_size_inches(largura, altura)

        if self.canvas is not None:
            resposta = QMessageBox.question(self.interface, "Aviso", "Ao gerar outro gráfico, o gráfico atual será perdido. Deseja continuar?")
            if resposta == QtWidgets.QMessageBox.StandardButton.Yes:    
                try:
                    self.ui.Layout_W_Grafico.removeWidget(self.canvas)
                    self.canvas.deleteLater()
                    self.Lista_Curvas_Plotadas.clear()
                    self.ui.Layout_W_Grafico_Personalizacao.removeWidget(self.canvas)
                    self.canvas_P.deleteLater()
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro: {e}")
            else:
                return

        self.ui.CombB_Selecionar_Curva.clear()
        self.ui.CombB_Selecionar_Curva_Legenda.clear()
        self.Lista_Curvas_Plotadas.clear()
        self.Indices_Curvas.clear()
        self.Dicionario_Global["Curvas"] = {}

        for Curva in self.Curvas:
            if Curva.CB_Ativar_Curva.isChecked():
                Nome_Curva = Curva.Box_Modelo.title()

                Var_X = Curva.CombB_Variavel_X_Curva.currentText()
                Var_Y = Curva.CombB_Variavel_Y_Curva.currentText()
                if Var_X == "":
                    QMessageBox.critical(self.interface, "Erro", f"Variavel X inválida para {Nome_Curva}")
                    return
                if Var_Y == "":
                    QMessageBox.critical(self.interface, "Erro", f"Variavel Y inválida para {Nome_Curva}")
                    return
                Dados_X = self.Lista_Variaveis.get(Var_X)
                Dados_Y = self.Lista_Variaveis.get(Var_Y)
                try:
                    self.Lista_Curvas_Plotadas[Nome_Curva], = self.ax.plot(Dados_X, Dados_Y, label=Nome_Curva)
                    self.Adicionar_Curva_Plotada(Nome_Curva)
                    self.ui.CombB_Selecionar_Curva.addItem(Nome_Curva)
                    self.ui.CombB_Selecionar_Curva_Legenda.addItem(Nome_Curva)
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao plotar curva {Nome_Curva}: {e}")
            

        Densidade_X = self.ui.SB_Densidade_X.value()
        Densidade_Y = self.ui.SB_Densidade_Y.value()

        if Densidade_X != 0 and Densidade_Y != 0:
            x_min, x_max = self.ax.get_xlim()
            y_min, y_max = self.ax.get_ylim()
            
            x_ticks = self.Calcula_Espacamento(x_min, x_max, Densidade_X)
            y_ticks = self.Calcula_Espacamento(y_min, y_max, Densidade_Y)

            self.ax.set_xticks(x_ticks)
            self.ax.set_yticks(y_ticks)

        self.nome_curva2 = ['']

        largura = self.fig.get_figwidth()
        altura = self.fig.get_figheight()

        self.fig.tight_layout()
        self.canvas_P = FigureCanvas(self.fig)
        self.canvas_P.setFixedSize(int(largura * 100), int(altura * 100))
        self.ui.Layout_W_Grafico_Personalizacao.insertWidget(0, self.canvas_P, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.B_Copiar_Grafico.setEnabled(True)
        self.ui.B_Exportar_Grafico.setEnabled(True)
        self.ui.B_Copiar_Grafico.setVisible(True)
        self.ui.B_Exportar_Grafico.setVisible(True)
        self.canvas_P.draw()

        if self.toolbar != None:
            self.ui.Layout_W_Grafico_Personalizacao.removeWidget(self.toolbar)
            self.toolbar.setParent(None)
            self.toolbar.deleteLater()
            self.toolbar = None

        self.toolbar = None

        self.toolbar = NavigationToolbar(self.canvas_P, self.interface)
        self.ui.Layout_W_Grafico_Personalizacao.insertWidget(1, self.toolbar)
        self.canvas_P.draw_idle()
        self.ui.statusbar.showMessage("Gráfico gerado com sucesso!", 3000)
        self.Inicia_Timer(3000)

        for Curva in self.Curvas:
            self.Atualiza_Configuracoes_Curva(Curva)


        self.Atualiza_Configuracoes_Interface()
        
        self.parametro == 0

        fig_bytes = pickle.dumps(self.fig)
        self.fig_2 = pickle.loads(fig_bytes)
        self.canvas = FigureCanvas(self.fig_2)
        self.canvas.setFixedSize(int(largura * 100), int(altura * 100))
        self.fig_2.tight_layout()
        self.ui.Layout_W_Grafico.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        self.canvas.draw()
        
    def Atualiza_Configuracoes_Interface(self):
        for Nome_Curva in self.Lista_Curvas_Plotadas:
            Curva1 = []
            for Curva in self.Curvas:
                if Curva.Box_Modelo.title() == Nome_Curva:
                    Curva1 = Curva
                    break
            self.ui.CombB_Selecionar_Curva.blockSignals(True)
            self.ui.CombB_Selecionar_Curva.setCurrentText(Nome_Curva)
            self.ui.CombB_Selecionar_Curva.blockSignals(False)
            if Curva1.CombB_Indice_Curva.currentText() in self.Dicionario_Global["Indices"].values():
                self.widgets_valores = {
                    self.ui.CB_Visibilidade_Curva: self.Dicionario_Global["Curvas"][Nome_Curva]["Visibilidade"],
                    self.ui.CombB_Cor_Curva: self.Dicionario_Global["Curvas"][Nome_Curva]["Cor"],
                    self.ui.SB_Espessura_Curva: self.Dicionario_Global["Curvas"][Nome_Curva]["Espessura"],
                    self.ui.CombB_Estilo_Curva: self.Dicionario_Estilos[self.Dicionario_Global["Curvas"][Nome_Curva]["Estilo"]] if self.Dicionario_Global["Curvas"][Nome_Curva]["Estilo"] in self.Dicionario_Estilos else self.Dicionario_Global["Curvas"][Nome_Curva]["Estilo"],
                    self.ui.Slider_Transp_Curva: self.Dicionario_Global["Curvas"][Nome_Curva]["Transparencia"],
                    self.ui.CB_Ativar_Marcador: self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Ativar"],
                    self.ui.CombB_Escolher_Marcador: self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador"],
                    self.ui.CombB_Cor_Marcador: self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Cor"],
                    self.ui.CombB_Cor_Borda_Marcador: self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Cor_Borda"],
                    self.ui.SB_Espessura_Marcador: self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Espessura"]
                }


                for widget, valor in self.widgets_valores.items():
                    widget.blockSignals(True)
                    
                    if isinstance(widget, QtWidgets.QComboBox):
                        widget.setCurrentText(valor)
                        widget.blockSignals(False)
                        widget.currentTextChanged.emit(widget.currentText())
                    elif isinstance(widget, QtWidgets.QSpinBox) or isinstance(widget, QtWidgets.QDoubleSpinBox):
                        widget.setValue(valor)
                        widget.blockSignals(False)
                        widget.valueChanged.emit(widget.value())

                    elif isinstance(widget, QtWidgets.QCheckBox):
                        widget.setCheckState(Qt.CheckState.Checked if valor else Qt.CheckState.Unchecked)
                        widget.blockSignals(False)
                        widget.stateChanged.emit(1 if widget.checkState() == Qt.CheckState.Checked else 0)

                    elif isinstance(widget, QtWidgets.QSlider):
                        widget.setValue(valor)
                        widget.blockSignals(False)
                        widget.valueChanged.emit(widget.value())
        
        Titulos = ["Gráfico", "Eixo X", "Eixo Y", "Valores X", "Valores Y"]
        for Titulo in Titulos:
            self.ui.CombB_Escolher_Qual_Titulo.setCurrentText(Titulo)
            if Titulo == "Gráfico":
                Titulo = "T_Grafico"
            elif Titulo == "Eixo X":
                Titulo = "T_Eixo_X"
            elif Titulo == "Eixo Y":
                Titulo = "T_Eixo_Y"
            
            self.widgets_valores = {
                    self.ui.FCombB_Fonte_Titulo: self.Dicionario_Global["Titulos"][Titulo]["Fonte"],
                    self.ui.SB_Tamanho_Fonte_Titulo: self.Dicionario_Global["Titulos"][Titulo]["Tamanho_Fonte"],
                    self.ui.CB_Negrito_Titulo: self.Dicionario_Global["Titulos"][Titulo]["Negrito"],
                    self.ui.CB_Italico_Titulo: self.Dicionario_Global["Titulos"][Titulo]["Italico"],
                    self.ui.CombB_Cor_Fonte_Titulo: self.Dicionario_Global["Titulos"][Titulo]["Cor_Fonte"]
                }
            for widget, valor in self.widgets_valores.items():
                widget.blockSignals(True)
                
                if isinstance(widget, QtWidgets.QComboBox) or isinstance(widget, QtWidgets.QFontComboBox):
                    widget.setCurrentText(valor)
                    widget.blockSignals(False)
                    widget.currentTextChanged.emit(widget.currentText())

                elif isinstance(widget, QtWidgets.QSpinBox) or isinstance(widget, QtWidgets.QDoubleSpinBox):
                    widget.setValue(valor)
                    widget.blockSignals(False)
                    widget.valueChanged.emit(widget.value())

                elif isinstance(widget, QtWidgets.QCheckBox):
                    widget.setCheckState(Qt.CheckState.Checked if valor else Qt.CheckState.Unchecked)
                    widget.blockSignals(False)
                    widget.stateChanged.emit(1 if widget.checkState() == Qt.CheckState.Checked else 0)

        self.widgets_valores = {
            self.ui.CB_Ativar_Legendas: self.Dicionario_Global["Legendas"]["Ativar"],
            self.ui.Slider_Arredond_Caixa_Legenda: self.Dicionario_Global["Legendas"]["Caixa"]["Arredondamento"],
            self.ui.CombB_Cor_Fundo_Legenda: self.Dicionario_Global["Legendas"]["Caixa"]["Cor_Fundo"],
            self.ui.Slider_Transp_Caixa_Legenda: self.Dicionario_Global["Legendas"]["Caixa"]["Transparencia"],
            self.ui.CB_Ativar_Borda_Legenda: self.Dicionario_Global["Legendas"]["Borda"]["Ativar"],
            self.ui.CombB_Cor_Borda_Legenda: self.Dicionario_Global["Legendas"]["Borda"]["Cor"],
            self.ui.SB_Espessura_Borda_Legenda: self.Dicionario_Global["Legendas"]["Borda"]["Espessura"],
            self.ui.CombB_Localizacao_Legenda: self.Dicionario_Global["Legendas"]["Localizacao"],
            
            self.ui.CB_Ativar_Grade_Principal: self.Dicionario_Global["Grades"]["Principal"]["Ativar"],
            self.ui.CombB_Estilo_Linha_Grade_Principal: self.Dicionario_Estilos[self.Dicionario_Global["Grades"]["Principal"]["Estilo"]] if self.Dicionario_Global["Grades"]["Principal"]["Estilo"] in self.Dicionario_Estilos else self.Dicionario_Global["Grades"]["Principal"]["Estilo"],
            self.ui.SB_Espessura_Grade_Principal: self.Dicionario_Global["Grades"]["Principal"]["Espessura"],
            self.ui.Slider_Transp_Grade_Principal: self.Dicionario_Global["Grades"]["Principal"]["Transparencia"],
            self.ui.CombB_Cor_Grade_Principal: self.Dicionario_Global["Grades"]["Principal"]["Cor"],

            self.ui.CB_Ativar_Grade_Secundaria: self.Dicionario_Global["Grades"]["Secundaria"]["Ativar"],
            self.ui.CombB_Estilo_Linha_Grade_Secundaria: self.Dicionario_Estilos[self.Dicionario_Global["Grades"]["Secundaria"]["Estilo"]] if self.Dicionario_Global["Grades"]["Secundaria"]["Estilo"] in self.Dicionario_Estilos else self.Dicionario_Global["Grades"]["Secundaria"]["Estilo"],
            self.ui.SB_Espessura_Grade_Secundaria: self.Dicionario_Global["Grades"]["Secundaria"]["Espessura"],
            self.ui.Slider_Transp_Grade_Secundaria: self.Dicionario_Global["Grades"]["Secundaria"]["Transparencia"],
            self.ui.CombB_Cor_Grade_Secundaria: self.Dicionario_Global["Grades"]["Secundaria"]["Cor"],

            self.ui.CB_Ativar_Borda_Superior: self.Dicionario_Global["Bordas"]["Superior"]["Ativar"],
            self.ui.SB_Espessura_Borda_S: self.Dicionario_Global["Bordas"]["Superior"]["Espessura"],
            self.ui.CombB_Cor_Borda_S: self.Dicionario_Global["Bordas"]["Superior"]["Cor"],

            self.ui.CB_Ativar_Borda_Inferior: self.Dicionario_Global["Bordas"]["Inferior"]["Ativar"],
            self.ui.SB_Espessura_Borda_I: self.Dicionario_Global["Bordas"]["Inferior"]["Espessura"],
            self.ui.CombB_Cor_Borda_I: self.Dicionario_Global["Bordas"]["Inferior"]["Cor"],

            self.ui.CB_Ativar_Borda_Direita: self.Dicionario_Global["Bordas"]["Direita"]["Ativar"],
            self.ui.SB_Espessura_Borda_D: self.Dicionario_Global["Bordas"]["Direita"]["Espessura"],
            self.ui.CombB_Cor_Borda_D: self.Dicionario_Global["Bordas"]["Direita"]["Cor"],

            self.ui.CB_Ativar_Borda_Esquerda: self.Dicionario_Global["Bordas"]["Esquerda"]["Ativar"],
            self.ui.SB_Espessura_Borda_E: self.Dicionario_Global["Bordas"]["Esquerda"]["Espessura"],
            self.ui.CombB_Cor_Borda_E: self.Dicionario_Global["Bordas"]["Esquerda"]["Cor"]
        }
        self.parametro = 0
        self.Atualizar_Legendas_Predefinidas()
        self.parametro = 1

        for widget, valor in self.widgets_valores.items():
                widget.blockSignals(True)
                
                if isinstance(widget, QtWidgets.QComboBox) or isinstance(widget, QtWidgets.QFontComboBox):
                    widget.setCurrentText(valor)
                    widget.blockSignals(False)
                    widget.currentTextChanged.emit(widget.currentText())

                elif isinstance(widget, QtWidgets.QSpinBox) or isinstance(widget, QtWidgets.QDoubleSpinBox):
                    widget.setValue(valor)
                    widget.blockSignals(False)
                    widget.valueChanged.emit(widget.value())

                elif isinstance(widget, QtWidgets.QCheckBox):
                    widget.setCheckState(Qt.CheckState.Checked if valor else Qt.CheckState.Unchecked)
                    widget.blockSignals(False)
                    widget.stateChanged.emit(1 if widget.checkState() == Qt.CheckState.Checked else 0)

                elif isinstance(widget, QtWidgets.QSlider):
                    widget.setValue(valor)
                    widget.blockSignals(False)
                    widget.valueChanged.emit(widget.value())
        if self.Dicionario_Global["Legendas"]["Borda"]["Ativar"]:
            caixa = self.legenda.get_frame()
            caixa.set_linewidth(self.Dicionario_Global["Legendas"]["Borda"]["Espessura"]/10)

    def Verifica_Grafico(self):
        if self.ui.CB_Usar_Predefinicao.isChecked():
            self.Gerar_Grafico_Predef()
        else:
            self.Gerar_Grafico()

    def Atualizar_Legendas_Predefinidas(self):
        if self.parametro == 0:
            self.legenda = self.ax.legend()
            mapeamento_legenda = {}
            mapeamento_legenda = {t.get_text(): t for t in self.legenda.get_texts()}           

            if self.Dicionario_Global["Legendas"]["Seleção_individual"]:
                for Nome_Curva in self.Lista_Curvas_Plotadas:
                    if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"] in self.Fontes_Disponiveis:
                        valor = self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Fonte"]
                    else:
                        valor = "Arial"
                    mapeamento_legenda[Nome_Curva].set_fontfamily(valor)
                    mapeamento_legenda[Nome_Curva].set_fontsize(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Tamanho_Fonte"])
                    mapeamento_legenda[Nome_Curva].set_color(self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Cor_Fonte"])
                    if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Negrito"] == True:
                        mapeamento_legenda[Nome_Curva].set_fontweight('bold')
                    else:
                        mapeamento_legenda[Nome_Curva].set_fontweight('normal')
                    if self.Dicionario_Global["Curvas"][Nome_Curva]["Legenda"]["Italico"] == True:
                        mapeamento_legenda[Nome_Curva].set_fontstyle('italic')
                    else:
                        mapeamento_legenda[Nome_Curva].set_fontstyle('normal')                    
            else:
                for Nome_Curva2 in self.Lista_Curvas_Plotadas:
                    for Nome_Curva in self.Lista_Curvas_Plotadas:
                        if self.Dicionario_Global["Curvas"][Nome_Curva2]["Legenda"]["Fonte"] in self.Fontes_Disponiveis:
                            valor = self.Dicionario_Global["Curvas"][Nome_Curva2]["Legenda"]["Fonte"]
                        else:
                            valor = "Arial"
                        mapeamento_legenda[Nome_Curva].set_fontfamily(valor)
                        mapeamento_legenda[Nome_Curva].set_fontsize(self.Dicionario_Global["Curvas"][Nome_Curva2]["Legenda"]["Tamanho_Fonte"])
                        mapeamento_legenda[Nome_Curva].set_color(self.Dicionario_Global["Curvas"][Nome_Curva2]["Legenda"]["Cor_Fonte"])
                        if self.Dicionario_Global["Curvas"][Nome_Curva2]["Legenda"]["Negrito"] == True:
                            mapeamento_legenda[Nome_Curva2].set_fontweight('bold')
                        else:
                            mapeamento_legenda[Nome_Curva2].set_fontweight('normal')
                        if self.Dicionario_Global["Curvas"][Nome_Curva2]["Legenda"]["Italico"] == True:
                            mapeamento_legenda[Nome_Curva2].set_fontstyle('italic')
                        else:
                            mapeamento_legenda[Nome_Curva2].set_fontstyle('normal')
                    break
            
            caixa = self.legenda.get_frame()
            bbox_x, bbox_y = caixa.get_x(), caixa.get_y()
            bbox_width, bbox_height = caixa.get_width(), caixa.get_height()

            if self.Dicionario_Global["Legendas"]["Caixa"]["Arredondamento"] == 0:
                caixa.set_boxstyle("square")
            else:
                valor = self.Dicionario_Global["Legendas"]["Caixa"]["Arredondamento"]
                caixa.set_boxstyle(f"round,pad=0.1, rounding_size={valor / 20}")
            caixa.set_bounds(bbox_x, bbox_y, bbox_width, bbox_height)
            caixa.set_facecolor(self.Dicionario_Global["Legendas"]["Caixa"]["Cor_Fundo"])
            caixa.set_alpha(self.Dicionario_Global["Legendas"]["Caixa"]["Transparencia"] / 100)
            caixa.set_edgecolor(self.Dicionario_Global["Legendas"]["Borda"]["Cor"])
            caixa.set_linewidth(self.Dicionario_Global["Legendas"]["Borda"]["Espessura"]/10)
            if not self.Dicionario_Global["Legendas"]["Borda"]["Ativar"]:
                caixa.set_linewidth(0)
            valor = self.Dicionario_Locais[self.Dicionario_Global["Legendas"]["Localizacao"]]
            self.legenda.set_loc(valor)

            if self.Dicionario_Global["Legendas"]["Ativar"] == False:
                self.legenda.set_visible(False)

            self.canvas_P.draw_idle()
        
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

    def Atualiza_Dicionario_Global(self):
        for Nome_Curva in self.Lista_Curvas_Plotadas:
            Curva = self.Lista_Curvas_Plotadas[Nome_Curva]
            Cor_Atual = Curva.get_color()
            self.Dicionario_Global["Curvas"][Nome_Curva]["Cor"] = str(Cor_Atual)
            if self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Ativar"] == True:
                Marcador_Cor = Curva.get_markerfacecolor()
                self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Cor"] = str(Marcador_Cor)
                Marcador_Cor_Borda = Curva.get_markeredgecolor()
                self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Cor_Borda"] = str(Marcador_Cor_Borda)

    def Modo_Predefinição(self):
        if self.ui.CB_Usar_Predefinicao.isChecked():
            self.ui.CB_Visibilidade_Curva.setEnabled(False)
            self.ui.CombB_Cor_Curva.setEnabled(False)
            self.ui.B_CDialog_Cor_Curva.setEnabled(False)
            self.ui.SB_Espessura_Curva.setEnabled(False)
            self.ui.CombB_Estilo_Curva.setEnabled(False)
            self.ui.Slider_Transp_Curva.setEnabled(False)
            self.ui.CB_Ativar_Marcador.setEnabled(False)
            self.ui.CombB_Escolher_Marcador.setEnabled(False)
            self.ui.CombB_Cor_Marcador.setEnabled(False)
            self.ui.B_CDialog_Cor_Marcador.setEnabled(False)
            self.ui.SB_Espessura_Marcador.setEnabled(False)
            self.ui.FCombB_Fonte_Titulo.setEnabled(False)
            self.ui.SB_Tamanho_Fonte_Titulo.setEnabled(False)
            self.ui.CB_Negrito_Titulo.setEnabled(False)
            self.ui.CB_Italico_Titulo.setEnabled(False)
            self.ui.CombB_Cor_Fonte_Titulo.setEnabled(False)
            self.ui.B_CDialog_Cor_Fonte_Titulo.setEnabled(False)
            self.ui.CB_Ativar_Legendas.setEnabled(False)
            self.ui.CB_Alteracao_Individual_Legenda.setEnabled(False)
            self.ui.FCombB_Fonte_Legenda.setEnabled(False)
            self.ui.SB_Tamanho_Fonte_Legenda.setEnabled(False)
            self.ui.CombB_Cor_Fonte_Legenda.setEnabled(False)
            self.ui.pushButton_9.setEnabled(False)
            self.ui.CB_Negrito_Legenda.setEnabled(False)
            self.ui.CB_Italico_Legenda.setEnabled(False)
            self.ui.CombB_Localizacao_Legenda.setEnabled(False)
            self.ui.Slider_Arredond_Caixa_Legenda.setEnabled(False)
            self.ui.CombB_Cor_Fundo_Legenda.setEnabled(False)
            self.ui.B_CDialog_Cor_Fundo_Legenda.setEnabled(False)
            self.ui.Slider_Transp_Caixa_Legenda.setEnabled(False)
            self.ui.CB_Ativar_Borda_Legenda.setEnabled(False)
            self.ui.CombB_Cor_Borda_Legenda.setEnabled(False)
            self.ui.B_CDialog_Cor_Borda_Legenda.setEnabled(False)
            self.ui.SB_Espessura_Borda_Legenda.setEnabled(False)
            self.ui.CB_Ativar_Grade_Principal.setEnabled(False)
            self.ui.CombB_Estilo_Linha_Grade_Principal.setEnabled(False)
            self.ui.SB_Espessura_Grade_Principal.setEnabled(False)
            self.ui.Slider_Transp_Grade_Principal.setEnabled(False)
            self.ui.CombB_Cor_Grade_Principal.setEnabled(False)
            self.ui.B_CDialog_Cor_Grade_Principal.setEnabled(False)
            self.ui.CB_Ativar_Grade_Secundaria.setEnabled(False)
            self.ui.CombB_Estilo_Linha_Grade_Secundaria.setEnabled(False)
            self.ui.SB_Espessura_Grade_Secundaria.setEnabled(False)
            self.ui.Slider_Transp_Grade_Secundaria.setEnabled(False)
            self.ui.CombB_Cor_Grade_Secundaria.setEnabled(False)
            self.ui.B_CDialog_Cor_Grade_Secundaria.setEnabled(False)
            self.ui.CB_Ativar_Borda_Superior.setEnabled(False)
            self.ui.SB_Espessura_Borda_S.setEnabled(False)
            self.ui.CombB_Cor_Borda_S.setEnabled(False)
            self.ui.B_CDialog_Borda_S.setEnabled(False)
            self.ui.CB_Ativar_Borda_Inferior.setEnabled(False)
            self.ui.SB_Espessura_Borda_I.setEnabled(False)
            self.ui.CombB_Cor_Borda_I.setEnabled(False)
            self.ui.B_CDialog_Borda_I.setEnabled(False)
            self.ui.CB_Ativar_Borda_Direita.setEnabled(False)
            self.ui.SB_Espessura_Borda_D.setEnabled(False)
            self.ui.CombB_Cor_Borda_D.setEnabled(False)
            self.ui.B_CDialog_Borda_D.setEnabled(False)
            self.ui.CB_Ativar_Borda_Esquerda.setEnabled(False)
            self.ui.SB_Espessura_Borda_E.setEnabled(False)
            self.ui.CombB_Cor_Borda_E.setEnabled(False)
            self.ui.B_CDialog_Borda_E.setEnabled(False)

            self.ui.CB_Visibilidade_Curva.blockSignals(True)
            self.ui.CombB_Cor_Curva.blockSignals(True)
            self.ui.B_CDialog_Cor_Curva.blockSignals(True)
            self.ui.SB_Espessura_Curva.blockSignals(True)
            self.ui.CombB_Estilo_Curva.blockSignals(True)
            self.ui.Slider_Transp_Curva.blockSignals(True)
            self.ui.CB_Ativar_Marcador.blockSignals(True)
            self.ui.CombB_Escolher_Marcador.blockSignals(True)
            self.ui.CombB_Cor_Marcador.blockSignals(True)
            self.ui.B_CDialog_Cor_Marcador.blockSignals(True)
            self.ui.SB_Espessura_Marcador.blockSignals(True)
            self.ui.FCombB_Fonte_Titulo.blockSignals(True)
            self.ui.SB_Tamanho_Fonte_Titulo.blockSignals(True)
            self.ui.CB_Negrito_Titulo.blockSignals(True)
            self.ui.CB_Italico_Titulo.blockSignals(True)
            self.ui.CombB_Cor_Fonte_Titulo.blockSignals(True)
            self.ui.B_CDialog_Cor_Fonte_Titulo.blockSignals(True)
            self.ui.CB_Ativar_Legendas.blockSignals(True)
            self.ui.CB_Alteracao_Individual_Legenda.blockSignals(True)
            self.ui.FCombB_Fonte_Legenda.blockSignals(True)
            self.ui.SB_Tamanho_Fonte_Legenda.blockSignals(True)
            self.ui.CombB_Cor_Fonte_Legenda.blockSignals(True)
            self.ui.pushButton_9.blockSignals(True)
            self.ui.CB_Negrito_Legenda.blockSignals(True)
            self.ui.CB_Italico_Legenda.blockSignals(True)
            self.ui.CombB_Localizacao_Legenda.blockSignals(True)
            self.ui.Slider_Arredond_Caixa_Legenda.blockSignals(True)
            self.ui.CombB_Cor_Fundo_Legenda.blockSignals(True)
            self.ui.B_CDialog_Cor_Fundo_Legenda.blockSignals(True)
            self.ui.Slider_Transp_Caixa_Legenda.blockSignals(True)
            self.ui.CB_Ativar_Borda_Legenda.blockSignals(True)
            self.ui.CombB_Cor_Borda_Legenda.blockSignals(True)
            self.ui.B_CDialog_Cor_Borda_Legenda.blockSignals(True)
            self.ui.SB_Espessura_Borda_Legenda.blockSignals(True)
            self.ui.CB_Ativar_Grade_Principal.blockSignals(True)
            self.ui.CombB_Estilo_Linha_Grade_Principal.blockSignals(True)
            self.ui.SB_Espessura_Grade_Principal.blockSignals(True)
            self.ui.Slider_Transp_Grade_Principal.blockSignals(True)
            self.ui.CombB_Cor_Grade_Principal.blockSignals(True)
            self.ui.B_CDialog_Cor_Grade_Principal.blockSignals(True)
            self.ui.CB_Ativar_Grade_Secundaria.blockSignals(True)
            self.ui.CombB_Estilo_Linha_Grade_Secundaria.blockSignals(True)
            self.ui.SB_Espessura_Grade_Secundaria.blockSignals(True)
            self.ui.Slider_Transp_Grade_Secundaria.blockSignals(True)
            self.ui.CombB_Cor_Grade_Secundaria.blockSignals(True)
            self.ui.B_CDialog_Cor_Grade_Secundaria.blockSignals(True)
            self.ui.CB_Ativar_Borda_Superior.blockSignals(True)
            self.ui.SB_Espessura_Borda_S.blockSignals(True)
            self.ui.CombB_Cor_Borda_S.blockSignals(True)
            self.ui.B_CDialog_Borda_S.blockSignals(True)
            self.ui.CB_Ativar_Borda_Inferior.blockSignals(True)
            self.ui.SB_Espessura_Borda_I.blockSignals(True)
            self.ui.CombB_Cor_Borda_I.blockSignals(True)
            self.ui.B_CDialog_Borda_I.blockSignals(True)
            self.ui.CB_Ativar_Borda_Direita.blockSignals(True)
            self.ui.SB_Espessura_Borda_D.blockSignals(True)
            self.ui.CombB_Cor_Borda_D.blockSignals(True)
            self.ui.B_CDialog_Borda_D.blockSignals(True)
            self.ui.CB_Ativar_Borda_Esquerda.blockSignals(True)
            self.ui.SB_Espessura_Borda_E.blockSignals(True)
            self.ui.CombB_Cor_Borda_E.blockSignals(True)
            self.ui.B_CDialog_Borda_E.blockSignals(True)
        else:
            self.ui.CB_Visibilidade_Curva.setEnabled(True)
            self.ui.CombB_Cor_Curva.setEnabled(True)
            self.ui.B_CDialog_Cor_Curva.setEnabled(True)
            self.ui.SB_Espessura_Curva.setEnabled(True)
            self.ui.CombB_Estilo_Curva.setEnabled(True)
            self.ui.Slider_Transp_Curva.setEnabled(True)
            self.ui.CB_Ativar_Marcador.setEnabled(True)
            self.ui.CombB_Escolher_Marcador.setEnabled(True)
            self.ui.CombB_Cor_Marcador.setEnabled(True)
            self.ui.B_CDialog_Cor_Marcador.setEnabled(True)
            self.ui.SB_Espessura_Marcador.setEnabled(True)
            self.ui.FCombB_Fonte_Titulo.setEnabled(True)
            self.ui.SB_Tamanho_Fonte_Titulo.setEnabled(True)
            self.ui.CB_Negrito_Titulo.setEnabled(True)
            self.ui.CB_Italico_Titulo.setEnabled(True)
            self.ui.CombB_Cor_Fonte_Titulo.setEnabled(True)
            self.ui.B_CDialog_Cor_Fonte_Titulo.setEnabled(True)
            self.ui.CB_Ativar_Legendas.setEnabled(True)
            self.ui.CB_Alteracao_Individual_Legenda.setEnabled(True)
            self.ui.FCombB_Fonte_Legenda.setEnabled(True)
            self.ui.SB_Tamanho_Fonte_Legenda.setEnabled(True)
            self.ui.CombB_Cor_Fonte_Legenda.setEnabled(True)
            self.ui.pushButton_9.setEnabled(True)
            self.ui.CB_Negrito_Legenda.setEnabled(True)
            self.ui.CB_Italico_Legenda.setEnabled(True)
            self.ui.CombB_Localizacao_Legenda.setEnabled(True)
            self.ui.Slider_Arredond_Caixa_Legenda.setEnabled(True)
            self.ui.CombB_Cor_Fundo_Legenda.setEnabled(True)
            self.ui.B_CDialog_Cor_Fundo_Legenda.setEnabled(True)
            self.ui.Slider_Transp_Caixa_Legenda.setEnabled(True)
            self.ui.CB_Ativar_Borda_Legenda.setEnabled(True)
            self.ui.CombB_Cor_Borda_Legenda.setEnabled(True)
            self.ui.B_CDialog_Cor_Borda_Legenda.setEnabled(True)
            self.ui.SB_Espessura_Borda_Legenda.setEnabled(True)
            self.ui.CB_Ativar_Grade_Principal.setEnabled(True)
            self.ui.CombB_Estilo_Linha_Grade_Principal.setEnabled(True)
            self.ui.SB_Espessura_Grade_Principal.setEnabled(True)
            self.ui.Slider_Transp_Grade_Principal.setEnabled(True)
            self.ui.CombB_Cor_Grade_Principal.setEnabled(True)
            self.ui.B_CDialog_Cor_Grade_Principal.setEnabled(True)
            self.ui.CB_Ativar_Grade_Secundaria.setEnabled(True)
            self.ui.CombB_Estilo_Linha_Grade_Secundaria.setEnabled(True)
            self.ui.SB_Espessura_Grade_Secundaria.setEnabled(True)
            self.ui.Slider_Transp_Grade_Secundaria.setEnabled(True)
            self.ui.CombB_Cor_Grade_Secundaria.setEnabled(True)
            self.ui.B_CDialog_Cor_Grade_Secundaria.setEnabled(True)
            self.ui.CB_Ativar_Borda_Superior.setEnabled(True)
            self.ui.SB_Espessura_Borda_S.setEnabled(True)
            self.ui.CombB_Cor_Borda_S.setEnabled(True)
            self.ui.B_CDialog_Borda_S.setEnabled(True)
            self.ui.CB_Ativar_Borda_Inferior.setEnabled(True)
            self.ui.SB_Espessura_Borda_I.setEnabled(True)
            self.ui.CombB_Cor_Borda_I.setEnabled(True)
            self.ui.B_CDialog_Borda_I.setEnabled(True)
            self.ui.CB_Ativar_Borda_Direita.setEnabled(True)
            self.ui.SB_Espessura_Borda_D.setEnabled(True)
            self.ui.CombB_Cor_Borda_D.setEnabled(True)
            self.ui.B_CDialog_Borda_D.setEnabled(True)
            self.ui.CB_Ativar_Borda_Esquerda.setEnabled(True)
            self.ui.SB_Espessura_Borda_E.setEnabled(True)
            self.ui.CombB_Cor_Borda_E.setEnabled(True)
            self.ui.B_CDialog_Borda_E.setEnabled(True)

            self.ui.CB_Visibilidade_Curva.blockSignals(False)
            self.ui.CombB_Cor_Curva.blockSignals(False)
            self.ui.B_CDialog_Cor_Curva.blockSignals(False)
            self.ui.SB_Espessura_Curva.blockSignals(False)
            self.ui.CombB_Estilo_Curva.blockSignals(False)
            self.ui.Slider_Transp_Curva.blockSignals(False)
            self.ui.CB_Ativar_Marcador.blockSignals(False)
            self.ui.CombB_Escolher_Marcador.blockSignals(False)
            self.ui.CombB_Cor_Marcador.blockSignals(False)
            self.ui.B_CDialog_Cor_Marcador.blockSignals(False)
            self.ui.SB_Espessura_Marcador.blockSignals(False)
            self.ui.FCombB_Fonte_Titulo.blockSignals(False)
            self.ui.SB_Tamanho_Fonte_Titulo.blockSignals(False)
            self.ui.CB_Negrito_Titulo.blockSignals(False)
            self.ui.CB_Italico_Titulo.blockSignals(False)
            self.ui.CombB_Cor_Fonte_Titulo.blockSignals(False)
            self.ui.B_CDialog_Cor_Fonte_Titulo.blockSignals(False)
            self.ui.CB_Ativar_Legendas.blockSignals(False)
            self.ui.CB_Alteracao_Individual_Legenda.blockSignals(False)
            self.ui.FCombB_Fonte_Legenda.blockSignals(False)
            self.ui.SB_Tamanho_Fonte_Legenda.blockSignals(False)
            self.ui.CombB_Cor_Fonte_Legenda.blockSignals(False)
            self.ui.pushButton_9.blockSignals(False)
            self.ui.CB_Negrito_Legenda.blockSignals(False)
            self.ui.CB_Italico_Legenda.blockSignals(False)
            self.ui.CombB_Localizacao_Legenda.blockSignals(False)
            self.ui.Slider_Arredond_Caixa_Legenda.blockSignals(False)
            self.ui.CombB_Cor_Fundo_Legenda.blockSignals(False)
            self.ui.B_CDialog_Cor_Fundo_Legenda.blockSignals(False)
            self.ui.Slider_Transp_Caixa_Legenda.blockSignals(False)
            self.ui.CB_Ativar_Borda_Legenda.blockSignals(False)
            self.ui.CombB_Cor_Borda_Legenda.blockSignals(False)
            self.ui.B_CDialog_Cor_Borda_Legenda.blockSignals(False)
            self.ui.SB_Espessura_Borda_Legenda.blockSignals(False)
            self.ui.CB_Ativar_Grade_Principal.blockSignals(False)
            self.ui.CombB_Estilo_Linha_Grade_Principal.blockSignals(False)
            self.ui.SB_Espessura_Grade_Principal.blockSignals(False)
            self.ui.Slider_Transp_Grade_Principal.blockSignals(False)
            self.ui.CombB_Cor_Grade_Principal.blockSignals(False)
            self.ui.B_CDialog_Cor_Grade_Principal.blockSignals(False)
            self.ui.CB_Ativar_Grade_Secundaria.blockSignals(False)
            self.ui.CombB_Estilo_Linha_Grade_Secundaria.blockSignals(False)
            self.ui.SB_Espessura_Grade_Secundaria.blockSignals(False)
            self.ui.Slider_Transp_Grade_Secundaria.blockSignals(False)
            self.ui.CombB_Cor_Grade_Secundaria.blockSignals(False)
            self.ui.B_CDialog_Cor_Grade_Secundaria.blockSignals(False)
            self.ui.CB_Ativar_Borda_Superior.blockSignals(False)
            self.ui.SB_Espessura_Borda_S.blockSignals(False)
            self.ui.CombB_Cor_Borda_S.blockSignals(False)
            self.ui.B_CDialog_Borda_S.blockSignals(False)
            self.ui.CB_Ativar_Borda_Inferior.blockSignals(False)
            self.ui.SB_Espessura_Borda_I.blockSignals(False)
            self.ui.CombB_Cor_Borda_I.blockSignals(False)
            self.ui.B_CDialog_Borda_I.blockSignals(False)
            self.ui.CB_Ativar_Borda_Direita.blockSignals(False)
            self.ui.SB_Espessura_Borda_D.blockSignals(False)
            self.ui.CombB_Cor_Borda_D.blockSignals(False)
            self.ui.B_CDialog_Borda_D.blockSignals(False)
            self.ui.CB_Ativar_Borda_Esquerda.blockSignals(False)
            self.ui.SB_Espessura_Borda_E.blockSignals(False)
            self.ui.CombB_Cor_Borda_E.blockSignals(False)
            self.ui.B_CDialog_Borda_E.blockSignals(False)

    def Inicia_Timer(self, duracao):
        if self.ui.CB_Usar_Predefinicao.isChecked():
            self.timer.start(duracao)
        else:
            return

    def Restaura_Mensagem_Fixa(self):
        self.ui.statusbar.showMessage("A interface está no modo de predefinição. Não é possível personalizar o gráfico neste modo.")

    def Salvar_Predefinicao(self):
        resposta = QMessageBox.question(self.interface, "Aviso", "Os índices das curvas serão usados ao aplicar esta predefinição. Eles estão configurados corretamente?")
        if resposta == QtWidgets.QMessageBox.StandardButton.Yes:
            self.Dicionario_Global["Indices"] = {}

            for Nome_Curva in self.Lista_Curvas_Plotadas:
                for Curva in self.Curvas:
                    if Nome_Curva == Curva.Box_Modelo.title():
                        self.Dicionario_Global["Indices"][Nome_Curva] = Curva.CombB_Indice_Curva.currentText()
            self.Atualiza_Dicionario_Global()
            
            try:
                if getattr(sys, 'frozen', False):
                    Caminho_Base = os.path.dirname(sys.executable)
                else:
                    Caminho_Base = os.path.dirname(os.path.abspath(__file__))
                diretorio_script = Caminho_Base + "\\Predefinicoes\\"
                caminho_json = os.path.join(diretorio_script, self.ui.LE_Nome_Predefinicao_Salvar.text() + ".json")
                with open(caminho_json, "w", encoding="utf-8") as arquivo:
                    arquivo
                    json.dump(self.Dicionario_Global, arquivo, indent=4, ensure_ascii=False)
                
                self.Atualiza_Lista_Predefinicoes()
                self.ui.statusbar.showMessage(f"Predefinição salva com sucesso!", 3000)
                self.Inicia_Timer(3000)
            except Exception as e:
                QMessageBox(self.interface, "Erro", f"Erro ao tentar salvar predefinição: {e}")
        else:
            return

    def Atualiza_Lista_Predefinicoes(self):
        if getattr(sys, 'frozen', False):
            Caminho_Base = os.path.dirname(sys.executable)
        else:
            Caminho_Base = os.path.dirname(os.path.abspath(__file__))

        Caminho_Pasta = os.path.join(Caminho_Base, "Predefinicoes")

        os.makedirs(Caminho_Pasta, exist_ok=True)

        arquivos_json = [f for f in os.listdir(Caminho_Pasta) if f.endswith(".json")]
        Predefinicoes_na_Lista = [self.ui.CombB_Predifinicoes_Disponiveis.itemText(i) for i in range(self.ui.CombB_Predifinicoes_Disponiveis.count())]
        for arquivo in arquivos_json:
            if arquivo not in Predefinicoes_na_Lista:
                self.ui.CombB_Predifinicoes_Disponiveis.addItem(arquivo)

    def Atualiza_Predefinicao_Geral(self):
        if self.ui.CB_Usar_Predefinicao.isChecked():
            resposta = QMessageBox.question(self.interface, "Confirmação", "Ao utilizar nova predefinição, todas as configurações atuais serão perdidas. Deseja continuar?")
            if resposta == QtWidgets.QMessageBox.StandardButton.Yes:
                try:
                    if getattr(sys, 'frozen', False):
                        Caminho_Base = os.path.dirname(sys.executable)
                    else:
                        Caminho_Base = os.path.dirname(os.path.abspath(__file__))


                    Caminho_Pasta = os.path.join(Caminho_Base, "Predefinicoes")

                    os.makedirs(Caminho_Pasta, exist_ok=True)
                    Arquivo_json = self.ui.CombB_Predifinicoes_Disponiveis.currentText()
                    Caminho_Completo = os.path.join(Caminho_Pasta, Arquivo_json)
                    with open(Caminho_Completo, "r", encoding="utf-8") as arquivo:
                        self.Dicionario_Global = json.load(arquivo)
                except Exception as e:
                    QMessageBox.critical(self.interface, "Erro", f"Erro ao carregar predefinição: {e}")
                    self.ui.CB_Usar_Predefinicao.setCheckState(Qt.CheckState(0))
                    return
                self.Lista_Curvas_Predef = self.Dicionario_Global["Curvas"]
                self.Dicionario_Global["Curvas"] = {}
                if self.Dicionario_Global["Legendas"]["Seleção_individual"] == True:
                    self.ui.CB_Alteracao_Individual_Legenda.setCheckState(Qt.CheckState.Checked)
                self.Modo_Predefinição()
                self.ui.statusbar.showMessage("A interface está no modo de predefinição. Não é possível personalizar o gráfico neste modo.")
                return
            else:
                self.ui.CB_Usar_Predefinicao.setCheckState(Qt.CheckState.Unchecked)
                return
        else:
            self.Modo_Predefinição()
            self.ui.statusbar.clearMessage()
            return

    def Atualizar_Indices_Disponiveis(self):
        if getattr(sys, 'frozen', False):
            Caminho_Base = os.path.dirname(sys.executable)
        else:
            Caminho_Base = os.path.dirname(os.path.abspath(__file__))

        Caminho_Pasta = os.path.join(Caminho_Base, "Predefinicoes")

        os.makedirs(Caminho_Pasta, exist_ok=True)        
        Arquivo_json = self.ui.CombB_Predifinicoes_Disponiveis.currentText()
        if Arquivo_json == "":
            return
        Caminho_Completo = os.path.join(Caminho_Pasta, Arquivo_json)
        try:
            with open(Caminho_Completo, "r", encoding="utf-8") as arquivo:
                Dicionario_Intermediario = json.load(arquivo)
            for Curva in self.Curvas:
                Indice_Atual = Curva.CombB_Indice_Curva.currentText()
                Curva.CombB_Indice_Curva.clear()
                for Indice in Dicionario_Intermediario["Indices"].values():
                    Curva.CombB_Indice_Curva.addItem(Indice)
                Curva.CombB_Indice_Curva.setCurrentText(Indice_Atual)
        except Exception as e:
            QMessageBox.critical(self.interface, "Erro", f"Erro ao verificar os índices da predefinição {Arquivo_json}: {e}")

    def Atualiza_Configuracoes_Curva(self, Curva):
        if Curva.CombB_Indice_Curva.currentText() in self.Dicionario_Global["Indices"].values() and Curva.CB_Ativar_Curva.isChecked():
            Indice_Desejado = Curva.CombB_Indice_Curva.currentText()
            Nome_Curva = next((curva for curva, indice in self.Dicionario_Global["Indices"].items() if indice == Indice_Desejado), None)
            self.Dicionario_Global["Curvas"][Curva.Box_Modelo.title()] = self.Lista_Curvas_Predef[Nome_Curva]
            self.Dicionario_Global["Curvas"][Curva.Box_Modelo.title()]["Legenda"]["Texto"] = Curva.Box_Modelo.title()

    def Atualizar_Curvas_Predefinidas(self, Nome_Curva):
        self.ui.CombB_Selecionar_Curva.setCurrentText(Nome_Curva)
        self.ui.CombB_Cor_Curva.setCurrentText("Preto")
        self.ui.CombB_Cor_Curva.setCurrentText(self.Dicionario_Global["Curvas"][Nome_Curva]["Cor"])

        self.ui.SB_Espessura_Curva.setValue(self.Dicionario_Global["Curvas"][Nome_Curva]["Espessura"] - 1)
        self.ui.SB_Espessura_Curva.setValue(self.Dicionario_Global["Curvas"][Nome_Curva]["Espessura"])

        self.ui.CombB_Estilo_Curva.setCurrentText("-")
        self.ui.CombB_Estilo_Curva.setCurrentText(self.Dicionario_Global["Curvas"][Nome_Curva]["Estilo"])

        self.ui.Slider_Transp_Curva.setValue(self.Dicionario_Global["Curvas"][Nome_Curva]["Transparencia"]-1)
        self.ui.Slider_Transp_Curva.setValue(self.Dicionario_Global["Curvas"][Nome_Curva]["Transparencia"])

        self.ui.CB_Ativar_Marcador.setChecked(not self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Ativar"])
        self.ui.CB_Ativar_Marcador.setChecked(self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Ativar"])

        self.ui.CombB_Escolher_Marcador.setCurrentText("o")
        self.ui.CombB_Escolher_Marcador.setCurrentText(self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador"])

        self.ui.CombB_Cor_Marcador.setCurrentText("Preto")
        self.ui.CombB_Cor_Marcador.setCurrentText(self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Cor"])

        self.ui.CombB_Cor_Borda_Marcador.setCurrentText("Preto")
        self.ui.CombB_Cor_Borda_Marcador.setCurrentText(self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Cor_Borda"])
        
        self.ui.SB_Espessura_Marcador.setValue(self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Espessura"]-1)
        self.ui.SB_Espessura_Marcador.setValue(self.Dicionario_Global["Curvas"][Nome_Curva]["Marcador_Espessura"])
      
    def Exportar_Grafico(self):
        caminho_arquivo, _ = QFileDialog.getSaveFileName(None, "Salvar Gráfico", "", "PNG (*.png);;JPEG (*.jpg);;PDF (*.pdf);;SVG (*.svg);;EPS (*.eps);;Todos os arquivos (*.*)")
        if caminho_arquivo:
            self.fig.savefig(caminho_arquivo)
            self.ui.statusbar.showMessage("Gráfico exportado com sucesso!", 3000)
            self.Inicia_Timer(3000)     
    
    def Copia_Grafico(self):
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png')
        buf.seek(0)

        QIm = QImage.fromData(buf.getvalue())
        pixmap = QPixmap.fromImage(QIm)
        
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(pixmap)

        self.ui.statusbar.showMessage("Gráfico copiado com sucesso!", 3000)
        self.Inicia_Timer(3000)
    
    def Excluir_Predefinicao(self):
        Nome_Predef = self.ui.CombB_Predifinicoes_Disponiveis.currentText()
        resposta = QMessageBox.question(self.interface, "Aviso", f"Deseja excluír a predefinição {Nome_Predef}")
        if resposta == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                Nome_Predef = Nome_Predef
                if getattr(sys, 'frozen', False):
                    Caminho_Base = os.path.dirname(sys.executable)
                else:
                    Caminho_Base = os.path.dirname(os.path.abspath(__file__))
                Caminho_Pasta = os.path.join(Caminho_Base, "Predefinicoes")
                Caminho_Predefinicao = os.path.join(Caminho_Pasta, Nome_Predef)
                if os.path.exists(Caminho_Predefinicao):
                    os.remove(Caminho_Predefinicao)
                self.ui.CombB_Predifinicoes_Disponiveis.clear()
                self.Atualiza_Lista_Predefinicoes()
                self.ui.statusbar.showMessage("Predefinição excluída com sucesso!", 3000)
                self.Inicia_Timer(3000)
            except Exception as e:
                QMessageBox.critical(self.interface, "Erro", f"Erro tentar excluír a predefinição.")
                return
        else:
            return

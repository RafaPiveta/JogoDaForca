# Projeto de CSBA
# Professora: Maria Angela Roveredo
# Alunos: Beatriz Sousa, Francisco Bley Ruthes, Rafael Olivare Piveta e Stefan Rodrigues

#-----------------------------------------------------------------------
# IMPORTS
#-----------------------------------------------------------------------

import os
os.environ ['KIVY_AUDIO'] = 'sdl2'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.image import Image
import random

#-----------------------------------------------------------------------
# CRIAÇÃO DA INTERFACE GRÁFICA NO PYTHON
#-----------------------------------------------------------------------

class Quadro(BoxLayout):
    #Imagens
    imagemForca = StringProperty("Forca.png")
    fundo_preto = StringProperty("Fundo Preto.png")

    #Iniciação do Jogo
    def __init__ (self, *args, **dic):
        super().__init__(*args, **dic)
        Window.size = (800,800)
        banco_de_palavras = ["cachorro","gato","flamengo","CaDeIRA","uvA","ÉpiCo","índice","motorista","político","faca","garfo","pão","brasil","espectativa",
                            "pêndulo","arma","coração","amor","dúvida","kiwi","xícara","longe","ozônio","térmico","mesa","goleiro","fábrica","pneumonia",
                            "neologismo","física","programação","computador","código","estábulo","caminhão","penalidade","concerteza","imperatriz","zoológico",
                            "nariz","papo","língua","produção","mosquito","histórico","navegador","imaginação","bagunça","novidade","cabeçalho","qualidade","animação"]
        l = random.choice(banco_de_palavras)
        palavra_aleatoria = l.lower()
        self.descobrir = [" _ "] * len(palavra_aleatoria)
        self.lista_palavra_aleatoria = []
        self.letras_já_selecionadas = []
        self.letras_já_selecionadas_corretas = []
        self.letras_já_selecionadas_incorretas = []
        self.lista_alfabeto = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        for l in palavra_aleatoria:
            self.lista_palavra_aleatoria.append(l)

        self.somVitoria = SoundLoader.load('vitoria.wav')
        self.somDerrota = SoundLoader.load('derrota.wav')
        self.tentativas = 6
        self.ids.tentativas.text = str(self.tentativas)
        self.ids.palavra_aleatoria.text = ' '.join(self.descobrir)
        self.popup_vitoria = "PARABÉNS, VOCÊ VENCEU \n    Aperte ESC para fechar"
        self.popup_derrota = "        VOCÊ PERDEU\n A palavra era: {}\n Aperte ESC para fechar".format(palavra_aleatoria)

        self.recomecaJogo()

    #-----------------------------------------------------------------------
    # CRIAÇÃO DAS FUNÇÕES
    #-----------------------------------------------------------------------

    def acentuacao(self,lista):

        lista_sem_acentuacao = []

        for elemento in lista:
            if elemento == 'á' or elemento == 'ã' or elemento == 'à':
                elemento = 'a'
            elif elemento == 'é' or elemento == 'ê':
                elemento = 'e'
            elif elemento == 'í':
                elemento = 'i'
            elif elemento == 'ó' or elemento == 'ô' or elemento == 'õ':
                elemento = 'o'
            elif elemento == 'ú':
                elemento = 'u'
            elif elemento == 'ç':
                elemento = 'c'

            lista_sem_acentuacao.append(elemento)

        return lista_sem_acentuacao


    def confirmaLetra(self):
        chute_usuario_qualquer_tamanho = self.ids.letra.text
        chute_usuario = chute_usuario_qualquer_tamanho.lower()
        v = self.acentuacao(self.lista_palavra_aleatoria)

        #Verifica se o usuário digitou algum acento
        if chute_usuario == 'á' or chute_usuario == 'ã' or chute_usuario == 'à':
            chute_usuario = 'a'
        elif chute_usuario == 'é' or chute_usuario == 'ê':
            chute_usuario = 'e'
        elif chute_usuario == 'í':
            chute_usuario = 'i'
        elif chute_usuario == 'ó' or chute_usuario == 'ô' or chute_usuario == 'õ':
            chute_usuario = 'o'
        elif chute_usuario == 'ú':
            chute_usuario = 'u'
        elif chute_usuario == 'ç':
            chute_usuario = 'c'
        
        #Verifica se o chute do usuário é apenas UMA LETRA 
        if chute_usuario not in self.lista_alfabeto:
            self.ids.letras_selecionadas.text = "Digite apenas UMA LETRA"
            self.ids.letra.text = ""

        else:
            if len(chute_usuario) == 1:
                #Verifica se o usuário já digitou essa letra
                for letras_escolhidas in self.letras_já_selecionadas:
                    if chute_usuario == letras_escolhidas:
                        self.ids.letras_selecionadas.text = "A letra \"{}\" já foi".format(self.ids.letra.text)
                        self.ids.letra.text = ""

                for i in range(0,len(self.lista_palavra_aleatoria)):
                    if chute_usuario == v[i]:
                        self.descobrir[i] = self.lista_palavra_aleatoria[i]
                        if chute_usuario not in self.letras_já_selecionadas:
                            self.letras_já_selecionadas.append(chute_usuario)
                            self.ids.letras_selecionadas.text = 'Letras já selecionadas: ' + ', '.join(self.letras_já_selecionadas)
                            self.ids.letra.text = ""

                        #PopUp de Vitória
                        if self.descobrir.count(" _ ") == 0:
                            popup = ModalView(size_hint=(0.85,0.5))
                            labelResultado = Label(text = self.popup_vitoria, font_size = 40)
                            popup.add_widget(labelResultado)
                            popup.open()
                            popup.background_color = "green"
                            self.somVitoria.play()

                    else:
                        if chute_usuario not in self.letras_já_selecionadas:
                            self.letras_já_selecionadas.append(chute_usuario)
                            self.ids.letras_selecionadas.text = 'Letras já selecionadas: ' + ', '.join(self.letras_já_selecionadas)
                            self.ids.letra.text = ""
                            #Diminui as tentativas
                            if chute_usuario not in v:
                                self.tentativas -= 1
                                self.ids.tentativas.text = str(self.tentativas)
                                self.mudaimagem()

                                #PopUp de Derrota
                                if self.tentativas == 0:
                                    popup = ModalView(size_hint=(0.75,0.5))
                                    labelResultado = Label(text = self.popup_derrota, font_size = 40)
                                    popup.add_widget(labelResultado)
                                    popup.open()
                                    popup.background_color = "red"
                                    self.somDerrota.play()
                                    self.ids.imagem.source = "Perna Esquerda.png"
            
            self.ids.palavra_aleatoria.text = ' '.join(self.descobrir)
    
    #Finaliza o jogo
    def sair(self):
        App.get_running_app().stop()

    #Desativa o som
    def desativaSom(self):
        desliga = self.ids.desativaAudio.text
        if desliga == "OFF":
            self.somVitoria.volume = 0
            self.somDerrota.volume = 0
        else:
            self.somVitoria.volume = 1
            self.somDerrota.volume = 1

    #Recomeça tudo
    def recomecaJogo(self):
        banco_de_palavras = ["cachorro","gato","flamengo","CaDeIRA","uvA","ÉpiCo","índice","motorista","político","faca","garfo","pão","brasil","pêndulo","arma","coração","amor","dúvida","kiwi","xícara","longe","ozônio","térmico","mesa","goleiro","fábrica","pneumonia","neologismo","física","programação","computador","código","estábulo"]
        self.tentativas = 6
        self.ids.tentativas.text = str(self.tentativas)
        self.letras_já_selecionadas.clear()
        self.lista_palavra_aleatoria.clear()
        l = random.choice(banco_de_palavras)
        palavra_aleatoria = l.lower()
        self.descobrir = [" _ "] * len(palavra_aleatoria)
        self.ids.palavra_aleatoria.text = ' '.join(self.descobrir)
        self.ids.letras_selecionadas.text = ''
        self.ids.letra.text = ''
        self.lista_alfabeto = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

        for l in palavra_aleatoria:
            self.lista_palavra_aleatoria.append(l)

        self.popup_vitoria = "PARABÉNS, VOCÊ VENCEU \n    Aperte ESC para fechar"
        self.popup_derrota = "        VOCÊ PERDEU\n A palavra era: {}\n Aperte ESC para fechar".format(palavra_aleatoria)

        self.ids.imagem.source = "Fundo Preto.png"

    #Monta o boneco
    def mudaimagem(self):
        if self.tentativas == 5:
            self.ids.imagem.source = "Cabeca.png"
        if self.tentativas == 4:
            self.ids.imagem.source = "Corpo.png"
        if self.tentativas == 3:
            self.ids.imagem.source = "Braco Direito.png"
        if self.tentativas == 2:
            self.ids.imagem.source = "Braco Esquerdo.png"
        if self.tentativas == 1:
            self.ids.imagem.source = "Perna Direita.png"
        
#-----------------------------------------------------------------------
# CRIAÇÃO DO APLICATIVO
#-----------------------------------------------------------------------

class Forca(App):
    def build(self):
        self.title = "Jogo da Forca"
        return Quadro()

Forca().run()
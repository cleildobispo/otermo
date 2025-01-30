import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout


class ForcaApp(BoxLayout):
    def __init__(self, **kwargs):

        super().__init__(orientation='vertical', **kwargs)
        with self.canvas.before:
            self.bg_image = Rectangle(
                source="fundo.jpg", size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        self.carregar_palavras()

    def _update_bg(self, *args):
        self.bg_image.size = self.size
        self.bg_image.pos = self.pos

    def carregar_palavras(self):
        with open("palavras.txt", "r", encoding="utf-8") as f:
            palavras = f.read().splitlines()

        self.palavra = random.choice(palavras)
        self.vida = 6
        self.n = len(self.palavra)
        self.exibicao = list("_" * self.n)
        self.palpites = []
        self.acertou = False

        self.clear_widgets()

        self.label_palavra = Label(
            text=f"A palavra é: {' '.join(self.exibicao)}", font_size='20sp', pos_hint={"center_x": 0.5, "top": 0.15}, size_hint=(0.8, 0.8))

        self.add_widget(self.label_palavra)

        self.label_vidas = Label(text=f"Vidas restantes: {
                                 self.vida}", font_size='18sp')
        self.add_widget(self.label_vidas)

        self.label_palpites = Label(text=f"Seus palpites: {
                                    ', '.join(self.palpites)}", font_size='16sp')
        self.add_widget(self.label_palpites)

        self.input_letra = TextInput(
            hint_text="Digite uma letra", multiline=False, font_size='18sp')
        self.input_letra.bind(on_text_validate=self.processar_palpite)
        self.add_widget(self.input_letra)
        self.btn_enviar = Button(text="Enviar", font_size='18sp')
        self.btn_enviar.bind(on_press=self.processar_palpite)
        self.add_widget(self.btn_enviar)
        self.label_mensagem = Label(text="", font_size='16sp')
        self.add_widget(self.label_mensagem)

        self.btn_reiniciar = Button(text="Recomeçar", size_hint=(None, None),
                                    size=(50, 50),
                                    pos_hint={"center_y": 0.1, "x": 0.05},
                                    background_normal='',
                                    background_color=(1, 1, 0.5, 0.5),
                                    font_size='20sp')
        self.btn_reiniciar.bind(on_press=self.reiniciar_jogo)
        self.btn_reiniciar.disabled = True
        self.add_widget(self.btn_reiniciar)
        self.btn_proximo = Button(text="Próximo", size_hint=(None, None),
                                  size=(50, 50),
                                  pos_hint={"center_y": 0.1, "x": 0.8},
                                  background_normal='',
                                  background_color=(1, 1, 0.5, 0.5),
                                  font_size='20sp')
        self.btn_proximo.bind(on_press=self.reiniciar_jogo)
        self.btn_proximo.disabled = True
        self.add_widget(self.btn_proximo)

    def processar_palpite(self, instance):
        letra = self.input_letra.text.lower()
        self.input_letra.text = ""

        if not letra or len(letra) != 1:
            self.label_mensagem.text = "Digite apenas uma letra."
            return
        if letra in self.palpites:
            self.label_mensagem.text = "Você já digitou essa letra!"
            return
        self.palpites.append(letra)

        if letra in self.palavra:
            for i in range(self.n):
                if self.palavra[i] == letra:
                    self.exibicao[i] = letra
        else:
            self.vida -= 1
        if self.vida == 0:
            self.label_mensagem.text = f"Você perdeu! A palavra era: {
                self.palavra}."
            self.btn_enviar.disabled = True
            self.btn_reiniciar.disabled = False
        elif "_" not in self.exibicao:
            self.label_mensagem.text = "Parabéns, você acertou!"
            self.btn_enviar.disabled = True
            self.btn_reiniciar.disabled = False
        else:
            self.label_mensagem.text = ""

        self.atualizar_interface()

    def atualizar_interface(self):
        self.label_palavra.text = f"A palavra é: {' '.join(self.exibicao)}"
        self.label_vidas.text = f"Vidas restantes: {self.vida}"
        self.label_palpites.text = f"Seus palpites: {', '.join(self.palpites)}"

    def reiniciar_jogo(self, instance):
        self.carregar_palavras()


class JogoForcaApp(App):
    def build(self):
        return ForcaApp()


if __name__ == "__main__":
    Window.size = (800, 600)
    JogoForcaApp().run()

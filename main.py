from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemLabel, ListView


class TestApp(App):
    def build(self):
        self.title = 'KSU Basestation'

        b = Button(text='Hello World')
        b.on_release = lambda: print(1)

        s = Slider(orientation='vertical', size_hint=(None, 1))

        la = ListAdapter(data=map(str, list(range(30))), cls=ListItemLabel)
        l = ListView(adapter=la)

        box = BoxLayout()
        box.add_widget(l)
        box.add_widget(b)
        box.add_widget(s)

        return box

TestApp().run()

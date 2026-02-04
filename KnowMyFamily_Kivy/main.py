from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from games.meet_my_family import meet_family
from games.find_my_family import find_family
from games.who_is_speaking import who_is_speaking

Builder.load_file("knowmyfamily.kv")

class MenuScreen(Screen):
    def meet_family(self):
        meet_family()

    def find_family(self):
        find_family()

    def who_speaking(self):
        who_is_speaking()

class KnowMyFamilyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        return sm

if __name__ == "__main__":
    KnowMyFamilyApp().run()

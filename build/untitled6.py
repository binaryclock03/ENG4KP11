from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import network_main as nm
import model as modeldef
import utility as util

Window.size=(340,610)
KV = '''
MDScreen:

    MDTopAppBar:
        id:tool1
        title:'ENG App'
        pos_hint:{'top':1}
        right_action_items : [["dots-vertical", lambda x: app.menu.open()]]

'''


class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        items_d = ['Select Files','Help','Exit']
        menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in items_d
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.tool1,
            items=menu_items,
            width_mult=2,
        )

    def menu_callback(self, text_item):     #python 3.10+ has match case (basically switch-case)
        if text_item == 'Select Files':
            print('3')
        elif text_item == 'Help':
            popup = Popup(title='Test popup', content=Label(text='Click on Select Files and the program will automatically output the accuracy of your TIFF files.'), size_hint=(None, None), size=(200, 400))
            popup.open()
        elif text_item == 'Exit':
            MDApp.get_running_app().stop()

        
        print(text_item)
        self.menu.dismiss()         #close dropdown every time u choose an option

    def build(self):
        return self.screen
    


Test().run()
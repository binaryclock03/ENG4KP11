from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from network_lib import network_main as nm
from network_lib.functions import model_definition as modeldef

from kivy.uix.modalview import ModalView
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast


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
        self.manager_open = False
        self.manager = None
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
            self.file_manager_open()
        elif text_item == 'Help':
            popup = Popup(title='Help Popup', content=Label(text_size=(180, None),text='Click on Select Files and the program will automatically output the accuracy of your TIFF files.'), size_hint=(None, None), size=(200, 400))
            popup.open()
        elif text_item == 'Exit':
            MDApp.get_running_app().stop()

        
        print(text_item)
        self.menu.dismiss()         #close dropdown every time u choose an option

    def build(self):
        return self.screen
    
    def file_manager_open(self):
        if not self.manager:
            self.manager = ModalView(size_hint=(1, 1), auto_dismiss=False)
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager, select_path=self.select_path)
            self.manager.add_widget(self.file_manager)
            self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True
        self.manager.open()

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager.dismiss()
        self.manager_open = False

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device..'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

Test().run()
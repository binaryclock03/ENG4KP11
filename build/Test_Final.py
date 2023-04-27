import kivy
kivy.require('1.11.1') # replace with your current Kivy version

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.colorpicker import Color
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty
from kivy.graphics import Rectangle

import network_lib.functions.model_definition as modeldef
import network_lib.functions.network_functions as fnf
from kivy.uix.popup import Popup

from pathlib import Path
#import tiff_reader_test

import os
import glob




class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the background color to white
        with self.canvas:
            Color(0.212, 0.208, 0.216)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # Bind the function to update the background color when the size or position changes
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Create a box layout for the main menu
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Add the logo to the layout
        logo = Image(source='logo.png',size_hint=(0.35, 0.35), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(logo)
        
        # Add buttons for each option
        file_viewer_button = Button(text='Open File Viewer', font_size=18, size_hint=(0.4, 0.15), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        file_viewer_button.bind(on_press=self.open_file_viewer)
        file_viewer_button.background_normal = 'button_1.png'
        file_viewer_button.background_down = 'button_1_down.png'
        file_viewer_button.background_color = (0.996, 0.98, 0.863)
        file_viewer_button.color = (0, 0, 0)
        layout.add_widget(file_viewer_button)
        
        app_settings_button = Button(text='App Settings', font_size=18, size_hint=(0.4, 0.15), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        app_settings_button.bind(on_press=self.open_app_settings)
        app_settings_button.background_normal = 'button_1.png'
        app_settings_button.background_down = 'button_1_down.png'
        app_settings_button.background_color = (0.996, 0.98, 0.863)
        app_settings_button.color = (0, 0, 0)
        layout.add_widget(app_settings_button)
        
        about_button = Button(text='About the App', font_size=18, size_hint=(0.4, 0.15), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        about_button.bind(on_press=self.open_about)
        about_button.background_normal = 'button_1.png'
        about_button.background_down = 'button_1_down.png'
        about_button.background_color = (0.996, 0.98, 0.863)
        about_button.color = (0, 0, 0)
        layout.add_widget(about_button)
        
        # Set the main menu screen to use the box layout
        self.add_widget(layout)
    
    def open_file_viewer(self, instance):
        self.manager.current = 'file_viewer'
    
    def open_app_settings(self, instance):
        self.manager.current = 'app_settings'
    
    def open_about(self, instance):
        self.manager.current = 'about'
       
    def _update_rect(self, instance, value):
        # Update the background color to fill the entire screen
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class FileViewer(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # create title for page
        self.title = Label(text="File Browser", size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=40)
        layout.add_widget(self.title)

        # create file chooser widget
        self.file_chooser = FileChooserListView(path="")#change to relative android path for apk C:/Users/Aditya Arora/Python/venv/ENG4KP11/build
        self.file_chooser.dirselect = True
        self.file_chooser.bind(selection=self.on_file_selection)
        layout.add_widget(self.file_chooser)
        
        # create image widget to display generated image
        self.image_widget = Image()
        layout.add_widget(self.image_widget)
        
        # create label widget
        self.label_widget = Label()
        layout.add_widget(self.label_widget)

        # create button widget to generate fake image
        self.generate_button = Button(text='Generate Image', on_press=self.generate_image, size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.generate_button)

        # add it all to the layout
        self.add_widget(layout)

    def on_file_selection(self, file_chooser, selection):
        if selection:
            self.image_path = selection[0]

    def generate_image(self, instance):
        '''
        model_path (str): path towards the model to generate outputs
        data_folder_path (str): path towards the data folder in which the function will itterate over
        background_image_path (str): path towards the background image in which to overlay onto
        output_file_path (str): path to and name of the image to be generated

        '''
        
        if self.image_path:
            if (Path(self.image_path).is_dir()):
                
                # get a list of all files in the directory with the given extension
                all_files = glob.glob(os.path.join(os.getcwd() + "\\assets\\saved_models", '*.h5'))
                #print(os.path.join(os.getcwd() + "\\assets\\saved_models"))
                latest_file = max(all_files, key=os.path.getmtime)
                print(latest_file)
                
                
                #cwd = os.getcwd()
                #print("THIS IS MY PATH: ")
                #print(r'' + cwd + "\\network_lib\\saved_models\\trained_model_2023-02-11_13-12-27.h5")   #works fine
                
                #tiff_reader_test.create_overlay_image("","","","")
            elif (Path(self.image_path).is_file()):
                if self.image_path.endswith('.tif'):
                    image = fnf.load_single_tiff(self.image_path)
                    model = fnf.load_model("build\\network_lib\\saved_models\\trained_model_2023-02-11_13-12-27.h5")#change to relative android path for apk
                    print(fnf.predict_class(model, image)[0])
                    self.label_widget.text = str(fnf.predict_class(model, image)[0])
                elif self.image_path.endswith('.png'):
                    generated_image = Image(source=f'{self.image_path}')
                    self.image_widget.texture = generated_image.texture
                    self.label_widget.text = 'This is not the proper input for the Neural Network'
        else:
            self.label_widget.text = 'No file/folder selected'    
    
    def close_file_viewer(self, instance):
        # This method will be called when the "Close" button is pressed
        # You can replace this with your own code to close the file viewer screen
        self.manager.current = 'menu'
        print('Closing File Viewer...')

class About(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create a box layout for the file viewer screen
        layout = BoxLayout(orientation='vertical')
        
        # Add a label to show the name of the file being viewed
        filename_label = Label(text='Filename: ')
        layout.add_widget(filename_label)
        
        # Add a button to close the file viewer screen
        back_button = Button(text='Back')
        back_button.bind(on_press=self.back_about_viewer)
        layout.add_widget(back_button)
        
        up_button = Button(text='Upgrade!')
        up_button.bind(on_press=self.upgrade_method)
        layout.add_widget(up_button)
        
        #show_popup(self, layout)
        
        # Set the file viewer screen to use the box layout
        self.add_widget(layout)
    def back_about_viewer(self, instance):
        # This method will be called when the "Back" button is pressed
        # You can replace this with your own code to close the file viewer screen
        self.manager.current = 'menu'
        
    def upgrade_method(self, instance):
        # This method will be called when the "up" button is pressed
        popup = Popup(title='Upgrade to Premium', content=BoxLayout(orientation='vertical'), size_hint=(None, None), size=(400, 200),
                          pos_hint={'center_x': 0.5, 'top': 1})
        popup.content.add_widget(Label(text='Upgrade to Premium to unlock more features!'))
        upgrade_button = Button(text='Upgrade', size_hint_y=None, height=40)
        #upgrade_button.bind()
        popup.content.add_widget(upgrade_button)
        
        dismiss_button = Button(text='Dismiss', size_hint_y=None, height=40)
        dismiss_button.bind(on_press=popup.dismiss)
        popup.content.add_widget(dismiss_button)
        popup.open()

    
def show_popup(self, content):
    popup = Popup(title='Upgrade to Premium', content=BoxLayout(orientation='vertical'), size_hint=(None, None), size=(400, 200),
                      pos_hint={'center_x': 0.5, 'top': 1})
    popup.content.add_widget(Label(text='Upgrade to Premium to unlock more features!'))
    
    upgrade_button = Button(text='Upgrade', size_hint_y=None, height=40)
    #upgrade_button.bind()
    popup.content.add_widget(upgrade_button)
    
    dismiss_button = Button(text='Dismiss', size_hint_y=None, height=40)
    dismiss_button.bind(on_press=popup.dismiss)
    popup.content.add_widget(dismiss_button)
    popup.open()
        
class AppSettings(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create a box layout for the app settings screen
        layout = BoxLayout(orientation='vertical')
        
        # Add a label to show the current settings
        settings_label = Label(text='Current settings:')
        layout.add_widget(settings_label)
        
        # Add a button to close the app settings screen
        back_button = Button(text='Back')
        back_button.bind(on_press=self.back_app_settings)
        layout.add_widget(back_button)
        
        # Set the file viewer screen to use the box layout
        self.add_widget(layout)
    def back_app_settings(self, instance):
        # This method will be called when the "Back" button is pressed
        # You can replace this with your own code to close the file viewer screen
        self.manager.current = 'menu'  

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.add_widget(MainMenu(name='menu'))
        self.add_widget(FileViewer(name='file_viewer'))
        self.add_widget(AppSettings(name='app_settings'))
        self.add_widget(About(name='about'))
   
class MyApp(App):

    def build(self):
        self.title = 'Disease Detector' # Set title
        return MyScreenManager()

if __name__ == '__main__':
    app = MyApp()
    app.run()

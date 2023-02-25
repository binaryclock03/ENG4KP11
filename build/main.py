import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty
from kivy.uix.label import Label

import network_lib.functions.model_definition as modeldef
import network_lib.functions.network_functions as fnf


def get_files_by_extension(file_paths, extension):
    filtered_files = []
    for file_path in file_paths:
        if file_path.endswith(extension):
            filtered_files.append(file_path)
    return filtered_files

class MainScreen(BoxLayout):

    image_path = StringProperty('')

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'

        # create file chooser widget
        self.file_chooser = FileChooserListView(path='/data/data/org.test.myapp/files')
        self.file_chooser.bind(selection=self.on_file_selection)

        # create button widget to generate fake image
        self.generate_button = Button(text='Generate Image', on_press=self.generate_image)

        # add widgets to main screen layout
        self.add_widget(self.file_chooser)
        self.add_widget(self.generate_button)

        # create image widget to display generated image
        self.image_widget = Image()
        self.add_widget(self.image_widget)
        
        # create label widget
        self.label_widget = Label()
        self.add_widget(self.label_widget)

    def on_file_selection(self, file_chooser, selection):
        if selection:
            self.image_path = selection[0]

    def generate_image(self, instance):
        if self.image_path:
            if self.image_path.endswith('.tif'):
                # fake function that generates image from file path
                # replace this with your own image generation function
                generated_image = self.generate_image_from_path(self.image_path)
                self.image_widget.texture = generated_image.texture
                model = "saved_models\\trained_model_2023-02-11_13-12-27.h5"
                self.label_widget.text = fnf.predict_class(model, self.image_path)
            elif self.image_path.endswith('.png'):
                generated_image = Image(source=f'{self.image_path}')
                self.image_widget.texture = generated_image.texture
                self.label_widget.text = 'Invalid file format'
        else:
            self.label_widget.text = 'No file selected'

class MyApp(App):

    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()

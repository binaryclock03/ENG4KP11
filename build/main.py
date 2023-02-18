import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty

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

    def on_file_selection(self, file_chooser, selection):
        if selection:
            self.image_path = selection[0]

    def generate_image(self, instance):
        if self.image_path:
            # fake function that generates image from file path
            # replace this with your own image generation function
            self.image_widget.source = 'fake_image.png'

class MyApp(App):

    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()
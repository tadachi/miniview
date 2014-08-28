import kivy
kivy.require('1.0.6')


### Python Libs
import glob
import os
from random import randint
from pprint import pprint
### Main
from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.widget import Widget

### Widgets
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup

### Layouts
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout

### Misc
from kivy.factory import Factory
from kivy.properties import ObjectProperty

from kivy.properties import StringProperty

class CustomPopup(Popup):
    content = ObjectProperty(None)
    title = ObjectProperty(None)
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    current_path = ObjectProperty(None)
    rootpath = StringProperty(None)
    sortfunc = ObjectProperty(None)

class ImagePage(Image):
    source = StringProperty(None)
    pass

class Root(AnchorLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    image_index = 0
    folder_index = 0
    number_of_images = 0
    merged_image_list = []

    current_path = os.path.normcase('/')
    current_path_folders = glob.glob(os.path.normcase(os.path.join(current_path, '*')))
    previous_path_folders = current_path_folders

    def show_popup(self, text):
        self.popup = CustomPopup(title=text)
        self.popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def dismiss_popup_filechooser(self, path):
        self.current_path = path
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup_filechooser, current_path=self.current_path, rootpath = '/')
        self._popup = Popup(title="Load file", content=content, size_hint=(1, 1))
        self._popup.open()

    def load(self, path, filename):
        pprint(path)
        # self.change_directory(path)
        pngs = glob.glob(os.path.join(path, '*.png'))
        jpgs = glob.glob(os.path.join(path, '*.jpg'))
        gifs = glob.glob(os.path.join(path, '*.gif'))
        merged_image_list = pngs + gifs + jpgs
        merged_image_list = sorted(merged_image_list)
        self.merged_image_list = merged_image_list

        self.previous_path_folders = self.current_path_folders

        self.current_path_folders = glob.glob(os.path.join('../',path, '*'))

        if (filename): # Select a file then load.

            if (merged_image_list): # If there's at least one valid image file with .png, .jpg, .gif, etc.
                for i in range(0, len(self.previous_path_folders)):
                    if ( os.path.normcase(filename[0]) in os.path.normcase(self.previous_path_folders[i]) ):
                        self.folder_index = i

                for i in range(0, len(merged_image_list)): # Set the index of current image.
                    if ( os.path.normcase(filename[0]) in os.path.normcase(merged_image_list[i]) ):
                        self.image_index = i
                pprint(self.previous_path_folders)
                pprint(filename[0])
                pprint(self.folder_index)
                self.number_of_images = len(merged_image_list)

            if ( filename[0].endswith('.jpg') or filename[0].endswith('.png') ):
                self.change_image(os.path.normcase(filename[0]))

                self.set_file_label(os.path.normcase(filename[0]))
                self.set_folder_label(os.path.normcase(path))

                self.dismiss_popup_filechooser(path)
            else:
                self.show_popup('Not a valid file type.')
        else:
            self.show_popup('Invalid file.')

    def load_folder(self, path, folder):
        pass

    def change_image(self, filename):
        self.ids.page.source = filename

    def change_directory(self, path):
        self.ids.filechooser.path = path

    def set_file_label(self, filename):
        self.ids.current_file.text = filename

    def set_folder_label(self, folder):
        self.ids.current_folder.text = folder

    def next_image(self):
        if ( len(self.merged_image_list) > 0 ):
            if ( (self.image_index+1) <= self.number_of_images-1 ):
                self.image_index += 1
                self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
            else:
                self.image_index = 0
                self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
        print("".join([str(self.image_index), '/', str((self.number_of_images-1))]))

    def prev_image(self):
        if ( len(self.merged_image_list) > 0 ):
            if ( (self.image_index-1) <= len(self.merged_image_list) and (self.image_index-1) >= 0):
                self.image_index -= 1
                self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
            else:
                self.image_index = self.number_of_images-1
                self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
        pass
        print("".join([str(self.image_index), '/', str((self.number_of_images-1))]))

    def next_folder(self):
        pass

    def prev_folder(self):
        pass

    pass

class Mangaget_App(App):
    def build(self):
        root = Root()
        return(root)

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Mangaget_App().run()

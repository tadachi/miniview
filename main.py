import kivy
kivy.require('1.0.6')

### Python Libs
import glob
import os
import time
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
from kivy.uix.scatter import Scatter

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
from kivy.clock import Clock
from kivy.core.window import Window

class CustomPopup(Popup):
    content = ObjectProperty(None)
    title = ObjectProperty(None)
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    up = ObjectProperty(None)
    rootpath = StringProperty(None)
    current_path = ObjectProperty(None)

class Root(AnchorLayout):
    image_index = 0
    folder_index = 0
    number_of_images = 0
    merged_image_list = [] # Combined image paths of all image types: png, jpg, gif.

    current_path = os.path.normcase('/')
    current_path_folders = glob.glob(os.path.normcase(os.path.join(current_path, '*')))
    previous_path_folders = current_path_folders

    ### Special Button Events ###
    def initialize_button_binds(self):
        btn1 = self.ids.next_bottom_right
        btn1.bind(state=self.on_down_next_image)
        btn2 = self.ids.next_top_right
        btn2.bind(state=self.on_down_next_image)
        btn3 = self.ids.prev_bottom_left
        btn3.bind(state=self.on_down_prev_image)
        btn4 = self.ids.prev_top_left
        btn4.bind(state=self.on_down_prev_image)

    def on_down_next_image(self, obj, value): # Hold down the button to cycle forward quickly.
        if (value == 'down'):
            Clock.schedule_interval(self.next_callback, 0.105 / 1)
        else:
            Clock.unschedule(self.next_callback)
        # print("Typical property change from", obj, "to", value)

    def on_down_prev_image(self, obj, value): # Hold down button cycle reverse.
        if (value == 'down'):
            Clock.schedule_interval(self.prev_callback, 0.105 / 1)
        else:
            Clock.unschedule(self.prev_callback)

    def next_callback(self, value, *args):
        self.next_image()

    def prev_callback(self, value, *args):
        self.prev_image()

    ### Popups ###
    def show_popup(self, text):
        self.popup = CustomPopup(title=text)
        self.popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def dismiss_popup_filechooser(self, path): # Save the current you were currently in upon cancel/dismissing load popup
        self.current_path = path
        self._popup.dismiss()

    ### File Chooser ###
    def show_load(self):
        content = LoadDialog(load=self.load, up=self.go_up_dir, cancel=self.dismiss_popup_filechooser, current_path=self.current_path, rootpath = '/')
        self._popup = Popup(title="Load Image..", content=content, size_hint=(1, 1))
        self._popup.open()

    def go_up_dir(self, path):
        pprint(path)
        previous_path = os.path.dirname(path)
        pprint(previous_path)
        #self.ids.filechooser.path = previous_pat
        #pprint(filechooser.path)
        #up = os.path.dirname(os.path.dirname(path))
        #self.ids.filechooser.path = up
        #print(up)
        #print(self.current_path)
        #print(selection)
        pass

    def load(self, path, filename):
        path = os.path.abspath(path)
        self.folder_index = 0
        self.merged_image_list = self.create_image_list(path)

        self.previous_path_folders = glob.glob( os.path.abspath(os.path.join(path, '..', '*')) ) #../mangahere/naruto/naruto_001/.. == ../mangahere/naruto/
        self.previous_path_folders = [folder for folder in self.previous_path_folders if os.path.isdir(folder) == True] # Filter for only folders and keep out .txt files, .exe files, etc

        self.current_path_folders = glob.glob( os.path.abspath(os.path.join(path, '*')) )
        self.current_path_folders = [folder for folder in self.current_path_folders if os.path.isdir(folder) == True] # Filter for only folders and keep out .txt files, .exe files, etc

        if (filename): # Select a file then load.

            if (self.merged_image_list): # If there's at least one valid image file with .png, .jpg, .gif, etc.
                # pprint(self.previous_path_folders)
                for i in range(0, len(self.previous_path_folders)):
                    if ( os.path.normcase(path) in os.path.normcase(self.previous_path_folders[i]) ):
                        self.folder_index = i

                for i in range(0, len(self.merged_image_list)): # Set the index of current image.
                    if ( os.path.normcase(filename[0]) in os.path.normcase(self.merged_image_list[i]) ):
                        self.image_index = i

                self.number_of_images = len(self.merged_image_list)

            if ( filename[0].endswith('.jpg') or filename[0].endswith('.png') ):
                self.change_image(os.path.normcase(filename[0]))

                self.set_file_label(os.path.normcase(path)) # normcase converts forward slashes to backwards slashes, converts upper to lower in case-insensitive filesystems.

                self.dismiss_popup_filechooser(path)
            else:
                self.show_popup('Not a valid file type.')
        else:
            self.show_popup('Invalid file.')

    ### Image ###
    # Goes to the next image.
    # If you go to the next image when you are on the last, go to the first image of the next directory.
    def next_image(self):
        print( "".join(['merged_image_list count:', str(len(self.merged_image_list))]) )

        if ( (self.image_index+1) <= self.number_of_images-1 ):
            self.image_index += 1
            self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
            path = self.previous_path_folders[self.folder_index]
            self.set_file_label(os.path.normcase(path[-20:])) # Set it to the last 20 characters of string path.
        else:
            print(self.folder_index)
            print(len(self.previous_path_folders)-1)

            if ( (self.folder_index+1) <= len(self.previous_path_folders)-1 ): # Go to next folder.
                self.folder_index += 1
                path = self.previous_path_folders[self.folder_index]
                self.set_file_label(os.path.normcase(path))
                self.current_path_folders = glob.glob(os.path.join(path, '*'))
                self.merged_image_list = self.create_image_list(path)
                self.number_of_images = len(self.merged_image_list)
                self.image_index = 0
                if (self.merged_image_list): # If there's at least one valid image file with .png, .jpg, .gif, etc.
                    self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
                else:
                    self.change_image(os.path.normcase('images/no_image.jpg'))
            else:
                self.folder_index = 0 # Go to the first folder.
                self.image_index = 0

        print("".join([str(self.image_index), '/', str((self.number_of_images-1))]))

    # Goes to the previous image.
    # If you go to the previous image when you are on the first, go to the last image of the previous directory.
    def prev_image(self):
        print( "".join(['merged_image_list count:', str(len(self.merged_image_list))]) )

        if ( (self.image_index-1) >= 0):
            self.image_index -= 1
            self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
            path = self.previous_path_folders[self.folder_index]
            self.set_file_label(os.path.normcase(path[-20:])) # Set it to the last 20 characters of string path.
        else:
            print(self.folder_index)
            print(len(self.previous_path_folders)-1)

            if ( (self.folder_index-1) >= 0 ): # Go to previous folder.
                self.folder_index -= 1
                path = self.previous_path_folders[self.folder_index]
                self.set_file_label(os.path.normcase(path))
                self.current_path_folders = glob.glob(os.path.join(path, '*'))
                self.merged_image_list = self.create_image_list(path)
                self.number_of_images = len(self.merged_image_list)
                self.image_index = (self.number_of_images-1) # Last image of the previous folder.
                if (self.merged_image_list): # If there's at least one valid image file with .png, .jpg, .gif, etc.
                    self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
                else:
                    self.change_image(os.path.normcase('images/no_image.jpg'))
            else:
                self.folder_index = len(self.previous_path_folders)-1 # Go to the last folder.
                if (self.previous_path_folders):
                    pprint(self.previous_path_folders)
                    path = self.previous_path_folders[self.folder_index]
                    self.current_path_folders = glob.glob(os.path.join(path, '*'))
                    self.merged_image_list = self.create_image_list(path)
                    self.number_of_images = len(self.merged_image_list)
                    self.image_index = (self.number_of_images-1)
                    if (self.number_of_images > 0):
                        self.change_image(os.path.normcase(self.merged_image_list[self.image_index]))
                        self.set_file_label(os.path.normcase(path[-20:])) # Set it to the last 20 characters of string path.

        print("".join([str(self.image_index), '/', str((self.number_of_images-1))]))

    def create_image_list(self, path):
        pngs = glob.glob(os.path.join(path, '*.png'))
        jpgs = glob.glob(os.path.join(path, '*.jpg'))
        gifs = glob.glob(os.path.join(path, '*.gif'))
        merged_image_list = pngs + gifs + jpgs
        merged_image_list = sorted(merged_image_list)
        return merged_image_list

    def change_image(self, filename):
        self.ids.page.source = filename
        #self.ids.center_parent.pos = (0,0)    # Return the image moved to the center of the screen.
        self.ids.scatter.scale = 1   # Unzoom the image.
        self.ids.page.pos = (0,0)    # Return the image moved to the center of the screen.
        self.ids.scatter.pos = (0,0) # Return the image moved to the center of the screen.

    def get_current_image_count(self):
        s1 = str(self.image_index)
        s2 = str((self.number_of_images-1))
        print(self.number_of_images)
        if (self.number_of_images == 0):
            return False
        else:
            print("".join( [s1, '/', s2] ))
            return "".join( [s1, '/', s2] )

    ### Set Labels ###
    def set_file_label(self, filename):
        filename = os.path.basename(filename)
        if (self.number_of_images > 0):
            text = "".join(['.../', filename, '    ', str(self.image_index+1), '/', str(self.number_of_images)])
        else:
            text = filename
        self.ids.current_file.text = text

    def set_folder_label(self, folder):
        self.ids.current_folder.text = folder

    ### Pause/Resume####
    def on_pause(self):
    # Here you can save data if needed
        return True

    def on_resume(self):
    # Here you can check if any data needs replacing (usually nothing)
        pass

class main(App):
    def build(self):
        root = Root()
        root.initialize_button_binds() # Initialize button binds.
        return(root)

if __name__ == '__main__':
    main().run()




import os
import csv
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class ImageButton(ButtonBehavior, Image):
    pass

class ClickableImageGridApp(App):
    def __init__(self, **kwargs):
        super(ClickableImageGridApp, self).__init__(**kwargs)
        self.data_file = "image_data.csv"  # CSV database file path
        self.image_data = {}  # Dictionary to store image data (name and path)

    def build(self):

        folder_path = "img/"  # Replace with the path to your image folder

        # Get a list of all image files in the folder
        image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        # Load data from CSV database file (if it exists)
        self.load_data()

        # Create a RelativeLayout as the main layout
        main_layout = RelativeLayout()

        # Create a Widget for the red rectangle
        red_rectangle = Widget(size_hint=(1, None), height=200, pos = (0, Window.height - 200))

        # Position the red rectangle at the top of the window
        red_rectangle.pos_hint = {'top': 1}

        with red_rectangle.canvas:
            Color(0.188235, 0.49019608, 0.6196078, 1)  # Set color to red (R, G, B, A)
            self.rect = Rectangle(pos=red_rectangle.pos, size=red_rectangle.size)

            Clock.schedule_interval(self.update_rect_size, 0)
            Clock.schedule_interval(self.update_rect_pos, 0)

        # Create a GridLayout to hold the images
        self.grid_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))  # Make the GridLayout height dynamically adjust based on content

        for filename in image_files:
            path = os.path.join(folder_path, filename)
            image = ImageButton(source="", size_hint=(None, None), size=(200, 200))
            image.source = path
            image.bind(on_release=self.on_image_click)
            self.grid_layout.add_widget(image)

            # Get image name without file extension
            image_name = os.path.splitext(filename)[0]
            self.image_data[image_name] = path
            print('image loaded into path')

        scroll_view_size_y = Window.height - 200


        # Create a ScrollView and add the GridLayout to it
        scroll_view = ScrollView(size_hint=(1, None), size= (Window.width, scroll_view_size_y))  #  ||||| Subtract 200 for the height of the red rectangle
        scroll_view.add_widget(self.grid_layout)

        # Add the red rectangle and the ScrollView to the main_layout
        main_layout.add_widget(red_rectangle)
        main_layout.add_widget(scroll_view)

        # Schedule the real-time updates of the columns
        self.grid_layout.bind(width=self.on_resize)
        print('build')


        return main_layout

    def on_resize(self, instance, width):
        cols = max(1, int(width / 200))  # 200 is the fixed image width
        self.grid_layout.cols = cols

    def update_rect_size(self, dt):
        """Update the size of the red rectangle as the window is resized."""
        self.rect.size = (Window.width, 200)

    def update_rect_pos(self, dt):
        """Update the size of the red rectangle as the window is resized."""
        self.rect.pos = (0, Window.height - 200)

    def on_window_size(self, instance, width, height):
        """Update the scroll view size when the window size changes."""
        self.scroll_view.size = (width, height - 200)  # Subtract 200 for the height of the red rectangle
        self.grid_layout.height = height - 200

    def on_image_click(self, instance):
        # Handle the click event here
        print("Image Clicked:", instance.source)
        cnt = 0

        cnt+=1
        print(cnt)
        print(Window.height)





    def img_display(self):
        pass



    def load_data(self):
        # Load data from the CSV database file and populate the image_data dictionary
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 2:
                        self.image_data[row[0]] = row[1]
                print('loaded')

    def save_data(self):
        # Save the image_data dictionary to the CSV database file
        with open(self.data_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for image_name, path in self.image_data.items():
                writer.writerow([image_name, path])
            print('saved')

    def on_stop(self):
        # Save data to CSV database when the app is closed
        self.save_data()

if __name__ == "__main__":
    ClickableImageGridApp().run()

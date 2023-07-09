from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime

class DialogContent(MDBoxLayout):
    # Init function for class constructor
    def __init__(self, **kwargs):
         super().__inti__(**kwargs)
         self.ids.date_text = datetime.now().strftime("%A %d %B %Y")

    # Function to show date picker
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date.dialog.bind(on_save = self.on_save)

    # Function to get and save date
    def on_save(self,instance,value,date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)

# Main app class
class MainApp(MDApp):
    task_list_dialog = None
    # Build function for theme
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

    # Function to show tasks
    def show_tasks(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create new task",
                type="custom",
                content_cls=DialogContent(),
            )

MainApp().run()
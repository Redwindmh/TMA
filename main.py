from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime


class DialogContent(MDBoxLayout):
    # Init function for class constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime("%A %d %B %Y"))

    # Function to show date picker
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    # Function to get and save date
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)


# Class for checking and deleting tasks
class ListItemCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    # Function for marking tasks complete
    def task_checked(self,check,list_item):
        if check.active == True:
            list_item.text = '[s]' + list_item.text + '[/s]'
        else:
            pass

    def task_delete(self,list_item):
        self.parent.remove_widget(list_item)

class LeftCheckbox(ILeftBody,MDCheckbox):
    pass

# Main app class
class MainApp(MDApp):
    task_list_dialog = None
    # Build function for theme
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

    # Function to show tasks
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create new task",
                type="custom",
                content_cls=DialogContent(),
            )
        self.task_list_dialog.open()

    # Function to add new task
    def add_task(self, task, task_date):
        print(task.text, task_date)

    # Function to close dialog
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

if __name__ == "__main__":
    app = MainApp()
    app.run()

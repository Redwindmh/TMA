from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime
from database import Database

db = Database()

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
            db.mark_task_completed(list_item.pk)
        else:
            list_item.text = str(db.mark_task_incompleted(list_item.pk))

    # Function for deleting task
    def task_delete(self,list_item):
        self.parent.remove_widget(list_item)
        db.delete_task(list_item.pk)

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
        created_task = db.create_task(task.text, task_date)
        self.root.ids['container'].add_widget(ListItemCheckbox(pk = created_task[0],  text = '[b]' + created_task[1] + '[/b]', secondary_text = created_task[2]))
        task.text = ''

    # Function to close dialog
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    # Function to add task to list widget
    def on_start(self):
        ''''Load saved tasks and add them to MDList widget'''
        completed_tasks, incompleted_tasks = db.get_tasks()

        if incompleted_tasks != []:
            for task in incompleted_tasks:
                add_task = ListItemCheckbox(pk = task[0], text = task[1], secondary_text = task[2])
                self.root.ids.container.add_widget(add_task)

        if completed_tasks != []:
            for task in completed_tasks:
                add_task = ListItemCheckbox(pk = task[0], text = "[s]" + task[1] + "[/s]", secondary_text = task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)

if __name__ == "__main__":
    app = MainApp()
    app.run()

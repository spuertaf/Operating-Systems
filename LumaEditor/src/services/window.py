from tkinter import *
from tkinter import messagebox as messagebox
from tkinter import filedialog as filedialog
from services.stack import Stack


class TextEditorWindow:
    """
    TextEditorWindow class provides methods for managing text editing operations.

    Methods:
        __init__: Initializes the TextEditorWindow.
        new_file: Creates a new file.
        open_file: Opens a file for editing.
        save_file: Saves changes to the current file.
        save_new_file: Saves changes to a new file.
        write_file: Writes content to a file.
        retrieve_input: Retrieves input from the text box.
        key_pressed: Handles key press events.
        undo: Undoes the last action.
        redo: Redoes the last undone action.
        on_closing: Handles window closing event.
        exit: Exits the application.
        change_mode: Changes the color mode of the text box.
        about: Displays information about the application.
        copy: Copies selected text.
        cut: Cuts selected text.
        paste: Pastes copied or cut text.
    """
    def __init__(self):
        """
        Initializes the TextEditorWindow.

        """
        self.is_file_open = True
        self.file_path = ""
        self.is_file_changed = False
        self.element_count = 0
        self.mode = "normal"
        self.file_types = [('All Files', '*.*'),
                           ('Python Files', '*.py'),
                           ('Text Document', '*.txt')]

        # Initialize window
        self.window = Tk()
        self.window.geometry("1200x700+200+150")
        self.window.wm_title("Untitled")

        # Initialize Text Widget
        self.text_box = Text(self.window, highlightthickness=0, font=("Helvetica", 14))

        # Initialize MenuBar
        self.menu_bar = Menu(self.window, bg="#eeeeee", font=("Helvetica", 13), borderwidth=0)
        self.window.config(menu=self.menu_bar)
        
        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.file_menu.add_command(label="    New       Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="    Open...      Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="    Save         Ctrl+S", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="    Exit          Ctrl+D", command=self.exit)
        self.menu_bar.add_cascade(label="   File   ", menu=self.file_menu)
        
        # Edit Menu
        self.edit_menu = Menu(self.menu_bar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.edit_menu.add_command(label="    Undo    Ctrl+Z", command=self.undo)
        self.edit_menu.add_command(label="    Redo    Ctrl+Shift+Z", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="    Cut    Ctrl+X", command=self.cut)
        self.edit_menu.add_command(label="    Copy    Ctrl+C", command=self.copy)
        self.edit_menu.add_command(label="    Paste   Ctrl+V", command=self.paste)
        self.menu_bar.add_cascade(label="   Edit   ", menu=self.edit_menu)
        
        # View Menu
        self.view_menu = Menu(self.menu_bar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.view_menu.add_command(label="   Change Mode   ", command=self.change_mode)
        self.menu_bar.add_cascade(label="   View   ", menu=self.view_menu)
        
        # Help Menu
        self.help_menu = Menu(self.menu_bar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.help_menu.add_command(label="    About   ", command=self.about)
        self.menu_bar.add_cascade(label="   Help   ", menu=self.help_menu)

        # Initialize Stack Objects by original state
        self.undo_stack = Stack(self.text_box.get("1.0", "end-1c"))
        self.redo_stack = Stack(self.text_box.get("1.0", "end-1c"))

    def new_file(self):
        """
        Creates a new file.

        """
        self.text_box.config(state=NORMAL)
        if self.is_file_open:
            if len(self.file_path) > 0:
                if self.is_file_changed:
                    self.save_file()
                self.window.wm_title("Untitled")
                self.text_box.delete('1.0', END)
                self.file_path = ''
            else:
                if self.is_file_changed:
                    result = messagebox.askquestion('New File', 'Do You Want to Save Changes?')
                    self.save_new_file(result)
                self.window.wm_title("Untitled")
                self.text_box.delete('1.0', END)
        else:
            self.is_file_open = True
            self.window.wm_title("Untitled")

        self.is_file_changed = False

        if self.undo_stack.size() > 0:
            self.undo_stack.clear_stack()
            self.undo_stack.add(self.text_box.get("1.0", "end-1c"))

    def open_file(self):
        """
        Opens a file for editing.

        """
        self.text_box.config(state=NORMAL)
        if self.is_file_open and self.is_file_changed:
            self.save_file()
        filename = filedialog.askopenfilename(filetypes=self.file_types, defaultextension=".txt")
        if len(filename) != 0:
            self.is_file_changed = False
            with open(filename, "r") as file:
                text = file.read()
            self.text_box.delete('1.0', END)
            self.text_box.insert(END, text)
            self.window.wm_title(filename)
            self.is_file_open = True
            self.file_path = filename

        if self.undo_stack.size() > 0:
            self.undo_stack.clear_stack()
            self.undo_stack.add(self.text_box.get("1.0", "end-1c"))

    def save_file(self):
        """
        Saves changes to the current file.

        """
        result = messagebox.askquestion('Save File', 'Do You Want to Save Changes?')
        if result == "yes":
            if len(self.file_path) == 0:
                save_file = filedialog.asksaveasfile(filetypes=self.file_types, defaultextension=".txt")
                if save_file:
                    self.write_file(save_file.name)
                    self.text_box.delete('1.0', END)
            else:
                self.write_file(self.file_path)

    def save_new_file(self, result):
        """
        Saves changes to a new file.

        Args:
            result: Result of the save operation.

        """
        self.is_file_changed = False
        if result == "yes":
            save_file = filedialog.asksaveasfile(filetypes=self.file_types, defaultextension=".txt")
            if save_file:
                self.write_file(save_file.name)
                self.file_path = save_file.name
        else:
            self.text_box.delete('1.0', END)

    def write_file(self, file):
        """
        Writes content to a file.

        Args:
            file: File to write content to.

        """
        input_value = self.text_box.get("1.0", "end-1c")
        with open(file, "w") as outfile:
            outfile.write(input_value)

    def retrieve_input(self):
        """
        Retrieves input from the text box.

        """
        if self.is_file_open and len(self.file_path) != 0:
            self.write_file(self.file_path)
            self.is_file_changed = False
        else:
            self.save_new_file("yes")
            self.window.wm_title(self.file_path)
            self.is_file_open = True

    def key_pressed(self, event):
        """
        Handles key press events.

        Args:
            event: The key press event.

        """
        if event.char == "\x1a" and event.keysym == "Z":
            self.redo()
        elif event.char == "\x1a" and event.keysym == "z":
            self.undo()
        elif event.char == "\x13":
            self.retrieve_input()
        elif event.char == "\x0f":
            self.open_file()
        elif event.char == "\x0e":
            self.new_file()
        elif event.char == "\x04":
            self.exit()
        elif event.char == " " or event.char == ".":
            self.is_file_changed = True
            input_value = self.text_box.get("1.0", "end-1c")
            self.undo_stack.add(input_value)
        elif event.keysym == 'Return':
            self.is_file_changed = True
            input_value = self.text_box.get("1.0", "end-1c")
            self.undo_stack.add(input_value)
        elif event.keysym == 'BackSpace':
            self.is_file_changed = True
            input_value = self.text_box.get("1.0", "end-1c")
            self.undo_stack.add(input_value)
        elif (event.keysym == 'Up' or event.keysym == 'Down') or (event.keysym == 'Left' or event.keysym == 'Right'):
            self.is_file_changed = True
            self.element_count = 0
            input_value = self.text_box.get("1.0", "end-1c")
            self.undo_stack.add(input_value)
        else:
            self.is_file_changed = True
            input_value = self.text_box.get("1.0", "end-1c")
            if self.element_count >= 1:
                self.undo_stack.remove()
            self.undo_stack.add(input_value)
            self.element_count += 1

        if self.text_box.get("1.0", "end-1c") == self.undo_stack.ele(0):
            self.is_file_changed = False

    def undo(self):
        """
        Undoes the last action.

        """

        self.is_file_changed = True
        if self.undo_stack.size() == 1:
            self.undo_stack.remove()
            self.undo_stack.add(self.text_box.get("1.0", "end-1c"))
        else:
            self.redo_stack.add(self.undo_stack.remove())
            text = self.undo_stack.peek()
            self.text_box.delete('1.0', END)
            self.text_box.insert(END, text)

    def redo(self):
        """
        Redoes the last undone action.

        """
        if self.redo_stack.size() > 1:
            text = self.redo_stack.peek()
            self.text_box.delete('1.0', END)
            self.text_box.insert(END, text)
            self.undo_stack.add(text)
            self.redo_stack.remove()

    def on_closing(self):
        """
        Handles window closing event.

        """
        if self.is_file_open and self.is_file_changed:
            self.save_file()
        self.exit()

    def exit(self):
        """
        Exits the application.

        """
        self.window.quit()
        self.window.destroy()

    def change_mode(self):
        """
        Changes the color mode of the text box.

        """
        if self.mode == "normal":
            self.mode = "dark"
            self.text_box.configure(background="#2f2b2b", foreground="#BDBDBD", font=("Helvetica", 14),
                                    insertbackground="white")
        else:
            self.mode = "normal"
            self.text_box.configure(background="white", foreground="black", font=("Helvetica", 14),
                                    insertbackground="black")

    def about(self):
        """
        Displays information about the application.

        """
        with open("About.txt", "r") as file:
            text = file.read()
        self.text_box.insert(END, text)
        self.text_box.config(state=DISABLED)

    def copy(self):
        """
        Copies selected text.

        """
        self.text_box.clipboard_clear()
        text = self.text_box.get("sel.first", "sel.last")
        self.text_box.clipboard_append(text)

    def cut(self):
        """
        Cuts selected text.

        """
        self.copy()
        self.text_box.delete("sel.first", "sel.last")
        self.undo_stack.add(self.text_box.get("1.0", "end-1c"))

    def paste(self):
        """
        Pastes copied or cut text.

        """
        text = self.text_box.selection_get(selection='CLIPBOARD')
        self.text_box.insert('insert', text)
        self.undo_stack.add(self.text_box.get("1.0", "end-1c"))
import os
import sys
from tkinter import *
from tkinter.filedialog import Open, SaveAs
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo, showerror,askyesno, askyesnocancel
from tkinter.colorchooser import askcolor

from mytext import MyText
from guimaker import GuiMaker

__version__ = 1.0

file_types = [('All files',     '*'),                 # for file open dialog
              ('Text files',   '.txt'),               # customize in subclass
              ('Python files', '.py')]                # or set in each instance

help_text = """
PyEdit version %s
April, 2016

In ShangHai
Liang Lee

A text editor program  written in Python/tkinter.
Use menu tear-offs  for quick access to actions,
no shortcut.

"""


class TextEditor(GuiMaker):

    def start(self):
        self.menuBar = [
            ('File', 0,                             # a GuiMaker menu def tree
             [('Open...',    0, self.on_open),   # build in method for self
              ('Save',       0, self.on_save),   # label, shortcut, callback
              ('Save As...', 0, self.on_save_as),
              ('New', 0, self.on_new),
              'separator',
              ('Quit...', 0, sys.exit)]
             ),

            ('Edit', 0,
             [('Undo',       0, lambda: self.text.on_my_undo()),
              ('Redo',       0, lambda: self.text.on_redo()),
              'separator',
              ('Cut',        0, lambda: self.text.on_cut()),
              ('Copy',       0, lambda: self.text.on_copy()),
              ('Paste',      0, lambda: self.text.on_paste()),
              'separator',
              ('Delete',     0, lambda: self.text.on_delete()),
              ('Select All', 0, lambda: self.text.on_select_all())]
             ),

            ('Search', 0,
             [('Goto...',    0, lambda: self.text.on_goto()),
              ('Find...',    0, lambda: self.text.on_find()),
              ('Replace',  0, None)]
             ),

            ('Tools', 0,
             [('Pick Font...', 0, None),
              ('Font List',    0, lambda: self.text.on_set_font()),
              'separator',
              ('Pick Bg...',   0, lambda: self.text.on_set_bg()),
              ('Pick Fg...',   0, lambda: self.text.on_set_fg()),
              ('Color List',   0, lambda: self.text.on_color_list()),
              'separator',
              ('Info...',      0, lambda: self.text.on_info()),
              ('Run Code',     0, self.on_run_code)]
             ),


        ]
        self.file = None

    def makeWidgets(self, **kwargs):
        self.text = MyText(self)
        self.text.pack(side=TOP, expand=YES, fill=BOTH)

    def my_askopenfile(self):
        file_name = Open(filetype=file_types).show()
        return file_name

    def my_asksaveasfile(self):
        user_file_name = SaveAs(filetype=file_types).show()
        return user_file_name

    def ask_whether_save(self):
        user_cmd =  askyesnocancel('PyEdit', 'Text has changed \nif save the change?')
        if user_cmd is True:
            self.on_save()
        else:
            pass

    def on_open(self, force_file=''):
        file = force_file or self.my_askopenfile()
        if file is None:
            return None

        if not os.path.isfile(file):
            showerror('PyEdit', 'Sorry, %s is not a file' % file)
            return None
        else:
            print(file)
            self.file = file

        text = None
        # try:
        text = open(self.file, 'r').read()
        # except:
        #     showerror('PyEdit', "Can't open\n %s" % file)

        if text is not None:
            self.text.set_text(text)

    def on_save(self):
        if  self.text.edit_modified():
            self.on_save_as(self.file)
            self.text.edit_modified(0)
        else:
            pass

    def on_save_as(self, force_file=''):
        file = force_file or self.my_asksaveasfile()
        print('file is:', file)
        if file is None:
            return None
        else:
            text = self.text.get_text()
            print('text:', text)
            try:
                open(file, 'w').write(text)
            except:
                showerror('Sorry', 'save failed')

    def on_new(self):
        os.startfile('%s' % __file__)

    def on_run_code(self):
        interpreter = StringVar()
        file = StringVar()
        args = StringVar()
        interpreter.initialize('python')
        file.initialize(self.file)
        win = Toplevel()
        config_args_list=[('     Interpreter:', interpreter),
                          ('            File:', file),
                          ('commandline args:', args)]
        r = 0
        for (text, var) in config_args_list:
            Label(win, text=text,width=18).grid(row=r, column=0)
            Entry(win, relief=SUNKEN, width=50, textvariable=var).grid(row=r, column=2)
            r += 1

        def click_run():
            win.destroy()
            shell_command = ' '.join((interpreter.get(),
                                      file.get(),
                                      args.get()))
            os.system(shell_command)
        Button(win, text='Run', width=15, command=click_run).grid(row=r, column=2,sticky=E)

        Button(win, text='Cancel', command=win.destroy).grid(row=r, column=2, sticky=W)

    def help(self):
        showinfo('PyEdit', help_text % __version__)


if __name__ == '__main__':
    root = Tk()
    TextEditor(root)
    root.mainloop()

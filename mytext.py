from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tkinter.simpledialog import askinteger, askstring
from tkinter.colorchooser import askcolor


WIN_TITLE = 'PyEdit'
start_font = ('courier', 18, 'normal')
fonts_list  = [('courier',    9, 'normal'),
               ('courier',   12, 'normal'),
               ('courier',   10, 'bold'),
               ('courier',   10, 'italic'),
               ('times',     10, 'normal'),
               ('helvetica', 10, 'normal'),
               ('ariel',     10, 'normal'),
               ('system',    10, 'normal'),
               ('courier',   20, 'normal')]
colors_list = [{'fg':'yellow',     'bg':'black'},      # first item is default
               {'fg':'white',      'bg':'blue'},       # tailor me as desired
               {'fg':'black',      'bg':'beige'},      # or do PickBg/Fg chooser
               {'fg':'yellow',     'bg':'purple'},
               {'fg':'black',      'bg':'brown'},
               {'fg':'lightgreen', 'bg':'darkgreen'},
               {'fg':'darkblue',   'bg':'orange'},
               {'fg':'orange',     'bg':'darkblue'},
               {'fg':'black',      'bg':'white'}]

class MyText(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack(expand=YES, fill=BOTH)       # Text pack in Frame??? NO ,frame pack in parents
        self.make_widgets()

    def make_widgets(self):
        self.make_frame()
        self.make_context_menu()
        self.text.bind('<Button-3>', self.popup_context_menu)

    def make_frame(self):
        v_bar = Scrollbar(self)
        h_bar = Scrollbar(self, orient='horizontal')
        text = Text(self, relief=SUNKEN,
                    font=start_font, wrap='none')

        v_bar.config(command=text.yview)
        h_bar.config(command=text.xview)
        text.config(yscrollcommand=v_bar.set)
        text.config(xscrollcommand=h_bar.set)

        v_bar.pack(side=RIGHT, fill=Y)
        h_bar.pack(side=BOTTOM, fill=X)
        text.pack(side=LEFT, fill=BOTH, expand=YES)
        text.config(undo=1, autoseparators=1)
        self.text = text

    def make_context_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label='Cut', command=self.on_cut)
        menu.add_command(label='Copy', command=self.on_copy)
        menu.add_command(label='Paste', command=self.on_paste)
        menu.add_command(label='Delete', command=self.on_delete)
        self.context_menu = menu

    def popup_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def set_text(self, text=''):
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.edit_reset()
        self.text.edit_modified(0)
        self.text.focus()

    def edit_modified(self, number=None):
        return self.text.edit_modified(number)

    def get_text(self):
        return self.text.get('1.0', END+'-1c')

    def on_undo(self):
        try:
            self.text.edit_undo()
        except TclError:
            showinfo(WIN_TITLE, 'Nothing to undo')

    def on_redo(self):
        try:
            self.text.edit_redo()
        except TclError:
            showinfo(WIN_TITLE, 'Nothing to undo')

    def on_my_undo(self):
        try:
            self.text.edit_undo()
        except TclError:
            showinfo(WIN_TITLE, 'Nothing to redo')

    def on_copy(self):
        print('no_copy')
        if not self.text.tag_ranges(SEL):            # ???
            showerror(WIN_TITLE, 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)

    def on_delete(self):
        if not self.text.tag_ranges(SEL):
            showerror(WIN_TITLE, 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    def on_cut(self):
        if not self.text.tag_ranges(SEL):
            showerror(WIN_TITLE, 'No text selected')
        else:
            self.on_copy()
            self.on_delete()

    def on_paste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')             # ???
        except TclError:
            showerror(WIN_TITLE, 'Nothing to paste')
            return None
        self.text.insert(INSERT, text)
        self.text.tag_remove(SEL, '1.0', END)
        self.text.see(INSERT)

    def on_select_all(self):
        self.text.tag_add(SEL, '1.0', END+'-1c')
        self.text.mark_set(INSERT, '1.0')
        self.text.see(INSERT)

    def on_goto(self, force_line_number=None):
        max_index = self.text.index(END+'-1c')
        max_line = int(max_index.split('.')[0])
        text = 'Please input a integer in range(1, %s)' % max_line
        line_number = force_line_number or askinteger('PyEditor', text)
        self.text.update()
        self.text.focus()
        if line_number is not None:
            if 0 < line_number <= max_line:
                print(line_number)
                self.text.mark_set(INSERT, '%d.0' % line_number)
                print(self.text.index(INSERT))
                self.text.tag_remove(SEL, '1.0', END)
                self.text.tag_add(SEL, INSERT, INSERT + '+1l')        #  1L
                self.text.see(INSERT)
            else:
                showerror(WIN_TITLE, 'Bad number')

    def on_find(self, force_word=None, **kwargs):
        key_word = force_word or askstring('PyEdit', 'Please input a string')
        if key_word:
            self.text.focus()
            match_count = 0
            self.text.tag_remove(SEL, '1.0', END)
            where = self.text.search(key_word, INSERT, END, **kwargs)
            print(where)
            while where:
                print(where)
                match_count += 1
                self.text.see(where)
                new_insert = where + '+%dc' % len(key_word)
                self.text.tag_add(SEL, where, new_insert)
                self.text.mark_set(INSERT, new_insert)
                self.text.update()
                where = self.text.search(key_word, INSERT, END, **kwargs)
            if match_count == 0:
                showinfo(WIN_TITLE, 'Can not find %s' % key_word)

    def my_on_delete(self):
        if self.text.tag_ranges(SEL):
            self.text.delete(SEL_FIRST, SEL_LAST)
        else:
            showerror(WIN_TITLE, 'No text selected')

    def on_set_font(self, force_font=None):
        font = force_font
        if font is None:
            font = fonts_list[0]
            fonts_list.append(fonts_list[0])
            del fonts_list[0]
        self.text.config(font=font)

    def on_set_bg(self, force_bg=None):
        bg = force_bg or askcolor()[1]
        if bg:
            self.text.config(bg=bg)

    def on_set_fg(self, force_fg=None):
        fg = force_fg or askcolor()[1]
        if fg:
            self.text.config(fg=fg)

    def on_color_list(self):
        color = colors_list[0]
        colors_list.append(colors_list[0])
        del colors_list[0]
        self.text.config(fg=color['fg'], bg=color['bg'])

    def on_info(self):
        text = self.get_text()
        bytes = len(text)
        lines = len(text.split('\n'))
        print(lines)
        words = len(text.split())
        index = self.text.index(INSERT)
        where = tuple(index.split('.'))
        info = ('Current location:\n\n' +
                'line:\t{0[0]}\n'.format(where) +
                'column:\t{0[1]}\n\n'.format(where) +
                'File text statistics:\n\n' +
                'chars:\t{0}\n'.format(bytes) +
                'lines:\t{0}\n'.format(lines) +
                'words:\t{0}\n'.format(words))
        print(info)
        showinfo('PyEdit Information',info)


if __name__ == '__main__':
    root = Tk()
    text = MyText(root)
    text.set_text('天生我材必有用')
    text.pack()
    print([ i for i in dir(MyText) if i.startswith('on')])
    mainloop()

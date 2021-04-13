import tkinter as tk
import time
import random

# Read example text and save as data variable
with open('some_text.txt', 'r', encoding='utf8') as text:
    data = text.readlines()
text.close()

# index is a number of character from our data to write by user


class Application:
    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry('750x485')
        self.app.bind('<KeyPress>', self.pressed_key)
        self.app.bind('<FocusIn>', self.clear_widget)
        self.index, self.mistakes, self.start, self.start, self.write_time, = None, None, None, None, None
        self.sentence, self.random_number = None, None
        self.sentence_to_write = tk.Text(self.app)
        self.sentence_to_write.grid(column=0, row=1, columnspan=2, padx=(50, 0), pady=(20, 20))
        self.sentence_to_write.configure(height=10)
        self.user_entry_text = tk.Text(self.app)
        self.user_entry_text.grid(column=0, row=3, columnspan=2, padx=(50, 0), pady=(20, 20))
        self.user_entry_text.configure(height=10)
        self.time_label = tk.Label(self.app, text='WPM:')
        self.time_label.grid(column=0, row=2, sticky='E')
        self.wpm_label = tk.Label(self.app, text=0)
        self.wpm_label.grid(row=2, column=1, sticky='W')
        self.app.title('Typing speed test')
        self.title_label = tk.Label(text='Typing Speed Test')
        self.title_label.grid(column=0, row=0, columnspan=2)
        self.exit_button = tk.Button(self.app, text="Exit", command=self.app.destroy)
        self.exit_button.grid(row=4, column=1)
        self.restart_button = tk.Button(self.app, text="Restart", command=self.new_game)
        self.restart_button.grid(row=4, column=0)
        self.new_game()
        self.app.mainloop()

# Refresh (words per minute)wpm every 1 second when user will start writing
    def refresh_cpm(self):
        if self.start != 0:
            self.write_time = time.time() - self.start
            try:
                self.wpm_label.config(text=f'{(int(len(self.sentence) / self.write_time) / 5 * 60)}')
            except ZeroDivisionError:
                pass
        self.app.after(1000, self.refresh_cpm)

# Clear label information text after focus on it
    def clear_widget(self, event):
        if self.user_entry_text == self.app.focus_get() and\
                self.user_entry_text.get('1.0', 'end-1c') == 'Type the words here':
            self.user_entry_text.delete('1.0', tk.END)

# Prepare new test by set variables and new random sentence. Random sentence is 3 next lines from our data
    def new_game(self):
        self.app.bind('<FocusIn>', self.clear_widget)
        self.user_entry_text.config(background='white')
        self.index, self.mistakes, self.start, self.start, self.write_time = 0, 0, 0, 0, 0
        self.sentence = ''
        self.random_number = random.randint(0, len(data) - 3)
        self.sentence_to_write.configure(state='normal')
        self.sentence_to_write.delete('1.0', tk.END)
        self.sentence_to_write.insert('end', f'{data[self.random_number]}')
#         self.sentence_to_write.insert('end', f'{data[self.random_number]}{data[self.random_number+1]}'
#                                              f'{data[self.random_number + 2]}')
        self.sentence_to_write.configure(state='disabled')
        self.user_entry_text.delete('1.0', tk.END)
        self.user_entry_text.insert('end', 'Type the words here')
        self.refresh_cpm()

    def pressed_key(self, event):
        self.sentence = self.sentence_to_write.get("1.0", 'end-1c')
        self.check_letter(event)

    # Symbol keys like ;/?/ /,/. etc. are determined by words semicolon/question/space/comma/period etc.
    def check_symbols(self, key, character):
        if (key == 'space' and character == ' ') or\
            (key == 'question' and character == '?') or\
                (key == 'comma' and character == ',') or\
                (key == 'period' and character == '.') or\
                (key == 'colon' and character == ':') or\
                (key == 'semicolon' and character == ';') or\
                (key == 'Return' and character == '\n') or\
                (key == 'quoteright' and character == '\'') or\
                (key == 'exclam' and character == '!'):
            return True
        else:
            return False

    # check what character user push at keyboard
    def check_letter(self, key):

        # Check if it is a letter or symbol key
        # We need to check if index is not bigger then sentence to avoid IndexError
        if self.index < len(self.sentence) and\
                (key.keysym == self.sentence[self.index] or self.check_symbols(key.keysym, self.sentence[self.index])):
            # When user is starting typing and he write first letter correct we want to start our timer.
            if self.index == 0 and key.keysym == self.sentence[0]:

                self.user_entry_text.config(background='white')
                self.index += 1
                self.start_timer()
            # When user hit last letter we automatically stop the counter.
            elif self.index + 2 == len(self.sentence) and (self.check_symbols(key.keysym, self.sentence[self.index])):
                self.user_entry_text.config(background='white')
                self.stop_timer()
            # Even if letter is wrong we want improve index.
            else:
                self.user_entry_text.config(background='white')
                self.index += 1
                if self.index + 1 == len(self.sentence):
                    self.stop_timer()
        elif key.keysym == 'BackSpace':
            if self.index > 0:
                self.index -= 1
        # When user want to capitalize letter and he need to use shift we don't want to do anything
        elif key.keysym == 'Shift_L' or key.keysym == 'Shift_R' or key.keysym == 'ALT_R':
            pass
        # Every time when user make a mistake we want to give him information and we changing background color
        elif len(key.keysym) == 1 or\
                key.keysym == 'space' or\
                key.keysym == 'question' or\
                key.keysym == 'comma' or\
                key.keysym == 'period' or\
                key.keysym == 'colon' or\
                key.keysym == 'semicolon' or\
                key.keysym == 'Return' or\
                key.keysym == 'quoteright' or\
                key.keysym == 'exclam':
            self.user_entry_text.config(background='red')
            self.mistakes += 1
            self.index += 1
        else:
            pass

    def start_timer(self):
        self.start = time.time()

    def stop_timer(self):
        self.new_game()


if __name__ == '__main__':
    root = Application()

from Sudoku import Sudoku
from Point import Point
import Tkinter
import ttk
import tkFont

# TODO
# 1. what should I do when the game is over?
#      - color every button a different color?
#      - disable all the buttons?
# 3. Bug ... should never be able to click on something that has 0 choices!


class GameGUI(Sudoku):
    def __init__(self, num_rows, num_columns):
        super(GameGUI, self).__init__()

        self.num_rows = num_rows
        self.num_columns = num_columns

        self._buttons = []

        self.gui_window = Tkinter.Tk()
        self.gui_window.title("Sudoku")
        self.gui_window.resizable(width=False, height=False)

        self.my_font = tkFont.Font(family="Helvetica", size=36, weight='bold')
        self._create_grid_gui()

        self.center_window(self.gui_window)

    def center_window(self, window):
        window.update_idletasks()
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        print "Screen: {} {}".format(screen_w, screen_h)
        window_w = window.winfo_width()
        window_h = window.winfo_height()
        print "Window: {} {}".format(window_w, window_h)
        top_left_x = screen_w/2.0 - window_w/2.0
        top_left_y = screen_h/2.0 - window_h/2.0
        print "X Y: {} {}".format(top_left_x, top_left_y)
        window.geometry("+%d+%d" % (top_left_x, top_left_y))

    def _create_grid_gui(self):
        for row in range(self.num_rows):
            self._buttons.append([])
            for column in range(self.num_columns):
                temp_button = Tkinter.Button(
                    self.gui_window,
                    height=1,
                    width=2,
                    font=self.my_font,
                    text=self._grid[row][column].get_value(),
                    state='normal' if self._grid[row][column].get_modifiable() else 'disabled',
                    command=lambda x=row, y=column: self.button_clicked(x, y),
                    bg='grey' if self._grid[row][column].get_modifiable() else 'white',
                )
                # http://stackoverflow.com/questions/35412290/change-button-colour-when-hovering-over-with-tkinter
                # if self._grid[row][column].get_modifiable():
                #     temp_button.bind("<Enter>", lambda event, tb=temp_button: tb.configure(bg="white"))
                #     temp_button.bind("<Leave>", lambda event, tb=temp_button: tb.configure(bg="maroon"))
                temp_button.grid(row=row, column=column)

                self._buttons[-1].append(temp_button)

    def process_red_buttons(self):
        for row_buttons in self._buttons:
            for button in row_buttons:
                if button['bg'] == 'red' and button['state'] == 'disabled':
                    button['bg'] = 'grey'
                    button['state'] = 'normal'
        for point in self.get_points_with_no_options():
            self._buttons[point.get_x()][point.get_y()]['bg'] = 'red'
            self._buttons[point.get_x()][point.get_y()]['state'] = 'disabled'

    def disable_all_buttons(self):
        for row_buttons in self._buttons:
            for button in row_buttons:
                button['state'] = 'disabled'

    def enable_all_modifiable_buttons_buttons(self):
        for row_index, row_buttons in enumerate(self._buttons):
            for col_index, button in enumerate(row_buttons):
                button['state'] = 'normal' if self.get_point(Point(row_index, col_index)).get_modifiable() else 'disabled'

    def column_selected(self, column):
        self.enable_all_modifiable_buttons_buttons()
        self.set_point(Point(self.current_row_num, self.current_column_num, self.current_available_string_numbers[column], True))
        self._buttons[self.current_row_num][self.current_column_num]['text'] = self.current_available_string_numbers[column]
        self._buttons[self.current_row_num][self.current_column_num]['bg'] = 'green'
        self.select_number_window.destroy()

        self.process_red_buttons()

    def _create_number_options(self):
        for column_num, available_number in enumerate(self.current_available_string_numbers):
            print "available_number:", available_number
            temp_button = Tkinter.Button(
                self.select_number_window,
                height=5,
                width=10,
                font=self.my_font,
                text=available_number,
                state='normal',
                command=lambda column=column_num: self.column_selected(column),
            )
            temp_button.grid(row=1, column=column_num)

    def button_clicked(self, row_num, column_num):
        self.disable_all_buttons()
        self.current_row_num = row_num
        self.current_column_num = column_num
        print "row num:", self.current_row_num
        print "col num:", self.current_column_num
        print ""

        self._buttons[self.current_row_num][self.current_column_num]['bg'] = 'blue'
        print "CURRENT VALUE:", self.get_point(Point(self.current_row_num, self.current_column_num)).get_value()
        if self.get_point(Point(self.current_row_num, self.current_column_num)).get_value():
            self.set_point(Point(x=self.current_row_num, y=self.current_column_num, value='', modifiable=True))
            self._buttons[self.current_row_num][self.current_column_num]['text'] = ''
            self.process_red_buttons()
            self.enable_all_modifiable_buttons_buttons()
            return
        available_numbers_set = self.get_available_numbers(self.current_row_num, self.current_column_num)

        self.current_available_string_numbers = []
        for available_number in available_numbers_set:
            self.current_available_string_numbers.append(available_number)
        self.current_available_string_numbers.sort()

        self.select_number_window = Tkinter.Tk()
        self.select_number_window.title("Choose a number!")
        self._create_number_options()
        self.center_window(self.select_number_window)

def main():
    game_gui = GameGUI(Sudoku.SQUARE_SIDE, Sudoku.SQUARE_SIDE)
    Tkinter.mainloop()

if __name__ == '__main__':
    main()

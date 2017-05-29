import tkinter

gui_window = tkinter.Tk()

class GameGUI():
    def __init__(self, num_rows, num_columns):
        self.num_rows = num_rows
        self.num_columns = num_columns

        self._frames = []
        self._buttons = []
        self._create_grid_gui()

    def _create_grid_gui(self):
        for row in range(self.num_rows):
            self._buttons.append([])
            for column in range(self.num_columns):
                # temp_button = tkinter.Button(gui_window)
                temp_button = tkinter.Button(
                    gui_window,
                    height=10,
                    width=10,
                    text='',
                    # command=self.foo
                    command=lambda x=row, y=column: self.button_clicked(x, y),
                )
                temp_button.grid(row=row, column=column)

                self._buttons[-1].append(temp_button)

        # quit button
        tkinter.Button(
            gui_window,
            fg='red',
            bg='green',
            text='QUIT',
            command=lambda : gui_window.destroy()
        ).grid(row = 3, column = 1)

    def button_clicked(self, row_num, column_num):
        print ("{} {}".format(row_num, column_num))

        if not self._buttons[row_num][column_num]['text']:
            self._buttons[row_num][column_num]['text'] = 'X'
            # HOW TO DISABLE A BUTTON
            # self._buttons[row_num][column_num]['state'] = 'disabled'
        elif self._buttons[row_num][column_num]['text'] == 'X':
            self._buttons[row_num][column_num]['text'] = 'O'
        elif self._buttons[row_num][column_num]['text'] == 'O':
            self._buttons[row_num][column_num]['text'] = ''

def main():
    TIC_TAC_TOE_NUM_ROWS = 3
    TIC_TAC_TOE_NUM_COLUMNS = 3
    game_gui = GameGUI(TIC_TAC_TOE_NUM_ROWS, TIC_TAC_TOE_NUM_COLUMNS)
    tkinter.mainloop()

if __name__ == '__main__':
    main()

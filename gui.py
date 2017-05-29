import Tkinter

gui_window = Tkinter.Tk()

#################################################################
# change these two variables to create an arbitrarily sized grid
num_rows = 3
num_columns = 2
#################################################################

# create frames
frames = []
for _ in xrange(num_rows):
    frames.append(Tkinter.Frame(gui_window))

# define the ONE button call button callback function
#     - receives 2 arguments: x and y
#     - arguments correspond to the button's location in the GUI grid
def button_callback(x, y):
    print "{} {}".format(x, y)

# create buttons
buttons = []
for row_index, frame in enumerate(frames):
    for column_index in xrange(num_columns):
        buttons.append(
            Tkinter.Button(
                frame,
                height=5,
                width=10,
                text="   row={} col={}   ".format(row_index, column_index),
                command=lambda x=row_index, y=column_index: button_callback(x, y)
            )
        )
        buttons[-1].pack(side='left', expand=True, fill='both')
    frame.pack(expand=True, fill='both')

Tkinter.mainloop()

import tkinter as tk

# variables & constants
ROWS = 3
COLS = 2
state = 0
color_mapping = [
    [['red','gray','gray'], ['red','gray','gray']],
    [['gray','gray','green'], ['red','gray','gray']],
    [['gray','yellow','gray'], ['red','gray','gray']],
    [['red','gray','gray'], ['red','gray','gray']],
    [['red','gray','gray'], ['gray','gray','green']],
    [['red','gray','gray'], ['gray','yellow','gray']],
] # state, col (light: A,B), row (top, middle, bottom)
STANDARD_TIME_UNIT = 1000 # ms
time_cycle = [int(time * STANDARD_TIME_UNIT) for time in [2, 5, 3, 2, 5, 3]] # note loops in green light until sensor is active
sensors_active = [False, False]

window = tk.Tk()

frames = []
for i in range(ROWS):
    temp = []
    for j in range(COLS):
        frame = tk.Frame(
            master=window,
            relief=tk.GROOVE,
            borderwidth=12,
            width=94,
            height=94,
            bg=color_mapping[state][j][i]
        )
        frame.grid(row=i, column=j, padx=5, pady=0)
        temp.append(frame)
    frames.append(temp)
panel = tk.Frame(master=window, width=100, height=100)
label = tk.Label(master=panel, text="Press 'a' or 'b' key!")
label.pack()
label_state = tk.Label(master=panel, text="State: {}".format(state))
label_state.pack()
label_sensors_active = tk.Label(master=panel, text="Sensors active: {}, {}".format(str(sensors_active[0])[:1], str(sensors_active[1])[:1]))
label_sensors_active.pack()
# panel.place(x=205, y=0)
panel.grid(row=0, column=2, rowspan=3, padx=5, pady=0)
        
def handle_keypress(event):
    """Print the character associated to the key pressed"""
    global state
    if event.char == 'a':
        sensors_active[0] = True
    elif event.char == 'b':
        sensors_active[1] = True
    label_sensors_active.configure(text="Sensors active: {}, {}".format(str(sensors_active[0])[:1], str(sensors_active[1])[:1]))
    print(event.char)

def next_state():
    global state
    if state == 1 or state == 4:
        if state == 1:
            if sensors_active[0]:
                sensors_active[0] = False
                label_sensors_active.configure(text="Sensors active: {}, {}".format(str(sensors_active[0])[:1], str(sensors_active[1])[:1]))
                if not sensors_active[1]:
                    window.after(time_cycle[state], next_state)
                    return
        if state == 4:
            if sensors_active[1]:
                sensors_active[1] = False
                label_sensors_active.configure(text="Sensors active: {}, {}".format(str(sensors_active[0])[:1], str(sensors_active[1])[:1]))
                if not sensors_active[0]:
                    window.after(time_cycle[state], next_state)
                    return
    state = (state + 1) % len(color_mapping)
    for i in range(ROWS):
        for j in range(COLS):
            frames[i][j].configure(bg=color_mapping[state][j][i])
    label_state.configure(text="State: {}".format(state))
    label_sensors_active.configure(text="Sensors active: {}, {}".format(str(sensors_active[0])[:1], str(sensors_active[1])[:1]))
    window.update()
    window.after(time_cycle[state], next_state)

# Bind keypress event to handle_keypress()
window.bind("<a>", handle_keypress)
window.bind("<b>", handle_keypress)
window.bind("<n>", handle_keypress)

window.after(int(time_cycle[state]), next_state)

window.mainloop()
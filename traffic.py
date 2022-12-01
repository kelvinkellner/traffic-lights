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
frames_label = []
for i in range(ROWS):
    temp = []
    temp2 = []
    for j in range(COLS):
        frame1 = tk.Frame(
            master=window,
            width=94,
            height=94,
            bg='gray'#color_mapping[state][j][ROWS-i-1] if j % 2 == 0 else color_mapping[state][j][i]
        )
        frame2 = tk.Frame(
            master=window,
            width=94,
            height=94,
            bg='gray'#color_mapping[state][j][i] if j % 2 == 0 else color_mapping[state][j][ROWS-i-1]
        )
        if j%2 == 0:
            label1 = tk.Label(master=frame1, text="A", width=8, height=4,
            relief=tk.GROOVE,
            borderwidth=12, bg=color_mapping[state][j][ROWS-i-1] if j % 2 == 0 else color_mapping[state][j][i])
            label2 = tk.Label(master=frame2, text="A", width=8, height=4,
            relief=tk.GROOVE,
            borderwidth=12, bg=color_mapping[state][j][i] if j % 2 == 0 else color_mapping[state][j][ROWS-i-1])
            label1.pack()
            label2.pack()
            frame1.grid(row=1+i, column=j, padx=5, pady=5)
            frame2.grid(row=1+i, column=4+j, padx=5, pady=5)
        else:
            label1 = tk.Label(master=frame1, text="B", width=8, height=4,
            relief=tk.GROOVE,
            borderwidth=12, bg=color_mapping[state][j][ROWS-i-1] if j % 2 == 0 else color_mapping[state][j][i])
            label2 = tk.Label(master=frame2, text="B", width=8, height=4,
            relief=tk.GROOVE,
            borderwidth=12, bg=color_mapping[state][j][i] if j % 2 == 0 else color_mapping[state][j][ROWS-i-1])
            label1.pack()
            label2.pack()
            frame1.grid(row=0, column=i+j, padx=5, pady=5)
            frame2.grid(row=4, column=i+j, padx=5, pady=5)
        temp.append(frame1)
        temp.append(frame2)
        temp2.append(label1)
        temp2.append(label2)
    frames.append(temp)
    frames_label.append(temp2)
panel = tk.Frame(master=window, width=100, height=100)
label = tk.Label(master=panel, text="Press the 'a' or 'b' key to activate traffic sensors!")
label.pack()
label_state = tk.Label(master=panel, text="State: S{}".format(state))
label_state.pack()
label_sensors_active = tk.Label(master=panel, text="Sensors active...\nA: {:<5s}\nB: {:<5s}".format(str(sensors_active[0]).upper(), str(sensors_active[1]).upper()))
label_sensors_active.pack()
print(frames)
panel.grid(row=2, column=1, columnspan=3, padx=0, pady=0)
        
def handle_keypress(event):
    """Print the character associated to the key pressed"""
    global state
    if event.char == 'a':
        sensors_active[0] = True
    elif event.char == 'b':
        sensors_active[1] = True
    label_sensors_active.configure(text="Sensors active...\nA: {:<5s}\nB: {:<5s}".format(str(sensors_active[0]).upper(), str(sensors_active[1]).upper()))
    print(event.char)

def next_state():
    global state
    if state == 1 or state == 4:
        if state == 1:
            if sensors_active[0]:
                sensors_active[0] = False
                label_sensors_active.configure(text="Sensors active...\nA: {:<5s}\nB: {:<5s}".format(str(sensors_active[0]).upper(), str(sensors_active[1]).upper()))
                if not sensors_active[1]:
                    window.after(time_cycle[state], next_state)
                    return
        if state == 4:
            if sensors_active[1]:
                sensors_active[1] = False
                label_sensors_active.configure(text="Sensors active...\nA: {:<5s}\nB: {:<5s}".format(str(sensors_active[0]).upper(), str(sensors_active[1]).upper()))
                if not sensors_active[0]:
                    window.after(time_cycle[state], next_state)
                    return
    state = (state + 1) % len(color_mapping)
    for i in range(ROWS):
        for j in range(COLS):
            # frames[i][(j*2)+0].configure(bg=color_mapping[state][j][ROWS-i-1] if j % 2 == 0 else color_mapping[state][j][i])
            # frames[i][(j*2)+1].configure(bg=color_mapping[state][j][i] if j % 2 == 0 else color_mapping[state][j][ROWS-i-1])
            frames_label[i][(j*2)+0].configure(bg=color_mapping[state][j][ROWS-i-1] if j % 2 == 0 else color_mapping[state][j][i])
            frames_label[i][(j*2)+1].configure(bg=color_mapping[state][j][i] if j % 2 == 0 else color_mapping[state][j][ROWS-i-1])
    label_state.configure(text="State: S{}".format(state))
    label_sensors_active.configure(text="Sensors active...\nA: {:<5s}\nB: {:<5s}".format(str(sensors_active[0]).upper(), str(sensors_active[1]).upper()))
    window.update()
    window.after(time_cycle[state], next_state)

# Bind keypress event to handle_keypress()
window.bind("<a>", handle_keypress)
window.bind("<b>", handle_keypress)
window.bind("<n>", handle_keypress)

window.after(int(time_cycle[state]), next_state)

window.mainloop()
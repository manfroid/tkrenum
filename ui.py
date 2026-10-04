import tkinter as tk


def tkNumberEntry(master, min=0, *args, **kwargs):
    def key_pressed(event, tv):
        if tv:
            value = int(tv.get() or str(min))
            if event.keysym == "Up":
                tv.set(str(value + 1))
            elif event.keysym == "Down" and value > min:
                tv.set(str(value - 1))

    def _validate(P):
        return P.isdigit() or P == ""

    tv = kwargs["textvariable"]
    entry = tk.Entry(master,
                     validate="key",
                     validatecommand=(master.register(_validate), "%P"),
                     *args,
                     **kwargs
                     )
    # entry.bind("<Key>", lambda event, tk_sv=tv: key_pressed(event, tk_sv))
    entry.bind("<Key>", lambda event: key_pressed(event, tv))
    return entry

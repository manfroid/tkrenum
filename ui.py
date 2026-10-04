import tkinter as tk


def tkNumberEntry(master: tk.Misc, min: int = 0, *args, **kwargs):
    def _key_pressed(event: tk.Event, tv: tk.StringVar) -> None:
        """Let Arrow up and down increment and decrement value, respectively"""
        if tv:
            value = int(tv.get() or str(min))
            if event.keysym == "Up":
                tv.set(str(value + 1))
            elif event.keysym == "Down" and value > min:
                tv.set(str(value - 1))

    def _validate(P) -> bool:
        """Validate input: permit digits and empty string for deletion"""
        return P.isdigit() or P == ""

    entry = tk.Entry(master,
                     validate="key",
                     validatecommand=(master.register(_validate), "%P"),
                     *args,
                     **kwargs)

    # install keyboard input handler for entry
    tv = kwargs["textvariable"]
    entry.bind("<Key>", lambda event: _key_pressed(event, tv))

    return entry

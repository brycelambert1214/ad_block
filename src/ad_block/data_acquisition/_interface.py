import tkinter as tk


class _Interface:
    """User interface for event confirmation."""

    def get_event_confirmation(self) -> bool | None:
        """Display an event confirmation popup and wait for a response."""

        result = {"value": None}

        root = tk.Tk()
        root.title("Event Detected")
        root.geometry("300x150")

        # Keep the popup above other windows and request keyboard focus.
        root.attributes("-topmost", True)
        root.lift()
        root.focus_force()

        # Request focus again after the window has been displayed.
        root.after(100, root.focus_force)

        label = tk.Label(
            root,
            text="Was an event detected?",
            font=("Arial", 14),
        )
        label.pack(pady=20)

        button_frame = tk.Frame(root)
        button_frame.pack()

        def yes():
            result["value"] = True
            root.destroy()

        def no():
            result["value"] = False
            root.destroy()

        yes_button = tk.Button(
            button_frame,
            text="Yes",
            command=yes,
            width=10,
        )
        yes_button.pack(side=tk.LEFT, padx=10)

        no_button = tk.Button(
            button_frame,
            text="No",
            command=no,
            width=10,
        )
        no_button.pack(side=tk.LEFT, padx=10)

        root.bind("<y>", lambda _: yes())
        root.bind("<Y>", lambda _: yes())
        root.bind("<n>", lambda _: no())
        root.bind("<N>", lambda _: no())

        root.mainloop()

        return result["value"]


if __name__ == "__main__":
    interface = _Interface()
    print(interface.get_event_confirmation())
# import tkinter
from tkinter import *
from typing import List, Tuple

def main():
    # init window with paint title and size 800x500
    window = Tk()
    window.title("Paint")
    window.geometry("800x500")
    window.state("normal")
    window.resizable(width=False, height=False)
    app = Paint(window)
    app.mainloop()

class Paint:
    def __init__(self, root: Tk) -> None:
        if not isinstance(root, Tk):
            raise TypeError("root must be a Tk instance")
        self.root: Tk = root
        self.initUI()
        self.color_picker()
        self.thick_picker()

    current_x: int = 0
    current_y: int = 0
    pencil_color: str = 'black'
    pencil_thickness: int = 10
    lines_ids: List[int] = []

    def set_pencil_color(self, color: str) -> None:
        self.pencil_color = color

    def set_pencil_thickness(self, thickness: int or str) -> None:
        """
        Sets the thickness of the pencil
        """
        self.pencil_thickness = thickness

    def initUI(self) -> None:
        # create a canvas to draw on and attach it to the window
        self.canvas = Canvas(self.root, bg="white", width=800, height=450)
        self.canvas.pack(fill=BOTH) # expand to fill window and fill both directions
        self.canvas.bind('<Button-1>', self.locate_xy)
        self.canvas.bind("<B1-Motion>", self.paint) # bind paint when mouse is clicked and dragged
        # self.canvas.bind("<Button-3>", self.choose_color) # bind choose color event to canvas

        # create a button to delete the drawing on the window
        self.delete_button = Button(self.root, text="🗑️", command=self.delete)
        self.undo_button = Button(self.root, text="⬅️", command=self.undo)
        self.delete_button.pack(side=LEFT, padx=5, pady=5)
        self.undo_button.pack(side=LEFT, padx=5, pady=5)

    def thick_picker(self) -> None:
        self.thickness_oval((3, 198, 5, 200), fill="black", width=2)
        self.thickness_oval((10, 195, 20, 205), fill="black", width=10)
        self.thickness_oval((25, 192.5, 40, 207.5), fill="black", width=15)
        self.thickness_oval((45, 190, 65, 210), fill="black", width=20)

    # display color picker
    def color_picker(self) -> None:
        """
        Create a color picker side window
        """
        # Left
        self.color_box((10, 10, 30, 30), fill="white")
        self.color_box((10, 40, 30, 60), fill="#525252")
        self.color_box((10, 70, 30, 90), fill="#ff0000")
        self.color_box((10, 100, 30, 120), fill="#48ff00")
        self.color_box((10, 130, 30, 150), fill="#00c3ff")
        self.color_box((10, 160, 30, 180), fill="#7b00ff")

        # Right
        self.color_box((40, 10, 60, 30), fill='#b5b5b5')
        self.color_box((40, 40, 60, 60), fill="black")
        self.color_box((40, 70, 60, 90), fill="#ffc400")
        self.color_box((40, 100, 60, 120), fill="#00ffc8")
        self.color_box((40, 130, 60, 150), fill="#0033ff")
        self.color_box((40, 160, 60, 180), fill="#f200ff")

    def thickness_oval(self, position: List[int] or Tuple[int], fill: str, width: int or str) -> None:
        id = self.canvas.create_oval(position, fill=fill)
        self.canvas.tag_bind(id, '<Button-1>', lambda x: self.set_pencil_thickness(width))

    def color_box(self, position: List[int] or Tuple[int], fill: str) -> None:
        """
        Creates a box with the given color and position
        and then creates a bind to set the pencil color
        to the color of the box when clicked
        """
        id = self.canvas.create_rectangle(position, fill=fill)
        self.canvas.tag_bind(id, '<Button-1>', lambda x: self.set_pencil_color(fill))



    def mainloop(self) -> None:
        self.root.mainloop()

    def locate_xy(self, event: Event) -> None:
        """
        locates the x and y coordinates of the mouse
        """
        self.current_x = event.x
        self.current_y = event.y
        # print(self.current_x, self.current_y)

    def paint(self, event: Event) -> None:
        """
        Paints the line when the mouse is moved
        """
        id = self.canvas.create_oval(self.current_x, self.current_y, event.x, event.y, outline=self.pencil_color, width=self.pencil_thickness)
        self.locate_xy(event)
        self.lines_ids.append(str(id))

    def delete(self) -> None:
        """
        Deletes the lines on the canvas
        """
        for id in self.lines_ids:
            self.canvas.delete(id)
    def undo(self) -> None:
        """
        Undoes the last line drawn
        """
        if len(self.lines_ids) > 0:
            self.canvas.delete(self.lines_ids[-1])
            self.lines_ids.pop()

if __name__ == "__main__":
    main()
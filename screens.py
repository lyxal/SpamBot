class Screen:
    def __init__(self, p_name, p_window):
        """
        Takes: Self, the name of the screen

        Does: Initialises the screen class

        Returns: Nothing
        """
        self.widgets = list()
        self.name = p_name
        self.window = p_window

    def add_item(self, p_widget, p_row, p_column):
        """
        Takes: Self, a tkinter widget, a row number and a column number

        Does: Adds the item to the list of widgets to show

        Returns: Nothing
        """
        self.widgets.append((p_widget, p_row, p_column))
        
    def show(self):
        for item in self.widgets:
            item[0].grid(row=item[1], column=item[2])
        self.window.title(self.name)
            
    def hide(self):
        for item in self.widgets:
            item[0].grid_forget()

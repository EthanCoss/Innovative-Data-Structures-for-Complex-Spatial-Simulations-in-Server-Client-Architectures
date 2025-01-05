import pyglet


class Shape:
    def __init__(self, type):
        self.type = type


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def get_pyglet_shape(self, x, y):
        return pyglet.shapes.Rectangle(
            x=x,
            y=y,
            width=self.width,
            height=self.height,
        )


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def get_pyglet_shape(self, x, y):
        return pyglet.shapes.Circle(x=x, y=y, radius=self.radius)

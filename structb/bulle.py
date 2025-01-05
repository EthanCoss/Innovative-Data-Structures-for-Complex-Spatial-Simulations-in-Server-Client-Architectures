from game.physics import Position
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math

import time

import cst

NB_CREA = [0]


class BaseBubble:

    def __init__(self, position: Position, radius: float):
        self.position = position
        self.radius = radius
        self.is_leaf = False
        self.creation_time = time.time()  # Servira d'ordre de priorité
        self.childrens = []
        self.parent = None
        self.layer = -1
        self.nb_crea = NB_CREA[0]
        NB_CREA[0] += 1

    def is_position_in_bubble(self, position: Position):
        return self.position.distance(position) < self.radius

    def is_bubble_in_bubble(self, bubble):
        return self.position.distance(bubble.position) + self.radius < bubble.radius

    def draw(self, ax, color="blue"):
        circle = Circle(
            (self.position.x, self.position.y), self.radius, fill=False, color=color
        )
        ax.add_patch(circle)

    def find_new_parent(self):
        current_bubble = self.parent
        current_bubble.remove_family_link(self)
        while current_bubble != None:
            if self.is_bubble_in_bubble(current_bubble):
                current_bubble.add_bubble_to_bubble_tree(self)
                return True
            current_bubble = current_bubble.parent
        return False

    def set_parent(self, parent):
        self.parent = parent
        self.update_layer(parent.layer + 1)

    def update_layer(self, layer):
        self.layer = layer
        for children in self.childrens:
            children.update_layer(layer + 1)


class BubbleTree(BaseBubble):

    def __init__(self, position: Position, radius: float):
        super().__init__(position, radius)
        self.linked_entity = None

    def add_children(self, children):
        children_radius = children.radius
        children_creation_time = children.creation_time
        if len(self.childrens) == 0:
            self.childrens.append(children)
            return True
        a = 0
        b = len(self.childrens)

        while a != b:
            pivot_ind = (b + a) // 2
            if self.childrens[pivot_ind].radius < children_radius:
                b = pivot_ind
            elif self.childrens[pivot_ind].radius > children_radius:
                a = pivot_ind + 1
            else:
                if self.childrens[pivot_ind].creation_time > children_creation_time:
                    b = pivot_ind
                else:
                    a = pivot_ind + 1

        self.childrens.insert(a, children)
        return True

    def remove_children(self, children):
        children_radius = children.radius
        children_creation_time = children.creation_time
        if not len(self.childrens):
            return False
        a = 0
        b = len(self.childrens) - 1

        while a != b:
            pivot_ind = (b + a) // 2
            if self.childrens[pivot_ind].radius < children_radius:
                b = pivot_ind - 1
            elif self.childrens[pivot_ind].radius > children_radius:
                a = pivot_ind + 1
            else:
                if self.childrens[pivot_ind].creation_time > children_creation_time:
                    b = pivot_ind
                else:
                    if self.childrens[pivot_ind] == children:
                        self.childrens.pop(pivot_ind)
                        return True
                    a = pivot_ind + 1

        if self.childrens[a] == children:
            self.childrens.pop(a)
            return True
        return False

    def add_bubble_to_bubble_tree(self, bubble: BaseBubble):
        for children in self.childrens:
            if not isinstance(children, Bubble) and bubble.is_bubble_in_bubble(
                children
            ):
                return children.add_bubble_to_bubble_tree(bubble)
        return self.add_family_link(bubble)

    def add_family_link(self, children):
        self.add_children(children)
        children.set_parent(self)

    def remove_family_link(self, children):
        self.remove_children(children)

    def move(self, position: Position):
        self.position = position
        for children in self.childrens:
            if not children.is_bubble_in_bubble(self):
                self.remove_family_link(children)
                children.find_new_parent()
        self.find_new_parent()

    def shake_tree(self):
        new_childrens = []

        while len(self.childrens) > 0:
            children = self.childrens.pop(0)
            if not isinstance(children, Bubble):
                pop_ind = []
                for children_test_ind in range(len(self.childrens)):
                    if self.childrens[children_test_ind].is_bubble_in_bubble(children):
                        pop_ind.append(children_test_ind)

                for poping_ind in range(len(pop_ind)):
                    children_test = self.childrens.pop(pop_ind[poping_ind] - poping_ind)
                    children.add_bubble_to_bubble_tree(children_test)

            new_childrens.append(children)
        self.childrens = new_childrens
        for children in self.childrens:
            if not isinstance(children, Bubble):
                children.shake_tree()

    def bubble_an_entity(self, entity):
        for children in self.childrens:
            if children.is_position_in_bubble(entity.position):
                return children.bubble_an_entity(entity)
        new_bubble = Bubble(entity.position, cst.BULLEAFRADIUS)
        self.add_bubble_to_bubble_tree(new_bubble)
        new_bubble.find_new_parent()
        return new_bubble.bubble_an_entity(entity)

    def link_an_entity(self, entity):
        self.linked_entity = entity

    def draw(self, ax, color="blue"):
        """Dessine la bubble et ses enfants."""
        super().draw(ax, color=color)  # Dessine la bubble actuelle
        for child in self.childrens:
            child.draw(ax, color="red")  # Dessine les enfants en rouge

    def __str__(self):
        return (
            "Arbre à Bubble de layer : "
            + str(self.layer)
            + " NB CREA "
            + str(self.nb_crea)
        )


class Bubble(BaseBubble):

    def __init__(self, position: Position, radius: float):
        super().__init__(position, radius)
        self.is_leaf = True
        self.entities = []

    def bubble_an_entity(self, entity):
        self.entities.append(entity)
        entity.link_bubble(self)
        return True

    def draw(self, ax, color="green"):
        """Dessine une bubble feuille."""
        super().draw(ax, color="green")

    def __str__(self):
        return "Bubble de layer : " + str(self.layer)


if __name__ == "__main__":
    """genesis_bubble = BubbleTree(Position(0, 0), radius=10**4)
    genesis_bubble.update_layer(0)

    ab = BubbleTree(position=Position(0, 0), radius=1000)

    genesis_bubble.add_bubble_to_bubble_tree(ab)

    b1 = Bubble(position=Position(0, 0), radius=cst.BULLEAFRADIUS)

    b2 = Bubble(position=Position(5000, 5000), radius=cst.BULLEAFRADIUS)

    genesis_bubble.add_bubble_to_bubble_tree(b1)
    genesis_bubble.add_bubble_to_bubble_tree(b2)

    print("a")

    ab.move(Position(500, 0))

    ab.move(Position(850, 0))

    ab.move(Position(-100, 0))"""
    genesis_bubble = BubbleTree(Position(0, 0), radius=10**4)
    genesis_bubble.update_layer(0)

    ab1 = BubbleTree(Position(0, 0), radius=1000)
    time.sleep(0.001)
    ab2 = BubbleTree(Position(0, 0), radius=1000)
    time.sleep(0.001)
    ab3 = BubbleTree(Position(0, 0), radius=1000)

    genesis_bubble.add_bubble_to_bubble_tree(ab2)
    genesis_bubble.add_bubble_to_bubble_tree(ab3)
    genesis_bubble.add_bubble_to_bubble_tree(ab1)

    assert genesis_bubble.childrens == [ab1, ab2, ab3]

    ab11 = BubbleTree(Position(0, 100), radius=990)
    ab22 = BubbleTree(Position(0, -100), radius=1010)

    genesis_bubble.add_bubble_to_bubble_tree(ab11)
    genesis_bubble.add_bubble_to_bubble_tree(ab22)

    assert genesis_bubble.childrens == [ab22, ab1, ab2, ab3, ab11]

    ab4 = BubbleTree(Position(0, 1000), radius=900)
    ab5 = BubbleTree(Position(-1000, 0), radius=950)
    ab6 = BubbleTree(Position(0, -1000), radius=975)

    genesis_bubble.add_bubble_to_bubble_tree(ab3)
    genesis_bubble.add_bubble_to_bubble_tree(ab4)
    genesis_bubble.add_bubble_to_bubble_tree(ab5)
    genesis_bubble.add_bubble_to_bubble_tree(ab6)

    b1 = Bubble(Position(0, 0), 100)

    genesis_bubble.add_bubble_to_bubble_tree(b1)

    assert b1.parent == ab22
    assert ab22.childrens == [b1]

    ab22.move(Position(5000, 3000))

    assert b1.parent == ab1

    ab11.move(Position(5000, 3000))
    ab1.move(Position(5000, 3000))
    ab2.move(Position(5000, 3000))
    ab3.move(Position(5000, 3000))

    print(b1.parent)

    assert b1.parent == genesis_bubble

    # genesis_bubble.shake_tree()

    fig, ax = plt.subplots()
    ax.set_xlim(-(10**4), 10**4)
    ax.set_ylim(-(10**4), 10**4)
    ax.set_aspect("equal", adjustable="box")

    genesis_bubble.draw(ax)

    plt.show()

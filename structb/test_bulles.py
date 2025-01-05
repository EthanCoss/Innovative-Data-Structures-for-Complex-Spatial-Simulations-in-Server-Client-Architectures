from bulle import Bubble, BubbleTree, BaseBubble
from game.physics import Position

import time


def test_create_genesis():
    genesis_bubble = BubbleTree(Position(100, 0), radius=10**4)
    genesis_bubble.update_layer(0)

    assert genesis_bubble.position.listify() == [100, 0]
    assert genesis_bubble.layer == 0
    assert len(genesis_bubble.childrens) == 0


def test_add_bubble():
    genesis_bubble = BubbleTree(Position(0, 0), radius=10**4)
    genesis_bubble.update_layer(0)

    ab = BubbleTree(Position(0, 0), radius=1000)
    assert ab.radius == 1000

    genesis_bubble.add_bubble_to_bubble_tree(ab)
    assert ab in genesis_bubble.childrens
    assert ab.layer == 1

    b = Bubble(position=Position(500, 100), radius=100)

    genesis_bubble.add_bubble_to_bubble_tree(b)
    assert b.parent == ab
    assert b.layer == 2
    assert b in ab.childrens
    assert not b in genesis_bubble.childrens


def test_move():
    genesis_bubble = BubbleTree(Position(0, 0), radius=10**4)
    genesis_bubble.update_layer(0)

    ab = BubbleTree(Position(0, 0), radius=1000)

    genesis_bubble.add_bubble_to_bubble_tree(ab)

    b = Bubble(position=Position(500, 0), radius=100)

    genesis_bubble.add_bubble_to_bubble_tree(b)

    ab.move(Position(-100, 0))

    assert ab.position.listify() == [-100, 0]

    assert b.parent == ab
    assert b.layer == 2
    assert b in ab.childrens
    assert not b in genesis_bubble.childrens

    ab.move(Position(-450, 0))

    assert b.parent == genesis_bubble
    assert b.layer == 1
    assert not b in ab.childrens
    assert b in genesis_bubble.childrens


def test_shake():
    genesis_bubble = BubbleTree(Position(0, 0), radius=10**4)
    genesis_bubble.update_layer(0)

    ab = BubbleTree(Position(0, 0), radius=1000)

    genesis_bubble.add_bubble_to_bubble_tree(ab)

    b = Bubble(position=Position(500, 0), radius=100)

    genesis_bubble.add_bubble_to_bubble_tree(b)

    ab.move(Position(-100, 0))

    assert ab.position.listify() == [-100, 0]

    ab.move(Position(-450, 0))

    ab.move(Position(0, 0))

    assert b.parent == genesis_bubble
    assert b.layer == 1
    assert not b in ab.childrens
    assert b in genesis_bubble.childrens

    genesis_bubble.shake_tree()

    assert b.parent == ab
    assert b.layer == 2
    assert b in ab.childrens
    assert not b in genesis_bubble.childrens


def test_multiple_bubbles():
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

    b2 = Bubble(Position(5000, 3000), 100)

    genesis_bubble.add_bubble_to_bubble_tree(b2)

    ab22.move(Position(5000, 3000))

    assert b2.parent == genesis_bubble

    assert b1.parent == ab1

    ab11.move(Position(5000, 3000))
    ab1.move(Position(5000, 3000))
    ab2.move(Position(5000, 3000))
    ab3.move(Position(5000, 3000))

    assert ab11.parent == ab22

    assert ab22.childrens == [ab1, ab2, ab3, ab11]

    assert b1.parent == genesis_bubble

    assert b2.parent == genesis_bubble

    genesis_bubble.shake_tree()

    assert b1.parent == genesis_bubble

    assert ab11.parent == ab1
    assert ab1.childrens == [ab11]
    assert ab2.childrens == [] and ab3.childrens == []
    assert ab2.parent == ab22 and ab3.parent == ab22 and ab1.parent == ab22
    assert b2.parent == ab11
    assert ab11.childrens == [b2]
    assert b2.layer == 4

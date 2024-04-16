# Вам дано описание пирамиды из кубиков в формате XML.
# Для каждого кубика известны его цвет, и известны кубики, расположенные прямо под ним.
# Введем понятие ценности для кубиков. Самый верхний кубик, соответствующий корню XML документа имеет ценность 1.
# Кубики, расположенные прямо под ним, имеют ценность 2.
# Кубики, расположенные прямо под нижележащими кубиками, имеют ценность 3. И т. д.
# Ценность цвета равна сумме ценностей всех кубиков этого цвета.
# Выведите через пробел три числа: ценности красного, зеленого и синего цветов.

from xml.etree import ElementTree


class Colors:
    def __init__(self):
        self.colors = {'red': 0, 'green': 0, 'blue': 0}
        self.root = ElementTree.fromstring(input())
        self.colors[self.root.attrib["color"]] += 1

    def get_children(self, tree, lvl=1):
        lvl += 1
        for child in tree:
            self.colors[child.attrib["color"]] += lvl
            self.get_children(child, lvl)

    def print_red_green_blue_values(self):
        for value in self.colors.values():
            print(value, end=" ")

    def main(self):
        self.get_children(self.root)
        self.print_red_green_blue_values()


if __name__ == '__main__':
    Colors().main()

# Sample input
# <cube color="blue"><cube color="red"><cube color="green"></cube></cube><cube color="red"></cube></cube>
# Output: 4 3 1

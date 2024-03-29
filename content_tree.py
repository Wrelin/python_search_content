from operator import attrgetter


class ContentTree:
    def __init__(self, parent=None, content=''):
        self.parent = parent
        self.children = []
        self.content = content
        self.weight = 0

    def add_child(self, child):
        self.children.append(child)

    def set_content(self, content):
        content = content.strip()
        if content:
            self.content = content
            self.update_weight(len(content))

    def update_weight(self, weight):
        self.weight += weight
        if self.parent:
            self.parent.update_weight(weight)

    def get_main_child(self):
        main_child = max(self.children, key=attrgetter('weight'))
        unnecessary_content = int(100 * (self.weight - main_child.weight) / self.weight)

        if unnecessary_content < 5:
            main_child = main_child.get_main_child()
        elif unnecessary_content > 30:
            main_child = self

        return main_child

    def get_content(self, content=''):
        if self.children:
            for child in self.children:
                content += child.get_content()
        else:
            content = self.content + '\n'

        return content

    def build_tree(cls, tree, source):
        for child in source.getchildren():
            tree_elem = ContentTree(tree)
            tree.add_child(tree_elem)
            if len(child):
                cls.build_tree(tree_elem, child)
            elif child.text:
                tree_elem.set_content(child.text)

    build_tree = classmethod(build_tree)

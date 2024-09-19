import os
import pathlib


class Tree:
    class Node:
        def __init__(self, name):
            self.name = name
            self.children = []

        def add_child(self, child):
            if child not in self.children:
                self.children.append(child)

        def __repr__(self, ):
            return str(self.name)

    def __init__(self, root_name, edges):
        self.edges = edges
        self.root = self._build_tree(root_name)
        self.tree_plot = ''

    def _build_tree(self, root_name):
        root = self.Node(root_name)
        for e in self.edges:
            if e[0] == root_name:
                root.add_child(self._build_tree(e[1]))
        return root

    def _tree(self, node, prefix=[]):
        space = '     '
        branch = '│   '
        tee = '├─ '
        last = '└─ '

        if len(prefix) == 0:
            self.tree_plot = ''

        self.tree_plot += ''.join(prefix) + str(node) + '\n'

        if len(prefix) > 0:
            prefix[-1] = branch if prefix[-1] == tee else space

        for i, e in enumerate(node.children):
            if i < len(node.children) - 1:
                self._tree(e, prefix + [tee])
            else:
                self._tree(e, prefix + [last])

        return self.tree_plot

    def __repr__(self):
        return self._tree(self.root)


def print_tree():
    print(f"The project has been init by PyPKG")
    edges = []
    for root, dirs, files in os.walk("."):
        dirs.sort()
        files.sort()
        if root.startswith(("./.idea", "./.vscode")):
            continue
        _dirname = os.path.split(os.path.abspath(root))[-1]
        for dir in dirs:
            if dir in (".idea", ".vscode"):
                continue
            edges.append((_dirname, dir))
        for file in files:
            if file in ("readme", "__init__.py"):
                continue
            edges.append((_dirname, file))

    dirname = pathlib.Path(".").absolute().name
    print(Tree(dirname, edges))

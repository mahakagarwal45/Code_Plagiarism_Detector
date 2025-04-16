import ast
import networkx as nx

class CFGGenerator(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_node = 0
        self.counter = 0

    def add_node(self, label):
        """Add a node to the graph with a given label."""
        self.counter += 1
        self.graph.add_node(self.counter, label=label)
        if self.current_node != 0:
            self.graph.add_edge(self.current_node, self.counter)
        self.current_node = self.counter

    def visit_FunctionDef(self, node):
        """Visit function definitions and add to the CFG."""
        self.add_node(f"FUNC: {node.name}")
        self.generic_visit(node)

    def visit_If(self, node):
        """Visit if statements and add to the CFG."""
        self.add_node("IF")
        self.generic_visit(node)

    def visit_For(self, node):
        """Visit for loops and add to the CFG."""
        self.add_node("FOR")
        self.generic_visit(node)

    def visit_While(self, node):
        """Visit while loops and add to the CFG."""
        self.add_node("WHILE")
        self.generic_visit(node)

    def visit_Return(self, node):
        """Visit return statements and add to the CFG."""
        self.add_node("RETURN")
        self.generic_visit(node)

def generate_cfg(code):
    """Generate the control flow graph (CFG) for the given code."""
    try:
        tree = ast.parse(code)
        cfg_gen = CFGGenerator()
        cfg_gen.visit(tree)
        return cfg_gen.graph
    except Exception as e:
        return f"Error generating CFG: {str(e)}"

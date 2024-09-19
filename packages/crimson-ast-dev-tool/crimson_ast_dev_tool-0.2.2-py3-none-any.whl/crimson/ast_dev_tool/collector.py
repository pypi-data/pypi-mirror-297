from typing import List, Type, Literal, Union, overload, TypeVar, Generic
import ast
from ast import unparse
from .getter import get_node, _SourceObjectTypes, _SourceObjectType

T = TypeVar('T', bound=ast.AST)

class NodeCollector(ast.NodeVisitor, Generic[T]):
    def __init__(self, node_type: Type[T]):
        self.node_type = node_type
        self.nodes: List[T] = []

    def visit(self, node: ast.AST):
        if isinstance(node, self.node_type):
            self.nodes.append(node)
        self.generic_visit(node)

@overload
def collect_nodes(
    node: ast.AST,
    node_type: Type[T],
    return_type: Literal["nodes"] = "nodes",
) -> List[T]:
    ...

@overload
def collect_nodes(
    node: ast.AST,
    node_type: Type[T],
    return_type: Literal["sources"],
) -> List[str]:
    ...

@overload
def collect_nodes(
    source: str,
    node_type: Type[T],
    return_type: Literal["nodes"] = "nodes",
) -> List[T]:
    ...

@overload
def collect_nodes(
    source: str,
    node_type: Type[T],
    return_type: Literal["sources"],
) -> List[str]:
    ...

@overload
def collect_nodes(
    object: _SourceObjectType,
    node_type: Type[T],
    return_type: Literal["nodes"] = "nodes",
) -> List[T]:
    ...

@overload
def collect_nodes(
    object: _SourceObjectType,
    node_type: Type[T],
    return_type: Literal["sources"],
) -> List[str]:
    ...

def collect_nodes(
    input: Union[str, ast.AST, _SourceObjectType],
    node_type: Type[T],
    return_type: Literal["nodes", "sources"] = "nodes",
) -> Union[List[T], List[str]]:

    if any([type(input) is str, type(input) in _SourceObjectTypes]):
        node = get_node(input)
    elif isinstance(input, ast.AST):
        node = input
    else:
        raise Exception("Input is not valid")

    collector = NodeCollector(node_type)
    collector.visit(node)
    nodes = collector.nodes

    if return_type == "nodes":
        return nodes
    elif return_type == "sources":
        return [unparse(node) for node in nodes]

    raise ValueError("Invalid return_type")
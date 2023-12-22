from .diagram_layout import DiagramLayout
from ..diagram_class import DiagramClass


class HierarchicalLayout(DiagramLayout):

    def apply(self) -> None:
        first_level_nodes = list(self.diagram.objects)
        for name, obj in self.diagram.objects.items():
            if not isinstance(obj, DiagramClass) or len(obj.edges) != 0:
                first_level_nodes.remove(obj.name)

        self.assign_object_coordinates(first_level_nodes, 0)

    def assign_object_coordinates(self, nodes: list, y: int):
        if len(nodes) == 0:
            return

        next_nodes = []
        x_range = self.range_around_zero(len(nodes))
        for i, name in enumerate(nodes):
            self.diagram[name].x = x_range[i]
            self.diagram[name].y = y

            for _, obj in self.diagram.objects.items():
                if hasattr(obj, 'edges'):
                    for edge in obj.edges:
                        if edge.target.name == name:
                            next_nodes.append(obj.name)

        self.assign_object_coordinates(next_nodes, y + 1)

    @staticmethod
    def range_around_zero(n):
        half_n = n // 2
        return list(range(-half_n, half_n + 1))

from networkx.drawing.nx_agraph import graphviz_layout

from .diagram_layout import DiagramLayout


class DotLayout(DiagramLayout):

    def apply(self) -> None:
        layout = graphviz_layout(self.get_graph(), prog='dot')

        scale_x, scale_y = self.calculate_scaling_factors(layout)

        for key, pos in layout.items():
            self.diagram[key].x = pos[0] * scale_x * 25
            self.diagram[key].y = pos[1] * scale_y * 3

    @staticmethod
    def calculate_scaling_factors(layout):
        x_distances = []
        y_distances = []
        for key1, pos1 in layout.items():
            for key2, pos2 in layout.items():
                if key1 != key2:
                    x_distance = abs(pos1[0] - pos2[0])
                    y_distance = abs(pos1[1] - pos2[1])
                    x_distances.append(x_distance)
                    y_distances.append(y_distance)

        if x_distances and y_distances:
            average_x_distance = sum(x_distances) / len(x_distances)
            average_y_distance = sum(y_distances) / len(y_distances)

            x_scaling_factor = 1.0 / average_x_distance if average_x_distance != 0 else 1.0
            y_scaling_factor = 1.0 / average_y_distance if average_y_distance != 0 else 1.0
            
            return x_scaling_factor, y_scaling_factor
        else:
            return 1.0, 1.0

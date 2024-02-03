from pyplaml import *


class MyScene(ZoomedScene):
    def construct(self):
        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

        header = Text("PyPLAML exmaple", font_size=44, color=BLACK, weight=BOLD)
        self.play(Write(header), Create(Underline(header, color=BLACK)))

        # Prepare classes for diagram
        animal = DiagramClass("Animal", attributes=[
            ClassAttribute('name', modifier=AttributeModifier.PRIVATE),
            ClassAttribute('pet()', True)
        ])
        animal.set_abstract(True)
        dog = DiagramClass("Dog")
        cat = DiagramClass("Cat")

        # Prepare edges between classes
        dog.add_edge(
            DiagramEdge(dog, animal, target_rel=Relation.EXTENSION, edge_text="inherits from"))
        cat.add_edge(DiagramEdge(cat, animal, target_rel=Relation.EXTENSION))

        # Prepare diagram with a layout
        diagram = Diagram(DotLayout())
        diagram.add(animal, dog, cat, *dog.get_edges(), *cat.get_edges())  # remember to add the edges
        diagram.apply_layout(1, 0.75)  # after all objects are in the diagram, we can apply the layout

        diagram.move_to(ORIGIN).shift(DOWN * 3)
        self.play(self.camera.auto_zoom(self.mobjects + [diagram], margin=2))
        self.play(FadeIn(diagram))

        self.play(dog.animate.shift(LEFT))
        self.play(cat.animate.shift(RIGHT))

        self.play(animal.animate.rotate(45 * DEGREES))
        self.play(animal.animate.rotate(-90 * DEGREES))
        self.play(animal.animate.rotate(45 * DEGREES))

        self.play(FadeOut(animal), FadeOut(*dog.get_edges()), FadeOut(*cat.get_edges()))

        dog.add_attributes([
            ClassAttribute('void bark()', True)
        ])

        self.play(Indicate(dog))

        self.play(VGroup(dog, cat).animate.arrange(DOWN, buff=2).shift(DOWN * 3))

        dog_cat_assoc_edge = dog.add_edge(DiagramEdge(dog, cat, target_rel=Relation.ASSOCIATION))
        self.play(GrowFromEdge(
            dog_cat_assoc_edge,
            dog.get_edge_center(DOWN))
        )

        self.play(Indicate(dog))
        self.play(Indicate(dog_cat_assoc_edge))
        self.play(Indicate(cat))

        self.play(Swap(cat, dog))

        self.wait(2)

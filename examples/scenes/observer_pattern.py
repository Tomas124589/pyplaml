from pyplaml import *


class MyScene(ZoomedScene):
    def construct(self):
        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

        header = Text("Observer Pattern", font_size=44, color=BLACK, weight=BOLD)

        observer = DiagramInterface("Observer").add_attributes([
            ClassAttribute("update()", True),
        ])

        subject = DiagramInterface("Subject").add_attributes([
            ClassAttribute("observerCollection"),
            ClassAttribute("registerObserver(observer)", True, AttributeModifier.PRIVATE),
            ClassAttribute("unregisterObserver(observer)", True, AttributeModifier.PRIVATE),
            ClassAttribute("notifyObservers", True, AttributeModifier.PRIVATE),
        ])

        concrete_observer = DiagramClass("ConcreteObserver").add_attributes([
            ClassAttribute("update()", True)
        ])
        concrete_subject = DiagramClass("ConcreteSubject")

        concrete_observer.add_edge(DiagramEdge(concrete_observer, observer, target_rel=Relation.EXTENSION))
        concrete_subject.add_edge(DiagramEdge(concrete_subject, subject, target_rel=Relation.EXTENSION))

        d = Diagram(layout=DotLayout())
        d.add(observer, subject, concrete_observer, *concrete_observer.get_edges(), concrete_subject,
              *concrete_subject.get_edges())
        d.apply_layout(2)

        self.play(Write(header))
        self.play(Create(Underline(header, color=BLACK)))

        d.move_to(header, DOWN).shift(DOWN * 5)
        self.play(self.camera.auto_zoom(self.mobjects + [d], margin=1))
        self.play(FadeIn(d))

        self.play(Create(observer.add_edge(DiagramEdge(observer, subject, target_rel=Relation.AGGREGATION))))

        self.play(
            observer.animate.move_to(ORIGIN + DOWN),
            concrete_observer.animate.shift(UP),
            subject.animate.match_y(concrete_observer).shift(UP * 0.75),
            self.camera.frame.animate.scale(1.2).shift(DOWN),
            concrete_subject.animate.shift(DOWN * 1.5), run_time=2
        )

        for o in [observer, concrete_observer, subject, concrete_subject]:
            self.play(Indicate(o))

        self.wait(5)

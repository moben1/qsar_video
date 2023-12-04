from manim import *


# -qk flag to generate in 4k

class Pipeline(Scene):
    def construct(self):
        self.create_pipeline()
        self.create_gan()

    def create_neural_network(self, layers):
        # Position layers
        for i, layer in enumerate(layers):
            layer.move_to((i - 1) * 2 * RIGHT)

        # Draw the layers
        for layer in layers:
            self.play(Create(layer, run_time=0.5))

        # Connect the layers
        for i in range(len(layers) - 1):
            for neuron in layers[i]:
                for next_neuron in layers[i + 1]:
                    self.play(
                        Create(Line(neuron.get_center(), next_neuron.get_center(), buff=0.1).set_stroke(WHITE, 2),
                               run_time=0.01))

    def create_gan(self):
        # Display the generator
        gen_layers = [
            VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1) for _ in range(3)]).arrange(DOWN, buff=0.4),
            VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1) for _ in range(5)]).arrange(DOWN, buff=0.35),
            VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1) for _ in range(5)]).arrange(DOWN, buff=0.35),
            VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1) for _ in range(7)]).arrange(DOWN, buff=0.3),
        ]
        self.create_neural_network(layers=gen_layers)

        desc_layers = [
            VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1) for _ in range(7)]).arrange(DOWN, buff=0.3),
            VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1) for _ in range(5)]).arrange(DOWN, buff=0.36),
            VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1) for _ in range(5)]).arrange(DOWN, buff=0.35),
            VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1) for _ in range(3)]).arrange(DOWN, buff=0.4)
        ]
        self.create_neural_network(layers=desc_layers)
        self.wait(1)

    def create_pipeline(self):
        # Display the title
        title = Tex("qsarKit: outil ML dédiés à la prédiction de transfert de toxines réalisé par Mohammed Benabbassi",
                    color=BLUE).scale(0.7).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)

        # Tranfer the title to upper left corner
        workflow_title = Tex("Flux de travail", color=BLUE)
        workflow_title.to_corner(UP + LEFT)
        self.play(Transform(title, workflow_title))
        self.wait(1)

        # Define pastel colors
        colors = [BLUE, YELLOW, PINK, GREEN]

        # Create boxes for each step with graded colors
        steps = ["Génération", "Prétraitement", "Entrainement", "Évaluation"]
        boxes = [Rectangle(width=2.5, height=1.5, fill_color=c, fill_opacity=0.5, stroke_width=2).shift(
            5 * LEFT + i * 3 * RIGHT) for i, c in enumerate(colors)]

        arrows = [Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.5, stroke_width=3, stroke_color=WHITE) for
                  i in range(3)]

        for idx, (box, step) in enumerate(zip(boxes, steps)):
            self.play(Create(box))
            step_text = Text(step, color=BLACK).scale(0.5).move_to(box.get_center())
            self.play(Write(step_text))
            if idx < 3:
                self.play(Create(arrows[idx]))
        self.wait(1)
        self.play(FadeOut(Group(*boxes, *arrows)))

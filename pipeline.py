from manim import *


# -qk flag to generate in 4k

class Pipeline(Scene):
    def construct(self):
        self.create_pipeline()

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

        arrows = [Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.5, stroke_width=7, stroke_color=WHITE) for
                  i in range(3)]

        for idx, (box, step) in enumerate(zip(boxes, steps)):
            self.play(Create(box), run_time=0.5)
            step_text = Text(step, color=BLACK).scale(0.5).move_to(box.get_center())
            self.play(Write(step_text), run_time=0.5)
            if idx < 3:
                self.play(Create(arrows[idx]), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(Group(*boxes, *arrows)))

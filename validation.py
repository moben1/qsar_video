from random import random

from manim import *
import numpy as np


class Validation(Scene):
    def construct(self):
        title = Tex("Validation et évaluation", color=BLUE, font_size=48).to_edge(UP)
        self.play(Write(title), run_time=0.5)

        training_label = Text("Données d'entrainement", color=GREEN, font_size=18).to_edge(0.5*UP + RIGHT)
        test_label = Text("Données de test", color=RED, font_size=18).next_to(training_label, DOWN)
        self.play(Write(training_label), Write(test_label), run_time=0.5)

        r_2 = MathTex(
            "R^{2} = 1 - \\frac{\\sum_{i=1}^{n}(y_{i} - \\hat{y}_{i})^{2}}{\\sum_{i=1}^{n}(y_{i} - \\bar{y})^{2}}",
            color=WHITE, font_size=24).to_edge(RIGHT, buff=2)

        dataset_box = Rectangle(width=5, height=1, color=WHITE).next_to(r_2, DOWN)
        folds = VGroup(*[Rectangle(width=1, height=1, color=BLUE) for _ in range(5)])
        folds.arrange(RIGHT, buff=0).move_to(dataset_box.get_center())
        fold_labels = VGroup(
            *[Text(f"Fold {i + 1}", color=WHITE, font_size=18).move_to(folds[i].get_center()) for i in range(5)])

        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[0, 22, 1],
        ).to_edge(RIGHT, buff=1)

        NB_POINTS = 120

        x_values = np.random.uniform(0, 10, NB_POINTS)
        y_values = (2.0 + 0.1 * random()) * x_values + np.random.normal(0, 1, NB_POINTS)

        colors = self.get_colors(len(x_values))
        points = VGroup(
            *[Dot(axes.c2p(x, y), color=c, fill_opacity=0.7) for x, y, c in zip(x_values, y_values, colors)])
        self.play(LaggedStart(*[Create(dot) for dot in points], lag_ratio=0.05), run_time=1)
        self.play(Create(dataset_box), Create(axes), run_time=0.5)
        self.play(LaggedStart(*[Create(fold) for fold in folds], lag_ratio=0.1), run_time=1)
        self.play(LaggedStart(*[Write(label) for label in fold_labels], lag_ratio=0.1), run_time=1)
        self.play(Write(r_2), run_time=1)

        for i in range(5):
            colors = self.get_colors(len(x_values))
            for p in points:
                p.set_color(colors.pop())
            test_fold = folds[i]
            training_folds = VGroup(*[folds[j] for j in range(5) if j != i])
            self.play(training_folds.animate.set_fill(GREEN, opacity=0.4), test_fold.animate.set_fill(RED, opacity=0.4),
                      run_time=0.1)
            self.wait(1)
            m, b = np.polyfit(x_values, y_values, 1)
            regression_line = axes.plot_line_graph(
                x_values=[min(x_values), max(x_values)],
                y_values=[m * min(x_values) + b, m * max(x_values) + b],
                line_color=BLUE
            )
            self.play(Create(regression_line), run_time=1)

        self.wait(1)

    def get_colors(self, count):
        return [GREEN if random() > 0.25 else RED for _ in range(count)]

from random import random

from manim import *
import numpy as np


class Regression(Scene):
    def construct(self):
        title = Tex("Régression linéaire", color=BLUE, font_size=48).to_edge(UP)
        self.play(Write(title), run_time=0.5)
        # Create axes
        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[0, 22, 1],
        )

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        self.play(Create(axes))
        self.add(x_label, y_label)
        self.wait(1)

        x_values = np.random.uniform(0, 10, 70)
        y_values = (2.0 + 0.1 * random()) * x_values + np.random.normal(0, 1, 70)
        points = VGroup(*[Dot(axes.c2p(x, y), color=PINK, fill_opacity=0.8) for x, y in zip(x_values, y_values)])

        self.play(LaggedStart(*[Create(dot) for dot in points], lag_ratio=0.05))
        self.wait(1)

        m, b = np.polyfit(x_values, y_values, 1)

        # Create regression line
        regression_line = axes.plot_line_graph(
            x_values=[min(x_values), max(x_values)],
            y_values=[m * min(x_values) + b, m * max(x_values) + b],
            line_color=GREEN
        )

        # Draw regression line
        self.play(Create(regression_line), run_time=1)

        lasso_regression = MathTex(
            "Lasso: \\mathcal{L}_{1} = \\sum\\limits_{i=1}^{p}(y_{i}-x_{i}\\beta)^{2} + \\lambda\\sum\\limits_{j=1}^{n}|\\beta_{j}|",
            color=WHITE, font_size=24).to_edge(RIGHT, buff=2)
        self.play(Write(lasso_regression))

        ridge_regression = MathTex(
            "Ridge: \\mathcal{L}_{2} = \\sum\\limits_{i=1}^{p}(y_{i}-x_{i}\\beta)^{2} + \\lambda\\sum\\limits_{j=1}^{n}\\beta^{2}_{j}",
            color=WHITE, font_size=24).next_to(lasso_regression, DOWN)
        self.play(Write(ridge_regression))

        elasticnet_regression = MathTex(
            "ElasticNet: \\mathcal{L}_{elastic} = \\frac{\\sum\\limits_{i=1}^{p}(y_{i} - x_{i}\\beta)^{2}}{2p} + \\lambda(\\frac{1-\\alpha}{2} \\sum\\limits^{n}_{j=1}\\beta_{j}^{2} + \\alpha \\sum\\limits^{n}_{j=1}|\\beta_{j}|)",
            color=WHITE, font_size=24).next_to(ridge_regression, DOWN)
        self.play(Write(elasticnet_regression))

        self.wait(2)

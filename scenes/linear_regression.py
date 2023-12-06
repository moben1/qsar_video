from random import random

from manim import *
import numpy as np


def scene_regression(scene: Scene):
    title = Text("3 Modèles de régression linéaire", color=BLUE, font_size=48).to_edge(UP)
    scene.add(title)
    scene.play(Write(title), run_time=0.5)

    axes = Axes(
        x_range=[0, 12, 1],
        y_range=[0, 22, 1],
    )

    x_label = axes.get_x_axis_label("x").scale(0.5)
    y_label = axes.get_y_axis_label("y").scale(0.5)

    scene.play(Create(axes))
    scene.add(x_label, y_label)
    scene.wait(1)

    x_values, y_values, points = display_scatter_plot(scene, axes, colors=[PINK for _ in range(120)])

    display_regression_line(scene, axes, x_values, y_values)

    lasso_regression = MathTex(
        "Lasso: \\mathcal{L}_{1} = \\sum\\limits_{i=1}^{p}(y_{i}-x_{i}\\beta)^{2} + \\lambda\\sum\\limits_{j=1}^{n}|\\beta_{j}|",
        color=WHITE, font_size=24).to_edge(RIGHT, buff=2)
    scene.play(Write(lasso_regression))

    ridge_regression = MathTex(
        "Ridge: \\mathcal{L}_{2} = \\sum\\limits_{i=1}^{p}(y_{i}-x_{i}\\beta)^{2} + \\lambda\\sum\\limits_{j=1}^{n}\\beta^{2}_{j}",
        color=WHITE, font_size=24).next_to(lasso_regression, DOWN)
    scene.play(Write(ridge_regression))

    elasticnet_regression = MathTex(
        "ElasticNet: \\mathcal{L}_{elastic} = \\frac{\\sum\\limits_{i=1}^{p}(y_{i} - x_{i}\\beta)^{2}}{2p} + \\lambda(\\frac{1-\\alpha}{2} \\sum\\limits^{n}_{j=1}\\beta_{j}^{2} + \\alpha \\sum\\limits^{n}_{j=1}|\\beta_{j}|)",
        color=WHITE, font_size=24).next_to(ridge_regression, DOWN)
    scene.play(Write(elasticnet_regression))
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.5)


def display_scatter_plot(scene: Scene, axes: Axes, colors, points_count=120):
    x_values = np.random.uniform(0, 10, points_count)
    y_values = (2.0 + 0.1 * random()) * x_values + np.random.normal(0, 1, points_count)
    points = VGroup(
        *[Dot(axes.c2p(x, y), color=c, fill_opacity=0.7) for x, y, c in zip(x_values, y_values, colors)])
    scene.play(LaggedStart(*[Create(dot) for dot in points], lag_ratio=0.05), run_time=1)
    return x_values, y_values, points


def display_regression_line(scene: Scene, axes: Axes, x_values, y_values, c=GREEN):
    m, b = np.polyfit(x_values, y_values, 1)

    regression_line = axes.plot_line_graph(
        x_values=[min(x_values), max(x_values)],
        y_values=[m * min(x_values) + b, m * max(x_values) + b],
        line_color=c
    )

    scene.play(Create(regression_line), run_time=1)
    return regression_line

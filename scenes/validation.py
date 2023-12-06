from random import random

from manim import *

from scenes.linear_regression import display_regression_line, display_scatter_plot


def scene_validation(scene: Scene):
    title = Tex("Validation et évaluation", color=BLUE, font_size=48).to_edge(UP)
    scene.add(title)
    scene.play(Write(title), run_time=0.5)

    training_label = Text("Données d'entrainement", color=GREEN, font_size=18).to_edge(0.5 * UP + RIGHT)
    test_label = Text("Données de test", color=RED, font_size=18).next_to(training_label, DOWN)
    scene.play(Write(training_label), Write(test_label), run_time=0.5)

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

    for i in range(5):
        if i == 0:
            scene.play(Create(dataset_box), Create(axes), run_time=0.5)
            scene.play(LaggedStart(*[Create(fold) for fold in folds], lag_ratio=0.1), run_time=1)
            scene.play(LaggedStart(*[Write(label) for label in fold_labels], lag_ratio=0.1), run_time=1)
            scene.play(Write(r_2), run_time=1)

        colors = get_colors(120)
        test_fold = folds[i]
        training_folds = VGroup(*[folds[j] for j in range(5) if j != i])
        scene.play(training_folds.animate.set_fill(GREEN, opacity=0.4), test_fold.animate.set_fill(RED, opacity=0.4),
                   run_time=0.1)
        x_values, y_values, points = display_scatter_plot(scene, axes, colors)

        reg_lin = display_regression_line(scene, axes, x_values, y_values, PURPLE)
        scene.play(FadeOut(points), FadeOut(reg_lin), run_time=0.5)

        for p in points:
            p.set_color(colors.pop())

    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.5)


def get_colors(count):
    return [GREEN if random() > 0.25 else RED for _ in range(count)]

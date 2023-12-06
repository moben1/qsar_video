from manim import *


def scene_pipeline(scene: Scene):
    poster = ImageMobject("../qsar_video/images/poster_qsar.png").scale(0.8)
    scene.play(FadeIn(poster))
    scene.wait(2)
    scene.play(FadeOut(poster, ))

    workflow_title = Tex("Flux de travail", font_size=48, color=BLUE)
    workflow_title.to_edge(UP)
    scene.play(FadeIn(workflow_title))

    colors = [BLUE, YELLOW, PINK, GREEN]

    steps = ["Génération de données", "Prétraitement de données", "Entrainement des modèles", "Évaluation et validation"]
    boxes = [Rectangle(width=2.5, height=1.5, fill_color=c, fill_opacity=0.6, stroke_width=2).shift(
        4.5 * LEFT + i * 3 * RIGHT) for i, c in enumerate(colors)]

    arrows = [Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.1, stroke_width=6, stroke_color=YELLOW)
              for
              i in range(3)]

    for idx, (box, step) in enumerate(zip(boxes, steps)):
        scene.play(Create(box), run_time=0.5)
        step_text = Text(step, color=BLACK, font_size=15).move_to(box.get_center())
        scene.play(Write(step_text), run_time=0.5)
        if idx < 3:
            scene.play(Create(arrows[idx]), run_time=0.5)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.5)

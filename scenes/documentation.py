from manim import *


def scene_documentation(scene: Scene):
    title = Tex("Le code et la documentation complets sont accessibles via GitHub et Sphinx", color=BLUE,
                font_size=28).to_edge(UP)
    scene.add(title)
    scene.play(Write(title), run_time=0.5)

    image1 = ImageMobject("../qsar_video/images/doc_github.png").scale(0.86)
    image2 = ImageMobject("../qsar_video/images/doc_sphinx.png").scale(0.9)

    image1.to_edge(LEFT + DOWN)
    image2.to_edge(RIGHT + DOWN)

    scene.play(FadeIn(image1), FadeIn(image2))
    scene.wait(2)

    scene.play(FadeOut(image1), FadeOut(image2))

    merci = Tex("Merci !", color=BLUE, font_size=48).move_to(ORIGIN)
    scene.play(Transform(title, merci), run_time=0.5)

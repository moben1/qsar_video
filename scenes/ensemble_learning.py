from manim import *


def scene_ensemble_learning(scene: Scene):
    title = Tex("3 Modèles d'apprentissage ensembliste", font_size=48, color=BLUE).to_edge(UP)
    scene.add(title)

    # add images of the 3 models in the left side of the screen
    image1 = ImageMobject("../qsar_video/images/random_forest.png").scale(0.7).to_corner(DOWN + LEFT)
    image2 = ImageMobject("../qsar_video/images/catboost.png").scale(0.5).to_corner(UP + RIGHT)
    image3 = ImageMobject("../qsar_video/images/xgboost.png").scale(0.4).to_corner(UP + LEFT)
    scene.play(FadeIn(image1), FadeIn(image2), FadeIn(image3), run_time=0.5)

    subsets_list = []
    for i in range(3):
        t = f"{i + 1}" if i < 2 else "n"
        subsets_list.append(Tex("$Sous{-}ensemble_{" + t + "}$", font_size=28))
    subsets = VGroup(*subsets_list)
    subsets.arrange(RIGHT, buff=2).next_to(title, DOWN, buff=0.5)

    scene.play(Write(title), run_time=0.3)
    scene.play(LaggedStart(*[Write(subset) for subset in subsets], lag_ratio=0.1))
    scene.wait()

    tree_positions = [4 * LEFT + 2 * UP, 2 * UP, 4 * RIGHT + 2 * UP]
    trees = VGroup(*[create_decision_tree(pos) for pos in tree_positions])
    for tree in trees:
        scene.play(FadeIn(tree, shift=UP), run_time=1)
    scene.wait()

    paths = [
        [0, 14, 1, 7, 2, 6, 5],
        [0, 28, 15, 21, 16, 20, 19],
        [0, 14, 1, 13, 8, 12, 11]
    ]

    predictions = []
    for i, path in enumerate(paths):
        for j in path:
            scene.play(ApplyMethod(trees[i][j].set_color, YELLOW), run_time=0.1)
        t = f"{i + 1}" if i < 2 else "n"
        prediction = Tex("$Prediction_{" + t + "}$", font_size=28, color=WHITE).next_to(trees[i], DOWN)
        predictions.append(prediction)
        scene.play(Write(prediction), run_time=0.5)

    final_prediction = MathTex("Prediction finale = \\frac{1}{T} \\sum_{i=1}^{T} Prediction_{i}",
                               color=WHITE, font_size=28).next_to(trees[1], 5 * DOWN)

    arrow1 = Arrow(start=predictions[0].get_right(), end=final_prediction.get_left(), buff=0.1,
                   stroke_width=6).set_color(YELLOW)
    arrow2 = Arrow(start=predictions[1].get_center(), end=final_prediction.get_center(), buff=0.1,
                   stroke_width=6).set_color(YELLOW)
    arrow3 = Arrow(start=predictions[2].get_left(), end=final_prediction.get_right(), buff=0.1,
                   stroke_width=6).set_color(YELLOW)
    scene.play(Create(arrow1), Create(arrow2), Create(arrow3), run_time=0.01)

    scene.play(Write(final_prediction), run_time=1)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.5)


def create_decision_tree(root_position, depth=4):
    tree = VGroup()

    def create_nodes(position, level, max_width=4.0):
        node = Dot(position, stroke_color=BLUE, stroke_width=3)
        tree.add(node)
        if level < depth:
            left_child_position = position + LEFT * max_width / 2 ** (level + 1) + DOWN
            right_child_position = position + RIGHT * max_width / 2 ** (level + 1) + DOWN

            tree.add(Line(node.get_center(), create_nodes(left_child_position, level + 1, max_width).get_center()))
            tree.add(Line(node.get_center(), create_nodes(right_child_position, level + 1, max_width).get_center()))
        return node

    create_nodes(root_position, 1)

    return tree

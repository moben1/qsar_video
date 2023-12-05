from manim import *


class Models(Scene):
    def construct(self):
        training_data = Text("Apprentissage ensembliste", font_size=18, color=BLUE).to_edge(UP)
        subsets_list = []
        for i in range(3):
            t = f"{i + 1}" if i < 2 else "n"
            subsets_list.append(Tex("$Sous{-}ensemble_{" + t + "}$", font_size=28))
        subsets = VGroup(*subsets_list)
        subsets.arrange(RIGHT, buff=2).next_to(training_data, DOWN, buff=0.5)

        self.play(Write(training_data))
        self.play(LaggedStart(*[Write(subset) for subset in subsets], lag_ratio=0.5))
        self.wait()

        tree_positions = [4 * LEFT + 2 * UP, 2 * UP, 4 * RIGHT + 2 * UP]
        trees = VGroup(*[self.create_decision_tree(pos) for pos in tree_positions])
        for tree in trees:
            self.play(FadeIn(tree, shift=UP), run_time=2)
        self.wait()

        predictions_list = []
        for i in range(3):
            t = f"{i + 1}" if i < 2 else "n"
            predictions_list.append(Tex("$Prediction_{" + t + "}$", font_size=28, color=WHITE).next_to(trees[i], DOWN))
        predictions = VGroup(*predictions_list)
        final_prediction = MathTex("Final Prediction = \\frac{1}{T} \\sum_{i=1}^{T} Prediction_{i}",
                                   color=GREEN).next_to(
            predictions, DOWN, buff=1)

        for prediction in predictions:
            self.play(Write(prediction))

        self.play(Write(final_prediction))
        self.wait()

        for prediction in predictions:
            arrow = Arrow(prediction, final_prediction, buff=0.1)
            self.play(Create(arrow))
        self.wait()

    def create_decision_tree(self, root_position):
        depth = 4
        tree = VGroup()

        def create_nodes(position, level, max_width):
            node = Dot(position, stroke_color=BLUE, stroke_width=2)
            tree.add(node)
            if level < depth:
                left_child_position = position + LEFT * max_width / 2 ** (level + 1) + DOWN
                right_child_position = position + RIGHT * max_width / 2 ** (level + 1) + DOWN

                tree.add(Line(node.get_center(), create_nodes(left_child_position, level + 1, max_width).get_center()))
                tree.add(Line(node.get_center(), create_nodes(right_child_position, level + 1, max_width).get_center()))
            return node

        max_width = 4.0
        create_nodes(root_position, 1, max_width)

        return tree

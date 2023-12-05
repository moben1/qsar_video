from manim import *


class Models(Scene):
    def construct(self):
        training_data = Tex("Apprentissage ensembliste", font_size=28, color=BLUE).to_edge(UP)
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

        paths = [
            [0, 14, 1, 7, 2, 6, 5],
            [0, 28, 15, 21, 16, 20, 19],
            [0, 14, 1, 13, 8, 12, 11]
        ]

        predictions_list = []
        for i in range(3):
            t = f"{i + 1}" if i < 2 else "n"
            predictions_list.append(Tex("$Prediction_{" + t + "}$", font_size=28, color=WHITE).next_to(trees[i], DOWN))
        predictions = VGroup(*predictions_list)

        for i, path in enumerate(paths):
            for j in path:
                self.play(ApplyMethod(trees[i][j].set_color, YELLOW))
                self.wait()

        final_prediction = MathTex("Prediction finale = \\frac{1}{T} \\sum_{i=1}^{T} Prediction_{i}",
                                   color=WHITE, font_size=28).next_to(
            predictions, DOWN, buff=1)

        for prediction in predictions:
            self.play(Write(prediction))

        self.play(Write(final_prediction))
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

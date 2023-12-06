from manim import *
from scenes.ensemble_learning import scene_ensemble_learning

from scenes.documentation import scene_documentation
from scenes.gan import scene_gan
from scenes.linear_regression import scene_regression
from scenes.pipeline import scene_pipeline
from scenes.validation import scene_validation


class CompleteVideo(Scene):

    def construct(self):
        scene_pipeline(self)
        scene_gan(self)
        scene_regression(self)
        self.wait(1)
        scene_ensemble_learning(self)
        self.wait(1)
        scene_validation(self)
        scene_documentation(self)
        self.wait(2)

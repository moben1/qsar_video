from random import random

from manim import *


def scene_gan(scene: Scene):
    title = Tex("Réseau adverse génératif (GAN)", color=BLUE, font_size=48).to_edge(UP)
    scene.play(Write(title), run_time=0.5)
    scene.add(title)
    subtitle = Tex("Enrechir l'esemble de données via la génération de molécules synthétiques", color=BLUE,
                   font_size=24).next_to(title, DOWN)
    scene.play(Write(subtitle), run_time=0.5)

    def create_layer(num_neurons, radius=0.1, buff=0.3):
        return VGroup(
            *[Circle(radius=radius, fill_color=WHITE, fill_opacity=1, stroke_color=BLUE, stroke_width=2) for _ in
              range(num_neurons)]).arrange(DOWN,
                                           buff=buff)

    generator_layers = [create_layer(size) for size in [3, 5, 5, 7]]
    discriminator_layers = [create_layer(size) for size in [7, 5, 5, 3]]

    def position_layers(layers, spacing=1.25):
        for i, layer in enumerate(layers):
            layer.move_to((i - 1) * spacing * RIGHT)

    position_layers(generator_layers)
    position_layers(discriminator_layers)

    generator = VGroup(*generator_layers)
    discriminator = VGroup(*discriminator_layers)
    networks = VGroup(generator, discriminator).arrange(RIGHT, buff=5)
    networks.move_to(ORIGIN)

    for network in [generator, discriminator]:
        scene.play(
            LaggedStart(*(Create(layer) for layer in network), lag_ratio=0.1),
            run_time=0.35
        )
        for i in range(len(generator_layers) - 1):
            scene.play(
                LaggedStart(
                    *(Create(Line(neuron.get_center(), next_neuron.get_center(), buff=0.1).set_stroke(WHITE, 2))
                      for neuron in network[i]
                      for next_neuron in network[i + 1]
                      ),
                    lag_ration=0.1
                ),
                run_time=0.35
            )

    generator_label = Text("Générateur", color=GREEN, font_size=28).next_to(generator, DOWN)
    discriminator_label = Text("Discriminateur", color=RED, font_size=28).next_to(discriminator, DOWN)
    scene.play(Write(generator_label), Write(discriminator_label), run_time=0.01)

    def create_connections(layer1, layer2):
        connections_white = VGroup()
        connections_green = VGroup()
        for neuron1 in layer1:
            for neuron2 in layer2:
                line_white = Line(neuron1.get_center(), neuron2.get_center(), buff=0.1).set_stroke(WHITE, 2)
                line_green = Line(neuron1.get_center(), neuron2.get_center(), buff=0.1).set_stroke(YELLOW, 2)
                connections_white.add(line_white)
                connections_green.add(line_green)
                scene.add(line_white)
                scene.add(line_green)
                line_green.set_opacity(0)
        return connections_white, connections_green

    def training_simulation(network_layers, color_to_use=GREEN):
        all_connections = []
        for i in range(len(network_layers) - 1):
            connections_white, connections_green = create_connections(network_layers[i], network_layers[i + 1])
            all_connections.append((connections_white, connections_green))

        for i in range(len(network_layers) - 1):
            if i == 0:
                current_layer = network_layers[i]
                neuron_anims = [neuron.animate.set_fill(opacity=random(), color=color_to_use) for neuron in current_layer]
                scene.play(AnimationGroup(*neuron_anims, lag_ration=0.1), run_time=0.35)

            next_layer = network_layers[i + 1]
            connections_white, connections_green = all_connections[i]

            line_anims_to_green = [line.animate.set_opacity(1) for line in connections_green]
            scene.play(AnimationGroup(*line_anims_to_green, lag_ration=0.1), run_time=0.35)

            neuron_anims_layer2 = [neuron.animate.set_fill(opacity=random(), color=color_to_use) for neuron in
                                   next_layer]
            scene.play(AnimationGroup(*neuron_anims_layer2, lag_ration=0.1), run_time=0.35)

            line_anims_to_white = [line.animate.set_opacity(0) for line in connections_green]
            scene.play(AnimationGroup(*line_anims_to_white, lag_ratio=0.1), run_time=0.35)

    training_simulation(generator_layers, GREEN)

    molecule = ImageMobject("../qsar_video/images/smiles.png").scale(0.5)
    scene.play(FadeIn(molecule))
    scene.wait(1)
    scene.play(FadeOut(molecule))

    arrow = Arrow(start=generator.get_right(), end=discriminator.get_left(), buff=0.1, stroke_width=6).set_color(
        YELLOW)
    scene.play(Create(arrow), run_time=0.01)
    training_simulation(discriminator_layers, RED)
    arrow2 = Arrow(start=discriminator.get_left(), end=generator.get_right(), buff=0.1, stroke_width=6).set_color(
        YELLOW)
    scene.play(Transform(arrow, arrow2), run_time=0.01)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.5)

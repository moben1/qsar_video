from random import random

from manim import *


class Gan(Scene):
    def construct(self):
        # Function to create a neural network layer
        def create_layer(num_neurons, radius=0.1, buff=0.3):
            return VGroup(
                *[Circle(radius=radius, fill_color=WHITE, fill_opacity=1, stroke_color=BLUE, stroke_width=2) for _ in
                  range(num_neurons)]).arrange(DOWN,
                                               buff=buff)

        # Create layers for both networks
        generator_layers = [create_layer(size) for size in [3, 5, 5, 7]]
        discriminator_layers = [create_layer(size) for size in [7, 5, 5, 3]]

        # Position the layers to form two networks
        def position_layers(layers, spacing=1.5):
            for i, layer in enumerate(layers):
                layer.move_to((i - 1) * spacing * RIGHT)

        position_layers(generator_layers)
        position_layers(discriminator_layers)

        # Group the networks and position them
        generator = VGroup(*generator_layers)
        discriminator = VGroup(*discriminator_layers)
        networks = VGroup(generator, discriminator).arrange(RIGHT, buff=3)
        networks.move_to(ORIGIN)

        # Draw the networks
        for network in [generator, discriminator]:
            for layer in network:
                self.play(Create(layer), run_time=0.001)
            for i in range(len(generator_layers) - 1):
                for neuron in network[i]:
                    for next_neuron in network[i + 1]:
                        self.play(
                            Create(Line(neuron.get_center(), next_neuron.get_center(), buff=0.1).set_stroke(WHITE, 2)),
                            run_time=0.001)

        # Add labels for Generator and Discriminator
        generator_label = Text("Generator", color=BLUE).next_to(generator, DOWN)
        discriminator_label = Text("Discriminator", color=RED).next_to(discriminator, DOWN)
        self.play(Write(generator_label), Write(discriminator_label), run_time=0.01)

        # Function to create connections between layers
        def create_connections(layer1, layer2):
            connections_white = VGroup()
            connections_green = VGroup()
            for neuron1 in layer1:
                for neuron2 in layer2:
                    line_white = Line(neuron1.get_center(), neuron2.get_center(), buff=0.1).set_stroke(WHITE, 2)
                    line_green = Line(neuron1.get_center(), neuron2.get_center(), buff=0.1).set_stroke(GREEN, 2)
                    connections_white.add(line_white)
                    connections_green.add(line_green)
                    self.add(line_white)
                    self.add(line_green)
                    line_green.set_opacity(0)  # Initially, green lines are invisible
            return connections_white, connections_green

        def training_simulation(network_layers, color_to_use=GREEN):
            all_connections = []
            for i in range(len(network_layers) - 1):
                connections_white, connections_green = create_connections(network_layers[i], network_layers[i + 1])
                all_connections.append((connections_white, connections_green))

            # Training simulation
            for i in range(len(network_layers) - 1):
                if i == 0:
                    layer1 = network_layers[i]
                    # Switch neurons to green
                    for neuron in layer1:
                        self.play(neuron.animate.set_fill(opacity=random(), color=color_to_use), run_time=0.001)

                layer2 = network_layers[i + 1]
                connections_white, connections_green = all_connections[i]

                # Switch connections to green
                for line in connections_green:
                    self.play(line.animate.set_opacity(1), run_time=0.001)

                # switch neurons layer2 to green
                for neuron in layer2:
                    self.play(neuron.animate.set_fill(opacity=random(), color=color_to_use), run_time=0.001)

                # Switch connections back to white
                for line in connections_green:
                    self.play(line.animate.set_opacity(0), run_time=0.001)

        training_simulation(generator_layers, GREEN)
        # draw an arrow from generator to discriminator
        arrow = Arrow(start=generator.get_right(), end=discriminator.get_left(), buff=0.1, stroke_width=6).set_color(
            YELLOW)
        self.play(Create(arrow), run_time=0.01)
        training_simulation(discriminator_layers, RED)
        # replace the arrow with a new one from discriminator to generator
        arrow2 = Arrow(start=discriminator.get_left(), end=generator.get_right(), buff=0.1, stroke_width=6).set_color(
            YELLOW)
        self.play(Transform(arrow, arrow2), run_time=0.01)
        self.wait(2)

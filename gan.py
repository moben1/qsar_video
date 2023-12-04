from manim import *


class Gan(Scene):
    def construct(self):
        # Function to create a neural network layer
        def create_layer(num_neurons, radius=0.1, buff=0.3):
            return VGroup(
                *[Circle(radius=radius, fill_color=WHITE, fill_opacity=1) for _ in range(num_neurons)]).arrange(DOWN,
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
        networks = VGroup(generator, discriminator).arrange(RIGHT, buff=4)
        networks.move_to(ORIGIN)

        # Draw the networks
        for network in [generator, discriminator]:
            for layer in network:
                self.play(Create(layer))
            for i in range(len(generator_layers) - 1):
                for neuron in network[i]:
                    for next_neuron in network[i + 1]:
                        self.play(
                            Create(Line(neuron.get_center(), next_neuron.get_center(), buff=0.1).set_stroke(WHITE, 2)),
                            run_time=0.01)

        # Add labels for Generator and Discriminator
        generator_label = Text("Generator", color=BLUE).next_to(generator, DOWN)
        discriminator_label = Text("Discriminator", color=RED).next_to(discriminator, DOWN)
        self.play(Write(generator_label), Write(discriminator_label))

        self.wait(2)

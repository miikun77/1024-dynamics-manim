import numpy as np
from manim import *


class WaveEquationScene(Scene):
    def construct(self):
        # Adjust the frame size
        self.camera.frame_width = 14

        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[-1, 1, 0.2],
            axis_config={"color": BLUE},
            tips=False,
        ).add_coordinates()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # Slide in axes and labels
        self.play(Write(axes_labels))
        self.play(Create(axes.x_axis), Create(axes.y_axis))
        self.wait(1)

        # Initial straight string
        straight_line = axes.plot(lambda x: 0, color=YELLOW)
        self.play(Create(straight_line))
        self.wait(1)

        # Initial shape created by pulling the string
        x0_label = MathTex(rf"x_0 = {x0}")
        x0_label.next_to(axes, UP)
        self.play(Write(x0_label))
        initial_wave = axes.plot(lambda x: initial_shape(x, x0), color=YELLOW)
        self.play(Transform(straight_line, initial_wave))
        self.wait(1)

        # Wave equation animation
        wave = axes.plot(lambda x: wave_equation(x, 0, x0, num_terms), color=YELLOW)
        wave_label = MathTex(
            rf"y(x,t) = \frac{{2}}{{\pi^2 x_0 (1 - x_0)}} \sum_{{n=1}}^{{{num_terms}}} \frac{{1}}{{n^2}} \sin(n \pi x_0) \sin(n \pi x) \cos(n \pi t)"
        ).scale(0.9).next_to(axes, DOWN)
        wave_label.to_edge(UP).shift(DOWN + RIGHT)
        self.play(Transform(straight_line, wave), Write(wave_label))
        self.wait()

        # Add num_terms label
        num_terms_label = MathTex(rf"\text{{Number of terms}}: {num_terms}").scale(0.9).next_to(wave_label, DOWN)
        self.play(Write(num_terms_label))
        self.wait()

        for t in np.linspace(0, 2, 200):
            new_wave = axes.plot(
                lambda x: wave_equation(x, t, x0, num_terms), color=YELLOW
            )
            self.play(Transform(straight_line, new_wave), run_time=0.02)
            self.wait(0.02)


class WaveModesScene(Scene):
    def construct(self):
        # Adjust the frame size
        self.camera.frame_width = 14

        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[-1, 1, 0.2],
            axis_config={"color": BLUE},
            tips=False,
        ).add_coordinates()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # Slide in axes and labels
        self.play(Write(axes_labels))
        self.play(Create(axes.x_axis), Create(axes.y_axis))
        self.wait(1)

        # Plot n=1 mode
        mode1 = axes.plot(lambda x: wave_equation(x, 0, x0, 1), color=RED)
        mode1_label = MathTex(r"n=1",color=RED).scale(0.7).next_to(mode1, UP)
        self.play(Create(mode1), Write(mode1_label))
        self.wait(1)

        # Plot n=2 mode
        mode2 = axes.plot(lambda x: wave_equation(x, 0, x0, 2) - wave_equation(x, 0, x0, 1), color=GREEN)
        mode2_label = MathTex(r"n=2",color=GREEN).scale(0.7).next_to(mode2, UP)
        self.play(Create(mode2), Write(mode2_label))
        self.wait(1)

        # Plot n=3 mode
        mode3 = axes.plot(lambda x: wave_equation(x, 0, x0, 3) - wave_equation(x, 0, x0, 2), color=PINK)
        mode3_label = MathTex(r"n=3", color=PINK).scale(0.7).next_to(mode3, UP)
        self.play(Create(mode3), Write(mode3_label))
        self.wait(1)

        # Sum of modes
        sum_modes = axes.plot(lambda x: wave_equation(x, 0, x0, 3), color=YELLOW)
        sum_modes_label = MathTex(r"\text{Sum of modes}", color=YELLOW).scale(0.7).next_to(sum_modes, UP)
        self.play(Create(sum_modes), Write(sum_modes_label))
        self.wait(1)

        # Add motion to the modes
        for t in np.linspace(0, 2, 200):
            new_mode1 = axes.plot(lambda x: wave_equation(x, t, x0, 1), color=RED)
            new_mode2 = axes.plot(lambda x: wave_equation(x, t, x0, 2) - wave_equation(x, t, x0, 1), color=GREEN)
            new_mode3 = axes.plot(lambda x: wave_equation(x, t, x0, 3) - wave_equation(x, t, x0, 2), color=PINK)
            new_sum_modes = axes.plot(lambda x: wave_equation(x, t, x0, 3), color=YELLOW)
            self.play(
                Transform(mode1, new_mode1),
                Transform(mode2, new_mode2),
                Transform(mode3, new_mode3),
                Transform(sum_modes, new_sum_modes),
                run_time=0.02
            )
            self.wait(0.02)

# Define the wave equation function
def wave_equation(x, t, x0, num_terms=100):
    pi = np.pi
    y = (2 / (pi**2 * x0 * (1 - x0))) * np.sum(
        [
            (1 / n**2) * np.sin(n * pi * x0) * np.sin(n * pi * x) * np.cos(n * pi * t)
            for n in range(1, num_terms + 1)
        ],
        axis=0,
    )
    return y


# Define the initial shape function
def initial_shape(x, x0):
    return np.where(x < x0, x / x0, (1 - x) / (1 - x0))


# Set variables
x0 = 0.3  # Middle of the string
num_terms = 1000  # Number of terms in the series

# Add a __main__ block to run the simulation
if __name__ == "__main__":
    from manim import *

    config.media_width = "100%"
    scene = WaveEquationScene()
    scene.render()

    # Render the wave modes scene
    wave_modes_scene = WaveModesScene()
    wave_modes_scene.render()
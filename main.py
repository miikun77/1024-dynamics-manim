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

        for t in np.linspace(0, 2, 200):
            new_wave = axes.plot(
                lambda x: wave_equation(x, t, x0, num_terms), color=YELLOW
            )
            self.play(Transform(straight_line, new_wave), run_time=0.02)
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
num_terms = 100  # Number of terms in the series

# Add a __main__ block to run the simulation
if __name__ == "__main__":
    from manim import *

    config.media_width = "100%"
    scene = WaveEquationScene()
    scene.render()
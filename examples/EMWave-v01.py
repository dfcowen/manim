from manim import *

class EMWave(ThreeDScene):  # Changed from Scene to ThreeDScene
    def construct(self):
        # Create axes
        axes = ThreeDAxes(
            x_range=[-8, 8, 1],
            y_range=[-4, 4, 1],
            z_range=[-2, 2, 1],
            x_length=8,
            y_length=4,
            z_length=4
        )

        # Create time-dependent functions for E and B fields
        def e_field(x, t):
            return 2.*np.cos(x - t)

        def b_field(x, t):
            return 2.*np.cos(x - t)

        # Create electric field (blue) and magnetic field (red) waves
        e_wave = always_redraw(
            lambda: ParametricFunction(
                lambda x: np.array([x, e_field(x, self.renderer.time), 0]),
                color=BLUE,
                t_range=[-8, 8, 0.1]
            )
        )

        b_wave = always_redraw(
            lambda: ParametricFunction(
                lambda x: np.array([x, 0, b_field(x, self.renderer.time)]),
                color=RED,
                t_range=[-8, 8, 0.1]
            )
        )

        # Labels
        e_label = Text("E", color=BLUE).move_to([4.5, 1, 0])
        b_label = Text("B", color=RED).move_to([4.5, 0, 1])
        title = Text("EM Wave", font_size=32).to_edge(UP)

        # Direction of propagation arrow and label
        prop_arrow = Arrow(start=[-4, -1.5, 0], end=[-2, -1.5, 0], color=WHITE)
        prop_label = Text("Direction of propagation", font_size=24).next_to(prop_arrow, DOWN)

        # Animation
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.0)

        self.play(Create(axes))
        self.play(Write(title))
        self.add(e_wave, b_wave)
        self.play(
            Create(prop_arrow),
            Write(prop_label),
            Write(e_label),
            Write(b_label)
        )
        self.wait(5)  # Show wave propagation for 5 seconds
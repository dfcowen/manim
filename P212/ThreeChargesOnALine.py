#   

from manim import *

class ThreeChargesCoulombForce(Scene):
    def __init__(
        self,
        q1=1.0,
        q2=-1.0,
        q3=1.0,
        x1=-1.0,
        x2=1.0,
        x3_start=5.0,
        x3_end=-5.0,
        line_length=10,
        dot_scale=2,
        force_scale=2.0,
        arrow_stroke=3,
        arrow_tip=0.15,
        y_offset_f13=-0.3,
        y_offset_f23=-0.4,
        animation_time=3,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.q1, self.q2, self.q3 = q1, q2, q3
        self.x1, self.x2 = x1, x2
        self.x3_start, self.x3_end = x3_start, x3_end
        self.line_length = line_length
        self.dot_scale = dot_scale
        self.force_scale = force_scale
        self.arrow_params = {
            "stroke_width": arrow_stroke,
            "tip_length": arrow_tip,
            "buff": 0
        }
        self.y_offset_f13 = y_offset_f13
        self.y_offset_f23 = y_offset_f23
        self.animation_time = animation_time

    def create_charge_dot(self, position, color, charge):
        """Create a dot with charge sign and value label"""
        sign = "+" if charge > 0 else "-"
        dot = VGroup(
            Dot(position).set_color(color).scale(self.dot_scale),
            Text(sign, font_size=24, color=BLACK).move_to(position)
        )
        label = Text(f"{charge:.0f}").next_to(dot, UP)
        return dot, label

    def create_force_arrow(self, start_pos, color):
        """Create a force arrow with standard parameters"""
        return Arrow(
            start=start_pos,
            end=[start_pos[0] + 1, start_pos[1], start_pos[2]],
            color=color,
            **self.arrow_params
        )

    def create_force_updater(self, moving_dot, fixed_dot, charge_product, y_offset):
        """Create an updater function for force arrows"""
        def update_force(arrow):
            moving_pos = moving_dot.get_center()
            fixed_pos = fixed_dot.get_center()
            
            r = np.linalg.norm(moving_pos - fixed_pos)
            force_mag = abs(charge_product) / ((r+.2)**2) + 0.1
            force_length = force_mag * self.force_scale
            direction = np.sign(moving_pos[0] - fixed_pos[0]) * np.sign(charge_product)
            
            start_pos = [moving_pos[0], moving_pos[1] + y_offset, moving_pos[2]]
            end_pos = [moving_pos[0] + force_length*direction, moving_pos[1] + y_offset, moving_pos[2]]
            
            arrow.put_start_and_end_on(start_pos, end_pos)
        return update_force

    def construct(self):
        # Create baseline
        line = Line([-self.line_length, 0, 0], [self.line_length, 0, 0]).set_color(WHITE)
        self.add(line)

        # Create fixed charges
        q1pos = [self.x1, 0, 0]
        q2pos = [self.x2, 0, 0]
        q3pos = [self.x3_start, 0, 0]

        dot1, label1 = self.create_charge_dot(q1pos, BLUE, self.q1)
        dot2, label2 = self.create_charge_dot(q2pos, RED, self.q2)
        dot3, _ = self.create_charge_dot(q3pos, YELLOW, self.q3)

        self.add(dot1, dot2, dot3, label1, label2)

        # Create force arrows
        force13 = self.create_force_arrow(dot3.get_center(), BLUE)
        force23 = self.create_force_arrow(dot3.get_center(), RED)

        # Add updaters
        force13.add_updater(self.create_force_updater(dot3, dot1, self.q1*self.q3, self.y_offset_f13))
        force23.add_updater(self.create_force_updater(dot3, dot2, self.q2*self.q3, self.y_offset_f23))

        self.add(force13, force23)

        # Continuous animation
#        self.play(
#            dot3.animate.move_to([self.x3_end, 0, 0]),
#            rate_func=linear,
#            run_time=self.animation_time
#        )

        # Animation in snapshots in time
        def stepped_rate(t, steps=9):
            return np.floor(t * (steps-1)) / (steps-1)

        self.play(
            dot3.animate.move_to([self.x3_end, 0, 0]),
            rate_func=stepped_rate,
            run_time=3
        )

if __name__ == "__main__":
    with tempconfig({"output_file": "ThreeChargesOnALine-v02"}):
        scene = ThreeChargesCoulombForce(
            q1=1.0,
            q2=-9.0,
            q3=1.0,
            # Add any other parameter overrides here
        )
        scene.render()
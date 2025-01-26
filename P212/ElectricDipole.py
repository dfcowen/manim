#
# Electric dipole experiencing torque in a constant E.
# Run with: manim -pql /storage/home/dfc13/manim/P212/ElectricDipole.py ElectricDipole
#
from manim import *

class ElectricDipole(Scene):
    def construct(self):
        # Constants
        d = 4  # dipole distance
        angle = 30 * DEGREES
        arrow_length = d/5
        force_length = d/5
        charge_radius = d/20
        
        # Create axes
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            axis_config={"include_tip": True}
        )
        
        # Add axis labels
        x_label = Text("x").next_to(axes.x_axis, RIGHT)
        y_label = Text("y").next_to(axes.y_axis, UP)
        
        # Create dipole
        start_point = d/2 * np.array([np.cos(angle), np.sin(angle), 0])
        end_point = -start_point
        
        dipole_line = Line(start_point, end_point, color=YELLOW)
        pos_charge = Circle(radius=charge_radius, color=BLUE, fill_opacity=1).move_to(start_point)
        neg_charge = Circle(radius=charge_radius, color=WHITE, fill_opacity=1).move_to(end_point)
        
        pos_label = Text("+q").next_to(pos_charge, UP)
        neg_label = Text("-q").next_to(neg_charge, DOWN)
        
        # Create force vectors
        pos_force = Arrow(
            start=start_point,
            end=start_point + np.array([force_length, 0, 0]),
            color=RED,
            buff=0
        )
        neg_force = Arrow(
            start=end_point,
            end=end_point + np.array([-force_length, 0, 0]),
            color=RED,
            buff=0
        )
        
        pos_force_label = Text("Fc").next_to(pos_force, DOWN)
        neg_force_label = Text("Fc").next_to(neg_force, UP)
        
        # Group elements
        force_elements = VGroup(pos_force, neg_force, pos_force_label, neg_force_label)
        dipole_group = VGroup(dipole_line, pos_charge, neg_charge)
        label_group = VGroup(pos_label, neg_label)
        
        # Create electric field arrows
        arrows = []
        positions = [
            # First quadrant
            [2.5, 2.5, 0], [1.5, 2.5, 0], [2.5, 1.5, 0], [1.5, 1.5, 0],
            # Second quadrant
            [-2.5, 2.5, 0], [-1.5, 2.5, 0], [-2.5, 1.5, 0], [-1.5, 1.5, 0],
            # Third quadrant
            [-2.5, -2.5, 0], [-1.5, -2.5, 0], [-2.5, -1.5, 0], [-1.5, -1.5, 0],
            # Fourth quadrant
            [2.5, -2.5, 0], [1.5, -2.5, 0], [2.5, -1.5, 0], [1.5, -1.5, 0]
        ]
        
        for pos in positions:
            arrow = Arrow(
                start=np.array(pos),
                end=np.array([pos[0] + arrow_length, pos[1], 0]),
                color=GRAY,
                buff=0
            )
            arrows.append(arrow)
        
        field_arrows = VGroup(*arrows)
        E_label = Text("E").next_to(arrows[4], UP)
        
        # Animation sequence
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(dipole_group), Write(label_group))
        self.wait(2)
        
        self.play(FadeIn(field_arrows), Write(E_label))
        self.wait(2)
        
        self.play(Create(force_elements))
        self.wait(2)

        
        # Updater function
        def update_positions(mob):
            pos_point = pos_charge.get_center()
            neg_point = neg_charge.get_center()
            
            # Update force vectors while keeping them horizontal
            pos_force.put_start_and_end_on(
                pos_point,
                pos_point + np.array([force_length, 0, 0])
            )
            neg_force.put_start_and_end_on(
                neg_point,
                neg_point + np.array([-force_length, 0, 0])
            )
            
            # Update force labels
            pos_force_label.next_to(pos_force, DOWN)
            neg_force_label.next_to(neg_force, UP)
            
            # Update charge labels
            pos_label.next_to(pos_charge, UP)
            neg_label.next_to(neg_charge, DOWN)
        
        # Add updaters
        force_elements.add_updater(update_positions)
        label_group.add_updater(lambda m: update_positions(m))
        
        # Rotation animation
        for _ in range(3):
            self.play(
                Rotate(dipole_group, angle=-60*DEGREES, about_point=ORIGIN),
                run_time=2
            )
            self.play(
                Rotate(dipole_group, angle=60*DEGREES, about_point=ORIGIN),
                run_time=2
            )
        
        self.wait(2)
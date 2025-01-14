from manim import *

# Run from command line with
#    python -m manim /storage/home/dfc13/manim/examples/ThreeChargesOnALine.py ThreeChargesCoulombForce -ql

class ThreeChargesCoulombForce(Scene):

    def __init__(self, q1=1.0, q2=-1.0, q3=1.0, **kwargs):
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        super().__init__(**kwargs)

    def construct(self):
        p1 = [-10, 0, 0]
        p2 = [ 10, 0, 0]
        line = Line(p1,p2)
        line.set_color(WHITE)  # Set color before adding
        self.add(line)        # Add the colored line

        q1pos = [-1, 0, 0]
        q2pos = [ 1, 0, 0]
        q3pos = [ 5, 0, 0]
        q3posFinal = [ -5, 0, 0]

        dot1 = Dot(q1pos).set_color(BLUE).scale(2)
        dot2 = Dot(q2pos).set_color(RED).scale(2)
        self.add(dot1, dot2)
        q1_label = Text(f"{self.q1:.0f}").next_to(dot1, UP)
        q2_label = Text(f"{self.q2:.0f}").next_to(dot2, UP)
        self.add(q1_label, q2_label)


        if q3 > 0: 
            q3sign = "+"
        else:
            q3sign = "-"
        dot3 = VGroup(
            Dot(q3pos).set_color(YELLOW).scale(2),
            Text(q3sign, font_size=24, color=BLACK).move_to(q3pos)
        )
        # Create moving yellow dot starting at far right
        #dot3 = Dot([4, 0, 0]).set_color(YELLOW).scale(2)
        self.add(dot3)

        dot3_pos = dot3.get_center()
        force23 = Arrow(
            start=dot3_pos,
            end=[dot3_pos[0] + 1, dot3_pos[1], dot3_pos[2]],
            color=RED,
            buff=0,
            #max_tip_length_to_length_ratio=0.15,  # Makes tip smaller (default is 0.25)
            #max_stroke_width_to_length_ratio=0.5    # Controls thickness
            stroke_width=3,        # Constant line thickness
            tip_length=0.15,        # Constant tip size
            )
        force13 = Arrow(
            start=dot3_pos,
            end=[dot3_pos[0] + 1, dot3_pos[1], dot3_pos[2]],
            color=BLUE,
            buff=0,
            #max_tip_length_to_length_ratio=0.15,  # Makes tip smaller (default is 0.25)
            #max_stroke_width_to_length_ratio=0.5    # Controls thickness
            stroke_width=3,        # Constant line thickness
            tip_length=0.15,        # Constant tip size
        )
        # Add updater to force13
        def update_force13(arrow):
            dot3_pos = dot3.get_center()
            dot1_pos = dot1.get_center()

            # Calculate distance between charges
            r = np.linalg.norm(dot3_pos - dot1_pos)
            
            # Calculate force magnitude (1/r^2 law)
            force_mag = abs(self.q1 * self.q3) / ((r+1)**2) + 0.1
            
            # Scale force for visualization (adjust scale_factor as needed)
            scale_factor = 3.
            force_length = force_mag * scale_factor
    
            # Calculate direction using sign
            direction = np.sign(dot3_pos[0] - dot1_pos[0]) * np.sign(self.q1 * self.q3)            
        
            y_offset = -0.3  # Adjust this value to move arrow down more or less
            
            # Calculate start and end points with offset
            start_pos = [dot3_pos[0], dot3_pos[1] + y_offset, dot3_pos[2]]
            end_pos = [dot3_pos[0] + force_length*direction, dot3_pos[1] + y_offset, dot3_pos[2]]
            
            arrow.put_start_and_end_on(start_pos, end_pos)

        # Add updater to force23
        def update_force23(arrow):
            dot3_pos = dot3.get_center()
            dot2_pos = dot2.get_center()

            # Calculate distance between charges
            r = np.linalg.norm(dot3_pos - dot2_pos)
            
            # Calculate force magnitude (1/r^2 law)
            force_mag = abs(self.q2 * self.q3) / ((r+1)**2) + 0.1
            
            # Scale force for visualization (adjust scale_factor as needed)
            scale_factor = 3.
            force_length = force_mag * scale_factor
    
            # Calculate direction using sign
            direction = np.sign(dot3_pos[0] - dot2_pos[0]) * np.sign(self.q2 * self.q3)            
        
            y_offset = -0.4  # Adjust this value to move arrow down more or less
            
            # Calculate start and end points with offset
            start_pos = [dot3_pos[0], dot3_pos[1] + y_offset, dot3_pos[2]]
            end_pos = [dot3_pos[0] + force_length*direction, dot3_pos[1] + y_offset, dot3_pos[2]]
            
            arrow.put_start_and_end_on(start_pos, end_pos)

        force13.add_updater(update_force13)
        self.add(force13)
        force23.add_updater(update_force23)
        self.add(force23)

        # Animate dot3 moving from right to left
        self.play(dot3.animate.move_to(q3posFinal), rate_func=linear, run_time=3)

with tempconfig({"output_file": "ThreeChargesOnALine"}):
    q1 = 1.
    q2 = -4.
    q3 = 1.
    scene = ThreeChargesCoulombForce(q1, q2, q3)
    scene.render()
from manim import *

class CircularCapacitorMagnetic(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = WHITE
        
        # Basic capacitor setup
        plate1_body = Rectangle(height=3.0, width=0.25, color=BLACK)
        plate2_body = Rectangle(height=3.0, width=0.25, color=BLACK)
        plate1_front = Ellipse(width=0.25, height=3.0, color=BLACK)
        plate2_front = Ellipse(width=0.25, height=3.0, color=BLACK)
        plate1_back = Ellipse(width=0.25, height=3.0, color=BLACK)
        plate2_back = Ellipse(width=0.25, height=3.0, color=BLACK)
        
        # Position plates
        plate1_body.shift(LEFT * 1)
        plate2_body.shift(RIGHT * 1)
        plate1_front.shift(LEFT * 1 + RIGHT * 0.125)
        plate2_front.shift(RIGHT * 1 + RIGHT * 0.125)
        plate1_back.shift(LEFT * 1 - RIGHT * 0.125)
        plate2_back.shift(RIGHT * 1 - RIGHT * 0.125)
        
        # Fill plates
        for plate in [plate1_body, plate2_body, plate1_front, plate2_front]:
            plate.set_fill(color=GRAY, opacity=0.9)
        for plate in [plate1_back, plate2_back]:
            plate.set_fill(color=GRAY_D, opacity=0.7)
        
        # Basic structure
        rod = Line(LEFT * 4, RIGHT * 4, color=BLACK)
        vert_line1 = Line(plate1_body.get_center(), rod.get_center(), color=BLACK)
        vert_line2 = Line(plate2_body.get_center(), rod.get_center(), color=BLACK)
        
        # Create magnetic field circles as ellipses (to show perspective)
        def create_b_circle_perspective(radius, pos, thickness):
            # Create ellipse with 3:1 ratio to show perspective
            ellipse = Ellipse(width=radius/5, height=radius, color=GREEN_E)
            ellipse.move_to(pos)
            ellipse.set_stroke(width=thickness)
            return ellipse
        
        # Create B field circles with thicker lines
        small_r = 1.0
        large_r = 4.0  # Increased by 50%
        left_pos = LEFT * 2.5
        mid_pos = ORIGIN
        
        # Triple the thickness of all lines while maintaining relative proportions
        b_small_left = create_b_circle_perspective(small_r, left_pos, 5)  # Was 1
        b_large_left = create_b_circle_perspective(large_r, left_pos, 8)  # Was 2
        b_small_mid = create_b_circle_perspective(small_r, mid_pos, 3)  # Was 0.5
        b_large_mid = create_b_circle_perspective(large_r, mid_pos, 8)    # Was 1
        
        # Electric field lines
        e_field_lines = VGroup()
        num_lines = 12
        line_spacing = 2.4 / (num_lines - 1)
        for i in range(num_lines):
            y_pos = -1.2 + i * line_spacing
            field_line = Arrow(
                start=LEFT * 0.8 + UP * y_pos,
                end=RIGHT * 0.8 + UP * y_pos,
                color=BLUE_E,
                buff=0,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.1
            )
            e_field_lines.add(field_line)
        
        # Current arrows
        i_arrow_left = Arrow(LEFT * 5, LEFT * 4, color=RED_E)
        i_arrow_right = Arrow(RIGHT * 4, RIGHT * 5, color=RED_E)
        i_label_left = Text("I", color=RED_E, font_size=24).next_to(i_arrow_left, LEFT)
        i_label_right = Text("I", color=RED_E, font_size=24).next_to(i_arrow_right, RIGHT)
        
        # Add everything to the scene at once
        self.add(
            plate1_back, plate2_back,
            plate1_body, plate2_body,
            plate1_front, plate2_front,
            rod, vert_line1, vert_line2,
            b_small_left, b_large_left,
            b_small_mid, b_large_mid,
            e_field_lines,
            i_arrow_left, i_arrow_right,
            i_label_left, i_label_right
        )
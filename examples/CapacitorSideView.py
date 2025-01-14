from manim import *

class CircularCapacitorSideView(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = WHITE
        
        # Create the main body of each plate (thinner rectangles)
        plate1_body = Rectangle(height=3.0, width=0.25, color=BLACK)
        plate2_body = Rectangle(height=3.0, width=0.25, color=BLACK)
        
        # Create elliptical ends for the plates
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
        
        # Fill the plates with solid color
        plate1_body.set_fill(color=GRAY, opacity=0.9)
        plate2_body.set_fill(color=GRAY, opacity=0.9)
        plate1_front.set_fill(color=GRAY, opacity=0.9)
        plate2_front.set_fill(color=GRAY, opacity=0.9)
        plate1_back.set_fill(color=GRAY_D, opacity=0.7)
        plate2_back.set_fill(color=GRAY_D, opacity=0.7)
        
        # Create connecting rod
        rod = Line(LEFT * 4, RIGHT * 4, color=BLACK)
        
        # Create current arrows
        i_arrow_left = Arrow(LEFT * 5, LEFT * 4, color=RED_E)  # Darker red
        i_arrow_right = Arrow(RIGHT * 4, RIGHT * 5, color=RED_E)
        i_label_left = Text("I", color=RED_E, font_size=24).next_to(i_arrow_left, LEFT)
        i_label_right = Text("I", color=RED_E, font_size=24).next_to(i_arrow_right, RIGHT)
        
        # Create vertical connections between plates and rod
        vert_line1 = Line(plate1_body.get_center(), rod.get_center(), color=BLACK)
        vert_line2 = Line(plate2_body.get_center(), rod.get_center(), color=BLACK)
        
        # Create electric field lines (horizontal lines between plates)
        e_field_lines = VGroup()
        num_lines = 12
        line_spacing = 2.4 / (num_lines - 1)
        for i in range(num_lines):
            y_pos = -1.2 + i * line_spacing
            field_line = Arrow(
                start=LEFT * 0.8 + UP * y_pos,
                end=RIGHT * 0.8 + UP * y_pos,
                color=BLUE_E,  # Darker blue
                buff=0,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.1
            )
            e_field_lines.add(field_line)
        
        # Create the drawing all at once (no animation)
        self.add(e_field_lines,
                plate1_back, plate2_back,
                plate1_body, plate2_body,
                plate1_front, plate2_front,
                rod, vert_line1, vert_line2,
                i_arrow_left, i_arrow_right, 
                i_label_left, i_label_right)
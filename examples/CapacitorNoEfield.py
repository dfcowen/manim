from manim import *

class CircularCapacitorSideView(Scene):
    def construct(self):
        # Create plate outlines (ellipses to show perspective)
        plate1 = Ellipse(width=0.8, height=3.0, color=WHITE)
        plate2 = Ellipse(width=0.8, height=3.0, color=WHITE)
        
        # Create the "thickness" of the plates
        plate1_back = Ellipse(width=0.8, height=3.0, color=WHITE)
        plate2_back = Ellipse(width=0.8, height=3.0, color=WHITE)
        
        # Position plates side by side
        plate1.shift(LEFT * 1)
        plate2.shift(RIGHT * 1)
        plate1_back.shift(LEFT * 1 + LEFT * 0.2)
        plate2_back.shift(RIGHT * 1 + LEFT * 0.2)
        
        # Create connecting rods
        rod = Line(LEFT * 4, RIGHT * 4, color=WHITE)
        
        
        # Create current arrows
        i_arrow_left = Arrow(LEFT * 5, LEFT * 4, color=RED)
        i_arrow_right = Arrow(RIGHT * 4, RIGHT * 5, color=RED)
        i_label_left = Text("I", color=RED, font_size=24).next_to(i_arrow_left, LEFT)
        i_label_right = Text("I", color=RED, font_size=24).next_to(i_arrow_right, RIGHT)
        
        # Create vertical connections between plates and rod
        vert_line1 = Line(plate1.get_center(), rod.get_center(), color=WHITE)
        vert_line2 = Line(plate2.get_center(), rod.get_center(), color=WHITE)
        
        # Add shading to plates
        plate1.set_fill(color=WHITE, opacity=0.2)
        plate2.set_fill(color=WHITE, opacity=0.2)
        
        # Create the drawing all at once (no animation)
        self.add(plate1_back, plate2_back, plate1, plate2, rod, 
                vert_line1, vert_line2,
                i_arrow_left, i_arrow_right, i_label_left, i_label_right)
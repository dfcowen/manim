from manim import *
import numpy as np

class ElectricFieldSymmetry(ThreeDScene):
    def construct(self):
        # Set up the scene with simpler camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Create a cylinder with lower resolution
        cylinder = Cylinder(
            height=8,
            radius=0.5,
            direction=RIGHT,
            resolution=(12, 12),  # Reduced resolution
            fill_opacity=0.5,
            fill_color=LIGHT_GRAY,
            stroke_width=1
        ).move_to(ORIGIN)
        
        # Add plus signs on the cylinder surface - significantly reduced quantity
        plus_signs = VGroup()
        num_plus_signs_around = 4  # Reduced from 8
        num_plus_signs_along = 4   # Reduced from 8
        
        for i in range(num_plus_signs_around):
            theta = i * 2 * PI / num_plus_signs_around
            for j in range(num_plus_signs_along):
                x = (j - num_plus_signs_along/2 + 0.5) * (7/num_plus_signs_along)
                plus_sign = Text("+", color=RED, font_size=16)
                r = cylinder.radius
                # Position the plus sign on the cylinder surface
                plus_sign.move_to(cylinder.get_center() + x * RIGHT + r * np.cos(theta) * UP + r * np.sin(theta) * OUT)
                plus_signs.add(plus_sign)
        
        # Group the cylinder and plus signs
        charged_cylinder = VGroup(cylinder, plus_signs)
        
        # Initial display of the cylinder - combine animations to reduce rendering steps
        self.play(Create(cylinder), Create(plus_signs), run_time=1.5)
        self.wait(1)
        
        # First rotation of the cylinder - CHANGED to rotate around vertical axis (UP)
        self.play(
            Rotate(
                charged_cylinder, 
                angle=PI, 
                axis=UP,  # Changed from RIGHT to UP for vertical axis rotation
                run_time=2
            )
        )
        self.wait(1.5)
        
        # Create the first set of electric field vectors (45 degrees) - reduced quantity
        vectors_45deg = VGroup()
        num_vectors_around = 4  # Reduced from 8
        num_vectors_along = 3   # Reduced from 4
        
        # Use built-in Arrow instead of custom creation function
        for i in range(num_vectors_around):
            theta = i * 2 * PI / num_vectors_around
            for j in range(num_vectors_along):
                x = (j - num_vectors_along/2 + 0.5) * (6/num_vectors_along)
                
                # Start point on cylinder surface
                start_point = cylinder.get_center() + x * RIGHT + cylinder.radius * np.cos(theta) * UP + cylinder.radius * np.sin(theta) * OUT
                
                # Vector direction (45 degrees from horizontal)
                radial_dir = np.array([0, np.cos(theta), np.sin(theta)])
                axial_dir = np.array([1, 0, 0])
                combined_dir = radial_dir + axial_dir
                direction = combined_dir / np.linalg.norm(combined_dir)
                
                # Create arrow using manim's built-in Arrow
                end_point = start_point + direction * 0.8
                arrow = Arrow(start_point, end_point, buff=0, color=RED, 
                              max_stroke_width_to_length_ratio=5,
                              max_tip_length_to_length_ratio=0.3)
                vectors_45deg.add(arrow)
        
        # Show the 45-degree vectors
        self.play(Create(vectors_45deg), run_time=1)
        self.wait(1)
        
        # Rotate the cylinder and vectors - CHANGED to rotate around vertical axis (UP)
        self.play(
            Rotate(
                VGroup(charged_cylinder, vectors_45deg), 
                angle=PI, 
                axis=UP,  # Changed from RIGHT to UP for vertical axis rotation
                run_time=2
            )
        )
        self.wait(1)
        
        # Fade out the first set of vectors
        self.play(FadeOut(vectors_45deg))
        
        # Create the second set of electric field vectors (90 degrees) - reduced quantity
        vectors_90deg = VGroup()
        for i in range(num_vectors_around):
            theta = i * 2 * PI / num_vectors_around
            for j in range(num_vectors_along):
                x = (j - num_vectors_along/2 + 0.5) * (6/num_vectors_along)
                
                # Start point on cylinder surface
                start_point = cylinder.get_center() + x * RIGHT + cylinder.radius * np.cos(theta) * UP + cylinder.radius * np.sin(theta) * OUT
                
                # Vector direction (90 degrees from horizontal, purely radial)
                direction = np.array([0, np.cos(theta), np.sin(theta)])
                
                # Create arrow
                end_point = start_point + direction * 0.8
                arrow = Arrow(start_point, end_point, buff=0, color=RED,
                             max_stroke_width_to_length_ratio=5,
                             max_tip_length_to_length_ratio=0.3)
                vectors_90deg.add(arrow)
        
        # Show the 90-degree vectors
        self.play(Create(vectors_90deg), run_time=1)
        self.wait(1)
        
        # Rotate the cylinder and vectors again - CHANGED to rotate around vertical axis (UP)
        self.play(
            Rotate(
                VGroup(charged_cylinder, vectors_90deg), 
                angle=PI, 
                axis=UP,  # Changed from RIGHT to UP for vertical axis rotation
                run_time=2
            )
        )
        self.wait(1)
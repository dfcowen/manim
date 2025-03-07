# Run with manim -pql ChargeAndEFieldSymmetry-v01.py ElectricFieldSymmetry (--disable_caching?)
# May want to salloc first: salloc -N 4 --partition=mgc-mri -t 1:00:00 --mem=64GB
# Remember to run conda activate manim first
from manim import *
import numpy as np

class ElectricFieldSymmetry(ThreeDScene):
    def construct(self):
        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Create a cylinder
        cylinder = Cylinder(
            height=8,
            radius=0.5,
            direction=RIGHT,
            resolution=(20, 20),
            fill_opacity=0.5,
            fill_color=LIGHT_GRAY,
            stroke_width=1
        ).move_to(ORIGIN)
        
        # Add plus signs on the cylinder surface
        plus_signs = VGroup()
        num_plus_signs_around = 8
        num_plus_signs_along = 8
        
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
        
        # Initial display of the cylinder
        self.play(Create(cylinder))
        self.play(Create(plus_signs))
        self.wait(1)
        
        # First rotation of the cylinder
        self.play(
            Rotate(
                charged_cylinder, 
                angle=PI, 
                axis=RIGHT,
                run_time=2
            )
        )
        self.wait(2)
        
        # Define a function to create arrows
        def create_arrow(start_point, direction, length=0.8, color=RED):
            end_point = start_point + direction * length
            line = Line(start_point, end_point, color=color)
            # Add a cone for arrowhead
            cone = Cone(base_radius=0.05, height=0.1, direction=direction, color=color)
            cone.move_to(end_point + direction * 0.05)
            return VGroup(line, cone)
        
        # Create the first set of electric field vectors (45 degrees)
        vectors_45deg = VGroup()
        num_vectors_around = 8
        num_vectors_along = 4
        
        for i in range(num_vectors_around):
            theta = i * 2 * PI / num_vectors_around
            for j in range(num_vectors_along):
                x = (j - num_vectors_along/2 + 0.5) * (7/num_vectors_along)
                
                # Start point on cylinder surface
                start_point = cylinder.get_center() + x * RIGHT + cylinder.radius * np.cos(theta) * UP + cylinder.radius * np.sin(theta) * OUT
                
                # Vector direction (45 degrees from horizontal)
                # Mix of radial and axial components
                radial_dir = np.array([0, np.cos(theta), np.sin(theta)])
                axial_dir = np.array([1, 0, 0])
                combined_dir = radial_dir + axial_dir
                direction = combined_dir / np.linalg.norm(combined_dir)
                
                # Create the arrow
                arrow = create_arrow(start_point, direction)
                vectors_45deg.add(arrow)
        
        # Show the 45-degree vectors
        self.play(Create(vectors_45deg))
        self.wait(1)
        
        # Rotate the cylinder and vectors
        self.play(
            Rotate(
                VGroup(charged_cylinder, vectors_45deg), 
                angle=PI, 
                axis=RIGHT,
                run_time=2
            )
        )
        self.wait(2)
        
        # Fade out the first set of vectors
        self.play(FadeOut(vectors_45deg))
        self.wait(1)
        
        # Create the second set of electric field vectors (90 degrees)
        vectors_90deg = VGroup()
        for i in range(num_vectors_around):
            theta = i * 2 * PI / num_vectors_around
            for j in range(num_vectors_along):
                x = (j - num_vectors_along/2 + 0.5) * (7/num_vectors_along)
                
                # Start point on cylinder surface
                start_point = cylinder.get_center() + x * RIGHT + cylinder.radius * np.cos(theta) * UP + cylinder.radius * np.sin(theta) * OUT
                
                # Vector direction (90 degrees from horizontal, purely radial)
                direction = np.array([0, np.cos(theta), np.sin(theta)])
                
                # Create the arrow
                arrow = create_arrow(start_point, direction)
                vectors_90deg.add(arrow)
        
        # Show the 90-degree vectors
        self.play(Create(vectors_90deg))
        self.wait(1)
        
        # Rotate the cylinder and vectors again
        self.play(
            Rotate(
                VGroup(charged_cylinder, vectors_90deg), 
                angle=PI, 
                axis=RIGHT,
                run_time=2
            )
        )
        self.wait(2)
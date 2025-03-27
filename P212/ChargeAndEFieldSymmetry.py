# conda activate manim
# manim render /storage/home/dfc13/manim/examples/ChargeAndEFieldSymmetry-v03.py ElectricFieldSymmetry -ql

from manim import *
import numpy as np

class ElectricFieldSymmetry(ThreeDScene):
    def construct(self):
        # Set up the scene with simpler camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Create a smoother cylinder with medium resolution
        CylinderHeight = 8
        cylinder = Cylinder(
            height=CylinderHeight,
            radius=0.8,
            direction=RIGHT,
            resolution=(12, 12),  # (circumference segments, height segments)
            checkerboard_colors=None,  # List of two colors for alternating squares
            #shade_in_3d=True,      # Whether to use 3D shading
            fill_opacity=0.8,
            fill_color=LIGHT_GRAY,
            stroke_width=0
        ).move_to(ORIGIN)
        
        # Add plus signs on the cylinder surface
        # The cylinder's central axis lies in the x direction
        plus_signs = VGroup()
        num_plus_signs_around = 4  # Reduced from 8
        num_plus_signs_along = 4   # Reduced from 8
        

        for i in range(num_plus_signs_around):
            theta = i * 2 * PI / num_plus_signs_around
            for j in range(num_plus_signs_along):
                x = (j - num_plus_signs_along/2 + 0.5) * ((CylinderHeight-1)/num_plus_signs_along)
                r = cylinder.radius
                
                # Calculate position on cylinder surface
                surface_point = cylinder.get_center() + x * RIGHT + r * np.cos(theta) * UP + r * np.sin(theta) * OUT
                
                # Create tangent plane vectors
                # Tangent along the cylinder axis
                tangent_axial = RIGHT  
                
                # Tangent perpendicular to the axis (tangent to the circular cross-section)
                tangent_circular = np.array([0, -np.sin(theta), np.cos(theta)])
                
                # Create the horizontal line segment
                # Use a hack to make the positive charges behind the cylinder look like they're behind it.
                # Here, I just make them a little bit smaller.
                # This works for the animation, too, because the charges behind the cylinder stay behind it for the chosen rotation.
                # Ideally the renderer would take care of this for us, but that requires opengl to work.
                in_front = -PI/2 < theta < PI/2
                if in_front: 
                    line_length = 0.2  # Adjust size as needed
                else:
                    line_length = 0.1
                horizontal_line = Line(
                    surface_point - line_length/2 * tangent_axial,
                    surface_point + line_length/2 * tangent_axial,
                    color=PURE_RED,
                    stroke_width=3
                )
                
                # Create the vertical line segment (perpendicular to horizontal line on the tangent plane)
                vertical_line = Line(
                    surface_point - line_length/2 * tangent_circular,
                    surface_point + line_length/2 * tangent_circular,
                    color=PURE_RED,
                    stroke_width=3
                )
                
                # Group both lines to form a plus sign
                plus_shape = VGroup(horizontal_line, vertical_line)
                
                # Add to the plus_signs group
                plus_signs.add(plus_shape)

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

        # Create a text message as part of the camera's display, not the 3D scene
        message = Text("The charge distribution looks the same.", font_size=24, color=WHITE)
        message.to_corner(DOWN + RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(message) # Add the text to the fixed orientation background (the "foreground")
        self.wait(3)
        self.remove_fixed_in_frame_mobjects(message) # To remove it later, we need to remove it from the fixed frame mobjects
        self.remove(message)
        self.wait(1)

        #self.wait(1.5)
        
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

        # Create a text message as part of the camera's display, not the 3D scene
        message = Text("Choose E field directions (incorrectly).", font_size=24, color=WHITE)
        message.to_corner(DOWN + RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(message) # Add the text to the fixed orientation background (the "foreground")
        self.wait(3)
        self.remove_fixed_in_frame_mobjects(message) # To remove it later, we need to remove it from the fixed frame mobjects
        self.remove(message)
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

        # Create a text message as part of the camera's display, not the 3D scene
        message = Text("E field is now different but charge distribution looks the same!", font_size=24, color=WHITE)
        message.to_corner(DOWN + RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(message) # Add the text to the fixed orientation background (the "foreground")
        self.wait(3)
        self.remove_fixed_in_frame_mobjects(message) # To remove it later, we need to remove it from the fixed frame mobjects
        self.remove(message)
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

        # Create a text message as part of the camera's display, not the 3D scene
        message = Text("Choose E field directions (correctly).", font_size=24, color=WHITE)
        message.to_corner(DOWN + RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(message) # Add the text to the fixed orientation background (the "foreground")
        self.wait(3)
        self.remove_fixed_in_frame_mobjects(message) # To remove it later, we need to remove it from the fixed frame mobjects
        self.remove(message)
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

        # Create a text message as part of the camera's display, not the 3D scene
        message = Text("E field looks the same, as it must since charge distribution also looks the same.", font_size=24, color=WHITE)
        message.to_corner(DOWN + RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(message) # Add the text to the fixed orientation background (the "foreground")
        self.wait(3)
        self.remove_fixed_in_frame_mobjects(message) # To remove it later, we need to remove it from the fixed frame mobjects
        self.remove(message)
        self.wait(1)
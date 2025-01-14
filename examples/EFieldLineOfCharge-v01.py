from manim import *
import numpy as np

class ElectricFieldLineCharge(Scene):
    def __init__(self, L=4.0, z=3.0, num_segments=8, **kwargs):
        self.L = L  # Length of line charge
        self.z = z  # Height of test point
        self.num_segments = num_segments  # Number of segments to show
        super().__init__(**kwargs)

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-self.L, self.L, 1],
            y_range=[-0.5, self.z + 0.5, 1],
            axis_config={"include_tip": True}
        ).scale(1.0)
        
        # Add labels
        x_label = Text("x").next_to(axes.x_axis, RIGHT)
        z_label = Text("z").next_to(axes.y_axis, UP)
        
        # Create line charge
        line_charge = Line(
            start=[-self.L/2, 0, 0],
            end=[self.L/2, 0, 0],
            color=RED
        ).set_stroke(width=4)
        
        # Create test point
        test_point = Dot([0, self.z, 0], color=BLUE)
        
        # Add basic elements
        self.add(axes, x_label, z_label, line_charge, test_point)

        # Create and animate field vectors
        segment_points = np.linspace(-self.L/2, self.L/2, self.num_segments)
        field_vectors = []
        
        for x in segment_points:
            # Calculate E-field vector components from this segment
            dx = 0 - x  # x-component of r
            dz = self.z - 0  # z-component of r
            r = np.sqrt(dx**2 + dz**2)
            
            # E-field vector (normalized for visualization)
            Ex = dx/r**3
            Ez = dz/r**3
            scale = 1.0  # Adjust for visibility
            
            # Create arrow for this segment's contribution
            vector = Arrow(
                start=[0, self.z, 0],
                end=[scale*Ex, self.z + scale*Ez, 0],
                color=YELLOW,
                buff=0
            )
            field_vectors.append(vector)
            
            # Show vector
            self.play(Create(vector))
            
        # Add vectors to make resultant
        # (This is simplified - you might want to add actual vector addition)
        resultant = Arrow(
            start=[0, self.z, 0],
            end=[0, self.z + 1, 0],  # Simplified - should calculate actual resultant
            color=GREEN,
            buff=0
        )
        
        self.play(Create(resultant))
        self.wait()

        if __name__ == "__main__":
            with tempconfig({"output_file": "ElectricField-v01"}):
                scene = ElectricFieldLineCharge()
                scene.render()
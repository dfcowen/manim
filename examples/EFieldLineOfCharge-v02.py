from manim import *
import numpy as np

class ElectricFieldLineCharge(Scene):
    def __init__(self, L=4.0, y=1.0, N=4, k=1.0, lambda_charge=1.0, **kwargs):
        self.L = L              # Length of line charge
        self.y = y              # Height of test point
        self.N = N              # Number of segments
        self.k = k              # Coulomb's constant (scaled for visualization)
        self.lambda_charge = lambda_charge  # Linear charge density
        self.dx = L/N           # Length of each segment
        self.dq = lambda_charge * self.dx  # Charge of each segment
        super().__init__(**kwargs)

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-self.L, self.L, 1],
            y_range=[-0.5, 4.0, 1],  # Set fixed range regardless of test point position
            axis_config={"include_tip": True}
        ).scale(1.0)
        
        # Add labels
        x_label = Text("x").next_to(axes.x_axis, RIGHT)
        y_label = Text("y").next_to(axes.y_axis, UP)
        
        # Create line charge
        # Find the x-axis y-coordinate position
        x_axis_y = axes.c2p(0, 0)[1]  # Get y-coordinate of the axes origin

        # Create line charge at the x-axis height
        line_charge = Line(
            start=[-self.L/2, x_axis_y, 0],  # Place at x-axis height
            end=[self.L/2, x_axis_y, 0],     # Place at x-axis height
            color=RED
        ).set_stroke(width=6)
        
        # Create test point
        test_point = Dot([0, self.y, 0], color=BLUE)
        
        # Add basic elements
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Create(line_charge),
            Create(test_point),
        )

        # Calculate and show contributions from each segment
        segment_centers = np.linspace(-self.L/2 + self.dx/2, self.L/2 - self.dx/2, self.N)
        total_Ex = 0
        total_Ey = 0
        scale = 3.0  # Scaling factor for vector visualization

        # Create initial total field vector (zero length)
        total_vector = Arrow(
            start=[0, self.y, 0],
            end=[0, self.y, 0],
            color=GREEN,
            buff=0,
            stroke_width=4
        )
        total_label = Text("E_total", color=GREEN).next_to(total_vector, LEFT, buff=0.5)
        self.add(total_vector, total_label)

        for i, x in enumerate(segment_centers):
            # Create visual segment at x-axis height
            x_axis_y = axes.c2p(0, 0)[1]  # Get y-coordinate of the axes origin
            segment = Line(
                start=[x - self.dx/2, x_axis_y, 0],
                end=[x + self.dx/2, x_axis_y, 0],
                color=YELLOW
            ).set_stroke(width=4)
            self.play(Create(segment))

            # Calculate E-field from this segment
            r = np.sqrt(x**2 + self.y**2)
            
            # Calculate dE components
            dE = self.k * self.dq / r**2
            dEx = -(dE * x/r)
            dEy = dE * self.y/r
            
            # Create dE vector
            dE_vector = Arrow(
                start=[0, self.y, 0],
                end=[scale*dEx, self.y + scale*dEy, 0],
                color=YELLOW,
                buff=0,
                stroke_width=4
            )
            dE_label = Text(f"dE{i+1}", color=YELLOW).next_to(dE_vector, RIGHT, buff=0.5)
            
            # Show dE vector
            self.play(
                Create(dE_vector),
                #Write(dE_label)
            )

            # Update total field
            total_Ex += dEx
            total_Ey += dEy
            
            # Update total field vector
            new_total = Arrow(
                start=[0, self.y, 0],
                end=[scale*total_Ex, self.y + scale*total_Ey, 0],
                color=GREEN,
                buff=0,
                stroke_width=4
            )
            
            # Update total vector
            self.play(
                Transform(total_vector, new_total),
                total_label.animate.next_to(new_total, LEFT, buff=0.5)
            )

            # Fade out segment contribution
            self.play(
                FadeOut(segment),
                FadeOut(dE_vector),
                FadeOut(dE_label)
            )

        self.wait()

if __name__ == "__main__":
    with tempconfig({"output_file": "ElectricField"}):
        scene = ElectricFieldLineCharge()
        scene.render()
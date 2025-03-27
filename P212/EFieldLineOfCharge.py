# Run with, e.g.,
#    python /storage/home/dfc13/manim/P212/EFieldLineOfCharge.py -pl

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
           y_range=[-0.5, 4.0, 1],
           axis_config={"include_tip": True}
       ).scale(1.0)
       
       # Add labels
       x_label = Text("x").next_to(axes.x_axis, RIGHT)
       y_label = Text("y").next_to(axes.y_axis, UP)
       
       # Create line charge using axes coordinates
       line_charge = Line(
           start=axes.coords_to_point(-self.L/2, 0),
           end=axes.coords_to_point(self.L/2, 0),
           color=RED
       ).set_stroke(width=10)
       line_charge_label = Text("+λ", color=RED).next_to(line_charge, DOWN+RIGHT, buff=0.1)
       
       # Create test point
       test_point = Dot(axes.coords_to_point(0, self.y), color=BLUE)
       test_point_label = Text("p").next_to(test_point, LEFT)
       
       # Add basic elements
       self.play(
           Create(axes),
           Write(x_label),
           Write(y_label),
           Create(line_charge),
           Write(line_charge_label),
           Create(test_point),
           Write(test_point_label),
       )

       # Calculate and show contributions from each segment
       segment_centers = np.linspace(-self.L/2 + self.dx/2, self.L/2 - self.dx/2, self.N)
       total_Ex = 0
       total_Ey = 0
       scale = 1.5  # Scaling factor for vector visualization

       # Create initial total field vector (zero length)
       total_vector = Arrow(
           start=axes.coords_to_point(0, self.y),
           end=axes.coords_to_point(0, self.y),
           color=GREEN,
           buff=0,
           stroke_width=4
       )
       #total_label = Text("E(P)", color=GREEN).next_to(total_vector, LEFT, buff=0.5)
       total_label = Text("E(p)", color=GREEN).next_to(total_vector.get_end(), RIGHT+DOWN, buff=0.1) # Put label near end of vector
       #total_label = MathTex(r"\vec{E}_\mathrm{tot}", color=GREEN).next_to(total_vector, LEFT, buff=0.5)

       #self.add(total_vector, total_label)
       self.add(total_vector)

       for i, x in enumerate(segment_centers):
           # Create visual segment using axes coordinates
           segment = Line(
               start=axes.coords_to_point(x - self.dx/2, 0),
               end=axes.coords_to_point(x + self.dx/2, 0),
               color=YELLOW
           ).set_stroke(width=4)
           self.play(Create(segment))

           # Calculate E-field from this segment
           r = np.sqrt(x**2 + self.y**2)
           
           # Calculate dE components
           dE = self.k * self.dq / r**2
           dEx = -(dE * x/r)
           dEy = dE * self.y/r
           
           # Create dE vector using axes coordinates
           dE_vector = Arrow(
               start=axes.coords_to_point(0, self.y),
               end=axes.coords_to_point(scale*dEx, self.y + scale*dEy),
               color=YELLOW,
               buff=0,
               stroke_width=4
           )
           #dE_label = Text(f"dE{i+1}", color=YELLOW).next_to(dE_vector, UR, buff=0.5)
           dE_label = Text(f"dE{i+1}", color=YELLOW).next_to(dE_vector.get_end(), UR, buff=0.1) # put dE label near end of vector

           
           # Show dE vector
#           self.play(
#               Create(dE_vector),
#               #Write(dE_label)
#           )
           self.play(Create(dE_vector))
           self.add(dE_label)

           # Update total field
           total_Ex += dEx
           total_Ey += dEy
           
           # Update total field vector using axes coordinates
           new_total = Arrow(
               start=axes.coords_to_point(0, self.y),
               end=axes.coords_to_point(scale*total_Ex, self.y + scale*total_Ey),
               color=GREEN,
               buff=0,
               stroke_width=4
           )

           # Fade out this dE contribution
           self.play(
               FadeOut(segment),
               FadeOut(dE_vector),
               FadeOut(dE_label)
           )

           # Update total vector
           self.play(
               Transform(total_vector, new_total),
               total_label.animate.next_to(new_total.get_end(), UR, buff=0.1) # put label near end of vector
               #total_label.animate.next_to(new_total, LEFT, buff=0.5)
           )


       self.wait()

if __name__ == "__main__":
   with tempconfig({"output_file": "ElectricField"}):
       scene = ElectricFieldLineCharge()
       scene.render()
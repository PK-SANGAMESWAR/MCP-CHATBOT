from manim import *

class LinearTransformation(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_basis_vectors=False,
            show_coordinates=True,
            leave_ghost_vectors=True,
        )
    
    def construct(self):
        # Add title
        title = Text("Linear Algebra: Matrix Transformation Demo", font_size=36)
        title.to_edge(UP)
        self.add_foreground_mobject(title)
        self.wait()
        
        # Define transformation matrix
        matrix = [[2, 1], [1, 1]]
        
        # Create basis vectors
        i_hat = Vector([1, 0], color=RED)
        j_hat = Vector([0, 1], color=BLUE)
        
        # Add labels for basis vectors
        i_label = MathTex(r"\hat{\imath}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_label = MathTex(r"\hat{\jmath}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Add basis vectors to the scene
        self.add_vector(i_hat)
        self.add_vector(j_hat)
        self.add(i_label, j_label)
        
        self.wait(1)
        
        # Show the transformation matrix
        matrix_tex = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}",
            font_size=36
        )
        matrix_tex.to_corner(UL).shift(DOWN * 0.8)
        self.add_foreground_mobject(matrix_tex)
        self.wait(1)
        
        # Apply the linear transformation
        self.apply_matrix(matrix)
        
        # Update labels to follow the transformed vectors
        transformed_i = Vector([2, 1], color=RED)
        transformed_j = Vector([1, 1], color=BLUE)
        
        new_i_label = MathTex(r"A\hat{\imath}", color=RED).next_to([2, 1, 0], RIGHT)
        new_j_label = MathTex(r"A\hat{\jmath}", color=BLUE).next_to([1, 1, 0], UP)
        
        self.play(
            Transform(i_label, new_i_label),
            Transform(j_label, new_j_label)
        )
        
        self.wait(2)

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def analyze_and_plot_ode(dxdt_str, dydt_str, x_range=(-5, 5), y_range=(-5, 5)):
    """
    Parses a 2D autonomous ODE system:
    dx/dt = f(x, y)
    dy/dt = g(x, y)
    Computes equilibrium points, Jacobian eigenvalues, and plots phase portrait.
    """
    x, y = sp.symbols('x y')
    
    # Step 1: Safely parse strings to SymPy expressions
    f = sp.sympify(dxdt_str)
    g = sp.sympify(dydt_str)
    
    # Step 2: Compute Equilibrium Points where dx/dt = 0 and dy/dt = 0
    equilibria_raw = sp.solve([f, g], (x, y), dict=True)
    real_equilibria = []
    for pt in equilibria_raw:
        px, py = pt[x], pt[y]
        if px.is_real and py.is_real:
            real_equilibria.append((float(px), float(py)))
            
    # Step 3: Compute Jacobian Matrix for stability analysis
    J = sp.Matrix([[sp.diff(f, x), sp.diff(f, y)],
                   [sp.diff(g, x), sp.diff(g, y)]])
    
    stability_analysis = []
    for (eq_x, eq_y) in real_equilibria:
        J_eval = J.subs({x: eq_x, y: eq_y})
        # Evaluate eigenvalues numerically
        eigenvals = [complex(v.evalf()) for v in J_eval.eigenvals().keys()]
        
        # Stability classification
        real_parts = [v.real for v in eigenvals]
        imag_parts = [v.imag for v in eigenvals]
        
        if all(r < 0 for r in real_parts):
            node_type = "Stable Attractor / Sink"
        elif all(r > 0 for r in real_parts):
            node_type = "Unstable Repeller / Source"
        elif any(r > 0 for r in real_parts) and any(r < 0 for r in real_parts):
            node_type = "Saddle Point (Unstable)"
        elif all(abs(r) < 1e-5 for r in real_parts) and any(abs(i) > 1e-5 for i in imag_parts):
            node_type = "Center (Neutral Orbit)"
        else:
            node_type = "Complex Dynamics / Spiral"
            
        stability_analysis.append({
            "point": (eq_x, eq_y),
            "eigenvalues": [str(ev) for ev in eigenvals],
            "type": node_type
        })
        
    # Step 4: Render Phase Portrait using Streamplot
    f_num = sp.lambdify((x, y), f, modules='numpy')
    g_num = sp.lambdify((x, y), g, modules='numpy')
    
    X, Y = np.meshgrid(
        np.linspace(x_range[0], x_range[1], 100),
        np.linspace(y_range[0], y_range[1], 100)
    )
    
    U = f_num(X, Y)
    V = g_num(X, Y)
    
    # Handle scalar constants if f or g does not contain both variables
    if not isinstance(U, np.ndarray):
        U = np.full_like(X, float(U))
    if not isinstance(V, np.ndarray):
        V = np.full_like(Y, float(V))
        
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Plot streamlines / trajectories
    ax.streamplot(X, Y, U, V, color='deepskyblue', density=1.2, linewidth=1, arrowsize=1.2)
    
    # Mark equilibrium points
    for eq in real_equilibria:
        ax.plot(eq[0], eq[1], 'ro', markersize=8, label=f"Eq ({eq[0]:.2f}, {eq[1]:.2f})")
        
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Phase Portrait: dx/dt = {dxdt_str}, dy/dt = {dydt_str}")
    ax.grid(True, linestyle="--", alpha=0.5)
    if real_equilibria:
        ax.legend()
        
    return fig, real_equilibria, stability_analysis
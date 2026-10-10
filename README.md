# Ordinary Differential Equation Physics Interpreter

Track: DeepMind Google (Gemma 4)  
Status: Working Prototype (24-Hour Hackathon Build)

# The Core Problem
it is a open source git repository which can be used at schools by the teachers to show their students the behavior and actual world application of differential equation. we are using gemma 4 to give a visual representation of differential equation.

# Our Solution
We bridges Gemma 4's multimodal reasoning with SymPy's deterministic computational engine. 

1. **Perception (Gemma 4):** The user uploads a raw image of a 2D differential equation system. Gemma 4 acts as a strict OCR agent, parsing the image into sanitized algebraic strings.
2. **Computation (SymPy & NumPy):** A pure Python backend takes over to safely compute Jacobian matrices, classify eigenvalues, evaluate equilibrium points, and render a precise vector phase field (eliminating AI hallucination).
3. **Synthesis (Gemma 4):** The model ingests the mathematical classifications and translates the abstract math back into a grounded, plain-English physical intuition (e.g., predator-prey dynamics, damped oscillators).

# Tech Stack
*   **AI:** Google Generative AI SDK (`models/gemma-4-26b-a4b-it` & `gemini-1.5-flash` fallback)
*   **Math Engine:** `sympy`, `numpy`
*   **Visualization:** `matplotlib`
*   **Frontend:** `streamlit`

# How to Run Locally
1. Clone the repository.
2. Create a `.env` file and add your `GEMINI_API_KEY`.
3. Run `pip install -r requirements.txt` (install streamlit, sympy, numpy, matplotlib, google-generativeai, python-dotenv).
4. Execute `streamlit run app.py`.

## Current Capabilities & Mathematical Boundaries

To ensure absolute deterministic stability during execution, the current math engine is strictly bounded to solve specific types of systems:

**Supported Systems (What works perfectly):**
* **2D Coupled First-Order ODEs:** Strictly systems defined as $dx/dt = f(x,y)$ and $dy/dt = g(x,y)$.
* **Autonomous Systems:** The equations must not contain explicit time dependency (no $t$ variable in the right-hand side).
* **Cartesian Variables:** The extracted variables must be specifically $x$ and $y$.
* **Polynomial & Simple Non-Linear Dynamics:** Safely processes systems with finite equilibrium points (e.g., Simple Harmonic Oscillators, Lotka-Volterra Predator-Prey models).

**Out of Scope (Will raise an error):**
* Single higher-order equations (e.g., 2nd-order ODEs) without manual state-space reduction.
* Non-autonomous systems (time-dependent fields cannot be plotted on a static 2D phase mesh).
* Complex transcendental equations (e.g., nested trigonometric functions) that cause analytical root-finding loops in SymPy.

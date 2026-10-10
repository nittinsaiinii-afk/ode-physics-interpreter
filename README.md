# Neuro-Symbolic Physics Interpreter 

Track: DeepMind Google (Gemma 4)  
Status: Working Prototype (24-Hour Hackathon Build)

# The Core Problem
Generative AI models are exceptional at parsing unstructured visual data but notoriously hallucinate when asked to compute deterministic calculus or evaluate dynamic physical systems. 
Traditional solvers (like MATLAB or SymPy) execute perfect math but cannot read messy, real-world handwritten equations. 

# Our Solution
We engineered a **Neuro-Symbolic Pipeline** that bridges Gemma 4's multimodal reasoning with SymPy's deterministic computational engine. 

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

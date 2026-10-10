import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
import math_engine

# Load Environment Variables securely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key is missing! Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Initialize the classic, stable GenAI client
genai.configure(api_key=api_key)
vision_model = genai.GenerativeModel('models/gemma-4-26b-a4b-it')

# ----- STREAMLIT UI CONFIG -----
st.set_page_config(page_title="ODE Physics Interpreter", layout="wide")
st.title("Differential Equation Physics Interpreter ⚙️")
st.markdown("Upload a photo of a 2D ODE system to see its phase portrait and physical meaning.")
# ----- SIDEBAR: SYSTEM LIMITATIONS -----
with st.sidebar:
    st.header("⚠️ System Capabilities")
    st.markdown("""
    **Supported Systems:**
    * **2D Coupled Systems:** Strictly 1st-order pairs ($dx/dt$, $dy/dt$).
    * **Autonomous:** No explicit time variable ($t$) in equations.
    * **Variables:** Must strictly use $x$ and $y$.
    
    **Not Supported (Will cause errors):**
    * Single 2nd-order equations ($d^2y/dx^2$).
    * Time-dependent vector fields.
    * Complex transcendental root-finding loops.
    """)
    st.divider()
    st.caption("Powered by Gemma 4 & SymPy")
# ----- UI LAYOUT -----
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("1. Upload Equation")
    uploaded_file = st.file_uploader("Upload Image (PNG, JPG)", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Equation", use_container_width=True)

        if st.button("Analyze System"):
            with st.spinner("Parsing equation via Gemini 1.5 Flash..."):
                try:
                    # Phase A: Multimodal Extraction Prompt
                    extraction_prompt = """
                    You are a strict mathematical OCR system. Look at the image of the differential equations.
                    Extract the equations for dx/dt and dy/dt. 
                    Format your response EXACTLY in this format, with no extra text or markdown:
                    DXDT: [your parsed dx/dt equation in sympy syntax]
                    DYDT: [your parsed dy/dt equation in sympy syntax]
                    
                    Example:
                    DXDT: y
                    DYDT: -x
                    """
                    
                    # Direct image passing with classic SDK
                    response = vision_model.generate_content([extraction_prompt, image])
                    
                    # Parse the raw text output
                    lines = response.text.strip().split('\n')
                    dxdt_str = ""
                    dydt_str = ""
                    for line in lines:
                        if line.startswith("DXDT:"):
                            dxdt_str = line.replace("DXDT:", "").strip()
                        elif line.startswith("DYDT:"):
                            dydt_str = line.replace("DYDT:", "").strip()
                    
                    st.success(f"Parsed Successfully!\n* dx/dt = {dxdt_str}\n* dy/dt = {dydt_str}")
                    
                    # Save to session state
                    st.session_state['dxdt'] = dxdt_str
                    st.session_state['dydt'] = dydt_str

                except Exception as e:
                    st.error(f"Failed to parse image via API: {e}")

with col2:
    if 'dxdt' in st.session_state and 'dydt' in st.session_state:
        st.subheader("2. Mathematical Reality & Phase Portrait")
        dxdt_val = st.session_state['dxdt']
        dydt_val = st.session_state['dydt']
        
        try:
            with st.spinner("Generating Phase Portrait..."):
                # Phase B & C: Deterministic Engine Execution
                fig, eq_points, analysis = math_engine.analyze_and_plot_ode(dxdt_val, dydt_val)
                st.pyplot(fig)
                
                with st.expander("Show Mathematical Breakdown"):
                    st.write("**Equilibrium Points:**", eq_points)
                    for item in analysis:
                        st.write(f"Point {item['point']}: {item['type']}")

            # Phase D: Physical Context Translation
            with st.spinner("Consulting AI for Physical Meaning..."):
                physics_prompt = f"""
                You are a university physics professor. 
                I have a 2D differential equation system:
                dx/dt = {dxdt_val}
                dy/dt = {dydt_val}
                
                The system has these equilibrium points and classifications: {analysis}.
                
                In one short, engaging paragraph, explain what this mathematical system represents in the real physical world. 
                Keep it grounded and explain what the trajectories (arrows in the phase portrait) actually mean in reality. 
                Do not regurgitate the math; explain the physics.
                """
                
                physics_response = vision_model.generate_content(physics_prompt)
                
                st.subheader("3. Physical Interpretation")
                st.info(physics_response.text)
                
        except Exception as e:
            st.error(f"Deterministic Math Engine failed to evaluate the equations. Ensure they are valid 2D equations. Error: {e}")
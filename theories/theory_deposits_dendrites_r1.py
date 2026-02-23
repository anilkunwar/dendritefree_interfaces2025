import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Dendrite Formation Models",
    page_icon="⚡",
    layout="centered"
)

# Title and introduction
st.title("⚡ Dendrite Formation Models in Metal-Ion Batteries")
st.markdown("""
This app presents a curated collection of theoretical models that describe the formation and growth 
of dendrites in metal (Li, Zn, Na, etc.) ion batteries. Each model is accompanied by its physical 
concepts, mathematical expression, original reference, and a summary of its applications and limitations.

*All mathematical formulas are rendered with LaTeX for clarity.*
""")

# Sidebar with additional info
st.sidebar.header("About this app")
st.sidebar.markdown("""
This interactive tool lets you explore key models of dendrite formation.  
Select a model from the dropdown to see its details.

**LaTeX rendering** is enabled throughout – look for formulas enclosed in `$...$` (inline) or `$$...$$` (display).
""")

# Data for each model (based on the table and summary provided)
models = [
    {
        "name": "Wranglen Theory (1960)",
        "mechanisms": "Concept of critical current density ($j_c$) in aqueous solutions; dendrites grow when the global or local current density exceeds $j_c$.",
        "math": "Condition for dendrite growth: $j_{\\text{global}} > j_c$ or $j_{\\text{local}} > j_c$",
        "reference": "G. Wranglen, *Electrochimica Acta* **1960**, 2, 130–132. [77]",
        "applications": [
            "Predicting the onset of dendrites in electrodeposition processes (e.g., metal plating).",
            "Used in early battery design to set safe current limits."
        ],
        "limitations": [
            "Limited to aqueous systems; ignores diffusion or overpotential kinetics.",
            "Does not account for SEI layers or solid electrolytes.",
            "Oversimplifies dendrite morphology (no branching prediction)."
        ]
    },
    {
        "name": "Barton–Bockris Model (1962) / Diggle et al. extension (1969)",
        "mechanisms": "Maximum velocity of dendrite growth in ionic solutions, assuming spherical diffusion and tip-controlled growth.",
        "math": "$v_{\\text{max}} = j_0 \\frac{V \\eta}{RT}$",
        "reference": "J. L. Barton & J. O. Bockris, *Proc. R. Soc. Lond. A* **1962**, 268, 485–505. [78]; J. W. Diggle et al., *J. Electrochem. Soc.* **1969**, 116, 1503. [79]",
        "applications": [
            "Analyzing growth rates in molten salts or liquid electrolytes.",
            "Applied in Li/Na battery simulations for velocity prediction under constant overpotential."
        ],
        "limitations": [
            "Assumes linear kinetics and static hemispheres; ignores inertial/mechanical forces.",
            "Limited to low overpotentials; not suitable for high-current or branched dendrites."
        ]
    },
    {
        "name": "Kim–Jorne Theory (1980)",
        "mechanisms": "Dendrite growth mechanism at the edge of a rotating disk electrode, focusing on mass transfer and limiting current.",
        "math": "$c_s = c_b \\left(1 - \\frac{j}{j_l}\\right)$ where $c_s$ = surface concentration, $c_b$ = bulk concentration, $j_l$ = limiting current density.",
        "reference": "J. T. Kim & J. Jorné, *J. Electrochem. Soc.* **1980**, 127, 8. [80]",
        "applications": [
            "Mass-transfer-limited processes in rotating electrodes.",
            "Used in electrochemical engineering for zinc/metal deposition control in batteries."
        ],
        "limitations": [
            "Specific to rotating disks and liquid electrolytes; ignores electric fields or stress.",
            "Limited to edge effects; does not model full 3D growth or solid systems."
        ]
    },
    {
        "name": "Chazalviel Model (1990)",
        "mechanisms": "Theory of ramified metallic deposits growth via electrodeposition in the presence of high electric fields; space‑charge buildup leads to dendrites.",
        "math": r"$\nabla \cdot (D_a \nabla c_a + \mu_a c_a \nabla \phi - v_a c_a) = 0$, where $v_a$ is filament growth velocity at the anode.",
        "reference": "J.-N. Chazalviel, *Phys. Rev. A* **1990**, 42, 7355–7367. [81]",
        "applications": [
            "High-current regimes in polymer/liquid electrolytes.",
            "Predicts induction time (Sand's time); applied in Li‑polymer cells for dendrite onset forecasting."
        ],
        "limitations": [
            "Applies only above the limiting current; neglects surface effects or mechanics.",
            "Assumes binary electrolytes; limited validation for low currents or solid systems."
        ]
    },
    {
        "name": "Whisker Model (1998) – Yamaki et al.",
        "mechanisms": "Whisker growth driven by competition between deposition and dissolution currents, and by Laplace pressure from curvature.",
        "math": r"Deformation caused by pressure difference $\Delta P = \gamma \left( \frac{1}{R_1} + \frac{1}{R_2} \right)$",
        "reference": "J. Yamaki et al., *J. Power Sources* **1998**, 74, 219–227. [82]",
        "applications": [
            "Low‑current whisker formation in organic electrolytes.",
            "Used in symmetric Li cells to explain root‑controlled growth and morphologies."
        ],
        "limitations": [
            "Focuses on whiskers, not full dendrites; ignores high‑current branching.",
            "Limited to specific electrolytes; does not quantify initiation time accurately."
        ]
    },
    {
        "name": "Monroe–Newman Model (2003)",
        "mechanisms": "Dendrite propagation in lithium/polymer cells under galvanostatic conditions; surface‑energy controlled with tip curvature.",
        "math": "$j_L = \\frac{2c_b D F}{(1-t^0_+)L}$",
        "reference": "C. Monroe & J. Newman, *J. Electrochem. Soc.* **2003**, 150, A1377. [83]",
        "applications": [
            "Polymer electrolytes; predicts growth velocity/height.",
            "Applied to design stiff electrolytes (shear modulus criterion: $Y > 2 Y_{\\text{Li}}$)."
        ],
        "limitations": [
            "Assumes elastic deformation only (ignores plasticity).",
            "Limited to parallel electrodes; overestimates suppression threshold."
        ]
    },
    {
        "name": "Internal Resistance Theory (2008) – Park et al.",
        "mechanisms": "Links dendrite growth to temperature‑dependent internal resistance; uses Sand's time and critical current.",
        "math": r"Sand's time $\tau = \frac{\pi D (C_0 q_e)^2}{\left(2 J t_a\right)^2}$, critical current $J^* = \frac{8 \tau J^2 t_a}{\pi C_0 q_e L}$",
        "reference": "H. E. Park et al., *J. Power Sources* **2008**, 178, 765–768. [84]",
        "applications": [
            "Temperature effects in Li secondary batteries.",
            "Used to optimize operating conditions for dendrite suppression."
        ],
        "limitations": [
            "Focuses on resistance/temperature; ignores mechanics or SEI.",
            "Does not model morphology evolution."
        ]
    },
    {
        "name": "Heterogeneous Nucleation Model (2013) – Ely & Garcia",
        "mechanisms": "Nucleation at heterointerfaces; overpotential‑controlled critical radius for dendrite stability.",
        "math": "Equation incomplete in source (critical radius concept).",
        "reference": "D. R. Ely & R. E. García, *J. Electrochem. Soc.* **2013**, 160, A662. [85]",
        "applications": [
            "Predicting deposit morphology and energy barriers in negative electrodes.",
            "Applied in anode design to understand nucleation preferences."
        ],
        "limitations": [
            "Limited to early nucleation stages; ignores full growth.",
            "Assumes ideal interfaces; does not include diffusion/stress."
        ]
    },
    {
        "name": "Akolkar Model (2013)",
        "mechanisms": "Quantification of current density at dendrite tip versus flat surface under activation control.",
        "math": r"$\frac{j_t}{j_f} = \Big \{ \frac{-1}{b C_0} \ln \Big ( e^{-b C_0} + \frac{j_f}{j_{L,f}} (1 - e^{-b C_0}) \Big ) \Big \}^{-\frac{\alpha_c}{n}}$",
        "reference": "R. Akolkar, *J. Power Sources* **2013**, 232, 23–28. [86]",
        "applications": [
            "Low‑current activation‑limited growth; sub‑ambient temperature extensions.",
            "Used in Li electrodeposition simulations."
        ],
        "limitations": [
            "Assumes pure activation control; ignores mass transfer at high currents.",
            "Limited to early stages; does not include mechanics."
        ]
    },
    {
        "name": "Stress-Driven Dendrite Growth (2018) – Wang et al.",
        "mechanisms": "Residual stress during electrodeposition drives growth; stress relaxation on soft substrates mitigates dendrites.",
        "math": r"Chemical potential of metallic filament $\mu_m = \mu_0 - \sigma \Omega$; critical stress $\sigma_0 = \frac{RT}{F D_m} j r$",
        "reference": "X. Wang et al., *Nature Energy* **2018**, 3, 227–235. [87]",
        "applications": [
            "Design of dendrite‑free anodes using soft substrates (e.g., polymer).",
            "Explains stress‑relief mechanisms in electrodes."
        ],
        "limitations": [
            "Focuses on stress; ignores electrokinetics.",
            "Limited to specific substrates; does not model high‑rate or solid electrolytes fully."
        ]
    },
    {
        "name": "Preferential Growth Model (2023) – Zhu et al.",
        "mechanisms": "Dendrite growth pathway along grain boundaries in solid electrolytes, driven by electron accumulation.",
        "math": r"$\theta = \frac{4 \pi r^3 n_{\text{Li}} \rho_{\text{Li}}}{3A}$",
        "reference": "C. Zhu et al., *Nature Communications* **2023**, 14, 1300. [76]",
        "applications": [
            "Solid electrolytes (e.g., LLZO); predicts penetration at defects.",
            "Applied in garnet‑type SSE design."
        ],
        "limitations": [
            "Limited to grain boundaries in solids; ignores liquids or low‑defect systems.",
            "Assumes electron trapping dominates; experimental validation ongoing."
        ]
    }
]

# Dropdown to select a model
model_names = [m["name"] for m in models]
selected_name = st.selectbox("Select a model", model_names)

# Find the selected model dictionary
selected_model = next(m for m in models if m["name"] == selected_name)

# Display the information
st.header(selected_model["name"])

# Physics (Mechanisms) – using markdown for LaTeX rendering
st.subheader("📘 Physics / Mechanisms")
st.markdown(selected_model["mechanisms"])

# Mathematical expression – using markdown to support mixed text/LaTeX
st.subheader("📐 Mathematical Expression")
st.markdown(selected_model["math"])

# Reference
st.subheader("📄 Reference")
st.markdown(selected_model["reference"])

# Applications
st.subheader("✅ Applications")
for app in selected_model["applications"]:
    st.markdown(f"- {app}")

# Limitations
st.subheader("⚠️ Limitations")
for lim in selected_model["limitations"]:
    st.markdown(f"- {lim}")

# Optional separator and footer
st.markdown("---")
st.markdown("⬆️ Use the dropdown to explore other models.")

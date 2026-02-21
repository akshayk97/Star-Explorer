import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Star Explorer",
    page_icon="⭐",
    layout="wide"
)

# ---------------- GLOBAL FONT (Open Sans) ---------------- #

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Open Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-weight:700;'>⭐ Star Explorer</h1>", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    return pd.read_csv("data/stars.csv")

df = load_data()

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Star Parameters")
st.sidebar.subheader("Preset Stars")

presets = {
    "Sun ☀": {"T": 5778, "L": 1.0, "R": 1.0, "M": 4.8},
    "Betelgeuse 🔴": {"T": 3500, "L": 120000, "R": 950, "M": -5.6},
    "Sirius ⭐": {"T": 9940, "L": 25.4, "R": 1.7, "M": 1.4},
    "Proxima Centauri 🔵": {"T": 3042, "L": 0.0017, "R": 0.15, "M": 15.5}
}

selected_preset = st.sidebar.selectbox(
    "Choose a preset star (optional)",
    ["Custom"] + list(presets.keys())
)

if selected_preset != "Custom":
    preset = presets[selected_preset]
    default_temp = preset["T"]
    default_lum = preset["L"]
    default_rad = preset["R"]
    default_mag = preset["M"]
else:
    default_temp = 5778
    default_lum = 1.0
    default_rad = 1.0
    default_mag = 4.8

temperature = st.sidebar.slider("Temperature (K)", 2000, 40000, int(default_temp), 100)

luminosity = st.sidebar.slider(
    "Luminosity (L/Lo)",
    min_value=0.0001,
    max_value=1_000_000.0,
    value=float(default_lum),
    step=0.1
)

radius = st.sidebar.slider("Radius (R/Ro)", 0.01, 1000.0, float(default_rad), 0.1)
magnitude = st.sidebar.slider("Absolute Magnitude", -20.0, 20.0, float(default_mag), 0.1)

# ---------------- PHYSICS CLASSIFICATION ---------------- #

def physics_classification(temp, lum, radius):
    if lum > 100000:
        return "Supergiant"
    elif radius > 10 and lum > 100:
        return "Giant"
    elif temp > 8000 and radius < 0.5:
        return "White Dwarf"
    elif temp < 4000 and lum < 0.01:
        return "Red Dwarf"
    else:
        return "Main Sequence"

def explanation(star_type, temp, lum, radius):
    if star_type == "Giant":
        return f"High luminosity ({lum:.2f}) and large radius ({radius:.2f}) suggest an expanded stellar envelope."
    elif star_type == "Supergiant":
        return "Extremely high luminosity indicates a massive evolved star."
    elif star_type == "White Dwarf":
        return "Hot surface but very small radius suggests a compact stellar remnant."
    elif star_type == "Red Dwarf":
        return "Cool and low-luminosity star with low mass."
    else:
        return "Stable hydrogen-burning star in equilibrium."

star_type = physics_classification(temperature, luminosity, radius)

# ---------------- LAYOUT ---------------- #

col1, col2 = st.columns([2, 1])

# ================= LEFT PANEL (HR DIAGRAM) ================= #

with col1:
    st.markdown("### 🌌 Hertzsprung–Russell Diagram")

    fig = go.Figure()

    # Safe marker scaling
    log_l = np.log10(df["L"].clip(lower=1e-4))
    sizes = 10 + (log_l - log_l.min()) * 6

    fig.add_trace(go.Scatter(
        x=df["Temperature"],
        y=df["L"],
        mode="markers",
        marker=dict(
            size=sizes,
            color=df["Temperature"],
            colorscale="Inferno_r",
            opacity=0.85
        ),
        hovertemplate=
        "Temperature: %{x} K<br>" +
        "Luminosity: %{y:.4f}<extra></extra>",
        name="Stars"
    ))

    # Selected star
    fig.add_trace(go.Scatter(
        x=[temperature],
        y=[luminosity],
        mode="markers",
        marker=dict(
            size=22,
            color="#FF6B6B",
            line=dict(width=2, color="white")
        ),
        name="Selected Star"
    ))

    fig.update_layout(
        height=680,  # Taller chart
        margin=dict(l=60, r=40, t=40, b=60),
        paper_bgcolor="#0E1117",
        plot_bgcolor="#1c1d1f",
        font=dict(
            family="Open Sans, sans-serif",
            color="#BBBBBB"
        ),
        xaxis=dict(
            title="Temperature (K)",
            autorange="reversed",
            color="#BBBBBB"
        ),
        yaxis=dict(
            title="Luminosity",
            type="log",
            range=[-4, 6],
            color="#BBBBBB"
        ),
        legend=dict(
            bgcolor="#1E1E1E",
            font=dict(color="white")
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= RIGHT PANEL ================= #

with col2:

    # Big Section Header
    st.markdown(
        """
        <div style='
            font-size:30px;
            font-weight:700;
            color:white;
            margin-bottom:15px;
        '>
            Classification
        </div>
        """,
        unsafe_allow_html=True
    )

    # Star Type
    st.markdown(
        f"""
        <div style='
            font-size:26px;
            font-weight:600;
            color:#4FC3F7;
            margin-bottom:10px;
        '>
             {star_type}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(explanation(star_type, temperature, luminosity, radius))

    st.markdown("---")

    # Current Parameters Section
    st.markdown(
        """
        <div style='
            font-size:22px;
            font-weight:600;
            color:white;
            margin-bottom:10px;
        '>
            Current Parameters
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='
            font-size:18px;
            color:#DDDDDD;
            line-height:1.8;
        '>
            • Temperature: {temperature} K<br>
            • Luminosity: {luminosity:.4f}<br>
            • Radius: {radius:.2f}<br>
            • Absolute Magnitude: {magnitude}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        <div style='
            font-size:22px;
            font-weight:600;
            color:white;
            margin-bottom:10px;
        '>
            About
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <div style='
        font-size:18px;
        color:#DDDDDD;
        line-height:1.6;
    '>
        <b>Interactive Hertzsprung–Russell Diagram & Stellar Classification Tool.</b><br><br>
        This tool visualizes stellar classification using simplified 
        physical heuristics on the Hertzsprung–Russell diagram.
        It is designed for educational exploration of stellar properties.
    </div>
    """,
    unsafe_allow_html=True
)
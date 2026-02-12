import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

# ----------------------------------------------------------------------
# Streamlit page configuration
# ----------------------------------------------------------------------
st.set_page_config(page_title="Dendrite Control Roadmap", layout="wide")
st.title("Dendrite Control Strategy Roadmap")
st.markdown("Vision: **Dendrite‑Free High‑Energy Batteries by 2040**")

# ----------------------------------------------------------------------
# Build the matplotlib figure
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

# ----- Curved road (quadratic Bezier) -----
P0 = np.array([1.0, 3.0])   # 2025
P1 = np.array([5.0, 1.2])   # 2035 dip
P2 = np.array([9.0, 3.0])   # 2040

verts = [P0, P1, P2]
codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
path = Path(verts, codes)

# Road base
road_patch = patches.PathPatch(path, facecolor='none',
                               edgecolor='#555555', linewidth=22, alpha=0.5)
ax.add_patch(road_patch)
# Road edge (dashed white)
road_edge = patches.PathPatch(path, facecolor='none',
                              edgecolor='white', linewidth=3, linestyle='dashed')
ax.add_patch(road_edge)

# ----- Bezier interpolation for milestone positions -----
def bezier_quad(t, p0, p1, p2):
    return (1-t)**2 * p0 + 2*(1-t)*t * p1 + t**2 * p2

pos_start = bezier_quad(0.0, P0, P1, P2)
pos_mid   = bezier_quad(0.5, P0, P1, P2)
pos_end   = bezier_quad(1.0, P0, P1, P2)

# ----- Year labels -----
ax.text(pos_start[0], pos_start[1]+0.3, '2025', fontsize=16,
        ha='center', va='bottom', weight='bold')
ax.text(pos_mid[0], pos_mid[1]-0.4, '2035', fontsize=16,
        ha='center', va='top', weight='bold')
ax.text(pos_end[0], pos_end[1]+0.3, '2040', fontsize=16,
        ha='center', va='bottom', weight='bold')

# ----- Chinese zodiac animals (emojis) -----
ax.text(pos_start[0], pos_start[1]+0.1, '🐍', fontsize=40,
        ha='center', va='center')
ax.text(pos_mid[0], pos_mid[1]-0.1, '🐇', fontsize=40,
        ha='center', va='center')
ax.text(pos_end[0], pos_end[1]+0.1, '🐒', fontsize=40,
        ha='center', va='center')

# ----- Battery with / without dendrites -----
def draw_battery(ax, x, y, dendrites=True):
    w, h = 0.65, 0.35
    # main body
    rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2.5,
                             edgecolor='black', facecolor='#d9d9d9')
    ax.add_patch(rect)
    # terminals
    ax.plot([x + w/2, x + w/2 + 0.12], [y, y], 'k-', linewidth=2.5)
    ax.plot([x - w/2, x - w/2 - 0.12], [y, y], 'k-', linewidth=2.5)
    ax.text(x + w/2 + 0.06, y, '+', fontsize=14, ha='center', va='center')
    ax.text(x - w/2 - 0.06, y, '-', fontsize=14, ha='center', va='center')

    if dendrites:
        # red spiky dendrites
        for ang in np.linspace(-0.6, 0.6, 6):
            dx = 0.25 * np.cos(ang * np.pi)
            dy = 0.25 * np.sin(ang * np.pi)
            ax.plot([x + dx, x + 0.5*dx], [y + dy, y + 0.5*dy],
                    color='#c44e3a', linewidth=2.2)
        for ang in np.linspace(2.5, 3.7, 5):
            dx = 0.25 * np.cos(ang)
            dy = 0.25 * np.sin(ang)
            ax.plot([x + dx, x + 0.5*dx], [y + dy, y + 0.5*dy],
                    color='#c44e3a', linewidth=2.2)
        for i in range(4):
            ax.plot([x - 0.2, x - 0.45], [y - 0.1 + i*0.07, y - 0.15 + i*0.07],
                    color='#c44e3a', linewidth=2)

# Battery at 2025 (with dendrites)
draw_battery(ax, pos_start[0] - 0.7, pos_start[1] - 0.8, dendrites=True)
ax.text(pos_start[0] - 0.7, pos_start[1] - 1.15, 'DENDRITES', fontsize=10,
        ha='center', va='center', weight='bold', color='#a12d1f')

# Battery at 2040 (dendrite‑free)
draw_battery(ax, pos_end[0] + 0.7, pos_end[1] - 0.8, dendrites=False)
ax.text(pos_end[0] + 0.7, pos_end[1] - 1.15, 'DENDRITE‑FREE', fontsize=10,
        ha='center', va='center', weight='bold', color='#1f7a3d')

# ----- Start and end signs -----
# START sign (green)
start_x, start_y = pos_start[0] - 0.9, pos_start[1] + 0.7
start_sign = patches.Rectangle((start_x-0.4, start_y-0.2), 0.8, 0.4,
                               linewidth=3, edgecolor='#1f7a3d',
                               facecolor='#b8e0b8', alpha=0.9)
ax.add_patch(start_sign)
ax.text(start_x, start_y, 'START', fontsize=16, ha='center', va='center',
        weight='bold', color='#1f4d1f')

# END sign (red)
end_x, end_y = pos_end[0] + 0.9, pos_end[1] + 0.7
end_sign = patches.Rectangle((end_x-0.4, end_y-0.2), 0.8, 0.4,
                             linewidth=3, edgecolor='#b33f2f',
                             facecolor='#f9c2c2', alpha=0.9)
ax.add_patch(end_sign)
ax.text(end_x, end_y, 'END', fontsize=16, ha='center', va='center',
        weight='bold', color='#7a2e2e')

# ----- Subtle timeline description -----
ax.text(0.5, 0.2, 'Snake (2025) → Rabbit (2035) → Monkey (2040)',
        fontsize=11, ha='left', va='center', style='italic', color='#4f4f4f')

plt.tight_layout()

# ----------------------------------------------------------------------
# Display the figure in Streamlit
# ----------------------------------------------------------------------
st.pyplot(fig)

# ----------------------------------------------------------------------
# Optional: Add some interactive explanation
# ----------------------------------------------------------------------
with st.expander("📘 About this roadmap"):
    st.markdown("""
    - **2025 (Year of the Snake)**: Current state – batteries with dendrite growth issues.
    - **2035 (Year of the Rabbit)**: Intermediate milestone – advanced control strategies.
    - **2040 (Year of the Monkey)**: Vision – fully dendrite‑free, safe high‑energy batteries.
    """)

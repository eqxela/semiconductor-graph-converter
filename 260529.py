from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib as mpl
import numpy as np

mpl.rcParams['font.family'] = 'DejaVu Sans'

fig, ax = plt.subplots(figsize=(11, 4), dpi=300)

# -------------------------
# Base layers
# -------------------------
substrate = Rectangle((0, 0), 10, 1.2,
                      facecolor='#d0d0d0',
                      edgecolor='black',
                      linewidth=1.5)

oxide = Rectangle((0, 1.2), 10, 0.65,
                  facecolor='#cfe8ff',
                  edgecolor='black',
                  linewidth=1.5)

# -------------------------
# Bottom-contact electrodes
# -------------------------
# Cr
cr_left = Rectangle((1.3, 1.85), 1.2, 0.06,
                    facecolor='#5f5f5f',
                    edgecolor='black',
                    linewidth=1)

cr_right = Rectangle((7.5, 1.85), 1.2, 0.06,
                     facecolor='#5f5f5f',
                     edgecolor='black',
                     linewidth=1)

# Au
au_left = Rectangle((1.3, 1.91), 1.2, 0.22,
                    facecolor='#efc84a',
                    edgecolor='black',
                    linewidth=1)

au_right = Rectangle((7.5, 1.91), 1.2, 0.22,
                     facecolor='#efc84a',
                     edgecolor='black',
                     linewidth=1)

# -------------------------
# MoS2 flake
# touching SiO2 and overlapping electrodes
# -------------------------
mos2_x = [2.0, 2.0, 2.5, 7.5, 8.0, 8.0]
mos2_y = [2.13, 1.86, 1.86, 1.86, 1.86, 2.13]

ax.fill(mos2_x, mos2_y,
        facecolor='#7755aa',
        edgecolor='black',
        linewidth=1.2,
        zorder=5)

# -------------------------
# AuNPs directly attached
# -------------------------
np_positions = np.linspace(2.7, 7.3, 8)

for x in np_positions:
    # nanoparticle radius
    r = 0.11
    
    # attach directly to MoS2 top surface
    center_y = 2.13 + r
    
    ax.add_patch(
        Circle((x, center_y),
               r,
               facecolor='#d4af37',
               edgecolor='black',
               linewidth=0.8,
               zorder=6)
    )

# -------------------------
# Add base patches
# -------------------------
for item in [
    substrate, oxide,
    cr_left, cr_right,
    au_left, au_right
]:
    ax.add_patch(item)

# -------------------------
# Labels
# -------------------------
ax.text(5, 0.55,
        'n++ Si substrate (As doped)',
        ha='center',
        va='center',
        fontsize=12)

ax.text(5, 1.53,
        'SiO$_2$ (100 nm)',
        ha='center',
        va='center',
        fontsize=11)

ax.text(5, 2.02,
        'MoS$_2$',
        ha='center',
        va='center',
        fontsize=11,
        color='#4b2e83')

# Electrode labels repositioned
ax.text(1.2, 2.02,
        'Au (20 nm)',
        ha='right',
        va='center',
        fontsize=9)

ax.text(1.9, 1.70,
        'Cr (5 nm)',
        ha='center',
        fontsize=9)

ax.text(8.8, 2.02,
        'Au (20 nm)',
        ha='left',
        va='center',
        fontsize=9)

ax.text(8.1, 1.70,
        'Cr (5 nm)',
        ha='center',
        fontsize=9)

ax.text(1.9, 2.62,
        'Source',
        ha='center',
        fontsize=10)

ax.text(8.1, 2.62,
        'Drain',
        ha='center',
        fontsize=10)

ax.text(2.7, 2.58,
        'AuNPs',
        fontsize=10)

# -------------------------
# Style
# -------------------------
ax.set_xlim(0, 10)
ax.set_ylim(0, 3.0)
ax.axis('off')

plt.tight_layout()

png_path = "mos2_bottom_contact_schematic_v3.png"
pdf_path = "mos2_bottom_contact_schematic_v3.pdf"

plt.savefig(png_path, bbox_inches='tight', transparent=True)
plt.savefig(pdf_path, bbox_inches='tight', transparent=True)

print("Saved:", png_path)
print("Saved:", pdf_path)

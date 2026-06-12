import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages

# ─────────────────────────────────────────────────────────────
# UML primitives
# ─────────────────────────────────────────────────────────────

def initial_node(ax, x, y, r=0.18):
    ax.add_patch(plt.Circle((x, y), r, color='black', zorder=6))

def final_node(ax, x, y, r=0.23):
    ax.add_patch(plt.Circle((x, y), r, color='black', fill=False, lw=2.2, zorder=6))
    ax.add_patch(plt.Circle((x, y), r * 0.55, color='black', zorder=6))

def activity(ax, cx, cy, w, h, text, fs=8):
    rect = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                   boxstyle="round,pad=0.12",
                                   facecolor='#FFFDE7', edgecolor='#444', lw=1.4, zorder=5)
    ax.add_patch(rect)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
            multialignment='center', zorder=6)

def decision(ax, cx, cy, size, text='', fs=7):
    pts = [[cx, cy+size], [cx+size*1.8, cy], [cx, cy-size], [cx-size*1.8, cy]]
    ax.add_patch(plt.Polygon(pts, facecolor='#E3F2FD', edgecolor='#444', lw=1.4, zorder=5))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
            multialignment='center', zorder=6)

def merge_node(ax, cx, cy, size=0.28):
    pts = [[cx, cy+size], [cx+size*1.5, cy], [cx, cy-size], [cx-size*1.5, cy]]
    ax.add_patch(plt.Polygon(pts, facecolor='white', edgecolor='#444', lw=1.4, zorder=5))

def arrow_v(ax, x, y1, y2, label='', lside='right', fs=7):
    """Vertical arrow from y1 down to y2."""
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    if label:
        ox = 0.18 if lside == 'right' else -0.18
        ax.text(x + ox, (y1+y2)/2 + 0.1, label, fontsize=fs, color='#1565C0',
                fontstyle='italic', zorder=7)

def arrow_h(ax, x1, x2, y, label='', fs=7):
    """Horizontal arrow."""
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    if label:
        ax.text((x1+x2)/2, y + 0.13, label, ha='center', fontsize=fs,
                color='#1565C0', fontstyle='italic', zorder=7)

def line_h(ax, x1, x2, y):
    ax.plot([x1, x2], [y, y], 'k-', lw=1.2, zorder=3)

def line_v(ax, x, y1, y2):
    ax.plot([x, x], [y1, y2], 'k-', lw=1.2, zorder=3)

def arrow_end(ax, x, y, direction='down'):
    """Arrow head at end of a path segment."""
    if direction == 'down':
        ax.annotate('', xy=(x, y), xytext=(x, y+0.01),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    elif direction == 'right':
        ax.annotate('', xy=(x, y), xytext=(x-0.01, y),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)

def guard(ax, x, y, text, fs=7, color='#1565C0'):
    ax.text(x, y, text, fontsize=fs, color=color, fontstyle='italic', zorder=7)

def swimlane_frame(ax, lanes, xs, y_bot, y_top, hdr=0.7):
    for i, name in enumerate(lanes):
        xl, xr = xs[i], xs[i+1]
        # header
        ax.add_patch(patches.Rectangle((xl, y_top - hdr), xr-xl, hdr,
                                        facecolor='#CFD8DC', edgecolor='#333', lw=1.5, zorder=2))
        ax.text((xl+xr)/2, y_top - hdr/2, name, ha='center', va='center',
                fontsize=9, fontweight='bold', zorder=3)
        # body
        ax.add_patch(patches.Rectangle((xl, y_bot), xr-xl, y_top-hdr-y_bot,
                                        facecolor='white', edgecolor='#333', lw=1.5, zorder=1))


# ══════════════════════════════════════════════════════════════
# ACTIVITY DIAGRAM 1 — Search for a Building
# ══════════════════════════════════════════════════════════════

def activity_diagram_1(ax):
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 23)
    ax.axis('off')

    ax.text(8, 22.6, 'Activity Diagram 1: Search for a Building',
            ha='center', fontsize=12, fontweight='bold', zorder=8)
    ax.text(8, 22.2, 'Smart Campus Navigation App  |  MSc-DS-2025-10-0041',
            ha='center', fontsize=8, color='gray', zorder=8)

    # Swimlane columns: User | Mobile App UI | Navigation Service | Campus Map DB
    xs = [0.2, 4.2, 8.2, 12.2, 15.8]
    lanes = ['User', 'Mobile App UI', 'Navigation Service', 'Campus Map DB']
    swimlane_frame(ax, lanes, xs, y_bot=0.3, y_top=21.9, hdr=0.7)

    uc = (xs[0]+xs[1])/2   # 2.2
    mc = (xs[1]+xs[2])/2   # 6.2
    nc = (xs[2]+xs[3])/2   # 10.2
    dc = (xs[3]+xs[4])/2   # 14.0
    W, H = 3.4, 0.62

    # ── USER ──
    initial_node(ax, uc, 20.8)
    arrow_v(ax, uc, 20.62, 20.05)
    activity(ax, uc, 19.72, W, H, 'Open Campus App')
    arrow_v(ax, uc, 19.41, 18.84)
    activity(ax, uc, 18.51, W, H, 'Tap Search Bar')
    arrow_v(ax, uc, 18.20, 17.63)
    activity(ax, uc, 17.30, W, H, 'Enter Building Name')
    arrow_v(ax, uc, 16.99, 16.42)
    activity(ax, uc, 16.09, W, H, 'Tap Search / Submit')
    # cross-lane arrow to Mobile App
    arrow_h(ax, xs[1], xs[1]+0.5, 15.78)
    ax.annotate('', xy=(mc-W/2, 15.78), xytext=(xs[1]+0.5, 15.78),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)

    # ── MOBILE APP UI ──
    activity(ax, mc, 15.45, W, H, 'Receive Search Input')
    arrow_v(ax, mc, 15.14, 14.57)
    decision(ax, mc, 14.18, 0.37, 'Input\nValid?', fs=7)

    # [No] branch — goes left to error box
    guard(ax, mc - 1.9, 13.82, '[No]', fs=7)
    # left from decision
    line_h(ax, mc - 0.67, mc - 2.0, 14.18)
    arrow_v(ax, mc - 2.0, 14.18, 13.65)
    activity(ax, mc - 2.05, 13.32, 1.85, 0.62, 'Show Error\nMessage', fs=7.5)
    # error box feeds back down to merge
    line_v(ax, mc - 2.05, 13.01, 12.55)
    line_h(ax, mc - 2.05, mc - 0.42, 12.55)

    # [Yes] branch
    guard(ax, mc + 0.72, 13.82, '[Yes]', fs=7)
    arrow_v(ax, mc, 13.81, 13.18)
    # [Yes] also comes to merge
    line_v(ax, mc, 13.18, 12.55)

    # merge node
    merge_node(ax, mc, 12.2)
    ax.annotate('', xy=(mc, 12.48), xytext=(mc, 12.48+0.01),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    arrow_v(ax, mc, 11.92, 11.35)
    activity(ax, mc, 11.02, W, H, 'Send Query to\nNavigation Service')
    arrow_h(ax, mc + W/2, nc - W/2 - 0.05, 10.71)

    # ── NAVIGATION SERVICE ──
    activity(ax, nc, 10.38, W, H, 'Receive Search Query')
    arrow_v(ax, nc, 10.07, 9.50)
    activity(ax, nc, 9.17, W, H, 'Validate & Parse Query')
    arrow_h(ax, nc + W/2, dc - W/2 - 0.05, 8.86)

    # ── CAMPUS MAP DB ──
    activity(ax, dc, 8.53, W, H, 'Search Building Records')
    arrow_v(ax, dc, 8.22, 7.65)
    decision(ax, dc, 7.26, 0.37, 'Building\nFound?', fs=7)

    # [No] — left branch
    guard(ax, dc - 2.3, 6.90, '[No]', fs=7)
    line_h(ax, dc - 0.67, dc - 2.1, 7.26)
    arrow_v(ax, dc - 2.1, 7.26, 6.73)
    activity(ax, dc - 2.15, 6.40, 1.85, 0.62, 'Return "Not\nFound" Result', fs=7.5)

    # [Yes] — down
    guard(ax, dc + 0.72, 6.90, '[Yes]', fs=7)
    arrow_v(ax, dc, 6.89, 6.32)
    activity(ax, dc, 5.99, W, H, 'Return Building\nData & Location')

    # both merge at nav service level
    # [No] path: down then left
    line_v(ax, dc - 2.15, 6.09, 5.5)
    line_h(ax, dc - 2.15, nc - 0.42, 5.5)
    # [Yes] path: left
    arrow_h(ax, dc - W/2, nc + W/2 + 0.05, 5.68)

    # merge node at Navigation Service
    merge_node(ax, nc, 5.3)
    ax.annotate('', xy=(nc, 5.58), xytext=(nc, 5.59),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)

    # [No] feeds into merge from left
    ax.annotate('', xy=(nc - 0.42, 5.3), xytext=(nc - 2.0, 5.3),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    line_v(ax, nc - 2.0, 5.5, 5.3)

    arrow_v(ax, nc, 5.02, 4.45)
    activity(ax, nc, 4.12, W, H, 'Format Results &\nSend to App')
    arrow_h(ax, nc - W/2, mc + W/2 + 0.05, 3.81)

    # ── MOBILE APP UI (final display) ──
    activity(ax, mc, 3.48, W, H, 'Display Search\nResults / No Match')
    arrow_h(ax, mc - W/2, uc + W/2 + 0.05, 3.17)

    # ── USER final ──
    activity(ax, uc, 2.84, W, H, 'View Results &\nSelect Building')
    arrow_v(ax, uc, 2.53, 1.9)
    final_node(ax, uc, 1.72)


# ══════════════════════════════════════════════════════════════
# ACTIVITY DIAGRAM 2 — Get Directions
# ══════════════════════════════════════════════════════════════

def activity_diagram_2(ax):
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 23)
    ax.axis('off')

    ax.text(8, 22.6, 'Activity Diagram 2: Get Directions',
            ha='center', fontsize=12, fontweight='bold', zorder=8)
    ax.text(8, 22.2, 'Smart Campus Navigation App  |  MSc-DS-2025-10-0041',
            ha='center', fontsize=8, color='gray', zorder=8)

    xs = [0.2, 4.2, 8.2, 12.2, 15.8]
    lanes = ['User', 'Mobile App UI', 'Navigation Service', 'Campus Map DB']
    swimlane_frame(ax, lanes, xs, y_bot=0.3, y_top=21.9, hdr=0.7)

    uc = (xs[0]+xs[1])/2
    mc = (xs[1]+xs[2])/2
    nc = (xs[2]+xs[3])/2
    dc = (xs[3]+xs[4])/2
    W, H = 3.4, 0.62

    # ── USER ──
    initial_node(ax, uc, 20.8)
    arrow_v(ax, uc, 20.62, 20.05)
    activity(ax, uc, 19.72, W, H, 'Select Destination\nfrom Results')
    arrow_v(ax, uc, 19.41, 18.84)
    activity(ax, uc, 18.51, W, H, 'Tap "Get Directions"')
    arrow_h(ax, xs[1], mc - W/2 - 0.05, 18.20)

    # ── MOBILE APP UI ──
    activity(ax, mc, 17.87, W, H, 'Detect Current\nLocation (GPS)')
    arrow_v(ax, mc, 17.56, 16.99)
    decision(ax, mc, 16.60, 0.37, 'GPS\nAvailable?', fs=7)

    # [No] — prompt user to enter location
    guard(ax, mc - 2.3, 16.24, '[No]', fs=7)
    line_h(ax, mc - 0.67, mc - 2.1, 16.60)
    arrow_v(ax, mc - 2.1, 16.60, 16.07)
    activity(ax, mc - 2.15, 15.74, 1.85, 0.62, 'Prompt User to\nEnter Location', fs=7.5)
    line_v(ax, mc - 2.15, 15.43, 15.1)
    line_h(ax, mc - 2.15, mc - 0.42, 15.1)

    # [Yes]
    guard(ax, mc + 0.72, 16.24, '[Yes]', fs=7)
    arrow_v(ax, mc, 16.23, 15.65)
    line_v(ax, mc, 15.65, 15.1)

    # merge
    merge_node(ax, mc, 14.75)
    ax.annotate('', xy=(mc - 0.42, 14.75), xytext=(mc - 2.0, 14.75),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    line_v(ax, mc - 2.0, 15.1, 14.75)
    arrow_v(ax, mc, 14.47, 13.90)
    activity(ax, mc, 13.57, W, H, 'Package Request\n(origin + destination)')
    arrow_h(ax, mc + W/2, nc - W/2 - 0.05, 13.26)

    # ── NAVIGATION SERVICE ──
    activity(ax, nc, 12.93, W, H, 'Receive Directions\nRequest')
    arrow_v(ax, nc, 12.62, 12.05)
    decision(ax, nc, 11.66, 0.37, 'Accessibility\nMode On?', fs=7)

    # [Yes] → fetch from DB
    guard(ax, nc + 0.72, 11.30, '[Yes]', fs=7)
    arrow_h(ax, nc + 0.67, dc - W/2 - 0.05, 11.66)

    # [No] — bypass, go directly to route map request
    guard(ax, nc - 2.3, 11.30, '[No]', fs=7)
    line_h(ax, nc - 0.67, nc - 1.5, 11.66)
    line_v(ax, nc - 1.5, 11.66, 10.5)
    ax.annotate('', xy=(nc - 0.42, 10.5), xytext=(nc - 1.5, 10.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)

    # ── CAMPUS MAP DB ──
    activity(ax, dc, 11.33, W, H, 'Fetch Accessibility\nData (elevators/ramps)')
    arrow_v(ax, dc, 11.02, 10.45)
    activity(ax, dc, 10.12, W, H, 'Return Accessibility\nInfo to Nav Service')
    arrow_h(ax, dc - W/2, nc + W/2 + 0.05, 9.81)

    # Nav requests map segments from DB
    activity(ax, nc, 10.17, W, H, 'Request Route Map\nData from DB')
    # merge node at nc
    merge_node(ax, nc, 9.5)
    ax.annotate('', xy=(nc, 9.78), xytext=(nc, 9.79),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    # [Yes] path returns come in from right
    ax.annotate('', xy=(nc + 0.42, 9.5), xytext=(nc + 2.0, 9.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    line_v(ax, nc + 2.0, 9.81, 9.5)
    arrow_v(ax, nc, 9.22, 8.65)
    arrow_h(ax, nc + W/2, dc - W/2 - 0.05, 9.5 - 0.3)

    # DB returns route data
    activity(ax, dc, 8.99, W, H, 'Return Map /\nRoute Segments')
    arrow_h(ax, dc - W/2, nc + W/2 + 0.05, 8.68)

    activity(ax, nc, 8.32, W, H, 'Compute Optimal\nRoute & ETA')
    arrow_v(ax, nc, 8.01, 7.44)
    decision(ax, nc, 7.05, 0.37, 'Route\nFound?', fs=7)

    # [No]
    guard(ax, nc - 2.3, 6.69, '[No]', fs=7)
    line_h(ax, nc - 0.67, nc - 2.1, 7.05)
    arrow_v(ax, nc - 2.1, 7.05, 6.52)
    activity(ax, nc - 2.15, 6.19, 1.85, 0.62, 'Generate Error\nResponse', fs=7.5)
    line_v(ax, nc - 2.15, 5.88, 5.5)
    line_h(ax, nc - 2.15, nc - 0.42, 5.5)

    # [Yes]
    guard(ax, nc + 0.72, 6.69, '[Yes]', fs=7)
    arrow_v(ax, nc, 6.68, 6.11)
    activity(ax, nc, 5.78, W, H, 'Send Route +\nETA to App')
    arrow_v(ax, nc, 5.47, 5.35)
    line_v(ax, nc, 5.35, 5.0)
    # [No] feeds in from left
    merge_node(ax, nc, 5.0)
    ax.annotate('', xy=(nc - 0.42, 5.0), xytext=(nc - 2.0, 5.0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.3), zorder=4)
    line_v(ax, nc - 2.0, 5.5, 5.0)
    arrow_h(ax, nc - W/2, mc + W/2 + 0.05, 4.72)

    # ── MOBILE APP UI (final) ──
    activity(ax, mc, 4.39, W, H, 'Render Turn-by-Turn\nDirections on Map')
    arrow_v(ax, mc, 4.08, 3.51)
    activity(ax, mc, 3.18, W, H, 'Display ETA &\nAccessibility Notes')
    arrow_h(ax, mc - W/2, uc + W/2 + 0.05, 2.87)

    # ── USER final ──
    activity(ax, uc, 2.54, W, H, 'Follow Route on\nMap / Arrive')
    arrow_v(ax, uc, 2.23, 1.65)
    final_node(ax, uc, 1.47)


# ══════════════════════════════════════════════════════════════
# SEQUENCE DIAGRAM — Search for Faculty Office and Get Directions
# ══════════════════════════════════════════════════════════════

def sequence_diagram(ax):
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 27)
    ax.axis('off')

    ax.text(9, 26.55, 'Sequence Diagram: Search for Faculty Office and Get Directions',
            ha='center', fontsize=11, fontweight='bold', zorder=8)
    ax.text(9, 26.1, 'Smart Campus Navigation App  |  MSc-DS-2025-10-0041',
            ha='center', fontsize=8.5, color='gray', zorder=8)

    # ── Lifelines ──
    lx = {'user': 2.0, 'app': 6.5, 'nav': 11.5, 'db': 16.5}
    lnames = {'user': '«actor»\n:User', 'app': ':Mobile App UI',
              'nav': ':Navigation Service', 'db': ':Map Database'}
    lcolors = {'user': '#FFF9C4', 'app': '#E8F5E9', 'nav': '#E3F2FD', 'db': '#FCE4EC'}

    box_top = 25.7
    box_h = 0.7
    for key in lx:
        bw = 2.8
        bx, by = lx[key] - bw/2, box_top - box_h
        ax.add_patch(patches.FancyBboxPatch((bx, by), bw, box_h,
                                             boxstyle="round,pad=0.1",
                                             facecolor=lcolors[key], edgecolor='#444',
                                             lw=1.6, zorder=5))
        ax.text(lx[key], by + box_h/2, lnames[key], ha='center', va='center',
                fontsize=8.5, fontweight='bold', zorder=6)
        ax.plot([lx[key], lx[key]], [0.5, by], 'k--', lw=1.0, zorder=2)

    # ── Activation bar helper ──
    def act_bar(key, y_top, y_bot, w=0.22):
        ax.add_patch(patches.Rectangle((lx[key]-w/2, y_bot), w, y_top-y_bot,
                                        facecolor='#B0BEC5', edgecolor='#444',
                                        lw=0.8, zorder=4))

    # ── Message helpers ──
    def sync_arrow(x1, x2, y, label, fs=8.2):
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.5,
                                    mutation_scale=13), zorder=5)
        ax.text((x1+x2)/2, y+0.15, label, ha='center', fontsize=fs, zorder=6)

    def ret_arrow(x1, x2, y, label, fs=7.8):
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.3,
                                    linestyle='dashed', mutation_scale=11), zorder=5)
        ax.text((x1+x2)/2, y+0.15, label, ha='center', fontsize=fs,
                fontstyle='italic', color='#424242', zorder=6)

    def async_arrow(x1, x2, y, label, fs=8.2):
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5,
                                    mutation_scale=13), zorder=5)
        ax.text((x1+x2)/2, y+0.15, label, ha='center', fontsize=fs,
                color='#1565C0', zorder=6)

    def self_arrow(key, y_start, y_end, label, fs=7.8):
        xv = lx[key] + 0.11
        off = 1.0
        ax.plot([xv, xv+off, xv+off, xv], [y_start, y_start, y_end, y_end],
                'k-', lw=1.3, zorder=4)
        ax.annotate('', xy=(xv, y_end), xytext=(xv+off+0.01, y_end),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.3,
                                    mutation_scale=10), zorder=5)
        ax.text(xv+off+0.12, (y_start+y_end)/2, label, ha='left', va='center',
                fontsize=fs, zorder=6)

    # ── Sequence ──
    # Activation bars
    act_bar('user', 24.9, 22.0)
    act_bar('app',  24.7, 19.8)
    act_bar('nav',  24.0, 19.8)
    act_bar('db',   23.3, 22.6)

    y = 24.5
    sync_arrow(lx['user']+0.14, lx['app']-1.4, y, 'searchFaculty(professorName)')
    y -= 0.7
    sync_arrow(lx['app']+1.4, lx['nav']-0.14, y, 'findFacultyOffice(professorName)')
    y -= 0.7
    sync_arrow(lx['nav']+0.14, lx['db']-1.4, y, 'queryFaculty(professorName)')

    # ── ALT fragment ──
    alt_top  = y - 0.15   # top of the combined fragment = 22.65
    # We'll place messages, then set alt_bot at end

    # [faculty found] section — messages after query
    y -= 0.65
    ret_arrow(lx['db']-1.4, lx['nav']+0.14, y, 'return officeLocation + buildingID')
    y -= 0.65
    self_arrow('nav', y, y-0.42, 'computeRoute(origin, dest)')
    y -= 0.65
    async_arrow(lx['nav']+0.14, lx['db']-1.4, y, 'getMapSegments(routeID)')
    # DB activation for map
    act_bar('db', y+0.08, y-0.42)
    y -= 0.55
    ret_arrow(lx['db']-1.4, lx['nav']+0.14, y, 'return mapData + walkTime')
    y -= 0.62
    ret_arrow(lx['nav']-0.14, lx['app']+1.4, y, 'return directions + ETA')
    y -= 0.62
    ret_arrow(lx['app']-1.4, lx['user']+0.14, y, 'displayDirections(route, ETA)')

    alt_mid = y - 0.35   # divider = 18.39

    # [faculty not found] section
    y = alt_mid - 0.5
    # Re-draw short DB activation for not-found
    act_bar('db', alt_top - 0.55, y + 0.1)
    ret_arrow(lx['db']-1.4, lx['nav']+0.14, y, 'return null / empty result')
    y -= 0.65
    ret_arrow(lx['nav']-0.14, lx['app']+1.4, y, 'return error("Faculty not found")')
    y -= 0.65
    ret_arrow(lx['app']-1.4, lx['user']+0.14, y, 'showErrorMessage("Faculty not found")')

    alt_bot = y - 0.35   # bottom of alt block

    # Draw the alt box last (so it's behind messages but drawn over lifelines)
    bx, bw = 0.4, 17.2
    alt_h = alt_top - alt_bot
    ax.add_patch(patches.Rectangle((bx, alt_bot), bw, alt_h,
                                    facecolor='none', edgecolor='#3949AB',
                                    lw=1.8, linestyle='--', zorder=3))
    # 'alt' label tab
    tab_w, tab_h = 1.0, 0.45
    ax.add_patch(patches.Rectangle((bx, alt_top - tab_h), tab_w, tab_h,
                                    facecolor='#E8EAF6', edgecolor='#3949AB', lw=1.5, zorder=4))
    ax.text(bx + tab_w/2, alt_top - tab_h/2, 'alt', ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#3949AB', zorder=5)

    # [found] guard
    ax.text(bx + tab_w + 0.15, alt_top - tab_h/2, '[faculty found]',
            fontsize=8.5, color='#1B5E20', fontstyle='italic', va='center', zorder=5)

    # divider
    ax.plot([bx, bx+bw], [alt_mid, alt_mid], color='#3949AB', lw=1.2,
            linestyle='--', zorder=3)

    # [not found] guard
    ax.text(bx + tab_w + 0.15, alt_mid - 0.22, '[faculty not found]',
            fontsize=8.5, color='#B71C1C', fontstyle='italic', zorder=5)

    # ── Post alt: user taps start navigation ──
    y_p = alt_bot - 0.65
    act_bar('user', y_p+0.12, y_p-0.55)
    act_bar('app',  y_p+0.05, y_p-0.38)
    act_bar('nav',  y_p-0.2,  y_p-0.95)
    sync_arrow(lx['user']+0.14, lx['app']-1.4, y_p, 'tapStartNavigation()')
    y_p -= 0.65
    async_arrow(lx['app']+1.4, lx['nav']-0.14, y_p, 'startLiveNavigation(route)')
    y_p -= 0.62
    ret_arrow(lx['nav']-0.14, lx['app']+1.4, y_p, 'return stepInstructions[]')
    y_p -= 0.62
    ret_arrow(lx['app']-1.4, lx['user']+0.14, y_p, 'renderMapWithTurnByTurn()')

    # Legend box (bottom-right)
    lbx, lby = 12.5, 1.0
    ax.add_patch(patches.FancyBboxPatch((lbx, lby), 5.0, 2.4,
                                         boxstyle="round,pad=0.1",
                                         facecolor='#FAFAFA', edgecolor='#777',
                                         lw=1.2, zorder=5))
    ax.text(lbx+2.5, lby+2.1, 'Legend', ha='center', fontsize=9,
            fontweight='bold', zorder=6)
    # sync
    ax.annotate('', xy=(lbx+1.8, lby+1.7), xytext=(lbx+0.3, lby+1.7),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.4), zorder=6)
    ax.text(lbx+2.0, lby+1.7, 'Synchronous call', fontsize=7.5, va='center', zorder=6)
    # async
    ax.annotate('', xy=(lbx+1.8, lby+1.25), xytext=(lbx+0.3, lby+1.25),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.4), zorder=6)
    ax.text(lbx+2.0, lby+1.25, 'Asynchronous call', fontsize=7.5, va='center',
            color='#1565C0', zorder=6)
    # return
    ax.annotate('', xy=(lbx+1.8, lby+0.8), xytext=(lbx+0.3, lby+0.8),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.3,
                                linestyle='dashed'), zorder=6)
    ax.text(lbx+2.0, lby+0.8, 'Return message', fontsize=7.5, va='center',
            color='#424242', fontstyle='italic', zorder=6)


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

out = '/Users/abhaychaturvedi/Documents/dfl/notes/term-3/Software-systems/assignments/Assignment2_MSc-DS-2025-10-0041.pdf'

with PdfPages(out) as pdf:
    for fn, fsz in [(activity_diagram_1, (14, 21)),
                    (activity_diagram_2, (14, 21)),
                    (sequence_diagram,   (16, 25))]:
        fig, ax = plt.subplots(figsize=fsz)
        fig.patch.set_facecolor('white')
        fn(ax)
        plt.tight_layout(pad=0.3)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

print(f'Saved: {out}')

from drafter import *
from dataclasses import dataclass
from typing import List

set_site_information(
    author="wrenrust@udel.edu",
    description="""This website includes an interactive online tracker for 
    which state parks you've visited.""",
    sources=[],
    planning=["plan.pdf"],
    links=["https://ud-f25-cs1.github.io/honors-hackathon-2025-rust/"]
)
#hide_debug_information()
set_website_title("Delaware State Parks Passport")
set_website_framed(False)

# --- Website settings ---
hide_debug_information()

# Use the uploaded image file path as the passport cover.
# (Your environment will serve /mnt/data/webpassport.png as an asset.)
PASSPORT_IMAGE_PATH = "images/passport-image.png"

add_website_css("body", """
    margin: 0;
    display: flex;
    justify-content: center;
    background: #f7fffc;
""")

# --- Consolidated CSS for layout and look ---

# Background
add_website_css("body", "background: #f6fdf9; font-family: system-ui, -apple-system, sans-serif;")

# Layout
add_website_css(".page-row", "display: flex; gap: 3rem; align-items: flex-start; padding: 2rem;")
add_website_css(".passport-left", "flex: 0 0 360px; display: flex; align-items: center; justify-content: center;")
add_website_css(".passport-right", "flex: 1; padding-top: 0;") # Removed padding-top

# ---------- Navbar Styling ----------
add_website_css(".navbar button", """
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    

    border: 1px solid #ccc;
    background: #ffffff;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
""")

add_website_css(".navbar", """
    display: flex;
    align-items: center;
    justify-content: flex-end;
    text-align: center;
    color: #131c3e;
    width: 100%;
    height: 60px;

""")

add_website_css(".navbar", """ 
    display: flex; 
    justify-content: 
    width: 100%;
    flex-end; /* Align controls to the right */ 
    padding: 1rem 3rem; background: #131c3e;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05); """)

add_website_css(".navbar .controls", "margin-bottom: 0;")
add_website_css(".navbar button", "border: 1px solid #ccc; background: #fff; padding: 0.5rem 1rem; border-radius: 6px;")
add_website_css(".navbar button:hover", "background: #f0f0f0;")


# Passport Cover (Height: 560px)
add_website_css(".passport-cover", """
    width: 360px;
    height: 560px; 
    border-radius: 22px;
    overflow: hidden;
    background: #0f1a3a;
    box-shadow: 0 8px 0 rgba(0,0,0,0.08);
""")

# ---------- Grid Container (Responsive for Squares) ----------
add_website_css(".parks-grid", """
    display: flex;
    flex-wrap: wrap;
    gap: 12px;           /* space between tiles */
    max-width: 500px;    /* optional: controls line breaks */
""")


# ---------- Park Tiles (The Square Trick) ----------
add_website_css(".park-tile-wrapper", """
    position: relative;
    width: 100px;
    height: 100px;
    flex: 0 0 100px;   /* prevents flex from resizing it */
""")


add_website_css(".park-tile", """
    position: absolute;
    inset: 0;             /* shorthand for top/left/right/bottom: 0 */
    
    background: #87af9c;
    text-color: #0f1a3a;
    padding: 12px;
    border-radius: 18px;

    display: flex;
    align-items: center;
    justify-content: center;

    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border: 1px solid #ddd;
""")


add_website_css(".park-name", """
    font-weight: 700;
    font-size: 13px; /* Smaller font for small squares */
    line-height: 1.2;
    color: #0f1a3a;
    text-align: center;
    padding: 10px; /* Internal padding to prevent text touching edges */
""")

# Checkbox Button (Rectangle Indicator)
add_website_css(".park-button-indicator", """
    all: unset; /* Remove default button styles */
    position: absolute;
    top: -8px;
    right: -8px;
    border-radius: 6px; 
    border: 4px solid #131c3e;
    background: white;
    cursor: pointer;
    padding: 0;
    box-sizing: border-box;
    display: block;
    line-height: 0;
    font-size: 0;
    flex: display;
    justify-content: flex-end;
    align-items: center;
    width: 10px;
    height: 10px;
""")

add_website_css(".park-button-indicator.checked", "background: #0b2540;")

add_website_css(".controls", "display: flex; gap: 0.8rem; " \
    "text-align: center;"
    "display: flex;"
    "align-items: center;"
    "justify-content: center;"
    "color: #0b2540;")

add_website_css(".park-info-page", """
    padding: 3rem;
    font-family: system-ui, sans-serif;
""")

add_website_css(".park-info-title", """
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 1rem;
    color: #0b2540;
""")

add_website_css(".park-info-status", """
    font-size: 1.2rem;
    margin-bottom: 2rem;
""")
add_website_css(".tile-link-overlay", """
    all: unset;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
    background: transparent;
    border: none;
    outline: none;
    border-radius: 18px;
    pointer-events: auto;
    z-index: 2;
""")
add_website_css(".tile-overlay", """
    all: unset;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
    background: transparent;
    border: none;
    outline: none;
    border-radius: 18px;
    pointer-events: auto;
    z-index: 2;
""")




# --- Data structures ---
@dataclass
class State:
    parks: List[str]
    visited: List[bool]


# --- Helper functions ---
def make_tile(index: int, name: str, visited: bool) -> PageContent:
    indicator_classes = ["park-button-indicator"]
    if visited:
        indicator_classes.append("checked")

    indicator_button = Button(
        "",
        "toggle_park",
        Argument("park_index", index),
        classes=indicator_classes
    )

    tile_overlay = Button(
        "",
        "park_info",
        Argument("park_index", index),
        classes="tile-overlay"
    )

    tile = Div(
        Div(name, classes="park-name"),
        indicator_button,
        tile_overlay,
        classes="park-tile"
    )

    return Div(tile, classes="park-tile-wrapper")





# --- Routes ---
@route
def index(state: State) -> Page:
    """
    Main page: Navbar with controls, followed by the main content row.
    """
    # 1. Navbar (Controls moved here)
    controls = Row(
        Button("Mark All Visited", "mark_all"),
        Button("Clear All", "clear_all"),
        classes="controls"
    )
    navbar = Div(controls, classes="navbar")


    # 2. Grid of tiles (Right side of the main row)
    tiles: list[PageContent] = []
    for i, p in enumerate(state.parks):
        tiles.append(make_tile(i, p, state.visited[i]))

    grid_container = Div(Div(*tiles, classes="parks-grid"))

    # Combined right-side container
    right_side_content = Div(
        grid_container,
        classes="passport-right"
    )

    # 3. Passport image (Left side of the main row)
    left = Div(
        Image(PASSPORT_IMAGE_PATH, style_width="100%", style_height="100%"),
        classes="passport-cover"
    )

    # 4. Main content row
    main_content_row = Row(
        Div(left, classes="passport-left"),
        right_side_content,
        classes="page-row"
    )
    
    # 5. Final Page Content: Navbar THEN Main Row
    content = Div(
        navbar,
        main_content_row
    )
    
    return Page(state, content)


@route
def toggle_park(state: State, park_index: int) -> Page:
    """
    Toggle the visited status for a specific park index.
    """
    if 0 <= park_index < len(state.visited):
        state.visited[park_index] = not state.visited[park_index]
    return index(state)


@route
def mark_all(state: State) -> Page:
    for i in range(len(state.visited)):
        state.visited[i] = True
    return index(state)


@route
def clear_all(state: State) -> Page:
    for i in range(len(state.visited)):
        state.visited[i] = False
    return index(state)

@route
def park_info(state: State, park_index: int) -> Page:
    park_name = state.parks[park_index]
    visited = state.visited[park_index]

    return Page(
        state,
        Div(
            Div(
                f"{park_name}",
                classes="park-info-title"
            ),
            Div(
                "Visited" if visited else "Not visited yet",
                classes="park-info-status"
            ),
            Button("Back to Passport", "index"),
            classes="park-info-page"
        )
    )


# --- Initial state ---
initial_parks = [
    "Alapocas Run",
    "Ashland Nature",
    "Bellevue",
    "Brandywine Creek",
    "Brandywine Zoo",
    "Cape Henlopen",
    "Delaware Seashore",
    "Fenwick Island",
    "First State Heritage Park",
    "Fort Delaware",
    "Fort DuPont",
    "Fort DuPont (North)",
    "Fox Point",
    "Holt Landing",
    "Killens Pond",
    "Trap Pond",
    "White Clay Creek",
    "Wilmington State Parks",
]

# Start with none visited
initial_visited = [False for _ in initial_parks]

if __name__ == '__main__':
    start_server(State(initial_parks, initial_visited), port="8067")

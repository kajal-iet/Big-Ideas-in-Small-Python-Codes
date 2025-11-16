import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from functools import lru_cache


# -------------------------------------------------
# SAFE RECURSIVE FIBONACCI (WITH LRU CACHE)
# -------------------------------------------------
@lru_cache(maxsize=None)
def fib_safe(n: int):
    if n <= 1:
        return n
    return fib_safe(n - 1) + fib_safe(n - 2)


# -------------------------------------------------
# ITERATIVE FIBONACCI
# -------------------------------------------------
def fib_fast(n: int):
    if n == 1:
        return 0
    if n == 2:
        return 1

    a, b = 0, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# -------------------------------------------------
# BUILD GRAPH FOR RECURSION TREE
# -------------------------------------------------
def build_recursion_graph(n, G, parent=None):
    node_label = f"fib({n})"
    G.add_node(node_label)

    if parent:
        G.add_edge(parent, node_label)

    if n <= 1:
        return

    build_recursion_graph(n - 1, G, node_label)
    build_recursion_graph(n - 2, G, node_label)


# -------------------------------------------------
# CUSTOM HIERARCHICAL TREE LAYOUT (NO GRAPHVIZ)
# -------------------------------------------------
def hierarchy_pos(G, root):
    """
    Custom tree layout without graphviz.
    Places nodes in a hierarchical top-down tree.
    """
    pos = {}
    width = 1.0
    vert_gap = 0.2
    vert_loc = 1.0
    xcenter = 0.5

    def _hierarchy_pos(G, node, x, y, dx):
        pos[node] = (x, y)
        neighbors = list(G.neighbors(node))
        if neighbors:
            step = dx / len(neighbors)
            for i, nbr in enumerate(neighbors):
                _hierarchy_pos(G, nbr, x - dx/2 + step/2 + step*i, y - vert_gap, step)
        return pos

    return _hierarchy_pos(G, root, xcenter, vert_loc, width)


# -------------------------------------------------
# DRAW TREE WITHOUT GRAPHVIZ
# -------------------------------------------------
def draw_tree_graph(n):
    G = nx.DiGraph()
    build_recursion_graph(n, G)

    root = "fib(" + str(n) + ")"
    pos = hierarchy_pos(G, root)

    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        arrows=False,
        node_size=1800,
        font_size=9,
        font_weight="bold",
    )
    st.pyplot(plt)


# -------------------------------------------------
# ITERATIVE VISUALIZATION (TIMELINE)
# -------------------------------------------------
def draw_iterative_timeline(n):
    seq = []
    a, b = 0, 1
    seq.append(a)
    if n > 1:
        seq.append(b)

    for _ in range(3, n + 1):
        a, b = b, a + b
        seq.append(b)

    plt.figure(figsize=(12, 2))
    plt.plot(range(len(seq)), seq, marker="o")
    plt.xticks(range(len(seq)), [f"F{i+1}" for i in range(len(seq))], rotation=45)
    plt.title("Iterative Fibonacci Timeline")
    plt.grid(True)

    st.pyplot(plt)


# -------------------------------------------------
# MAIN STREAMLIT APP
# -------------------------------------------------
def run():
    st.set_page_config(page_title="Fibonacci Generator", layout="centered")

    st.title("🌀 Fibonacci Sequence Generator")

    st.write(
        """
    ### Rules  
    - Enter a positive integer **N**.  
    - **Iterative Mode** → Fast, timeline visualization.  
    - **Recursive Mode** → Shows branching recursion tree.  
    - **Golden Ratio Convergence Number** →  
      F(n+1) / F(n) approaches **1.6180339887…**.
    """
    )

    mode = st.radio(
        "Choose Computation Mode:",
        ["⚡ Iterative (Fast)", "🛡 Recursive (Visualizable)"],
    )

    n = st.number_input("Enter N (example: 5, 20, 40):", min_value=1, step=1)

    if mode.startswith("🛡") and n > 200:
        st.error("Recursive mode supports N ≤ 200 due to recursion depth limits.")
        st.stop()

    if st.button("Generate Fibonacci"):
        st.write("### ✅ Result")

        if mode.startswith("⚡"):
            result = fib_fast(n)
            st.success(f"Iterative Mode → Fibonacci #{n}: {result}")
        else:
            result = fib_safe(n)
            st.success(f"Recursive Mode → Fibonacci #{n}: {result}")

        # --------------------------
        # GOLDEN RATIO CONVERGENCE
        # --------------------------
        if n >= 3:
            approx_phi = fib_fast(n) / fib_fast(n - 1)
            st.metric("Golden Ratio Convergence", f"{approx_phi:.10f}")

        # --------------------------
        # VISUALIZATIONS
        # --------------------------
        st.write("---")
        st.write("## 📊 Visualization")

        if mode.startswith("⚡"):
            draw_iterative_timeline(n)
        else:
            st.write("### 🌳 Recursion Tree")
            if n > 10:
                st.warning("Tree too large! Visualization only allowed for N ≤ 10.")
            else:
                draw_tree_graph(n)


if __name__ == "__main__":
    run()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1) Page setup
st.set_page_config(page_title="Quadratic Explorer")
st.title("Quadratic Explorer")
st.write("Choose a, b and c in the sidebar to plot the parabola y = ax^2 + bx + c.")
st.write("The app shows the vertex, the roots (if any), a graph and a data table.")

# 2) INPUT
with st.sidebar:
    st.header("Parameters")
    a = st.slider("Coefficient a", -5.0, 5.0, 1.0, 0.5)
    b = st.slider("Coefficient b", -10.0, 10.0, 0.0, 0.5)
    c = st.slider("Coefficient c", -10.0, 10.0, 0.0, 0.5)
    n = st.number_input("Number of points", 50, 1000, 200)
    show_table = st.checkbox("Show data table", value=True)

# check the input before calculating
if a == 0:
    st.error("a must not be 0, otherwise the graph is a straight line, not a parabola.")
    st.stop()

# 3) CALCULATION
vertex_x = -b / (2 * a)
vertex_y = a * vertex_x**2 + b * vertex_x + c
disc = b**2 - 4 * a * c

x = np.linspace(vertex_x - 6, vertex_x + 6, n)
y = a * x**2 + b * x + c
data = pd.DataFrame({"x": x, "y": y})

# 4) OUTPUT
st.metric("Vertex x", f"{vertex_x:.2f}")
st.metric("Vertex y", f"{vertex_y:.2f}")

if a > 0:
    st.write("a > 0, so the parabola opens upward and the vertex is the minimum point.")
else:
    st.write("a < 0, so the parabola opens downward and the vertex is the maximum point.")

if disc > 0:
    root1 = (-b + np.sqrt(disc)) / (2 * a)
    root2 = (-b - np.sqrt(disc)) / (2 * a)
    st.write("Discriminant =", round(disc, 2), "so there are 2 real roots:", round(root1, 2), "and", round(root2, 2))
elif disc == 0:
    st.write("Discriminant = 0, so there is 1 real root: x =", round(vertex_x, 2))
else:
    st.warning("Discriminant < 0, so the parabola does not cross the x-axis (no real roots).")

fig, ax = plt.subplots()
ax.plot(x, y, color="#123f6c", linewidth=2, label="y = ax^2 + bx + c")
ax.plot(vertex_x, vertex_y, "o", color="#dc8d29", label="Vertex")
ax.axvline(vertex_x, color="gray", linestyle="--", alpha=0.5, label="Axis of symmetry")
ax.axhline(0, color="black", linewidth=0.8)
ax.set(xlabel="x", ylabel="y", title="Quadratic function")
ax.grid(alpha=0.25)
ax.legend()
st.pyplot(fig)
plt.close(fig)

# 5) TABLE / DOWNLOAD
if show_table:
    st.dataframe(data.round(2), hide_index=True)

csv_bytes = data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download CSV",
    csv_bytes,
    file_name="quadratic_data.csv",
    mime="text/csv",
)

if st.button("Show equation"):
    st.latex(r"y = ax^2 + bx + c")
    st.latex(r"x_v = -\frac{b}{2a}, \quad D = b^2 - 4ac")
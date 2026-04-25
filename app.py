import streamlit as st
from sympy import symbols, Eq, solve, latex, sympify, simplify
import matplotlib.pyplot as plt
import numpy as np

# Nombre de la IA destacado
st.markdown(
    "<h1 style='color: #1a76d2; font-weight: bold; text-align: center;'>TutorUsMath</h1>",
    unsafe_allow_html=True,
)
# Marca del profesor, menos visible pero perceptible
st.markdown(
    "<div style='text-align:right; color: grey; font-size: 16px; opacity:0.6;'><i>prof Usbaldo P</i></div>",
    unsafe_allow_html=True,
)

st.title("Solucionador de ecuaciones cuadráticas")

ecuacion = st.text_input(
    "Escribe la ecuación cuadrática (ejemplo: 2*x**2 + 3*x + 1 = 0)"
)
if ecuacion:
    try:
        x = symbols('x')
        lado_izq, lado_der = ecuacion.split('=')
        eq = Eq(sympify(lado_izq), sympify(lado_der))
        expr = simplify(sympify(lado_izq) - sympify(lado_der))
        st.latex(latex(eq))
        confirmar = st.checkbox("¿Es esta tu ecuación?")
        if confirmar:
            poly = expr.as_poly(x)
            if poly.degree() != 2:
                st.error("Por ahora esta app solo resuelve ecuaciones cuadráticas de la forma ax² + bx + c = 0.")
            else:
                a = poly.coeff_monomial(x**2)
                b = poly.coeff_monomial(x)
                c = poly.coeff_monomial(1)
                st.markdown(
                    f"Coeficientes:<br>**a** = {a} &nbsp;&nbsp; **b** = {b} &nbsp;&nbsp; **c** = {c}",
                    unsafe_allow_html=True,
                )

                D = b**2 - 4*a*c
                st.latex(r"D = b^2 - 4ac")
                st.latex(f"D = {b}^2 - 4*{a}*{c} = {D}")

                if D > 0:
                    st.success("🔹 El discriminante es positivo, tiene dos soluciones reales distintas.")
                elif D == 0:
                    st.info("🔹 El discriminante es cero, tiene una única solución real.")
                else:
                    st.warning("🔹 El discriminante es negativo, tiene dos soluciones complejas conjugadas.")

                st.markdown("**Fórmula cuadrática:**")
                st.latex(r"x = \frac{-b \pm \sqrt{D}}{2a}")
                st.latex(f"x = \\frac{{-{b} \\pm \\sqrt{{{D}}}}}{{2*{a}}}")

                soluciones = solve(eq, x)
                st.markdown("**Soluciones:**")
                for i, s in enumerate(soluciones, 1):
                    st.latex(f"x_{i} = {latex(s)}")

                # Opción para mostrar gráfica
                mostrar_grafica = st.checkbox("Mostrar la gráfica de la función y sus cortes")
                if mostrar_grafica:
                    # Calcular el vértice
                    x_v = -b / (2*a)
                    y_v = a * x_v**2 + b * x_v + c

                    # Valores para graficar
                    x_reales = [float(s.evalf()) for s in soluciones if s.is_real]
                    x_points = x_reales + [x_v]
                    x_min = min(x_points) - 2 if x_points else -10
                    x_max = max(x_points) + 2 if x_points else 10

                    x_vals = np.linspace(x_min, x_max, 400)
                    y_vals = a*x_vals**2 + b*x_vals + c

                    fig, ax = plt.subplots()
                    ax.plot(x_vals, y_vals, label=f"${a}x^2 + {b}x + {c}$")
                    ax.axhline(0, color="black", linewidth=0.7)

                    # Puntos de corte (raíces reales)
                    if x_reales:
                        ax.scatter(x_reales, [0]*len(x_reales), color="red", zorder=5, label="Puntos de corte")

                    # Vértice
                    ax.scatter([x_v], [y_v], color="green", s=60, marker="o", zorder=6, label="Vértice")
                    ax.annotate(
                        f"({x_v:.2f}, {y_v:.2f})",
                        (x_v, y_v),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha="center",
                        color="green",
                        fontsize=10,
                        fontweight="bold"
                    )

                    ax.set_xlabel("x")
                    ax.set_ylabel("y")
                    ax.set_title("Gráfica de la función cuadrática")
                    ax.legend()
                    st.pyplot(fig)

                    # Mostrar las coordenadas del vértice debajo de la gráfica
                    st.info(f"El vértice de la parábola está en  \n**({x_v:.3f}, {y_v:.3f})**")

    except Exception as e:
        st

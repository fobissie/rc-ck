import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_daq as daq  # für den Toggle-Schalter

# Dash-App + WSGI-Server (für Azure wichtig)
app = Dash(__name__)
server = app.server

app.title = "RC-Kreis Visualisierung"

app.layout = html.Div(
    style={
        "fontFamily": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "maxWidth": "1100px",
        "margin": "0 auto",
        "padding": "2rem"
    },
    children=[
        html.H1("Interaktive RC-Kreis Visualisierung", style={"textAlign": "center"}),

        html.P(
            "Diese Web-App zeigt das zeitliche Verhalten eines einfachen RC-Kreises. "
            "Du kannst Widerstand R, Kapazität C und Versorgungsspannung U₀ verändern "
            "und zwischen Laden und Entladen umschalten. Die Diagramme zeigen die "
            "Spannung U_C(t), die Ladung Q(t) und den Strom I(t).",
            style={"textAlign": "center", "maxWidth": "800px", "margin": "0 auto 2rem"}
        ),

        # Steuer-/Parameterbereich
        html.Div(
            style={
                "background": "#f5f5f7",
                "borderRadius": "12px",
                "padding": "1.5rem",
                "marginBottom": "2rem",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.05)"
            },
            children=[
                html.H2("Parameter", style={"marginTop": 0}),
                html.Div(
                    style={"display": "flex", "flexWrap": "wrap", "gap": "2rem"},
                    children=[
                        # Spalte 1: R-Slider
                        html.Div(
                            style={"flex": "1 1 240px"},
                            children=[
                                html.Label("Widerstand R [Ω]", style={"fontWeight": 600}),
                                dcc.Slider(
                                    id="R-slider",
                                    min=100,
                                    max=10000,
                                    step=100,
                                    value=1000,
                                    marks={
                                        100: "100",
                                        1000: "1k",
                                        5000: "5k",
                                        10000: "10k"
                                    },
                                    tooltip={"placement": "bottom", "always_visible": True}
                                ),
                            ],
                        ),
                        # Spalte 2: C-Slider
                        html.Div(
                            style={"flex": "1 1 240px"},
                            children=[
                                html.Label("Kapazität C [µF]", style={"fontWeight": 600}),
                                dcc.Slider(
                                    id="C-slider",
                                    min=1,
                                    max=1000,
                                    step=1,
                                    value=100,  # 100 µF
                                    marks={
                                        1: "1",
                                        10: "10",
                                        100: "100",
                                        1000: "1000",
                                    },
                                    tooltip={"placement": "bottom", "always_visible": True}
                                ),
                            ],
                        ),
                        # Spalte 3: U0-Slider
                        html.Div(
                            style={"flex": "1 1 240px"},
                            children=[
                                html.Label("Versorgungsspannung U₀ [V]", style={"fontWeight": 600}),
                                dcc.Slider(
                                    id="U0-slider",
                                    min=1.0,
                                    max=12.0,
                                    step=0.5,
                                    value=5.0,
                                    marks={1: "1", 5: "5", 9: "9", 12: "12"},
                                    tooltip={"placement": "bottom", "always_visible": True}
                                ),
                            ],
                        ),
                        # Spalte 4: Laden/Entladen-Toggle
                        html.Div(
                            style={"flex": "0 0 220px"},
                            children=[
                                daq.ToggleSwitch(
                                    id="mode-toggle",
                                    label="Betriebsart",
                                    labelPosition="top",
                                    value=True,  # True = Laden
                                    size=35
                                ),
                                html.Div(
                                    id="mode-label",
                                    style={
                                        "marginTop": "0.5rem",
                                        "fontWeight": 600
                                    }
                                )
                            ]
                        ),
                    ],
                ),
                html.Div(
                    id="info-panel",
                    style={
                        "marginTop": "1rem",
                        "fontSize": "0.9rem",
                        "color": "#555",
                        "background": "white",
                        "borderRadius": "8px",
                        "padding": "0.75rem 1rem"
                    }
                ),
            ],
        ),

        # Diagramm-Bereich
        html.Div(
            children=[
                html.H2("Zeitverläufe", style={"marginTop": 0}),
                html.P(
                    "Alle Diagramme zeigen die Zeit von t = 0 bis t = 5·τ. "
                    "Die gestrichelte Linie markiert die Zeitkonstante τ = R·C.",
                    style={"fontSize": "0.9rem", "color": "#444"}
                ),

                html.H3("Spannung am Kondensator U_C(t)"),
                dcc.Graph(id="voltage-graph"),

                html.H3("Ladung des Kondensators Q(t)"),
                dcc.Graph(id="charge-graph"),

                html.H3("Strom I(t) durch den Widerstand"),
                dcc.Graph(id="current-graph"),
            ]
        ),

        html.H2("Schaltplan des RC-Kreises", style={"marginTop": "3rem"}),

        dcc.Markdown(
            """
```text
   + ── U₀ ── R ──+───||─── -
                       C	
  •	U₀: ideale Gleichspannungsquelle
	•	R : Widerstand
	•	C : Kondensator

Beim Laden wird ein zunächst ungeladener Kondensator an U₀ gelegt.
Beim Entladen ist der Kondensator anfangs auf U₀ geladen und entlädt sich nur über R.
“””,
style={“background”: “#f5f5f7”, “padding”: “1rem”, “borderRadius”: “8px”}
),
html.H2("Theoretischer Hintergrund", style={"marginTop": "2rem"}),

    dcc.Markdown(
        """Zeitkonstante τ = R·C

Die Zeitkonstante τ beschreibt, wie schnell der RC-Kreis reagiert:
	•	Einheit: Sekunden
	•	Nach t = τ gilt:
	•	Laden: U_C(τ) ≈ 0,63 · U₀
	•	Entladen: U_C(τ) ≈ 0,37 · U₀

Nach ungefähr 5·τ ist der Vorgang praktisch abgeschlossen.

⸻

Laden eines RC-Kreises (U_C(0) = 0 V)
	•	Spannung:
\( U_C(t) = U_0 \cdot \bigl(1 - e^{-t/(R C)}\bigr) \)
	•	Ladung:
\( Q(t) = C \cdot U_C(t) \)
	•	Strom:
\( I(t) = \frac{U_0}{R} \cdot e^{-t/(R C)} \)

Der Strom ist zu Beginn am größten und fällt exponentiell ab.

⸻

Entladen eines RC-Kreises (U_C(0) = U₀)
	•	Spannung:
\( U_C(t) = U_0 \cdot e^{-t/(R C)} \)
	•	Ladung:
\( Q(t) = C \cdot U_0 \cdot e^{-t/(R C)} \)
	•	Strom:
\( I(t) = -\frac{U_0}{R} \cdot e^{-t/(R C)} \)

Das Minuszeichen zeigt die umgekehrte Stromrichtung im Vergleich zum Ladevorgang.

⸻

In dieser App werden alle Größen in sinnvollen Einheiten dargestellt:
	•	Zeit t in Millisekunden (ms)
	•	Ladung Q in Milli-Coulomb (mC)
	•	Strom I in Milliampere (mA)
“””,
style={“background”: “#f5f5f7”, “padding”: “1rem”, “borderRadius”: “8px”}
),

html.Footer(
      "Hinweis: Es wird ein idealer RC-Kreis ohne parasitäre Widerstände, Leckströme "
      "oder nichtlineare Effekte angenommen.",
      style={"marginTop": "2rem", "fontSize": "0.8rem", "color": "#777"}
  )

  ]
)

@app.callback(
Output(“voltage-graph”, “figure”),
Output(“charge-graph”, “figure”),
Output(“current-graph”, “figure”),
Output(“info-panel”, “children”),
Output(“mode-label”, “children”),
Input(“R-slider”, “value”),
Input(“C-slider”, “value”),
Input(“U0-slider”, “value”),
Input(“mode-toggle”, “value”)
)
def update_graphs(R_ohm, C_micro_f, U0, mode_is_charge):
“””
mode_is_charge = True  -> Laden
False -> Entladen
“””
# Einheiten umrechnen
C = C_micro_f * 1e-6  # µF -> F
tau = R_ohm * C       # Zeitkonstante in Sekunden

# Simulationszeit: 0 bis 5 * tau (mindestens etwas > 0)
t_max = max(5 * tau, 0.01)
t = np.linspace(0, t_max, 500)

if mode_is_charge:
    mode_text = "Modus: Laden"
    # Laden: U_C(0) = 0
    Uc = U0 * (1 - np.exp(-t / tau))
    Q = C * Uc
    I = (U0 / R_ohm) * np.exp(-t / tau)
else:
    mode_text = "Modus: Entladen"
    # Entladen: U_C(0) = U0
    Uc = U0 * np.exp(-t / tau)
    Q = C * U0 * np.exp(-t / tau)
    I = -(U0 / R_ohm) * np.exp(-t / tau)

# Info-Box-Text
info_text = (
    f"R = {R_ohm:.0f} Ω, "
    f"C = {C_micro_f:.0f} µF, "
    f"U₀ = {U0:.1f} V → "
    f"Zeitkonstante τ = {tau*1000:.2f} ms, "
    f"Darstellung von t = 0 bis {t_max*1000:.2f} ms"
)

t_ms = t * 1000
tau_ms = tau * 1000

# --- Spannung U_C(t) ---
fig_u = go.Figure()
fig_u.add_trace(
    go.Scatter(
        x=t_ms,
        y=Uc,
        mode="lines",
        name="U_C(t)"
    )
)
# Vertikale Linie bei t = τ
fig_u.add_vline(x=tau_ms, line_dash="dash", line_width=1)
fig_u.add_annotation(
    x=tau_ms,
    y=max(Uc),
    text="t = τ",
    showarrow=True,
    arrowhead=2,
    yshift=20
)
fig_u.update_layout(
    xaxis_title="Zeit t [ms]",
    yaxis_title="Spannung U_C [V]",
    template="plotly_white",
    margin=dict(l=40, r=10, t=10, b=40),
)

# --- Ladung Q(t) in mC ---
fig_q = go.Figure()
fig_q.add_trace(
    go.Scatter(
        x=t_ms,
        y=Q * 1e3,   # C -> mC
        mode="lines",
        name="Q(t)"
    )
)
fig_q.add_vline(x=tau_ms, line_dash="dash", line_width=1)
fig_q.add_annotation(
    x=tau_ms,
    y=max(Q * 1e3),
    text="t = τ",
    showarrow=True,
    arrowhead=2,
    yshift=20
)
fig_q.update_layout(
    xaxis_title="Zeit t [ms]",
    yaxis_title="Ladung Q [mC]",
    template="plotly_white",
    margin=dict(l=40, r=10, t=10, b=40),
)

# --- Strom I(t) in mA ---
fig_i = go.Figure()
fig_i.add_trace(
    go.Scatter(
        x=t_ms,
        y=I * 1e3,   # A -> mA
        mode="lines",
        name="I(t)"
    )
)
fig_i.add_vline(x=tau_ms, line_dash="dash", line_width=1)
# Annotation irgendwo sinnvoll (oberhalb oder unterhalb)
y_for_annot = float(np.max(I * 1e3)) if mode_is_charge else float(np.min(I * 1e3))
fig_i.add_annotation(
    x=tau_ms,
    y=y_for_annot,
    text="t = τ",
    showarrow=True,
    arrowhead=2,
    yshift=20 if mode_is_charge else -20
)
fig_i.update_layout(
    xaxis_title="Zeit t [ms]",
    yaxis_title="Strom I [mA] (Vorzeichen = Richtung)",
    template="plotly_white",
    margin=dict(l=40, r=10, t=10, b=40),
)

return fig_u, fig_q, fig_i, info_text, mode_text
if name == “main”:
app.run_server(debug=True)

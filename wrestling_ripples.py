import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Sample data - you can expand or load from CSV
data = [
    {"Source": "MSG Curtain Call (1996)", "Target": "Austin wins King of the Ring", "Ripple": "HHH punished, Austin push begins"},
    {"Source": "Austin wins King of the Ring", "Target": "Austin becomes top guy", "Ripple": "Birth of Austin 3:16 promo"},
    {"Source": "Austin becomes top guy", "Target": "HHH rebuilds through DX", "Ripple": "Leads Attitude Era"},
    {"Source": "HHH rebuilds through DX", "Target": "HHH becomes main eventer", "Ripple": "Regains credibility via faction"},
    {"Source": "HHH becomes main eventer", "Target": "Evolution forms", "Ripple": "Starts his reign of dominance"},
    {"Source": "Evolution forms", "Target": "Orton & Batista become stars", "Ripple": "Mentors Orton & Batista"},
    {"Source": "Orton & Batista become stars", "Target": "HHH transitions to backstage power", "Ripple": "Batista eventually dethrones HHH"},
    {"Source": "HHH transitions to backstage power", "Target": "Takes over creative in 2022", "Ripple": "Creates NXT vision"},
]

# Load into DataFrame
df = pd.DataFrame(data)

# Streamlit UI
st.title("Wrestling Ripple Effect Web")
st.subheader("From MSG Curtain Call to Creative Control")

# Build Graph
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row["Source"], row["Target"], ripple=row["Ripple"])

# Position nodes
pos = nx.spring_layout(G, k=1.2)

# Build plot
edge_x, edge_y, node_x, node_y, labels = [], [], [], [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    labels.append(node)

# Build figure
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='gray'),
    hoverinfo='none',
    mode='lines'))

fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    marker=dict(size=20, color='skyblue'),
    text=labels,
    textposition="top center",
    hoverinfo='text'))

fig.update_layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(l=20, r=20, t=40, b=20),
    height=700
)

st.plotly_chart(fig)

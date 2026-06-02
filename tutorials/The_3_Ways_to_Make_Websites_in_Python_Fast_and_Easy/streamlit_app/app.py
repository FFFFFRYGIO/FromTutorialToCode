"""
Streamlit Feature Showcase
==========================

A single-file Streamlit application demonstrating the main features that make
Streamlit great for data apps and prototypes:

- Page configuration, titles, markdown, and layout (columns, tabs, expanders)
- Sidebar navigation and a wide range of input widgets
- Session state (a counter + a to-do list that persist across reruns)
- Caching expensive computations with @st.cache_data
- Interactive data exploration with pandas + built-in charts
- Native charts (line, bar, area, map) and a matplotlib figure
- File upload + download
- Forms, metrics, progress bars, and status messages
- A simple chat interface using st.chat_input / st.chat_message

Run it with:
    streamlit run app.py
"""

from __future__ import annotations

import time
from datetime import date, datetime

import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit command).
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Streamlit Feature Showcase",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Cached data helpers. @st.cache_data memoizes the return value so the
# expensive work only runs once per unique set of arguments.
# ---------------------------------------------------------------------------
@st.cache_data
def generate_sales_data(rows: int, seed: int = 42) -> pd.DataFrame:
    """Create a fake but plausible sales dataset for the demos."""
    rng = np.random.default_rng(seed)
    regions = ["North", "South", "East", "West"]
    products = ["Widget", "Gadget", "Gizmo", "Doohickey"]
    dates = pd.date_range(end=date.today(), periods=rows, freq="D")

    return pd.DataFrame(
        {
            "date": rng.choice(dates, size=rows),
            "region": rng.choice(regions, size=rows),
            "product": rng.choice(products, size=rows),
            "units": rng.integers(1, 100, size=rows),
            "revenue": rng.normal(500, 150, size=rows).round(2),
        }
    )


@st.cache_data
def make_map_points(n: int, seed: int = 7) -> pd.DataFrame:
    """Generate random lat/lon points scattered around the continental US."""
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "lat": rng.normal(39.5, 4.0, size=n),
            "lon": rng.normal(-98.35, 12.0, size=n),
        }
    )


# ---------------------------------------------------------------------------
# Session state initialisation. Anything stored here survives reruns, which is
# how Streamlit keeps state across user interactions.
# ---------------------------------------------------------------------------
if "counter" not in st.session_state:
    st.session_state.counter = 0
if "todos" not in st.session_state:
    st.session_state.todos = []
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me anything about Streamlit."}
    ]


# ---------------------------------------------------------------------------
# Sidebar: navigation + a few global controls.
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🎈 Streamlit Showcase")
    st.caption("A tour of the framework's main features.")

    page = st.radio(
        "Jump to a section",
        [
            "Home",
            "Widgets & State",
            "Data Explorer",
            "Charts",
            "Files",
            "Forms & Status",
            "Chat",
        ],
    )

    st.divider()
    rows = st.slider("Sample dataset size", 100, 5000, 1000, step=100)
    st.caption("Used by the Data Explorer and Charts pages.")


# Build the shared dataset once (cached).
data = generate_sales_data(rows)


# ---------------------------------------------------------------------------
# Page: Home
# ---------------------------------------------------------------------------
def render_home() -> None:
    st.title("Welcome to the Streamlit Feature Showcase 🎈")
    st.markdown(
        """
        **Streamlit** turns plain Python scripts into interactive web apps with
        almost no boilerplate. Every time a user interacts with a widget, the
        whole script reruns top-to-bottom and Streamlit efficiently updates the UI.

        Use the sidebar to explore each feature category:
        """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("⚡ Fast")
        st.write("Go from a script to a shareable web app in minutes.")
    with col2:
        st.subheader("🧩 Simple")
        st.write("Pure Python. No HTML, CSS, or JavaScript required.")
    with col3:
        st.subheader("📊 Data-first")
        st.write("First-class support for pandas, numpy, and popular chart libs.")

    st.divider()

    with st.expander("How does Streamlit work under the hood?"):
        st.markdown(
            """
            - The script runs from top to bottom on every interaction.
            - Widgets return their current value where they are defined.
            - `st.session_state` lets you persist data across reruns.
            - `@st.cache_data` / `@st.cache_resource` avoid redoing expensive work.
            """
        )

    st.info("Tip: open the sidebar and click through each section.", icon="💡")


# ---------------------------------------------------------------------------
# Page: Widgets & State
# ---------------------------------------------------------------------------
def render_widgets() -> None:
    st.title("Widgets & Session State")
    st.write("Streamlit ships with a rich set of input widgets.")

    left, right = st.columns(2)

    with left:
        st.subheader("Common inputs")
        name = st.text_input("Your name", "Ada")
        age = st.number_input("Your age", min_value=0, max_value=120, value=30)
        mood = st.select_slider(
            "Mood", options=["😴", "🙂", "😄", "🤩"], value="😄"
        )
        favorite = st.selectbox("Favorite framework", ["Streamlit", "Flask", "Django"])
        likes = st.multiselect(
            "Topics you like", ["Data", "Web", "AI", "APIs"], default=["Data", "AI"]
        )
        agree = st.checkbox("I love building with Python")
        when = st.date_input("Pick a date", value=date.today())

        st.write(
            f"Hello **{name}**, age **{age}**, feeling {mood}. "
            f"You picked **{favorite}** and like {', '.join(likes) or 'nothing yet'}."
        )
        st.write(f"Selected date: {when:%A, %B %d, %Y}")
        if agree:
            st.success("Great choice! 🐍")

    with right:
        st.subheader("Counter (session state)")
        st.write("The value below persists across reruns.")
        c1, c2, c3 = st.columns(3)
        if c1.button("➖ Decrease"):
            st.session_state.counter -= 1
        if c2.button("🔄 Reset"):
            st.session_state.counter = 0
        if c3.button("➕ Increase"):
            st.session_state.counter += 1
        st.metric("Counter", st.session_state.counter)

        st.divider()

        st.subheader("To-do list (session state)")
        new_todo = st.text_input("Add a task", key="new_todo_input")
        if st.button("Add task") and new_todo.strip():
            st.session_state.todos.append({"task": new_todo.strip(), "done": False})

        if not st.session_state.todos:
            st.caption("No tasks yet — add one above.")
        for i, todo in enumerate(st.session_state.todos):
            cols = st.columns([0.1, 0.7, 0.2])
            done = cols[0].checkbox("", value=todo["done"], key=f"done_{i}")
            st.session_state.todos[i]["done"] = done
            label = f"~~{todo['task']}~~" if done else todo["task"]
            cols[1].markdown(label)
            if cols[2].button("Delete", key=f"del_{i}"):
                st.session_state.todos.pop(i)
                st.rerun()


# ---------------------------------------------------------------------------
# Page: Data Explorer
# ---------------------------------------------------------------------------
def render_data_explorer() -> None:
    st.title("Interactive Data Explorer")
    st.write("Filter a cached pandas dataset and inspect the results live.")

    f1, f2, f3 = st.columns(3)
    regions = f1.multiselect(
        "Region", sorted(data["region"].unique()), default=sorted(data["region"].unique())
    )
    products = f2.multiselect(
        "Product",
        sorted(data["product"].unique()),
        default=sorted(data["product"].unique()),
    )
    min_units = f3.slider("Minimum units", 1, 100, 1)

    filtered = data[
        data["region"].isin(regions)
        & data["product"].isin(products)
        & (data["units"] >= min_units)
    ]

    m1, m2, m3 = st.columns(3)
    m1.metric("Rows", f"{len(filtered):,}")
    m2.metric("Total units", f"{int(filtered['units'].sum()):,}")
    m3.metric("Total revenue", f"${filtered['revenue'].sum():,.0f}")

    tab_table, tab_summary = st.tabs(["📋 Table", "📈 Summary"])
    with tab_table:
        st.dataframe(filtered, use_container_width=True)
    with tab_summary:
        st.write("Revenue by region")
        st.bar_chart(filtered.groupby("region")["revenue"].sum())
        st.write("Statistical summary")
        st.dataframe(filtered.describe(), use_container_width=True)


# ---------------------------------------------------------------------------
# Page: Charts
# ---------------------------------------------------------------------------
def render_charts() -> None:
    st.title("Charts & Visualisations")

    daily = (
        data.assign(date=pd.to_datetime(data["date"]))
        .groupby("date")[["units", "revenue"]]
        .sum()
        .sort_index()
    )

    st.subheader("Built-in charts")
    c1, c2 = st.columns(2)
    c1.caption("Line chart — revenue over time")
    c1.line_chart(daily["revenue"])
    c2.caption("Area chart — units over time")
    c2.area_chart(daily["units"])

    st.caption("Bar chart — revenue by product")
    st.bar_chart(data.groupby("product")["revenue"].sum())

    st.divider()
    st.subheader("Map")
    st.caption("st.map renders geographic points on an interactive map.")
    st.map(make_map_points(200))

    st.divider()
    st.subheader("Matplotlib figure")
    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.hist(data["units"], bins=20, color="#ff4b4b", edgecolor="white")
        ax.set_title("Distribution of units sold")
        ax.set_xlabel("Units")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    except ModuleNotFoundError:
        st.warning("Install matplotlib to see this chart: `pip install matplotlib`")


# ---------------------------------------------------------------------------
# Page: Files
# ---------------------------------------------------------------------------
def render_files() -> None:
    st.title("File Upload & Download")

    st.subheader("Upload a CSV")
    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded is not None:
        user_df = pd.read_csv(uploaded)
        st.success(f"Loaded {len(user_df):,} rows from **{uploaded.name}**.")
        st.dataframe(user_df.head(50), use_container_width=True)
    else:
        st.caption("No file uploaded — showing the sample dataset instead.")
        user_df = data

    st.divider()
    st.subheader("Download data")
    st.write("Download the current dataset as a CSV file.")
    csv_bytes = user_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV",
        data=csv_bytes,
        file_name="streamlit_data.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# Page: Forms & Status
# ---------------------------------------------------------------------------
def render_forms() -> None:
    st.title("Forms, Status & Feedback")

    st.subheader("A form (batches inputs into one submit)")
    with st.form("signup_form"):
        email = st.text_input("Email")
        plan = st.radio("Plan", ["Free", "Pro", "Enterprise"], horizontal=True)
        newsletter = st.checkbox("Subscribe to the newsletter", value=True)
        submitted = st.form_submit_button("Sign up")
    if submitted:
        if "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            st.success(f"Signed up **{email}** on the **{plan}** plan.")
            st.balloons()

    st.divider()
    st.subheader("Status messages")
    s1, s2, s3, s4 = st.columns(4)
    s1.info("This is info", icon="ℹ️")
    s2.success("This is success", icon="✅")
    s3.warning("This is a warning", icon="⚠️")
    s4.error("This is an error", icon="🚨")

    st.divider()
    st.subheader("Progress & spinners")
    if st.button("Run a fake long task"):
        progress = st.progress(0, text="Starting...")
        for pct in range(0, 101, 10):
            time.sleep(0.05)
            progress.progress(pct, text=f"Working... {pct}%")
        with st.spinner("Finalizing..."):
            time.sleep(0.5)
        st.toast("Task complete!", icon="🎉")
        st.success("Done!")


# ---------------------------------------------------------------------------
# Page: Chat
# ---------------------------------------------------------------------------
def render_chat() -> None:
    st.title("Chat Interface")
    st.caption(
        "Streamlit has native chat primitives. This demo echoes a canned reply."
    )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type a message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        reply = (
            f"You said: _{prompt}_\n\n"
            "In a real app you'd send this to an LLM or backend and stream the "
            "response back here."
        )
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
PAGES = {
    "Home": render_home,
    "Widgets & State": render_widgets,
    "Data Explorer": render_data_explorer,
    "Charts": render_charts,
    "Files": render_files,
    "Forms & Status": render_forms,
    "Chat": render_chat,
}

PAGES[page]()

st.sidebar.divider()
st.sidebar.caption(f"Rendered at {datetime.now():%H:%M:%S}")

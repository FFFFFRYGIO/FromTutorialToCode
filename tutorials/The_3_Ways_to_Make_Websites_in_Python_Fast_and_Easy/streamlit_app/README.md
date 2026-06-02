# Streamlit Feature Showcase

A single-file [Streamlit](https://streamlit.io) app that demonstrates the main
features that make Streamlit great for data apps and rapid prototypes.

## What it shows

| Section | Features demonstrated |
| --- | --- |
| **Home** | Page config, markdown, columns, expanders, info boxes |
| **Widgets & State** | Text/number/select/slider/date inputs, `st.session_state` (a persistent counter and to-do list), `st.metric` |
| **Data Explorer** | Cached pandas dataset, live filtering, tabs, `st.dataframe` |
| **Charts** | `line_chart`, `area_chart`, `bar_chart`, `st.map`, and a Matplotlib figure |
| **Files** | `st.file_uploader` (CSV) and `st.download_button` |
| **Forms & Status** | `st.form`, status messages, progress bar, spinner, toast, balloons |
| **Chat** | Native `st.chat_message` / `st.chat_input` |

It also uses `@st.cache_data` to memoize the sample data generation.

## Setup

```bash
# from this folder
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Streamlit will open the app in your browser (usually at http://localhost:8501).
Every time you edit `app.py` and save, the app offers to rerun automatically.

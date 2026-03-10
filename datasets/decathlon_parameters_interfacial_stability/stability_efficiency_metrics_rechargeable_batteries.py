import streamlit as st
import pandas as pd
import yaml
import json
import glob
import os

# ------------------------------
# Configuration – robust path
# ------------------------------
# Use the directory where this script is located
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, "battery_metrics")
SUPPORTED_EXTENSIONS = ["*.yaml", "*.yml", "*.json"]

# ------------------------------
# Load all parameter files
# ------------------------------
@st.cache_data
def load_all_parameters(data_dir):
    """Scan the data directory, load all YAML/JSON files and return a list of parameter dicts."""
    parameter_list = []
    if not os.path.exists(data_dir):
        # Instead of returning empty, we raise a clear error that will be shown in the app
        st.error(f"Data directory not found at: **{data_dir}**\n\n"
                 f"Please create this folder and place the YAML/JSON files inside.")
        return parameter_list

    for ext in SUPPORTED_EXTENSIONS:
        for filepath in glob.glob(os.path.join(data_dir, ext)):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    if filepath.endswith('.json'):
                        data = json.load(f)
                    else:
                        data = yaml.safe_load(f)

                # Basic validation: must contain 'section' and 'tables'
                if 'section' not in data or 'tables' not in data:
                    st.warning(f"Skipping {os.path.basename(filepath)}: missing 'section' or 'tables'")
                    continue

                # Add file info and store
                parameter_list.append({
                    'file': os.path.basename(filepath),
                    'section': data['section'],
                    'symbol': data.get('symbol', ''),
                    'tables': data['tables']
                })
            except Exception as e:
                st.warning(f"Error loading {filepath}: {e}")

    # Sort alphabetically by section name for a cleaner dropdown
    parameter_list.sort(key=lambda x: x['section'].lower())
    return parameter_list

# ------------------------------
# Build the app
# ------------------------------
st.set_page_config(page_title="Battery Decathlon Metrics", layout="wide")
st.title("🔋 The Decathlon of Interfacial Stability")
st.markdown("Select a parameter from the dropdown to view its technical metrics and development roadmap.")

# Show the data directory being used (helpful for debugging)
st.caption(f"Looking for data files in: `{DATA_DIR}`")

parameters = load_all_parameters(DATA_DIR)

if not parameters:
    st.info("No parameter files found. Please ensure the YAML/JSON files are placed in the folder above.")
    st.stop()

# Create dropdown choices: show "section (symbol)" if symbol exists, else just section
choices = {}
for p in parameters:
    display_name = p['section']
    if p['symbol']:
        display_name += f" ({p['symbol']})"
    choices[display_name] = p

selected_display = st.selectbox("Choose a parameter", list(choices.keys()))
selected_param = choices[selected_display]

# ------------------------------
# Display the selected parameter
# ------------------------------
st.header(selected_param['section'])
if selected_param['symbol']:
    st.subheader(f"Symbol: {selected_param['symbol']}")

# Iterate through each table in the parameter
for idx, table in enumerate(selected_param['tables']):
    with st.container():
        st.markdown(f"**Table {idx+1}:** {table.get('caption', '')}")

        # Convert rows to DataFrame
        if 'columns' in table and 'rows' in table:
            df = pd.DataFrame(table['rows'])
            # Ensure columns are in the order specified (if they exist in the DataFrame)
            # Note: This reorders and also drops any extra columns not in the list
            existing_cols = [col for col in table['columns'] if col in df.columns]
            if existing_cols:
                df = df[existing_cols]
            # If some columns from the list are missing, show a warning
            missing_cols = set(table['columns']) - set(df.columns)
            if missing_cols:
                st.warning(f"Missing columns in data: {missing_cols}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Table format is incomplete (missing 'columns' or 'rows').")

        st.divider()

# Optional: show the source filename for reference
st.caption(f"Source file: `{selected_param['file']}`")

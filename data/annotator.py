import streamlit as st
import pandas as pd
import os

csv_path = "./final_one cleaned.csv"

st.set_page_config(page_title="Dataset Cleaner", layout="wide")

if 'current_row' not in st.session_state:
    st.session_state.current_row = 0
if 'df' not in st.session_state:
    st.session_state.df = None
if 'total_rows' not in st.session_state:
    st.session_state.total_rows = 0


@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'type' not in df.columns:
            df['type'] = ''
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None


def save_data(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving CSV: {e}")
        return False


st.title("Dataset Cleaning Tool")

if st.button("Load Dataset") or st.session_state.df is None:
    if os.path.exists(csv_path):
        st.session_state.df = load_data(csv_path)
        if st.session_state.df is not None:
            st.session_state.total_rows = len(st.session_state.df)
            st.success(
                f"Dataset loaded successfully! Total rows: {st.session_state.total_rows}")
    else:
        st.error("File not found!")

if st.session_state.df is not None:
    st.markdown("---")

    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.current_row == 0):
            st.session_state.current_row -= 1
            st.rerun()

    with col2:
        if st.button("Next ➡️", disabled=st.session_state.current_row >= st.session_state.total_rows - 1):
            st.session_state.current_row += 1
            st.rerun()

    with col3:
        selected_row = st.number_input(
            "Jump to row:",
            min_value=0,
            max_value=st.session_state.total_rows - 1,
            value=st.session_state.current_row,
            step=1
        )
        if selected_row != st.session_state.current_row:
            st.session_state.current_row = selected_row
            st.rerun()

    with col4:
        st.write(
            f"Row {st.session_state.current_row + 1} of {st.session_state.total_rows}")

    st.markdown("---")

    video_col, data_col = st.columns([0.4, 1.6])

    current_data = st.session_state.df.iloc[st.session_state.current_row]

    with video_col:
        st.subheader("Video")
        video_path = current_data['filepath']

        if pd.notna(video_path) and os.path.exists(video_path):
            try:
                video_file = open(video_path, 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
            except Exception as e:
                st.error(f"Error loading video: {e}")
                st.info(f"Video path: {video_path}")
        else:
            st.warning("Video file not found or path is empty")
            st.info(f"Video path: {video_path}")

    with data_col:
        st.subheader("Edit Data")

        with st.form(key=f"edit_form_{st.session_state.current_row}"):
            edited_data = {}

            edited_data['original_a'] = st.text_area(
                "Original Audio:",
                value=str(current_data['original_a']) if pd.notna(
                    current_data['original_a']) else "",
                height=100
            )

            edited_data['attack_a'] = st.text_area(
                "Attack Audio:",
                value=str(current_data['attack_a']) if pd.notna(
                    current_data['attack_a']) else "",
                height=100
            )

            edited_data['original_v'] = st.text_area(
                "Original Video:",
                value=str(current_data['original_v']) if pd.notna(
                    current_data['original_v']) else "",
                height=100
            )

            edited_data['attack_v'] = st.text_area(
                "Attack Video:",
                value=str(current_data['attack_v']) if pd.notna(
                    current_data['attack_v']) else "",
                height=100
            )

            edited_data['original_p'] = st.text_area(
                "Original Perception:",
                value=str(current_data['original_p']) if pd.notna(
                    current_data['original_p']) else "",
                height=100
            )

            edited_data['attack_p'] = st.text_area(
                "Attack Perception:",
                value=str(current_data['attack_p']) if pd.notna(
                    current_data['attack_p']) else "",
                height=100
            )

            edited_data['GT'] = st.text_area(
                "Ground Truth:",
                value=str(current_data['GT']) if pd.notna(
                    current_data['GT']) else "",
                height=68
            )

            edited_data['label'] = st.text_area(
                "Label:",
                value=str(current_data['label']) if pd.notna(
                    current_data['label']) else "",
                height=68
            )

            edited_data['type'] = st.text_input(
                "Type:",
                value=str(current_data['type']) if pd.notna(
                    current_data['type']) else ""
            )

            col1, col2 = st.columns(2)
            with col1:
                save_button = st.form_submit_button(
                    "💾 Save Changes", type="primary", use_container_width=True)
            with col2:
                save_and_next = st.form_submit_button(
                    "💾 Save & Next", use_container_width=True)

            if save_button or save_and_next:
                for field, value in edited_data.items():
                    st.session_state.df.at[st.session_state.current_row,
                                           field] = value

                if save_data(st.session_state.df, csv_path):
                    st.success("Changes saved successfully!")

                    if save_and_next and st.session_state.current_row < st.session_state.total_rows - 1:
                        st.session_state.current_row += 1
                        st.rerun()
                else:
                    st.error("Failed to save changes!")

    st.markdown("---")
    with st.expander("View Full Row Data"):
        st.json(current_data.to_dict())

else:
    st.info("Please load a dataset to begin cleaning.")

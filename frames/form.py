import streamlit as st


def params_selector_ui(params: dict) -> dict:
    params_parse = dict()
    with st.form("params"):
        for param in params:
            if param["type"] == "int":
                col1, col2 = st.columns(2)
                with col1:
                    min_number = st.number_input("min " + param["name"], value=param["min"])
                with col2:
                    max_number = st.number_input("max " + param["name"], value=param["max"])
                params_parse[param["name"]] = range(min_number, max_number, param["step"])
            else:
                pass
        submitted = st.form_submit_button("Submit")
    return submitted, params_parse

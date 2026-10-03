import streamlit as st


def flash(result):
    """Store an (ok, message) result, then rerun so tables refresh."""
    st.session_state["flash"] = result
    st.rerun()


def show_flash():
    if "flash" in st.session_state:
        ok, msg = st.session_state.pop("flash")
        (st.success if ok else st.error)(msg)
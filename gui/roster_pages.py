import streamlit as st
import pandas as pd
from app.schedule import DAYS
from gui.common import flash, show_flash


def show_roster_page(manager):
    st.header("Daily Roster")
    show_flash()

    day = st.selectbox("Select a day", DAYS)
    rows = manager.get_roster(day)
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info(f"No lessons scheduled on {day}.")

    st.subheader("Student Check-in")
    if not manager.students or not manager.courses:
        st.warning("Add students and courses before checking in.")
        return
    with st.form("check_in_form"):
        students = {s.name: s.id for s in manager.students}
        courses = {c.name: c.id for c in manager.courses}
        sname = st.selectbox("Select Student", list(students))
        cname = st.selectbox("Select Course", list(courses))
        if st.form_submit_button("Check-in Student"):
            flash(manager.check_in(students[sname], courses[cname]))
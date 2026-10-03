import streamlit as st
from datetime import datetime
from app.schedule import ScheduleManager, DAYS
from gui.student_pages import show_student_management_page
from gui.roster_pages import show_roster_page
from gui.course_pages import show_course_page
from gui.history_pages import show_history_page


def show_summary(manager):
    st.header("Dashboard")
    today = datetime.now().date().isoformat()
    checkins = sum(a["timestamp"].startswith(today) for a in manager.attendance)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", len(manager.students))
    c2.metric("Teachers", len(manager.teachers))
    c3.metric("Courses", len(manager.courses))
    c4.metric("Check-ins today", checkins)
    weekday = datetime.now().strftime("%A")
    st.subheader(f"Today's lessons ({weekday})")
    rows = manager.get_roster(weekday) if weekday in DAYS else []
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No lessons scheduled today.")


def launch():
    st.set_page_config(layout="wide", page_title="Music School Management System")
    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()
    m = st.session_state.manager

    st.sidebar.title("MSMS Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Student Management", "Courses & Teachers",
                                      "Daily Roster", "Attendance History", "Payments (stub)"])
    if page == "Dashboard":
        show_summary(m)
    elif page == "Student Management":
        show_student_management_page(m)
    elif page == "Courses & Teachers":
        show_course_page(m)
    elif page == "Daily Roster":
        show_roster_page(m)
    elif page == "Attendance History":
        show_history_page(m)
    else:
        st.header("Payments")
        st.warning("This feature will be implemented in PST5.")
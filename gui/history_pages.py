import streamlit as st
import pandas as pd


def show_history_page(manager):
    st.header("Attendance History")
    rows = manager.get_attendance_rows()
    if not rows:
        st.info("No attendance recorded yet.")
        return
    df = pd.DataFrame(rows)
    c1, c2, c3 = st.columns(3)
    student = c1.selectbox("Student", ["All"] + sorted(df["Student"].unique()))
    course = c2.selectbox("Course", ["All"] + sorted(df["Course"].unique()))
    dates = c3.date_input("Date range", value=[], help="Pick a start and end date")
    if student != "All":
        df = df[df["Student"] == student]
    if course != "All":
        df = df[df["Course"] == course]
    if len(dates) == 2:
        d = pd.to_datetime(df["Date"]).dt.date
        df = df[(d >= dates[0]) & (d <= dates[1])]
    st.caption(f"{len(df)} record(s)")
    st.dataframe(df.drop(columns="Date"), use_container_width=True, hide_index=True)
    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"),
                       "attendance.csv", "text/csv")
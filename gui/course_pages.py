import streamlit as st
from datetime import time
from app.schedule import DAYS
from gui.common import flash, show_flash


def show_course_page(manager):
    st.header("Courses, Lessons & Teachers")
    show_flash()
    tab_courses, tab_lessons, tab_teachers = st.tabs(["Courses", "Lessons", "Teachers"])

    teacher_opts = {f"{t.name} ({t.speciality})": t.id for t in manager.teachers}

    with tab_courses:
        rows = [{"ID": c.id, "Course": c.name, "Instrument": c.instrument,
                 "Teacher": getattr(manager.get_teacher(c.teacher_id), "name", "?"),
                 "Students": len(c.enrolled_student_ids), "Lessons": len(c.lessons)}
                for c in manager.courses]
        st.dataframe(rows, use_container_width=True, hide_index=True)
        if teacher_opts:
            with st.form("course_form", clear_on_submit=True):
                name = st.text_input("Course name")
                teacher = st.selectbox("Teacher", list(teacher_opts))
                if st.form_submit_button("Add course"):
                    flash(manager.add_course(name, teacher_opts[teacher]))
        else:
            st.warning("Add a teacher first.")

    with tab_lessons:
        if not manager.courses:
            st.info("No courses yet.")
        else:
            course_opts = {c.name: c.id for c in manager.courses}
            course = manager.get_course(course_opts[st.selectbox("Course", list(course_opts))])
            if course.lessons:
                st.dataframe([{"Lesson ID": l["lesson_id"], "Day": l["day"],
                               "Start": l["start_time"], "Room": l["room"]}
                              for l in course.lessons], use_container_width=True, hide_index=True)
                rid = st.selectbox("Remove lesson ID", [l["lesson_id"] for l in course.lessons])
                if st.button("Remove lesson"):
                    flash(manager.remove_lesson(course.id, rid))
            else:
                st.info("This course has no lessons yet.")
            with st.form("lesson_form"):
                day = st.selectbox("Day", DAYS)
                start = st.time_input("Start time", value=time(16, 0), step=900)
                room = st.text_input("Room", value="Room A")
                if st.form_submit_button("Add lesson"):
                    flash(manager.add_lesson(course.id, day, start.strftime("%H:%M"), room))

    with tab_teachers:
        st.dataframe([{"ID": t.id, "Name": t.name, "Speciality": t.speciality}
                      for t in manager.teachers], use_container_width=True, hide_index=True)
        with st.form("teacher_form", clear_on_submit=True):
            name = st.text_input("Teacher name")
            spec = st.text_input("Speciality (instrument)")
            if st.form_submit_button("Add teacher"):
                flash(manager.add_teacher(name, spec))
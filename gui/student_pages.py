import streamlit as st
from gui.common import flash, show_flash


def show_student_management_page(manager):
    st.header("Student Management")
    show_flash()

    st.subheader("Find a Student")
    query = st.text_input("Search by name")
    results = manager.search_students(query) if query else manager.students
    if results:
        rows = []
        for s in results:
            courses = [manager.get_course(cid) for cid in s.enrolled_course_ids]
            rows.append({"ID": s.id, "Name": s.name,
                         "Courses": ", ".join(c.name for c in courses if c) or "None"})
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No students found.")

    st.subheader("Register New Student")
    instruments = manager.instruments()
    if not instruments:
        st.warning("Add a teacher first (Courses & Teachers page).")
    else:
        with st.form("registration_form", clear_on_submit=True):
            reg_name = st.text_input("New Student Name")
            reg_instrument = st.selectbox("First Instrument", instruments)
            if st.form_submit_button("Register Student"):
                if reg_name.strip():
                    student = manager.register_new_student(reg_name, reg_instrument)
                    flash((True, f"Registered {student.name}!") if student
                          else (False, "Could not register student."))
                else:
                    st.warning("Please enter a name.")

    if not manager.students:
        return
    st.subheader("Edit a Student")
    names = {f"{s.name} (#{s.id})": s.id for s in manager.students}
    sid = names[st.selectbox("Student", list(names))]
    student = manager.get_student(sid)

    with st.form("rename_form"):
        new_name = st.text_input("Name", value=student.name)
        if st.form_submit_button("Rename"):
            flash(manager.rename_student(sid, new_name))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Enroll in a course**")
        options = {c.name: c.id for c in manager.courses if c.id not in student.enrolled_course_ids}
        if options:
            choice = st.selectbox("Course", list(options), key="enroll_sel")
            if st.button("Enroll"):
                flash(manager.enroll(sid, options[choice]))
        else:
            st.caption("Already enrolled in every course.")
    with col2:
        st.markdown("**Remove from a course**")
        options = {manager.get_course(cid).name: cid for cid in student.enrolled_course_ids
                   if manager.get_course(cid)}
        if options:
            choice = st.selectbox("Course", list(options), key="unenroll_sel")
            if st.button("Remove from course"):
                flash(manager.unenroll(sid, options[choice]))
        else:
            st.caption("Not enrolled in any course.")

    st.markdown("**Delete student**")
    confirm = st.checkbox(f"Yes, permanently delete {student.name}")
    if st.button("Delete student", disabled=not confirm):
        flash(manager.delete_student(sid))
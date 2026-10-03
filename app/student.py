from app.user import User


class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.enrolled_course_ids = []

    def to_dict(self):
        d = super().to_dict()
        d["enrolled_course_ids"] = list(self.enrolled_course_ids)
        return d

    @classmethod
    def from_dict(cls, d):
        s = cls(d["id"], d["name"])
        s.enrolled_course_ids = list(d.get("enrolled_course_ids", []))
        return s
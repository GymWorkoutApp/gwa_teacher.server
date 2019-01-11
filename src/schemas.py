from gwa_framework.schemas.base import BaseSchema
from schematics.types import StringType


class TeacherInputSchema(BaseSchema):
    teacher_id = StringType(required=False, serialized_name='teacherId')
    current_gym_id = StringType(required=False, serialized_name='currentGymId')


class TeacherOutputSchema(BaseSchema):
    teacher_id = StringType(required=True, serialized_name='teacherId')
    current_gym_id = StringType(required=False, serialized_name='currentGymId')

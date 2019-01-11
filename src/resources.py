from typing import Dict
from uuid import uuid4

from gwa_framework.resource.base import BaseResource
from gwa_framework.utils.decorators import validate_schema

from src.cache import cache
from src.database import master_async_session, read_replica_async_session
from src.models import TeacherModel
from src.schemas import TeacherInputSchema, TeacherOutputSchema


class TeacherResource(BaseResource):
    cache = cache
    method_decorators = {
        'create': [validate_schema(TeacherInputSchema)],
        'update': [validate_schema(TeacherInputSchema)],
    }

    def create(self, request_model: 'TeacherInputSchema') -> Dict:
        teacher = TeacherModel()
        teacher.id = request_model.teacher_id or str(uuid4())
        teacher.current_gym_id = request_model.current_gym_id
        with master_async_session() as session:
            session.add(teacher)
            output = TeacherOutputSchema()
            output.teacher_id = teacher.id
            output.current_gym_id = teacher.current_gym_id
            output.validate()
            return output.to_primitive()

    def update(self, request_model: 'TeacherInputSchema', teacher_id=None):
        teacher = TeacherModel()
        teacher.id = teacher_id
        teacher.current_gym_id = request_model.current_gym_id
        with master_async_session() as session:
            session.merge(teacher)
            output = TeacherOutputSchema()
            output.teacher_id = teacher.id
            output.current_gym_id = teacher.current_gym_id
            output.validate()
            return output.to_primitive()

    def list(self, args=None, kwargs=None):
        with read_replica_async_session() as session:
            results = []
            for teacher in session.query(TeacherModel).all():
                output = TeacherOutputSchema()
                output.teacher_id = teacher.id
                output.current_gym_id = teacher.current_gym_id
                output.validate()
                results.append(output.to_primitive())
        return results

    def retrieve(self, teacher_id):
        with read_replica_async_session() as session:
            teacher = session.query(TeacherModel).filter_by(id=teacher_id).first()
            output = TeacherOutputSchema()
            output.teacher_id = teacher.id
            output.current_gym_id = teacher.current_gym_id
            output.validate()
            return output.to_primitive()

    def destroy(self, teacher_id):
        with master_async_session() as session:
            session.query(TeacherModel).filter_by(id=teacher_id).delete()
            return None


resources_v1 = [
    {'resource': TeacherResource, 'urls': ['/teachers/<teacher_id>'], 'endpoint': 'Teachers TeacherId',
     'methods': ['GET', 'PUT', 'PATCH', 'DELETE']},
    {'resource': TeacherResource, 'urls': ['/teachers'], 'endpoint': 'Teachers',
     'methods': ['POST', 'GET']},
]

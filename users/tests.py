from django.test import TestCase

from .models import MyUser, SubTask, Task


class TaskSubTaskRelationshipTests(TestCase):
    def test_subtasks_are_related_to_task_via_subtasks_manager(self):
        user = MyUser.objects.create_user(username='tester', password='12345678')
        task = Task.objects.create(user=user, title='Task', description='Task description')
        subtask = SubTask.objects.create(task=task, title='Subtask', description='Subtask description')

        self.assertEqual(task.subtasks.count(), 1)
        self.assertIn(subtask, task.subtasks.all())

    def test_task_does_not_have_parent_task_field(self):
        self.assertFalse(hasattr(Task, 'parent_task'))

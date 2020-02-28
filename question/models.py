from django.db import models

from users.models import User
from course.models import Course
from django.db.models import Sum


class Lesson(models.Model):
    title = models.CharField(max_length=400)
    description = models.CharField(max_length=400)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    prev = models.ForeignKey("Lesson", related_name="previousOne", on_delete=models.SET_NULL, blank=True, null=True)
    next = models.ForeignKey("Lesson", related_name="nextOne", on_delete=models.SET_NULL, blank=True, null=True)

    def get_score(self, user):
        correct_answers = Question.objects.filter(lesson=self.id).aggregate(Sum('score'))
        questions = LogQuestionUser.objects.filter(user=user, lesson=self, correct=True).aggregate(Sum('points'))

        to_use = 0

        if questions['points__sum'] is not None:
            to_use = questions['points__sum']
        else:
            return 0

        return {'possible': correct_answers['score__sum'], 'score': to_use,
                'decimal': (to_use / correct_answers['score__sum'])*100}

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.id is None:
            prev = Lesson.objects.filter(next=None, course=self.course).first()

            if prev is not None:
                self.prev = prev

            super(Lesson, self).save(force_insert, force_update, using, update_fields)

            if prev is not None:
                prev.next = self
                prev.save()

        else:
            super(Lesson, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        lesson = None

        if self.prev is not None:
            lesson = Lesson.objects.filter(pk=self.prev.id).first()

            if lesson is not None:
                lesson.next = self.next
                lesson.save()

        if self.next is not None:
            lesson = Lesson.objects.filter(pk=self.next.id).first()

            if lesson is not None:
                lesson.prev = self.prev
                lesson.save()

        super(Lesson, self).delete()


class Question(models.Model):
    A = "BO"
    B = "MC1C"
    C = "MCWC"
    D = "MCAC"
    TYPE_ANSWER_CHOICE = (
        (A, 'Boolean'),
        (B, 'Multiple choice one correct'),
        (C, 'Multiple choice more than one is correct'),
        (D, 'Multiple choice more than one answer is correct all of them mustbe answered correctly'),
    )

    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    value = models.CharField(max_length=400)
    type = models.CharField(max_length=4, choices=TYPE_ANSWER_CHOICE)
    score = models.IntegerField()

    def delete(self, using=None, keep_parents=False):
        answers = Answers.objects.filter(question=self.id)

        for item in answers:
            item.delete()

        super(Question, self).delete()


class LogQuestionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, blank=True, null=True)
    correct = models.BooleanField()
    points = models.IntegerField()


class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    value = models.TextField()
    correct = models.BooleanField()




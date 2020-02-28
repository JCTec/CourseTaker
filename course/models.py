from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=400)
    description = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published')
    prev = models.ForeignKey("Course", related_name="previousOne", on_delete=models.SET_NULL, blank=True, null=True)
    next = models.ForeignKey("Course", related_name="nextOne", on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.id is None:
            prev = Course.objects.filter(next=None).first()

            if prev is not None:
                self.prev = prev

            super(Course, self).save(force_insert, force_update, using, update_fields)

            if prev is not None:
                prev.next = self
                prev.save()

        else:
            super(Course, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        course = None

        if self.prev is not None:
            course = Course.objects.filter(pk=self.prev.id).first()

            if course is not None:
                course.next = self.next
                course.save()

        if self.next is not None:
            course = Course.objects.filter(pk=self.next.id).first()

            if course is not None:
                course.prev = self.prev
                course.save()

        super(Course, self).delete(using, keep_parents)

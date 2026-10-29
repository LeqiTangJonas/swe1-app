import datetime

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


@override_settings(ALLOWED_HOSTS=["testserver"])
class PollsViewTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="What is your favorite color?",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Blue",
        )

    def test_index_displays_published_questions(self):
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.question_text)

    def test_index_hides_future_questions(self):
        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=1),
        )

        response = self.client.get(reverse("polls:index"))

        self.assertNotContains(response, future_question.question_text)

    def test_detail_displays_choices(self):
        response = self.client.get(reverse("polls:detail", args=(self.question.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.choice.choice_text)

    def test_vote_increments_choice_and_redirects_to_results(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.pk,)),
            {"choice": self.choice.pk},
        )

        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)
        self.assertRedirects(
            response,
            reverse("polls:results", args=(self.question.pk,)),
        )

    def test_vote_without_choice_shows_error(self):
        response = self.client.post(reverse("polls:vote", args=(self.question.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please select a choice.")

from django.test import TestCase
from .serializers import NewsItemSerializer
from .models import NewsItem
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .views import generate_id, read_news
from django.contrib.auth.models import User


class GetAllNewsTest(TestCase):
    """Test module for GET all NewsItem API"""

    def setUp(self):
        # create dummy user

        user = User.objects.create(
            username="dummy", password="dummy", email="dummy@dummy.com"
        )
        NewsItem.objects.create(
            story_type="job",
            date_created="2022-12-25",
            created_by=user,
            title="obidatti is the goal 22443211",
            url="rand_url",
            news_detail="jajso swjshs shshwi shhwshs hshsiwhs hsjsiwhs",
            news_id=generate_id(),
        )

        NewsItem.objects.create(
            story_type="job",
            created_by=user,
            date_created="2022-12-25",
            title="messi wins the world cup",
            url="rand_url",
            news_detail="jajso swjshs shshwi shhwshs hshsiwhs hsjsiwhs",
            news_id=generate_id(),
        )
        NewsItem.objects.create(
            story_type="job",
            created_by=user,
            date_created="2022-12-25",
            title="obidatti is the goal 22443211",
            url="rand_url",
            news_detail="jajso swjshs shshwi shhwshs hshsiwhs hsjsiwhs",
            news_id=generate_id(),
        )
        NewsItem.objects.create(
            story_type="job",
            created_by=user,
            date_created="2022-12-25",
            title="obidatti is the goal 22443211",
            url="rand_url",
            news_detail="jajso swjshs shshwi shhwshs hshsiwhs hsjsiwhs",
            news_id=generate_id(),
        )

    def test_get_all_news(self):
        client = Client()
        # get API response
        response = client.get(reverse("read-news"))
        # get data from db
        news_items = NewsItem.objects.all()
        serializer = NewsItemSerializer(news_items, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

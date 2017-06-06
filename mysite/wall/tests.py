# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Post


def create_post(post_text, days):
    """
    Creates a post with the given `post_text` and published the
    given number of `days` offset to now (negative for posts published
    in the past, positive for posts that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(post_text=post_text, pub_date=time)

class PostViewTests(TestCase):

    def test_index_view_with_no_posts(self):
        """
        If no posts exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('wall:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_index_view_with_a_past_post(self):
        """
        Posts with a pub_date in the past should be displayed on the
        index page.
        """
        create_post(post_text="Past post.", days=-30)
        response = self.client.get(reverse('wall:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post.>']
        )

    def test_index_view_with_a_future_post(self):
        """
        Posts with a pub_date in the future should not be displayed on
        the index page.
        """
        create_post(post_text="Future post.", days=30)
        response = self.client.get(reverse('wall:index'))
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_index_view_with_future_post_and_past_post(self):
        """
        Even if both past and future posts exist, only past posts
        should be displayed.
        """
        create_post(post_text="Past post.", days=-30)
        create_post(post_text="Future post.", days=30)
        response = self.client.get(reverse('wall:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post.>']
        )

    def test_index_view_with_two_past_posts(self):
        """
        The index page may display multiple questions.
        """
        create_post(post_text="Past post 1.", days=-30)
        create_post(post_text="Past post 2.", days=-5)
        response = self.client.get(reverse('wall:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post 2.>', '<Post: Past post 1.>']
        )

        
class PostIndexDetailTests(TestCase):
    
    def test_detail_view_with_a_future_post(self):
        """
        The detail view of a post with a pub_date in the future should
        return a 404 not found.
        """
        future_post = create_post(post_text='Future post.', days=5)
        url = reverse('wall:detail', args=(future_post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_post(self):
        """
        The detail view of a post with a pub_date in the past should
        display the post's text.
        """
        past_post = create_post(post_text='Past post.', days=-5)
        url = reverse('wall:detail', args=(past_post.id,))
        response = self.client.get(url)
        self.assertContains(response, past_post.post_text)

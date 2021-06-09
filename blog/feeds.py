from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    """
    That provides users with the most recently updated content.
    Users will be able to subscribe to your feed usin a feed aggregator.
    """

    title = 'My Blog'
    link = reverse_lazy('blog:post_list')
    description = 'New post of my blog'

    def items(self):
        return Post.published.all()[:5]

    def items_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)

from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """
    that class allows us to associate objects to a particular websites
    that are running with your project.
    this comes in handy when we want to run multiple sites using a single django project
    make our site more visible in search engine rankings.
    """

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated

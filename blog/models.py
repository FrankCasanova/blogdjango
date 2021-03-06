from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.


class PublishedManager(models.Manager):
    """
    The managers provide a confortable custom system to query some determinate datas
    with a special method, for example "Post.publised.all" instead "Post.objects.all()
    """

    def get_queryset(self):
        # just return all post that has been published
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):

    """
    Data model for blog post.
    """

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)  # post title
    slug = models.SlugField(max_length=250,  # this field intended to be used in URLs
                            unique_for_date='publish')  # useful for SEO-friendly URLs (unique url for each publish)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')  # related name allow to acces related objects easily.
    body = models.TextField()
    # return a current datetime in a timezone-aware format.
    publish = models.DateTimeField(default=timezone.now)
    # when the post was published
    created = models.DateTimeField(auto_now_add=True)
    # the last time the post was update
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,  # status of a post
                              default='draft')

    objects = models.Manager()  # the defaul manager
    published = PublishedManager()  # Our custom manager
    # thirth party app, that app can help us to tag our post by subjects
    tags = TaggableManager()

    class Meta:
        # how ordering, so much important to include the comma
        ordering = ('-publish',)

    def __str__(self):  # human-readable representation of the object
        return self.title

    # now we will use the get_absolute_url in your templates to link to specific posts
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    """
    a model to store comments
    """
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')  # related_name allows us to name attr from the realted name
    # agter defining this, we can retrieve the post of a comment object using comment.post
    # as if it were implicit on the model.
    # and retrieve all comments of a post using post.comments.all()
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'comment by {self.name} on {self.post} '

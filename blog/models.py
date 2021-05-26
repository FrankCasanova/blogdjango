from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    """
    The managers provide a confortable custom system to query some determinate datas
    with a special method, for example "Post.publised.all" instead "Post.objects.all()
    """  
    
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published') #just return all post that has been published
      

class Post(models.Model):
    
    """
    Data model for blog post.
    """
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=250) #post title
    slug = models.SlugField(max_length=250,         #this field intended to be used in URLs
                            unique_for_date='publish') #useful for SEO-friendly URLs (unique url for each publish)
    author = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='blog_posts') #related name allow to acces related objects easily.
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now) #return a current datetime in a timezone-aware format.
    created = models.DateTimeField(auto_now_add=True) #when the post was published
    update = models.DateTimeField(auto_now=True)# the last time the post was update
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, #status of a post
                              default='draft')
    
    objects = models.Manager() #the defaul manager
    published = PublishedManager() #Our custom manager
    
    class Meta:
        ordering = ('-publish',) #how ordering, so much important to include the comma
    
    def __str__(self): #human-readable representation of the object
       return self.title
    
    def get_absolute_url(self): #now we will use the get_absolute_url in your templates to link to specific posts
        return reverse('blog:post_detail',
                                        args=[self.publish.year,
                                              self.publish.month,
                                              self.publish.day,
                                              self.slug])
    
   
        

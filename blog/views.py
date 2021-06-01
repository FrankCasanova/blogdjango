from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail



# Create your views here.




# def post_list(request):
    
#     object_list = Post.published.all()    
#     paginator = Paginator(object_list,3) #3 posts in each page
#     page = request.GET.get('page')
    
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         #if page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         #if page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)        
    
#     return render(request,  
#                             template_name='blog/post/list.html',
#                             context={'posts': posts,
#                                      'page': page})
                  
def post_share(request, post_id):
    """
    retrieve a post by id
    """
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    
    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #form fields passed validation
            try:
                cd = form.cleaned_data
                post_url = request.build_absolute_uri(post.get_absolute_url)
                subject = f'{cd["name"]} recomends you read {post.title}'
                message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']} "
                send_mail(subject, message, 'frankcasanova.info@gmail.com', [cd['to']])
                sent = True
                
            except:
                form = EmailPostForm()
                
            # ... send email
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})    
    
        
    pass                  

def post_detail(request, year, month, day, post):
    
    post = get_object_or_404(Post,
                                slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day,)
    
    #list of active comments for this post
    comments = post.comments.filter(active=True) #leverage the post object to retrieve the related comment objects
    
    new_comment = None
    
    if request.method == 'POST':
        #a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment object but don't save to database yet
            #Calling with commit=False, allow us create an instance but without save changes on DB
            new_comment = comment_form.save(commit=False)
            #assign the current post to the comment
            #by doing this, we specify tha the new comment belongs to this post
            new_comment.post = post
            #save comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()    
    
        
    return render(request,
                            template_name='blog/post/detail.html',
                            context={'post': post,
                                     'comments': comments,
                                     'new_comment': new_comment,
                                     'comment_form': comment_form})
    
class PostListView(ListView):
    
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'    
                                
                                
                                 

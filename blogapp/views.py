from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .form import BlogPost

def home(request):
    blogs = Blog.objects #쿼리셋
    #블로그 모든 글들을 대상으로
    blog_list = Blog.objects.all()
    #블로그 객체 세 개를 한 페이지로 자른다
    paginator = Paginator(blog_list, 3)
    #request된 페이지가 뭔지를 알아내고 (request 페이지를 변수에 담아내고)
    page = request.GET.get('page')
    #request된 페이지를 얻어온 뒤 return 해 준다
    posts= paginator.get_page(page)
    return render(request, 'home.html', {'blogs':blogs, 'posts':posts})

def detail(request, blog_id):
    details = get_object_or_404(Blog, pk = blog_id)
    return render(request, 'detail.html', {'details':details})

def new(request): #new.html을 띄워주는 함수
    return render(request, 'new.html')

def create(request): #입력받은 내용을 데이터베이스에 넣어주는 함수
    blog = Blog() #객체 생성
    blog.title = request.GET['title'] #new.html에서 입력한 title을 가져와서 blog.title변수에 넣어준다.
    blog.body = request.GET['body']
    blog.pub_data = timezone.datetime.now() #블로그를 작성한 시점을 넣어준 그 시점
    blog.save() #쿼리셋 메소드 중 하나, 지금까지 넣은 데이터를 데이터베이스에 저장해라 라는 메소드 / 객체.delete() 데이터베이스에서 지워라
    return redirect('/blog/'+str(blog.id)) #blog.id는 int형이기때문, url 항상 문자열이기에 형변환
    # redirect (이동하고 싶은 url) , 데이터베이스에 저장, url로 이동
    # redirect와 return의 차이 = 인자에 따라 다른데, redirect는 다른 url을 입력할 수 있음, 프로젝트 외 url로 연결가능
    # render 3번째 인자, 키값, 데이터를 담아서 처리하고 싶을 때 사용

def blogpost(request):
    # 1. 입력된 내용을 처리하는기능 -> POST
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid(): #입력이 잘 됐는지 확인
            post = form.save(commit=False) #모델 객체를 반한하되, 저장하지 않고
            post.pub_data = timezone.now()
            post.save()
            return redirect('home')
    # 2. 빈페이지를 띄워주는 기능 -> GET
    else:
        form = BlogPost()
        return render(request, 'new.html', {'form':form})
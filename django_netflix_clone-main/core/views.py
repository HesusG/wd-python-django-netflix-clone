from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .forms import ProfileForm
from .models import CustomUser, Movie, Profile
from .serializers import MovieSerializer,CustomUserSerializer,ProfileSerializer



from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def api_view(request):

    num_Libros = Movie.objects.count()

    return Response({"num_Libros": num_Libros})

class MovieView(ModelViewSet):
    queryset = Movie.objects.all().order_by('id')
    serializer_class = MovieSerializer

class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer

class ProfileView(ModelViewSet):
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer

class Home(View):
    def get(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/profile/')
        return render(request,'index.html')

@method_decorator(login_required,name='dispatch')
class ProfileList(View):
    
    def get(self,request,*args, **kwargs):

        profiles=request.user.profiles.all()

        print(profiles)


        return render(request,'profileList.html',{
            'profiles':profiles
        })


@method_decorator(login_required,name='dispatch')
class ProfileCreate(View):
    def get(self,request,*args, **kwargs):
        form=ProfileForm()

        return render(request,'profileCreate.html',{
            'form':form
        })

    def post(self,request,*args, **kwargs):
        form=ProfileForm(request.POST or None)

       
        if form.is_valid():
            print(form.cleaned_data)
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect(f'/watch/{profile.uuid}')

        return render(request,'profileCreate.html',{
            'form':form
        })

@method_decorator(login_required,name='dispatch')
class Watch(View):
    def get(self,request,profile_id,*args, **kwargs):
        try:
            profile=Profile.objects.get(uuid=profile_id)

            movies=Movie.objects.filter(age_limit=profile.age_limit)

            try:
                showcase=movies[0]
            except :
                showcase=None
            

            if profile not in request.user.profiles.all():
                return redirect(to='core:profile_list')
            return render(request,'movieList.html',{
            'movies':movies,
            'show_case':showcase
            })
        except Profile.DoesNotExist:
            return redirect(to='core:profile_list')


@method_decorator(login_required,name='dispatch')
class ShowMovieDetail(View):
    def get(self,request,movie_id,*args, **kwargs):
        try:
            
            movie=Movie.objects.get(uuid=movie_id)

            return render(request,'movieDetail.html',{
                'movie':movie
            })
        except Movie.DoesNotExist:
            return redirect('core:profile_list')

@method_decorator(login_required,name='dispatch')
class ShowMovie(View):
    def get(self,request,movie_id,*args, **kwargs):
        try:
            
            movie=Movie.objects.get(uuid=movie_id)

            movie=movie.videos.values()
            

            return render(request,'showMovie.html',{
                'movie':list(movie)
            })
        except Movie.DoesNotExist:
            return redirect('core:profile_list')
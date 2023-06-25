from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import Student
from .serilizers import StudentSerilizer,UserSerilizer,RegisterSerilizer
from rest_framework.response import Response
from rest_framework import status
import requests
from django.contrib.auth import authenticate


# Create your views here.
def show(request):
    r = requests.get("http://127.0.0.1:8000/student")
    
    data = r.json()
    return render(request,'index.html',{'data':data})

def add(request):
    url = "http://127.0.0.1:8000/student"
    
    if request.method == 'POST':
        data = request.POST
        r = requests.post(url=url,data=data)
        # data = r.json()
        return  redirect('/show')

    return render(request,'add.html')
def update(request,id):
    url = f"http://127.0.0.1:8000/student/{id}"
    if request.method == 'GET':
        r = requests.get(url =url)
        data = r.json()

    if request.method == 'POST':
        data = request.POST
        r = requests.put(url=url,data=data)
        data = r.json()
        print(data)
        return  redirect('/show')

    # return render(request,'add.html')
    return render(request,'update.html',{'data':data,'id':id})


def delete(request,id):

    url = f"http://127.0.0.1:8000/student/{id}"
    requests.delete(url=url)
    return  redirect('/show')



    # data = request.POST
    return render(request,'add.html')

def login(request):
    if request.method == 'POST':
        data = request.POST
        url = "http://127.0.0.1:8000/login"

        r = requests.get(url = url,data = data)
        if (r.json()):
            return redirect('/show')


        
    
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        data = request.POST
        url = "http://127.0.0.1:8000/login"

        r = requests.post(url = url,data = data)
        return redirect('/')


        
    
    return render(request,'login.html')
    

def logout(register):
    pass

class LoginApi(APIView):
    def get(self,request):
        print(request.data)
        username = request.data['username']
        password = requests.data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            request.Session['username'] = username
            return Response({'msg':'login completed'})


    def post(self,request):
        data = request.data
        user = RegisterSerilizer(data=data)
        if user.is_valid():
            user.save()
            return Response({'msg':'created successfully'})
class studentApi(APIView):
    def get(self,request,pk=None):
        # id = request.data.get('pk')

        if pk is not None:
            stu = Student.objects.get(id = pk)
            serilizer = StudentSerilizer(stu)
            # serilizer.data['id']=id
            # response_data = serializer.data
            # response_data['id'] = instance.id
            return Response(serilizer.data)



            
        stu = Student.objects.all()
        serilizer = StudentSerilizer(stu,many = True)
        # serilizer.data['id']=id
        return Response(serilizer.data)
    def post(self ,request):
        serilizer = StudentSerilizer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Data Created'})
        return Response({'msg':'data not created'})
    def delete(self,request,pk):
        id = request.data.get('pk')
        stu = Student.objects.get(id = pk)
        stu.delete()
        return Response({'msg':'data deleted successfully'})
    
    def put(self,request,pk):
        stu = Student.objects.get(id =pk)
        # stu = self.get_object(pk)
        serilizer = StudentSerilizer(stu,data=request.data)
        # serializer = StudentSerilizer(stu, data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

        


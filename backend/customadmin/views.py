from app.models import CustomUser
from .serializers import AdminCustomSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from django.db.models import Q


class AdminLogin(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        print(email,password)
        
        if not(email and password):
            raise AuthenticationFailed({
                'error':'Both email and password is required'
            })
        
        user = CustomUser.objects.filter(email=email,is_staff=True).first()
        if user is None:
            raise AuthenticationFailed({'error':'Admin Access is required'})

        if not user.check_password(password):
            raise AuthenticationFailed({"error":'Incorrect Password'})
        
        payload = {
            'id':user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm="HS256")
        response = Response()
        
        response.data = {
            'jwt' : token
        }
        
        return response


class AdminUsersList(APIView):
    def get(self, request):
        obj = CustomUser.objects.filter(is_staff=False)
        print(obj)
        serializer = AdminCustomSerializers(obj, many=True)
        return Response(serializer.data)
    
class AdminUpdateUser(APIView):
    def post(self,request,pk):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        print(first_name,last_name,email,phone)
        user_obj = CustomUser.objects.filter(pk=pk).first()
        if user_obj:
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = email
            user_obj.phone = phone
            user_obj.save()
            return Response({"message":"User Updated Successfully"})
        else:
            return Response({"error":"User Not Found"})
        
class AdminUserDelete(APIView):
    def post(self,request,pk):
        user_obj = CustomUser.objects.filter(pk=pk).first()
        name = user_obj.first_name
        print(name)
        user_obj.delete()
        print("Deleted")
        return Response({
            "message" : f"Deleted user{name}"
        })
        
        
class AdminSearchUser(APIView):
    def get(self,request):
        name = request.query_params.get('name')
        name = name.strip()
        if not name:
            user_obj = CustomUser.objects.filter(is_staff=False)
        else:
            user_obj = CustomUser.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name) | Q(email__icontains=name),is_staff = False)
        serializer = AdminCustomSerializers(user_obj,many=True)
        return Response(serializer.data)
        

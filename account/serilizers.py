from rest_framework import serializers
from .models import Student
from django.contrib.auth.models import User

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerilizer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = User
        fields = ['username','password']
        extra_kwargs = {'password': {'write_only': True},}

        

class StudentSerilizer(serializers.Serializer):
    id = serializers.IntegerField( read_only=True)
    name = serializers.CharField(max_length = 100)
    age = serializers.IntegerField()
    address = serializers.CharField(max_length = 100)

    def create(self, validated_data):
        return Student.objects.create(name = validated_data['name'],age = validated_data['age'],address =validated_data['address'])
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.age = validated_data.get('age',instance.age)
        instance.address = validated_data.get('address',instance.address)
        instance.save()
        return instance
        # return super().update(instance, validated_data)
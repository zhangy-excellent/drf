from rest_framework import serializers

from api.models import Teacher
from drf_day2 import settings


class TeacherSerializer(serializers.Serializer):
    #定义序列化器类
    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    phone = serializers.CharField()
    # pic = serializers.ImageField()
    gender = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()


    def get_gender(self,obj):
        print(obj.get_gender_display())
        return obj.get_gender_display()

    def get_pic(self,obj):
        return "%s %s %s"%("http://127.0.0.1:8000/",settings.MEDIA_URL,str(obj.pic))

class TeacherDeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=3,
        min_length=2,
        error_messages={
            "max_length":"太长啦",
            "min_length":"太短啦",
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()

    def validate(self, attrs):#arrs是一个orderedDict类型的字典[(键,值),(),()]
        print("先执行",attrs.get("username"))#attrs.get可以直接获得键对应的值
        return attrs

    def validate_username(self,obj):
        pass
        print(obj,type(obj),21111111111)#此时的obj就是JSON的username
        return obj

    def create(self, validated_data):
        print(self,validated_data)
        return Teacher.objects.create(**validated_data)
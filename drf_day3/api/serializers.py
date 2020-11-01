from rest_framework import serializers

from api.models import Book, Press
from drf_day3 import settings

class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ["press_name", "address"]

class BookModelSerializer(serializers.ModelSerializer):
    # 自定义连表查询
    # 必须是publish,必须是外键,否则报错,就是说这个publisher必须是当前表的外键,否则报错,或者底下的fields不显示publish也不行,也报错呢
    publish = PressModelSerializer()  # 不加这句话之前就只显示1,2,3,之类的,加了以后,就显示上面那个类的fields里的东西

    class Meta:
        # 指定当前序列化器要序列化的模型
        model = Book
        # 比如说我只想要一个press_name
        fields = ("book_name", "price", "publish", "press_name", "author_list","pic")

        # depth = 1 #不常用
        # fields = "__all__"
        # exclude = ("create_time",)#得加,

class BookDeModelSerializer(serializers.ModelSerializer):
    # 反序列化器
    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "publish", "author")

        # 添加DRF提供的默认校验,is_valid就是判断这个的
        extra_kwargs = {
            "book_name": {
                "required": True,  # 必加字段,
                "min_length": 2,  # 最小长度,
                "error_messages": {
                    "required": "图书名必须提供",  # 必加字段,
                    "min_length": "图书名不能小于2个字符"
                }
            }
        }

    # 仍然支持全局钩子与局部钩子的使用

    def validate(self, attrs):
        print(1111111)
        return attrs

    # 先执行局部钩子
    def validate_book_name(self, obj):
        print(2222222222)
        return obj

class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print(instance)  # 要修改的实例
        print(validated_data)  # 要修改的实例的值
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance

class BookDeModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "press_name", "author_list", "pic", "author")
        list_serializer_class = BookListSerializer

        extra_kwargs = {
            "book_name": {
                "required": True,  # 必加字段,
                "min_length": 2,  # 最小长度,
                "error_messages": {
                    "required": "图书名必须提供",  # 必加字段,
                    "min_length": "图书名不能小于2个字符"
                }
            },
            "press_name": {
                "read_only": True
            },

            "author_list": {
                "read_only": True
            },

            # "pic": {
            #     "write_only": True
            # },

            "author": {
                "write_only": True
            }
        }

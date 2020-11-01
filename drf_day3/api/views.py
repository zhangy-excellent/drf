from django.http import HttpResponse
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, views
from api.models import Book
from api.serializers import BookModelSerializer, BookDeModelSerializer, BookDeModelSerializerV2
from rest_framework import mixins,generics,viewsets

class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book = Book.objects.get(pk=book_id)
            data = BookModelSerializer(book).data

            # return Response({
            #     "status": 200,
            #     "message": "查询单个图书成功1",
            #     "result": data,
            # })
            return Response(data)
        else:
            book_objects_all = Book.objects.all()
            data = BookModelSerializer(book_objects_all,many=True).data
            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "result": data,
            })

    def post(self,request,*args,**kwargs):
        request_data = request.data
        print(request_data)
        serializer = BookDeModelSerializer(data=request_data)#要加data=,否则报错

        serializer.is_valid(raise_exception=True)#直接将异常抛出来
        book_obj = serializer.save()
        #原来是手动抛异常,现在直接加个参数就行了
        #if serializer.is_valid()...
            #raise....

        return Response({
            "status": 200,
            "message": "添加图书成功",
            "result": BookModelSerializer(book_obj).data,
        })

class BookAPIViewV2(APIView):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book = Book.objects.get(pk=book_id,is_delete=False)
            data = BookDeModelSerializerV2(book).data

            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "result": data,
            })
        else:
            book_objects_all = Book.objects.filter(is_delete=False)
            data = BookDeModelSerializerV2(book_objects_all,many=True).data
            return Response({
                "status": 200,
                "message": "查询所有图书成功1",
                "result": data,
            })


    def post(self,request,*args,**kwargs):
        #增加单个:传递参数是字典
        #增加多个:[{}{}{}{}],列表中嵌套的是一个个的图书对象
        request_data = request.data

        if isinstance(request_data,dict):#代表添加的是单个对象
            many = False
        elif isinstance(request_data,list):#代表添加的是多个对象
            many = True
        else:
            return Response({
                "status": 400,
                "message": "参数有误",
            })
        serializer = BookDeModelSerializerV2(data=request_data,many=many)#要加data=,否则报错
        serializer.is_valid(raise_exception=True)#直接将异常抛出来
        book_obj = serializer.save()
        #原来是手动抛异常,现在直接加个参数就行了
        #if serializer.is_valid()...
            #raise....
        return Response({
            "status": 200,
            "message": "添加单个图书成功",
            "result": BookDeModelSerializerV2(book_obj,many=many).data,
        })

    def delete(self,request,*args,**kwargs):
        #删除单个:通过url传id
        #删除多个:有多个id,{ids:[1,2,3]}
        book_id = kwargs.get("id")
        if book_id:
            #删除单个
            ids = [book_id]

        else:
            #删除多个
            ids = request.data.get("ids")
            print(ids)
            pass

        response = Book.objects.filter(pk__in=ids,is_delete=False).update(is_delete=True)
        print(response,type(response))
        if response:
            return Response({
                "status":200,
                "message":"删除成功"
            })
        return Response({
            "status": 400,
            "message": "删除失败或图书不存在"
        })

    def put(self,request,*args,**kwargs):
        """
        修改单个:修改一个对象的全部字段
        修改多个
        局部修改单个:,partial=True
        局部修改多个
        """
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status":400,
                "message":"图书不存在"
            })
        #更新的时候对前端传递的数据进行安全校验
        #更新的时候需要指定关键字参数data
        #如果是修改,需要指定关键字参数instance,指定要修改的实例对象是哪一个
        #不加instance这个属性就是新建的意思,加了就是修改
        #底层调用ModelSerializer的update帮助完成了更新
        #反序列化的时候加data=
        serializer = BookDeModelSerializerV2(data=request_data,instance=book_obj,partial=True)
        serializer.is_valid(raise_exception=True)

        #经过序列化器  全局钩子  局部钩子校验后  开始更新
        serializer.save()

        return Response({
            "status":200,
            "message":"修改成功",
            "result":BookDeModelSerializerV2(book_obj).data
        })

    def patch(self,request,*args,**kwargs):
        """
        单个:id,传递的修改的内容   1 [book_name:"python"]
        多个:多个id,多个request.data
        id:[1,2,3] request.data [{}{}{}{}]
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.data
        book_id = kwargs.get("id")
        print(request_data)
        # print(book_ids)
        if book_id and isinstance(request_data,dict):
            book_ids = [book_id]
        elif not book_id and isinstance(request_data,list):
            book_ids = []
            for dic in request_data:
                pk = dic.pop("id",None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message":"PK不存在"
                    })
        else:
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"参数格式有误"
            })
        book_list = []#所有要修改的图书对象
        new_data = []#图书对象要修改的值
        for index,pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
            except Book.DoesNotExist:
                continue
                #图书对象不存在,将id和其数据移除
        Book_ser = BookDeModelSerializerV2(data=new_data,instance=book_list,partial=True,many=True)
        Book_ser.is_valid(raise_exception=True)
        Book_ser.save()
        return Response({
            "status":status.HTTP_200_OK,
            "message":"修改成功",
        })


#GenericAPIView可以完成查询单个,查询多个,但代码量没减少多少,主要不是让开发者用,是与mixins结合使用
class BookGenericView(GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookDeModelSerializerV2
    def get(self,request,*args,**kwargs):
        if kwargs.get("pk"):
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)

    #这里的lookup_field规定了url中应该使用<str:...>,参数要匹配,不然报错
    # lookup_field = "id"
    # def get(self,request,*args,**kwargs):
    #     #此处的get(名字),名字必须是lookup_field里规定好的,不然会报错
    #     book_id = kwargs.get("pk")
    #     if book_id:
    #         book_obj = self.get_object()
    #         serializer_data = self.get_serializer(book_obj,many=False).data
    #         return Response({
    #             "status": 200,
    #             "result": serializer_data
    #         })
    #     else:
    #         # 获取要操作的book模型中的所有数据,该方法得到一个queryset对象,里面放的是所有你需要的model对象
    #         book_list = self.get_queryset()
    #     #获取一个序列化器,这里面有很多杂的东西,那些错误信息error_message啥的
    #         serializer = self.get_serializer(book_list,many=True)
    #         #获得序列化后的数据
    #         serializer_data = serializer.data
    #         return Response({
    #             "status":200,
    #             "result":serializer_data
    #         })


class BookGenericViewV2(generics.CreateAPIView,generics.ListAPIView,generics.RetrieveAPIView,generics.UpdateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookDeModelSerializerV2
    lookup_field = "pk"


class BookViewSetView(viewsets.GenericViewSet,mixins.ListModelMixin):#viewsets.GenericViewSet,mixins.ListModelMixin
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookDeModelSerializerV2
    lookup_field = "pk"
    def user_login(self,request,*args,**kwargs):
        print("登陆成功")
        return Response("登陆成功")

    def get_user_count(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def user_register(self,request,*args,**kwargs):
        print("您已注册成功")
        return Response("您已注册成功")

> 摘要：本文是基于[项目文档](https://gitee.com/liuwei16/sweettalk-django4.2/blob/main/docs/P09.md)来完成task4的任务。上一个task我们学习了如何在view.py中添加方法来实现不同的接口，这次任务我们将学习Django中的一个新概念-APIView，APIview可以将增删改查函数封装在一个类中，大大提高了代码可读性。此外，本次任务还将学习序列化的使用，可以将响应结果转换为 json格式返回给前端。
## 序列化的使用
概念：将 queryset 和 instance 转换为 json/xml/yaml 返回给前端

用法：新建```serializers.py```,定义如下：

```python
from rest_framework.serializers import *
from .models import *

class GoodsCategorySerilizer(ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsSerializer(ModelSerializer):
    category = GoodsCategorySerilizer() # 外键字段相关的数据 需要单独写
    class Meta:
        model = Goods # 指定需要序列化的表
        fields = '__all__' # 所有需要序列化的字段
        # fields = ('name', 'number') # 指定需要序列化的字段
```
### 序列化对象
序列化单个对象（instance）：

```python
data = Goods.objects.get(id=1)
serializer = GoodsSerializer(instance=data)
print(serializer.data)
```

序列化多个对象（queryset）：

```python
data = Goods.objects.all() # 获取对象
serializer = GoodsSerializer(instance=data,many=True) # 创建序列化器，many表示序列化多个对象，默认为单个
print(serializer.data) # 转换数据
```
## APIView 的使用
APIview 是 Django REST Framework 提供的一个视图类。上一节中我们需要定义多个函数来实现不同的API，APIview可以将多个函数封装在一个类中，大大提高了代码可读性。我们只需要在view.py中分别为两个类新增get post delete方法，将代码新增如下：

```python
# 面向对象编程
class GoodsCategoryAPI(APIView):
    def get(self, request):
        data = GoodsCategory.objects.all()
        serializer = GoodsCategorySerilizer(instance=data, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        category_name = request.data.get('分类名字')
        remark = request.data.get('备注', '无')
        category, created = GoodsCategory.objects.get_or_create(name=category_name, remark=remark)
        if not created:
            return Response({"status": "已存在", "category": category_name}, status=200)
        else:
            return Response({"message": f"Successfully inserted category '{category_name}'."})
    
    def delete(self, request):
        name = request.data.get('分类名字')
        try:
            cate_to_del = GoodsCategory.objects.filter(name=name)
            cate_to_del.delete()
            return Response({"status": "success" ,"category": name}, status=200)
        except Exception as e:
            return Response({"message": f"Failed for del '{name}' with error: {e}"}, status=404)

class GoodsAPI(APIView):
    def get(self, request):
        name = request.data.get('name', '')
        try:
            if name:
                good = Goods.objects.filter(name=name)
                serializer = GoodsSerializer(instance=good, many=True)
                print(serializer.data)
                return Response(serializer.data)
            else:
                data = Goods.objects.all()
                serializer = GoodsSerializer(instance=data, many=True)
                print(serializer.data)
                return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"Failed for del '{name}' with error: {e}"}, status=404)

    def delete(self, request):
        name = request.data.get('name')
        try:
            cate_to_del = GoodsCategory.objects.filter(name=name)
            print(type(cate_to_del), cate_to_del)
            cate_to_del.delete()
            return Response({"status": "del success"}, status=200)
        except Exception as e:
            return Response({"message": f"Failed for del '{name}' with error: {e}"}, status=404)
    
    def post(self, request):
        cate_name = request.data.get("Goodscategory")
        category_ins = GoodsCategory.objects.get(name=cate_name)
        if not category_ins:
            category_ins = GoodsCategory(name=cate_name)
            category_ins.save()
        request_data = {
            "category": category_ins,
            "number": request.data.get("number", 1),
            "name": request.data.get("name"),
            "barcode": request.data.get("barcode", 1),
            "spec": request.data.get("spec", 'high'),
            "shelf_life_days": request.data.get("shelf_life_days", 5),
            "purchase_price": request.data.get("purchase_price", 5),
            "retail_price": request.data.get("retail_price", 5),
            "remark": request.data.get("remark", '无'),
        }
        try:
            new_goods = Goods.objects.create(**request_data)
            serializer = GoodsSerializer(instance=new_goods) # 对创建的对象进行序列化，并作为响应返回
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"Failed with {e}"}, status=404)
```
然后在urls.py新增：

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('insertgoodscategory/', InsertGoodsCategory),
    path('filtergoodscategory/', FilterGoodsCategory),
    path('delgoodscategory/', DelGoodsCategory),
    path('addgoods/', AddGoods),
    path('goodscateapi/', GoodsCategoryAPI.as_view()),
    path('goodsapi/', GoodsAPI.as_view()),
]
```
之后打开postman，输入```http://127.0.0.1:8000/goodscateapi/```和```http://127.0.0.1:8000/goodsapi/```，分别选用GET POST DELETE方法就可以对两个表进行增删改查了。

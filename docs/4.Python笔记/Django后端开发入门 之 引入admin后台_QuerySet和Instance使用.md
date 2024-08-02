
> 摘要：本文是基于[项目文档](https://gitee.com/liuwei16/sweettalk-django4.2#day3)来完成day3的任务，day3的任务是，通过项目文档了解了如何引入 admin 后台和管理员，如何使用postman进行接口测试。

## 引入 admin 后台和管理员
创建后台管理员需要执行如下指令
```python
python manage.py createsuperuser
```
根据提示填入账号名，邮箱，密码，然后执行：
```python
python manage.py runserver
```
服务启动之后，在浏览器中输入http://127.0.0.1:8000/admin
可以用刚才设置的账号密码进行登陆了。
最后需要在admin.py文件中注册你的模型：
```python
from django.contrib import admin
from .models import Goods, GoodsCategory
# Register your models here.
admin.site.register(Goods) # 在admin站点中 注册产品表
admin.site.register(GoodsCategory) # 在admin站点中 注册产品表
```
## 外键的使用
按照项目文档：
step1: 修改apps/erp_test/view.py
```python
from django.shortcuts import render
from rest_framework.response import Response
from .models import GoodsCategory, Goods
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
# Create your views here.

# 函数式编程
@api_view(['POST', 'GET'])
def InsertGoodsCategory(request):
    category_name = request.data.get('分类名字')
    # 获取分类对象或创建新的分类对象
    category, created = GoodsCategory.objects.get_or_create(name=category_name)
    # 判断是否已存在分类
    if not created:
        return Response({"status": "已存在", "goods_category": category_name}, status=200)
    else:
        return Response({"message": f"Successfully inserted category '{category_name}'."})

@api_view(['POST','GET'])
def FilterGoodsCategory(request):
    data = request.data.get('分类名字')
    goods = GoodsCategory.objects.filter(name=data)
    if goods.exists():
        return Response({"status": "已存在", "goods_category": data}, status=200)
    else:
        return Response({"status": "不存在" ,"goods_category": data}, status=404)
```
step 2：修改erp/urls.py
```python
from django.contrib import admin
from django.urls import path
from apps.erp_test.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filtergoodscategory/', FilterGoodsCategory),
    path('insertgoodscategory/', InsertGoodsCategory),
  ]
```
### postman下载和使用
前往https://www.postman.com/downloads/，当然也可以使用postman的web版，不过速度比较慢。
启动服务：```python manage.py runserver```
New一个HTTP请求，输入http://127.0.0.1:8000/filtergoodscategory/，测试刚才新增的api，没什么问题的话应该会返回：
```python
{
    "status": "已存在",
    "goods_category": "交通工具"
}
```
## 熟悉QuerySet 和 Instance
按照项目文档执行：
```python
queryset = GoodsCategory.objects.all()
print(type(queryset), queryset)
```
可以看到输出的类型是：
```python
<class 'django.db.models.query.QuerySet'> <QuerySet [<GoodsCategory: GoodsCategory object (1)>, <GoodsCategory: GoodsCategory object (4)>]>
```
## 增删查改
在view.py文件中添加如下功能分别实现增删改查：

```python
# 函数式编程
@api_view(['POST', 'GET'])
def InsertGoodsCategory(request):
    category_name = request.data.get('分类名字')
    remark = request.data.get('备注', '无')
    print(remark)
    category, created = GoodsCategory.objects.get_or_create(name=category_name, remark=remark)
    print(type(category), category)
    # 判断是否已存在分类
    if not created:
        return Response({"status": "已存在", "category": category_name}, status=200)
    else:
        return Response({"message": f"Successfully inserted category '{category_name}'."})

@api_view(['POST','GET'])
def FilterGoodsCategory(request):
    queryset = GoodsCategory.objects.all()
    print(type(queryset), queryset)
    data = request.data.get('分类名字')
    cate = GoodsCategory.objects.filter(name=data)
    print(type(cate), cate)
    if cate.exists():
        return Response({"status": "已存在", "goods_category": data}, status=200)
    else:
        return Response({"status": "不存在" ,"goods_category": data}, status=404)

@api_view(['POST','GET'])
def DelGoodsCategory(request):
    data = request.data.get('分类名字')
    try:
        cate_to_del = GoodsCategory.objects.filter(name=data)
        print(type(cate_to_del), cate_to_del)
        cate_to_del.delete()
        return Response({"status": "success" ,"category": data}, status=200)
    except Exception as e:
        return Response({"message": f"Failed for del '{data}' with error: {e}"}, status=404)


@api_view(['POST', 'GET'])
def AddGoods(request):
    cate_name = request.data.get("Goodscategory")
    category_ins = GoodsCategory.objects.get(name=cate_name)
    if not category_ins:
        category_ins = GoodsCategory(name=cate_name)
        category_ins.save()
    request_data = {
        "category": category_ins,
        "number": request.data.get("number"),
        "name": request.data.get("name"),
        "barcode": request.data.get("barcode"),
        "spec": request.data.get("spec"),
        "shelf_life_days": request.data.get("shelf_life_days"),
        "purchase_price": request.data.get("purchase_price"),
        "retail_price": request.data.get("retail_price"),
        "remark": request.data.get("remark"),
    }
    try:
        name = request.data.get("name")
        new_good = Goods.objects.create(**request_data)
        print(new_good)
        return Response({"message": f"Successfully add good'{name}'."})
    except Exception as e:
        return Response({"message": f"Failed for good '{name}' with {e}"}, status=404)
```
然后在urls.py文件中对应添加上：

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('insertgoodscategory/', InsertGoodsCategory),
    path('filtergoodscategory/', FilterGoodsCategory),
    path('delgoodscategory/', DelGoodsCategory),
    path('addgoods/', AddGoods),
]
```
通过postman测试对应接口

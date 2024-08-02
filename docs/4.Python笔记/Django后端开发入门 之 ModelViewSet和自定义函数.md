> 摘要：本文是基于[项目文档](https://gitee.com/liuwei16/sweettalk-django4.2/blob/main/docs/P11.md)来完成task5和task6的任务。上一个task我们学习了如何使用APIView来实现不同的接口，这次任务我们将学习Django中的一个新概念-ModelViewSet，ModelViewSet最大的优势是支持自定义函数，大大提高了代码可读性和自由度。为了将新建的方法引入到urls，我们还需要学习路由的概念，通过这种方式，就可以掌握如何在Django中便捷地对数据表进行增删改查了。
# ModelViewSet
概念：是 Django REST framework 提供的一个视图集类，它封装了常见的模型操作方法，包括默认的增删改查功能。也就是使用 ModelViewSet 后，你将自动获得默认的 CRUD 方法。

使用：
我们只需要在view.py中将代码新增如下：

```python
# modelviewset
class GoodsCategoryViewSet(ModelViewSet):
    queryset = GoodsCategory.objects.all()

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_obj = GoodsCategory.objects.latest('id') # 获取最大id对应的对象
        serializer = GoodsCategorySerilizer(instance=latest_obj)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get','post'])
    def delete_example(self, request):
        try:
            name = request.data.get('name', '')
            categories_to_delete = GoodsCategory.objects.filter(name=name)
            deleted_count = categories_to_delete.delete()
            print(f"Deleted {deleted_count} categories.")
            return Response({"status": "success" ,"category": name}, status=200)
        except Exception as e:
            return Response({"message": f"Failed for del with error: {e}"}, status=404)

    @action(detail=False, methods=['get','post'])
    def create_example(self, request):
        name = request.data.get('name')
        remark = request.data.get('remark', '无')
        category, created = GoodsCategory.objects.create(name=name, remark=remark)
        print(category, created)
        if not created:
            return Response({"status": "已存在", "category": name}, status=200)
        else:
            return Response({"message": f"Successfully create category '{name}'."})

class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.all()

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_obj = Goods.objects.latest('id') # 获取最大id对应的对象
        serializer = GoodsSerializer(instance=latest_obj)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get','post'])
    def delete_example(self, request):
        try:
            name = request.data.get('name', '')
            goods_to_delete = Goods.objects.filter(name=name)
            deleted_count = goods_to_delete.delete()
            print(f"Deleted {deleted_count} goods.")
            return Response({"status": "success" ,"goods": name}, status=200)
        except Exception as e:
            return Response({"message": f"Failed for del with error: {e}"}, status=404)

    @action(detail=False, methods=['get','post'])
    def create_example(self, request):
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
            serializer = GoodsSerializer(instance=new_goods)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"Failed with {e}"}, status=404)
```
## 自定义函数
上述代码中的@action的DRF中一个装饰器，用于在 ViewSet 中创建自定义动作（custom action），为 ViewSet 提供了更灵活应用且 @action 只在ViewSet视图集中生效。视图集中附加action装饰器可接收两个参数：
- methods: 声明该action对应的请求方式.
- detail: detail=False表示该动作不需要处理单个对象，而是处理整个集合；
# 路由组件
概念：将URL与视图函数或视图集关联起来的一种机制。Django REST framework的路由器通过简单的配置可以自动生成标准的URL路由，从而减少了手动编写URL路由的工作量。

用法：
在urls.py引入```from rest_framework import routers```，然后将view.py中新增的两个ModelViewSet注册进来：
```python
router = routers.DefaultRouter()
router.register('Goods', GoodsViewSet)
router.register('GoodsCate', GoodsCategoryViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('insertgoodscategory/', InsertGoodsCategory),
    path('filtergoodscategory/', FilterGoodsCategory),
    path('delgoodscategory/', DelGoodsCategory),
    path('addgoods/', AddGoods),
    path('goodscateapi/', GoodsCategoryAPI.as_view()),
    path('goodsapi/', GoodsAPI.as_view()),
]
urlpatterns += router.urls
```
# 接口测试
定义了上述自定义函数，并经过路由后，打开postman进行接口测试，注意在ViewSet后面需要接上自定义的方法名，如下：
```python
http://127.0.0.1:8000/GoodsCate/latest/
http://127.0.0.1:8000/GoodsCate/create_example/
http://127.0.0.1:8000/GoodsCate/delete_example/
http://127.0.0.1:8000/Goods/latest/
http://127.0.0.1:8000/Goods/create_example/
http://127.0.0.1:8000/Goods/delete_example/
```
可能遇到下面报错：
```python
You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set. Django can't redirect to the slash URL while maintaining POST data. Change your form to point to 127.0.0.1:8000/goodsapi/ (note the trailing slash), or set APPEND_SLASH=False in your Django settings. 
```
这个错误提示是由Django的APPEND_SLASH设置引起的。APPEND_SLASH设置为True时，Django会自动在URL末尾添加斜杠('/')，以确保URL一致性。但是，当使用POST请求访问不以斜杠结尾的URL时，Django无法在重定向时保持POST数据的完整性，因此会出现该错误。


所以以上url最后要加上'/'，这样，请求会直接匹配到以斜杠结尾的URL规则，而不会触发重定向。

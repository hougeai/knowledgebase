> 摘要：本文是基于[项目文档](https://gitee.com/liuwei16/sweettalk-django4.2#day2)来完成day2的任务，day2的任务是构建数据表并合并，通过项目文档了解数据表构建的基本原理，并尝试通过命令将代码和数据库关联上。

## 如何创建数据表
在项目文档中提高需要创建两个数据表，注意应该是在day1新建的apps/erp_test文件夹下，有个model.py文件，采用项目文档中的代码，同时需要注意import相关的模块：

```python
from django.db.models import Model, CharField, IntegerField, FloatField, ForeignKey, SET_NULL
```

## 配置数据表的字段
按照项目文档执行，需要注意的是第5行这里：应该去掉'goods.'，应该我们没有新建goods app

```python
category = ForeignKey('goods.GoodsCategory',
```
否则会出现如下报错：

```python
SystemCheckError: System check identified some issues:

ERRORS:
erp_test.Goods.category: (fields.E300) Field defines a relation with model 'goods.GoodsCategory', which is either not installed, or is abstract.
erp_test.Goods.category: (fields.E307) The field erp_test.Goods.category was declared with a lazy reference to 'goods.goodscategory', but app 'goods' isn't installed.
```

## 执行迁移
按照项目文档执行：
```python
python manage.py makemigrations
python manage.py migrate
```
看到成功信息：

```python
Operations to perform:
Apply all migrations: admin, auth, contenttypes, erp_test, sessions
Running migrations:
Applying erp_test.0001_initial... OK
```


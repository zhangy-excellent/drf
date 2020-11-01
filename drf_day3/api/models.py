from django.db import models

# Create your models here.
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Book(BaseModel):
    book_name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    pic = models.ImageField(upload_to="img",default="img/1.jpg")
    publish = models.ForeignKey(to="Press",on_delete=models.CASCADE,db_constraint=False,related_name="books")
    author = models.ManyToManyField(to="Author",db_constraint=False,related_name="books")


    class Meta:
        db_table = "bz_book"
        verbose_name = "图书"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name

    #自定义属性,加个property
    # @property
    # def aaa(self):
    #     return "aaa"

    @property
    def press_name(self):
        return self.publish.press_name#一个多可以这样,这样取到的就是唯一的
    @property#property加不加不影响使用,但建议加上
    def author_list(self):
        return self.author.values("author_name","age","detail__phone")

class Press(BaseModel):
    press_name = models.CharField(max_length=128)
    pic = models.ImageField(upload_to="img",default="img/1.jpg")
    address = models.CharField(max_length=256)

    class Meta:
        db_table = "bz_press"
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name

class Author(BaseModel):
    author_name = models.CharField(max_length=128)
    age = models.IntegerField()
    class Meta:
        db_table = "bz_author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name

class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)
    author = models.OneToOneField(to="Author",on_delete=models.CASCADE,related_name="detail")#related_name反向获取的名字detail__

    class Meta:
        db_table = "bz_author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s的详情" % self.author.author_name


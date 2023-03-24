from django.db import models
from django.db.models import CharField, ForeignKey


'''
Модель Menu - модель меню
'''
class Menu(models.Model):
    name = CharField(max_length=200, verbose_name='МЕНЮ')

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


'''
Модель MenuItem - модель пункта меню (может иметь родительский пункт - если не имеет, то на первом уровне вложенности)
'''
class MenuItem(models.Model):
    name = CharField(max_length=200, verbose_name='Пункт меню')
    menu = ForeignKey(Menu, verbose_name='Для меню', on_delete=models.CASCADE, related_name='menuitems')
    otheritem = ForeignKey('MenuItem', verbose_name='Пункт-родитель', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name

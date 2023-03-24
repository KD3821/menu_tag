from django import template
from django.template.loader import get_template
from one_app.models import *


register = template.Library()


def draw_menu(menu_name):
    menu_items = MenuItem.objects.select_related('menu', 'otheritem').order_by('menu__name')
    menu_names = []
    first_level = []
    '''
    Получаем названия всех меню и записываем в список "menu_names",
    Все пункты меню, которые не принадлежат активному меню и не имеют родительских пунктов, т.е. первого уровеня
    вложенности - записываем в список"first_level"
    '''
    for i in menu_items:
        if i.menu.name not in menu_names:
            menu_names.append(i.menu.name)
        if i.menu.name != menu_name and i.otheritem is None:
            first_level.append(i)
    sub_level = []
    '''
    Все пункты меню, которые не принадлежат активному меню и имеют родительские пункты, т.е. это второй и более уровень
    вложенности - записываем в список "sub_level"
    '''
    for i in menu_items:
        if i.menu.name != menu_name and i.otheritem is not None:
            sub_level.append(i)
    sub_context = {}
    '''
    Проверяем список "sub_level" на наличие в нем родственных пунктов меню - при наличии записываем в словарь 
    "sub_context" по схеме {ключ-родительский пункт : значение-список дочерних пунктов} и затем перепроверяем 
    чтобы ключи не повторялись в значениях.
    '''
    for i in sub_level:
        sub_list = []
        for j in sub_level:
            if j.otheritem == i:
                sub_list.append(j)
        if len(sub_list) > 0:
            sub_context[i] = sub_list
    remove_key_list = []
    for key in sub_context.keys():
        for value in sub_context.values():
            if key in value:
                index = value.index(key)
                value.pop(index)
                value.append({key: sub_context[key]})
                remove_key_list.append(key)
    for i in remove_key_list:
        sub_context.pop(i)
    menu_context = {}
    '''
    Связываем пункты меню первого уровня вложенности с остальными пунктами меню, проверяя имеются ли у них дочерние 
    пункты меню - проверяем являются ли они ключами словаря "sub_context". Результат записываем в словарь "menu_context"
    '''
    for i in first_level:
        menu_list = []
        for j in sub_level:
            if j.otheritem == i:
                if j not in sub_context.keys():
                    menu_list.append(j)
                else:
                    menu_list.append({j: sub_context[j]})
        menu_context[i] = menu_list
    final_context = {}
    '''
    Связываем названия меню из созданого вначале списка "menu_names" с элементами первого уровня меню из словаря 
    "menu_context". Также связываем имя активного меню с пунктами первого уровня,т.е. у которых нет родительских пунктов
    Остальным меню после активного меню ниже по списку назначаем вместо списка элементов первого уровня - пустой список.
    Результат записываем в словарь "final_context".   
    '''
    for i in menu_names:
        final_list = []
        if i != menu_name:
            for j in menu_context.keys():
                if j.menu.name == i:
                    final_list.append({j: menu_context[j]})
            final_context[i] = final_list
        else:
            for j in menu_items:
                if j.menu.name == menu_name and j.otheritem is None:
                    final_list.append(j)
            final_context[i] = final_list
            for name in menu_names:
                if name not in final_context.keys():
                    final_context[name] = []
            break
    return {'menus': final_context}

menu_template = get_template('custom_menu.html')
register.inclusion_tag(menu_template)(draw_menu)

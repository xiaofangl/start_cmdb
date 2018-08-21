#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.core.paginator import Paginator


def paging(data, page):
    if data:
        p = Paginator(data, 15)
        # 对象个数
        count = p.count
        #
        num_pages = p.num_pages

        pag = p.page(page)
        pag_data = pag.object_list
    return count, pag_data
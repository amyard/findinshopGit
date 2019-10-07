# -*- coding: utf-8 -*-


def set_paginator_window(page, window=10):
    if page.number < window/2:
        page.paginator.pages_window = range(1, min(window+1, page.paginator.num_pages+1))
    elif page.number > page.paginator.num_pages-window/2:
        page.paginator.pages_window = range(max(1, page.paginator.num_pages+1-window), page.paginator.num_pages+1)
    else:
        page.paginator.pages_window = range(page.number-window/2, page.number+window/2+1)

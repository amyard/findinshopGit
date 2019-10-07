# -*- coding: utf-8 -*-

#Python imports
import os
import xlwt
import StringIO

#Django imports
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


#TODO: change to celery task
def export_report(report_key):
    if not os.path.exists('%s/%s' % (settings.MEDIA_ROOT, 'report_export')):
        os.mkdir('%s/%s' % (settings.MEDIA_ROOT, 'report_export'))

    if os.path.exists('%s/report_export/%s.xls' % (settings.MEDIA_ROOT, report_key)):
        filename = '%s/report_export/%s.xls' % (settings.MEDIA_ROOT, report_key)                                
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type="application/ms-excel")
        response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % report_key
        return response

    book = xlwt.Workbook()
    sheet = book.add_sheet(u'Отчет о кликах')
    reports = cache.get(report_key)

    headings = [u'Раздел', u'Собственная категория', u'Продукт', u'Стоимость клика(грн.)', u'IP клика', u'Дата\Время']
    rowx = 0
    for colx, value in enumerate(headings):
        sheet.write(rowx, colx, value)

    sheet.set_panes_frozen(True) # frozen headings instead of split panes
    sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
    sheet.set_remove_splits(True) # if user does unfreeze, don't leave a split there

    data = []
    for report in reports.order_by('date'):
        data.append(
                [
                    report.section.name if report.section else '-',
                    report.category.name,
                    report.product_name,
                    report.cost,
                    report.ip if report.ip else '-',
                    report.date.strftime("%d.%m.%Y %H:%S")
                ]
        )

    for row in data:
        rowx += 1
        for colx, value in enumerate(row):
            sheet.write(rowx, colx, value)

    book.save('%s/report_export/%s.xls' % (settings.MEDIA_ROOT, report_key))

    filename = '%s/report_export/%s.xls' % (settings.MEDIA_ROOT, report_key)                                
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type="application/ms-excel")
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % report_key
    return response

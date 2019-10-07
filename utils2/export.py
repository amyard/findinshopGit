# def exportXML(request):
#     website = request.website
#     catalog = Catalog.objects.get(website=website)
#     categories = Category.objects.filter(catalog=catalog)
#     items = Item.objects.filter(category__in=categories, site=website)
#     xml_data = []
#     xml_data.append('<price>')
#     xml_data.append('<date>')
#     xml_data.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
#     xml_data.append('</date>')
#     xml_data.append('<firmName>' + smart_str(website.name) + '</firmName>')
#     xml_data.append('<firmId></firmId>')
#     xml_data.append('<rate/>')

#     xml_data.append('<categories>')
#     for row in categories:
#         xml_data.append('<category>')
#         xml_data.append('<id>' + str(row.id) + '</id>')
#         xml_data.append('<name>')
#         xml_data.append(conditional_escape(row.name))
#         xml_data.append('</name>')
#         if row.parent:
#             xml_data.append('<parentId>' + str(row.parent.id) + '</parentId>')
#         xml_data.append('</category>')
#     xml_data.append('</categories>')

#     xml_data.append('<items>')
#     for row in items:
#         xml_data.append('<item>')
#         xml_data.append('<id>' + str(row.id) + '</id>')
#         xml_data.append('<categoryId>' + str(row.category.id) + '</categoryId>')
#         xml_data.append('<code>' + row.code + '</code>')

#         if row.vendor:
#             vendor = conditional_escape(row.vendor)
#             xml_data.append('<vendor>' + vendor + '</vendor>')

#         name = conditional_escape(row.name)
#         xml_data.append('<name>' + name + '</name>')

#         xml_data.append('<description>')
#         if row.description:
#             desc = conditional_escape(row.description)
#             xml_data.append(desc)
#         xml_data.append('</description>')

#         xml_data.append('<url>')
#         if row.url:
#             url = row.url.replace('&', '&amp;')
#             xml_data.append(url)
#         xml_data.append('</url>')

#         xml_data.append('<image>')
#         if row.image_url:
#             image_url = row.image_url.replace('&', '&amp;')
#             xml_data.append(image_url)
#         xml_data.append('</image>')

#         xml_data.append('<priceRUAH>')
#         xml_data.append(row.priceRUAH)
#         xml_data.append('</priceRUAH>')
#         xml_data.append('<stock>')
#         xml_data.append(row.stock)
#         xml_data.append('</stock>')
#         xml_data.append('<guarantee>')
#         xml_data.append(row.guarantee)
#         xml_data.append('</guarantee>')
#         xml_data.append('</item>')
#     xml_data.append('</items>')

#     xml_data.append('</price>')
#     return HttpResponse(xml_data, content_type='text/xml')

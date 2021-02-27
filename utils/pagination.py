__author__ = "Ldaze"

from django.utils.safestring import mark_safe


class Page(object):
    # For turning pages
    def __init__(self, currentPage, count, per=10):
        self.currentPage = currentPage
        self.count = count
        self.per = per

    @property
    def start(self):
        return (self.currentPage - 1) * self.per

    @property
    def end(self):
        return self.currentPage * self.per

    @property
    def totalCount(self):
        v,y = divmod(self.count, self.per)
        if y:
            v += 1
        return v

    def page_str(self, base_url):
        page_list = []
        if self.currentPage <= 1:
            prev = '<li class="am-disabled"><a>«</a></li>'
        else:
            prev = '<li><a href="%s/%s">«</a></li>'%(base_url, self.currentPage-1)
        page_list.append(prev)

        for i in range(1, self.totalCount + 1):
            if i==self.currentPage:
                temp = '<li class="am-active"><a>%s</a></li>'%(self.currentPage)
            else:
                temp = '<li><a href="%s/%s">%s</a></li>'%(base_url,i,i)
            page_list.append(temp)
        if self.currentPage+1 > self.totalCount:
            nex = '<li class="am-disabled"><a>»</a></li>'
        else:
            nex = '<li><a href="%s/%s">»</a></li>'%(base_url, self.currentPage+1)
        page_list.append(nex)
        page_str = mark_safe("".join(page_list))
        return page_str

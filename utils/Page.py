# _author: lily
# _date: 2019/2/24

class PageHelper:
    def __init__(self, total, cur_page, base_url, per_page=10):
        self.total = total
        self.cur_page = cur_page
        self.base_url = base_url
        self.per_page = per_page

    @property
    def db_start(self):
        return (self.cur_page-1)*self.per_page

    @property
    def db_end(self):
        return self.cur_page*self.per_page

    def total_page(self):
        c, v = divmod(self.total, self.per_page)
        if v != 0:
            c += 1
        return c

    def page_str(self):

        c = self.total_page()
        page_list = []
        if self.cur_page == 1:
            page_list.append('<a href="javascript:void(0)">上一页</a>')
        else:
            page_list.append('<a href="%s?page=%i">上一页</a>' % (self.base_url, self.cur_page - 1))

        if c <= 11:
            page_range_start = 1
            page_range_end = c + 1
        else:
            if self.cur_page < 6:
                page_range_start = 1
                page_range_end = 12
            else:
                page_range_end = self.cur_page + 5 + 1
                if page_range_end > c:
                    page_range_start = c - 10
                    page_range_end = c + 1
                else:
                    page_range_start = self.cur_page - 5
                    page_range_end = self.cur_page + 5 + 1

        for i in range(page_range_start, page_range_end):
            if i == self.cur_page:
                temp = '<a class="active" href="%s?page=%i">%i</a>' % (self.base_url, i, i)
            else:
                temp = '<a href="%s?page=%i">%i</a>' % (self.base_url, i, i)
            page_list.append(temp)
        if self.cur_page == c:
            page_list.append('<a href="javascript:void(0)">下一页</a>')
        else:
            page_list.append('<a href="%s?page=%i">下一页</a>' % (self.base_url, self.cur_page + 1))
        page_str = ''.join(page_list)
        return page_str



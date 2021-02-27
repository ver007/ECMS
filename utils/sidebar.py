__author__ = "Ldaze"
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe


class Sidebar(object):
    # For rendering sidebar.
    def __init__(self, logger, username, type):
        self.logger = logger
        self.username = username
        self.sidebar_list = []
        if type == 0:
            self.type = '欢迎同学：'
        elif type == 1:
            self.type = '欢迎教工：'
        elif type == 2:
            self.type = '欢迎主任：'
        else:
            self.type = '欢迎系统管理员：'

    def head(self):
        self.sidebar_list.append('<div class="nav-navicon admin-main admin-sidebar">')
        self.sidebar_list.append('\n<div class="sideMenu am-icon-dashboard" '
                                 'style="color:#aeb2b7; margin: 10px 0 0 0;"> %s%s</div>' % (self.type, self.username))
        self.sidebar_list.append('<div class="sideMenu">')
        for item in self.logger:
            col = '''\n<h3 class="am-icon-gears"><em></em> <a href="#">%s</a></h3>\n<ul>''' % item.column
            self.sidebar_list.append(col)
            for i in range(1, 4):
                command1 = 'item.url%s' % i
                command2 = 'item.item%s' % i
                if eval(command2):
                    temp = '\n<li><a href="%s">%s</a></li>' % (eval(command1), eval(command2))
                    self.sidebar_list.append(temp)
                else:
                    break
            self.sidebar_list.append('\n</ul>')
        self.sidebar_list.append('\n</div>')

    def script(self):
        scriptStr = """
<script type="text/javascript">
    jQuery(".sideMenu").slide({
    titCell:"h3",
    targetCell:"ul",
    effect:"slideDown",
    delayTime:300 ,
    triggerTime:150,
    defaultPlay:true,
    returnDefault:true
    });
</script>"""
        self.sidebar_list.append(scriptStr)

    def sidebar_str(self):
        self.head()
        self.script()
        self.sidebar_list.append('\n</div>')
        sidebar_str = mark_safe("".join(self.sidebar_list))
        return sidebar_str

# if __name__ == "__main__":

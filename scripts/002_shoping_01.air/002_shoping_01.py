# -*- encoding=utf8 -*-
__author__ = "10237"

from airtest.core.api import *

auto_setup(__file__)


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

touch(Template(r"tpl1776849715729.png", record_pos=(-0.375, 0.973), resolution=(1260, 2800)))
touch(Template(r"tpl1776850035276.png", record_pos=(-0.231, 0.616), resolution=(1260, 2800)))
touch(Template(r"tpl1776850054277.png", record_pos=(0.296, 0.977), resolution=(1260, 2800)))
print((poco("com.dkzsxt.ruizhidian:id/total_price_view").get_text()))
assert_equal(poco("com.dkzsxt.ruizhidian:id/total_price_view").get_text(), "￥500", "确认订单页，实付款金额！")

if not exists(Template(r"tpl1776850479110.png", record_pos=(-0.419, 0.748), resolution=(1260, 2800))):
    touch(Template(r"tpl1776850311007.png", record_pos=(-0.419, 0.748), resolution=(1260, 2800)))
touch(Template(r"tpl1776850514908.png", record_pos=(0.245, 0.975), resolution=(1260, 2800)))







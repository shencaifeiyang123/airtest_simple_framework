# -*- encoding=utf8 -*-
__author__ = "10237"

from airtest.core.api import *

auto_setup(__file__)

wake()
start_app("com.dkzsxt.ruizhidian")

touch(Template(r"tpl1776329476227.png", record_pos=(0.377, 0.972), resolution=(1260, 2800)))
touch(Template(r"tpl1776329500849.png", record_pos=(-0.071, -0.801), resolution=(1260, 2800)))
touch(Template(r"tpl1776329520251.png", record_pos=(0.203, 0.34), resolution=(1260, 2800)))
touch(Template(r"tpl1776329558367.png", target_pos=8, record_pos=(0.007, -0.455), resolution=(1260, 2800)))
if exists(Template(r"tpl1776331533353.png", record_pos=(0.375, -0.345), resolution=(1260, 2800))):
    touch(Template(r"tpl1776330003060.png", record_pos=(0.375, -0.347), resolution=(1260, 2800)))
text("136****5091")
touch(Template(r"tpl1776331246761.png", target_pos=8, record_pos=(0.0, -0.382), resolution=(1260, 2800)))
if exists(Template(r"tpl1776330003060.png", record_pos=(0.375, -0.347), resolution=(1260, 2800))):
    touch(Template(r"tpl1776330003060.png", record_pos=(0.375, -0.347), resolution=(1260, 2800)))
text("qwer1234")
touch(Template(r"tpl1776331742087.png", record_pos=(0.003, 0.04), resolution=(1260, 2800)))
if exists(Template(r"tpl1776332426221.png", record_pos=(0.005, -0.314), resolution=(1260, 2800))):
    print("="*10+"需要验证码登录！"+"="*10)
    touch(Template(r"tpl1776332426221.png", target_pos=8, record_pos=(0.005, -0.314), resolution=(1260, 2800)))
    touch(Template(r"tpl1776333120007.png", record_pos=(0.271, -0.194), resolution=(1260, 2800)))
    sleep(30)
    touch(Template(r"tpl1776333194297.png", record_pos=(-0.004, 0.041), resolution=(1260, 2800)))







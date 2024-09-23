# -*- coding: utf-8 -*-
# @Time    : 2024/9/14 17:10
# @Author  : Jieay
# @File    : home_view.py

import logging

logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


@login_required(login_url='/frd/login')
def index(request):
    return TemplateResponse(request, "home/home.html", {})

# -*- coding: utf-8 -*-
from rest_framework import serializers


class TableSerializer(serializers.ModelSerializer):
    """table api 序列化"""
    class Meta:
        fields = "__all__"

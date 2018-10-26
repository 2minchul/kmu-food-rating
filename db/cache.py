# -*- coding: utf-8 -*-

import redis

EXPIRE = 60 * 60 * 24 * 2  # 2days


def _get_conn():
    return redis.Redis(password='kmurating')


def save(key, value):
    conn = _get_conn()
    conn.set(key, value, EXPIRE)


def load(key):
    conn = _get_conn()
    return conn.get(key)
# from urllib.parse import urljoin


# class NormalizeUrl(object):
#     """url拼接， 使用场景：consul返回服务的域名，将域名和path拼接"""

#     def normalize_url(self, domain, path, scheme='http'):
#         """url拼接"""
#         url = urljoin(domain if domain.__contains__(scheme) else "".join([scheme, '://', domain]), path)
#         return url
# -*- coding: utf-8 -*-

import pprint


class DisplayRawRequest(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pretty_printer = pprint.PrettyPrinter(indent=4)
        pretty_printer.pprint(vars(request))
        response = self.get_response(request)
        return response

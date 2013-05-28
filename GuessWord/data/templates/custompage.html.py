# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1369743679.802085
_template_filename='/var/www/GuessWord/guessword/templates/custompage.html'
_template_uri='/custompage.html'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from markupsafe import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<html>\n<head>\n    <title>Greetings</title>\n    <style type="text/css">\n        p {\n         text-align:center;\n         letter-spacing: 5px;\n         color: green;\n       }\n        h1 {\n         text-align:center;\n         letter-spacing: 5px;\n         color: green;\n       }\n        div {\n         background-color: yellow;\n       }\n    </style>\n    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js" type="text/javascript"></script>\n</head>\n<body>\n\t<div id="clickme">\n\t\t<h2>Press ME</h2>\n\t\t<script>\n\t\t\t$(document).ready(function(){\n\n\t\t\t// Using multiple unit types within one animation.\n\t\t\t\t$("#clickme").click(function(){\n\t\t\t\t\t$("#niceblock").animate({\n\t\t\t\t\t\twidth: "70%",\n\t\t\t\t\t\topacity: 0.4,\n\t\t\t\t\t\tmarginLeft: "0.6in",\n\t\t\t\t\t\tfontSize: "3em",\n\t\t\t\t\t\tborderWidth: "10px"\n\n\t\t\t\t\t}, 1500 );\n\t\t\t\t});\n\n\t\t\t});\n\t\t</script>\n\t\t</div>\n    <div id = "niceblock">\n       <h1>NICE</h1>\n       <p>Hello ')
        # SOURCE LINE 44
        __M_writer(escape(c.teamname))
        __M_writer(u"!</p>\n       <p>Don't be strict? it's just EXAMPLE</p>\n    </div>\n</body>\n</html>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()



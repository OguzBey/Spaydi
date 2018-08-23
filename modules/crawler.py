import re
import logging


class Crawler(object):

    def __init__(self):
        pass

    def get_urls(self, source):
        f = re.findall(r'<a href=[\'"]?([^\'">]+)', source)
        return f

    def get_forms(self, source, url):
        source = source.replace("\n","")
        f = re.findall(r'<form.*?</form>', source)
        forms = []
        for i in range(len(f)):
            attr = dict()
            """
            [
                {
                    url:
                    action:
                    method:
                    inputs:
                        [
                            {
                                name:
                                type:
                                placeholder:
                                value
                            }
                        ]
                    }
                ]
            """
            # input - > name, type, placeholder, value
            form = f[i]
            action = re.findall(r'action=[\'"]?([^\'"]+)', form)
            method = re.findall(r'method=[\'"]?([^\'"]+)', form)
            action = action[0] if action else ""
            method = method[0] if method else ""
            attr.update({'url':url})
            attr.update({'form_action':action})
            attr.update({'form_method':method})
            c_inputs = []
            inputs = re.findall(r'(<input.*?/?>)', form)
            for i in inputs:
                input_attr = dict()
                _name = re.findall(r'name=[\'"]?([^\'"]+)', i)
                _type = re.findall(r'type=[\'"]?([^\'"]+)', i)
                _value = re.findall(r'value=[\'"]?([^\'"]+)', i)
                _placeholder = re.findall(r'placeholder=[\'"]?([^\'"]+)', i)
                input_name = _name[0] if _name else ""
                input_type = _type[0] if _type else ""
                input_value = _value[0] if _value else ""
                input_placeholder = _placeholder[0] if _placeholder else ""
                input_attr.update({'name':input_name})
                input_attr.update({'type':input_type})
                input_attr.update({'value':input_value})
                input_attr.update({'placeholder':input_placeholder})
                c_inputs.append(input_attr)
            attr.update({'inputs':c_inputs})
            forms.append(attr)
        return forms

    def get_uparameters(self, url):
        # http:www.site.com/index.php?id=12&ex=10&ex2=123
        _url = url.split("?")
        _url2 = _url[-1]
        if re.findall("(\w+=\w*)", _url2):
            params_v = re.findall("(\w+=\w*[\/?.*]?[a-zA-Z0-9\.\-]*)", _url2)
            return params_v if len(params_v) != 0 else False
        return False

if __name__ == '__main__':
    pass
    # cr = Crawler()
    # with open("../outputs/links.txt", "r") as fl:
    #   for i in fl:
    #       print(cr.get_uparameters(i))

from lxml import etree
import base64

from ajenti.com import Plugin, implements
from ajenti.ui.api import IXSLTFunctionProvider


def attr(_, v, d):
    return d if v == [] or v == ['None'] else v[0]

def css(_, v, d):
    v = d if v == [] or v == ['None'] else v[0]
    if v == 'auto': 
            return v
    return v if '%' in v else '%spx'%v

def iif(_, q, a, b):
    return a if len(q)>0 and q[0].lower() == 'true' else b
    
def b64(_, s):
    try:
        return base64.b64encode(str(s[0]))
    except:
        return base64.b64encode(str(s))


class Selector(etree.XSLTExtension):
    def execute(self, context, self_node, input_node, output_parent):
        child = input_node[int(self_node.get('index'))]
        results = self.apply_templates(context, child)
        output_parent.append(results[0])
            
                    
class CoreFunctions (Plugin):
    implements(IXSLTFunctionProvider)
    
    def get_funcs(self):
        return {
            'attr' : attr,
            'iif' : iif,
            'b64' : b64,
            'css' : css
        }


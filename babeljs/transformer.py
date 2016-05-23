__author__ = 'yetone'

from babeljs import execjs
from babeljs.source import get_abspath


class TransformError(Exception):
    pass


class Transformer(object):

    def __init__(self):
        path = get_abspath('babeljs/browser.js')
        try:
            self.context = execjs.compile(
                'var babel = require("{}");'.format(path)
            )
        except:
            raise TransformError()

    def transform_string(self, js, out_path=None, **opts):
        try:
            out = self.context.call('babel.transform', js, opts)
        except execjs.ProgramError as e:
            raise TransformError(e.message[7:])
        if out_path:
            with open(out_path, 'w') as f:
                f.write(out)
        return out

    def transform(self, in_path, **opts):
        with open(in_path, 'r') as f:
            return self.transform_string(f.read(), **opts)



def transform(*args, **opts):
    return Transformer().transform(*args, **opts)


def transform_string(*args, **opts):
    return Transformer().transform_string(*args, **opts)

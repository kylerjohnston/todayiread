from flask.ext.assets import Bundle

css_all = Bundle('scss/layout.scss',
                 filters = 'scss',
                 output = 'gen/packed.css')

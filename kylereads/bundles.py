from flask.ext.assets import Bundle

css_all = Bundle('scss/base.scss',
                 'scss/layout.scss',
                 'scss/typography.scss',
                 filters = 'scss',
                 output = 'gen/packed.css')

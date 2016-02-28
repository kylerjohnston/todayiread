from flask.ext.assets import Bundle

css_all = Bundle('scss/base.scss',
                 'scss/layout.scss',
                 'scss/typography.scss',
                 'scss/d3.scss',
                 filters = 'scss,cssutils',
                 output = 'gen/packed.css')

js_sessions = Bundle('js/get_sessions.js',
                     filters='rjsmin',
                     output = 'gen/packed.js')

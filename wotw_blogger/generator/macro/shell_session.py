# pylint: disable=W,C,R

from wotw_blogger.generator.macro import Macro


class ShellSession(Macro):
    macro_name = 'shell_session.j2'
    contents = """\
{% macro shell_session(contents) %}

{{
    highlight_block(
        contents,
        raw = contents,
        linenos = False,
        explicit_lexer_name = 'BashSessionLexer',
        no_header = True
    )
}}

{% endmacro %}
"""

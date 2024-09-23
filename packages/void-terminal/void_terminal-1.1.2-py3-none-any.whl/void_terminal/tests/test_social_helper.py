"""
Test each plugin in the project。Running method：Run python tests/test_plugins.py directly
"""

import init_test
import os, sys


if __name__ == "__main__":
    from test_utils import plugin_test
    plugin_test(
        plugin='crazy_functions.Social_Helper->I assistant', 
        main_input="""
Add contact.：
Eddard Stark.：My adoptive father.，He is the Duke of Winterfell。
Catelyn Stark：My adoptive mother，She was cold towards me.，Because I am a bastard。
Robb Stark：My brother，He is the heir of the North。
Arya Stark：My sister.，She has a close relationship with me.，Strong and independent character。
Sansa Stark：My sister.，She dreams of becoming a lady。
Bran Stark.：My brother，He has the ability to foresee the future.。
Reichen Stark：My brother，He is an innocent child.。
Samuel Tarly：My friend，He fought alongside me in the Night Watch Legion。
Igret.：My lover，She is one of the savages.。
        """)

from pybo import BoPipeline

from .a_preprocessors import *
from .b_tokenizers import *
from .c_processors import *
from .d_formatters import *

pipes = {
            # Preprocessing
            'extract_tib_only': extract_tib_only,
            'extract_all': extract_all,

            # Processing
            'find_mistake_types': find_mistake_types,
            'find_mistake_concs': find_mistake_concs,

            # Formatting
            'vertical_text': verical_text
         }


__all__ = ['BoPipeline', 'pipes']

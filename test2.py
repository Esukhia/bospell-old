from bospell import SpellCheck, CheckFile

pybo_error_types = {'tok': 'pybo',
                    'pybo_profile': 'GMD',
                    'proc': 'pybo_types',
                    'frm': 'types'}

text = '''[བསྟོད་ཚོགས། ཀ 61b.6]{D001_བསྟོད།_ཀ_༠༠༠༧}༄༅།།ཆོས་ཀྱི་སྐུ་ལ་གནས་པའི་ཡོན་ཏན་ཐུན་མོང་མ་ཡིན་པ་ལ་བསྟོད་པ།#༄༅༅།།ཆོས་ཀྱི་སྐུ་ལ་གནས་པའི་ཡོན་ཏན་ཐུན་མོང་མ་ཡིན་པ་ལ་བསྟོད་པ། དེ་བཞིན་གཤེགས་པ་ཐམས་
[61b.7]ཅད་ལ་ཕྱག་འཚལ་ལོ། །སེམས་ཅན་རྣམས་ལ་ཐུགས་བརྩེ་བ། །ཕྲད་དང་བྲལ་བར་དགོངས་པ་ཅན། །མི་འབྲལ་དགོངས་ཤིང་བདེ་བ་ཅན། །དགོངས་པ་ཁྱོད་ལ་ཕྱག་འཚལ་ལོ། །སྒྲིབ་པ་ཀུན་ལས་ངེས་པར་གྲོལ། །ཐུབ་པས་འཇིག་རྟེན་ཀུན་ཟིལ་མནན། །ཁྱོད་ཀྱི་མཁྱེན་པས་ཤེས་བྱ་'''

bs = SpellCheck('pybo_raw_content')
out = bs.check(text)
print(out)

in_file = 'to-check/nalanda/D001_བསྟོད།_ཀ_༠༠༠༧.txt'
cf = CheckFile('pybo_raw_content')
cf.check_file(in_file)

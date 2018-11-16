from bospell import spellcheck_folder

in_dir = 'to-check/corpus-sample'
out_dir = 'checked/'

spellcheck_folder(in_dir, out_dir,
                  tok='sgmt_corpus',
                  matcher='corpus_cor',
                  format='conc',
                  left=10,
                  right=10)

from bospell import spellcheck_folder

in_dir = 'to-check/corpus'
out_dir = 'checked/'

spellcheck_folder(in_dir, out_dir,
                  preproc='corpus',
                  tok='sgmt_corpus',
                  proc='corpus_cor',
                  format='conc',
                  left=10,
                  right=10)

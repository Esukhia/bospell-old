from pathlib import Path
import yaml


default = '''\
basic:
    pre: pre_basic
    tok: spaces
    proc: spaces_fulltext
    frm: plaintext
pybo_raw_content:
    pre: pre_basic
    tok: pybo
    pybo_profile: GMD
    proc: pybo_raw_content
    frm: plaintext
pybo_raw_lines:
    pre: pre_basic_lines
    tok: pybo
    pybo_profile: GMD
    proc: pybo_raw_content
    frm: plaintext
omegat:
    pre: pre_basic_lines
    tok: pybo
    pybo_profile: GMD
    proc: pybo_raw_content
    frm: dash_separated
syls:
    pre: pre_basic
    tok: syls
    proc: spaces_fulltext
    frm: plaintext
pybo_raw_types:
    pre: pre_basic
    tok: pybo
    pybo_profile: GMD
    proc: pybo_raw_types
    frm: types
corpus_seg_adjusted:
    pre: pre_corpus_cleanall
    tok: corpus_correct
    proc: spaces_fulltext
    frm: corpus_adjust
corpus_stats_per_file:
    pre: pre_corpus_cleanall
    tok: corpus_correct
    proc: spaces_fulltext
    frm: types
'''


class Config:
    def __init__(self, filename):
        self.filename = Path(filename).resolve()
        if self.filename.suffix != ".yaml":
            raise Exception("Unrecognised file extension. It only supports .yaml files")

        # if the file doesn't exist, write it with the default values
        if not self.filename.is_file():
            with self.filename.open('w', encoding='utf-8-sig') as f:
                f.write(default)

        with self.filename.open('r', encoding='utf-8-sig') as g:
            self.config = yaml.load(g.read())
            self.is_valid_config()

    def get_profile(self, profile):
        return self.config[profile]

    def is_valid_config(self):
        for profile, values in self.config.items():
            assert isinstance(profile, str)
            for key, value in values.items():
                assert isinstance(key, str)
                assert isinstance(value, str) or isinstance(value, int)

    def reset_default(self):
        """Resets the configuration file to the default values"""
        with self.filename.open('w', encoding='utf-8-sig') as f:
            f.write(default)


if __name__ == '__main__':
    config = Config("bospell.yaml")
    config.reset_default()
    print(config.get_profile('pybo_raw_types'))
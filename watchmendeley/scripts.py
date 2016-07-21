import argparse as _argparse
import re


def fix_higgs_paper(path, output='/Users/joelfrederico/Thesis/overleaf/Dissertation.bib'):
    print('Path: {}'.format(path))
    print('Output: {}'.format(output))

    punctuation = {0x2018: 0x27, 0x2019: 0x27, 0x201C: 0x22, 0x201D: 0x22}

    # ================================
    # Open files for reading, writing
    # ================================
    with open(path, encoding='utf-8') as f_in:
        with open(output, mode='w', encoding='utf-8') as f_out:
            # ================================
            # Regex for replacing title
            # ================================
            prog_title           = re.compile('^title = ')
            prog_url             = re.compile('^url = ')
            sub_paren            = re.compile('(^title = )({{)(.*)(}})(,\n)')
            wrap_parens_list     = {'TeV', 'SDDS', 'Higgs', 'Gaussian', 'Euler-Mascheroni'}
            wrap_parens_compiled = []
            for wrap_parens_target in wrap_parens_list:
                wrap_parens_compiled.append(re.compile(wrap_parens_target))

            url_fix_und   = re.compile(r'{\\_}')
            url_fix_tilde = re.compile(r'{~}')

            math_mode_amp           = re.compile(r'{\\\$}')
            math_mode_backslash     = re.compile(r'\\backslash')
            math_mode_parens_open   = re.compile(r'{\\{}')
            math_mode_parens_closed = re.compile(r'{\\}}')

            # ================================
            # Run through each line.
            # ================================
            for i, line in enumerate(f_in):
                m_title = prog_title.match(line)
                m_url   = prog_url.match(line)

                # ================================
                # Fix title parentheses
                # ================================
                m = sub_paren.match(line)
                if m:
                    line = sub_paren.sub('\g<1>{\g<3>}\g<5>', line)

                if m_title:
                    # ================================
                    # Fix math mode
                    # ================================
                    line = math_mode_amp.sub('$', line)
                    line = math_mode_backslash.sub(r'\\', line)
                    line = math_mode_parens_open.sub(r'{', line)
                    line = math_mode_parens_closed.sub(r'}', line)

                    # ================================
                    # Fix words that should be wrapped
                    # in parentheses
                    # ================================
                    wrap_parens_repl = '{\g<0>}'
                    for wrap_parens in wrap_parens_compiled:
                        line = wrap_parens.sub(wrap_parens_repl, line)

                # ================================
                # Fix url underscores
                # ================================
                if m_url:
                    line = url_fix_und.sub('_', line)
                    line = url_fix_tilde.sub('~', line)

                f_out.writelines(line.translate(punctuation))


def _mendeleysync():
    # ================================
    # Access command line arguments
    # ================================
    parser = _argparse.ArgumentParser(description=
            'Copies Mendeley\'s BibTeX and fixes it.')
    parser.add_argument('-V', action='version', version='%(prog)s v0.1')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Verbose mode.')
    parser.add_argument('-i', '--input',
            help='Path to BibTeX input file.')
    parser.add_argument('-o', '--output',
            help='Path to BibTeX input file.')

    arg = parser.parse_args()

    # ================================
    # Run with command line arguments
    # ================================
    fix_higgs_paper(arg.input, arg.output)

if __name__ == '__main__':
    # ================================
    # Access command line arguments
    # ================================
    parser = _argparse.ArgumentParser(description=
            'Copies Mendeley\'s BibTeX and fixes it.')
    parser.add_argument('-V', action='version', version='%(prog)s v0.1')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Verbose mode.')
    parser.add_argument('-p', '--path',
            help='Path to BibTeX file.')

    arg = parser.parse_args()

    # ================================
    # Run with command line arguments
    # ================================
    fix_higgs_paper(arg.path)

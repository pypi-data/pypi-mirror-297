# Copyright 2024 Mario Graff (https://github.com/mgraffg)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
from encexp.utils import compute_b4msa_vocabulary, compute_seqtm_vocabulary
from encexp.text_repr import SeqTM
import encexp
import numpy as np
import gzip


def main(args):
    """CLI"""

    filename  = args.file[0]
    lang = args.lang
    limit = args.limit
    if limit < 0:
        limit = None
    voc_size_exponent = args.voc_size_exponent
    data = compute_b4msa_vocabulary(filename, limit=limit, lang=lang)
    voc = compute_seqtm_vocabulary(SeqTM, data, filename, limit=limit,
                                   voc_size_exponent=voc_size_exponent)
    seqtm = SeqTM(lang=lang, voc_size_exponent=voc_size_exponent,
                  vocabulary=voc)
    output_filename = args.output
    if output_filename is None:
        output_filename = seqtm.identifier + '.json.gz'
    with gzip.open(output_filename, 'wb') as fpt:
        fpt.write(bytes(json.dumps(voc), encoding='utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute SeqTM Vocabulary',
                                     prog='EncExp.build_voc')
    parser.add_argument('-v', '--version', action='version',
                        version=f'EncExp {encexp.__version__}')
    parser.add_argument('-o', '--output',
                        help='Output filename',
                        dest='output', default=None, type=str)
    parser.add_argument('--lang', help='Language (ar | ca | de | en | es | fr | hi | in | it | ko | nl | pl | pt | ru | tl | tr )',
                        type=str, default='es')
    parser.add_argument('--limit', help='Maximum size of the dataset',
                        dest='limit',
                        type=int, default=-1)
    parser.add_argument('--voc_size_exponent',
                        help='Vocabulary size express as log2',
                        dest='voc_size_exponent',
                        type=int, default=-1) 
    parser.add_argument('file',
                        help='Input filename',
                        nargs=1, type=str)
    args = parser.parse_args()
    main(args)
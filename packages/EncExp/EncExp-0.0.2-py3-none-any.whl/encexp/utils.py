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
from itertools import count
from urllib import request
from urllib.error import HTTPError
try:
    USE_TQDM = True
    from tqdm import tqdm
except ImportError:
    USE_TQDM = False
from microtc.utils import tweet_iterator, Counter
from b4msa import TextModel
import numpy as np
import os


DialectID_URL = 'https://github.com/INGEOTEC/dialectid/releases/download/data'
EncExp_URL = 'https://github.com/INGEOTEC/EncExp/releases/download/data'
MODELS = os.path.join(os.path.dirname(__file__),
                      'models')

class Download(object):
    """Download
    
    >>> from EncExp.utils import Download
    >>> d = Download("http://github.com", "t.html")
    """

    def __init__(self, url, output='t.tmp') -> None:
        self._url = url
        self._output = output
        self._use_tqdm = USE_TQDM
        try:
            request.urlretrieve(url, output, reporthook=self.progress)
        except HTTPError as exc:
            self._use_tqdm = False
            self.close()
            raise RuntimeError(f'URL=> {url}') from exc
        self.close()

    @property
    def tqdm(self):
        """tqdm"""

        if not self._use_tqdm:
            return None
        try:
            return self._tqdm
        except AttributeError:
            self._tqdm = tqdm(total=self._nblocks,
                              leave=False, desc=self._output)
        return self._tqdm

    def close(self):
        """Close tqdm if used"""
        if self._use_tqdm:
            self.tqdm.close()

    def update(self):
        """Update tqdm if used"""
        if self._use_tqdm:
            self.tqdm.update()

    def progress(self, nblocks, block_size, total):
        """tqdm progress"""

        self._nblocks = total // block_size
        self.update()


def b4msa_params(lang='es'):
    """B4MSA default parameters"""

    from microtc.params import OPTION_DELETE, OPTION_NONE
    tm_kwargs=dict(num_option=OPTION_NONE,
                   usr_option=OPTION_DELETE,
                   url_option=OPTION_DELETE,
                   emo_option=OPTION_NONE,
                   hashtag_option=OPTION_NONE,
                   ent_option=OPTION_NONE,
                   lc=True,
                   del_dup=False,
                   del_punc=True,
                   del_diac=True,
                   select_ent=False,
                   select_suff=False,
                   select_conn=False,
                   max_dimension=False,
                   unit_vector=True,
                   q_grams_words=True)
    if lang == 'ja' or lang == 'zh':
        tm_kwargs['token_list'] = [1, 2, 3]
    else:
        tm_kwargs['token_list'] = [-1, 2, 3, 4, 5, 6]
    return tm_kwargs


def progress_bar(data, total=np.inf, **kwargs):
    """Progress bar"""

    if not USE_TQDM:
        return data
    if total == np.inf:
        total = None
    return tqdm(data, total=total, **kwargs)


def compute_b4msa_vocabulary(filename, limit=None, lang='es',
                             **kwargs):
    """Compute the vocabulary"""

    params = b4msa_params(lang=lang)
    params.update(kwargs)
    tokenize = TextModel(**params).tokenize
    if limit is None:
        limit = np.inf
    counter = Counter()
    if limit == np.inf:
        loop = count()
    else:
        loop = range(limit)
    for tweet, _ in progress_bar(zip(tweet_iterator(filename),
                                        loop), total=limit,
                                        desc=filename):
        counter.update(set(tokenize(tweet)))
    _ = dict(update_calls=counter.update_calls,
             dict=dict(counter.most_common()))
    data = dict(counter=_, params=params)
    return data


def compute_seqtm_vocabulary(instance, vocabulary,
                             filename, limit=None,
                             voc_size_exponent=13):
    """Compute SeqTM"""
    def current_lost_words():
        words = [w for w, _ in base_voc.most_common() if w[:2] != 'q:']
        current = words[:2**voc_size_exponent]
        lost =  words[2**voc_size_exponent:]
        return current, lost

    def optimize_vocabulary():
        cnt = Counter({k: v for k, v in base_voc.items() if k[:2] == 'q:'},
                      update_calls=base_voc.update_calls)
        _ = dict(params=vocabulary['params'], counter=cnt)
        tokenize = instance(vocabulary=_).tokenize        
        current, lost = current_lost_words()
        for _ in progress_bar(range(32)):
            cnt = Counter()
            for word in lost:
                tokens = set(tokenize(word))
                _ = {token: base_voc[word] for token in tokens}
                cnt.update(_)
            for word in current:
                cnt[word] = base_voc[word]
            mask = set(current)
            u_lost = [k for k, _ in cnt.most_common()[2**voc_size_exponent:]
                      if k in mask]
            lost = lost + u_lost
            current = [w for w, _ in cnt.most_common()[:2**voc_size_exponent]
                       if w[:2] != 'q:']
            if len(u_lost) == 0:
                break
        return cnt.most_common()[:2**voc_size_exponent]

    limit = np.inf if limit is None else limit
    loop = count() if limit == np.inf else range(limit)
    base_voc = Counter(vocabulary['counter']["dict"],
                       vocabulary['counter']["update_calls"])
    voc = optimize_vocabulary()
    cnt = Counter(dict(voc),
                  update_calls=base_voc.update_calls)
    _ = dict(params=vocabulary['params'], counter=cnt)
    tokenize = instance(vocabulary=_).tokenize
    counter = Counter()
    for tweet, _ in progress_bar(zip(tweet_iterator(filename),
                                        loop), total=limit,
                                        desc=filename):
        counter.update(set(tokenize(tweet)))
    _ = dict(update_calls=counter.update_calls,
             dict=dict(counter.most_common()[:2**voc_size_exponent]))
    data = dict(counter=_, params=vocabulary['params'])
    return data


def uniform_sample(N, avail_data):
    """Uniform sample from the available data"""
    remaining = avail_data.copy()
    M = 0
    while M < N:
        index = np.where(remaining > 0)[0]
        if index.shape[0] == 0:
            break
        sample = np.random.randint(index.shape[0], size=N - M)
        sample_i, sample_cnt = np.unique(index[sample], return_counts=True)
        remaining[sample_i] = remaining[sample_i] - sample_cnt
        remaining[remaining < 0] = 0
        M = (avail_data - remaining).sum()
    return avail_data - remaining
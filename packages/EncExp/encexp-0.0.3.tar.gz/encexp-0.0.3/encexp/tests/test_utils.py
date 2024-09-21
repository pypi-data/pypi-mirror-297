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
from os.path import isfile
import os
from microtc.utils import Counter
from encexp.utils import Download, DialectID_URL
from encexp.utils import compute_b4msa_vocabulary


def test_download():
    """Test Download"""

    from os.path import isfile

    Download("http://github.com", "t.html")
    assert isfile("t.html")
    os.unlink("t.html")
    try:
        Download("adasdf", "t1.html")
    except ValueError:
        return
    assert False


def test_download_use_tqdm():
    """Test to disable tqdm"""

    from encexp import utils 

    utils.USE_TQDM = False
    utils.Download("http://github.com", "t.html")
    os.unlink("t.html")


def samples():
    """Download MX sample"""

    from zipfile import ZipFile

    filename = 'es-mx-sample.json.zip'
    if isfile(filename):
        return
    Download(f'{DialectID_URL}/es-mx-sample.json.zip',
             filename)
    with ZipFile(filename, "r") as fpt:
        fpt.extractall(path=".",
                       pwd="ingeotec".encode("utf-8"))


def test_compute_b4msa_vocabulary():
    """Compute vocabulary"""

    samples()
    data = compute_b4msa_vocabulary('es-mx-sample.json')
    _ = data['counter']
    counter = Counter(_["dict"], _["update_calls"])
    assert counter.most_common()[0] == ('q:e~', 1847)
    data = compute_b4msa_vocabulary('es-mx-sample.json', 10)
    _ = data['counter']
    counter = Counter(_["dict"], _["update_calls"])
    assert counter.update_calls == 10


def test_uniform_sample():
    """Test uniform sample"""

    from encexp.utils import uniform_sample
    import numpy as np

    data = uniform_sample(10, np.array([20, 5, 4, 7]))
    assert data.sum() == 10

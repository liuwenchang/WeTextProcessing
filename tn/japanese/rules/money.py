# Copyright (c) 2024 Logan Liu (2319277867@qq.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tn.japanese.rules.cardinal import Cardinal
from tn.processor import Processor
from tn.utils import get_abs_path

from pynini import string_file
from pynini.lib.pynutil import delete, insert


class Money(Processor):

    def __init__(self):
        super().__init__(name='money')
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        code = string_file(get_abs_path('japanese/data/money/code.tsv'))
        symbol = string_file(get_abs_path('japanese/data/money/symbol.tsv'))

        number = Cardinal().number
        tagger = (insert('currency: "') + (code | symbol) + delete(' ').ques +
                  insert('" ') + insert('value: "') + number + insert('"'))
        self.tagger = self.add_tokens(tagger)

    def build_verbalizer(self):
        value = delete('value: "') + self.SIGMA + delete('" ')
        currency = delete('currency: "') + self.SIGMA + delete('"')
        verbalizer = value + currency
        self.verbalizer = self.delete_tokens(verbalizer)

# Copyright (c) 2022 Xingchen Song (sxc19@tsinghua.org.cn)
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

from tn.processor import Processor
from tn.utils import get_abs_path

from pynini import string_file, accep
from pynini.lib.pynutil import delete, insert


class Date(Processor):

    def __init__(self):
        super().__init__(name='date')
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        digit = string_file(
            get_abs_path('../itn/chinese/data/number/digit.tsv'))  # 1 ~ 9
        zero = string_file(
            get_abs_path('../itn/chinese/data/number/zero.tsv'))  # 0

        yyyy = digit + (digit | zero)**3  # 二零零八年
        yyy = digit + (digit | zero)**2  # 公元一六八年
        yy = (digit | zero)**2  # 零八年奥运会
        mm = string_file(get_abs_path('../itn/chinese/data/date/mm.tsv'))
        dd = string_file(get_abs_path('../itn/chinese/data/date/dd.tsv'))

        year = insert('year: "') + (yyyy | yyy | yy) + \
            delete('年') + insert('" ')
        year_only = insert('year: "') + (yyyy | yyy | yy) + \
            accep('年') + insert('"')
        month = insert('month: "') + mm + insert('"')
        month_only = insert('month: "') + mm + insert('"')
        day = insert(' day: "') + dd + insert('"')
        day_only = insert('day: "') + dd + insert('"')
        # yyyy/mm/dd | yyyy/mm | mm/dd | yyyy
        date = ((year + month + day)
                | (year + month)
                | (month + day)) | year_only | month_only | day_only
        self.tagger = self.add_tokens(date)

    def build_verbalizer(self):
        #addsign = insert("/")
        yearsign = insert("年")
        monthsign = insert("月")
        daysign = insert("日")
        year = delete('year: "') + self.SIGMA + delete('" ')
        year_only = delete('year: "') + self.SIGMA + delete('"')
        month = delete('month: "') + self.SIGMA + delete('"')
        month_only = delete('month: "') + self.SIGMA + delete('"') + monthsign
        day = delete(' day: "') + self.SIGMA + delete('"')
        day_only = delete('day: "') + self.SIGMA + delete('"') + daysign
        verbalizer = (year + yearsign).ques + (month + monthsign).ques + (day + daysign).ques
        verbalizer |= year_only
        verbalizer |= day_only
        verbalizer |= month_only
        self.verbalizer = self.delete_tokens(verbalizer)

# credit jcrist
# https://github.com/jcrist/msgspec/blob/main/benchmarks/generate_data.py

"""
Copyright (c) 2021, Jim Crist-Harif
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
  may be used to endorse or promote products derived from this software
  without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import datetime
import random
import string


class Generator:
    UTC = datetime.timezone.utc
    DATE_2018 = datetime.datetime(2018, 1, 1, tzinfo=UTC)
    DATE_2023 = datetime.datetime(2023, 1, 1, tzinfo=UTC)
    PERMISSIONS = ["READ", "WRITE", "READ_WRITE"]
    NAMES = [
        "alice",
        "ben",
        "carol",
        "daniel",
        "esther",
        "franklin",
        "genevieve",
        "harold",
        "ilana",
        "jerome",
        "katelyn",
        "leonard",
        "monique",
        "nathan",
        "ora",
        "patrick",
        "quinn",
        "ronald",
        "stephanie",
        "thomas",
        "uma",
        "vince",
        "wendy",
        "xavier",
        "yitzchak",
        "zahra",
    ]

    def __init__(self, capacity, seed=42):
        self.capacity = capacity
        self.random = random.Random(seed)

    def randdt(self, min, max):
        ts = self.random.randint(int(min.timestamp()), int(max.timestamp()))
        return datetime.datetime.fromtimestamp(ts).replace(tzinfo=self.UTC)

    def randstr(self, min=None, max=None):
        if max is not None:
            min = self.random.randint(min, max)
        return "".join(self.random.choices(string.ascii_letters, k=min))

    def make(self, is_dir):
        name = self.randstr(4, 30)
        created_by = self.random.choice(self.NAMES)
        created_at = self.randdt(self.DATE_2018, self.DATE_2023)
        data = {
            "type": "directory" if is_dir else "file",
            "name": name,
            "created_by": created_by,
            "created_at": created_at.isoformat(),
        }
        if self.random.random() > 0.75:
            updated_by = self.random.choice(self.NAMES)
            updated_at = self.randdt(created_at, self.DATE_2023)
            data.update(
                updated_by=updated_by,
                updated_at=updated_at.isoformat(),
            )
        if is_dir:
            n = min(self.random.randint(0, 30), self.capacity)
            self.capacity -= n
            data["contents"] = [self.make_node() for _ in range(n)]
        else:
            data["nbytes"] = self.random.randint(0, 1000000)
            data["permissions"] = self.random.choice(self.PERMISSIONS)
        return data

    def make_node(self):
        return self.make(self.random.random() > 0.8)

    def generate(self):
        self.capacity -= 1
        if self.capacity == 0:
            out = self.make(False)
        else:
            out = self.make(True)
            while self.capacity:
                self.capacity -= 1
                out["contents"].append(self.make_node())
        return out


def make_filesystem_data(n):
    return Generator(n).generate()

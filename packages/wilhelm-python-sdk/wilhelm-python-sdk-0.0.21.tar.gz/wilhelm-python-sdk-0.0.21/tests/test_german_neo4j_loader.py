# Copyright Jiaqi (Hutao of Emberfire)
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
import unittest

import yaml

from wilhelm_python_sdk.german_neo4j_loader import get_attributes


class TestGermanNeo4JLoader(unittest.TestCase):

    def test_get_definitions(self):
        self.assertEqual(
            {
                "name": "der Hut",
                "language": "German",
                "declension": {
                    0: {0: "",           1: "singular", 2: "singular", 3: "singular",    4: "plural", 5: "plural"},
                    1: {0: "",           1: "indef.",   2: "def.",     3: "noun",        4: "def.",   5: "noun"},
                    2: {0: "nominative", 1: "ein",      2: "der",      3: "Hut",         4: "die",    5: "Hüte"},
                    3: {0: "genitive",   1: "eines",    2: "des",      3: "Hutes, Huts", 4: "der",    5: "Hüte"},
                    4: {0: "dative",     1: "einem",    2: "dem",      3: "Hut",         4: "den",    5: "Hüten"},
                    5: {0: "accusative", 1: "einen",    2: "den",      3: "Hut",         4: "die",    5: "Hüte"}
                }
            },
            get_attributes(
                yaml.safe_load(
                    """
                    term: der Hut
                    definition: the hat
                    declension:
                      - ["",         singular, singular, singular,      plural, plural]
                      - ["",         indef.,   def.,     noun,          def.,   noun  ]
                      - [nominative, ein,      der,      Hut,           die,    Hüte  ]
                      - [genitive,   eines,    des,      "Hutes, Huts", der,    Hüte  ]
                      - [dative,     einem,    dem,      Hut,           den,    Hüten ]
                      - [accusative, einen,    den,      Hut,           die,    Hüte  ]
                    """
                )
            ),
        )

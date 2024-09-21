# Copyright 2024 mbodi ai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import importlib

# Import embdata and make it available as mbodied.data
embdata = importlib.import_module('embdata')
sys.modules['mbodied.data'] = embdata

# Make all embdata attributes available in mbodied namespace
from embdata import *

# Get all non-private attributes from embdata
embdata_attrs = [attr for attr in dir(embdata) if not attr.startswith('_')]

__all__ = ['data'] + embdata_attrs



"""
NeuralMag - A nodal finite-difference code for inverse micromagnetics

Copyright (c) 2024 NeuralMag team

This program is free software: you can redistribute it and/or modify
it under the terms of the Lesser Python General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Lesser Python General Public License for more details.

You should have received a copy of the Lesser Python General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from neuralmag.common import engine
from neuralmag.common.code_class import *
from neuralmag.common.config import config
from neuralmag.common.function import *
from neuralmag.common.logging import *
from neuralmag.common.mesh import *
from neuralmag.common.state import *

__all__ = (
    ["config", "engine"]
    + logging.__all__
    + function.__all__
    + mesh.__all__
    + state.__all__
)

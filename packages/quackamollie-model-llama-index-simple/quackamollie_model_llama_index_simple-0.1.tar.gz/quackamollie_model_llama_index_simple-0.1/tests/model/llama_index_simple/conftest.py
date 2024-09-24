# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import pytest

from typing import Optional


@pytest.fixture(scope='session')
def ollama_url(request) -> Optional[str]:
    return None


@pytest.fixture(scope='session')
def ollama_base_model(request) -> Optional[str]:
    return None

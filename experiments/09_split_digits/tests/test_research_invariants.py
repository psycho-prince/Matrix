"""Regression tests for the Split Digits helpers and native GAL inheritance.

Run from repository root:
    python -m unittest discover -s experiments/09_split_digits/tests -v
"""
from __future__ import annotations

import unittest

import torch
from torch import nn

from experiments import _unused  # noqa: F401

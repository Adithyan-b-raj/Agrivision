"""
Application Views Package (Tabs and Pages)
"""

from src.views.tab_diagnosis import render_tab_diagnosis
from src.views.tab_voice import render_tab_voice
from src.views.tab_benchmark import render_tab_benchmark
from src.views.tab_report import render_tab_report

__all__ = [
    "render_tab_diagnosis",
    "render_tab_voice",
    "render_tab_benchmark",
    "render_tab_report"
]

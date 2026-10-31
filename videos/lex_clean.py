# -*- coding: utf-8 -*-
"""Lexicon additions for the cleaning-course videos (C01..C07): pandas names that appear in subtitles. Kept
specific (whole identifiers, longest first in lexicon.py), so other courses' subtitles are not touched by accident.
Anything with arguments (dropna(axis=1), keep='last', mode()[0] …) carries its own say=."""

WORDS = {
    "DataFrame": "דָאטָה פְרֵיים",
    "pandas": "פַּנְדָס",
    "NaN": "נָאן",
    "isnull().sum()": "אִיז נָאל סָאם",
    "isnull()": "אִיז נָאל",
    "dropna()": "דְרוֹפּ אֶן אֵיי",
    "dropna": "דְרוֹפּ אֶן אֵיי",
    "fillna": "פִיל אֶן אֵיי",
    "ffill()": "אֶף פִיל",
    "drop_duplicates()": "דְרוֹפּ דּוּפְּלִיקֵייטְס",
    "drop_duplicates": "דְרוֹפּ דּוּפְּלִיקֵייטְס",
    "duplicated()": "דּוּפְּלִיקֵייטֵד",
    "get_dummies": "גֶט דָאמִיז",
    "True": "טְרוּ",
    "False": "פוֹלְס",
    "One-Hot": "וָואן הוֹט",
    "MCAR": "אֶם סִי אֵיי אָר",
    "MNAR": "אֶם אֶן אֵיי אָר",
}

HOMOPHONES = {}

TEX_TOKENS = {}

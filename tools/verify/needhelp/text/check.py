"""Machine check for the regex / text course (T01..T08). Run from the repo root:  python tools/verify/needhelp/text/check.py

Every option that is Python (a list, a string, a re call, a pattern) is evaluated or run for real."""
import os
import re
import sys

from sklearn.feature_extraction.text import CountVectorizer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import Checker  # noqa: E402

c = Checker("text")


def ev(o):
    try:
        return eval(o, {"re": re})
    except Exception:
        return object()   # not valid python -> never equals anything


def is_value(qid, expected):
    c.pred(qid, lambda o: ev(o) == expected)


# ---- T01 -------------------------------------------------------------------------------------------
assert re.search("mary", "Mary has a little lamb") is None
c.contains("T01-Q1", "None, כי הביטוי רגיש")
is_value("T01-Q2", re.findall(r"[A-Z]", "Dana and Dan"))
is_value("T01-Q3", re.findall(r"\d\d", "a1b22c333"))
is_value("T01-Q4", re.findall(r"\b\w", "hi big world"))
c.exact("T01-Q5", re.search(r".a", "banana").group())

# ---- T02 -------------------------------------------------------------------------------------------
is_value("T02-Q1", re.findall(r"ab+", "ab abb a abbb"))
is_value("T02-Q2", re.findall(r"\d{2,3}", "1 22 333 4444"))
c.pred("T02-Q3", lambda o: all(re.fullmatch(o, s) for s in ("color", "colour")) and not re.fullmatch(o, "colouur"))
is_value("T02-Q4", re.findall(r"\b[A-Z][a-z]*\b", "Dan met Eli in NYC"))
is_value("T02-Q5", re.findall(r"\w+@\w+\.com", "a@b.com, x_y@site.com, bad@site.org"))

# ---- T03 -------------------------------------------------------------------------------------------
c.pred("T03-Q1", lambda o: bool(ev(o)))
is_value("T03-Q2", re.findall(r"cat|dog", "cat dogs bird"))
is_value("T03-Q3", re.findall(r"(\d+)-(\d+)", "10-20 and 3-4"))
c.exact("T03-Q4", re.search(r"(\w+)@(\w+)", "mail dan@site now").group(2))
EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
assert EMAIL in c.qs["T03-Q5"]["question"].replace("`", "")
c.pred("T03-Q5", lambda o: bool(re.match(EMAIL, o)))

# ---- T04 -------------------------------------------------------------------------------------------
m_, s_ = re.match("b", "abc"), re.search("b", "abc")
assert m_ is None and s_ is not None
c.exact("T04-Q1", "match מחזירה None, ו-search מחזירה התאמה")
is_value("T04-Q2", re.split(r"[,;] ?", "a, b;c,d"))
c.exact("T04-Q3", re.sub(r"\d+", "#", "a1b22c333"))
c.num("T04-Q4", len(re.findall(r"o", "foo boo")))
c.exact("T04-Q5", re.search(r"\d+", "a12b345").group())

# ---- T05 -------------------------------------------------------------------------------------------
c.exact("T05-Q1", re.search(r"<.+>", "<a><b>").group())
c.exact("T05-Q2", re.search(r"<.+?>", "<a><b>").group())
assert re.search(r"a.*b", "xaabbby").group() == "aabbb"
c.exact("T05-Q3", re.search(r"a.*?b", "xaabbby").group())
c.exact("T05-Q4", re.search(r"(\w+) (\w+)", "A new day").group(2))
assert len(re.search(r"a.*a", "a1a2a").group()) == 5
c.num("T05-Q5", len(re.search(r"a.*?a", "a1a2a").group()))

# ---- T06: each option is a real pattern, run with findall ---------------------------------------------
def finds(text, expected):
    return lambda o: re.findall(o, text) == expected


c.pred("T06-Q1", finds("call 03-6610304 or 02 3434884 ok", ["03-6610304", "02 3434884"]))
c.pred("T06-Q2", finds("The price is $15.99 or €20.50", ["$15.99", "€20.50"]))
c.pred("T06-Q3", finds("AB-1234 xy-12 CD-99999 EF-5678", ["AB-1234", "EF-5678"]))
c.pred("T06-Q4", finds("on 05/03/2024 and 5/3/24", ["05/03/2024"]))
c.pred("T06-Q5", finds("love #python and #data_science!", ["#python", "#data_science"]))

# ---- T07: real CountVectorizer --------------------------------------------------------------------------
docs = ["the cat sat", "the cat the dog"]
cv = CountVectorizer()
X = cv.fit_transform(docs).toarray()
assert list(cv.get_feature_names_out()) == ["cat", "dog", "sat", "the"]
is_value("T07-Q1", X[1].tolist())
docs2 = ["red fox", "blue fox", "red sky"]
assert str(CountVectorizer().fit_transform(docs2).shape) == "(3, 4)"
is_value("T07-Q2", CountVectorizer().fit_transform(docs2).shape)
cvs = CountVectorizer(stop_words="english").fit(docs)
c.num("T07-Q3", len(cvs.vocabulary_))
c.num("T07-Q4", X[1][list(cv.get_feature_names_out()).index("the")])
v = CountVectorizer().fit_transform(["dog bites man", "man bites dog"]).toarray()
assert (v[0] == v[1]).all()
c.contains("T07-Q5", "הם זהים, כי הגישה מתעלמת מסדר המילים")

# ---- T08 boss: bank questions, re-run -----------------------------------------------------------------
c.exact("T08:P-61", re.search(r"[A-Z]\w\w", " Dina and Dan came for a visit").group(0))
is_value("T08:P-62", re.findall(r"[A-Z]\w\w", "Dina and Dan came for a visit"))
is_value("T08:P-65", re.split(r"\W+", "Hello, hello, hello."))
words = ["Dan", "NYC", "eLi", "hello", "Hello"]
assert [w for w in words if re.fullmatch(r"\b[A-Z][a-z]*\b", w)] == ["Dan", "Hello"]
c.contains("T08:24A-B-Q4", "למצוא כל המילים שמתחילות באות גדולה וממשיכות באותיות קטנות")
assert re.match("b", "abc") is None and re.search("b", "abc")
c.contains("T08:26A-B-Q4", "re.match מחפשת התאמה רק מתחילת המחרוזת")
assert re.findall(r"\b[Aa]\w+", "Apple ant banana a Aardvark") == ["Apple", "ant", "Aardvark"]
c.contains("T08:25-S-Q4", "מלים שמתחילות באות A גדולה או קטנה")

c.finish()

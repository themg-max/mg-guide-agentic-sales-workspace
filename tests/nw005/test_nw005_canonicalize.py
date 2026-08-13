from __future__ import annotations

import json
import unicodedata

import pytest

from mg_guide.firestore_audit.canonicalize import (
    CANONICALIZER_ID,
    CanonicalizationError,
    fingerprint_hex,
    nw005_canonical_json_v1,
)


def test_canonicalizer_id():
    assert CANONICALIZER_ID == "nw005_canonical_json_v1"


def test_golden_bytes_object_key_sort_and_no_whitespace():
    # Keys must sort by Unicode code point after NFC.
    value = {"b": 2, "a": 1, "nested": {"z": 0, "m": [3, 1]}}
    raw = nw005_canonical_json_v1(value)
    assert raw == b'{"a":1,"b":2,"nested":{"m":[3,1],"z":0}}'


def test_golden_bytes_string_nfc():
    # U+0065 + U+0301 (e + combining acute) normalizes to U+00E9
    decomposed = "cafe" + "\u0301"
    composed = unicodedata.normalize("NFC", decomposed)
    assert decomposed != composed
    raw = nw005_canonical_json_v1({"s": decomposed})
    assert raw == nw005_canonical_json_v1({"s": composed})
    assert raw == ('{"s":"%s"}' % composed).encode("utf-8")


def test_golden_bytes_booleans_null_and_arrays():
    raw = nw005_canonical_json_v1([True, False, None, "x"])
    assert raw == b'[true,false,null,"x"]'


def test_integers_only_no_float_fraction():
    assert nw005_canonical_json_v1({"n": 0}) == b'{"n":0}'
    assert nw005_canonical_json_v1({"n": 42}) == b'{"n":42}'
    # Integer-valued float coerces to int
    assert nw005_canonical_json_v1({"n": 2.0}) == b'{"n":2}'
    with pytest.raises(CanonicalizationError):
        nw005_canonical_json_v1({"n": 1.5})


def test_control_char_escaping():
    raw = nw005_canonical_json_v1({"s": "a\nb"})
    assert raw == b'{"s":"a\\nb"}'


def test_fingerprint_stable():
    import hashlib

    a = fingerprint_hex({"run_id": "r1", "n": 1})
    b = fingerprint_hex({"n": 1, "run_id": "r1"})
    assert a == b
    assert len(a) == 64
    expected = hashlib.sha256(b'{"n":1,"run_id":"r1"}').hexdigest()
    assert a == expected


def test_no_rfc8785_claim_in_module_doc():
    import mg_guide.firestore_audit.canonicalize as mod

    doc = (mod.__doc__ or "") + (nw005_canonical_json_v1.__doc__ or "")
    assert "not RFC 8785" in doc or "not** RFC 8785" in doc or "NOT" in doc.upper()
    assert "RFC 8785" in doc

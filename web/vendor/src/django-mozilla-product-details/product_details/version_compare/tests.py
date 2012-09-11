"""
Most of these tests are directly migrated from mozilla-central's reference
implementation.
"""
import copy

from nose.tools import eq_

from product_details.version_compare import (
    Version, version_list, version_dict, version_int)


# Versions to test listed in ascending order, none can be equal.
# TODO Add support for asterisks.
COMPARISONS = (
    "0.9",
    "0.9.1",
    "1.0pre1",
    "1.0pre2",
    "1.0",
    "1.1pre",
    "1.1pre1a",
    "1.1pre1",
    "1.1pre10a",
    "1.1pre10",
    "1.1",
    "1.1.0.1",
    "1.1.1",
    #"1.1.*",
    #"1.*",
    "2.0",
    "2.1",
    "3.0.-1",
    "3.0",
)

# Every version in this list means the same version number.
# TODO add support for + signs.
EQUALITY = (
  "1.1pre",
  "1.1pre0",
  #"1.0+",
)


def test_version_compare():
    """Test version comparison code, for parity with mozilla-central."""
    numlist = enumerate(map(lambda v: Version(v), COMPARISONS))
    for i, v1 in numlist:
        for j, v2 in numlist:
            if i < j:
                assert v1 < v2, '%s is not less than %s' % (v1, v2)
            elif i > j:
                assert v1 > v2, '%s is not greater than %s' % (v1, v2)
            else:
                eq_(v1, v2)

    equal_vers = map(lambda v: Version(v), EQUALITY)
    for v1 in equal_vers:
        for v2 in equal_vers:
            eq_(v1, v2)


def test_simplify_version():
    """Make sure version simplification works."""
    versions = {
        '4.0b1': '4.0b1',
        '3.6': '3.6',
        '3.6.4b1': '3.6.4b1',
        '3.6.4build1': '3.6.4',
        '3.6.4build17': '3.6.4',
    }
    for v in versions:
        ver = Version(v)
        eq_(ver.simplified, versions[v])


def test_dict_vs_int():
    """
    version_dict and _int can use each other's data but must not overwrite
    it.
    """
    version_string = '4.0b8pre'
    dict1 = copy.copy(version_dict(version_string))
    int1 = version_int(version_string)
    dict2 = version_dict(version_string)
    int2 = version_int(version_string)
    eq_(dict1, dict2)
    eq_(int1, int2)


def test_version_list():
    """Test if version lists are generated properly."""
    my_versions = {
        '4.0b2build8': '2010-12-06',
        '3.0': '2010-12-01',
        '4.0b1': '2010-11-24',
        '4.0b2build7': '2010-12-05',
    }
    expected = ('4.0b2', '4.0b1')

    test_list = version_list(my_versions, hide_below='4.0b1')

    # Check if the generated version list is the same as we expect.
    eq_(len(expected), len(test_list))
    for n, v in enumerate(test_list):
        eq_(v, expected[n])

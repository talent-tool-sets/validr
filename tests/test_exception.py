from validr import Invalid, mark_index, mark_key

from .helper import expect_position


def test_exception_message():
    assert Invalid('invalid').message == 'invalid'
    assert Invalid().message is None


def test_exception_position():
    e = Invalid('invalid').mark_key('key')
    assert e.position == 'key'

    e = Invalid('invalid').mark_index(0)
    assert e.position == '[0]'

    e = Invalid('invalid').mark_index()
    assert e.position == '[]'

    e = Invalid('invalid').mark_key('key').mark_index(0).mark_index()
    assert e.position == '[][0].key'

    e = Invalid('invalid').mark_index().mark_index(0).mark_key('key')
    assert e.position == 'key[0][]'


def test_exception_str():
    ex = Invalid('invalid').mark_index(0).mark_key('key')
    assert str(ex) == 'invalid in key[0]'

    ex = Invalid().mark_index(0).mark_key('key')
    assert str(ex) == 'in key[0]'

    ex = Invalid('invalid')
    assert str(ex) == 'invalid'

    ex = Invalid()
    assert str(ex) == ''


@expect_position('[0]')
def test_mark_index():
    with mark_index(0):
        raise Invalid('invalid')


@expect_position('[]')
def test_mark_index_uncertainty():
    with mark_index():
        raise Invalid('invalid')


@expect_position('key')
def test_mark_key():
    with mark_key('key'):
        raise Invalid('invalid')


@expect_position('[][0].key')
def test_mark_index_key():
    with mark_index():
        with mark_index(0):
            with mark_key('key'):
                raise Invalid('invalid')


@expect_position('key[0][]')
def test_mark_key_index():
    with mark_key('key'):
        with mark_index(0):
            with mark_index():
                raise Invalid('invalid')

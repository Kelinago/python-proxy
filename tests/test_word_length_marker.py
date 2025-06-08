from handlers.word_length_marker import DEFAULT_MARKER_LIST, WordLengthMarkerHandler


def test_default_marking():
    handler = WordLengthMarkerHandler()
    text = 'Welcome friends to the testing ground'
    expected = f'Welcome{DEFAULT_MARKER_LIST[0]} friends{DEFAULT_MARKER_LIST[1]} to the testing{DEFAULT_MARKER_LIST[0]} ground'

    actual = handler.handle(text)

    assert actual == expected

def test_custom_word_length_and_markers():
    handler = WordLengthMarkerHandler(word_length=4, markers=['😀', '😎'])
    text = 'This test will mark only four words'
    expected = 'This😀 test😎 will😀 mark😎 only😀 four😎 words'

    actual = handler.handle(text)

    assert actual == expected

def test_no_matching_words():
    handler = WordLengthMarkerHandler(word_length=10)
    text = 'short tiny text'

    actual = handler.handle(text)

    assert actual == text

def test_punctuation_handling():
    handler = WordLengthMarkerHandler(word_length=5)
    text = 'abcde! 12345? ABCDE.'
    expected = f'abcde{DEFAULT_MARKER_LIST[0]}! 12345{DEFAULT_MARKER_LIST[1]}? ABCDE{DEFAULT_MARKER_LIST[0]}.'
    
    actual = handler.handle(text)

    assert actual == expected

def test_marker_cycles_through_markers():
    handler = WordLengthMarkerHandler(word_length=3, markers=['🙂', '🙃'])
    text = 'one two six ten'
    expected = 'one🙂 two🙃 six🙂 ten🙃'

    actual = handler.handle(text)

    assert actual == expected

def test_empty_text():
    handler = WordLengthMarkerHandler()
    
    actual = handler.handle('')

    assert actual == ''

def test_non_ascii_words():
    handler = WordLengthMarkerHandler(word_length=5)
    text = 'привет мир hello'
    expected = f'привет мир hello{DEFAULT_MARKER_LIST[0]}'

    actual = handler.handle(text)

    assert actual == expected

def test_custom_markers():
    custom_markers = ['FIRST', 'SECOND']
    handler = WordLengthMarkerHandler(word_length=6, markers=custom_markers)
    text = 'abcdef ghi jklmno pqrstu'
    expected = f'abcdef{custom_markers[0]} ghi jklmno{custom_markers[1]} pqrstu{custom_markers[0]}'

    actual = handler.handle(text)

    assert actual == expected
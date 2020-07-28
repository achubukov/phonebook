from phonebook.data_operations.api.api import API


def test_send_request():
    api = API()
    assert set(api.send_request('not_number').keys()) == {'code', 'type', 'info'}
    assert not api.send_request('3num45be6r')['valid']

    api = API()
    dict = api.send_request('9111319831')
    assert 'valid' in dict
    assert 'number' in dict
    assert 'country_name' in dict
    assert dict['valid'] is True

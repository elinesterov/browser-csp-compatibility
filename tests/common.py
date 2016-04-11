from utils.config import config


def generate_test_url(policy="default-src 'none'", meta=False,
                      header=False, allow=False, fixture_url='', params=False):
    """
    Generates test URL

    policy: CSP policy. default CSP policy is 'default-src 'none'
    meta: CSP policy in meta element. default value is False
    header: CSP policy in CSP header. default is True
    allow: Do changes allowed by  CSP policy? Need for client side javascript
           to generate test result
    fixture_url: Test fixture base URL. Specific for each tests category
    """
    q_str = ''
    if allow is True:
        q_str += 'allow=True&'
    if meta is True:
        q_str += 'meta=True&'
    if header is True:
        q_str += 'header=True&'
    if params:
        q_str += '{}&'.format(params)
    q_str += 'policy={}'.format(policy)

    url = 'http://{}:{}/{}?{}'.format(config['server_address'],
                                      config['server_port'],
                                      fixture_url,
                                      q_str)
    print(url)
    return url

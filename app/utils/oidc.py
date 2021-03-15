from oidc_provider import settings as oidc_settings
from oidc_provider.lib.claims import StandardScopeClaims


def get_scopes_information(scope_o):
    """
    Return a list with the description of all the scopes requested.
    """
    scopes = StandardScopeClaims.get_scopes_info(scope_o)
    if oidc_settings.get('OIDC_EXTRA_SCOPE_CLAIMS'):
        scopes_extra = oidc_settings.get(
            'OIDC_EXTRA_SCOPE_CLAIMS', import_str=True).get_scopes_info(scope_o)
        for index_extra, scope_extra in enumerate(scopes_extra):
            for index, scope in enumerate(scopes[:]):
                if scope_extra['scope'] == scope['scope']:
                    del scopes[index]
    else:
        scopes_extra = []

    return scopes + scopes_extra

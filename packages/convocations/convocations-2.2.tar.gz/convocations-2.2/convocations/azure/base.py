from raft.tasks import Task
from raft.context import Context


def print_username(creds):
    """
    prints the username from the jwt we get from the credentials
    """
    from ..base.utils import notice, notice_end
    import jwt
    notice('logged in as')
    token = creds.get_token('https://management.azure.com/.default')
    data = jwt.decode(token.token.encode('utf8'), options={ 'verify_signature': False })
    # dump_yaml(data, quiet=False)
    notice_end(f"{data['unique_name']}")


class AzureTask(Task):
    def __call__(self, *args, **kwargs):
        from azure.identity import ClientSecretCredential
        from azure.identity import DefaultAzureCredential
        from azure.identity import TokenCachePersistenceOptions
        from ..base.utils import get_context_value
        from ..base.utils import notice, notice_end
        ctx = args[0]
        has_context = isinstance(ctx, Context)
        client_id = kwargs.get('client_id')
        client_secret = kwargs.get('client_secret')
        home_tenant_id = kwargs.get('home_tenant_id')
        tenant_id = kwargs.get('tenant_id')
        allowed_tenants = kwargs.get('allowed_tenants')
        if allowed_tenants:
            allowed_tenants = allowed_tenants.split(',')
        creds = kwargs.get('creds')
        quiet = kwargs.get('quiet') or False
        cache_name = kwargs.get('cache_name') or None
        verbose = not quiet
        redirect_uri = kwargs.get('redirect_uri', 'http://localhost:8050')
        if has_context:
            client_id = client_id or get_context_value(ctx, 'azure.client_id')
            client_secret = client_secret or get_context_value(ctx, 'azure.client_secret')
            tenant_id = tenant_id or get_context_value(ctx, 'azure.tenant_id')
            home_tenant_id = home_tenant_id or get_context_value(ctx, 'azure.home_tenant_id')
            redirect_uri = redirect_uri or get_context_value(ctx, 'azure.redirect_uri')
            allowed_tenants = allowed_tenants or get_context_value(ctx, 'azure.additionally_allowed_tenants')
            cache_name = cache_name or get_context_value(ctx, 'azure.cache_name')
        cache_name = cache_name or 'convocations'
        if verbose:
            notice('client_id')
            notice_end(client_id)
            notice('tenant_id')
            notice_end(tenant_id)
            notice('cache name')
            notice_end(cache_name)
        if not creds and client_id and client_secret and tenant_id:
            creds = ClientSecretCredential(tenant_id, client_id, client_secret)
        elif not creds:
            if verbose:
                notice('using interactive credential')
            options = TokenCachePersistenceOptions(name=cache_name)
            cred_kwargs = {}
            if tenant_id:
                cred_kwargs['shared_cache_tenant_id'] = tenant_id
                cred_kwargs['interactive_browser_tenant_id'] = tenant_id
            if client_id:
                cred_kwargs['interactive_browser_client_id'] = client_id
            if allowed_tenants:
                cred_kwargs['additionally_allowed_tenants'] = allowed_tenants
            creds = DefaultAzureCredential(
                exclude_interactive_browser_credential=False,
                cache_persistence_options=options,
                redirect_uri=redirect_uri,
                **cred_kwargs
            )
            if verbose:
                notice_end()
        if verbose:
            print_username(creds)
        kwargs['creds'] = creds
        return super().__call__(*args, **kwargs)

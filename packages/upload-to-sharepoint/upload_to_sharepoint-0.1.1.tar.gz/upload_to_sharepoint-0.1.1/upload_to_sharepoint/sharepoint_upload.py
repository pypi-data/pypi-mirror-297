import os
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

def upload_file_to_sharepoint(username, password, sharepoint_site, target_folder_relative_url_base, file_name):    

    ctx_auth = AuthenticationContext(url=sharepoint_site)
    ctx_auth.acquire_token_for_user(username, password)
    ctx = ClientContext(sharepoint_site, ctx_auth)

    upload_file_path = f"{file_name}"
    with open(upload_file_path, 'rb') as content_file:
        file_content = content_file.read()
    target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_relative_url_base)
    name = os.path.basename(upload_file_path)
    target_folder.upload_file(name, file_content).execute_query()
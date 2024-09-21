import requests

def get_assets_by_layout_id(api_baseurl, api_key, asset_layout_id):
    page = 1
    headers = {'x-api-key': api_key}
    all_assets = []
    page_size = 100  # Adjust as needed

    while True:
        url = f'{api_baseurl}/assets?asset_layout_id={asset_layout_id}&page={page}&page_size={page_size}'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            
            assets = data.get('assets', [])
            if not assets:  # If no assets are returned, break the loop
                break
            
            all_assets.extend(assets)

            # If fewer assets are returned than per_page, it's the last page
            if len(assets) < page_size:
                break
            
            page += 1
        
        except requests.exceptions.RequestException as e:
            return {"assets": []}, f"Error fetching assets: {e}"
    
    return all_assets, None

def create_asset(api_baseurl, api_key, company_id, layout_id, asset_name, custom_fields):
    """Create an asset in Hudu

    Args:
        api_key (str): Your Hudu API key
        company_id (str): The
        layout_id (str): The asset layout ID
        asset_name (str): The name of the asset
        custom_fields (dict): A dictionary of custom fields to set on the asset
        
    Returns:
        dict: The created asset
    """

    url = f"{api_baseurl}/companies/{company_id}/assets"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "asset": {
            "name": asset_name,
            "asset_layout_id": layout_id,
            "primary_serial": "",
            "primary_mail": "",
            "primary_model": "",
            "primary_manufacturer": "",
            "custom_fields": custom_fields
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {}, f"Error creating asset: {e}"
    
def update_asset(api_baseurl, api_key, company_id, asset_id, custom_fields):
    """Update an asset in Hudu

    Args:
        api_baseurl (str): The base URL for the Hudu API
        api_key (str): Your Hudu API key
        company_id (str): The ID of the company to update the asset for
        asset_id (str): The ID of the asset to update
        custom_fields (dict): A dictionary of custom fields to update on the asset

    Returns:
        dict: The updated asset
    """
    url = f"{api_baseurl}/companies/{company_id}/assets/{asset_id}"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "asset": {
            "custom_fields": custom_fields
        }
    }
    try:
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {}, f"Error updating asset: {e}"
  

def check_is_existing_asset(api_baseurl, api_key, company_id, layout_id, asset_name):
    """Check if an asset already exists in Hudu, return id if it does

    Args:
        api_baseurl (str): The base URL for the Hudu API
        api_key (str): Your Hudu API key
        company_id (str): The ID of the company to check
        layout_id (str): The asset layout ID
        asset_name (str): The name of the asset

    Returns:
        str: The ID of the asset if it exists, None if it does not, or False if there was an error
        
    """
    url = f"{api_baseurl}/assets"
    headers = {
        "x-api-key": api_key
    }
    params = {
        "company_id": company_id,
        "asset_layout_id": layout_id,
        "name": asset_name
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        assets = data.get("assets", [])
        if assets:
            return assets[0]["id"]
        return None
    except requests.exceptions.RequestException as e:
        return False

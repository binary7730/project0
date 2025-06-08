import requests
import json
import sys

class UserInfoError(Exception):
    """Custom exception for errors in get_user_info."""
    pass

def get_user_info(mallid: str) -> dict:
    """
    Retrieves user information from the specified mall ID.

    Args:
        mallid: The ID of the mall user.

    Returns:
        A dictionary containing the user information from the JSON response.

    Raises:
        UserInfoError: If there's an issue fetching or parsing user info.
    """
    url = f"https://infra-apigw.hanpda.com/ptool_userinfo/user_info.php?display_type=json&user_id={mallid}"
    try:
        response = requests.get(url, timeout=10)  # Added timeout
        if response.status_code != 200:
            raise UserInfoError(f"API request failed with status code {response.status_code}: {response.text}")

        return response.json()
    except requests.exceptions.Timeout:
        raise UserInfoError(f"API request timed out for mallid: {mallid}")
    except requests.exceptions.RequestException as e:
        raise UserInfoError(f"API request failed for mallid {mallid}: {e}")
    except json.JSONDecodeError as e:
        raise UserInfoError(f"Failed to decode JSON response for mallid {mallid}: {e}. Response text: {response.text[:200]}...")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Fetch and display user info for a given mall ID.")
    parser.add_argument("mallid", type=str, help="The mall ID of the user.")
    args = parser.parse_args()

    try:
        user_info = get_user_info(args.mallid)
        print(json.dumps(user_info, indent=4, ensure_ascii=False))
    except UserInfoError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

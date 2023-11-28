from rich.prompt import Prompt


def input_security_token() -> str:
    # input a security token
    security_token = str(
        Prompt.ask(
            f"Insert your security token. You can ask for one at [link=https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication_and_authorisation]this link[/link]",
        )
    ).lower()

    # write security token to .env file
    with open(".env", "w") as f:
        f.write(f"SECURITY_TOKEN={security_token}")

    return security_token

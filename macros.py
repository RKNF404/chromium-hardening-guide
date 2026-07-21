def define_env(env) -> None:
    """This file is used to define reusable macros for the website which run at build time. It is not part of the config generator."""
    attrs: str = "{title='Homepage'}"
    policyattrs: str = "{title='Policy Documentation'}"
    @env.macro
    def b(name: str, homepage: str, policies: str) -> str:
        """
        Create browser header with necessary info. Call this method from a markdown file like so:

        {{ b("name", "homepage link", "policy link") }}

        Args:
            name (str): Browser name.
            homepage (str): Browser homepage. Set to "" to disable.
            policies (str): Browser policies page. Set to "" to disable. Set to "chrome" or "firefox" for their respective policy pages.
        """
        if policies == "chrome":
            policies = "https://chromeenterprise.google/policies"
        elif policies == "firefox":
            policies = "https://firefox-admin-docs.mozilla.org/reference/policies"
        if policies == "":
            if homepage == "":
                return name
            else:
                return f"[{name}]({homepage}){attrs}"
        else:
            if homepage == "":
                    return f"{name} [:lucide-scroll-text:]({policies}){policyattrs}"
            else:
                    return f"[{name}]({homepage}) [:lucide-scroll-text:]({policies}){policyattrs}"

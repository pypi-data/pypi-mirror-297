from typing import Any, Dict, List, Optional

from browserforge.fingerprints import Fingerprint, Screen
from playwright.sync_api import Browser, Playwright, PlaywrightContextManager

from .addons import DefaultAddons
from .utils import ListOrString, get_launch_options


class Camoufox(PlaywrightContextManager):
    """
    Wrapper around playwright.sync_api.PlaywrightContextManager that automatically
    launches a browser and closes it when the context manager is exited.
    """

    def __init__(self, **launch_options):
        super().__init__()
        self.launch_options = launch_options
        self.browser: Optional[Browser] = None

    def __enter__(self) -> Browser:
        super().__enter__()
        self.browser = NewBrowser(self._playwright, **self.launch_options)
        return self.browser

    def __exit__(self, *args: Any):
        if self.browser:
            self.browser.close()
        super().__exit__(*args)


def NewBrowser(
    playwright: Playwright,
    *,
    config: Optional[Dict[str, Any]] = None,
    addons: Optional[List[str]] = None,
    fingerprint: Optional[Fingerprint] = None,
    exclude_addons: Optional[List[DefaultAddons]] = None,
    screen: Optional[Screen] = None,
    os: Optional[ListOrString] = None,
    user_agent: Optional[ListOrString] = None,
    fonts: Optional[List[str]] = None,
    args: Optional[List[str]] = None,
    executable_path: Optional[str] = None,
    **launch_options: Dict[str, Any]
) -> Browser:
    """
    Launches a new browser instance for Camoufox.

    Parameters:
        playwright (Playwright):
            The playwright instance to use.
        config (Optional[Dict[str, Any]]):
            The configuration to use.
        addons (Optional[List[str]]):
            The addons to use.
        fingerprint (Optional[Fingerprint]):
            The fingerprint to use.
        exclude_addons (Optional[List[DefaultAddons]]):
            The default addons to exclude, passed as a list of camoufox.DefaultAddons enums.
        screen (Optional[browserforge.fingerprints.Screen]):
            The screen constraints to use.
        os (Optional[ListOrString]):
            The operating system to use for the fingerprint. Either a string or a list of strings.
        user_agent (Optional[ListOrString]):
            The user agent to use for the fingerprint. Either a string or a list of strings.
        fonts (Optional[List[str]]):
            The fonts to load into Camoufox, in addition to the default fonts.
        args (Optional[List[str]]):
            The arguments to pass to the browser.
        executable_path (Optional[str]):
            The path to the Camoufox browser executable.
        **launch_options (Dict[str, Any]):
            Additional Firefox launch options.
    """
    opt = get_launch_options(
        config=config,
        addons=addons,
        fingerprint=fingerprint,
        exclude_addons=exclude_addons,
        screen=screen,
        os=os,
        user_agent=user_agent,
        fonts=fonts,
        args=args,
        executable_path=executable_path,
    )
    return playwright.firefox.launch(**opt, **launch_options)

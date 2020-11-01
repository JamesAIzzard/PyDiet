from typing import Callable, Optional

from pyconsoleapp import Component, styles, builtin_components

_template_with_title = '''{header}
{page_title}
{page_title_underline}
{page_content}
>>> '''
_template_without_title = '''{header}
{page_content}
>>> '''


class StandardPageComponent(Component):
    """Standard page, including header bar and input arrows >>>. Content is passed into print_view()"""

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._page_title: Optional[str] = None
        self._header_component = self.use_component(builtin_components.HeaderComponent)

    def printer(self, page_content: str, **kwds) -> str:
        """Returns the standard page component view as a string, with the page content inserted."""
        # Populate the correct template and return;
        if self._page_title:
            return _template_with_title.format(
                header=self._header_component.printer(),
                page_title=styles.weight(self._page_title, 'bright'),
                page_title_underline=len(self._page_title) * '\u2500',
                page_content=page_content)
        elif not self._page_title:
            return _template_without_title.format(
                header=self._header_component.printer(),
                page_content=page_content)

    def configure(self, page_title: Optional[str] = None,
                  go_back: Optional[Callable[[], None]] = None, **kwds) -> None:
        """Configures the StandardPageComponent instance."""
        if page_title is not None:
            self._page_title = page_title
        if go_back is not None:
            self._header_component.configure(go_back=go_back)
        super().configure(**kwds)

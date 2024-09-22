import curses
from contextlib import suppress
from typing import Any, List, Optional, Set, Tuple

from .base import BaseMenu
from .utils import KeyboardAction


class MultiMenu(BaseMenu):
    """
    menu with multiple selection
    """

    def __init__(
        self,
        title: str = "",
    ) -> None:
        super().__init__(title)
        self.__max_count = None
        self.__selected: Set[int] = set()
        self._control_config[KeyboardAction.SELECT] = self.__select

    def max_count(self, max_count: int):
        """
        set the max count of options could be selected
        """
        self.__max_count = max_count
        return self

    def __select(self) -> None:
        with suppress(KeyError):
            self.__selected.remove(self._index)
            return
        if self.__max_count is None or len(self.__selected) < self.__max_count:
            self.__selected.add(self._index)

    def _get_selected_index(self) -> Set[int]:  # type: ignore
        return self.__selected

    def _draw_options(self, max_x: int) -> None:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        for local_y, line in enumerate(self._options):
            if local_y == self._index:
                line = f"{self._prefix}{line}{self._suffix}"
            else:
                line = f'{" " * len(self._prefix)}{line}'

            if local_y in self.__selected:
                self.stdscr.addnstr(self._y, 0, line, max_x, curses.color_pair(1))
            else:
                self.stdscr.addnstr(self._y, 0, line, max_x)
            self._y += 1

    def run_get_item(self) -> List[str]:  # type: ignore
        return list(map(self._options.__getitem__, self.__selected))

    def run(self) -> Set[int]:  # type: ignore
        """
        Return a set of indexes of selected options
        """
        return super().run()  # type: ignore


class ItemMenu(BaseMenu):
    """
    A menu with user given items related to each menu items.
    """

    def __init__(
        self,
        title: str = "",
    ) -> None:
        self.__items: List[Optional[Any]] = []
        super().__init__(title)

    def add_option(self, option: str, callback: Optional[Any] = None):
        self.__items.append(callback)
        super().add_option(option)
        return self

    # we need to rewrite the method
    def add_options(  # type: ignore
        self, options: List[Optional[Tuple[str, Any]]]
    ):
        names, items = zip(*options)
        self.__items.extend(items)
        super().add_options(names)
        return self

    def run_get_item(self) -> Any:  # type: ignore
        assert len(self.__items) == len(self._options), "Invalid number of items"
        return self.__items[super().run()]  # type: ignore

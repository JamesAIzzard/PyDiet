import abc
from typing import Dict, List, Type, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, PrimaryArg, StandardPageComponent, menu_tools, ResponseValidationError
from pydiet import persistence, completion

if TYPE_CHECKING:
    from pydiet.persistence import SupportsPersistence

_main_view_template = '''
Edit {item_u_name}   | -edit [{item_l_name} number]
Delete {item_u_name} | -del  [{item_l_name} number]

{item_u_name}:
{item_menu}
'''


class BaseViewerComponent(ConsoleAppComponent, abc.ABC):

    def __init__(self, app, item_type: Type['SupportsPersistence'], item_editor_route: str):
        super().__init__(app)
        self._item_editor_route: str = item_editor_route
        self._item_type: Type['SupportsPersistence'] = item_type
        self._unique_val_num_map: Dict[int, str] = {}

        self.configure_state('main', self._print_main_view, responders=[
            self.configure_responder(self._on_edit_item, args=[
                PrimaryArg('item_num', has_value=True, markers=['-edit'], validators=[
                    self._validate_item_number])]),
            self.configure_responder(self._on_delete_item, args=[
                PrimaryArg('item_num', has_value=True, markers=['-del'], validators=[
                    self._validate_item_number])])
        ])

    @property
    @abc.abstractmethod
    def _get_saved_unique_vals(self) -> List[str]:
        raise NotImplementedError

    @property
    def _item_menu(self) -> str:
        menu = ''
        for num in self._unique_val_num_map:
            unique_val = self._unique_val_from_num(num)
            item = self._load_item(unique_val=unique_val)
            if isinstance(item, completion.SupportsCompletion):
                item_status = item.completion_status_summary
            else:
                item_status = ''
            menu = menu + '{name_and_num:<40} {subject_status}\n'.format(
                name_and_num=str(num) + '. ' + unique_val + ':', subject_status=item_status)
        return menu

    def _unique_val_from_num(self, num: int) -> str:
        return self._unique_val_num_map[num]

    def _load_item(self, unique_val:str) -> #todo Figure out how to express this return type as the type in self._item_type:

    def _validate_item_number(self, value) -> int:
        try:
            num = int(value)
        except ValueError:
            raise ResponseValidationError('Please enter a valid item number.')
        if num not in self._unique_val_num_map:
            raise ResponseValidationError('Please enter a valid item number.')
        return num

    def _on_load(self) -> None:
        unique_vals = self._get_saved_unique_vals
        unique_vals.sort()
        self._unique_val_num_map = menu_tools.create_number_name_map(unique_vals)

    def _print_main_view(self) -> str:
        return self.app.get_component(StandardPageComponent).print(
            page_title='{self._item_u_name} Viewer',
            page_content=_main_view_template.format(
                ingredient_menu=self._item_menu
            )
        )

    def _on_edit_item(self, args) -> None:
        item_name = self._item_name_from_num(args['item_num'])
        item = persistence.persistence_service.load(self._item_type, item_name)
        item_editor = self.app.get_component_for_route(self._item_editor_route)
        item_editor.configure(subject=item)
        self.app.goto(self._item_editor_route)

    def _on_delete_item(self, args) -> None:
        item_name = self._item_name_from_num(args['item_num'])
        persistence.persistence_service.delete(self._item_type, item_name)
        self.app.info_message = '{} was deleted.'.format(item_name)

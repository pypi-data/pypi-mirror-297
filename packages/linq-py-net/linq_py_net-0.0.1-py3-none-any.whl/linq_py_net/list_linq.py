from typing import TypeVar, Callable

T = TypeVar('T')
U = TypeVar('T')

class List(list):
    def where(self, func: Callable[[T], bool]) -> 'List[T]': 
        return List([item for item in self if func(item)])
    
    def select(self, func: Callable[[T], U]) -> 'List[U]':
        return List([func(item) for item in self])
    
    def count(self, func: Callable[[T], bool] | None = None) -> int:
        return len([item for item in self if (func(item) if func else True)])
    
    def first_or_default(self, func: Callable[[T], bool] | None = None) -> T | None:
        return next((item for item in self if (func(item) if func else True)), None)
    
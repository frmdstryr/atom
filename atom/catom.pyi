# --------------------------------------------------------------------------------------
# Copyright (c) 2021, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# --------------------------------------------------------------------------------------
from enum import IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    overload,
)

from atom.atom import Atom

def reset_property(*args, **kwargs) -> Any: ...

class CAtom:
    def __init__(self, **kwargs) -> None: ...
    def freeze(self) -> None: ...
    def get_member(self, member: str) -> Member: ...
    def has_observer(
        self, member: str, func: Callable[[Dict[str, Any]], None]
    ) -> bool: ...
    def has_observers(self, member: str) -> bool: ...
    def notifications_enabled(self) -> bool: ...
    def notify(self, member_name: str, *args, **kwargs) -> None: ...
    def observe(self, member: str, func: Callable[[Dict[str, Any]], None]) -> None: ...
    def set_notifications_enabled(self, enabled: bool) -> bool: ...
    def unobserve(
        self, member: str, func: Callable[[Dict[str, Any]], None]
    ) -> None: ...
    def __sizeof__(self) -> int: ...

M = TypeVar("M", bound=Member)
T = TypeVar("T")
S = TypeVar("S")

class Member(Generic[T, S]):
    default_value_mode: DefaultValue = ...
    delattr_mode: DelAttr = ...
    getattr_mode: GetAttr = ...
    index: int = ...
    metadata: Optional[Dict[str, Any]] = ...
    name: str = ...
    post_getattr_mode: PostGetAttr = ...
    post_setattr_mode: PostSetAttr = ...
    post_validate_mode: PostValidate = ...
    setattr_mode: SetAttr = ...
    validate_mode: Validate = ...
    def __init__(self) -> None: ...
    @overload
    def __get__(self: M, instance: None, owner: Type[Atom]) -> M: ...
    @overload
    def __get__(self: M, instance: Atom, owner: Type[Atom]) -> T: ...
    def __set__(self, instance: Atom, value: S) -> None: ...
    def __delete__(self, instance: Atom) -> None: ...
    def tag(self: M, **kwargs) -> M: ...
    def clone(self: M) -> M: ...
    def add_static_observer(self, observer: str | Callable[..., None]) -> Any: ...
    def remove_static_observer(self, observer: str | Callable[..., None]) -> Any: ...
    def static_observers(self) -> Tuple[str | Callable[..., None], ...]: ...
    def has_observer(self, observer: str | Callable[..., None]) -> Any: ...
    def has_observers(self) -> bool: ...
    def copy_static_observers(self, other: Member) -> None: ...
    def notify(self, owner: CAtom, *args, **kwargs) -> None: ...
    def get_slot(self, owner: CAtom) -> Any: ...
    def set_slot(self, owner: CAtom, value: Any) -> None: ...
    def del_slot(self, owner: CAtom) -> None: ...
    # Manual operation of the member
    def do_default_value(self, owner: CAtom) -> Any: ...
    def do_delattr(self, owner: CAtom) -> None: ...
    def do_full_validate(self, owner: CAtom, old: T, new: Any) -> T: ...
    def do_getattr(self, owner: CAtom) -> Any: ...
    def do_post_getattr(self, owner: CAtom, value: Any) -> T: ...
    def do_post_setattr(self, owner: CAtom, old: T, new: T) -> None: ...
    def do_post_validate(self, owner: CAtom, old, T, new: T) -> T: ...
    def do_setattr(self, owner: CAtom, value: Any) -> Any: ...
    def do_validate(self, owner: CAtom, old: T, new: Any) -> T: ...
    # Setter for the member
    def set_index(self, index: int) -> None: ...
    def set_name(self, name: str) -> None: ...
    # Default value mode
    @overload
    def set_default_value_mode(
        self, mode: Literal[DefaultValue.List], context: list
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self, mode: Literal[DefaultValue.Set], context: set
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self, mode: Literal[DefaultValue.Dict], context: dict
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self, mode: Literal[DefaultValue.Delegate], context: Member
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self, mode: Literal[DefaultValue.CallObject], context: Callable[[], Any]
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self,
        mode: Literal[DefaultValue.CallObject_Object],
        context: Callable[[CAtom], Any],
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self,
        mode: Literal[DefaultValue.CallObject_ObjectName],
        context: Callable[[CAtom, str], Any],
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self,
        mode: Literal[DefaultValue.ObjectMethod]
        | Literal[DefaultValue.ObjectMethod_Name]
        | Literal[DefaultValue.MemberMethod_Object],
        context: str,
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self, mode: Literal[DefaultValue.Static], context: Any
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self, mode: Literal[DefaultValue.NonOptional], context: None
    ) -> None: ...
    @overload
    def set_default_value_mode(
        self, mode: Literal[DefaultValue.NoOp], context: None
    ) -> None: ...
    # Delattr mode
    @overload
    def set_delattr_mode(
        self, mode: Literal[DelAttr.Delegate], context: Member
    ) -> None: ...
    @overload
    def set_delattr_mode(
        self,
        mode: Literal[DelAttr.Property],
        context: Optional[Callable[[CAtom], None]],
    ) -> None: ...
    @overload
    def set_delattr_mode(
        self,
        mode: Literal[DelAttr.Constant]
        | Literal[DelAttr.Event]
        | Literal[DelAttr.NoOp]
        | Literal[DelAttr.ReadOnly]
        | Literal[DelAttr.Signal]
        | Literal[DelAttr.Slot],
        context: None,
    ) -> None: ...
    # Getattr mode
    @overload
    def set_getattr_mode(
        self, mode: Literal[GetAttr.Delegate], context: Member
    ) -> None: ...
    @overload
    def set_getattr_mode(
        self,
        mode: Literal[GetAttr.Property] | Literal[GetAttr.CachedProperty],
        context: Optional[Callable[[CAtom], Any]],
    ) -> None: ...
    @overload
    def set_getattr_mode(
        self, mode: Literal[GetAttr.CallObject_Object], context: Callable[[CAtom], Any]
    ) -> None: ...
    @overload
    def set_getattr_mode(
        self,
        mode: Literal[GetAttr.CallObject_ObjectName],
        context: Callable[[CAtom, str], Any],
    ) -> None: ...
    @overload
    def set_getattr_mode(
        self,
        mode: Literal[GetAttr.ObjectMethod]
        | Literal[GetAttr.ObjectMethod_Name]
        | Literal[GetAttr.MemberMethod_Object],
        context: str,
    ) -> None: ...
    @overload
    def set_getattr_mode(
        self,
        mode: Literal[GetAttr.Event]
        | Literal[GetAttr.NoOp]
        | Literal[GetAttr.Signal]
        | Literal[GetAttr.Slot],
        context: str,
    ) -> None: ...
    # Post getattr mode
    @overload
    def set_post_getattr_mode(
        self, mode: Literal[PostGetAttr.NoOp], context: None
    ) -> None: ...
    @overload
    def set_post_getattr_mode(
        self, mode: Literal[PostGetAttr.Delegate], context: Member
    ) -> None: ...
    @overload
    def set_post_getattr_mode(
        self,
        mode: Literal[PostGetAttr.ObjectMethod_Value]
        | Literal[PostGetAttr.ObjectMethod_NameValue]
        | Literal[PostGetAttr.MemberMethod_ObjectValue],
        context: Member,
    ) -> None: ...
    # Post setattr mode
    @overload
    def set_post_setattr_mode(
        self, mode: Literal[PostSetAttr.NoOp], context: None
    ) -> None: ...
    @overload
    def set_post_setattr_mode(
        self, mode: Literal[PostSetAttr.Delegate], context: Member
    ) -> None: ...
    @overload
    def set_post_setattr_mode(
        self,
        mode: Literal[PostSetAttr.ObjectMethod_OldNew]
        | Literal[PostSetAttr.ObjectMethod_NameOldNew]
        | Literal[PostSetAttr.MemberMethod_ObjectOldNew],
        context: str,
    ) -> None: ...
    # Post validate mode
    @overload
    def set_post_validate_mode(
        self, mode: Literal[PostValidate.NoOp], context: None
    ) -> None: ...
    @overload
    def set_post_validate_mode(
        self, mode: Literal[PostValidate.Delegate], context: Member
    ) -> None: ...
    @overload
    def set_post_validate_mode(
        self,
        mode: Literal[PostValidate.ObjectMethod_OldNew]
        | Literal[PostValidate.ObjectMethod_NameOldNew]
        | Literal[PostValidate.MemberMethod_ObjectOldNew],
        context: str,
    ) -> None: ...
    # Setattr mode
    @overload
    def set_setattr_mode(
        self,
        mode: Literal[SetAttr.Constant]
        | Literal[SetAttr.Event]
        | Literal[SetAttr.NoOp]
        | Literal[SetAttr.ReadOnly]
        | Literal[SetAttr.Signal]
        | Literal[SetAttr.Slot],
        context: None,
    ) -> None: ...
    @overload
    def set_setattr_mode(
        self, mode: Literal[SetAttr.Delegate], context: Member
    ) -> None: ...
    @overload
    def set_setattr_mode(
        self,
        mode: Literal[SetAttr.Property],
        context: Optional[Callable[[CAtom], Any]],
    ) -> None: ...
    @overload
    def set_setattr_mode(
        self,
        mode: Literal[SetAttr.CallObject_ObjectValue],
        context: Callable[[CAtom, Any], Any],
    ) -> None: ...
    @overload
    def set_setattr_mode(
        self,
        mode: Literal[SetAttr.CallObject_ObjectNameValue],
        context: Callable[[CAtom, str, Any], Any],
    ) -> None: ...
    @overload
    def set_setattr_mode(
        self,
        mode: Literal[SetAttr.ObjectMethod_Value]
        | Literal[SetAttr.ObjectMethod_NameValue]
        | Literal[SetAttr.MemberMethod_ObjectValue],
        context: str,
    ) -> None: ...
    # Validate mode
    @overload
    def set_validate_mode(
        self,
        mode: Literal[Validate.Bool]
        | Literal[Validate.Bytes]
        | Literal[Validate.BytesPromote]
        | Literal[Validate.Callable]
        | Literal[Validate.Float]
        | Literal[Validate.FloatPromote]
        | Literal[Validate.Int]
        | Literal[Validate.IntPromote]
        | Literal[Validate.NoOp]
        | Literal[Validate.Str]
        | Literal[Validate.StrPromote],
        context: None,
    ) -> None: ...
    @overload
    def set_validate_mode(
        self,
        mode: Literal[Validate.Tuple]
        | Literal[Validate.List]
        | Literal[Validate.ContainerList]
        | Literal[Validate.Set],
        context: Optional[Member],
    ) -> None: ...
    @overload
    def set_validate_mode(
        self,
        mode: Literal[Validate.Dict],
        context: Tuple[Optional[Member], Optional[Member]],
    ) -> None: ...
    @overload
    def set_validate_mode(
        self,
        mode: Literal[Validate.Instance] | Literal[Validate.Subclass],
        context: type | Tuple[type, ...],
    ) -> None: ...
    @overload
    def set_validate_mode(
        self, mode: Literal[Validate.Typed], context: type
    ) -> None: ...
    @overload
    def set_validate_mode(
        self, mode: Literal[Validate.Enum], context: Sequence
    ) -> None: ...
    @overload
    def set_validate_mode(
        self,
        mode: Literal[Validate.FloatRange],
        context: Tuple[Optional[float], Optional[float]],
    ) -> None: ...
    @overload
    def set_validate_mode(
        self,
        mode: Literal[Validate.Range],
        context: Tuple[Optional[int], Optional[int]],
    ) -> None: ...
    @overload
    def set_validate_mode(
        self,
        mode: Literal[Validate.Coerced],
        context: Tuple[Type[T], Callable[[Any], T]],
    ) -> None: ...
    @overload
    def set_validate_mode(
        self, mode: Literal[Validate.Delegate], context: Member
    ) -> None: ...
    @overload
    def set_validate_mode(
        self,
        mode: Literal[Validate.ObjectMethod_OldNew]
        | Literal[Validate.ObjectMethod_NameOldNew]
        | Literal[Validate.MemberMethod_ObjectOldNew],
        context: str,
    ) -> None: ...

KT = TypeVar("KT")
VT = TypeVar("VT")

class atomlist(List[T]): ...
class atomclist(atomlist[T]): ...
class atomset(Set[T]): ...
class atomdict(Dict[KT, VT]): ...

A = TypeVar("A", bound=CAtom)

class atomref(Generic[A]):
    def __new__(cls, atom: A) -> atomref[A]: ...
    def __bool__(self) -> bool: ...
    def __call__(self) -> Optional[A]: ...
    def __sizeof__(self) -> int: ...

class SignalConnector:
    def __call__(self, *args, **kwargs) -> None: ...
    def emit(self, *args, **kwargs) -> None: ...
    def connect(self, slot: Callable) -> None: ...
    def disconnect(self, slot: Callable) -> None: ...

class EventBinder:
    def bind(self, observer: Callable[[Dict[str, Any]], None]) -> None: ...
    def unbind(self, observer: Callable[[Dict[str, Any]], None]) -> None: ...

class DefaultValue(IntEnum):
    CallObject = ...
    CallObject_Object = ...
    CallObject_ObjectName = ...
    Delegate = ...
    Dict = ...
    List = ...
    MemberMethod_Object = ...
    NonOptional = ...
    NoOp = ...
    ObjectMethod = ...
    ObjectMethod_Name = ...
    Set = ...
    Static = ...

class DelAttr(IntEnum):
    Constant = ...
    Delegate = ...
    Event = ...
    NoOp = ...
    Property = ...
    ReadOnly = ...
    Signal = ...
    Slot = ...

class GetAttr(IntEnum):
    CachedProperty = ...
    CallObject_Object = ...
    CallObject_ObjectName = ...
    Delegate = ...
    Event = ...
    MemberMethod_Object = ...
    NoOp = ...
    ObjectMethod = ...
    ObjectMethod_Name = ...
    Property = ...
    Signal = ...
    Slot = ...

class PostGetAttr(IntEnum):
    Delegate = ...
    MemberMethod_ObjectValue = ...
    NoOp = ...
    ObjectMethod_NameValue = ...
    ObjectMethod_Value = ...

class PostSetAttr(IntEnum):
    Delegate = ...
    MemberMethod_ObjectOldNew = ...
    NoOp = ...
    ObjectMethod_NameOldNew = ...
    ObjectMethod_OldNew = ...

class PostValidate(IntEnum):
    Delegate = ...
    MemberMethod_ObjectOldNew = ...
    NoOp = ...
    ObjectMethod_NameOldNew = ...
    ObjectMethod_OldNew = ...

class SetAttr(IntEnum):
    CallObject_ObjectNameValue = ...
    CallObject_ObjectValue = ...
    Constant = ...
    Delegate = ...
    Event = ...
    MemberMethod_ObjectValue = ...
    NoOp = ...
    ObjectMethod_NameValue = ...
    ObjectMethod_Value = ...
    Property = ...
    ReadOnly = ...
    Signal = ...
    Slot = ...

class Validate(IntEnum):
    Bool = ...
    Bytes = ...
    BytesPromote = ...
    Callable = ...
    Coerced = ...
    ContainerList = ...
    Delegate = ...
    Dict = ...
    Enum = ...
    Float = ...
    FloatPromote = ...
    FloatRange = ...
    Instance = ...
    Int = ...
    IntPromote = ...
    List = ...
    MemberMethod_ObjectOldNew = ...
    OptionalInstance = ...
    OptionalTyped = ...
    NoOp = ...
    ObjectMethod_NameOldNew = ...
    ObjectMethod_OldNew = ...
    Range = ...
    Set = ...
    Str = ...
    StrPromote = ...
    Subclass = ...
    Tuple = ...
    Typed = ...

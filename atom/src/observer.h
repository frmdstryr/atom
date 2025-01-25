/*-----------------------------------------------------------------------------
| Copyright (c) 2022-2024, Nucleic Development Team.
|
| Distributed under the terms of the Modified BSD License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
#pragma once

#include <cppy/cppy.h>
#include "utils.h"


namespace atom
{

extern PyObject* PyChangeType;

namespace ChangeType
{

enum Type {
    Create = 1,
    Update = 2,
    Delete = 4,
    Event = 8,
    Property = 16,
    Container = 32,
    Any = 0xFF,
};

} // end ChangeType

inline bool matches_change(PyObject* observer_info, uint8_t change_types )
{
    return (PyLong_AsLong( observer_info ) & change_types) != 0;
}

} // namespace atom

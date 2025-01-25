/*-----------------------------------------------------------------------------
| Copyright (c) 2013-2024, Nucleic Development Team.
|
| Distributed under the terms of the Modified BSD License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
#pragma once

#include <vector>
#include <cppy/cppy.h>
#include "platstdint.h"
#include "observer.h"
#include "modifyguard.h"
#include "utils.h"


namespace atom
{


class ObserverPool
{

    // ModifyGuard template interface
    friend class ModifyGuard<ObserverPool>;
    ModifyGuard<ObserverPool>* get_modify_guard() { return m_modify_guard; }
    void set_modify_guard( ModifyGuard<ObserverPool>* guard ) { m_modify_guard = guard; }

public:

    ObserverPool() : m_modify_guard( 0 ), m_items(PyDict_New()) {}

    ~ObserverPool() {
        Py_CLEAR(m_items);
    }

    bool has_topic( PyObject* topic ) const;

    bool has_observer( PyObject* topic, PyObject* observer ) const
    {
        return has_observer( topic, observer, ChangeType::Any );
    }

    bool has_observer( PyObject* topic, PyObject* observer, uint8_t change_types ) const;

    bool add( PyObject* topic, PyObject* observer, uint8_t member_changes );

    bool remove( PyObject* topic, PyObject* observer );

    bool remove( PyObject* topic );

    void clear();

    bool notify( PyObject* topic, PyObject* args, PyObject* kwargs )
    {
        return notify( topic, args, kwargs, ChangeType::Any );
    }

    bool notify( PyObject* topic, PyObject* args, PyObject* kwargs, uint8_t change_types );

    Py_ssize_t py_sizeof();

    int py_traverse( visitproc visit, void* arg );

private:

    ModifyGuard<ObserverPool>* m_modify_guard;
    PyObject* m_items; // dict[topic, dict[observer, change_types]]
    ObserverPool(const ObserverPool& other);
    ObserverPool& operator=(const ObserverPool&);

};


} // namespace atom

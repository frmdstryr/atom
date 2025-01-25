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

    struct Topic
    {
        Topic( cppy::ptr& topic ) : m_topic( topic ), m_count( 0 ) {}
        Topic( cppy::ptr& topic, uint32_t count ) : m_topic( topic ), m_count( count ) {}
        ~Topic() {}
        bool match( cppy::ptr& topic )
        {
            return m_topic == topic || utils::safe_richcompare( m_topic, topic, Py_EQ );
        }
        cppy::ptr m_topic;
        uint32_t m_count;
    };

    // ModifyGuard template interface
    friend class ModifyGuard<ObserverPool>;
    ModifyGuard<ObserverPool>* get_modify_guard() { return m_modify_guard; }
    void set_modify_guard( ModifyGuard<ObserverPool>* guard ) { m_modify_guard = guard; }

public:

    ObserverPool() : m_modify_guard( 0 ), m_items(PyDict_New()) {}

    ~ObserverPool() {}

    bool has_topic( cppy::ptr& topic );

    bool has_observer( cppy::ptr& topic, cppy::ptr& observer )
    {
        return has_observer( topic, observer, ChangeType::Any );
    }

    bool has_observer( cppy::ptr& topic, cppy::ptr& observer, uint8_t change_types );

    bool add( cppy::ptr& topic, cppy::ptr& observer, uint8_t member_changes );

    bool remove( cppy::ptr& topic, cppy::ptr& observer );

    bool remove( cppy::ptr& topic );

    bool notify( cppy::ptr& topic, cppy::ptr& args, cppy::ptr& kwargs )
    {
        return notify( topic, args, kwargs, ChangeType::Any );
    }

    bool notify( cppy::ptr& topic, cppy::ptr& args, cppy::ptr& kwargs, uint8_t change_types );

    Py_ssize_t py_sizeof()
    {
        Py_ssize_t size = sizeof( ModifyGuard<ObserverPool>* );
        //size += sizeof( std::vector<Topic> ) + sizeof( Topic ) * m_topics.capacity();
        //size += sizeof( std::vector<Observer> ) + sizeof( Observer ) * m_observers.capacity();
        return size;
    };

    int py_traverse( visitproc visit, void* arg );

    void py_clear()
    {
        Py_CLEAR(m_items);
    }

private:

    ModifyGuard<ObserverPool>* m_modify_guard;
    // dict[topic, dict[observer, change_types]]
    PyObject* m_items;
    ObserverPool(const ObserverPool& other);
    ObserverPool& operator=(const ObserverPool&);

};


} // namespace atom

/*-----------------------------------------------------------------------------
| Copyright (c) 2013-2024, Nucleic Development Team.
|
| Distributed under the terms of the Modified BSD License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
#include "observerpool.h"
#include "utils.h"


namespace atom
{

namespace
{

struct BaseTask : public ModifyTask
{
    BaseTask( ObserverPool& pool, cppy::ptr& topic, cppy::ptr& observer ) :
        m_pool( pool ), m_topic( topic ), m_observer( observer ) {}
    ObserverPool& m_pool;
    cppy::ptr m_topic;
    cppy::ptr m_observer;
};


struct AddTask : public BaseTask
{
    AddTask( ObserverPool& pool, cppy::ptr& topic, cppy::ptr& observer, uint8_t change_types ) :
        BaseTask( pool, topic, observer ), m_change_types(change_types) {}
    void run() { m_pool.add( m_topic, m_observer, m_change_types ); }
    uint8_t m_change_types;
};


struct RemoveTask : public BaseTask
{
    RemoveTask( ObserverPool& pool, cppy::ptr& topic, cppy::ptr& observer ) :
        BaseTask( pool, topic, observer ) {}
    void run() { m_pool.remove( m_topic, m_observer ); }
};


struct RemoveTopicTask : ModifyTask
{
    RemoveTopicTask( ObserverPool& pool, cppy::ptr& topic ) :
        m_pool( pool ), m_topic( topic ) {}
    void run() { m_pool.remove( m_topic ); }
    ObserverPool& m_pool;
    cppy::ptr m_topic;
};

} // namespace


bool
ObserverPool::has_topic( cppy::ptr& topic )
{
    if ( !m_items )
        return false;
    int r = PyDict_Contains( m_items, topic.get() );
    if (r < 0)
    {
        if ( PyErr_Occurred() )
            PyErr_Clear();
        return false;
    }
    return r;
}


bool
ObserverPool::has_observer( cppy::ptr& topic, cppy::ptr& observer, uint8_t change_types )
{
    if ( !m_items )
        return false;
    PyObject* observer_map = PyDict_GetItem( m_items, topic.get() );
    if ( !observer_map )
        return false;
    PyObject* info = PyDict_GetItem( observer_map, observer.get() );
    if ( !info )
        return false;
    return matches_change(info, change_types);
}


bool
ObserverPool::add( cppy::ptr& topic, cppy::ptr& observer, uint8_t change_types )
{
    if ( !m_items )
        return false;
    if( m_modify_guard )
    {
        ModifyTask* task = new AddTask( *this, topic, observer, change_types );
        m_modify_guard->add_task( task );
        return true;
    }
    PyObject* observer_map = PyDict_GetItem( m_items, topic.get() );
    if ( !observer_map )
    {
        cppy::ptr new_map( PyDict_New() );
        if ( !new_map )
            return false;
        if ( PyDict_SetItem( m_items, topic.get(), new_map.get() ) < 0 )
            return false;
        observer_map = new_map.release();
    }

    PyObject* info = PyDict_GetItem( observer_map, observer.get() );
    if ( !info || PyLong_AsLong( info ) != change_types )
    {
        cppy::ptr new_info( PyLong_FromLong( change_types ) );
        if ( !new_info )
            return false;
        if ( PyDict_SetItem( observer_map, observer.get(), new_info.get() ) < 0 )
            return false;
    }
    return true;
}


bool
ObserverPool::remove( cppy::ptr& topic, cppy::ptr& observer )
{
    if ( !m_items )
        return false;
    if( m_modify_guard )
    {
        ModifyTask* task = new RemoveTask( *this, topic, observer );
        m_modify_guard->add_task( task );
        return true;
    }

    PyObject* observer_map = PyDict_GetItem( m_items, topic.get() );
    if ( !observer_map )
        return true;
    if ( PyDict_DelItem( observer_map, observer.get() ) < 0 )
    {
        if ( !PyErr_ExceptionMatches( PyExc_KeyError ) )
            return false;
        PyErr_Clear();
    }
    return true;
}


bool
ObserverPool::remove( cppy::ptr& topic )
{
    if ( !m_items )
        return false;
    if( m_modify_guard )
    {
        ModifyTask* task = new RemoveTopicTask( *this, topic );
        m_modify_guard->add_task( task );
        return true;
    }

    if ( PyDict_DelItem( m_items, topic.get() ) < 0 )
    {
        if ( !PyErr_ExceptionMatches( PyExc_KeyError ) )
            return false;
        PyErr_Clear();
    }
    return true;
}


bool
ObserverPool::notify( cppy::ptr& topic, cppy::ptr& args, cppy::ptr& kwargs, uint8_t change_types )
{
    if ( !m_items )
        return false;
    ModifyGuard<ObserverPool> guard( *this );

    PyObject* observer_map = PyDict_GetItem( m_items, topic.get() );
    if ( !observer_map )
        return false;

    cppy::ptr iter( PyObject_GetIter( observer_map ) );
    if ( !iter )
        return false;
    cppy::ptr observer;
    while ( ( observer = iter.next() ) )
    {
        if ( !observer.is_truthy() )
        {
            ModifyTask* task = new RemoveTask( *this, topic, observer );
            m_modify_guard->add_task( task );
            continue;
        }

        PyObject* info = PyDict_GetItem( observer_map, observer.get() );
        if ( matches_change(info, change_types) )
        {
            cppy::ptr ok( observer.call( args, kwargs ) );
            if ( !ok )
                return false;
        }
    }
    return true;
}


int
ObserverPool::py_traverse( visitproc visit, void* arg )
{
    Py_VISIT( m_items );
    return 0;
}


}  //namespace atom

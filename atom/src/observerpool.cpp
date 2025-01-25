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
    BaseTask( ObserverPool& pool, PyObject* topic, PyObject* observer ) :
        m_pool( pool ), m_topic( cppy::incref( topic ) ), m_observer( cppy::incref( observer ) ) {}
    ObserverPool& m_pool;
    cppy::ptr m_topic;
    cppy::ptr m_observer;
};


struct AddTask : public BaseTask
{
    AddTask( ObserverPool& pool, PyObject*  topic, PyObject* observer, uint8_t change_types ) :
        BaseTask( pool, topic, observer ), m_change_types(change_types) {}
    void run() { m_pool.add( m_topic.get(), m_observer.get(), m_change_types ); }
    uint8_t m_change_types;
};


struct RemoveTask : public BaseTask
{
    RemoveTask( ObserverPool& pool, PyObject* topic, PyObject* observer ) :
        BaseTask( pool, topic, observer ) {}
    void run() { m_pool.remove( m_topic.get(), m_observer.get() ); }
};


struct RemoveTopicTask : ModifyTask
{
    RemoveTopicTask( ObserverPool& pool, PyObject* topic ) :
        m_pool( pool ), m_topic( cppy::incref( topic ) ) {}
    void run() { m_pool.remove( m_topic.get() ); }
    ObserverPool& m_pool;
    cppy::ptr m_topic;
};

struct ClearTask : ModifyTask
{
    ClearTask( ObserverPool& pool ) : m_pool( pool ) {}
    void run() { m_pool.clear(); }
    ObserverPool& m_pool;
};

} // namespace


bool
ObserverPool::has_topic( PyObject* topic ) const
{
    PyObject* observer_map = PyDict_GetItem( m_items, topic );
    if ( !observer_map )
        return false;
    return PyObject_IsTrue( observer_map );
}


bool
ObserverPool::has_observer( PyObject* topic, PyObject* observer, uint8_t change_types ) const
{
    PyObject* observer_map = PyDict_GetItem( m_items, topic );
    if ( !observer_map )
        return false;
    PyObject* info = PyDict_GetItem( observer_map, observer );
    if ( !info )
        return false;
    return matches_change(info, change_types);
}


bool
ObserverPool::add( PyObject* topic, PyObject* observer, uint8_t change_types )
{
    if( m_modify_guard )
    {
        ModifyTask* task = new AddTask( *this, topic, observer, change_types );
        m_modify_guard->add_task( task );
        return true;
    }

    if ( !PyObject_IsTrue( observer ) )
        return true; // Owner of method was deleted

    PyObject* observer_map = PyDict_GetItem( m_items, topic );
    if ( !observer_map )
    {
        cppy::ptr new_map( PyDict_New() );
        if ( !new_map )
            return false;
        if ( PyDict_SetItem( m_items, topic, new_map.get() ) < 0 )
            return false;
        observer_map = new_map.get(); // TODO: Is this safe?
    }

    PyObject* info = PyDict_GetItem( observer_map, observer );
    if ( !info || PyLong_AsLong( info ) != change_types )
    {
        cppy::ptr new_info( PyLong_FromLong( change_types ) );
        if ( !new_info )
            return false;
        if ( PyDict_SetItem( observer_map, observer, new_info.get() ) < 0 )
            return false;
    }
    return true;
}


bool
ObserverPool::remove( PyObject* topic, PyObject* observer )
{
    if( m_modify_guard )
    {
        ModifyTask* task = new RemoveTask( *this, topic, observer );
        m_modify_guard->add_task( task );
        return true;
    }

    PyObject* observer_map = PyDict_GetItem( m_items, topic );
    if ( !observer_map )
        return true; // No observers on topic
    if ( PyDict_DelItem( observer_map, observer ) < 0 )
    {
        if ( !PyErr_ExceptionMatches( PyExc_KeyError ) )
            return false;
        PyErr_Clear();
    }

    if ( !PyObject_IsTrue( observer_map ) )
        return PyDict_DelItem( m_items, topic ) == 0; // Also remove topic
    return true;
}


bool
ObserverPool::remove( PyObject* topic )
{
    if( m_modify_guard )
    {
        ModifyTask* task = new RemoveTopicTask( *this, topic );
        m_modify_guard->add_task( task );
        return true;
    }

    if ( PyDict_DelItem( m_items, topic ) < 0 )
    {
        if ( !PyErr_ExceptionMatches( PyExc_KeyError ) )
            return false;
        PyErr_Clear();
    }
    return true;
}

void ObserverPool::clear()
{
    if( m_modify_guard )
    {
        m_modify_guard->add_task( new ClearTask( *this ) );
        return;
    }

    PyDict_Clear( m_items );
}


bool
ObserverPool::notify( PyObject* topic, PyObject* args, PyObject* kwargs, uint8_t change_types )
{
    PyObject* observer_map = PyDict_GetItem( m_items, topic );
    if ( !observer_map )
        return true; // No observers on topic

    ModifyGuard<ObserverPool> guard( *this );
    PyObject *observer, *info;
    Py_ssize_t pos = 0;
    while ( PyDict_Next( observer_map, &pos, &observer, &info ) )
    {
        if ( !PyObject_IsTrue( observer ) )
        {
            ModifyTask* task = new RemoveTask( *this, topic, observer );
            m_modify_guard->add_task( task );
            continue;
        }

        if ( matches_change(info, change_types) )
        {
            PyObject* ok = PyObject_Call( observer, args, kwargs );
            if ( !ok )
                return false;
            Py_DECREF(ok);
        }
    }
    return true;
}

Py_ssize_t
ObserverPool::py_sizeof()
{
    Py_ssize_t size = sizeof( ModifyGuard<ObserverPool>* );
    cppy::ptr sys( PyImport_ImportModule("sys") );
    if ( !sys )
        return 0;
    cppy::ptr getsizeof( PyObject_GetAttrString( sys.get(), "getsizeof" ) );
    if ( !getsizeof )
        return 0;
    cppy::ptr result( PyObject_CallOneArg( getsizeof.get(), m_items ) );
    if ( !result || !PyLong_Check( result.get() ) )
        return 0;
    size += PyLong_AsLong( result.get() );
    // TODO: Walk items use getsize of on each
    return size;
}

int
ObserverPool::py_traverse( visitproc visit, void* arg )
{
    Py_VISIT( m_items );
    return 0;
}


}  //namespace atom

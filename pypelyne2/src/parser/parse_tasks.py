import json
import logging
import operator
import pypelyne2.src.modules.task.task as class_task
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_tasks():

    """Parses the pypelyne2.src.conf.settings.TASKS_FILE file and returns a sorted list of dicts.

    Parameters
    ----------


    Examples
    --------


    Returns
    -------
    list
        a sorted list of container dicts.

    """

    logging.info('parsing tasks')

    with open(SETTINGS.TASKS_FILE, 'r') as f:
        json_object = json.load(f)

    tasks = [task for task in json_object if task['task_enable']]

    # for task in tasks:
    #     task['entity_type'] = 'task'

    return sorted(tasks,
                  key=operator.itemgetter(SETTINGS.SORT_TASKS),
                  reverse=SETTINGS.SORT_TASKS_REVERSE)


def get_tasks():

    """Get all Task() objects in a list

    Parameters
    ----------


    Returns
    -------
    list
        list of pypelyne2.src.modules.task.task.Task() objects

    """

    task_objects = []
    tasks = parse_tasks()
    for task in tasks:
        new_task_object = class_task.Task(task)
        task_objects.append(new_task_object)

    return task_objects

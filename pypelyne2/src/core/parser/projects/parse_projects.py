import json
import logging
# import operator
import os
import pypelyne2.src.core.entities.entityproject as entityproject
# import pypelyne2.src.core.entities.entitycontainer as entitycontainer
# import pypelyne2.src.core.entities.entitytask as entitytask
# import pypelyne2.src.core.entities.entityoutput as entityoutput
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_projects():

    """Parses the pypelyne2.src.conf.settings.taskS_FILE file and returns a sorted list of dicts.

    :returns: list -- a sorted list of task dicts.

    """

    logging.info('parsing projects')

    projects_list = []

    for project_file in SETTINGS.DATABASE_FILES_PROJECTS:

        logging.info('processing project source file: [P_DATABASE_PROJECTS]{0}{1}'.format(os.sep, project_file))

        # print SETTINGS.DATABASE_DIR_ENTITIES
        #
        # print database_file
        #
        # print os.path.join(SETTINGS.DATABASE_DIR_ENTITIES, database_file)

        print os.path.join(SETTINGS.DATABASE_DIR_PROJECTS, project_file)

        with open(os.path.join(SETTINGS.DATABASE_DIR_PROJECTS, project_file), 'r') as f:
            project_object = json.load(f)

            projects_list.append(project_object)

    return projects_list


def get_projects():

    """Get all task() objects in a list

    :returns: list -- of pypelyne2.src.modules.task.task.Task() objects

    """

    project_objects = set()
    projects = parse_projects()

    # print kwargs[u'rcontainers']
    # print kwargs[u'rtasks']
    # print kwargs[u'rplugins']
    # print kwargs[u'routput']

    for project in projects:

        new_entity_object = None

        if project[u'entity_type'] == 'project':
            new_entity_object = entityproject.EntityProject(d=project,
                                                            entity_identifier=project[u'identifier'])

        # if project[u'entity_type'] == 'container':
        #     rcontainer_object = None
        #     # for rcontainer in kwargs[u'rcontainers']:
        #     # if rcontainer.identifier == project[u'entity_specific'][u'rcontainer']:
        #     #     rcontainer_object = rcontainer
        #     #     break
        #     new_entity_object = entitycontainer.EntityContainer(d=project,
        #                                                         entity_identifier=project[u'identifier'],
        #                                                         rcontainer=rcontainer_object)

        # elif project[u'entity_type'] == 'task':
        #     rtask_object = None
        #     for rtask in kwargs[u'rtasks']:
        #         if rtask.identifier == project[u'entity_specific'][u'rtask']:
        #             rtask_object = rtask
        #             break
        #     rplugin_object = None
        #     for rplugin in kwargs[u'rplugins']:
        #         if rplugin.identifier == project[u'entity_specific'][u'rplugin']:
        #             rplugin_object = getattr(rplugin, project[u'entity_specific'][u'rplugin_arch'])
        #             break
        #     new_entity_object = entitytask.EntityTask(d=project,
        #                                               entity_identifier=project[u'identifier'],
        #                                               rtask=rtask_object,
        #                                               rplugin=rplugin_object)
        #
        # elif project[u'entity_type'] == 'output':
        #     routput_object = None
        #     for routput in kwargs[u'routputs']:
        #         if routput.identifier == project[u'entity_specific'][u'routput']:
        #             routput_object = routput
        #             break
        #     new_entity_object = entityoutput.EntityOutput(d=project,
        #                                                   entity_identifier=project[u'identifier'],
        #                                                   routput=routput_object)

        project_objects.add(new_entity_object)

    # for i in entity_objects:
    #     print i.identifier

    return project_objects

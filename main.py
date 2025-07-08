# tootdo - a lightweight CLI todo list app
# credit to Microsoft Windows for the app icon
# © 2025 berriz44. All rights reserved.


import argparse, json, platformdirs, os, pathlib
def touch(fpath: os.PathLike):
    os.close(os.open(fpath, os.O_CREAT | os.O_WRONLY, 0o664))
def remove_items_by_value(d: dict, predicate) -> None:
    """
    Remove items from dict d where predicate(value) is True.

    Args:
        d (dict): The dictionary to modify in-place.
        predicate (callable): A function that takes a value and returns True if
                              the item should be removed.

    Returns:
        None
    """
    for key, value in list(d.items()):
        if predicate(value):
            del d[key]
def strikethrough(text):
    return ''.join(c + '\u0336' for c in text) if text else text

TODO_PATH = pathlib.Path(platformdirs.user_config_path("tootdo")).with_suffix(".json")

if not os.path.isfile(TODO_PATH):
    print("Creating todo file!")
    os.makedirs(os.path.dirname(TODO_PATH))
    touch(TODO_PATH)

with open(TODO_PATH, 'r') as f:
    try:
        todo_dict = json.load(f)
    except:
        todo_dict = dict()

main_parser = argparse.ArgumentParser(prog='tootdo',description='A minimal CLI todo list.',epilog='Additional help can be found by running tootdo {action} -h.\n\nMade with \x1b[5;31;91m\u2661\x1b[0m by berriz44',formatter_class=argparse.RawDescriptionHelpFormatter)
subparsers = main_parser.add_subparsers(title='actions',description='valid actions',required=True,dest='selected_action')

add_parser = subparsers.add_parser("add",help='add either a new todo list or a new task')
add_subparsers = add_parser.add_subparsers(title="add",dest='add_what',required=True)

add_task_parser = add_subparsers.add_parser("task",help='adds a new task to a todo list')
add_task_parser.add_argument("list_name",help='name of the list to add the task to')
add_task_parser.add_argument("task",help='task content',type=str)

add_list_parser = add_subparsers.add_parser("list",help='adds a new todo list')
add_list_parser.add_argument("list_name",help='name of the list to be added',type=str)

remove_parser = subparsers.add_parser("remove",help='remove either an existing todo list or an task')
remove_subparsers = remove_parser.add_subparsers(title="remove",dest='remove_what',required=True)

remove_task_parser = remove_subparsers.add_parser("task",help='removes a task from a todo list')
remove_task_parser.add_argument("list_name",help='name of the list from which the task to be removed is')
remove_task_parser.add_argument("task_number",help='number of the task that will be removed',type=int)

remove_list_parser = remove_subparsers.add_parser("list",help='removes a todo list')
remove_list_parser.add_argument("list_name",help='name of the list to be removed')

complete_parser = subparsers.add_parser("complete",help='mark a task as completed')
complete_parser.add_argument("list_name",help='name of the list from which the task to be completed is')
complete_parser.add_argument("task_number",help='number of the task that will be completed',type=int)

uncomplete_parser = subparsers.add_parser("uncomplete",help='mark a task as completed')
uncomplete_parser.add_argument("list_name",help='name of the list from which the task to be uncompleted is')
uncomplete_parser.add_argument("task_number",help='number of the task that will be uncompleted',type=int)

remove_completed_parser = subparsers.add_parser("remove_completed",help='removes all fully completed todo lists')

remove_completed_tasks_parser = subparsers.add_parser("remove_completed_tasks",help='removes all completed tasks from a specific todo list')

list_parser = subparsers.add_parser("list",help='lists either lists or tasks from a list')
list_subparsers = list_parser.add_subparsers(title="list",dest='list_what',required=True)

list_lists_parser = list_subparsers.add_parser("lists",help='list lists')

list_tasks_parser = list_subparsers.add_parser("tasks",help='lists tasks from a list')
list_tasks_parser.add_argument("list_name",help='list to list tasks from')

args = main_parser.parse_args()

# print(args)

def commit():
    print("Committing JSON...")
    with open(TODO_PATH, 'w') as f:
        json.dump(todo_dict, f)
    print("\x1b[32;92mJSON successfully committed!\x1b[0m")

match args.selected_action:
    case 'add':
        match args.add_what:
            case 'task':
                if not "lists" in todo_dict:
                    todo_dict['lists'] = dict()
                if args.list_name in todo_dict['lists']:
                    todo_dict['lists'][args.list_name].append(args.task)
                    commit()
                else:
                    print("\x1b[31;91mERROR: Invalid list name!\x1b[0m")
            case 'list':
                if not "lists" in todo_dict:
                    todo_dict['lists'] = dict()
                if not args.list_name in todo_dict['lists']:
                    todo_dict['lists'][args.list_name] = list()
                    commit()
    case 'remove':
        match args.remove_what:
            case 'task':
                if not "lists" in todo_dict:
                    print("\x1b[31;91mERROR: No lists!\x1b[0m")
                if args.list_name in todo_dict['lists']:
                    if input("Are you sure? (Y/n): ").lower() == 'y':
                        if 0 <= args.task_number - 1 < len(todo_dict['lists'][args.list_name]):
                            del todo_dict['lists'][args.list_name][args.task_number-1]
                            commit()
                        else:
                            print("\x1b[31;91mERROR: Invalid task index!\x1b[0m")
                else:
                    print("\x1b[31;91mERROR: Invalid list name!\x1b[0m")
            case 'list':
                if not "lists" in todo_dict:
                    print("\x1b[31;91mERROR: No lists!\x1b[0m")
                if args.list_name in todo_dict['lists']:
                    if input("Are you sure? (Y/n): ").lower() == 'y':
                        del todo_dict['lists'][args.list_name]
                        commit()
                else:
                    print("\x1b[31;91mERROR: Invalid list name!\x1b[0m") 
    case 'complete':
        if not "lists" in todo_dict:
            print("\x1b[31;91mERROR: No lists!\x1b[0m")
        if args.list_name in todo_dict['lists']:
            if 0 <= args.task_number-1 <= len(todo_dict['lists'][args.list_name]) - 1:
                if not todo_dict['lists'][args.list_name][args.task_number-1].endswith(chr(6)):
                    todo_dict['lists'][args.list_name][args.task_number-1] += chr(6)
                    commit()
                else:
                    print("\x1b[31;91mERROR: Task already complete!\x1b[0m")
            else:
                print("\x1b[31;91mERROR: Invalid task index!\x1b[0m")
        else:
            print("\x1b[31;91mERROR: Invalid list name!")
    case 'uncomplete':
        if not "lists" in todo_dict:
            print("\x1b[31;91mERROR: No lists!\x1b[0m")
        if args.list_name in todo_dict['lists']:
            if 0 <= args.task_number -1 <= len(todo_dict['lists'][args.list_name]) - 1:
                if todo_dict['lists'][args.list_name][args.task_number].endswith(chr(6)):
                    todo_dict['lists'][args.list_name][args.task_number] = todo_dict['lists'][args.list_name][args.task_number - 1][:-1]
                    commit()
                else:
                    print("\x1b[31;91mTask not complete!\x1b[0m")
        else:
            print("Invalid list name!")
    case 'remove_completed':
        lists = todo_dict.get('lists', {})
        for list_name, tasks in list(lists.items()):
            if tasks and all(task.endswith(chr(6)) for task in tasks):
                del lists[list_name]
        commit()
    case 'remove_completed_tasks':
        for l in todo_dict['lists']:
            tasks = todo_dict['lists'][l]
            todo_dict['lists'][l] = [task for task in tasks if not task.endswith(chr(6))]
        commit()
    case 'list':
        match args.list_what:
            case "lists":
                print(", ".join(todo_dict['lists'].keys()))
            case "tasks":
                for i,t in enumerate(todo_dict['lists'][args.list_name], start=1):
                    print(f"{i}. {t if not t.endswith(chr(6)) else strikethrough(t[:-1])}")
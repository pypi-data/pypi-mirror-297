#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h> 
#include <conio.h> 

typedef struct {
    char **options;
    Py_ssize_t count; 
    int selected;
} Menu;

void init_menu(Menu *menu, char **options, Py_ssize_t count) {
    menu->options = options;
    menu->count = count;
    menu->selected = 0;
}

void display_menu(Menu *menu) {
    system("cls");
    for (Py_ssize_t i = 0; i < menu->count; i++) {
        if (i == menu->selected) {
            printf("--> %s\n", menu->options[i]);
        } else {
            printf("  %s\n", menu->options[i]);
        }
    }
}

void navigate_menu(Menu *menu) {
    int ch;
    while (1) {
        display_menu(menu);
        ch = _getch();

        if (ch == 72) { // вверх
            menu->selected = (menu->selected - 1 + menu->count) % menu->count;
        } else if (ch == 80) { // вниз
            menu->selected = (menu->selected + 1) % menu->count;
        } else if (ch == 13) { // Enter
            break;
        }
    }
}

static PyObject* run_menu(PyObject* self, PyObject* args) {
    PyObject *list;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &list)) {
        return NULL;
    }

    Py_ssize_t count = PyList_Size(list);
    char **options = malloc(count * sizeof(char *));
    
    for (Py_ssize_t i = 0; i < count; i++) {
        PyObject *item = PyList_GetItem(list, i);
        options[i] = malloc((strlen(PyUnicode_AsUTF8(item)) + 1) * sizeof(char));
        strcpy(options[i], PyUnicode_AsUTF8(item));
    }

    Menu menu;
    init_menu(&menu, options, count);
    navigate_menu(&menu);
    
    for (Py_ssize_t i = 0; i < count; i++) {
        free(options[i]);
    }
    free(options);
    
    return PyLong_FromLong(menu.selected);
}

static PyMethodDef MenuMethods[] = {
    {"run_menu", run_menu, METH_VARARGS, "Показать меню."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef menumodule = {
    PyModuleDef_HEAD_INIT,
    "Kpicknenu", 
    NULL, 
    -1, 
    MenuMethods
};

PyMODINIT_FUNC PyInit_Kpickmenu(void) {
    return PyModule_Create(&menumodule);
}

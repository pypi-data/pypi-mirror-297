/*[clinic input]
preserve
[clinic start generated code]*/

#if defined(Py_BUILD_CORE) && !defined(Py_BUILD_CORE_MODULE)
#  include "pycore_gc.h"            // PyGC_Head
#  include "pycore_runtime.h"       // _Py_ID()
#endif


PyDoc_STRVAR(unicodedata_UCD_decimal__doc__,
"decimal($self, chr, default=<unrepresentable>, /)\n"
"--\n"
"\n"
"Converts a Unicode character into its equivalent decimal value.\n"
"\n"
"Returns the decimal value assigned to the character chr as integer.\n"
"If no such value is defined, default is returned, or, if not given,\n"
"ValueError is raised.");

#define UNICODEDATA_UCD_DECIMAL_METHODDEF    \
    {"decimal", _PyCFunction_CAST(unicodedata_UCD_decimal), METH_FASTCALL, unicodedata_UCD_decimal__doc__},

static PyObject *
unicodedata_UCD_decimal_impl(PyObject *self, int chr,
                             PyObject *default_value);

static PyObject *
unicodedata_UCD_decimal(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *return_value = NULL;
    int chr;
    PyObject *default_value = NULL;

    if (!_PyArg_CheckPositional("decimal", nargs, 1, 2)) {
        goto exit;
    }
    if (!PyUnicode_Check(args[0])) {
        _PyArg_BadArgument("decimal", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    if (PyUnicode_READY(args[0])) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(args[0]) != 1) {
        _PyArg_BadArgument("decimal", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(args[0], 0);
    if (nargs < 2) {
        goto skip_optional;
    }
    default_value = args[1];
skip_optional:
    return_value = unicodedata_UCD_decimal_impl(self, chr, default_value);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_digit__doc__,
"digit($self, chr, default=<unrepresentable>, /)\n"
"--\n"
"\n"
"Converts a Unicode character into its equivalent digit value.\n"
"\n"
"Returns the digit value assigned to the character chr as integer.\n"
"If no such value is defined, default is returned, or, if not given,\n"
"ValueError is raised.");

#define UNICODEDATA_UCD_DIGIT_METHODDEF    \
    {"digit", _PyCFunction_CAST(unicodedata_UCD_digit), METH_FASTCALL, unicodedata_UCD_digit__doc__},

static PyObject *
unicodedata_UCD_digit_impl(PyObject *self, int chr, PyObject *default_value);

static PyObject *
unicodedata_UCD_digit(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *return_value = NULL;
    int chr;
    PyObject *default_value = NULL;

    if (!_PyArg_CheckPositional("digit", nargs, 1, 2)) {
        goto exit;
    }
    if (!PyUnicode_Check(args[0])) {
        _PyArg_BadArgument("digit", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    if (PyUnicode_READY(args[0])) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(args[0]) != 1) {
        _PyArg_BadArgument("digit", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(args[0], 0);
    if (nargs < 2) {
        goto skip_optional;
    }
    default_value = args[1];
skip_optional:
    return_value = unicodedata_UCD_digit_impl(self, chr, default_value);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_numeric__doc__,
"numeric($self, chr, default=<unrepresentable>, /)\n"
"--\n"
"\n"
"Converts a Unicode character into its equivalent numeric value.\n"
"\n"
"Returns the numeric value assigned to the character chr as float.\n"
"If no such value is defined, default is returned, or, if not given,\n"
"ValueError is raised.");

#define UNICODEDATA_UCD_NUMERIC_METHODDEF    \
    {"numeric", _PyCFunction_CAST(unicodedata_UCD_numeric), METH_FASTCALL, unicodedata_UCD_numeric__doc__},

static PyObject *
unicodedata_UCD_numeric_impl(PyObject *self, int chr,
                             PyObject *default_value);

static PyObject *
unicodedata_UCD_numeric(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *return_value = NULL;
    int chr;
    PyObject *default_value = NULL;

    if (!_PyArg_CheckPositional("numeric", nargs, 1, 2)) {
        goto exit;
    }
    if (!PyUnicode_Check(args[0])) {
        _PyArg_BadArgument("numeric", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    if (PyUnicode_READY(args[0])) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(args[0]) != 1) {
        _PyArg_BadArgument("numeric", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(args[0], 0);
    if (nargs < 2) {
        goto skip_optional;
    }
    default_value = args[1];
skip_optional:
    return_value = unicodedata_UCD_numeric_impl(self, chr, default_value);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_category__doc__,
"category($self, chr, /)\n"
"--\n"
"\n"
"Returns the general category assigned to the character chr as string.");

#define UNICODEDATA_UCD_CATEGORY_METHODDEF    \
    {"category", (PyCFunction)unicodedata_UCD_category, METH_O, unicodedata_UCD_category__doc__},

static PyObject *
unicodedata_UCD_category_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_category(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("category", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("category", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_category_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_bidirectional__doc__,
"bidirectional($self, chr, /)\n"
"--\n"
"\n"
"Returns the bidirectional class assigned to the character chr as string.\n"
"\n"
"If no such value is defined, an empty string is returned.");

#define UNICODEDATA_UCD_BIDIRECTIONAL_METHODDEF    \
    {"bidirectional", (PyCFunction)unicodedata_UCD_bidirectional, METH_O, unicodedata_UCD_bidirectional__doc__},

static PyObject *
unicodedata_UCD_bidirectional_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_bidirectional(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("bidirectional", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("bidirectional", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_bidirectional_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_combining__doc__,
"combining($self, chr, /)\n"
"--\n"
"\n"
"Returns the canonical combining class assigned to the character chr as integer.\n"
"\n"
"Returns 0 if no combining class is defined.");

#define UNICODEDATA_UCD_COMBINING_METHODDEF    \
    {"combining", (PyCFunction)unicodedata_UCD_combining, METH_O, unicodedata_UCD_combining__doc__},

static int
unicodedata_UCD_combining_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_combining(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;
    int _return_value;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("combining", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("combining", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    _return_value = unicodedata_UCD_combining_impl(self, chr);
    if ((_return_value == -1) && PyErr_Occurred()) {
        goto exit;
    }
    return_value = PyLong_FromLong((long)_return_value);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_mirrored__doc__,
"mirrored($self, chr, /)\n"
"--\n"
"\n"
"Returns the mirrored property assigned to the character chr as integer.\n"
"\n"
"Returns 1 if the character has been identified as a \"mirrored\"\n"
"character in bidirectional text, 0 otherwise.");

#define UNICODEDATA_UCD_MIRRORED_METHODDEF    \
    {"mirrored", (PyCFunction)unicodedata_UCD_mirrored, METH_O, unicodedata_UCD_mirrored__doc__},

static int
unicodedata_UCD_mirrored_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_mirrored(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;
    int _return_value;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("mirrored", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("mirrored", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    _return_value = unicodedata_UCD_mirrored_impl(self, chr);
    if ((_return_value == -1) && PyErr_Occurred()) {
        goto exit;
    }
    return_value = PyLong_FromLong((long)_return_value);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_east_asian_width__doc__,
"east_asian_width($self, chr, /)\n"
"--\n"
"\n"
"Returns the east asian width assigned to the character chr as string.");

#define UNICODEDATA_UCD_EAST_ASIAN_WIDTH_METHODDEF    \
    {"east_asian_width", (PyCFunction)unicodedata_UCD_east_asian_width, METH_O, unicodedata_UCD_east_asian_width__doc__},

static PyObject *
unicodedata_UCD_east_asian_width_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_east_asian_width(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("east_asian_width", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("east_asian_width", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_east_asian_width_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_script__doc__,
"script($self, chr, /)\n"
"--\n"
"\n"
"Returns the script of the character chr as string.");

#define UNICODEDATA_UCD_SCRIPT_METHODDEF    \
    {"script", (PyCFunction)unicodedata_UCD_script, METH_O, unicodedata_UCD_script__doc__},

static PyObject *
unicodedata_UCD_script_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_script(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("script", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("script", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_script_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_block__doc__,
"block($self, chr, /)\n"
"--\n"
"\n"
"Returns the block of the character chr as string.");

#define UNICODEDATA_UCD_BLOCK_METHODDEF    \
    {"block", (PyCFunction)unicodedata_UCD_block, METH_O, unicodedata_UCD_block__doc__},

static PyObject *
unicodedata_UCD_block_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_block(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("block", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("block", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_block_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_script_extensions__doc__,
"script_extensions($self, chr, /)\n"
"--\n"
"\n"
"Returns the script extensions of the character chr as a list of strings.");

#define UNICODEDATA_UCD_SCRIPT_EXTENSIONS_METHODDEF    \
    {"script_extensions", (PyCFunction)unicodedata_UCD_script_extensions, METH_O, unicodedata_UCD_script_extensions__doc__},

static PyObject *
unicodedata_UCD_script_extensions_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_script_extensions(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("script_extensions", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("script_extensions", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_script_extensions_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_indic_conjunct_break__doc__,
"indic_conjunct_break($self, chr, /)\n"
"--\n"
"\n"
"Returns the Indic Conjunct Break category of the character chr as string.");

#define UNICODEDATA_UCD_INDIC_CONJUNCT_BREAK_METHODDEF    \
    {"indic_conjunct_break", (PyCFunction)unicodedata_UCD_indic_conjunct_break, METH_O, unicodedata_UCD_indic_conjunct_break__doc__},

static PyObject *
unicodedata_UCD_indic_conjunct_break_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_indic_conjunct_break(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("indic_conjunct_break", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("indic_conjunct_break", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_indic_conjunct_break_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_indic_positional_category__doc__,
"indic_positional_category($self, chr, /)\n"
"--\n"
"\n"
"Returns the Indic Positional Category of the character chr as string.");

#define UNICODEDATA_UCD_INDIC_POSITIONAL_CATEGORY_METHODDEF    \
    {"indic_positional_category", (PyCFunction)unicodedata_UCD_indic_positional_category, METH_O, unicodedata_UCD_indic_positional_category__doc__},

static PyObject *
unicodedata_UCD_indic_positional_category_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_indic_positional_category(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("indic_positional_category", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("indic_positional_category", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_indic_positional_category_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_indic_syllabic_category__doc__,
"indic_syllabic_category($self, chr, /)\n"
"--\n"
"\n"
"Returns the Indic Syllabic Category of the character chr as string.");

#define UNICODEDATA_UCD_INDIC_SYLLABIC_CATEGORY_METHODDEF    \
    {"indic_syllabic_category", (PyCFunction)unicodedata_UCD_indic_syllabic_category, METH_O, unicodedata_UCD_indic_syllabic_category__doc__},

static PyObject *
unicodedata_UCD_indic_syllabic_category_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_indic_syllabic_category(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("indic_syllabic_category", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("indic_syllabic_category", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_indic_syllabic_category_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_grapheme_cluster_break__doc__,
"grapheme_cluster_break($self, chr, /)\n"
"--\n"
"\n"
"Returns the Grapheme Cluster Break property of the character chr as string.");

#define UNICODEDATA_UCD_GRAPHEME_CLUSTER_BREAK_METHODDEF    \
    {"grapheme_cluster_break", (PyCFunction)unicodedata_UCD_grapheme_cluster_break, METH_O, unicodedata_UCD_grapheme_cluster_break__doc__},

static PyObject *
unicodedata_UCD_grapheme_cluster_break_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_grapheme_cluster_break(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("grapheme_cluster_break", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("grapheme_cluster_break", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_grapheme_cluster_break_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_vertical_orientation__doc__,
"vertical_orientation($self, chr, /)\n"
"--\n"
"\n"
"Returns the Vertical Orientation property of the character chr as string.");

#define UNICODEDATA_UCD_VERTICAL_ORIENTATION_METHODDEF    \
    {"vertical_orientation", (PyCFunction)unicodedata_UCD_vertical_orientation, METH_O, unicodedata_UCD_vertical_orientation__doc__},

static PyObject *
unicodedata_UCD_vertical_orientation_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_vertical_orientation(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("vertical_orientation", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("vertical_orientation", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_vertical_orientation_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_age__doc__,
"age($self, chr, /)\n"
"--\n"
"\n"
"Returns the Age property of the character chr as string.");

#define UNICODEDATA_UCD_AGE_METHODDEF    \
    {"age", (PyCFunction)unicodedata_UCD_age, METH_O, unicodedata_UCD_age__doc__},

static PyObject *
unicodedata_UCD_age_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_age(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("age", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("age", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_age_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_total_strokes__doc__,
"total_strokes($self, chr, /, source=\'G\')\n"
"--\n"
"\n"
"Returns the total number of strokes of a character as integer. The optional \'source\' argument allows one to specify \'G\' (Simplified) or \'T\' (Traditional) stroke counts (default \'G\')\n"
"\n"
"If no such value is defined, returns 0.");

#define UNICODEDATA_UCD_TOTAL_STROKES_METHODDEF    \
    {"total_strokes", _PyCFunction_CAST(unicodedata_UCD_total_strokes), METH_FASTCALL|METH_KEYWORDS, unicodedata_UCD_total_strokes__doc__},

static PyObject *
unicodedata_UCD_total_strokes_impl(PyObject *self, int chr,
                                   const char *source);

static PyObject *
unicodedata_UCD_total_strokes(PyObject *self, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
    #if defined(Py_BUILD_CORE) && !defined(Py_BUILD_CORE_MODULE)

    #define NUM_KEYWORDS 1
    static struct {
        PyGC_Head _this_is_not_used;
        PyObject_VAR_HEAD
        PyObject *ob_item[NUM_KEYWORDS];
    } _kwtuple = {
        .ob_base = PyVarObject_HEAD_INIT(&PyTuple_Type, NUM_KEYWORDS)
        .ob_item = { &_Py_ID(source), },
    };
    #undef NUM_KEYWORDS
    #define KWTUPLE (&_kwtuple.ob_base.ob_base)

    #else  // !Py_BUILD_CORE
    #  define KWTUPLE NULL
    #endif  // !Py_BUILD_CORE

    static const char * const _keywords[] = {"", "source", NULL};
    static _PyArg_Parser _parser = {
        .keywords = _keywords,
        .fname = "total_strokes",
        .kwtuple = KWTUPLE,
    };
    #undef KWTUPLE
    PyObject *argsbuf[2];
    Py_ssize_t noptargs = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0) - 1;
    int chr;
    const char *source = "G";

    args = _PyArg_UnpackKeywords(args, nargs, NULL, kwnames, &_parser, 1, 2, 0, argsbuf);
    if (!args) {
        goto exit;
    }
    if (!PyUnicode_Check(args[0])) {
        _PyArg_BadArgument("total_strokes", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    if (PyUnicode_READY(args[0])) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(args[0]) != 1) {
        _PyArg_BadArgument("total_strokes", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(args[0], 0);
    if (!noptargs) {
        goto skip_optional_pos;
    }
    if (!PyUnicode_Check(args[1])) {
        _PyArg_BadArgument("total_strokes", "argument 'source'", "str", args[1]);
        goto exit;
    }
    Py_ssize_t source_length;
    source = PyUnicode_AsUTF8AndSize(args[1], &source_length);
    if (source == NULL) {
        goto exit;
    }
    if (strlen(source) != (size_t)source_length) {
        PyErr_SetString(PyExc_ValueError, "embedded null character");
        goto exit;
    }
skip_optional_pos:
    return_value = unicodedata_UCD_total_strokes_impl(self, chr, source);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_decomposition__doc__,
"decomposition($self, chr, /)\n"
"--\n"
"\n"
"Returns the character decomposition mapping assigned to the character chr as string.\n"
"\n"
"An empty string is returned in case no such mapping is defined.");

#define UNICODEDATA_UCD_DECOMPOSITION_METHODDEF    \
    {"decomposition", (PyCFunction)unicodedata_UCD_decomposition, METH_O, unicodedata_UCD_decomposition__doc__},

static PyObject *
unicodedata_UCD_decomposition_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_decomposition(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("decomposition", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("decomposition", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_decomposition_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_is_normalized__doc__,
"is_normalized($self, form, unistr, /)\n"
"--\n"
"\n"
"Return whether the Unicode string unistr is in the normal form \'form\'.\n"
"\n"
"Valid values for form are \'NFC\', \'NFKC\', \'NFD\', and \'NFKD\'.");

#define UNICODEDATA_UCD_IS_NORMALIZED_METHODDEF    \
    {"is_normalized", _PyCFunction_CAST(unicodedata_UCD_is_normalized), METH_FASTCALL, unicodedata_UCD_is_normalized__doc__},

static PyObject *
unicodedata_UCD_is_normalized_impl(PyObject *self, PyObject *form,
                                   PyObject *input);

static PyObject *
unicodedata_UCD_is_normalized(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *return_value = NULL;
    PyObject *form;
    PyObject *input;

    if (!_PyArg_CheckPositional("is_normalized", nargs, 2, 2)) {
        goto exit;
    }
    if (!PyUnicode_Check(args[0])) {
        _PyArg_BadArgument("is_normalized", "argument 1", "str", args[0]);
        goto exit;
    }
    if (PyUnicode_READY(args[0]) == -1) {
        goto exit;
    }
    form = args[0];
    if (!PyUnicode_Check(args[1])) {
        _PyArg_BadArgument("is_normalized", "argument 2", "str", args[1]);
        goto exit;
    }
    if (PyUnicode_READY(args[1]) == -1) {
        goto exit;
    }
    input = args[1];
    return_value = unicodedata_UCD_is_normalized_impl(self, form, input);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_normalize__doc__,
"normalize($self, form, unistr, /)\n"
"--\n"
"\n"
"Return the normal form \'form\' for the Unicode string unistr.\n"
"\n"
"Valid values for form are \'NFC\', \'NFKC\', \'NFD\', and \'NFKD\'.");

#define UNICODEDATA_UCD_NORMALIZE_METHODDEF    \
    {"normalize", _PyCFunction_CAST(unicodedata_UCD_normalize), METH_FASTCALL, unicodedata_UCD_normalize__doc__},

static PyObject *
unicodedata_UCD_normalize_impl(PyObject *self, PyObject *form,
                               PyObject *input);

static PyObject *
unicodedata_UCD_normalize(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *return_value = NULL;
    PyObject *form;
    PyObject *input;

    if (!_PyArg_CheckPositional("normalize", nargs, 2, 2)) {
        goto exit;
    }
    if (!PyUnicode_Check(args[0])) {
        _PyArg_BadArgument("normalize", "argument 1", "str", args[0]);
        goto exit;
    }
    if (PyUnicode_READY(args[0]) == -1) {
        goto exit;
    }
    form = args[0];
    if (!PyUnicode_Check(args[1])) {
        _PyArg_BadArgument("normalize", "argument 2", "str", args[1]);
        goto exit;
    }
    if (PyUnicode_READY(args[1]) == -1) {
        goto exit;
    }
    input = args[1];
    return_value = unicodedata_UCD_normalize_impl(self, form, input);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_name__doc__,
"name($self, chr, default=<unrepresentable>, /)\n"
"--\n"
"\n"
"Returns the name assigned to the character chr as a string.\n"
"\n"
"If no name is defined, default is returned, or, if not given,\n"
"ValueError is raised.");

#define UNICODEDATA_UCD_NAME_METHODDEF    \
    {"name", _PyCFunction_CAST(unicodedata_UCD_name), METH_FASTCALL, unicodedata_UCD_name__doc__},

static PyObject *
unicodedata_UCD_name_impl(PyObject *self, int chr, PyObject *default_value);

static PyObject *
unicodedata_UCD_name(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *return_value = NULL;
    int chr;
    PyObject *default_value = NULL;

    if (!_PyArg_CheckPositional("name", nargs, 1, 2)) {
        goto exit;
    }
    if (!PyUnicode_Check(args[0])) {
        _PyArg_BadArgument("name", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    if (PyUnicode_READY(args[0])) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(args[0]) != 1) {
        _PyArg_BadArgument("name", "argument 1", "a unicode character", args[0]);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(args[0], 0);
    if (nargs < 2) {
        goto skip_optional;
    }
    default_value = args[1];
skip_optional:
    return_value = unicodedata_UCD_name_impl(self, chr, default_value);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_lookup__doc__,
"lookup($self, name, /)\n"
"--\n"
"\n"
"Look up character by name.\n"
"\n"
"If a character with the given name is found, return the\n"
"corresponding character.  If not found, KeyError is raised.");

#define UNICODEDATA_UCD_LOOKUP_METHODDEF    \
    {"lookup", (PyCFunction)unicodedata_UCD_lookup, METH_O, unicodedata_UCD_lookup__doc__},

static PyObject *
unicodedata_UCD_lookup_impl(PyObject *self, const char *name,
                            Py_ssize_t name_length);

static PyObject *
unicodedata_UCD_lookup(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    const char *name;
    Py_ssize_t name_length;

    if (!PyArg_Parse(arg, "s#:lookup", &name, &name_length)) {
        goto exit;
    }
    return_value = unicodedata_UCD_lookup_impl(self, name, name_length);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_is_emoji__doc__,
"is_emoji($self, chr, /)\n"
"--\n"
"\n"
"Returns True if chr is Emoji=Yes.");

#define UNICODEDATA_UCD_IS_EMOJI_METHODDEF    \
    {"is_emoji", (PyCFunction)unicodedata_UCD_is_emoji, METH_O, unicodedata_UCD_is_emoji__doc__},

static PyObject *
unicodedata_UCD_is_emoji_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_is_emoji(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("is_emoji", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("is_emoji", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_is_emoji_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_is_emoji_presentation__doc__,
"is_emoji_presentation($self, chr, /)\n"
"--\n"
"\n"
"Returns True if chr is Emoji_Presentation=Yes.");

#define UNICODEDATA_UCD_IS_EMOJI_PRESENTATION_METHODDEF    \
    {"is_emoji_presentation", (PyCFunction)unicodedata_UCD_is_emoji_presentation, METH_O, unicodedata_UCD_is_emoji_presentation__doc__},

static PyObject *
unicodedata_UCD_is_emoji_presentation_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_is_emoji_presentation(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("is_emoji_presentation", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("is_emoji_presentation", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_is_emoji_presentation_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_is_emoji_modifier__doc__,
"is_emoji_modifier($self, chr, /)\n"
"--\n"
"\n"
"Returns True if chr is Emoji_Modifier=Yes.");

#define UNICODEDATA_UCD_IS_EMOJI_MODIFIER_METHODDEF    \
    {"is_emoji_modifier", (PyCFunction)unicodedata_UCD_is_emoji_modifier, METH_O, unicodedata_UCD_is_emoji_modifier__doc__},

static PyObject *
unicodedata_UCD_is_emoji_modifier_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_is_emoji_modifier(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("is_emoji_modifier", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("is_emoji_modifier", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_is_emoji_modifier_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_is_emoji_modifier_base__doc__,
"is_emoji_modifier_base($self, chr, /)\n"
"--\n"
"\n"
"Returns True if chr is Emoji_Modifier_Base=Yes.");

#define UNICODEDATA_UCD_IS_EMOJI_MODIFIER_BASE_METHODDEF    \
    {"is_emoji_modifier_base", (PyCFunction)unicodedata_UCD_is_emoji_modifier_base, METH_O, unicodedata_UCD_is_emoji_modifier_base__doc__},

static PyObject *
unicodedata_UCD_is_emoji_modifier_base_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_is_emoji_modifier_base(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("is_emoji_modifier_base", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("is_emoji_modifier_base", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_is_emoji_modifier_base_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_is_emoji_component__doc__,
"is_emoji_component($self, chr, /)\n"
"--\n"
"\n"
"Returns True if chr is Emoji_Component=Yes.");

#define UNICODEDATA_UCD_IS_EMOJI_COMPONENT_METHODDEF    \
    {"is_emoji_component", (PyCFunction)unicodedata_UCD_is_emoji_component, METH_O, unicodedata_UCD_is_emoji_component__doc__},

static PyObject *
unicodedata_UCD_is_emoji_component_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_is_emoji_component(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("is_emoji_component", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("is_emoji_component", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_is_emoji_component_impl(self, chr);

exit:
    return return_value;
}

PyDoc_STRVAR(unicodedata_UCD_is_extended_pictographic__doc__,
"is_extended_pictographic($self, chr, /)\n"
"--\n"
"\n"
"Returns True if chr is Extended_Pictographic=Yes.");

#define UNICODEDATA_UCD_IS_EXTENDED_PICTOGRAPHIC_METHODDEF    \
    {"is_extended_pictographic", (PyCFunction)unicodedata_UCD_is_extended_pictographic, METH_O, unicodedata_UCD_is_extended_pictographic__doc__},

static PyObject *
unicodedata_UCD_is_extended_pictographic_impl(PyObject *self, int chr);

static PyObject *
unicodedata_UCD_is_extended_pictographic(PyObject *self, PyObject *arg)
{
    PyObject *return_value = NULL;
    int chr;

    if (!PyUnicode_Check(arg)) {
        _PyArg_BadArgument("is_extended_pictographic", "argument", "a unicode character", arg);
        goto exit;
    }
    if (PyUnicode_READY(arg)) {
        goto exit;
    }
    if (PyUnicode_GET_LENGTH(arg) != 1) {
        _PyArg_BadArgument("is_extended_pictographic", "argument", "a unicode character", arg);
        goto exit;
    }
    chr = PyUnicode_READ_CHAR(arg, 0);
    return_value = unicodedata_UCD_is_extended_pictographic_impl(self, chr);

exit:
    return return_value;
}
/*[clinic end generated code: output=4fd16f4b0bec3307 input=a9049054013a1b77]*/

/*
 *                        _oo0oo_
 *                       o8888888o
 *                       88" . "88
 *                       (| -_- |)
 *                       0\  =  /0
 *                     ___/`---'\___
 *                   .' \\|     |// '.
 *                  / \\|||  :  |||// \
 *                 / _||||| -:- |||||- \
 *                |   | \\\  - /// |   |
 *                | \_|  ''\---/''  |_/ |
 *                \  .-\__  '-'  ___/-. /
 *              ___'. .'  /--.--\  `. .'___
 *           ."" '<  `.___\_<|>_/___.' >' "".
 *          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
 *          \  \ `_.   \_ __\ /__ _/   .-` /  /
 *      =====`-.____`.___ \_____/___.-`___.-'=====
 *                        `=---='
 * 
 *  Author       : Zhang Zetong
 *  Date         : 2024-07-10 09:17:11
 *  LastEdit     : 2024-09-19 17:24:47
 *  Description  : ZCurvePy Source Code
 */
#include<Python.h>
#include"ZCurveSeq.cpp"

#define PY_SSIZE_T_CLEAN

/* Python Index Error */
#define INDEX_ERR PyErr_SetString(PyExc_IndexError, "Out of index. ")
/* Python Value Error */
#define VALUE_ERR PyErr_SetString(PyExc_IndexError, "Invalid parameters. ")

/* Should return Z-Curve parameters in display mode */
static bool display = false;

/* General keywords list for some functions */
static char *kwListA[] = {"normalize", NULL};
static char *kwListB[] = {"phase", "normalize", NULL};
static char *kwListC[] = {"inplace", NULL};
static char *kwListD[] = {"window", "return_n", NULL};
static char *kwListE[] = {"subseq", "control", NULL};

/* Rich segmentation controls*/
static char RY[] = "RY", MK[] = "MK", SW[] = "SW", GC[] = "GC", AT[] = "AT";
static char zp[] = "zp", CpG[] = "CpG";
static char S1[] = "Genome_dS", S2[] = "GC_dS", S3[] = "CpG_dS";

/* ZCurvePy package */
static PyObject *zcurvepy;

/* Python build-in functions */
static PyObject *py_open, *py_load, *py_join, *py_exists;

/* Resource file storage path */
static PyObject *modelPath, *dataPath;
static PyObject *BioSeq, *SeqRecord, *BioMotifs, *find_peaks;

/* Rich-find controls */
static char forward[] = "f";
static char reverse[] = "r";
static char all[]     = "a";
static char forall[] = "fa";
static char revall[] = "ra";

/* pickle.load API for loading model files */
static PyObject *
pickleLoad(PyObject *path) {
    static PyObject *close = Py_BuildValue("s", "close");
    PyObject *binary = Py_None;

    if (Py_IsTrue(PyObject_CallFunction(py_exists, "O", path))) {
        PyObject *file = PyObject_CallFunction(py_open, "Os", path, "rb");
        binary = PyObject_CallFunction(py_load, "O", file);
        PyObject_CallMethodNoArgs(file, close);
    }

    return binary;
}

/* Try to convert paramters array to display mode matrix */
static PyObject *
toMatrix(float *params, int row, int col) {
    PyObject *paramList;
    int i, j, len = row * col;

    if (display) {
        paramList = PyList_New(row);

        for (i = 0; i < row; i ++) {
            PyObject *vec = PyList_New(col);
            
            for (j = 0; j < col; j ++)
                PyList_SetItem(vec, j, Py_BuildValue("f", params[j * 3 + i]));

            PyList_SetItem(paramList, i, vec);
        }
    } else {
        paramList = PyList_New(len);

        for (i = 0; i < len; i ++)
            PyList_SetItem(paramList, i, Py_BuildValue("f", params[i]));
    }

    return paramList;
}

/* Convert parameters to x-y curve */
static PyObject *
toCurve(float *params, int len, bool back) {
    if (back) {
        PyObject *xList = PyList_New(len);
        PyObject *yList = PyList_New(len);

        for (int i = 0; i < len; i++) {
            PyList_SetItem(xList, i, Py_BuildValue("i", i));
            PyList_SetItem(yList, i, Py_BuildValue("f", params[i]));
        }

        delete[] params;

        return Py_BuildValue("[O,O]", xList, yList);
    } else {
        PyObject *yList = PyList_New(len);

        for (int i = 0; i < len; i++)
            PyList_SetItem(yList, i, Py_BuildValue("f", params[i]));

        delete[] params;

        return yList;
    }
}

/* ZCurveSeq PyObject */
typedef struct {
    PyObject_HEAD
    int iter;
    ZCurveSeq *cppObject;
} ZCurveSeqObject;

/* ZCurveSeq C API */
static ZCurveSeqObject *ZCurveSeq_newObject(char *seq, bool isRNA);

static void
ZCurveSeq_dealloc(ZCurveSeqObject *self) {
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static int
ZCurveSeq_init(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    static char *kwlist[] = {"seq_or_record", "is_rna", NULL};
    bool isRNA = false;
    PyObject *seq;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "O|b", kwlist, &seq, &isRNA))
        return -1;
    
    char *cppSeq;

    if(PyObject_IsInstance(seq, SeqRecord))
        seq = PyObject_GetAttrString(seq, "seq");
    
    PyArg_Parse(PyObject_Str(seq), "s", &cppSeq);

    self->cppObject = new ZCurveSeq(cppSeq, isRNA);

    return 0;
}

static PyObject *
ZCurveSeq_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    ZCurveSeqObject *self;
    
    self = (ZCurveSeqObject *) type->tp_alloc(type, 0);
    self->iter = 0;

    return (PyObject *) self;
}

static PyObject *
ZCurveSeq_str(ZCurveSeqObject *self, PyObject *Py_UNUSED(ignored)) {
    return Py_BuildValue("s", self->cppObject->seq);
}

static PyObject *
ZCurveSeq_iter(ZCurveSeqObject *self, PyObject *Py_UNUSED(ignored)) {
    self->iter = 0;
    return Py_NewRef(self);
}

static PyObject *
ZCurveSeq_iternext(ZCurveSeqObject *self, PyObject *Py_UNUSED(ignored)) {
    static char buf[2] = {0};

    if (self->iter < self->cppObject->len) {
        buf[0] = self->cppObject->seq[self->iter ++];
        return Py_BuildValue("s", buf);
    }

    return NULL;
}

static PyObject *
ZCurveSeq_repr(ZCurveSeqObject *self, PyObject *Py_UNUSED(ignored)) {
    char message[75], *pseq = self->cppObject->seq;
    int l;
    
    if ((l = self->cppObject->len) <= 60)
        strcat(strcat(strcpy(message, "ZCurveSeq(\""), pseq), "\")");
    else {
        strncat(strcpy(message, "ZCurveSeq(\""), pseq, 29);
        strcat(strcat(strcpy(message + 40, "..."), pseq + l - 29), "\")");
    }

    return Py_BuildValue("s", message);
}

static Py_ssize_t 
ZCurveSeq_len(ZCurveSeqObject *self, PyObject *Py_UNUSED(ignored)) {
    return (Py_ssize_t) self->cppObject->len;
}

static PyObject *
ZCurveSeq_concat(ZCurveSeqObject *self, PyObject *other) {
    if (PyObject_IsInstance(other, SeqRecord))
        other = PyObject_GetAttrString(other, "seq");

    const char *seq = PyUnicode_AsUTF8(PyObject_Str(other));
    int slen = self->cppObject->len, alen = (int) strlen(seq);
    char *buf = new char[slen + alen + 1];
    
    strcat(strcpy(buf, self->cppObject->seq), seq);

    ZCurveSeqObject *newObject = ZCurveSeq_newObject(buf, self->cppObject->isRNA);
        
    return (PyObject *) newObject;
}

static PyObject *
ZCurveSeq_repeat(ZCurveSeqObject *self, Py_ssize_t repeat) {
    int newLen = self->cppObject->len * ((int) repeat), i;
    char *buf = new char[newLen + 1];

    for (i = 0, buf[0] = 0; i < repeat; i ++)
        strcat(buf, self->cppObject->seq);
    
    ZCurveSeqObject *newObject = ZCurveSeq_newObject(buf, self->cppObject->isRNA);
        
    return (PyObject *) newObject;
}

static PyObject *
ZCurveSeq_inplace_concat(ZCurveSeqObject *self, PyObject *other) {
    if (PyObject_IsInstance(other, SeqRecord))
        other = PyObject_GetAttrString(other, "seq");

    const char *seq = PyUnicode_AsUTF8(PyObject_Str(other));

    self->cppObject->inplaceConcat(seq);

    return Py_NewRef(self);
}

static PyObject *
ZCurveSeq_inplace_repeat(ZCurveSeqObject *self, Py_ssize_t repeat) {
    self->cppObject->inplaceRepeat((int) repeat);
    return Py_NewRef(self);
}

static PyObject *
ZCurveSeq_richcmpfunc(ZCurveSeqObject *self, PyObject *other, int op) {
    bool boolean;

    if (PyObject_IsInstance(other, SeqRecord))
        other = PyObject_GetAttrString(other, "seq");

    const char *seq = PyUnicode_AsUTF8(PyObject_Str(other));
    char *cppSeq = new char[strlen(seq) + 1];
    strcpy(cppSeq, seq);
        
    Seq seqObject(cppSeq);

    switch(op) {
        case Py_EQ: boolean = *self->cppObject == seqObject; break;
        case Py_NE: boolean = *self->cppObject != seqObject; break;
        case Py_LT: boolean = *self->cppObject <  seqObject; break;
        case Py_GT: boolean = *self->cppObject >  seqObject; break;
        case Py_LE: boolean = *self->cppObject <= seqObject; break;
        case Py_GE: boolean = *self->cppObject >= seqObject; break;
        default: return Py_NotImplemented;
    }

    return boolean ? Py_True : Py_False;
}

static int
ZCurveSeq_contains(ZCurveSeqObject *self, PyObject *other) {
    if (PyObject_IsInstance(other, SeqRecord))
        other = PyObject_GetAttrString(other, "seq");

    const char *seq = PyUnicode_AsUTF8(PyObject_Str(other));
    char *cppSeq = new char[strlen(seq) + 1];
    strcpy(cppSeq, seq);
        
    Seq seqObject(cppSeq);

    return *self->cppObject >= seqObject;
}

static PyObject *
ZCurveSeq_upper(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false, isRNA = self->cppObject->isRNA;
    ZCurveSeqObject *newObject;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListC, &inplace))
        Py_RETURN_NONE;

    if (inplace) {
        self->cppObject->upper();
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        newObject = ZCurveSeq_newObject(seq, isRNA);
        newObject->cppObject->upper();
        return (PyObject *) newObject;
    }
}

static PyObject *
ZCurveSeq_lower(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false, isRNA = self->cppObject->isRNA;
    ZCurveSeqObject *newObject;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListC, &inplace))
        Py_RETURN_NONE;

    if (inplace) {
        self->cppObject->lower();
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        newObject = ZCurveSeq_newObject(seq, isRNA);
        newObject->cppObject->lower();
        return (PyObject *) newObject;
    }
}

static PyObject *
ZCurveSeq_call(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    char *seq = self->cppObject->seq, *control, *result;
    const char *subseq;
    int len, sublen, i;
    PyObject *list, *pyObject;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "Os", kwListE, &pyObject, &control))
        Py_RETURN_NONE;

    if (PyObject_IsInstance(pyObject, SeqRecord))
        pyObject = PyObject_GetAttrString(pyObject, "seq");
    
    subseq = PyUnicode_AsUTF8(PyObject_Str(pyObject));
    
    len = self->cppObject->len, sublen = (int) strlen(subseq);

    if (!strcmp(control, forward) && (result = strcasestr(seq, subseq)))
        return Py_BuildValue("i", result - seq);
    else if (!strcmp(control, reverse)) {
        char *rev = new char[len + 1], *subrev = new char[sublen + 1];
        
        for (i = 0, rev[len] = 0; i < len; i ++)
            rev[i] = seq[len - i - 1];

        for (i = 0, subrev[sublen] = 0; i < sublen; i ++)
            subrev[i] = subseq[sublen - i - 1];

        if (result = strcasestr(rev, subrev)) {
            pyObject = Py_BuildValue("i", len - 2 - (result - rev));
            delete[] rev;
            delete[] subrev;
            return pyObject;
        }
    } else if (!strcmp(control, all)) {
        list = PyList_New(0), result = seq;

        while (result = strcasestr(result, subseq)) {
            PyList_Append(list, Py_BuildValue("i", result - seq));
            result ++;
        }
        
        return list;
    } else if (!strcmp(control, forall)) {
        list = PyList_New(0), result = seq;

        while (result = strcasestr(result, subseq)) {
            PyList_Append(list, Py_BuildValue("i", result - seq));
            result += sublen;
        }
        
        return list;
    } else if (!strcmp(control, revall)) {
        char *rev = new char[len + 1], *subrev = new char[sublen + 1];

        for (i = 0, rev[len] = 0; i < len; i ++)
            rev[i] = seq[len - i - 1];

        for (i = 0, subrev[sublen] = 0; i < sublen; i ++)
            subrev[i] = subseq[sublen - i - 1];

        list = PyList_New(0), result = rev;

        while (result = strcasestr(result, subrev)) {
            PyList_Append(list, Py_BuildValue("i", len - 2 - (result - rev)));
            result += sublen;
        }

        delete[] rev;
        delete[] subrev;
        PyList_Reverse(list);

        return list;
    } else VALUE_ERR;

    Py_RETURN_NONE;
}

static PyObject *
ZCurveSeq_swapcase(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false, isRNA = self->cppObject->isRNA;
    ZCurveSeqObject *newObject;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListC, &inplace))
        Py_RETURN_NONE;

    if (inplace) {
        self->cppObject->swapcase();
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        newObject = ZCurveSeq_newObject(seq, isRNA);
        newObject->cppObject->swapcase();
        return (PyObject *) newObject;
    }
}

static PyObject *
ZCurveSeq_transcribe(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListC, &inplace))
        Py_RETURN_NONE;

    if (inplace) {
        self->cppObject->transcribe();
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        ZCurveSeqObject *newObject = ZCurveSeq_newObject(seq, true);
        newObject->cppObject->transcribe();
        return (PyObject *) newObject;
    }
}

static PyObject *
ZCurveSeq_backTranscribe(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListC, &inplace))
        Py_RETURN_NONE;
    
    if (inplace) {
        self->cppObject->backTrans();
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        ZCurveSeqObject *newObject = ZCurveSeq_newObject(seq, false);
        newObject->cppObject->backTrans();
        return (PyObject *) newObject;
    }
}

static PyObject *
ZCurveSeq_reverse(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false, isRNA = self->cppObject->isRNA;
    ZCurveSeqObject *newObject;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListC, &inplace))
        Py_RETURN_NONE;

    if (inplace) {
        self->cppObject->rev();
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        newObject = ZCurveSeq_newObject(seq, isRNA);
        newObject->cppObject->rev();
        return (PyObject *) newObject;
    }
}

/* TODO */
static PyObject *
ZCurveSeq_shuffle(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false, isRNA = self->cppObject->isRNA;
    int n = 1, i;
    ZCurveSeqObject *newObject;
    static char *kwlist[] = {"inplace", "n", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|bi", kwlist, &inplace, &n))
        Py_RETURN_NONE;

    if (inplace) {
        for (i = 0; i < n; i ++)
            self->cppObject->shuffle();
        
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        newObject = ZCurveSeq_newObject(seq, isRNA);

        for (i = 0; i < n; i ++)
            newObject->cppObject->shuffle();

        return (PyObject *) newObject;
    }
}

static PyObject *
ZCurveSeq_subscript(ZCurveSeqObject *self, PyObject *value) {
    if (PySlice_Check(value)) {
        char *sub, *p;
        Py_ssize_t start, stop, step, i, len = (Py_ssize_t) self->cppObject->len;
        
        PySlice_GetIndices(value, len, &start, &stop, &step);

        if (start < 0) start = 0; else if (start > len - 1) start = len - 1;
        if (stop < 0) stop = 0; else if (stop > len) stop = len;

        sub = new char[(len = (stop - start) / step) + 1], p = sub;

        for (i = start; i < stop; i += step)
            *p ++ = self->cppObject->seq[i];
        
        *p = 0;

        ZCurveSeqObject *newObject = ZCurveSeq_newObject(sub, self->cppObject->isRNA);

        return (PyObject *) newObject;
    } else if (PyNumber_Check(value)) {
        int index, len = self->cppObject->len;
        static char base[2] = {0};

        PyArg_Parse(value, "i", &index);
        
        if (index < 0 ) index = len + index;

        if (index < 0 || index > len - 1) {
            INDEX_ERR;
            Py_RETURN_NONE;
        }

        base[0] = self->cppObject->seq[index];
        
        return Py_BuildValue("s", base);
    }
}

static int
ZCurveSeq_ass_subscript(ZCurveSeqObject *self, PyObject *value, PyObject *other) {
    int len = self->cppObject->len;

    if (PySlice_Check(value)) {
        Py_ssize_t start, stop, step;
        
        PySlice_GetIndices(value, len, &start, &stop, &step);

        if (start < 0) start = 0; else if (start > len - 1) start = len - 1;
        if (stop < 0) stop = 0; else if (stop > len) stop = len;

        if (PyObject_IsInstance(other, SeqRecord))
            other = PyObject_GetAttrString(other, "seq");
        
        self->cppObject->replace((int) start, (int) stop, PyUnicode_AsUTF8(PyObject_Str(other)));
    } if (PyNumber_Check(value)) {
        int index;

        PyArg_Parse(value, "i", &index);

        if (index < 0 ) index = len + index;

        if (index < 0 || index > len - 1) {
            INDEX_ERR;
            return -1;
        }

        if (PyObject_IsInstance(other, SeqRecord))
            other = PyObject_GetAttrString(other, "seq");

        self->cppObject->replace(index, index + 1, PyUnicode_AsUTF8(PyObject_Str(other)));
    }

    return 0;
}

static PyObject *
ZCurveSeq_complement(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false, isRNA = self->cppObject->isRNA;
    ZCurveSeqObject *newObject;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListC, &inplace))
        Py_RETURN_NONE;

    if (inplace) {
        self->cppObject->comp();
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        newObject = ZCurveSeq_newObject(seq, isRNA);
        newObject->cppObject->comp();
        return (PyObject *) newObject;
    }
}

static PyObject *
ZCurveSeq_reverseComplement(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool inplace = false, isRNA = self->cppObject->isRNA;
    ZCurveSeqObject *newObject;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListC, &inplace))
        Py_RETURN_NONE;

    if (inplace) {
        self->cppObject->revComp();
        return Py_NewRef(self);
    } else {
        char *seq = new char[self->cppObject->len + 1];
        strcpy(seq, self->cppObject->seq);
        newObject = ZCurveSeq_newObject(seq, isRNA);
        newObject->cppObject->revComp();
        return (PyObject *) newObject;
    }
}

static PyObject *
ZCurveSeq_gc(ZCurveSeqObject *self, PyObject *Py_UNUSED(ignored)) {
    return Py_BuildValue("f", self->cppObject->gc());
}

static PyObject *
ZCurveSeq_translate(ZCurveSeqObject *self, PyObject *Py_UNUSED(ignored)) {
    int len = self->cppObject->len;

    char *protein = new char[len / 3 + 1];

    self->cppObject->translate(protein);
    PyObject *retr = PyObject_CallFunction(BioSeq, "s", protein);

    return retr;
}

static PyObject *
ZCurveSeq_monoTrans(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    float params[3];
    bool norml = false;
    
    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListA, &norml))
        Py_RETURN_NONE;

    self->cppObject->monoTrans(params, norml);
    
    PyObject *paramList = PyList_New(3);
    
    for (int i = 0; i < 3; i++)
        PyList_SetItem(paramList, i, Py_BuildValue("f", params[i]));

    return paramList;
}

static PyObject *
ZCurveSeq_diTrans(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    float params[12];
    bool norml = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListA, &norml))
        Py_RETURN_NONE;
    
    self->cppObject->diTrans(params, norml);

    return toMatrix(params, 3, 4);
}

static PyObject *
ZCurveSeq_triTrans(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    float params[48];
    bool norml = false;
    
    if (!PyArg_ParseTupleAndKeywords(args, kw, "|b", kwListA, &norml))
        Py_RETURN_NONE;
    
    self->cppObject->triTrans(params, norml);

    return toMatrix(params, 3, 16);
}

static PyObject *
ZCurveSeq_monoPhaseTrans(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    int phase = 3;
    bool norml = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListB, &phase, &norml))
        Py_RETURN_NONE;

    float params[16 * 3];
    
    self->cppObject->monoPhaseTrans(params, phase, norml);

    return toMatrix(params, 3, phase);
}

static PyObject *
ZCurveSeq_diPhaseTrans(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    int phase = 3;
    bool norml = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListB, &phase, &norml))
        Py_RETURN_NONE;
    
    float params[16 * 12];

    self->cppObject->diPhaseTrans(params, phase, norml);
    
    return toMatrix(params, 3, phase * 4);
}

static PyObject *
ZCurveSeq_triPhaseTrans(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool norml = false;
    int phase = 3;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListB, &phase, &norml))
        Py_RETURN_NONE;
    
    float params[16 * 48];

    self->cppObject->triPhaseTrans(params, phase, norml);

    return toMatrix(params, 3, phase * 16);
}

static PyObject *
ZCurveSeq_nPhaseTrans(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    bool norml = false;
    int phase = 3, n = 3;
    int i, k;
    static char *kwlist[] = {"n", "phase", "normalize", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|iib", kwlist, &n, &phase, &norml))
        Py_RETURN_NONE;

    for (i = 0, k = 1; i < n - 1; i ++) k *= 4;

    float params[16 * 64 * 3];

    self->cppObject->nPhaseTrans(params, n, phase, norml);

    return toMatrix(params, 3, phase * k);
}

static PyObject *
ZCurveSeq_toSeq(ZCurveSeqObject *self, PyObject *Py_UNUSED(ignored)) {
    return PyObject_CallFunction(BioSeq, "s", self->cppObject->seq);
}

static PyObject *
ZCurveSeq_toSeqRecord(ZCurveSeqObject *self, PyObject *args, PyObject *kw) {
    char *id;
    static char *kwlist[] = {"id", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kw, "s", kwlist, &id))
        Py_RETURN_NONE;

    PyObject *seq = PyObject_CallFunction(BioSeq, "s", self->cppObject->seq);

    return PyObject_CallFunction(SeqRecord, "Osss", seq, id, "", "");
}

static PyMethodDef ZCurveSeq_methods[] = {
    {"upper", (PyCFunction) ZCurveSeq_upper, METH_VARARGS|METH_KEYWORDS, "To upper case"},
    {"lower", (PyCFunction) ZCurveSeq_lower, METH_VARARGS|METH_KEYWORDS, "To lower case"},
    {"swapcase", (PyCFunction) ZCurveSeq_swapcase, METH_VARARGS|METH_KEYWORDS, "Swap upper and lower case"},
    {"shuffle", (PyCFunction) ZCurveSeq_shuffle, METH_VARARGS|METH_KEYWORDS, "Shuffle the sequence"},
    {"GC", (PyCFunction) ZCurveSeq_gc, METH_NOARGS, "(G+C)% of a standard DNA or RNA sequence"},
    {"reverse", (PyCFunction) ZCurveSeq_reverse, METH_VARARGS|METH_KEYWORDS, "Reverse operation"},
    {"complement", (PyCFunction) ZCurveSeq_complement, METH_VARARGS|METH_KEYWORDS, "Complement operation"},
    {"reverse_complement", (PyCFunction) ZCurveSeq_reverseComplement, METH_VARARGS|METH_KEYWORDS, "Reverse complement operation"},
    {"transcribe", (PyCFunction) ZCurveSeq_transcribe, METH_VARARGS|METH_KEYWORDS, "Transcribe the DNA sequence"},
    {"back_transcribe", (PyCFunction) ZCurveSeq_backTranscribe, METH_VARARGS|METH_KEYWORDS, "Back transcribe the RNA sequence"},
    {"translate", (PyCFunction) ZCurveSeq_translate, METH_NOARGS, "Translate the DNA/RNA sequence (positive strand)"},
    {"mononucleotide_transform", (PyCFunction) ZCurveSeq_monoTrans, METH_VARARGS|METH_KEYWORDS, "Standard Z-Curve Transform"},
    {"dinucleotide_transform", (PyCFunction) ZCurveSeq_diTrans, METH_VARARGS|METH_KEYWORDS, "Dinucleotide Z-Curve Transform"},
    {"trinucleotide_transform", (PyCFunction) ZCurveSeq_triTrans, METH_VARARGS|METH_KEYWORDS, "Trinucleotide Z-Curve Transform"},
    {"mononucleotide_phase_transform", (PyCFunction) ZCurveSeq_monoPhaseTrans, METH_VARARGS|METH_KEYWORDS, "Phase-Specific Z-Curve Transform"},
    {"dinucleotide_phase_transform", (PyCFunction) ZCurveSeq_diPhaseTrans, METH_VARARGS|METH_KEYWORDS, "Dinucleotide Phase-Specific Z-Curve Transform"},
    {"trinucleotide_phase_transform", (PyCFunction) ZCurveSeq_triPhaseTrans, METH_VARARGS|METH_KEYWORDS, "Trinucleotide Phase-Specific Z-Curve Transform"},
    {"n_nucleotide_phase_transform", (PyCFunction) ZCurveSeq_nPhaseTrans, METH_VARARGS|METH_KEYWORDS, "Trinucleotide Phase-Specific Z-Curve Transform"},
    {"to_Seq", (PyCFunction) ZCurveSeq_toSeq, METH_NOARGS, "Convert To Bio.Seq"},
    {"to_SeqRecord", (PyCFunction) ZCurveSeq_toSeqRecord, METH_VARARGS|METH_KEYWORDS, "Convert To Bio.SeqRecord"},
    {NULL, NULL, 0, NULL}
};

static PySequenceMethods ZCurveSeq_sq_methods = {
    (lenfunc) ZCurveSeq_len,
    (binaryfunc) ZCurveSeq_concat,
    (ssizeargfunc) ZCurveSeq_repeat,
    NULL, /* sq_item */
    NULL, /* was_sq_slice */
    NULL, /* sq_ass_item */
    NULL, /* was_sq_ass_slice */
    (objobjproc) ZCurveSeq_contains,
    (binaryfunc) ZCurveSeq_inplace_concat,
    (ssizeargfunc) ZCurveSeq_inplace_repeat
};

static PyMappingMethods ZCurveSeq_mp_methods = {
    NULL /* mp_length */,
    (binaryfunc) ZCurveSeq_subscript,
    (objobjargproc) ZCurveSeq_ass_subscript
};

static PyTypeObject ZCurveSeqType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "zcurvepy.ZCurveSeq",
    sizeof(ZCurveSeqObject),
    0,
    (destructor) ZCurveSeq_dealloc,
    NULL, /* tp_vectorcall_offset */
    NULL, /* tp_getattr */
    NULL, /* tp_setattr */
    NULL, /* tp_as_async */
    (reprfunc) ZCurveSeq_repr,
    NULL, /* tp_as_number */
    &ZCurveSeq_sq_methods,
    &ZCurveSeq_mp_methods,
    NULL, /* tp_hash */
    (ternaryfunc) ZCurveSeq_call,
    (reprfunc) ZCurveSeq_str,
    NULL, /* tp_getattro */
    NULL, /* tp_setattro */
    NULL, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,
    PyDoc_STR("Util for Z-Curve operation"),
    NULL, /* tp_traverse */
    NULL, /* tp_clear */
    (richcmpfunc) ZCurveSeq_richcmpfunc,
    NULL, /* tp_weaklistoffset */
    (getiterfunc) ZCurveSeq_iter,
    (iternextfunc) ZCurveSeq_iternext,
    ZCurveSeq_methods,
    NULL, /* tp_members */
    NULL, /* tp_getset */
    NULL, /* tp_base */
    NULL, /* tp_dict */
    NULL, /* tp_descr_get */
    NULL, /* tp_descr_set */
    NULL, /* tp_dictoffset */
    (initproc) ZCurveSeq_init,
    NULL, /* tp_alloc */
    ZCurveSeq_new
};

static ZCurveSeqObject *ZCurveSeq_newObject(char *seq, bool isRNA) {
    ZCurveSeqObject *newObject = PyObject_New(ZCurveSeqObject, &ZCurveSeqType);
    newObject->cppObject = new ZCurveSeq(seq, isRNA);
    return newObject;
}

typedef struct {
    PyObject_HEAD
    ZCurveSeq *cppObject;
} GCProfileObject;

static void
GCProfile_dealloc(GCProfileObject *self) {
    Py_TYPE(self)->tp_free((PyObject *) self);
};

static PyObject *
GCProfile_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    GCProfileObject *self;
    
    self = (GCProfileObject *) type->tp_alloc(type, 0);
    self->cppObject = NULL;

    return (PyObject *) self;
}

static int
GCProfile_init(GCProfileObject *self, PyObject *args, PyObject *kw) {
    static char *kwlist[] = {"seq_or_record", NULL};
    PyObject *seq_or_record;
    char *seq;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "O", kwlist, &seq_or_record))
        return -1;
    
    if (Py_IS_TYPE(seq_or_record, &ZCurveSeqType)) {
        seq = ((ZCurveSeqObject *) seq_or_record)->cppObject->seq;
    } else {
        if (PyObject_IsInstance(seq_or_record, SeqRecord))
            seq_or_record = PyObject_GetAttrString(seq_or_record, "seq");
            
        PyArg_Parse(PyObject_Str(seq_or_record), "s", &seq);
    }

    self->cppObject = new ZCurveSeq(seq);

    return 0;
}

static PyObject *
GCProfile_str(GCProfileObject *self, PyObject *Py_UNUSED(ignored)) {
    return Py_BuildValue("s", self->cppObject->seq);
}

static PyObject *
GCProfile_repr(GCProfileObject *self, PyObject *Py_UNUSED(ignored)) {
    char message[75], *pseq = self->cppObject->seq;
    int l;
    
    if ((l = self->cppObject->len) <= 60)
        strcat(strcat(strcpy(message, "GCProfile(\""), pseq), "\")");
    else {
        strncat(strcpy(message, "GCProfile(\""), pseq, 29);
        strcat(strcat(strcpy(message + 40, "..."), pseq + l - 29), "\")");
    }

    return Py_BuildValue("s", message);
}

static PyObject *
GCProfile_genomeOrderIndex(GCProfileObject *self, PyObject *Py_UNUSED(ignored)) {
    return Py_BuildValue("f", self->cppObject->genomeOrderIndex());
}

static PyObject *
GCProfile_gcOrderIndex(GCProfileObject *self, PyObject *Py_UNUSED(ignored)) {
    return Py_BuildValue("f", self->cppObject->gcOrderIndex());
}

static PyObject *
GCProfile_CpGOrderIndex(GCProfileObject *self, PyObject *Py_UNUSED(ignored)) {
    return Py_BuildValue("f", self->cppObject->CpGOrderIndex());
}

static PyObject *
GCProfile_zCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0, i, j;
    float *params[3];
    bool back = true;

    for (i = 0; i < 3; i ++) params[i] = new float[len];

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;

    self->cppObject->zTrans(params, window);

    PyObject *paramList = PyList_New(0);

    if (back) {
        PyObject *vec = PyList_New(len);

        for (i = 0; i < len; i ++)
            PyList_SetItem(vec, i, Py_BuildValue("i", i));
        
        PyList_Append(paramList, vec);
    }

    for (i = 0; i < 3; i ++) {
        PyObject *vec = PyList_New(len);
            
        for (j = 0; j < len; j ++)
            PyList_SetItem(vec, j, Py_BuildValue("f", params[i][j]));

        PyList_Append(paramList, vec);
    }

    for (i = 0; i < 3; i ++) delete[] params[i];

    return paramList;
}

static PyObject *
GCProfile_RYCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;
    
    self->cppObject->ryTrans(params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}

static PyObject *
GCProfile_MKCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;
    
    self->cppObject->mkTrans(params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}

static PyObject *
GCProfile_SWCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;
    
    self->cppObject->swTrans(params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}

static PyObject *
GCProfile_ATCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;
    
    self->cppObject->atTrans(params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}

static PyObject *
GCProfile_GCCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;
    
    self->cppObject->gcTrans(params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}

static PyObject *
GCProfile_CpGCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    float *params = new float[len], k;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;
    
    k = self->cppObject->CpGTrans(params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyList_Append(retr, Py_BuildValue("f", k));
    } else retr = Py_BuildValue("[O,O]", toCurve(params, len, back), Py_BuildValue("f", k));

    return retr;
}

static PyObject *
GCProfile_zPrimeCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len], k;
    k = self->cppObject->zPrimeTrans(params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyList_Append(retr, Py_BuildValue("f", k));
    } else retr = Py_BuildValue("[O,O]", toCurve(params, len, back), Py_BuildValue("f", k));

    return retr;
}

static PyObject *
GCProfile_averGCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int window = 1000;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;
    
    int len = self->cppObject->len;
    float *params = new float[len];
    self->cppObject->averGCTrans(params, window);
    return toCurve(params, len, back);
}

static PyObject *
GCProfile_genomeDeltaSCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, m, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len];
    m = self->cppObject->genomeDeltaSTrans(params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyList_Append(retr, Py_BuildValue("i", m));
    } else retr = Py_BuildValue("[O,O]", toCurve(params, len, back), Py_BuildValue("i", m));
    
    return retr;
}

static PyObject *
GCProfile_gcDeltaSCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len];
    self->cppObject->gcDeltaSTrans(params, window);
    return toCurve(params, len, back);
}

static PyObject *
GCProfile_CpGdeltaSCurve(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int len = self->cppObject->len, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListD, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len];
    self->cppObject->CpGDeltaSTrans(params, window);
    return toCurve(params, len, back);
}

static PyObject *
GCProfile_segmentation(GCProfileObject *self, PyObject *args, PyObject *kw) {
    int k = 1, window = 1000, prom = 10, minLen = 0, maxLen = 0xFFFFFF, s, e;
    static char *kwtup[] = {"curve", "k", "window", "prominence", "min_len", "max_len", NULL};
    static PyObject *one = Py_BuildValue("i", 1), *zero = Py_BuildValue("i", 0);
    char *control;
    
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s|iiiii", kwtup, &control, &k, &window, &prom, &minLen, &maxLen))
        Py_RETURN_NONE;
    
    int len = self->cppObject->len, i, j;
    float *buf = new float[len];
    PyObject *iters[2], *start, *end;
    PyObject *retr = PyList_New(0), *yList = PyList_New(len);

    if (!strcmp(RY, control))
        self->cppObject->ryTrans(buf, window);
    else if (!strcmp(MK, control))
        self->cppObject->mkTrans(buf, window);
    else if (!strcmp(SW, control))
        self->cppObject->swTrans(buf, window);
    else if (!strcmp(AT, control))
        self->cppObject->atTrans(buf, window);
    else if (!strcmp(GC, control))
        self->cppObject->gcTrans(buf, window);
    else if (!strcmp(CpG, control))
        self->cppObject->CpGTrans(buf, window);
    else if (!strcmp(zp, control))
        self->cppObject->zPrimeTrans(buf, window);
    else if (!strcmp(S1, control))
        self->cppObject->genomeDeltaSTrans(buf, window);
    else if (!strcmp(S2, control))
        self->cppObject->gcDeltaSTrans(buf, window);
    else if (!strcmp(S3, control))
        self->cppObject->CpGDeltaSTrans(buf, window);
    else {
        VALUE_ERR;
        Py_RETURN_NONE;
    }

    for (i = -1, k = k < 0; i < 2; i += 2) {
        for (j = 0; j < len; j ++)
            PyList_SetItem(yList, j, Py_BuildValue("f", i * buf[j]));

        iters[i > 0] = PyObject_GetIter(PyObject_GetItem(
                       PyObject_CallFunction(find_peaks, "OOOii", yList, Py_None, Py_None, 50, prom), zero));
    }

    if ((start = PyIter_Next(iters[k])) == NULL) goto END;
    if ((end = PyIter_Next(iters[!k])) == NULL) goto FINAL;
    
    if (PyObject_RichCompareBool(start, end, Py_GT)) {
        PyArg_Parse(start, "i", &s);
        PyArg_Parse(end, "i", &e);

        if ((e - s) > minLen && (e - s) < maxLen)
            PyList_Append(retr, PySlice_New(zero, end, one));

        end = PyIter_Next(iters[!k]);
    }

    if (end != NULL)
        do {
            PyArg_Parse(start, "i", &s);
            PyArg_Parse(end, "i", &e);

            if ((e - s) > minLen && (e - s) < maxLen)
                    PyList_Append(retr, PySlice_New(start, end, one));
    } while ((start = PyIter_Next(iters[k])) && (end = PyIter_Next(iters[!k])));

    FINAL: if (start != NULL) {
        PyArg_Parse(start, "i", &s);

        if ((len - s) > minLen && (len - s) < maxLen)
            PyList_Append(retr, PySlice_New(start, Py_BuildValue("i", len), one));
    }
    
    delete[] buf;

    END: return retr;
}

static PyMethodDef GCProfile_methods[] = {
    {"genome_order_index", (PyCFunction) GCProfile_genomeOrderIndex, METH_NOARGS, "Genome order index"},
    {"GC_order_index", (PyCFunction) GCProfile_gcOrderIndex, METH_NOARGS, "GC-content order index"},
    {"CpG_order_index", (PyCFunction) GCProfile_CpGOrderIndex, METH_NOARGS, "CpG order index"},
    {"z_curve", (PyCFunction) GCProfile_zCurve, METH_VARARGS|METH_KEYWORDS, "Digit-specific Z-Curve transform"},
    {"RY_curve", (PyCFunction) GCProfile_RYCurve, METH_VARARGS|METH_KEYWORDS, "RY-disparity curve"},
    {"MK_curve", (PyCFunction) GCProfile_MKCurve, METH_VARARGS|METH_KEYWORDS, "MK-disparity curve"},
    {"SW_curve", (PyCFunction) GCProfile_SWCurve, METH_VARARGS|METH_KEYWORDS, "SW-disparity curve"},
    {"AT_curve", (PyCFunction) GCProfile_ATCurve, METH_VARARGS|METH_KEYWORDS, "AT-disparity curve"},
    {"GC_curve", (PyCFunction) GCProfile_GCCurve, METH_VARARGS|METH_KEYWORDS, "GC-disparity curve"},
    {"CpG_curve", (PyCFunction) GCProfile_CpGCurve, METH_VARARGS|METH_KEYWORDS, "CpG-disparity curve"},
    {"z_prime_curve", (PyCFunction) GCProfile_zPrimeCurve, METH_VARARGS|METH_KEYWORDS, "z'n curve transform"},
    {"average_GC_curve", (PyCFunction) GCProfile_averGCurve, METH_VARARGS|METH_KEYWORDS, "Get average G+C content curve"},
    {"genome_dS_curve", (PyCFunction) GCProfile_genomeDeltaSCurve, METH_VARARGS|METH_KEYWORDS, "Get genome △S curve"},
    {"GC_dS_curve", (PyCFunction) GCProfile_gcDeltaSCurve, METH_VARARGS|METH_KEYWORDS, "Get GC-content △S curve"},
    {"CpG_dS_curve", (PyCFunction) GCProfile_CpGdeltaSCurve, METH_VARARGS|METH_KEYWORDS, "Get CpG △S curve"},
    {"segmentation", (PyCFunction) GCProfile_segmentation, METH_VARARGS|METH_KEYWORDS, "Sequence segmentation"},
    {NULL, NULL, 0, NULL}
};

static PyTypeObject GCProfileType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "zcurvepy.GCProfile",
    sizeof(GCProfileObject),
    0,
    (destructor) GCProfile_dealloc,
    NULL, /* tp_vectorcall_offset */
    NULL, /* tp_getattr */
    NULL, /* tp_setattr */
    NULL, /* tp_as_async */
    (reprfunc) GCProfile_repr,
    NULL, /* tp_as_number */
    NULL, /* tp_as_sequence */
    NULL, /* tp_as_mapping */
    NULL, /* tp_hash */
    NULL, /* tp_call */
    (reprfunc) GCProfile_str,
    NULL, /* tp_getattro */
    NULL, /* tp_setattro */
    NULL, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,
    PyDoc_STR("GC-Profile"),
    NULL, /* tp_traverse */
    NULL, /* tp_clear */
    NULL, /* tp_richcompare */
    NULL, /* tp_weaklistoffset */
    NULL, /* tp_iter */ 
    NULL, /* tp_iternext */ 
    GCProfile_methods,
    NULL, /* tp_members */ 
    NULL, /* tp_getset */
    NULL, /* tp_base */
    NULL, /* tp_dict */ 
    NULL, /* tp_descr_get */ 
    NULL, /* tp_descr_set */ 
    NULL, /* tp_dictoffset */ 
    (initproc) GCProfile_init,
    NULL, /* tp_alloc */
    GCProfile_new
};

typedef struct {
    PyObject_HEAD
    int species;
    PyObject *model;
    PyObject *coding;
    // PyObject *segment;
} OriFinderObject;

static void
OriFinder_dealloc(OriFinderObject *self) {
    Py_XDECREF(self->model);
    Py_XDECREF(self->coding);
    // Py_XDECREF(self->segment);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
OriFinder_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    OriFinderObject *self;
    
    self = (OriFinderObject *) type->tp_alloc(type, 0);
    self->model = Py_None;
    self->coding = Py_None;
    // self->segment = Py_None;

    return (PyObject *) self;
}

static int
OriFinder_init(OriFinderObject *self, PyObject *args, PyObject *kw) {
    static char *kwlist[] = {"species", "model", "coding", "segment", NULL};
    PyObject *species = Py_None;
    PyObject *model = NULL, *coding = NULL, *segment = NULL;

    static PyObject *ScPath = PyObject_CallFunction(py_join, "Os", modelPath, "OriFinder_Sc.pkl");

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|OOOOO", kwlist, &species, &model, &coding, &segment))
        return -1;

    if (PyObject_RichCompareBool(species, Py_BuildValue("s", "Sc"), Py_EQ)) {
        self->model = pickleLoad(ScPath);
        self->coding = PyObject_GetAttrString(zcurvepy, "_sc_coding");
        // self->segment = PyObject_GetAttrString(zcurvepy, "_sc_segment");
    }

    if (model != NULL) {
        const char *repr = PyUnicode_AsUTF8(PyObject_Repr(PyObject_Type(model)));

        if (!strcmp(repr, "<class 'str'>"))
            self->model = pickleLoad(model);
        else self->model = model;
    }

    if (coding != NULL) self->coding = coding;
    // if (segment != NULL) self->segment = segment;

    return 0;
}

static PyObject *
OriFinder_predict(OriFinderObject *self, PyObject *args, PyObject *kw) {
    static char *kwlist[] = {"seqs", NULL};
    static PyObject *slot = Py_BuildValue("i", 1);
    PyObject *seqs;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "O", kwlist, &seqs))
        Py_RETURN_NONE;

    PyObject *iter = PyObject_GetIter(seqs);
    PyObject *predict = PyObject_GetAttrString(self->model, "predict_proba");
    PyObject *list = PyList_New(0), *results = PyList_New(0);
    PyObject *seq, *params, *item;

    while ((seq = PyIter_Next(iter))) {
        if (PyObject_IsInstance(seq, SeqRecord))
            seq = PyObject_GetAttrString(seq, "seq");
        
        params = PyObject_CallFunction(self->coding, "O", PyObject_Str(seq));
        PyList_Append(list, params);
    }

    iter = PyObject_GetIter(PyObject_CallFunction(predict, "O", list));

    while((item = PyIter_Next(iter)))
        PyList_Append(results, PyObject_GetItem(item, slot));

    return results;
}

// static PyObject *
// OriFinder_find(OriFinderObject *self, PyObject *args, PyObject *kw) {
//     static char *kwlist[] = {"seq", "min_proba", "motif", NULL};
//     PyObject *min_proba = Py_BuildValue("f", 0.5), *proba;
//     PyObject *seq, *slices, *motif, *iterA, *iterB, *slice, *list, *results;

//     if (!PyArg_ParseTupleAndKeywords(args, kw, "O|OO", kwlist, &seq, &min_proba, &motif))
//         Py_RETURN_NONE;

//     if (PyObject_IsInstance(seq, SeqRecord))
//         seq = PyObject_GetAttrString(seq, "seq");
    
//     results = PyList_New(0), list = PyList_New(0);
//     slices = PyObject_CallFunction(self->segment, "O", seq = PyObject_Str(seq));
//     iterA = PyObject_GetIter(slices);

//     while ((slice = PyIter_Next(iterA)))
//         PyList_Append(list, PyObject_GetItem(seq, slice));
    
//     list = PyObject_CallMethod((PyObject *) self, "predict", "O", list);
    
//     iterA = PyObject_GetIter(slices);
//     iterB = PyObject_GetIter(list);
    
//     while((slice = PyIter_Next(iterA)) && (proba = PyIter_Next(iterB))) {
//         if (PyObject_RichCompareBool(proba, min_proba, Py_GT)) {
//             PyObject *item = PyList_New(3);
//             PyList_SetItem(item, 0, PyObject_GetAttrString(slice, "start"));
//             PyList_SetItem(item, 1, PyObject_GetAttrString(slice, "stop"));
//             PyList_SetItem(item, 2, proba);
//             PyList_Append(results, item);
//         }
//     }

//     return results;
// }

static PyMethodDef OriFinder_methods[] {
    {"predict", (PyCFunction) OriFinder_predict, METH_VARARGS|METH_KEYWORDS, "Predict if a set of sequences are replication origins. "},
    // {"find", (PyCFunction) OriFinder_find, METH_VARARGS|METH_KEYWORDS, "Find replication origins of a DNA sequence (usually genome). "},
    {NULL, NULL, 0, NULL}
};

static PyTypeObject OriFinderType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "zcurvepy.OriFinder",
    sizeof(OriFinderObject),
    0,
    (destructor) OriFinder_dealloc,
    NULL, /* tp_vectorcall_offset */
    NULL, /* tp_getattr */ 
    NULL, /* tp_setattr */ 
    NULL, /* tp_as_async */
    NULL, /* tp_repr */
    NULL, /* tp_as_number */
    NULL, /* tp_as_sequence */ 
    NULL, /* tp_as_mapping */
    NULL, /* tp_hash */
    NULL, /* tp_call */
    NULL, /* tp_str */
    NULL, /* tp_getattro */
    NULL, /* tp_setattro */
    NULL, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,
    PyDoc_STR("Ori-Finder"),
    NULL, /* tp_traverse */
    NULL, /* tp_clear */
    NULL, /* tp_richcompare */
    NULL, /* tp_weaklistoffset */
    NULL, /* tp_iter */ 
    NULL, /* tp_iternext */
    OriFinder_methods,
    NULL, /* tp_members */
    NULL, /* tp_getset */
    NULL, /* tp_base */
    NULL, /* tp_dict */
    NULL, /* tp_descr_get */
    NULL, /* tp_descr_set */
    NULL, /* tp_dictoffset */
    (initproc) OriFinder_init,
    NULL, /* tp_alloc */
    OriFinder_new
};

static PyObject *
ZCurvePy_download(PyObject *self, PyObject *args, PyObject *kw) {
    static char *kwlist[] = {"item", "path", NULL};
    char *name, *path;
    
    if (!PyArg_ParseTupleAndKeywords(args, kw, "s|s", kwlist, &name, &path))
        return Py_False;
    
    return Py_True;
}

static PyObject *
ZCurvePy_setDisplay(PyObject *self, PyObject *args) {
    PyArg_ParseTuple(args, "b", &display);
    Py_RETURN_NONE;
}

static PyObject *
ZCurvePy_ScCoding(PyObject *self, PyObject *args) {
    char *seq;
    float params[249];

    PyArg_ParseTuple(args, "s", &seq);

    PyObject *list = PyList_New(249);
    ZCurveSeq *cppObject = new ZCurveSeq(seq);

    cppObject->diTrans(params, true);
    cppObject->triTrans(params + 12, true);
    cppObject->monoPhaseTrans(params + 60, 3, true);
    cppObject->diPhaseTrans(params + 69, 3, true);
    cppObject->triPhaseTrans(params + 105, 3, true);

    for (int i = 0; i < 249; i ++)
        PyList_SetItem(list, i, Py_BuildValue("f", params[i]));
    
    return list;
}

// static PyObject *
// ZCurvePy_ScSegment(PyObject *self, PyObject *args) {
//     GCProfileObject *gcProfile = PyObject_New(GCProfileObject, &GCProfileType);
//     char *seq;

//     PyArg_ParseTuple(args, "s", &seq);
//     gcProfile->cppObject = new ZCurveSeq(seq);

//     PyObject *segmentation = PyObject_GetAttrString((PyObject *) gcProfile, "segmentation");

//     return PyObject_CallFunction(segmentation, "iii", 1, 100, 10);
// }

static PyMethodDef ZCurvePy_methods[] = {
    {"download", (PyCFunction) ZCurvePy_download, METH_VARARGS|METH_KEYWORDS, "Download resources from TUBIC server. "},
    {"set_display", (PyCFunction) ZCurvePy_setDisplay, METH_VARARGS, "Enable or disable parameters display mode. "},
    {"_sc_coding", (PyCFunction) ZCurvePy_ScCoding, METH_VARARGS, "Z-Curve coding for S. cerevisiae ARS prediction. "},
    // {"_sc_segment", (PyCFunction) ZCurvePy_ScSegment, METH_VARARGS, "Z-Curve segmentation for S. cerevisiae ARS prediction. "},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef ZCurvePyModule = {
    PyModuleDef_HEAD_INIT,
    "zcurvepy",
    "Python Z-Curve Toolkit",
    -1,
    ZCurvePy_methods
};

PyMODINIT_FUNC 
PyInit_zcurvepy(void) {
    PyObject *py_os, *py_path, *userPath, *homePath, *py_mkdir;

    py_os = PyImport_ImportModule("os");
    py_open = PyObject_GetAttrString(PyImport_ImportModule("io"), "open");
    py_load = PyObject_GetAttrString(PyImport_ImportModule("pickle"), "load");

    py_path = PyObject_GetAttrString(py_os, "path");
    py_join = PyObject_GetAttrString(py_path, "join");
    py_exists = PyObject_GetAttrString(py_path, "exists");
    py_mkdir = PyObject_GetAttrString(py_os, "mkdir");

    userPath = PyObject_CallMethod(py_path, "expandvars", "s", "$HOMEPATH");
    homePath = PyObject_CallFunction(py_join, "Os", userPath, ".tubic");
    
    if (Py_IsFalse(PyObject_CallFunction(py_exists, "O", homePath)))
        PyObject_CallFunction(py_mkdir, "O", homePath);
    
    modelPath = PyObject_CallFunction(py_join, "Os", homePath, "models");

    if (Py_IsFalse(PyObject_CallFunction(py_exists, "O", modelPath)))
        PyObject_CallFunction(py_mkdir, "O", modelPath);
    
    dataPath = PyObject_CallFunction(py_join, "Os", homePath, "database");

    if (Py_IsFalse(PyObject_CallFunction(py_exists, "O", dataPath)))
        PyObject_CallFunction(py_mkdir, "O", dataPath);

    BioSeq = PyObject_GetAttrString(PyImport_ImportModule("Bio.Seq"), "Seq");
    SeqRecord = PyObject_GetAttrString(PyImport_ImportModule("Bio.SeqRecord"), "SeqRecord");
    find_peaks = PyObject_GetAttrString(PyImport_ImportModule("scipy.signal"), "find_peaks");

    if (PyType_Ready(&ZCurveSeqType) < 0 ||
        PyType_Ready(&GCProfileType) < 0 ||
        PyType_Ready(&OriFinderType) < 0)
        return NULL;
    
    zcurvepy = PyModule_Create(&ZCurvePyModule);

    if (zcurvepy == NULL)
        return NULL;
    
    Py_INCREF(&ZCurveSeqType);
    Py_INCREF(&GCProfileType);
    Py_INCREF(&OriFinderType);

    if (!PyModule_AddObject(zcurvepy, "ZCurveSeq", (PyObject *) &ZCurveSeqType))
    if (!PyModule_AddObject(zcurvepy, "GCProfile", (PyObject *) &GCProfileType))
    // if (!PyModule_AddObject(zcurvepy, "OriFinder", (PyObject *) &OriFinderType))
        return zcurvepy;

    Py_DECREF(&ZCurveSeqType);
    Py_DECREF(&GCProfileType);
    // Py_DECREF(&OriFinderType);
    
    Py_DECREF(zcurvepy);

    return NULL;
}

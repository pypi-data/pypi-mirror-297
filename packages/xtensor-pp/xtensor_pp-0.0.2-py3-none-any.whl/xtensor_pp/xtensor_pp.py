import numpy
import re
import gdb.printing


# import debugpy
# debugpy.listen(("localhost", 5678))
# print("Waiting for debugger attach...")
# debugpy.wait_for_client()

class ShowXtensorContentParameter(gdb.Parameter):
    """
    When arma-show-content is enabled (default) the armadillo pretty-printers
    will print the elements of armadillo vectors, matrices and cubes. When
    disabled only the dimension of the container are printed.
    """

    set_doc = "Enable/disable the xtensor-show-content parameter."
    show_doc = "Show the value of xtensor-show-content"

    def __init__(self):
        # It seems that gdb.Parameter does not inherit from `object` when gdb
        # uses Python 2. Therefore, we cannot use `super` to call init.
        gdb.Parameter.__init__(self, "xtensor-show-content", gdb.COMMAND_NONE, gdb.PARAM_BOOLEAN)
        self.value = True

    def get_set_string(self):
        if self.value:
            return "xtensor-show-content is enabled"
        else:
            return "xtensor-show-content is disabled"

    def get_show_string(self, svalue):
        return "xtensor-show-content is set to {0}".format(svalue)


xtensor_show_content = ShowXtensorContentParameter()

c2numpy_type = {
    'int': numpy.int32,
    'long': numpy.int64,
    'long long': numpy.int64,
    'short': numpy.int16,
    'char': numpy.int8,

    'unsigned int': numpy.uint32,
    'unsigned long': numpy.uint64,
    'unsigned long long': numpy.uint64,
    'unsigned short': numpy.uint16,
    'unsigned char': numpy.uint8,

    'float': numpy.float32,
    'double': numpy.float64,
    'long double': numpy.float128,

    'bool': numpy.bool_,

    'void*': numpy.uint64,
    'int*': numpy.uint64,
    'char*': numpy.uint64,

    'std::string': numpy.void,
    'std::vector<int>': numpy.int32,
    'std::vector<float>': numpy.float32,
}

numpy2c_type = {
    "int32": 'int',
    "int64": 'long',
    "int16": 'short',
    "int8": 'char',
    "uint32": 'unsigned int',
    "uint64": 'unsigned long',
    "uint16": 'unsigned short',
    "uint8": 'unsigned char',
    "float32": 'float',
    "float64": 'double',
    "float128": 'long double',
    "bool": 'bool',
    "void": 'std::string',
}

allocated_pointers = {}


class XtensorPrettyPrinterBase(gdb.ValuePrinter):
    def __init__(self, val):
        self.val = val
        self.name = self.get_variable_name(val)

    def count_template_arguments(self, gdb_val):        
        count = 0
        try:
            while True:
                gdb_val.type.template_argument(count)
                count += 1
        except RuntimeError:
            pass
        return count

    def get_variable_name(self, val):
        frame = gdb.selected_frame()
        block = frame.block()
        
        for symbol in block:
            if symbol.is_variable:
                try:
                    if gdb.parse_and_eval(symbol.name) == val:
                        return str(symbol.name).strip('"')
                except gdb.error:
                    continue
        return None
    
    def xtensor_cast(self, base, shape):
        # base = "self.p_type"
        for i in range(len(shape)):
            base += ".array({0})".format(shape[-(i+1)]-1)
        return eval(base)
        
    def numpy_to_gdb_value(self, array, gdb_array_type):
        array_size = array.nbytes

        if self.name in allocated_pointers:
            gdb_memory_pointer = allocated_pointers[self.name]
        else:
            gdb_memory_pointer = gdb.parse_and_eval(f"(void*) malloc({array_size})")
            self.inferior.write_memory(int(gdb_memory_pointer), array.tobytes())
            allocated_pointers[self.name] = gdb_memory_pointer

        gdb_value_array = gdb_memory_pointer.cast(gdb_array_type.pointer()).dereference()
        return gdb_value_array

    def to_string(self):
        raise RuntimeError("Implement-me")

    # def next_element(self):
    #     raise RuntimeError("Implement-me")

    def children(self):
        raise RuntimeError("Implement-me")
        # if xtensor_show_content.value and self.is_created():
        #     return self.next_element()
        # return []

    def is_created(self):
        # if self.n_elem == self.n_rows * self.n_cols and self.n_rows != 0 and self.n_cols != 0 and self.n_elem != 0:
            return True
        # return False

    def display_hint(self):
        return "array"



class XtensorXarrayPrinter(XtensorPrettyPrinterBase):

    def __init__(self, val):
        super(XtensorXarrayPrinter, self).__init__(val)

        self.inferior = gdb.selected_inferior()

        self.m_type = self.val["m_shape"]["m_begin"].type.strip_typedefs().target()
        self.m_begin = self.val["m_shape"]["m_begin"]
        self.m_end = self.val["m_shape"]["m_end"]
        # self.m_size = (self.m_end - self.m_begin) // self.m_type.sizeof
        self.m_size = (int(self.m_end) - int(self.m_begin))
        if self.m_size > 0:
            raw_memory = self.inferior.read_memory(self.m_begin, self.m_size)
            self.shape = numpy.frombuffer(raw_memory, dtype=c2numpy_type[self.m_type.name])
        else:
            self.shape = numpy.array([], dtype=c2numpy_type[self.m_type.name])

        self.p_type = self.val["m_storage"]["p_begin"].type.strip_typedefs().target()
        self.p_begin = self.val["m_storage"]["p_begin"]
        self.p_end = self.val["m_storage"]["p_end"]
        # self.p_size = (self.p_end - self.p_begin) // self.p_type.sizeof
        self.p_size = (int(self.p_end) - int(self.p_begin))
        if self.p_size > 0:
            raw_memory = self.inferior.read_memory(self.p_begin, self.p_size)
            self.storage = numpy.frombuffer(raw_memory, dtype=c2numpy_type[self.p_type.name]).reshape(self.shape)
        else:
            self.storage = numpy.array([], dtype=c2numpy_type[self.p_type.name])

    def children(self):
        shape = tuple(map(int, self.shape))
        if self.m_size > 0 and self.p_size > 0:
            yield "m_shape", ((self.m_begin).dereference()).cast(self.m_type.array(len(shape)-1))
            yield "m_storage", ((self.p_begin).dereference()).cast(self.xtensor_cast("self.p_type", shape))
        else:
            yield "m_storage ", self.p_begin.reference_value() #((self.p_begin).dereference()).cast(self.p_type.array(0))
            
    def to_string(self):
        return "xt::xarray<{0}>{1}".format(self.p_type, self.shape)






class XtensorXviewPrinter(XtensorPrettyPrinterBase):

    def __init__(self, val):
        super(XtensorXviewPrinter, self).__init__(val)

        self.inferior = gdb.selected_inferior()

        try:
            self.v_type = self.val["m_shape"]["m_begin"].type.strip_typedefs().target()
            self.v_begin = self.val["m_shape"]["m_begin"]
            self.v_end = self.val["m_shape"]["m_end"]
        except:
            self.v_type = self.val["m_shape"]["m_sequence"]["m_begin"].type.strip_typedefs().target()
            self.v_begin = self.val["m_shape"]["m_sequence"]["m_begin"]
            self.v_end = self.val["m_shape"]["m_sequence"]["m_end"]

        # self.m_size = (self.v_end - self.v_begin) // self.v_type.sizeof
        self.m_size = (int(self.v_end) - int(self.v_begin))
        if self.m_size > 0:
            raw_memory = self.inferior.read_memory(self.v_begin, self.m_size)
            self.view_shape = numpy.frombuffer(raw_memory, dtype=c2numpy_type[self.v_type.name])
        else:
            self.view_shape = numpy.array([], dtype=c2numpy_type[self.v_type.name])

        self.slices = []
        template_count = self.count_template_arguments(self.val["m_slices"])
        tuple_val = self.val["m_slices"]
        tuple_type = tuple_val.type
        for i in range(template_count):
            template_i = tuple_type.template_argument(i)
            if not re.match("xt::xnewaxis<.+>", template_i.name):
                tuple_i = self.val["m_slices"].cast(gdb.lookup_type("std::_Head_base<{0}, {1}, false>".format(i, template_i.name)))["_M_head_impl"]
            else:
                tuple_i = self.val["m_slices"].cast(gdb.lookup_type("std::_Head_base<{0}, {1}, true>".format(i, template_i.name)))["_M_head_impl"]
            self.slices.append([template_i, tuple_i])

        ###################################################################################################################################################################
        ###################################################################################################################################################################
        self.m_type = self.val["m_e"]["m_shape"]["m_begin"].type.strip_typedefs().target()
        self.m_begin = self.val["m_e"]["m_shape"]["m_begin"]
        self.m_end = self.val["m_e"]["m_shape"]["m_end"]
        # self.m_size = (self.m_end - self.m_begin) // self.m_type.sizeof
        self.m_size = (int(self.m_end) - int(self.m_begin))
        if self.m_size > 0:
            raw_memory = self.inferior.read_memory(self.m_begin, self.m_size)
            self.shape = numpy.frombuffer(raw_memory, dtype=c2numpy_type[self.m_type.name])
        else:
            self.shape = numpy.array([], dtype=c2numpy_type[self.m_type.name])


        self.p_type = self.val["m_e"]["m_storage"]["p_begin"].type.strip_typedefs().target()
        self.p_begin = self.val["m_e"]["m_storage"]["p_begin"]
        self.p_end = self.val["m_e"]["m_storage"]["p_end"]
        # self.p_size = (self.p_end - self.p_begin) // self.p_type.sizeof
        self.p_size = (int(self.p_end) - int(self.p_begin))
        if self.p_size > 0:
            raw_memory = self.inferior.read_memory(self.p_begin, self.p_size)
            self.storage = numpy.frombuffer(raw_memory, dtype=c2numpy_type[self.p_type.name]).reshape(self.shape)
        else:
            self.storage = numpy.array([], dtype=c2numpy_type[self.p_type.name])
        ###################################################################################################################################################################
        ###################################################################################################################################################################

    def view_cast(self, base, shape):
        # base = "self.p_type"
        for i in range(len(shape)):
            base += ".array({0})".format(shape[-(i+1)]-1)
        return eval(base)

    def children(self):
        slice2np = ""
        for i, _slice in enumerate(self.slices):
            if slice2np != "": slice2np += ", "

            if re.match("xt::xrange<.+>", _slice[0].name):
                m_start = _slice[1]["m_start"]
                m_size = int(_slice[1]["m_size"])

                slice2np += "{0}:{1}".format(m_start, m_start + m_size)
            elif re.match("xt::xstepped_range<.+>", _slice[0].name):
                m_start = _slice[1]["m_start"]
                m_size = int(_slice[1]["m_size"])
                m_step = int(_slice[1]["m_step"])

                slice2np += "{0}:{1}:{2}".format(m_start, m_start + m_size, m_step)
            elif re.match("xt::xall<.+>", _slice[0].name):
                m_size = int(_slice[1]["m_size"])

                slice2np += ":"
            elif re.match("xt::xkeep_slice<.+>", _slice[0].name):
                m_type = _slice[1]["m_indices"]["m_begin"].type.strip_typedefs().target()
                m_begin = _slice[1]["m_indices"]["m_begin"]
                m_end = _slice[1]["m_indices"]["m_end"]
                m_size = (int(m_end) - int(m_begin))
                m_data = _slice[1]["m_indices"]["m_data"]

                raw_memory = self.inferior.read_memory(m_begin, m_size)
                m_keep = numpy.frombuffer(raw_memory, dtype=c2numpy_type[m_type.name])

                slice2np += "[" + ",".join(map(str, m_keep)) + "]"
            elif re.match("xt::xdrop_slice<.+>", _slice[0].name):
                m_type = _slice[1]["m_indices"]["m_begin"].type.strip_typedefs().target()
                m_begin = _slice[1]["m_indices"]["m_begin"]
                m_end = _slice[1]["m_indices"]["m_end"]
                m_size = (int(m_end) - int(m_begin))
                m_data = _slice[1]["m_indices"]["m_data"]

                raw_memory = self.inferior.read_memory(m_begin, m_size)
                m_drop = numpy.frombuffer(raw_memory, dtype=c2numpy_type[m_type.name])

                slice2np += "[" + ",".join(map(str, numpy.delete(range(self.shape[i]), m_drop))) + "]"
            elif re.match("xt::xnewaxis<.+>", _slice[0].name):
                slice2np += "numpy.newaxis"

        slice2np = "[" + slice2np + "]"

        self.np_array = eval("self.storage" + slice2np)
        gdb_array_type = self.view_cast("gdb.lookup_type(numpy2c_type[str(self.np_array.dtype)])", self.np_array.shape)
        gdb_value = self.numpy_to_gdb_value(self.np_array, gdb_array_type)

        shape = tuple(map(int, self.view_shape))
        yield "v_shape", ((self.v_begin).dereference()).cast(self.v_type.array(len(shape)-1))
        yield "v_storage", gdb_value
            
    def to_string(self):
        return "" # "{0}{1}".format(self.p_type, self.shape)





pp = gdb.printing.RegexpCollectionPrettyPrinter('xtensor')
pp.add_printer('xt::xarray', '^xt::xarray', XtensorXarrayPrinter)
pp.add_printer('xt::xview', '^xt::xview', XtensorXviewPrinter)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, replace=True)

# https://pymotw.com/3/json/index.html#encoding-and-decoding-simple-data-types
import json
import io

# json_compact_encoding.py
data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))  # DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('repr(data)             :', len(repr(data)))  # repr(data)             : 35
plain_dump = json.dumps(data)
print('dumps(data)            :', len(plain_dump))  # dumps(data)            : 35
small_indent = json.dumps(data, indent=2)
print('dumps(data, indent=2)  :', len(small_indent))  # dumps(data, indent=2)  : 73
with_separators = json.dumps(data, separators=(',', ':'))
print('dumps(data, separators):', len(with_separators))  # dumps(data, separators): 29


# json_skipkeys
data = [{'a': 'A', 'b': (2, 4), 'c': 3.0, ('d',): 'D tuple'}]

print('First attempt')
try:
    print(json.dumps(data))
except TypeError as err:
    print('ERROR:', err)  # ERROR: keys must be str, int, float, bool or None, not tuple

print()
print('Second attempt')
print(json.dumps(data, skipkeys=True))  # [{"a": "A", "b": [2, 4], "c": 3.0}]

# Working with custom types
import json_myobj

obj = json_myobj.MyObj('instance value goes here')

print('First attempt')
try:
    print(json.dumps(obj))
except TypeError as err:
    print('ERROR:', err)


def convert_to_builtin_type(obj):
    print('default(', repr(obj), ')')
    # Convert objects to a dictionary of their representation
    d = {
        '__class__': obj.__class__.__name__,
        '__module__': obj.__module__,
    }
    d.update(obj.__dict__)
    return d


print()
print('With default')
print(json.dumps(obj, default=convert_to_builtin_type))
# {"__class__": "MyObj", "__module__": "json_myobj", "s": "instance value goes here"}

# To decode the results and create a MyObj() instance, use the object_hook argument to loads() to tie in to the decoder
# so the class can be imported from the module and used to create the instance.


def dict_to_object(d):
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        print('MODULE:', module.__name__)
        class_ = getattr(module, class_name)
        print('CLASS:', class_)
        args = {
            key: value
            for key, value in d.items()
        }
        print('INSTANCE ARGS:', args)
        inst = class_(**args)
    else:
        inst = d
    return inst


encoded_object = '''
    [{"s": "instance value goes here",
      "__module__": "json_myobj", "__class__": "MyObj"}]
    '''

myobj_instance = json.loads(
    encoded_object,
    object_hook=dict_to_object,
)
print(myobj_instance)
# MODULE: json_myobj
# CLASS: <class 'json_myobj.MyObj'>
# INSTANCE ARGS: {'s': 'instance value goes here'}
# [<MyObj(instance value goes here)>]

# Since json converts string values to unicode objects,
# they need to be re-encoded as ASCII strings before they can be used as keyword arguments to the class constructor.
# Similar hooks are available for the built-in types integers (parse_int), floating point numbers (parse_float),
# and constants (parse_constant).

# Encoder and Decoder Classes
# Using the classes directly gives access to extra APIs for customizing their behavior.
# The JSONEncoder uses an iterable interface for producing “chunks” of encoded data,
# making it easier to write to files or network sockets without having to represent an entire data structure in memory.

encoder = json.JSONEncoder()
data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

for part in encoder.iterencode(data):
    print('PART:', part)

# The encode() method is basically equivalent to ''.join(encoder.iterencode()), with some extra error checking up front.
# To encode arbitrary objects,
# override the default() method with an implementation similar to the one used in convert_to_builtin_type().


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        print('default(', repr(obj), ')')
        # Convert objects to a dictionary of their representation
        d = {
            '__class__': obj.__class__.__name__,
            '__module__': obj.__module__,
        }
        d.update(obj.__dict__)
        return d


obj = json_myobj.MyObj('internal data')
print(obj)
print(MyEncoder().encode(obj))
# The output is the same as the previous implementation.


class MyDecoder(json.JSONDecoder):

    def __init__(self):
        json.JSONDecoder.__init__(
            self,
            object_hook=self.dict_to_object,
        )

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            print('MODULE:', module.__name__)
            class_ = getattr(module, class_name)
            print('CLASS:', class_)
            args = {
                key: value
                for key, value in d.items()
            }
            print('INSTANCE ARGS:', args)
            inst = class_(**args)
        else:
            inst = d
        return inst


encoded_object = '''
[{"s": "instance value goes here",
  "__module__": "json_myobj", "__class__": "MyObj"}]
'''

myobj_instance = MyDecoder().decode(encoded_object)
print(myobj_instance)
# And the output is the same as the earlier example.

# Working with Streams and Files
# With large data structures, it may be preferable to write the encoding directly to a file-like object.
data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

f = io.StringIO()
json.dump(data, f)

print(f.getvalue())

# Although it is not optimized to read only part of the data at a time,
# the load() function still offers the benefit of encapsulating the logic of generating objects from stream input.

f = io.StringIO('[{"a": "A", "c": 3.0, "b": [2, 4]}]')
print(json.load(f))
# Just as for dump(), any file-like object can be passed to load().
# [{'a': 'A', 'c': 3.0, 'b': [2, 4]}]

# Mixed Data Streams
# JSONDecoder includes raw_decode(), a method for decoding a data structure followed by more data,
# such as JSON data with trailing text.
# The return value is the object created by decoding the input data,
# and an index into that data indicating where decoding left off.
decoder = json.JSONDecoder()


def get_decoded_and_remainder(input_data):
    obj, end = decoder.raw_decode(input_data)
    remaining = input_data[end:]
    return (obj, end, remaining)


encoded_object = '[{"a": "A", "c": 3.0, "b": [2, 4]}]'
extra_text = 'This text is not JSON.'

print('JSON first:')
data = ' '.join([encoded_object, extra_text])
obj, end, remaining = get_decoded_and_remainder(data)

print('Object              :', obj)
print('End of parsed input :', end)
print('Remaining text      :', repr(remaining))

print()
print('JSON embedded:')
try:
    data = ' '.join([extra_text, encoded_object, extra_text])
    obj, end, remaining = get_decoded_and_remainder(data)
except ValueError as err:
    print('ERROR:', err)
# Unfortunately, this only works if the object appears at the beginning of the input.


# JSON first:
# Object              : [{'a': 'A', 'c': 3.0, 'b': [2, 4]}]
# End of parsed input : 35
# Remaining text      : ' This text is not JSON.'

# JSON embedded:
# ERROR: Expecting value: line 1 column 1 (char 0)

# JSON at the Command Line
# [{"a": "A", "c": 3.0, "b": [2, 4]}]

# $ python3 -m json.tool example.json
#
# [
#     {
#         "a": "A",
#         "c": 3.0,
#         "b": [
#             2,
#             4
#         ]
#     }
# ]
#
# $ python3 -m json.tool --sort-keys example.json
#
# [
#     {
#         "a": "A",
#         "b": [
#             2,
#             4
#         ],
#         "c": 3.0
#     }
# ]
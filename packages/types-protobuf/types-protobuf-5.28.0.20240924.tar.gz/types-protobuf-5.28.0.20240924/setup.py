from setuptools import setup

name = "types-protobuf"
description = "Typing stubs for protobuf"
long_description = '''
## Typing stubs for protobuf

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`protobuf`](https://github.com/protocolbuffers/protobuf) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`protobuf`.

This version of `types-protobuf` aims to provide accurate annotations
for `protobuf==5.28.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/protobuf. All fixes for
types and metadata should be contributed there.

Partially generated using [mypy-protobuf==3.6.0](https://github.com/nipunn1313/mypy-protobuf/tree/v3.6.0) and libprotoc 26.1 on [protobuf v28.2](https://github.com/protocolbuffers/protobuf/releases/tag/v28.2) (python `protobuf==5.28.2`).

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`9f033bf439e064917e4b235b8a09b7530f182516`](https://github.com/python/typeshed/commit/9f033bf439e064917e4b235b8a09b7530f182516) and was tested
with mypy 1.11.1, pyright 1.1.381, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="5.28.0.20240924",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/protobuf.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['google-stubs'],
      package_data={'google-stubs': ['protobuf/__init__.pyi', 'protobuf/any_pb2.pyi', 'protobuf/api_pb2.pyi', 'protobuf/compiler/__init__.pyi', 'protobuf/compiler/plugin_pb2.pyi', 'protobuf/descriptor.pyi', 'protobuf/descriptor_pb2.pyi', 'protobuf/descriptor_pool.pyi', 'protobuf/duration_pb2.pyi', 'protobuf/empty_pb2.pyi', 'protobuf/field_mask_pb2.pyi', 'protobuf/internal/__init__.pyi', 'protobuf/internal/api_implementation.pyi', 'protobuf/internal/builder.pyi', 'protobuf/internal/containers.pyi', 'protobuf/internal/decoder.pyi', 'protobuf/internal/encoder.pyi', 'protobuf/internal/enum_type_wrapper.pyi', 'protobuf/internal/extension_dict.pyi', 'protobuf/internal/message_listener.pyi', 'protobuf/internal/python_message.pyi', 'protobuf/internal/type_checkers.pyi', 'protobuf/internal/well_known_types.pyi', 'protobuf/internal/wire_format.pyi', 'protobuf/json_format.pyi', 'protobuf/message.pyi', 'protobuf/message_factory.pyi', 'protobuf/reflection.pyi', 'protobuf/service.pyi', 'protobuf/source_context_pb2.pyi', 'protobuf/struct_pb2.pyi', 'protobuf/symbol_database.pyi', 'protobuf/text_format.pyi', 'protobuf/timestamp_pb2.pyi', 'protobuf/type_pb2.pyi', 'protobuf/util/__init__.pyi', 'protobuf/wrappers_pb2.pyi', 'METADATA.toml', 'protobuf/py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

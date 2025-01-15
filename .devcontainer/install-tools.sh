#!/bin/sh

# Install dev dependencies:
python3 -m pip install qgis-stubs

# Patch in additional type hints
cat << EOF | sed -i '/class Commands(BaseCommands, ABC)/r /dev/stdin' /usr/local/lib/python3.12/dist-packages/pydapper/commands.py
    
    # begin type hint patch
    @overload
    def query(
        self, sql: str, param: Optional["ParamType"] = ..., buffered: "Literal[True]" = True, *, model: Callable[..., "_T"]
    ) -> List["_T"]:
        ...
    # end type hint patch

EOF

cat << EOF | sed -i '/class ConnectionType/r /dev/stdin' /usr/local/lib/python3.12/dist-packages/pydapper/types.py

    # begin type hint patch
    @abstractmethod
    def close(self):
        ...
    # end type hint patch

EOF

# Install any additional tools, e.g.:
# apt update && apt install -y iputils-ping curl

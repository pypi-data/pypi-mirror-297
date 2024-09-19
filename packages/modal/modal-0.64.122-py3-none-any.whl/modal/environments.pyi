import modal.client
import modal_proto.api_pb2
import typing
import typing_extensions

class __delete_environment_spec(typing_extensions.Protocol):
    def __call__(self, name: str, client: typing.Optional[modal.client.Client] = None): ...
    async def aio(self, *args, **kwargs): ...

delete_environment: __delete_environment_spec

class __update_environment_spec(typing_extensions.Protocol):
    def __call__(
        self,
        current_name: str,
        *,
        new_name: typing.Optional[str] = None,
        new_web_suffix: typing.Optional[str] = None,
        client: typing.Optional[modal.client.Client] = None,
    ): ...
    async def aio(self, *args, **kwargs): ...

update_environment: __update_environment_spec

class __create_environment_spec(typing_extensions.Protocol):
    def __call__(self, name: str, client: typing.Optional[modal.client.Client] = None): ...
    async def aio(self, *args, **kwargs): ...

create_environment: __create_environment_spec

class __list_environments_spec(typing_extensions.Protocol):
    def __call__(
        self, client: typing.Optional[modal.client.Client] = None
    ) -> typing.List[modal_proto.api_pb2.EnvironmentListItem]: ...
    async def aio(self, *args, **kwargs) -> typing.List[modal_proto.api_pb2.EnvironmentListItem]: ...

list_environments: __list_environments_spec

def ensure_env(environment_name: typing.Optional[str] = None) -> str: ...

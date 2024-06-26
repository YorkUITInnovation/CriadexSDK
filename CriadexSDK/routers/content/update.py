from CriadexSDK.routers.content.upload import GroupContentUploadRoute


class GroupContentUpdateRoute(GroupContentUploadRoute):
    ENDPOINT: str = "update"
    METHOD: str = "_patch"

from .utils import get_app_instance


class AppConfigMixin:
    """
    This mixin must be attached to any class-based views used which implements AppHookConfig.

    It provides:
    * current namespace in self.namespace
    * namespace configuration in self.config
    * current application in the `current_app` context variable
    """

    def dispatch(self, request, *args, **kwargs):
        self.namespace, self.config = get_app_instance(request)
        request.current_app = self.namespace
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if "current_app" in response_kwargs:  # pragma: no cover
            response_kwargs["current_app"] = self.namespace
        return super().render_to_response(context, **response_kwargs)

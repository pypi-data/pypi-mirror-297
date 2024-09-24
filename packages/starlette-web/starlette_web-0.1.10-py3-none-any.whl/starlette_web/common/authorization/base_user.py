class BaseUserMixin:
    # Contrary to django's AbstractBaseUser, this is not bound to DB,
    # therefore a mixin
    username_field = None

    @property
    def is_authenticated(self) -> bool:
        raise NotImplementedError


class AnonymousUser(BaseUserMixin):
    @property
    def is_authenticated(self) -> bool:
        return False

import uuid
from dataclasses import asdict

import services.user.layer_models as layer_models
import services.user.payload_models as payload_models
import services.user.repositories.protocol as protocol
import sqlalchemy.exc as sqlalch_exc
import utils.exceptions as exc
from api.v1.utils import Pagination
from db import session_scope
from models import AllowedDevice, Permission, Role, RolePermission, RoleUser, Session, SocialAccount, User

DEFAULT_USER_ROLE = 'User'


class UserSqlalchemyRepository(protocol.UserRepositoryProtocol):
    def get_by_id(self, user_id: uuid.UUID) -> layer_models.User:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            raise exc.NotFoundError
        return layer_models.User.from_orm(user)

    def get_by_email(self, email: str) -> layer_models.User:
        user = User.query.filter(User.email == email).first()
        if user is None:
            raise exc.NotFoundError
        return layer_models.User.from_orm(user)

    def get_multi(self, filters: protocol.UserFilter | None = None) -> list[layer_models.User]:
        users = User.query
        if filters:
            for filter_name, filter_value in asdict(filters).items():
                model_attribute = getattr(User, filter_name, None)
                if model_attribute is not None:
                    users = users.filter(model_attribute == filter_value)

        return [layer_models.User.from_orm(user) for user in users.all()]

    def create(self, user: payload_models.UserCreatePayload) -> layer_models.User:
        new_user = User(**user.dict())
        role = Role.query.filter(Role.name == DEFAULT_USER_ROLE).first()
        try:
            with session_scope() as db_session:
                db_session.add(new_user)
                db_session.flush()
                role_user = RoleUser(user_id=new_user.id, role_id=role.id)
                db_session.add(role_user)
                return layer_models.User.from_orm(new_user)
        except sqlalch_exc.IntegrityError as ex:
            raise exc.UniqueConstraintError from ex

    def update(self, user_id: uuid.UUID, new_user: payload_models.UserUpdatePayload) -> layer_models.User:
        try:
            with session_scope():
                user = User.query.filter(User.id == user_id)
                if user.count() != 1:
                    raise exc.NotFoundError
                user.update(new_user.dict(exclude_none=True))
        except sqlalch_exc.IntegrityError as ex:
            raise exc.UniqueConstraintError from ex
        return layer_models.User.from_orm(user.first())

    def delete(self, user_id: uuid.UUID) -> layer_models.User | None:
        with session_scope():
            user = User.query.filter(User.id == user_id)
            if user.count() != 1:
                raise exc.NotFoundError
            user = user.first()
            user.cond_delete()
        return layer_models.User.from_orm(user)

    def add_allowed_device(self, device: payload_models.UserDevicePayload) -> layer_models.UserDevice:
        new_device = AllowedDevice(**device.dict())
        try:
            with session_scope() as db_session:
                db_session.add(new_device)
                db_session.flush()
                return layer_models.UserDevice.from_orm(new_device)
        except sqlalch_exc.IntegrityError as ex:
            raise exc.UniqueConstraintError from ex

    def get_allowed_device(self, device: payload_models.UserDevicePayload) -> layer_models.UserDevice:
        device = AllowedDevice.query.filter(
            AllowedDevice.user_id == device.user_id,
            AllowedDevice.user_agent == device.user_agent,
        )
        if device.count() == 0:
            raise exc.NotFoundError
        return layer_models.UserDevice.from_orm(device.first())

    def get_allowed_devices(self, user_id: uuid.UUID) -> list[layer_models.UserDevice]:
        devices = AllowedDevice.query.filter(
            AllowedDevice.user_id == user_id,
        ).all()
        return [layer_models.UserDevice.from_orm(device) for device in devices]

    def get_history(self, user_id: uuid.UUID, paginate: Pagination) -> list[layer_models.Session]:
        user_histories = (
            Session.query.filter(
                Session.user_id == user_id,
            )
            .paginate(paginate.page, paginate.size, False)
            .items
        )
        return [layer_models.Session.from_orm(user_history) for user_history in user_histories]

    def add_new_session(self, session: payload_models.SessionPayload) -> layer_models.Session:
        new_session = Session(**session.dict())
        with session_scope() as db_session:
            db_session.add(new_session)
            db_session.flush()
            return layer_models.Session.from_orm(new_session)

    def get_user_permissions(self, user_id: uuid.UUID) -> list[layer_models.Permission]:
        query = Permission.query
        query = query.join(RolePermission).join(RoleUser, RoleUser.role_id == RolePermission.role_id)
        permissions = query.filter(RoleUser.user_id == user_id).all()
        return [layer_models.Permission.from_orm(permission) for permission in permissions]

    def get_user_roles(self, user_id: uuid.UUID) -> list[layer_models.Role]:
        user_roles = Role.query.join(RoleUser).filter(RoleUser.user_id == user_id).all()
        return [layer_models.Role.from_orm(role) for role in user_roles]

    def add_role_for_user(self, user_id: uuid.UUID, role_id: uuid.UUID) -> None:
        role_user = RoleUser(role_id=role_id, user_id=user_id)
        try:
            with session_scope() as session:
                session.add(role_user)
        except sqlalch_exc.IntegrityError as ex:
            if exc.INTEGRITY_KEY_DIDNT_EXIST_MSG in str(ex):
                raise exc.NotFoundError from ex
            if exc.INTEGRITY_UNIQUE_CONSTRAINT_MSG in str(ex):
                raise exc.UniqueConstraintError from ex

    def delete_role_from_user(self, user_id: uuid.UUID, role_id: uuid.UUID) -> None:
        role_user = RoleUser.query.filter(RoleUser.user_id == user_id, RoleUser.role_id == role_id)
        if role_user.count() != 1:
            raise exc.NotFoundError
        with session_scope():
            role_user.update({'is_deleted': True})

    def create_social_account(self, social_account: payload_models.SocialAccountPayload) -> layer_models.SocialAccount:
        _social_account = SocialAccount(**social_account.dict())
        try:
            with session_scope() as session:
                session.add(_social_account)
                session.flush()
                return layer_models.SocialAccount.from_orm(_social_account)
        except sqlalch_exc.IntegrityError as ex:
            raise exc.UniqueConstraintError from ex

    def get_social_account(self, social_id: str, social_name: str) -> layer_models.SocialAccount:
        _social_account = SocialAccount.query.filter(
            SocialAccount.social_id == social_id,
            SocialAccount.social_name == social_name,
        ).first()
        if _social_account is None:
            raise exc.NotFoundError
        return layer_models.SocialAccount.from_orm(_social_account)

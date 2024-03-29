from db.db import db
from models.utils import BaseModel
from sqlalchemy.dialects.postgresql import UUID


class Permission(BaseModel):
    __tablename__ = 'permissions'
    protected = db.Column(db.Boolean(), nullable=False, default=False)
    name = db.Column(db.String(length=150), unique=True, nullable=False)
    code = db.Column(db.INTEGER, unique=True, nullable=False, index=True)
    description = db.Column(db.String(length=150), nullable=False)

    def __repr__(self) -> str:
        return f'Permission: {self.name} {self.id}'


class RolePermission(BaseModel):
    __tablename__ = 'roles_permissions'
    __table_args__ = (db.UniqueConstraint('perm_id', 'role_id'), {'schema': 'auth'})
    perm_id = db.Column(UUID(as_uuid=True), db.ForeignKey('auth.permissions.id'), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('auth.roles.id'), nullable=False)

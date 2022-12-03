"""partition

Revision ID: 0d26c28bc852
Revises: 0c62fa30dc0b
Create Date: 2022-11-10 13:54:58.288526

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0d26c28bc852'
down_revision = '0c62fa30dc0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('allowed_device_user_id_fkey', 'allowed_device', type_='foreignkey')
    op.create_foreign_key(
        None, 'allowed_device', 'users', ['user_id'], ['id'], source_schema='auth', referent_schema='auth'
    )
    op.drop_constraint('roles_permissions_perm_id_fkey', 'roles_permissions', type_='foreignkey')
    op.drop_constraint('roles_permissions_role_id_fkey', 'roles_permissions', type_='foreignkey')
    op.create_foreign_key(
        None, 'roles_permissions', 'roles', ['role_id'], ['id'], source_schema='auth', referent_schema='auth'
    )
    op.create_foreign_key(
        None, 'roles_permissions', 'permissions', ['perm_id'], ['id'], source_schema='auth', referent_schema='auth'
    )
    op.drop_constraint('sessions_user_id_fkey', 'sessions', type_='foreignkey')
    op.drop_constraint('sessions_device_id_fkey', 'sessions', type_='foreignkey')
    op.create_foreign_key(
        None, 'sessions', 'allowed_device', ['device_id'], ['id'], source_schema='auth', referent_schema='auth'
    )
    op.create_foreign_key(None, 'sessions', 'users', ['user_id'], ['id'], source_schema='auth', referent_schema='auth')
    op.create_unique_constraint(None, 'social_account', ['id'], schema='auth')
    op.drop_constraint('social_account_user_id_fkey', 'social_account', type_='foreignkey')
    op.create_foreign_key(
        None, 'social_account', 'users', ['user_id'], ['id'], source_schema='auth', referent_schema='auth'
    )
    op.create_unique_constraint(None, 'user_info', ['id', 'country'], schema='auth')
    op.drop_constraint('user_info_user_id_fkey', 'user_info', type_='foreignkey')
    op.create_foreign_key(None, 'user_info', 'users', ['user_id'], ['id'], source_schema='auth', referent_schema='auth')
    op.drop_constraint('users_roles_role_id_fkey', 'users_roles', type_='foreignkey')
    op.drop_constraint('users_roles_user_id_fkey', 'users_roles', type_='foreignkey')
    op.create_foreign_key(
        None, 'users_roles', 'roles', ['role_id'], ['id'], source_schema='auth', referent_schema='auth'
    )
    op.create_foreign_key(
        None, 'users_roles', 'users', ['user_id'], ['id'], source_schema='auth', referent_schema='auth'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_roles', schema='auth', type_='foreignkey')
    op.drop_constraint(None, 'users_roles', schema='auth', type_='foreignkey')
    op.create_foreign_key('users_roles_user_id_fkey', 'users_roles', 'users', ['user_id'], ['id'])
    op.create_foreign_key('users_roles_role_id_fkey', 'users_roles', 'roles', ['role_id'], ['id'])
    op.drop_constraint(None, 'user_info', schema='auth', type_='foreignkey')
    op.create_foreign_key('user_info_user_id_fkey', 'user_info', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'user_info', schema='auth', type_='unique')
    op.drop_constraint(None, 'social_account', schema='auth', type_='foreignkey')
    op.create_foreign_key('social_account_user_id_fkey', 'social_account', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'social_account', schema='auth', type_='unique')
    op.drop_constraint(None, 'sessions', schema='auth', type_='foreignkey')
    op.drop_constraint(None, 'sessions', schema='auth', type_='foreignkey')
    op.create_foreign_key('sessions_device_id_fkey', 'sessions', 'allowed_device', ['device_id'], ['id'])
    op.create_foreign_key('sessions_user_id_fkey', 'sessions', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'roles_permissions', schema='auth', type_='foreignkey')
    op.drop_constraint(None, 'roles_permissions', schema='auth', type_='foreignkey')
    op.create_foreign_key('roles_permissions_role_id_fkey', 'roles_permissions', 'roles', ['role_id'], ['id'])
    op.create_foreign_key('roles_permissions_perm_id_fkey', 'roles_permissions', 'permissions', ['perm_id'], ['id'])
    op.drop_constraint(None, 'allowed_device', schema='auth', type_='foreignkey')
    op.create_foreign_key('allowed_device_user_id_fkey', 'allowed_device', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###

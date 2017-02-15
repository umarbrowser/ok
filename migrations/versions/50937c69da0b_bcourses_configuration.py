"""bCourses configuration

Revision ID: 50937c69da0b
Revises: 0c98b865104f
Create Date: 2016-11-14 20:16:39.879837

"""

# revision identifiers, used by Alembic.
revision = '50937c69da0b'
down_revision = '0c98b865104f'

from alembic import op
import sqlalchemy as sa
import server


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('canvas_course',
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_domain', sa.String(length=255), nullable=False),
    sa.Column('external_id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(length=255), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name=op.f('fk_canvas_course_course_id_course')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_canvas_course'))
    )
    op.create_index(op.f('ix_canvas_course_course_id'), 'canvas_course', ['course_id'], unique=False)
    op.create_table('canvas_assignment',
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('external_id', sa.Integer(), nullable=False),
    sa.Column('score_kinds', server.models.StringList(), nullable=False),
    sa.Column('canvas_course_id', sa.Integer(), nullable=False),
    sa.Column('assignment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['assignment_id'], ['assignment.id'], name=op.f('fk_canvas_assignment_assignment_id_assignment')),
    sa.ForeignKeyConstraint(['canvas_course_id'], ['canvas_course.id'], name=op.f('fk_canvas_assignment_canvas_course_id_canvas_course')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_canvas_assignment'))
    )
    op.create_index(op.f('ix_canvas_assignment_assignment_id'), 'canvas_assignment', ['assignment_id'], unique=False)
    op.create_index(op.f('ix_canvas_assignment_canvas_course_id'), 'canvas_assignment', ['canvas_course_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_canvas_assignment_canvas_course_id'), table_name='canvas_assignment')
    op.drop_index(op.f('ix_canvas_assignment_assignment_id'), table_name='canvas_assignment')
    op.drop_table('canvas_assignment')
    op.drop_index(op.f('ix_canvas_course_course_id'), table_name='canvas_course')
    op.drop_table('canvas_course')
    ### end Alembic commands ###
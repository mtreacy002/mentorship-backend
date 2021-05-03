"""Add BIT personal background

Revision ID: 0cfd533818e7
Revises: 1272e4b54a32
Create Date: 2021-05-03 11:36:51.484640

"""
from alembic import op
from app.database.db_types.JsonCustomType import JsonCustomType
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0cfd533818e7"
down_revision = "1272e4b54a32"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "personal_backgrounds",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "gender",
            sa.Enum(
                "FEMALE", "MALE", "OTHER", "DECLINED", "NOT_APPLICABLE", name="gender"
            ),
            nullable=True,
        ),
        sa.Column(
            "age",
            sa.Enum(
                "UNDER_18",
                "AGE_18_TO_20",
                "AGE_21_TO_24",
                "AGE_25_TO_34",
                "AGE_35_TO_44",
                "AGE_45_TO_54",
                "AGE_55_TO_64",
                "ABOVE_65_YO",
                "DECLINED",
                "NOT_APPLICABLE",
                name="age",
            ),
            nullable=True,
        ),
        sa.Column(
            "ethnicity",
            sa.Enum(
                "AFRICAN_AMERICAN",
                "CAUCASIAN",
                "HISPANIC",
                "NATIVE_AMERICAN",
                "MIDDLE_EASTERN",
                "ASIAN",
                "OTHER",
                "DECLINED",
                "NOT_APPLICABLE",
                name="ethnicity",
            ),
            nullable=True,
        ),
        sa.Column(
            "sexual_orientation",
            sa.Enum(
                "HETEROSEXUAL",
                "LGBTIA",
                "OTHER",
                "DECLINED",
                "NOT_APPLICABLE",
                name="sexualorientation",
            ),
            nullable=True,
        ),
        sa.Column(
            "religion",
            sa.Enum(
                "CHRISTIANITY",
                "JUDAISM",
                "ISLAM",
                "HINDUISM",
                "BUDDHISM",
                "OTHER",
                "DECLINED",
                "NOT_APPLICABLE",
                name="religion",
            ),
            nullable=True,
        ),
        sa.Column(
            "physical_ability",
            sa.Enum(
                "WITH_DISABILITY",
                "WITHOUT_DISABILITY",
                "OTHER",
                "DECLINED",
                "NOT_APPLICABLE",
                name="physicalability",
            ),
            nullable=True,
        ),
        sa.Column(
            "mental_ability",
            sa.Enum(
                "WITH_DISORDER",
                "WITHOUT_DISORDER",
                "OTHER",
                "DECLINED",
                "NOT_APPLICABLE",
                name="mentalability",
            ),
            nullable=True,
        ),
        sa.Column(
            "socio_economic",
            sa.Enum(
                "UPPER",
                "UPPER_MIDDLE",
                "LOWER_MIDDLE",
                "WORKING",
                "BELOW_POVERTY",
                "OTHER",
                "DECLINED",
                "NOT_APPLICABLE",
                name="socioeconomic",
            ),
            nullable=True,
        ),
        sa.Column(
            "highest_education",
            sa.Enum(
                "BELOW_HIGH_SCHOOL",
                "HIGH_SCHOOL",
                "ASSOCIATE",
                "BACHELOR",
                "MASTER",
                "PHD",
                "OTHER",
                "DECLINED",
                "NOT_APPLICABLE",
                name="highesteducation",
            ),
            nullable=True,
        ),
        sa.Column(
            "years_of_experience",
            sa.Enum(
                "UNDER_ONE",
                "UP_TO_3",
                "UP_TO_5",
                "UP_TO_10",
                "OVER_10",
                "DECLINED",
                "NOT_APPLICABLE",
                name="yearsofexperience",
            ),
            nullable=True,
        ),
        sa.Column("others", JsonCustomType, nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("personal_backgrounds")
    # ### end Alembic commands ###

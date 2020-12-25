from app import db
from models import User, Image, Filter


def seed_db():
    drop_everything()
    db.create_all()

    bla = User.signup(username='bla', password='blablabla', email='bla@bla.com', image_url='')

    vintage = Filter(full_name='vintage')
    lomo = Filter(full_name='lomo')
    clarity = Filter(full_name='clarity')
    sincity = Filter(full_name='sincity')
    sunrise = Filter(full_name='sunrise')
    crossprocess = Filter(full_name='crossprocess')
    orangepeel = Filter(full_name='orangepeel')
    love = Filter(full_name='love')
    grungy = Filter(full_name='grungy')
    jarques = Filter(full_name='jarques')
    pinhole = Filter(full_name='pinhole')
    oldboot = Filter(full_name='oldboot')
    glowingsun = Filter(full_name='glowingsun')
    hazydays = Filter(full_name='hazydays')
    hermajesty = Filter(full_name='hermajesty')
    nostalgia = Filter(full_name='nostalgia')
    hemingway = Filter(full_name='hemingway')
    concentrate = Filter(full_name='concentrate')

    db.session.add_all([vintage, lomo, clarity, sincity, sunrise, crossprocess, orangepeel])
    db.session.commit()

def drop_everything():
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    ## This is here because the db doesnt always drop in the right order
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()

seed_db()
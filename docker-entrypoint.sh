#!/usr/bin/env sh
set -e

# Initialize DB schema and ensure base roles exist
python - <<'PY'
from app import app, db
from models import Role

with app.app_context():
    db.create_all()
    created = False
    for rn in ['admin', 'trainer', 'member']:
        if not Role.query.filter_by(name=rn).first():
            db.session.add(Role(name=rn, description=f'{rn.title()} role'))
            created = True
    if created:
        db.session.commit()
PY

exec "$@"



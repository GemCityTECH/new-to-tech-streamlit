import json
import logging

import model
import schema

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def create_geos(
    db: Session, geos: list[schema.Geo]
) -> list[schema.Geo]:
    for geo in geos:
        try:
            geo_model = model.Geo(
                state_name=geo.state_name,
                county=geo.county,
                city=geo.city
            )
            db.add(geo_model)
            #logger.info(f"Created geo: {geo_model}")
        except:
            logger.error(f"Failed to add {geo_model} to database")
            raise

    db.commit()
    logger.info(f"Added {len(geos)} geos to database")
    return geos

def get_geos(db: Session, skip: int = 0, limit: int = 100) -> list[schema.Geo]:
    return [
        schema.Geo.model_validate(geo_model) for geo_model in db.query(model.Geo).offset(skip).limit(limit).all()
    ]

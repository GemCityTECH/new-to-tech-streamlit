import logging

import model
import schema

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def create_geos(
    db: Session, geos: list[schema.GeoBase]
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
            logger.error(f"Failed to add {geo} to database")
            raise

    db.commit()
    logger.info(f"Added {len(geos)} geos to database")
    return get_geos(db)

def get_geos(db: Session, skip: int = 0, limit: int = 100) -> list[schema.Geo]:
    return [
        schema.Geo.model_validate(geo_model) for geo_model in db.query(model.Geo).offset(skip).limit(limit).all()
    ]

def get_geo_by_fields(db: Session, state_name: str, county: str, city: str | None) -> schema.Geo:
    db_geo = (
        db.query(model.Geo)
        .filter(
            model.Geo.state_name == state_name,
            model.Geo.county == county,
            model.Geo.city == city,
        )
        .first()
    )
    if not db_geo:
        logging.error(f"Could not retrieve geo with fields {state_name} {county} {city}")
        raise
    return schema.Geo.model_validate(db_geo)


def create_monitoring_sites(
    db: Session, monitoring_sites: list[schema.MonitoringSiteBase]
) -> list[schema.MonitoringSite]:
    for site in monitoring_sites:
        try:
            site_model = model.MonitoringSite(
                geo_id = site.geo_id,
                site_num=site.site_num,
                longitude=site.longitude,
                latitude=site.latitude
            )
            db.add(site_model)
            #logger.info(f"Created site: {site_model}")
        except:
            logger.error(f"Failed to add {site} to database")
            raise

    db.commit()
    logger.info(f"Added {len(monitoring_sites)} monitoring sites to database")
    return get_monitoring_sites(db)

def get_monitoring_sites(db: Session, skip: int = 0, limit: int = 100) -> list[schema.Geo]:
    return [
        schema.MonitoringSite.model_validate(site_model) for site_model in db.query(model.MonitoringSite).offset(skip).limit(limit).all()
    ]
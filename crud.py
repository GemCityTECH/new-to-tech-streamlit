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

def get_monitoring_site_by_fields(db: Session, site_num: int, longitude: float, latitude: float) -> schema.MonitoringSite:
    db_site = (
        db.query(model.MonitoringSite)
        .filter(
            model.MonitoringSite.site_num == site_num,
            model.MonitoringSite.longitude == longitude,
            model.MonitoringSite.latitude == latitude,
        )
        .first()
    )
    if not db_site:
        logging.error(f"Could not retrieve monitoring site with fields {site_num} {longitude} {latitude}")
        raise
    return schema.MonitoringSite.model_validate(db_site)

def create_measurements(
    db: Session, measurements: list[schema.MeasurementBase]
) -> list[schema.Measurement]:
    for measurement in measurements:
        try:
            measurement_model = model.Measurement(
                monitoring_site_id=measurement.monitoring_site_id,
                parameter_code=measurement.parameter_code,
                datum=measurement.datum,
                parameter_name=measurement.parameter_name,
                sample_duration=measurement.sample_duration,
                pollutant_standard=measurement.pollutant_standard,
                metric_used=measurement.metric_used,
                method_name=measurement.method_name,
                year=measurement.year,
                units_of_measure=measurement.units_of_measure,
                observation_count=measurement.observation_count,
                observation_percent=measurement.observation_percent,
                arithmetic_mean=measurement.arithmetic_mean,
                arithmetic_standard_dev=measurement.arithmetic_standard_dev,
                percentile_99=measurement.percentile_99,
                percentile_90=measurement.percentile_90,
            )
            db.add(measurement_model)
            #logger.info(f"Created site: {measurement_model}")
        except:
            logger.error(f"Failed to add {measurement} to database")
            raise

    db.commit()
    logger.info(f"Added {len(measurements)} measurements to database")
    return get_measurements(db)

def get_measurements(db: Session, skip: int = 0, limit: int = 100) -> list[schema.Measurement]:
    return [
        schema.Measurement.model_validate(measurement_model) for measurement_model in db.query(model.Measurement).offset(skip).limit(limit).all()
    ]

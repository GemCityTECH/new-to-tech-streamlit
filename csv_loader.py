import logging
import pandas as pd
import schema
import crud

class EPACSVLoader:
    logger = logging.getLogger(__name__)
    csv_file: str = "data/annual_conc_by_monitor_2023.csv"

    cols = [
        "State Name",
        "County Name",
        "City Name",
        "Completeness Indicator",
        "Site Num",
        "Latitude",
        "Longitude",
        "Parameter Code",
        "Datum",
        "Parameter Name",
        "Sample Duration",
        "Pollutant Standard",
        "Metric Used",
        "Method Name",
        "Year",
        "Units of Measure",
        "Observation Count",
        "Observation Percent",
        "Arithmetic Mean",
        "Arithmetic Standard Dev",
        "99th Percentile",
        "90th Percentile"
    ]

    def load_and_deserialize(self, session) -> None:
        df = self._parse_csv(self.csv_file)
        
        self._load_geos(session, df)
        self._load_monitoring_sites(session, df)
        self._load_measurements(session, df)


    def _parse_csv(self, csv_file: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(csv_file, header=0, usecols=self.cols)
            print("Sample row:")
            print(df.iloc[0])

            # TODO find a more performant way to filter the data than loading it all into memory up front
            df.drop(df[(df["Completeness Indicator"] != "Y")].index, inplace=True)

            # Drop the Completeness column - no longer needed
            df.drop(columns=["Completeness Indicator"], inplace=True)

            # Convert blank or 'NaN' fields to None
            df = df.astype(object)
            df = df.where(pd.notnull(df), None)
            
            return df
        except:
            self.logger.exception(f"Failed to parse {csv_file}")
            raise 

    def _load_geos(self, session, df: pd.DataFrame) -> list[schema.GeoBase]:
        # Disregard columns we don't care about for this operation
        geos_df = df[["State Name", "County Name", "City Name"]]

        # Grab unique geos
        geos_df = geos_df.drop_duplicates()

        geos: set[schema.GeoBase] = set()
        try:
            for index, row in df.iterrows():
                geos.add(schema.GeoBase(
                    state_name=row["State Name"],
                    county=row["County Name"],
                    city=row["City Name"],
                ))
            return crud.create_geos(session, geos)
        except:
            self.logger.exception("Failed to load geos from dataframe")
            raise

    def _load_monitoring_sites(self, session, df: pd.DataFrame) -> list[schema.MonitoringSiteBase]:
        # Disregard columns we don't care about for this operation
        sites_df = df[["State Name", "County Name", "City Name", "Site Num", "Latitude", "Longitude"]]

        # Grab unique geos
        sites_df = sites_df.drop_duplicates()

        try:
            monitoring_sites: set[schema.MonitoringSiteBase] = set()
            for index, row in df.iterrows():
                geo = crud.get_geo_by_fields(session, state_name=row["State Name"], county=row["County Name"], city=row["City Name"])
                if geo:
                    monitoring_sites.add(schema.MonitoringSiteBase(
                        geo_id=geo.id,
                        site_num=row["Site Num"],
                        latitude=row["Latitude"],
                        longitude=row["Longitude"],
                    ))
            return crud.create_monitoring_sites(session, monitoring_sites)
        except:
            self.logger.exception("Failed to load monitoring sites from dataframe")
            raise

    def _load_measurements(self, session, df: pd.DataFrame) -> list[schema.MeasurementBase]:
        try:
            measurements: list[schema.MeasurementBase] = []
            for index, row in df.iterrows():
                site = crud.get_monitoring_site_by_fields(session, site_num=row["Site Num"], latitude=row["Latitude"], longitude=row["Longitude"])
                if site:
                    measurements.append(schema.MeasurementBase(
                        monitoring_site_id=site.id,
                        parameter_code=row["Parameter Code"],
                        datum=row["Datum"],
                        parameter_name=row["Parameter Name"],
                        sample_duration=row["Sample Duration"],
                        pollutant_standard=row["Pollutant Standard"],
                        metric_used=row["Metric Used"],
                        method_name=row["Method Name"],
                        year=row["Year"],
                        units_of_measure=row["Units of Measure"],
                        observation_count=row["Observation Count"],
                        observation_percent=row["Observation Percent"],
                        arithmetic_mean=row["Arithmetic Mean"],
                        arithmetic_standard_dev=row["Arithmetic Standard Dev"],
                        percentile_99=row["99th Percentile"],
                        percentile_90=row["90th Percentile"],
                    ))
            return crud.create_measurements(session, measurements)
        except:
            self.logger.exception("Failed to load measurements from dataframe")
            raise

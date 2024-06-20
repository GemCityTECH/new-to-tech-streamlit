import logging
import pandas as pd
import schema

class EPACSVLoader:
    logger = logging.getLogger(__name__)
    csv_file: str = "data/annual_conc_by_monitor_2023.csv"

    cols = [
        "State Name",
        "County Name",
        "City Name",
        "Completeness Indicator"
    ]

    def load_and_deserialize(self) -> list[schema.Geo]:
        df = self._load_from_csv(self.csv_file)
        return self._deserialize(df)

    def _load_from_csv(self, csv_file: str) -> pd.DataFrame:
        
        try:
            df = pd.read_csv(csv_file, header=0, usecols=self.cols)
            print("Sample row:")
            print(df.iloc[0])

            # TODO find a more performant way to filter the data than loading it all into memory up front
            df.drop(df[(df["Completeness Indicator"] != "Y")].index, inplace=True)

            # Drop the Completeness column - no longer needed
            df.drop(columns=["Completeness Indicator"], inplace=True)

            # Convert blank or 'NaN' city fields to None
            df = df.astype(object)
            df = df.where(pd.notnull(df), None)

            # Grab unique geos
            df.drop_duplicates(inplace=True)
            
            return df
        except:
            self.logger.exception(f"Failed to parse {csv_file}")

    def _deserialize(self, df: pd.DataFrame) -> list[schema.Geo]:
        try:
            geos: list[schema.Geo] = []
            for index, row in df.iterrows():
                geos.append(schema.Geo(
                    state_name=row["State Name"],
                    county=row["County Name"],
                    city=row["City Name"],
                ))
            return geos
        except:
            self.logger.exception("Failed to populate database from dataframe")
            raise

import csv


class DataIngestor:
    def __init__(self, csv_path: str):
        file = open(csv_path)
        csv_reader = csv.reader(file)

        column_names = next(csv_reader)
        # Create a dictionary where the key is the column name and the value is the column index
        self.header = {key: i for i, key in enumerate(column_names)}

        self.rows = []
        for row in csv_reader:
            self.rows.append(row)
        file.close()

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily']

        self.questions_best_is_max = [
            '''Percent of adults who achieve at least 150 minutes a week of moderate-intensity
              aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic
                activity (or an equivalent combination)''',
            '''Percent of adults who achieve at least 150 minutes a week of moderate-intensity
              aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical
                activity and engage in muscle-strengthening activities on 2 or more days a week''',
            '''Percent of adults who achieve at least 300 minutes a week of
              moderate-intensity aerobic physical activity or 150 minutes a week
                of vigorous-intensity aerobic activity (or an equivalent combination)''',
            '''Percent of adults who engage in muscle-strengthening activities on 2 or more 
            days a week''',
        ]

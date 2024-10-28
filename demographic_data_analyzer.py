import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def calculate_demographic_data():
    # Load the dataset
    df = load_data("adult.data.csv")

    # Initialize the results dictionary
    results = {}

    # Calculate race count
    results['race_count'] = df['race'].value_counts().sort_index()

    # Calculate average age of men
    results['average_age_men'] = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # Calculate percentage of people with a Bachelor's degree
    bachelors_count = df[df['education'] == 'Bachelors'].shape[0]
    total_count = df.shape[0]
    results['percentage_bachelors'] = round((bachelors_count / total_count) * 100, 1)

    # Calculate percentage of people with higher education earning >50K
    advanced_degrees = ['Bachelors', 'Masters', 'Doctorate']
    advanced_count = df[df['education'].isin(advanced_degrees)]
    over_50k_count = advanced_count[advanced_count['salary'] == '>50K'].shape[0]
    results['higher_education_rich'] = round((over_50k_count / advanced_count.shape[0]) * 100, 1)

    # Calculate percentage of people without advanced education earning >50K
    non_advanced_count = df[~df['education'].isin(advanced_degrees)]
    over_50k_count_non_advanced = non_advanced_count[non_advanced_count['salary'] == '>50K'].shape[0]
    results['lower_education_rich'] = round((over_50k_count_non_advanced / non_advanced_count.shape[0]) * 100, 1)

    # Calculate minimum hours worked per week
    results['min_work_hours'] = df['hours-per-week'].min()

    # Calculate percentage of rich among those who work the minimum number of hours
    min_hours_workers = df[df['hours-per-week'] == results['min_work_hours']]
    over_50k_min_hours_count = min_hours_workers[min_hours_workers['salary'] == '>50K'].shape[0]
    results['rich_percentage'] = round((over_50k_min_hours_count / min_hours_workers.shape[0]) * 100, 1)

    # Calculate country with the highest percentage of people earning >50K
    countries = df['native-country'].unique()
    percentages = {}
    for country in countries:
        country_data = df[df['native-country'] == country]
        over_50k_count_country = country_data[country_data['salary'] == '>50K'].shape[0]
        percentages[country] = round((over_50k_count_country / country_data.shape[0]) * 100, 1) if country_data.shape[0] > 0 else 0
    
    highest_country = max(percentages, key=percentages.get)
    results['highest_earning_country'] = highest_country
    results['highest_earning_country_percentage'] = percentages[highest_country]

    # Calculate the most popular occupation for high earners in India
    india_workers = df[df['native-country'] == 'India']
    over_50k_india = india_workers[india_workers['salary'] == '>50K']
    results['top_IN_occupation'] = over_50k_india['occupation'].mode()[0] if not over_50k_india.empty else None

    return results

# This check allows the script to be run independently
if __name__ == "__main__":
    data = calculate_demographic_data()
    for key, value in data.items():
        print(f"{key}: {value}")

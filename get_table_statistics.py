from terminaltables import AsciiTable


def get_table_statistics(languages_salary, title):
    table_content = []
    table_header = ["Язык программирования", "Вакансий найдено",
                    "Вакансий обработано", "Средняя зарплата"]
    table_content.append(table_header)
    for language, statistics in languages_salary.items():
        table_content.append([language, statistics["vacancies_found"],
                              statistics["vacancies_processed"],
                              statistics["average_salary"]])
    table_instance = AsciiTable(table_content, title)
    return table_instance.table

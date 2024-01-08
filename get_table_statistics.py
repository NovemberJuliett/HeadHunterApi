from terminaltables import AsciiTable


def get_table_statistics(languages_salary, title):
    list_for_table = []
    table_header = ["Язык программирования", "Вакансий найдено",
                    "Вакансий обработано", "Средняя зарплата"]
    list_for_table.append(table_header)
    for key, value in languages_salary.items():
        list_for_table.append([key, value["vacancies_found"],
                               value["vacancies_processed"],
                               value["average_salary"]])
    table_instance = AsciiTable(list_for_table, title)
    return table_instance.table

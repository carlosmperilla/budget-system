#For shell arguments.
import argparse
#For the coloring of the separators.
from colorama import init

#For the creation of the Budget System and the addition of files.
from .budget_system import Budget
#To get spents by period.
from .spent import Spent
#To display data by period.
from .show_data import DisplayData

#To separate the displayed information.
from .show_data import separator
#To get the month by its index.
from .validators.Date import Month
#For the format of the month path.
from .settings.Config import ConfigBudget
#Type for the sector dictionary.
from .extra_types.SpentTypes import SectorsDict

def main():
    # Create a parser object
    description = """Command line for quick actions with the Budget system. 
                    Creation, addition of files and display of selected data.
                    NOTE: For more advanced uses it is recommended to execute by script instead of by shell.
                    """
    parser = argparse.ArgumentParser(description = description)

    #Subparser Files for Create and Add.
    subparsers = parser.add_subparsers(help='Files for Budget System')
    parser_a = subparsers.add_parser('Files', help='To add files to the Budget System.')
    parser_a.add_argument('budget_files', nargs= "*", type=str, help="To add files to the Budget System.")

    create_group = parser.add_argument_group('Create', "This creates the Budget System.")

    create_group.add_argument(
                        "--create", "-c",
                        nargs = 4, 
                        metavar = ("Lang", "PriceColumnName", "BaseFolder", "Action"), 
                        type = str,
                        help = ""
                        )

    add_group = parser.add_argument_group('Add', "This adds files to the Budget System.")

    add_group.add_argument(
                        "--add", "-a",
                        nargs = 2, 
                        metavar = ("BaseFolder", "Action"), 
                        type = str,
                        help = ""
                        )

    display_group = parser.add_argument_group('Display', "This displays the Budget System information.")

    display_group.add_argument(
                        "--displaytotal", "-dt",
                        action="store_true",
                        help = "This displays total data in the Budget System."
                        )
    display_group.add_argument(
                        "--displayyear", "-dy",
                        nargs = 1, 
                        metavar = ("Year"), 
                        type = str,
                        help = "This displays year data in the Budget System."
                        )
    display_group.add_argument(
                        "--displaymonth", "-dm",
                        nargs = 2, 
                        metavar = ("Year", "Month"), 
                        type = str,
                        help = "This displays month data in the Budget System"
                        )
    display_group.add_argument(
                        "--displaysector", "-ds",
                        nargs = 3, 
                        metavar = ("Year", "Month", "StoreName"), 
                        type = str,
                        help = "This displays sector data in the Budget System"
                        )
    display_group.add_argument(
                        "--displaysectordate", "-dd",
                        nargs = 4, 
                        metavar = ("Year", "Month", "StoreName", "Date"), 
                        type = str,
                        help = "This displays sector_date data in the Budget System"
                        )

    # parse the arguments from standard input
    args = parser.parse_args()


    # budgetsys --create ENG Price(USD) C:\Users\username\Documents\MyBudge COPY Files C:\Users\username\Documents\GenericFolderOne\Purchase_List_NameStoreOne_[23-04-22].csv C:\Users\username\Downloads\GenericFolderTwo\Purchase_List_NameStoretwo_[27-02-22].csv
    class Create:
        """This creates a budget system, it does not include the date format option, 
        so the standard day-month-year is used.
        To assign a format it is better to create a python script and the Budget class.
        """
        def __init__(self) -> None:
            self.lang = args.create[0]
            self.price_name = args.create[1]
            self.base_folder = args.create[2]
            self.budget_files_action = args.create[3]
            self.budget_files = args.budget_files

        def run(self) -> None:
            """This generates a Budget object and create the Budget System."""
            budget_system = Budget(
                self.base_folder, 
                self.budget_files,
                self.lang,
                self.price_name,
                self.budget_files_action
                )
            budget_system.create_budget_system()

    # budgetsys --add C:\Users\carlo\Desktop\pruebitas COPY Files C:\Users\username\Downloads\GenericFolderTwo\Purchase_List_NameStoreFour_[01-07-22].csv
    class Add:
        """This class adds files to the Budget System."""
        def __init__(self) -> None:
            self.base_folder = args.add[0]
            self.budget_files_action = args.add[1]
            self.budget_files = args.budget_files

        def run(self):
            """This generates a Budget object and adds files to the Budget System.."""
            budget_system = Budget(
                    base_folder=self.base_folder,
                    budget_files=self.budget_files,
                    budget_files_action=self.budget_files_action
                )
            budget_system.add_budget_files()


    class Show:
        """"""
        @staticmethod
        def to_month(month:str) -> str:
            """This takes a month, if it is decimal it converts it to a textual month."""
            if month.isdecimal():
                return Month().get_month_by_index(int(month))
            return month

        def __init__(self) -> None:
            init(autoreset=True)
            self.total = args.displaytotal
            self.year = args.displayyear
            self.month = args.displaymonth
            self.sector = args.displaysector
            self.sector_date = args.displaysectordate

            self.display_data = DisplayData()
            self.spent_data = Spent()
            self.month_path = ConfigBudget().MONTH_PATH

        def get_sector_dict(self, year:str, month:str, store_name:str) -> SectorsDict:
            """This gets from a store(sector) for a month."""
            month_path = self.month_path.format(year=year, month=month)
            sector_dict = self.spent_data.spending_by_sector_in_month(month_path, store_name)[0]

            return sector_dict

        # budgetsys -dt
        def show_total(self) -> None:
            """This displays total data."""
            self.display_data.show_total_data()

        # budgetsys -dy 2022
        def show_year(self) -> None:
            """This displays year data."""
            year = self.year[0]
            
            print("\n")
            self.display_data.show_year_data(
                year, 
                {
                    year : self.spent_data.spending_by_year(year)
                }
                )

        # budgetsys -dm 2022 April
        # budgetsys -dm 2022 4
        @separator("END")
        def show_month(self) -> None:
            """This displays month data."""
            year, month = self.month
            month = self.to_month(month)

            month_data = self.spent_data.spending_by_month(year, month)
            
            print("\n")
            self.display_data.show_month_data(month, {month: month_data})
        

        # budgetsys -ds 2022 April StoreOne
        # budgetsys -ds 2022 4 StoreOne
        @separator("BEGIN")
        @separator("END")
        def show_sector(self) -> None:
            """This displays store(sector) data."""
            year, month, store_name = self.sector
            month = self.to_month(month)

            sector_dict = self.get_sector_dict(year, month, store_name)
            
            print("\n")
            self.display_data.show_sector_data(store_name, sector_dict)


        # budgetsys -ds 2022 April StoreOne 23-04-22
        # budgetsys -ds 2022 4 StoreOne 23-04-22
        @separator("BEGIN")
        @separator("END")
        def show_sector_date(self) -> None:
            """This displays date store(sector) data."""
            year, month, store_name, buy_date = self.sector_date
            month = self.to_month(month)
            
            sector_dict = self.get_sector_dict(year, month, store_name)

            buy_date_data = {
                                buy_date : sector_dict[store_name][buy_date]
                            }
            
            self.display_data.show_date_data(buy_date, buy_date_data)

        def run(self):
            if self.total:
                self.show_total()
            if self.year:
                self.show_year()
            if self.month:
                self.show_month()
            if self.sector:
                print("\n")
                self.show_sector()
            if self.sector_date:
                print("\n")
                self.show_sector_date()

    if args.create:
        Create().run()

    if args.add:
        Add().run()

    displayers = [
        args.displaytotal,
        args.displayyear,
        args.displaymonth,
        args.displaysector,
        args.displaysectordate
    ]

    #If any of the displayers were defined then it shows them.
    if any(displayers):
        Show().run()

if __name__ == '__main__':
    main()

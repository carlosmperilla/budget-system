# Budget System

The Budget System allows you to manage dataframe data with store purchase budgets by date.

- It groups the relevant information, the most expensive and the cheapest products in a table.
- Spents per store purchase on a date, per store in a month, per month, per year and total spent.
- It shows this information segmented and colored, both by python code, and by a **command line** application to facilitate visualization.
- The system can be created relatively easily, starting from the budget files, copying them (_by default_) or moving them, as indicated.
- It has a translation system to be able to integrate languages beyond English or Spanish, for the months and the display in your language.
- Cross-platform compatibility.

### Dependencies
Budget System requires three external dependencies.
- [Pandas][pandas install]
 It is to manage the tables through dataframes.
- [Colorama][colorama install]
 It is to color the visualization by console.
- [Numpy][numpy install]
 It is for type float64.

### Instalation
```sh
pip install budget-system
```

## Introduction
### Pre-requirements
* The csv files with the purchase data must have at least one column with the prices of each product.
* The names of each table must have the following format to be identified by the package and correctly located in the Budget System folder tree:
 **whatever_storename_[day-month-year].csv**
    * Example:
     **Purchase_List_Amazon_[14-05-22].csv**
        * Note:
        _There is one subtle exception_: the **date format** can be changed if you want, before creating the **Budget System**. But this option is **not available on the command line**. But in the python script creation format. Please read further if this is what you require.
### Creation
* #### Complete script to create a Budget System:
   ```python
  from budget_system import Budget

  budget_files = [
	    r"C:\Users\username\Documents\GenericFolderOne\Purchase_List_NameStoreOne_[23-04-22].csv",
	    r"C:\Users\username\Downloads\GenericFolderTwo\Purchase_List_NameStoretwo_[27-02-22].csv",
	    r"C:\Users\username\Desktop\GenericFolderThree\Purchase_List_NameStoreThree_[23-05-23].csv",
	    ]
  context = {
    	"lang" : "ENG",
	    "price_name" : "Price(USD)",
        "base_folder" : r"C:\Users\username\Documents\MyBudget",
        "budget_files" : budget_files,
        "budget_files_action" : "COPY",
        "date_format" : "%d-%m-%y"
    }
    ```
    * The original files can be located in different folders.
    * By default, only two languages are available: **English (ENG)** and **Spanish (SPA)**. For other languages see the Translation section.
    * If a language is not specified, it will check if the operating system is configured by default in Spanish or English and choose one of these. Otherwise, it will choose **English as the default language**.
    * **_price_name_** refers to the name of the column that contains the prices.
    * **_base_folder_** refers to the path of the folder that will contain the **Budget System**. If the path does not exist, it creates it.
    * **_budget_files_action_** refers to the action that is carried out with the original files, this can be _MOVE_ or _COPY_. If not specified, the files will be copied.
    * **_date_format_** sets the _date format_, to know how to parse the dates that have the names of the files in square brackets. If not specified, defaults to **day-month-year**. [More about date formats in Python][date format python].
* #### Command line for create a Budget System:
   ```sh
  budgetsys --create ENG Price(USD) C:\Users\username\Documents\MyBudge COPY Files C:\Users\username\Documents\GenericFolderOne\Purchase_List_NameStoreOne_[23-04-22].csv C:\Users\username\Downloads\GenericFolderTwo\Purchase_List_NameStoretwo_[27-02-22].csv
   ```
   * **-\-create** can be reduced to **-c** .
   * The arguments are required, **not optional**. In order they are _Language, Price_Name, Base_Folder, Budget_File_Action_.
   * **Files** indicates that the following are the paths to the **original budget files**
   * Note that there is no option for date format. This is because the command line is meant for quick actions. **To set date format, use a python script and import Budget**.
### Addition Files




[pandas install]: https://pypi.org/project/pandas/
[colorama install]: https://pypi.org/project/colorama/
[numpy install]: https://pypi.org/project/numpy/
[date format python]: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes


